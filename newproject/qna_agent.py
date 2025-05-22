from bedrock_agent import ask_bedrock

class QnAAgent:
    def get_answer(self, question):
        response = ask_bedrock(question)
        return f"🧠 Here's a response to your question:\n👉 {response}"

