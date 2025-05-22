import re
import json
import requests
import pytz
from dateutil import parser
from datetime import datetime, timedelta

TOKEN_FILE = 'token.txt'
LOCAL_TZ = pytz.timezone('Asia/Kolkata')

def read_token():
    with open(TOKEN_FILE, 'r') as f:
        return f.read().strip()

def get_events(token, day_offset=0):
    now = datetime.now(LOCAL_TZ) + timedelta(days=day_offset)
    local_midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    local_end = local_midnight.replace(hour=23, minute=59, second=59)

    start = local_midnight.astimezone(pytz.utc).isoformat().replace('+00:00', 'Z')
    end = local_end.astimezone(pytz.utc).isoformat().replace('+00:00', 'Z')

    url = f"https://graph.microsoft.com/v1.0/me/calendarview?startdatetime={start}&enddatetime={end}"
    headers = {
        'Authorization': 'Bearer ' + token,
        'Prefer': 'outlook.timezone="Asia/Kolkata"',
        'Content-Type': 'application/json'
    }
    params = {
        '$orderby': 'start/dateTime',
        '$top': '50'
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        print("Failed to fetch events:", response.text)
        return []
    return response.json().get('value', [])

def find_meeting_by_term(events, match_term):
    for event in events:
        subject = event.get('subject', '')
        attendees = event.get('attendees', [])
        if match_term.lower() in subject.lower() or any(
            match_term.lower() in attendee.get('emailAddress', {}).get('name', '').lower()
            for attendee in attendees
        ):
            return event
    return None

def update_meeting(token, match_term, new_subject=None, new_start=None, new_end=None, add_emails=None, remove_emails=None):
    events = []
    for offset in range(7):
        events.extend(get_events(token, offset))

    event = find_meeting_by_term(events, match_term)
    if not event:
        return "No matching meeting found."

    event_id = event.get('id')
    if not event_id:
        return "Event ID not found."

    current_attendees = event.get('attendees', [])
    current_emails = [a['emailAddress']['address'] for a in current_attendees]

    final_attendees = set(current_emails)
    if add_emails:
        final_attendees.update([e.strip() for e in add_emails])
    if remove_emails:
        final_attendees.difference_update([e.strip() for e in remove_emails])

    update_body = {}
    if new_subject:
        update_body['subject'] = new_subject
    if new_start:
        update_body['start'] = {"dateTime": new_start, "timeZone": "Asia/Kolkata"}
    if new_end:
        update_body['end'] = {"dateTime": new_end, "timeZone": "Asia/Kolkata"}
    if final_attendees:
        update_body['attendees'] = [
            {
                "emailAddress": {"address": email, "name": email.split('@')[0]},
                "type": "required"
            } for email in final_attendees
        ]

    url = f"https://graph.microsoft.com/v1.0/me/events/{event_id}"
    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
    }
    response = requests.patch(url, headers=headers, json=update_body)
    if response.status_code == 200:
        return "✅ Meeting updated successfully."
    else:
        return f"❌ Failed to update meeting: {response.text}"

def delete_meeting(token, match_term):
    events = []
    for offset in range(7):
        events.extend(get_events(token, offset))

    event = find_meeting_by_term(events, match_term)
    if not event:
        return "No matching meeting found."

    event_id = event.get('id')
    if not event_id:
        return "Event ID not found."

    url = f"https://graph.microsoft.com/v1.0/me/events/{event_id}"
    headers = {
        'Authorization': 'Bearer ' + token
    }
    response = requests.delete(url, headers=headers)
    if response.status_code == 204:
        return "✅ Meeting deleted successfully."
    else:
        return f"❌ Failed to delete meeting: {response.text}"

# 🔍 Simulated AI agent with intent classification
def invoke_bedrock(user_input):
    # Simulated intent recognition logic (replace this with actual Bedrock call)
    user_input = user_input.lower()
    if "meeting" in user_input and ("list" in user_input or "show" in user_input):
        return json.dumps({"intent": "get_meetings"})
    elif "delete" in user_input:
        return json.dumps({"intent": "delete_meeting", "meeting_name": "shreya"})
    elif "update" in user_input:
        return json.dumps({
            "intent": "update_meeting",
            "meeting_name": "team sync",
            "new_subject": "Updated Sync",
            "new_start": "2025-05-20T10:00:00",
            "new_end": "2025-05-20T11:00:00",
            "add_emails": ["john@example.com"],
            "remove_emails": []
        })
    else:
        # General question fallback
        return json.dumps({
            "intent": "general_question",
            "question": user_input
        })

def process_user_query(token, user_input):
    response = invoke_bedrock(user_input)

    try:
        parsed = json.loads(response) if isinstance(response, str) else response
    except json.JSONDecodeError:
        return "❌ Sorry, I couldn't understand the response from the AI."

    intent = parsed.get("intent")

    if intent == "get_meetings":
        events = get_events(token)
        if not events:
            return "📅 You have no meetings scheduled for today."
        reply = "📅 Today's meetings:\n"
        for e in events:
            start = parser.isoparse(e['start']['dateTime']).strftime("%I:%M %p")
            subject = e.get("subject", "No Subject")
            reply += f"- {start}: {subject}\n"
        return reply

    elif intent == "delete_meeting":
        return delete_meeting(token, parsed.get("meeting_name"))

    elif intent == "update_meeting":
        return update_meeting(
            token,
            parsed.get("meeting_name"),
            new_subject=parsed.get("new_subject"),
            new_start=parsed.get("new_start"),
            new_end=parsed.get("new_end"),
            add_emails=parsed.get("add_emails"),
            remove_emails=parsed.get("remove_emails")
        )

    elif intent == "general_question":
        question = parsed.get("question", "")
        return f"🧠 Here's a response to your general question: '{question}'\n👉 Pune is a city in Maharashtra, India, known for its educational institutions, IT industry, and cultural heritage."

    else:
        return "❓ Sorry, I couldn't understand what action to perform."

if __name__ == "__main__":
    token = read_token()
    print("🧠 Welcome to AI Calendar Assistant!")
    while True:
        user_input = input("\n💬 Ask me anything about your meetings or a question (type 'exit' to quit): ")
        if user_input.lower() in ["exit", "quit"]:
            print("👋 Goodbye! Have a great day!")
            break
        result = process_user_query(token, user_input)
        print(result)

