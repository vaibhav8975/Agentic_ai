import boto3
import json

# Create Bedrock runtime client
client = boto3.client('bedrock-runtime', region_name='us-east-1')

def call_claude(prompt):
    body = {
        "prompt": f"\n\nHuman: {prompt}\n\nAssistant:",
        "max_tokens_to_sample": 500,
        "temperature": 0.7,
        "top_k": 250,
        "top_p": 1,
        "stop_sequences": ["\n\nHuman:"]
    }

    response = client.invoke_model(
        modelId="anthropic.claude-v2",
        contentType="application/json",
        accept="application/json",
        body=json.dumps(body)
    )

    result = json.loads(response['body'].read())
    return result['completion']

# Example
if __name__ == "__main__":
    user_input = input("🤖 Ask Claude something:\n> ")
    print(call_claude(user_input))

