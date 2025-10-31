import boto3
import json

dynamodb = boto3.resource("dynamodb")
state_table = dynamodb.Table("internet-search-agent-state")


def lambda_handler(event, context):
    """
    AWS LAmbda endpoint to check current state of assistant
    """
    body = json.loads(event["body"])
    session_id = body.get("session_id")

    response = state_table.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key("session_id").eq(
            session_id
        ),
        ScanIndexForward=False,
        Limit=1,
    )

    if not response["Items"]:
        body = {"state": "UNKNOWN"}
    else:
        body = response["Items"][0]

    response = {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body,default=str),
    }
    return response
