import requests
import os

API_URL = 'https://xemcclumj8.execute-api.us-east-1.amazonaws.com/internet_search_assistant/internet-search-assistant'
api_key = os.environ.get("ISA_API_KEY")
headers = {"api-key": api_key}

def call_assistant(user_message):
    r = requests.post(API_URL, headers=headers, json={"query": user_message})
    print(r)
    response = r.json().get("answer", "Error")
    print(response)
    answer = response.get("answer")
    return answer
