import boto3
import json

class BedrockAgent:
    def __init__(self):
        self.bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")

    def invoke_bedrock(self, prompt: str) -> str:
        system_instruction = (
            "You are a helpful calendar assistant.\n"
            "Respond ONLY with a JSON object in this exact format:\n"
            '{ "intent": "<intent>", "entities": { "key": "value", ... } }\n'
            "Do NOT include any extra explanation, text, or formatting.\n"
        )
        # The prompt format required by Claude models:
        full_prompt = (
            system_instruction +
            "\n\nHuman: " + prompt +
            "\n\nAssistant:"
        )

        body = {
            "prompt": full_prompt,
            "max_tokens_to_sample": 300,
            "temperature": 0,               # deterministic output
            "stop_sequences": ["\n\nHuman:"]
        }

        try:
            response = self.bedrock.invoke_model(
                modelId="anthropic.claude-v2",
                contentType="application/json",
                accept="application/json",
                body=json.dumps(body)
            )
            response_body = response['body'].read().decode('utf-8')
            completion = json.loads(response_body).get("completion", "")
            
            print("DEBUG: Raw completion from Bedrock:")
            print(completion)   # <---- Debug print to see raw response
            
            return completion.strip()
        except Exception as e:
            print(f"Error calling Bedrock API: {e}")
            return "(Error: Could not get response from Bedrock.)"

    def get_intent_entities(self, user_input: str) -> dict:
        completion = self.invoke_bedrock(user_input)
        try:
            intent_data = json.loads(completion)
            intent = intent_data.get("intent")
            entities = intent_data.get("entities", {})
            return {"intent": intent, "entities": entities}
        except json.JSONDecodeError:
            print("Bedrock response is not valid JSON:")
            print(completion)
            return {"intent": None, "entities": {}}

