import re
import json
import requests
import pytz
from dateutil import parser
from ms_graph_helper import get_users
from bedrock_agent import invoke_bedrock
from datetime import datetime, timedelta
 
TOKEN_FILE = "token.txt"
IST = pytz.timezone("Asia/Kolkata")
 
def read_access_token():
    try:
        with open(TOKEN_FILE, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        print("❌ Access token file not found. Please run ms_login first.")
        return None
 
def convert_utc_to_ist(utc_time_str):
    utc_dt = datetime.fromisoformat(utc_time_str.replace("Z", "+00:00"))
    ist_dt = utc_dt.astimezone(IST)
    return ist_dt.strftime("%Y-%m-%d %I:%M %p")
 
def parse_time_string(time_str):
    try:
        return parser.parse(time_str).time()
    except Exception:
        return None
 
def get_events(token, day_offset=0):
    now = datetime.now(IST) + timedelta(days=day_offset)
    local_midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    local_end = local_midnight.replace(hour=23, minute=59, second=59)
 
    start = local_midnight.astimezone(pytz.utc).isoformat().replace('+00:00', 'Z')
    end = local_end.astimezone(pytz.utc).isoformat().replace('+00:00', 'Z')
 
    url = f"https://graph.microsoft.com/v1.0/me/calendarView?startDateTime={start}&endDateTime={end}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Prefer": 'outlook.timezone="UTC"',
    }
 
    response = requests.get(url, headers=headers)
    return response.json().get("value", []) if response.status_code == 200 else []
 
def list_meetings(events, label):
    if not events:
        print(f"📅 You have no meetings scheduled for {label}.")
    else:
        print(f"📅 You have {len(events)} meeting(s) {label}:")
        for event in events:
            start = convert_utc_to_ist(event['start']['dateTime'])
            subject = event.get("subject", "No Subject")
            attendees = [a['emailAddress']['name'] for a in event.get("attendees", [])]
            print(f"🔸 {subject} at {start} with {', '.join(attendees)}")
 
def schedule_meeting(command, token):
    name_match = re.search(r"with (.+?) at", command)
    time_match = re.search(r"at ([\d: ]+(?:am|pm))", command)
 
    if not name_match or not time_match:
        print("🤖 Buddy: I couldn't understand who to invite or the time.")
        return True
 
    names = [n.strip().capitalize() for n in re.split(r"and|,", name_match.group(1))]
    time_input = time_match.group(1).replace(" ", "").lower()
    time_obj = parse_time_string(time_input)
 
    if not time_obj:
        print("❌ Invalid time format. Please try again with a valid time like 3pm or 14:00.")
        return True
 
    now = datetime.now(IST)
    meeting_time = now.replace(hour=time_obj.hour, minute=time_obj.minute, second=0, microsecond=0)
    if "tomorrow" in command:
        meeting_time += timedelta(days=1)
    end_time = meeting_time + timedelta(hours=1)
 
    attendees = []
    for name in names:
        print(f"🔍 Searching for users named '{name}'...")
        matches = get_users(token, name)
 
        if not matches:
            print(f"❌ No matching users found for '{name}'.")
            continue
 
        if len(matches) == 1:
            selected_user = matches[0]
        else:
            print("🔎 Multiple matches found:")
            for i, user in enumerate(matches, 1):
                print(f"{i}. {user['displayName']} ({user['mail'] or user['userPrincipalName']})")
            try:
                choice = int(input("👉 Choose the user number to invite: "))
                selected_user = matches[choice - 1]
            except Exception:
                print("❌ Invalid choice.")
                continue
 
        email = selected_user["mail"] or selected_user["userPrincipalName"]
        attendees.append({
            "email": email,
            "name": selected_user["displayName"]
        })
 
    if not attendees:
        print("❌ No valid attendees found.")
        return True
 
    subject = input("📜 Enter meeting subject: ")
 
    body = {
        "subject": subject,
        "start": {
            "dateTime": meeting_time.astimezone(pytz.utc).isoformat(),
            "timeZone": "UTC"
        },
        "end": {
            "dateTime": end_time.astimezone(pytz.utc).isoformat(),
            "timeZone": "UTC"
        },
        "attendees": [{
            "emailAddress": {
                "address": a["email"],
                "name": a["name"]
            },
            "type": "required"
        } for a in attendees],
        "isOnlineMeeting": True,
        "onlineMeetingProvider": "teamsForBusiness"
    }
 
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
 
    res = requests.post("https://graph.microsoft.com/v1.0/me/events", headers=headers, data=json.dumps(body))
    if res.status_code == 201:
        print(f"✅ Meeting scheduled with {', '.join(a['name'] for a in attendees)} at {meeting_time.strftime('%I:%M %p')} IST.")
    elif res.status_code == 401:
        print("🔐 Token may be expired. Please re-authenticate.")
    else:
        print("❌ Failed to schedule meeting:", res.text)
 
    return True
 
