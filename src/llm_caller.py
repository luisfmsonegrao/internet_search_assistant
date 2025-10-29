import boto3
import json
from config import AWS_REGION, BEDROCK_LLM_ID

bedrock = boto3.client('bedrock-runtime', region_name=AWS_REGION)

def call_llm(query):
    """Query foundation LLM"""
    
    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "messages": [
            {"role": "user", "content": query}
        ],
        "max_tokens": 5000,
        "temperature": 0.0,
        "top_p": 1.0
    })
    output = bedrock.invoke_model(
        modelId=BEDROCK_LLM_ID,
        body=body,
        contentType="application/json",
        accept="application/json"
    )
    payload = json.loads(output['body'].read())
    response = payload['content'][0]['text']
    return response