import boto3
import uuid
import time
import json
from decimal import Decimal

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("internet-search-agent-cache")
bedrock = boto3.client("bedrock-runtime")
embedding_model = "amazon.titan-embed-text-v2:0"
ttl_threshold = 7200 #seconds

def save_interaction(query, results):
    embedding = embed_query(query)
    embedding = [Decimal(str(x)) for x in embedding]
    table.put_item(Item={
        "query_id": str(uuid.uuid4()),
        "timestamp": int(time.time()),
        "query_text": query,
        "embedding": embedding,
        "results": json.dumps(results),
        "ttl": int(time.time()) + ttl_threshold
    })

def embed_query(query):
    response = bedrock.invoke_model(
        modelId=embedding_model,
        body=json.dumps({"inputText": query})
    )
    response = json.loads(response["body"].read())["embedding"]
    return response
