from llm_caller import call_llm
from config import KNOWLEDGEBASE_SOURCE_URI_STRING

def answer_from_context(query,context):
    """
    Build a prompt that instructs the LLM to answer a user query based on provided context, point to best sources,
    and produce a short answer + bullets + citations.
    """
    prompt = f"""You are an assistant that answers a user query based on provided context.

    User query: {query}

    Context:
    """
    for i, c in enumerate(context, start=1):
        text = c['text']
        uri = c['metadata'][KNOWLEDGEBASE_SOURCE_URI_STRING]
        prompt += "[{}]: {} (source: {})\n".format(i,text,uri)

    prompt += """
    Please:
    1) Provide a short answer.
    2) Provide up to 5 bullet points summarizing relevant facts, each with [n] citation pointing to result number.
    3) List the most relevant source URIs at the end.
    4) If you can't find an answer from the context or you aren't sure, you answer only "NO_ANSWER"
    Be concise and label citations like [1], [2].
    """
    answer = call_llm(prompt)
    return answer