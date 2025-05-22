def schedule_meeting(command, token):
    import re
    from datetime import datetime, timedelta

    name_match = re.search(r"with (\w+)", command)
    time_match = re.search(r"at (\d+ ?(am|pm))", command)

    if not name_match or not time_match:
        print("🤖 Buddy: I couldn't parse the meeting details.")
        return True

    name = name_match.group(1).capitalize()
    time_str = time_match.group(1).lower().replace(" ", "")
    hour = int(time_str[:-2])
    am_pm = time_str[-2:]
    if am_pm == "pm" and hour != 12:
        hour += 12
    elif am_pm == "am" and hour == 12:
        hour = 0

    now = datetime.utcnow()
    meeting_time = now.replace(hour=hour, minute=0, second=0, microsecond=0)
    end_time = meeting_time + timedelta(hours=1)

    print(f"🤖 Searching for users named '{name}'...")
    matches = get_users(token, name)

    if not matches:
        print("❌ No matching users found in your tenant.")
        return True

    if len(matches) == 1:
        selected_user = matches[0]
    else:
        print("🔎 Multiple matches found:")
        for i, user in enumerate(matches, 1):
            print(f"{i}. {user['displayName']} ({user['mail'] or user['userPrincipalName']})")
        choice = int(input("👉 Who do you want to invite? Enter number: "))
        selected_user = matches[choice - 1]

    attendee_email = selected_user["mail"] or selected_user["userPrincipalName"]
    attendee_name = selected_user["displayName"]
    subject = input("📝 Enter meeting subject: ")

    success, result = schedule_event(token, subject, meeting_time.isoformat(), end_time.isoformat(), attendee_email, attendee_name)
    if success:
        print(f"✅ Meeting scheduled with {attendee_name} at {meeting_time.strftime('%H:%M')} UTC.")
    else:
        print("❌ Failed to schedule meeting:", result)

    return True

