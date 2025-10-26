from intent_detector import detect_intent
from web_searcher import search_web, MAX_RESULTS
from context_answer import answer_from_context
from llm_caller import call_llm
from interaction_saver import save_interaction
from doc_ingester import upload_to_knowledge_base


def orchestrate(query):
    """Agen orchestration logic"""
    intent = detect_intent(query)
    intent = intent.get("task")
    #logger.info("Intent for query '%s' => %s", nquery, intent)
    print(f"INTENT: {intent}")
    if intent == "NOT_WEB_SEARCH":
        # Answer purely from LLM (no web)
        prompt = f"Answer concisely: {query}"
        answer = call_llm(prompt)
        answer = {"answer": answer, "sources": "NONE"}
        response = {"query": query, "source": "LLM_ONLY", "answer": answer}
        return response

    # Run DuckDuckGo search
    results = search_web(query, MAX_RESULTS)
    for doc in results:
        upload_to_knowledge_base(doc)

    if not results:
        # No results from DDG
        answer = f"I could not find web results for your query. Try rephrasing your question."
        response = {"query": query, "source": "LLM_ONLY", "answer": answer}
        return response

    # Summarize with LLM
    answer = answer_from_context(query)
    response = answer["answer"]
    sources = answer["sources"]
    save_interaction(query,response,sources)

    return {"query": query, "source": "WEB_ANSWER", "answer": answer}
