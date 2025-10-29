import boto3
import time
from config import STATE_DB_TTL

dynamodb = boto3.resource("dynamodb")
state_table = dynamodb.Table("internet-search-agent-state")

def update_state(session_id,state):
    init_time = int(time.time())
    state_table.put_item(
        Item={
        'session_id': session_id,
        'state': state,
        'timestamp': init_time,
        'ttl': init_time+STATE_DB_TTL
        }
    )