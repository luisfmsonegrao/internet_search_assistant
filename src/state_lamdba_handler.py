import boto3
import json

dynamodb = boto3.resource('dynamodb')
state_table = dynamodb.Table('agent_state')

def lambda_handler(event, context):
    session_id = event['queryStringParameters']['session_id']

    response = state_table.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key('session_id').eq(session_id),
        ScanIndexForward=False,
        Limit=1 
    )

    if not response['Items']:
        body = {"state": "UNKNOWN"}
    else:
        body = response['Items'][0]

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body)
    }