from intent_detector import detect_intent
from web_searcher import search_web, MAX_RESULTS
from search_summarizer import summarize_search_results
from llm_caller import call_llm

def orchestrate(query):
    intent = detect_intent(query)
    intent = intent.get("task")
    #logger.info("Intent for query '%s' => %s", nquery, intent)

    if intent == "NOT_WEB_SEARCH":
        # Answer purely from LLM (no web)
        prompt = f"Answer concisely: {query}"
        answer = call_llm(prompt)
        answer = {"answer": answer, "sources": "NONE"}
        response = {"query": query, "source": "LLM_ONLY", "answer": answer}
        return response

    # Run DuckDuckGo search
    results = search_web(query, MAX_RESULTS)

    if not results:
        # No results from DDG
        answer = f"I could not find web results for your query. Try rephrasing your question."
        response = {"query": query, "source": "LLM_ONLY", "answer": answer}
        return response

    # Summarize with LLM
    summary = summarize_search_results(query, results)
    return {"query": query, "source": "WEB_SUMMARY", "answer": summary}
