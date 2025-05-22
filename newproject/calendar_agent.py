# calendar_agent.py

class CalendarAgent:
    def __init__(self):
        # Example event storage, in real you connect to calendar API
        self.events = [
            {
                "id": "1",
                "subject": "demo of agentic ai",
                "start": {"dateTime": "2025-05-14T09:30:00.0000000"},
                "end": {"dateTime": "2025-05-14T10:30:00.0000000"},
                "attendees": []
            },
            # Add more sample events as needed
        ]

    def list_events(self):
        return {"value": self.events}

    def create_event(self, title, start_datetime, end_datetime, attendees):
        # Simple append example, normally API call to create event
        new_event = {
            "id": str(len(self.events) + 1),
            "subject": title,
            "start": {"dateTime": start_datetime.isoformat(), "timeZone": "UTC"},
            "end": {"dateTime": end_datetime.isoformat(), "timeZone": "UTC"},
            "attendees": attendees
        }
        self.events.append(new_event)
        return new_event

    def find_events_by_subject(self, subject):
        # Simple case-insensitive substring match
        return [e for e in self.events if subject.lower() in e['subject'].lower()]

    def update_event(self, event_id, update_payload):
        for ev in self.events:
            if ev["id"] == event_id:
                ev.update(update_payload)
                return ev
        raise Exception("Event not found")

    def delete_event(self, event_id):
        for i, ev in enumerate(self.events):
            if ev["id"] == event_id:
                del self.events[i]
                return True
        raise Exception("Event not found")