def delete_meeting(token, match_term):
    events = get_events(token, 0)
    for event in events:
        subject = event.get("subject", "").lower()
        attendees = [a.get("emailAddress", {}).get("name", "").lower() for a in event.get("attendees", [])]
        if match_term.lower() in subject or any(match_term.lower() in a for a in attendees):
            delete_url = f"https://graph.microsoft.com/v1.0/me/events/{event['id']}"
            headers = { "Authorization": f"Bearer {token}" }
            response = requests.delete(delete_url, headers=headers)
            if response.status_code == 204:
                return True, f"Deleted meeting: {subject}"
            else:
                return False, f"Failed to delete: {response.text}"
    return False, "No matching meeting found."
 
def update_meeting(token):
    events = get_events(token, 0)
    term = input("✏️ Enter subject or name to update: ").lower()
    for event in events:
        subject = event.get("subject", "").lower()
        attendees = [a['emailAddress']['name'].lower() for a in event.get("attendees", [])]
        if term in subject or any(term in a for a in attendees):
            time_input = input("🕒 Enter new time (e.g., 3:30pm): ").strip().lower()
            time_obj = parse_time_string(time_input)
            if not time_obj:
                print("❌ Invalid time format.")
                return
            now = datetime.now(IST)
            new_start = now.replace(hour=time_obj.hour, minute=time_obj.minute, second=0, microsecond=0).astimezone(pytz.utc)
            new_end = new_start + timedelta(hours=1)
            new_subject = input("📝 Enter new subject: ")
            patch_data = {
                "start": {"dateTime": new_start.isoformat(), "timeZone": "UTC"},
                "end": {"dateTime": new_end.isoformat(), "timeZone": "UTC"},
                "subject": new_subject,
            }
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            }
            url = f"https://graph.microsoft.com/v1.0/me/events/{event['id']}"
            res = requests.patch(url, headers=headers, data=json.dumps(patch_data))
            if res.status_code == 200:
                print("✅ Meeting updated.")
            else:
                print("❌ Failed to update meeting:", res.text)
            return
    print("❌ No matching meeting found.")
 
def handle_command(command, token):
    command = command.lower()
    if "schedule" in command and "meeting" in command:
        return schedule_meeting(command, token)
    elif "today" in command and "meeting" in command:
        events = get_events(token, 0)
        list_meetings(events, "today")
        return True
    elif "tomorrow" in command and "meeting" in command:
        events = get_events(token, 1)
        list_meetings(events, "tomorrow")
        return True
    elif "delete" in command and "meeting" in command:
        term = input("🗑️ Enter subject or name to delete: ").strip()
        success, msg = delete_meeting(token, term)
        print(f"{'✅' if success else '❌'} {msg}")
        return True
    elif "update" in command and "meeting" in command:
        update_meeting(token)
        return True
    else:
        reply = invoke_bedrock(command)
        print(f"🤖 {reply}")
        return True
 
if __name__ == "__main__":
    token = read_access_token()
    if not token:
        exit()
    print("👋 Hello! I'm your assistant. Type a command or 'exit' to quit.")
    while True:
        command = input("You: ")
        if command.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break
        handle_command(command, token)
