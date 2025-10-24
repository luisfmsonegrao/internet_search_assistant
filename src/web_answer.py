import os
import json
from llm_caller import call_llm

def answer_from_web_results(query, results):
    """
    Build a prompt that instructs the LLM to answer a user query based on web search results, point to best sources,
    and produce a short answer + bullets + citations.
    """
    prompt = f"""You are an assistant that answers a user query based on web search results.

User question: {query}

Search results:
"""
    for i, r in enumerate(results, start=1):
        prompt += f"\n[{i}] Title: {r.get('title')}\nURL: {r.get('url')}\nSnippet: {r.get('snippet')}\n"

    prompt += """
Please:
1) Provide a short direct answer (2-4 sentences).
2) Provide up to 5 bullet points summarizing relevant facts, each with [n] citation pointing to result number.
3) List the most relevant source URLs at the end.
Be concise and label citations like [1], [2].
"""
    ans = call_llm(prompt)
    # Return LLM output plus structured metadata
    return {"answer": ans, "sources": [r["url"] for r in results]}