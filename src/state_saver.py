import boto3
import time

dynamodb = boto3.resource("dynamodb")
state_table = dynamodb.Table("internet-search-agent-state")
ttl_time = 7200

def update_state(session_id,state):
    init_time = int(time.time())
    state_table.put_item(
        Item={
        'session_id': session_id,
        'state': state,
        'timestamp': init_time,
        'ttl': init_time+ttl_time
        }
    )