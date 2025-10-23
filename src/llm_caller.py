import boto3
import json

BEDROCK_MODEL_ID = 'anthropic.claude-3-sonnet-20240229-v1:0'
bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

def call_llm(query):
    """Query foundation LLM"""
    
    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "messages": [
            {"role": "user", "content": query}
        ],
        "max_tokens": 4000,
        "temperature": 0.0,
        "top_p": 1.0
    })
    output = bedrock.invoke_model(
        modelId=BEDROCK_MODEL_ID,
        body=body,
        contentType="application/json",
        accept="application/json"
    )
    payload = json.loads(output['body'].read())
    response = payload['content'][0]['text']
    return response