from orchestrator import orchestrate
from interaction_saver import save_interaction
import json


MAX_RESULTS = 2

def lambda_handler(event, context):
    """
    Expects JSON body: {"query": "tell me about X"}
    """
    try:
        body = json.loads(event.get("body","{}"))
        query = body.get("query", "").strip()
        if not query:
            return {"statusCode": 400, "body": json.dumps({"error": "query missing"})}

        response = orchestrate(query)
        save_interaction(query,response)
        return {"statusCode": 200, "body": json.dumps(response)}

       
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}