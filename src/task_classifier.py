import json
from llm_caller import call_llm


def classify_task(query,history):
    """ Detect intention of the user query. """

    query = query.lower()
    prompt = f"""
        You are a task classifier. 
        You are given a list of past queries and a new query.
        If the answer to the new query is common knowledge, you classify the task as "NO_SEARCH".
        If the new query and one or more past queries refer to the same topic, you classify the task as "CONTEXT_SEARCH".
        If the new query introduces a new topic, and answering it requires a web search, you classify the task as "WEB_SEARCH", and you convert the query to an optimized web query.
        
        You return only valid JSON:
        {{
            "task": "CONTEXT_SEARCH" or "WEB_SEARCH" or "NO_SEARCH"
            "content": web query if task is "WEB_SEARCH", otherwise "NONE"
        }}
        
        New query: {query}
        Past queries:
    """
    for (i,h) in enumerate(history):
        prompt += f"\n {i}: {h["query_text"]}"

    print(prompt)
    ans = call_llm(prompt)
    ans = json.loads(ans)
    return ans
