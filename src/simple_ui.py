import requests
import os

AGENT_API_URL = 'https://xemcclumj8.execute-api.us-east-1.amazonaws.com/internet_search_assistant/internet-search-assistant'
STATE_API_URL = 'https://2e8gd55dkh.execute-api.us-east-1.amazonaws.com/state/state'
api_key = os.environ.get("ISA_API_KEY")
headers = {"api-key": api_key}

session_id = "1234" #session id should be created inside agent application, not here.

def call_assistant(user_message):
    r = requests.post(AGENT_API_URL, headers=headers, json={"query": user_message, "session_id": session_id})
    response = r.json().get("answer", "Error")
    answer = response.get("answer")
    return answer

def check_assistant_state():
    r = requests.post(STATE_API_URL, headers=headers, json={"session_id": session_id})
    answer = r.json().get("state", "Error")
    return answer

