import re
import json
from datetime import datetime, timedelta
import pytz
from dateutil import parser
from ms_graph_helper import get_users, send_email, get_meetings, create_event, delete_event, update_event
from bedrock_agent import invoke_bedrock

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

def prompt_attendees(token, names):
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
        email = selected_user.get("mail") or selected_user.get("userPrincipalName")
        attendees.append({
            "email": email,
            "name": selected_user["displayName"]
        })
    return attendees

def send_email_flow(command, token):
    # parse recipient name after "send email to "
    match = re.search(r"send email to (.+)", command)
    if not match:
        print("🤖 Could not find recipient. Try: send email to [name]")
        return True
    names = [n.strip().capitalize() for n in re.split(r"and|,", match.group(1))]
    attendees = prompt_attendees(token, names)
    if not attendees:
        print("❌ No valid recipients found.")
        return True
    to_email = attendees[0]["email"]
    print(f"✉️ Preparing to send email to {attendees[0]['name']} ({to_email})")
    subject = input("📜 Enter subject: ").strip()
    body = input("📝 Enter body: ").strip()
    confirm = input(f"✅ Confirm send email to {attendees[0]['name']}? (yes/no): ").strip().lower()
    if confirm == "yes":
        success = send_email(token, to_email, subject, body)
        if success:
            print("✅ Email sent successfully.")
        else:
            print("❌ Failed to send email.")
    else:
        print("❌ Email sending canceled.")
    return True

def schedule_meeting(command, token):
    name_match = re.search(r"with (.+?) at", command)
    time_match = re.search(r"at ([\d: ]+(?:am|pm))", command)
    if not name_match or not time_match:
        print("🤖 I couldn't understand who to invite or the time. Please say like: schedule meeting with Ajay at 3pm")
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

    attendees = prompt_attendees(token, names)
    if not attendees:
        print("❌ No valid attendees found.")
        return True

    subject = input("📜 Enter meeting subject: ").strip()
    confirm = input(f"✅ Confirm schedule meeting with {', '.join(a['name'] for a in attendees)} at {meeting_time.strftime('%I:%M %p')} IST? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("❌ Meeting scheduling canceled.")
        return True

    event_body = {
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
    success = create_event(token, event_body)
    if success:
        print(f"✅ Meeting scheduled successfully.")
    else:
        print("❌ Failed to schedule meeting.")
    return True

def delete_meeting_flow(token):
    term = input("🗑️ Enter subject or name to delete: ").strip().lower()
    now = datetime.now(IST)
    start = now.replace(hour=0, minute=0, second=0, microsecond=0).astimezone(pytz.utc).isoformat()
    end = (now + timedelta(days=30)).replace(hour=23, minute=59, second=59, microsecond=999999).astimezone(pytz.utc).isoformat()
    events = get_meetings(token, start, end)
    for event in events:
        subject = event.get("subject", "").lower()
        attendees = [a.get("emailAddress", {}).get("name", "").lower() for a in event.get("attendees", [])]
        if term in subject or any(term in a for a in attendees):
            confirm = input(f"❗ Confirm delete meeting '{event.get('subject')}'? (yes/no): ").strip().lower()
            if confirm == "yes":
                if delete_event(token, event['id']):
                    print(f"✅ Deleted meeting: {event.get('subject')}")
                else:
                    print("❌ Failed to delete meeting.")
                return True
            else:
                print("❌ Deletion canceled.")
                return True
    print("❌ No matching meeting found.")
    return True

def update_meeting_flow(token):
    term = input("✏️ Enter subject or name to update: ").lower()
    now = datetime.now(IST)
    start = now.replace(hour=0, minute=0, second=0, microsecond=0).astimezone(pytz.utc).isoformat()
    end = (now + timedelta(days=30)).replace(hour=23, minute=59, second=59, microsecond=999999).astimezone(pytz.utc).isoformat()
    events = get_meetings(token, start, end)
    for event in events:
        subject = event.get("subject", "").lower()
        attendees = [a['emailAddress']['name'].lower() for a in event.get("attendees", [])]
        if term in subject or any(term in a for a in attendees):
            time_input = input("🕒 Enter new time (e.g., 3:30pm): ").strip().lower()
            time_obj = parse_time_string(time_input)
            if not time_obj:
                print("❌ Invalid time format.")
                return True
            now_local = datetime.now(IST)
            new_start = now_local.replace(hour=time_obj.hour, minute=time_obj.minute, second=0, microsecond=0).astimezone(pytz.utc)
            new_end = new_start + timedelta(hours=1)
            new_subject = input("📝 Enter new subject: ").strip()
            confirm = input(f"✅ Confirm update meeting '{event.get('subject')}'? (yes/no): ").strip().lower()
            if confirm != "yes":
                print("❌ Update canceled.")
                return True
            patch_data = {
                "start": {"dateTime": new_start.isoformat(), "timeZone": "UTC"},
                "end": {"dateTime": new_end.isoformat(), "timeZone": "UTC"},
                "subject": new_subject,
            }
            if update_event(token, event['id'], patch_data):
                print("✅ Meeting updated.")
            else:
                print("❌ Failed to update meeting.")
            return True
    print("❌ No matching meeting found.")
    return True

def list_meetings_flow(token, days=0, label="today"):
    now = datetime.now(IST)
    if days == 0:
        start = now.replace(hour=0, minute=0, second=0, microsecond=0).astimezone(pytz.utc)
        end = now.replace(hour=23, minute=59, second=59, microsecond=999999).astimezone(pytz.utc)
    else:
        start = now.astimezone(pytz.utc)
        end = (now + timedelta(days=days)).astimezone(pytz.utc)
    events = get_meetings(token, start.isoformat(), end.isoformat())
    if not events:
        print(f"🤖 No meetings found for {label}.")
        return True
    print(f"📅 Your meetings for {label}:")
    for e in events:
        start_time = convert_utc_to_ist(e["start"]["dateTime"])
        subj = e.get("subject", "No subject")
        print(f"- {start_time}: {subj}")
    return True

def main():
    print("🤖 Welcome to your Microsoft Graph Personal Assistant")
    token = read_access_token()
    if not token:
        return

    print("Type 'exit' or 'quit' to end the assistant.")

    while True:
        command = input("\n👉 You: ").lower().strip()

        if command in ["exit", "quit"]:
            print("🤖 Goodbye!")
            break

        if "send email to" in command:
            send_email_flow(command, token)
        elif "schedule meeting" in command or "create meeting" in command:
            schedule_meeting(command, token)
        elif "delete meeting" in command or "cancel meeting" in command:
            delete_meeting_flow(token)
        elif "update meeting" in command or "reschedule meeting" in command:
            update_meeting_flow(token)
        elif "list meetings today" in command:
            list_meetings_flow(token, 0, "today")
        elif "list meetings tomorrow" in command:
            list_meetings_flow(token, 1, "tomorrow")
        elif "list meetings this week" in command or "list meetings for a week" in command:
            list_meetings_flow(token, 7, "this week")
        else:
            # fallback to bedrock AI for open queries
            response = invoke_bedrock(command)
            print("🤖 AI:", response)

if __name__ == "__main__":
    main()

