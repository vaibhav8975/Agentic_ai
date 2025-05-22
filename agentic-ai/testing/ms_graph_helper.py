import requests

GRAPH_API_ENDPOINT = "https://graph.microsoft.com/v1.0"

def get_users(token, name):
    url = f"{GRAPH_API_ENDPOINT}/users?$filter=startswith(displayName,'{name}')"
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        return res.json().get("value", [])
    return []

def send_email(token, to_email, subject, body):
    url = f"{GRAPH_API_ENDPOINT}/me/sendMail"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    email_msg = {
        "message": {
            "subject": subject,
            "body": {
                "contentType": "Text",
                "content": body,
            },
            "toRecipients": [
                {"emailAddress": {"address": to_email}}
            ],
        },
        "saveToSentItems": "true"
    }
    res = requests.post(url, headers=headers, json=email_msg)
    return res.status_code == 202  # Accepted

def get_meetings(token, start, end):
    url = f"{GRAPH_API_ENDPOINT}/me/calendarView?startDateTime={start}&endDateTime={end}"
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        return res.json().get("value", [])
    return []

def create_event(token, event):
    url = f"{GRAPH_API_ENDPOINT}/me/events"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    res = requests.post(url, headers=headers, json=event)
    return res.status_code == 201

def delete_event(token, event_id):
    url = f"{GRAPH_API_ENDPOINT}/me/events/{event_id}"
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.delete(url, headers=headers)
    return res.status_code == 204

def update_event(token, event_id, patch_data):
    url = f"{GRAPH_API_ENDPOINT}/me/events/{event_id}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    res = requests.patch(url, headers=headers, json=patch_data)
    return res.status_code == 200

