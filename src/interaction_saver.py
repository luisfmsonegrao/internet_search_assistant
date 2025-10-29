import boto3
import uuid
import time
import json
from decimal import Decimal
from config import TEXT_EMBEDDING_MODEL_ID
from config import INTERACTION_DB_TTL

dynamodb = boto3.resource("dynamodb")
interaction_cache = dynamodb.Table("internet-search-agent-cache")
bedrock = boto3.client("bedrock-runtime")

def save_interaction(query, results,context):
    """Save interaction to DynamoDB"""
    embedding = embed_query(query)
    embedding = [Decimal(str(x)) for x in embedding]
    init_time = int(time.time())
    interaction_cache.put_item(Item={
        "query_id": str(uuid.uuid4()),
        "timestamp": init_time,
        "query_text": query,
        "embedding": embedding,
        "results": json.dumps(results),
        "context": json.dumps(context),
        "ttl": init_time + INTERACTION_DB_TTL
    })

def embed_query(query):
    response = bedrock.invoke_model(
        modelId=TEXT_EMBEDDING_MODEL_ID,
        body=json.dumps({"inputText": query})
    )
    response = json.loads(response["body"].read())["embedding"]
    return response
