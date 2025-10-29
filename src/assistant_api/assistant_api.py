import requests
from ..config import AGENT_API_URL
from ..config import STATE_API_URL
from ..config import API_KEY

headers = {"api-key": API_KEY}
session_id = "1234"  # session id should be created inside agent application, not here.


def call_assistant(user_message):
    """
    API to query the Search Assistant
    """
    r = requests.post(
        AGENT_API_URL,
        headers=headers,
        json={"query": user_message, "session_id": session_id},
    )
    answer = r.json().get("answer", "Error")
    return answer


def check_assistant_state():
    """
    API to check current state of assistant
    """
    r = requests.post(STATE_API_URL, headers=headers, json={"session_id": session_id})
    answer = r.json().get("state", "Error")
    return answer
