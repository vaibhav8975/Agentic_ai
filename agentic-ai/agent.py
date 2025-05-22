import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def detect_intent(user_input):
    system_prompt = """
You are an assistant who understands natural language input and determines the user's intent.
Return one of the following actions: schedule_meeting, delete_meeting, apply_leave, access_sharepoint, no_action.
Also return a 'reason' and any relevant 'details'.
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input}
    ]

    res = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages
    )

    return res.choices[0].message.content

if __name__ == "__main__":
    user_input = input("What can I help you with?\n> ")
    print(detect_intent(user_input))

