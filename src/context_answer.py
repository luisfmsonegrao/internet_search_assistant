import os
import json
import boto3
from llm_caller import call_llm
from context_retriever import retrieve_context

source_uri_string = 'x-amz-bedrock-kb-source-uri'

def answer_from_context(query):
    """
    Build a prompt that instructs the LLM to answer a user query based on provided context, point to best sources,
    and produce a short answer + bullets + citations.
    """

    context = retrieve_context(query)
    prompt = f"""You are an assistant that answers a user query based on provided context.

User question: {query}

Context:
"""
    for i, c in enumerate(context, start=1):
        print(f"CONTEXT: {c}")
        text = c['text']
        uri = c['metadata'][source_uri_string]
        prompt += "[{}]: {} (source: {})\n".format(i,text,uri)

    prompt += """
Please:
1) Provide a short answer.
2) Provide up to 5 bullet points summarizing relevant facts, each with [n] citation pointing to result number.
3) List the most relevant source URLs at the end.
Be concise and label citations like [1], [2].
"""

    ans = call_llm(prompt)
    # Return LLM output plus structured metadata
    return {"answer": ans, "sources": [c["metadata"]["url"] for c in context]}