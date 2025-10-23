import os

def lambda_handler(event, context):
    api_key = os.environ.get("AUTH_API_KEY")
    token = event["headers"].get("api-key")
    if token == api_key:
        return {
            "isAuthorized": True,
            "context": {"user": "trusted-user"}
        }
    else:
        return {"isAuthorized": False}