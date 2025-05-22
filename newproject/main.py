from bedrock_agent import BedrockAgent
from calendar_agent import CalendarAgent
import dateparser
from datetime import timedelta

def prompt_user(prompt):
    return input(prompt).strip()

def main():
    bedrock = BedrockAgent()
    calendar = CalendarAgent()

    print("Hello! I'm your personal assistant for managing your Outlook calendar. How can I help you today? (Type 'exit' to quit)")

    while True:
        user_input = prompt_user("You: ")
        if user_input.lower() in ['exit', 'quit']:
            print("Assistant: Goodbye! Have a great day.")
            break

        try:
            # Get intent and entities from Bedrock LLM
            result = bedrock.get_intent_entities(user_input)
            intent = result.get("intent")
            entities = result.get("entities", {})

        except Exception:
            # In case of any failure in intent detection
            print("Assistant: Sorry, I didn't quite get that. Could you please rephrase?")
            continue

        # Only handle calendar-related intents
        calendar_intents = {
            "list_calendar_events",
            "create_calendar_event", "schedule_meeting",
            "update_calendar_event", "update_meeting",
            "delete_calendar_event", "delete_meeting"
        }

        if intent not in calendar_intents:
            # Friendly fallback for unsupported intents
            print("Assistant: I’m here to help with your Outlook calendar — scheduling, listing, updating, or deleting events. How can I assist you with your calendar?")
            continue

        # Process calendar intents
        if intent == "list_calendar_events":
            events = calendar.list_events()
            if not events.get("value"):
                print("Assistant: You have no upcoming events.")
            else:
                print("Assistant: Here are your upcoming events:")
                for ev in events["value"]:
                    print(f"- {ev['subject']} at {ev['start']['dateTime']}")
            continue

        if intent in ["create_calendar_event", "schedule_meeting"]:
            title = entities.get("title") or entities.get("contact_name") or prompt_user("Assistant: What’s the title of the event? ")
            time_str = entities.get("time") or prompt_user("Assistant: When should the event start? Please specify date and time. ")
            start_dt = dateparser.parse(time_str)
            if not start_dt:
                print("Assistant: Sorry, I couldn't understand the time you provided.")
                continue
            end_dt = start_dt + timedelta(minutes=30)

            attendees_str = prompt_user("Assistant: Please provide attendee emails separated by commas (or leave blank): ")
            attendees = []
            if attendees_str:
                emails = [e.strip() for e in attendees_str.split(",") if e.strip()]
                attendees = [{"emailAddress": {"address": email}, "type": "required"} for email in emails]

            try:
                event = calendar.create_event(title, start_dt, end_dt, attendees)
                print(f"Assistant: Your event '{event['subject']}' has been scheduled for {event['start']['dateTime']}.")
            except Exception as e:
                print(f"Assistant: Sorry, I couldn't create the event due to an error: {e}")
            continue

        if intent in ["update_calendar_event", "update_meeting"]:
            subject = entities.get("title") or prompt_user("Assistant: Which event would you like to update? Please provide the event title or keyword: ")
            matches = calendar.find_events_by_subject(subject)
            if not matches:
                print("Assistant: I couldn't find any events matching that description.")
                continue

            if len(matches) > 1:
                print("Assistant: I found multiple events. Please select one to update:")
                for idx, ev in enumerate(matches, 1):
                    print(f"{idx}. {ev['subject']} at {ev['start']['dateTime']}")
                choice = prompt_user("Assistant: Enter the number of the event: ")
                try:
                    idx = int(choice) - 1
                    event_to_update = matches[idx]
                except (ValueError, IndexError):
                    print("Assistant: That's not a valid choice.")
                    continue
            else:
                event_to_update = matches[0]

            print(f"Assistant: Selected '{event_to_update['subject']}' scheduled for {event_to_update['start']['dateTime']}.")

            update_type = prompt_user("Assistant: What would you like to update? (title/time/attendees): ").lower()

            update_payload = {}

            if update_type == "time":
                new_time_str = prompt_user("Assistant: Please enter the new start time: ")
                new_start = dateparser.parse(new_time_str)
                if not new_start:
                    print("Assistant: I couldn't understand that time.")
                    continue
                orig_start = dateparser.parse(event_to_update['start']['dateTime'])
                orig_end = dateparser.parse(event_to_update['end']['dateTime'])
                duration = orig_end - orig_start
                new_end = new_start + duration
                update_payload["start"] = {"dateTime": new_start.isoformat(), "timeZone": "UTC"}
                update_payload["end"] = {"dateTime": new_end.isoformat(), "timeZone": "UTC"}

            elif update_type == "title":
                new_title = prompt_user("Assistant: Please enter the new title: ")
                update_payload["subject"] = new_title

            elif update_type == "attendees":
                emails_str = prompt_user("Assistant: Please enter the updated attendee emails separated by commas: ")
                emails = [e.strip() for e in emails_str.split(",") if e.strip()]
                update_payload["attendees"] = [{"emailAddress": {"address": email}, "type": "required"} for email in emails]

            else:
                print("Assistant: Sorry, I can't update that field right now.")
                continue

            try:
                updated_event = calendar.update_event(event_to_update["id"], update_payload)
                print(f"Assistant: Event '{updated_event['subject']}' has been updated successfully.")
            except Exception as e:
                print(f"Assistant: I couldn't update the event due to: {e}")
            continue

        if intent in ["delete_calendar_event", "delete_meeting"]:
            subject = entities.get("title") or entities.get("event_name") or prompt_user("Assistant: Which event would you like to delete? Please provide the title or keyword: ")
            matches = calendar.find_events_by_subject(subject)
            if not matches:
                print("Assistant: I couldn't find any matching events.")
                continue

            if len(matches) > 1:
                print("Assistant: I found multiple events matching that. Please select one to delete:")
                for idx, ev in enumerate(matches, 1):
                    print(f"{idx}. {ev['subject']} at {ev['start']['dateTime']}")
                choice = prompt_user("Assistant: Enter the number of the event to delete: ")
                try:
                    idx = int(choice) - 1
                    event_to_delete = matches[idx]
                except (ValueError, IndexError):
                    print("Assistant: Invalid choice.")
                    continue
            else:
                event_to_delete = matches[0]

            confirm = prompt_user(f"Assistant: Are you sure you want to delete '{event_to_delete['subject']}'? (yes/no): ").lower()
            if confirm == "yes":
                try:
                    calendar.delete_event(event_to_delete["id"])
                    print("Assistant: The event has been deleted.")
                except Exception as e:
                    print(f"Assistant: I couldn't delete the event due to: {e}")
            else:
                print("Assistant: Deletion cancelled.")
            continue

if __name__ == "__main__":
    main()

