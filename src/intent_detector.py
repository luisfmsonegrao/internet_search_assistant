import os
import json
from llm_caller import call_llm


def detect_intent(query):
    """
    LLM intent detection:
    """
    query = query.lower()
    prompt = f"""
        You are an intent classifier. 
        Your task is to classify the user query below as 'WEB_SEARCH' if it can only be answered by searching the web, or 'NOT_WEB_SEARCH' otherwise.
        You return only valid JSON:
        {{
            "task": "WEB_SEARCH" or "NOT_WEB_SEARCH"
        }}
        
        User query: {query}
    """
    
    ans = call_llm(prompt)
    ans = json.loads(ans)
    return ans
