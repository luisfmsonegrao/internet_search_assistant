import boto3
from decimal import Decimal

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("internet-search-agent-cache")

def load_interactions(top_k=5):
    """ Load most recent interactions from DynamoDB """
    response = table.scan()
    items = sorted(response["Items"], key=lambda x: x["timestamp"], reverse=True)
    return items[:top_k]