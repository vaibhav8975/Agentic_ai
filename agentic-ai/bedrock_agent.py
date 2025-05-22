import boto3
import json

bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")

def invoke_bedrock(prompt):
    body = {
        "prompt": f"\n\nHuman: {prompt}\n\nAssistant:",
        "max_tokens_to_sample": 300,
        "temperature": 0.5,
        "stop_sequences": ["\n\nHuman:"]
    }
    try:
        response = bedrock.invoke_model(
            modelId="anthropic.claude-v2",
            contentType="application/json",
            accept="application/json",
            body=json.dumps(body)
        )
        response_body = response['body'].read().decode('utf-8')
        completion = json.loads(response_body)["completion"]
        return completion
    except Exception as e:
        print(f"Error calling Bedrock API: {e}")
        return "(Error: Could not get response from Bedrock.)"

