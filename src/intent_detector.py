import os
import json
from llm_caller import call_llm


def detect_intent(query):
    """
    LLM intent detection:
    """
    q = query.lower()
    prompt = f"""
        You are an intent classifier. 
        Your task is to classify the user query below as 'WEB_SEARCH' or 'NOT_WEB_SEARCH'.
        You return only valid JSON:
        {{
            task: 'WEB_SEARCH' | 'NOT_WEB_SEARCH'
        }}
        
        User query: {query}
    """
    
    ans = call_llm(prompt)
    ans = json.loads(ans)
    return ans
