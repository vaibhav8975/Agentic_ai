import requests
from datetime import datetime, timedelta
import pytz

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

def update_meeting(token):
    match_term = input("Enter meeting name to update: ")
    events = []
    for offset in range(7):
        events.extend(get_events(token, offset))

    print("Fetched events for update:")
    for e in events:
        print(f" - {e.get('subject','No Subject')}")

    event = find_meeting_by_term(events, match_term)
    if not event:
        print("No matching meeting found.")
        return

    event_id = event.get('id')
    if not event_id:
        print("Event ID not found.")
        return

    # Gather update inputs
    new_subject = input("Enter new meeting subject (or press Enter to skip): ").strip()
    new_start_time = input("Enter new start time (YYYY-MM-DDTHH:MM:SS or press Enter to skip): ").strip()
    new_end_time = input("Enter new end time (YYYY-MM-DDTHH:MM:SS or press Enter to skip): ").strip()

    current_attendees = event.get('attendees', [])
    current_emails = [a['emailAddress']['address'] for a in current_attendees]

    print(f"Current attendees: {', '.join(current_emails) if current_emails else 'None'}")

    add_people = input("Enter email(s) to add (comma-separated or leave blank): ").strip().split(",") if input("Do you want to add people? (yes/no): ").lower() == "yes" else []
    remove_people = input("Enter email(s) to remove (comma-separated or leave blank): ").strip().split(",") if input("Do you want to remove people? (yes/no): ").lower() == "yes" else []

    final_attendees = set(current_emails)
    final_attendees.update([p.strip() for p in add_people if p.strip()])
    final_attendees.difference_update([p.strip() for p in remove_people if p.strip()])

    print("\n📝 Summary of Changes:")
    print(f"- Subject     : {new_subject or event.get('subject')}")
    print(f"- Start Time  : {new_start_time or event['start']['dateTime']}")
    print(f"- End Time    : {new_end_time or event['end']['dateTime']}")
    print(f"- Attendees   : {', '.join(final_attendees) if final_attendees else 'None'}")

    confirm = input("\nProceed with update? (yes/no): ")
    if confirm.lower() != "yes":
        print("Update cancelled.")
        return

    update_body = {}
    if new_subject:
        update_body['subject'] = new_subject
    if new_start_time:
        update_body['start'] = {"dateTime": new_start_time, "timeZone": "Asia/Kolkata"}
    if new_end_time:
        update_body['end'] = {"dateTime": new_end_time, "timeZone": "Asia/Kolkata"}
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
        print("✅ Meeting updated successfully.")
    else:
        print(f"❌ Failed to update meeting: {response.text}")

def delete_meeting(token):
    match_term = input("Enter meeting name to delete: ")
    events = []
    for offset in range(7):
        events.extend(get_events(token, offset))

    print("Fetched events for delete:")
    for e in events:
        print(f" - {e.get('subject','No Subject')}")

    event = find_meeting_by_term(events, match_term)
    if not event:
        print("No matching meeting found.")
        return

    confirm = input(f"Are you sure you want to delete meeting '{event.get('subject')}'? (yes/no): ")
    if confirm.lower() != "yes":
        print("Delete cancelled.")
        return

    event_id = event.get('id')
    if not event_id:
        print("Event ID not found.")
        return

    url = f"https://graph.microsoft.com/v1.0/me/events/{event_id}"
    headers = {
        'Authorization': 'Bearer ' + token
    }
    response = requests.delete(url, headers=headers)
    if response.status_code == 204:
        print("✅ Meeting deleted successfully.")
    else:
        print(f"❌ Failed to delete meeting: {response.text}")

if __name__ == "__main__":
    token = read_token()
    update_meeting(token)
    delete_meeting(token)

