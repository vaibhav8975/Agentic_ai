# ms_graph_helper.py
import requests

GRAPH_URL = "https://graph.microsoft.com/v1.0"

def get_users(token, name):
    url = f"{GRAPH_URL}/users?$filter=startswith(displayName,'{name}')&$select=displayName,mail,userPrincipalName"
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        return resp.json().get("value", [])
    else:
        print("❌ Failed to fetch users:", resp.text)
        return []

def schedule_event(token, subject, start, end, attendee_email, attendee_name):
    url = f"{GRAPH_URL}/me/events"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {
        "subject": subject,
        "start": {"dateTime": start, "timeZone": "Asia/Kolkata"},
        "end": {"dateTime": end, "timeZone": "Asia/Kolkata"},
        "attendees": [
            {
                "emailAddress": {
                    "address": attendee_email,
                    "name": attendee_name
                },
                "type": "required"
            }
        ]
    }
    resp = requests.post(url, headers=headers, json=data)
    return resp.status_code == 201, resp.text

