from orchestrator import orchestrate
import json


MAX_RESULTS = 2

def lambda_handler(event, context):
    """AWS Lambda endpoint to answer user queries"""
    try:
        body = json.loads(event.get("body","{}"))
        query = body.get("query", "").strip()
        if not query:
            return {"statusCode": 400, "body": json.dumps({"error": "query missing"})}

        response = orchestrate(query)
        return {"statusCode": 200, "body": json.dumps(response)}

       
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}