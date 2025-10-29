import boto3

dynamodb = boto3.resource("dynamodb")
cache_table = dynamodb.Table("internet-search-agent-cache")


def load_interactions(top_k=5):
    """
    Load most recent interactions from DynamoDB
    """
    response = cache_table.scan()
    items = sorted(response["Items"], key=lambda x: x["timestamp"], reverse=True)
    return items[:top_k]
