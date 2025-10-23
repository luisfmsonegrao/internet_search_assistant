import requests

API_URL = 'https://xemcclumj8.execute-api.us-east-1.amazonaws.com/internet_search_assistant/internet-search-assistant'

def call_assistant(user_message):
    r = requests.post(API_URL, json={"query": user_message})
    response = r.json().get("answer", "Error")
    answer = response.get("answer")
    return answer
