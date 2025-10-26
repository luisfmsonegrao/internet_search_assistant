from task_classifier import classify_task
from web_searcher import search_web
from context_answer import answer_from_context
from llm_caller import call_llm
from interaction_saver import save_interaction
from interaction_loader import load_interactions
from doc_ingester import upload_to_knowledge_base
from knowledgebase_retriever import retrieve_kb_context

source_uri_string = 'x-amz-bedrock-kb-source-uri'
HISTORY_SIZE = 3
CONTEXT_SIZE = 3
MAX_SEARCH_HITS = 1


def orchestrate(query):
    """Agent orchestration logic"""
    history = load_interactions(HISTORY_SIZE)#ToDo: recency-based context seems unreliable. change to relevance-based context
    task = classify_task(query,history)
    task_class = task.get("task")
    #logger.info("Intent for query '%s' => %s", nquery, intent)
    print(f"Task: {task_class}")
    if task_class == "NO_SEARCH": 
        prompt = f"Answer concisely: {query}"
        answer = call_llm(prompt)
        response = {"query": query, "task_type": task_class, "answer": answer}
        return response

    if task_class == "CONTEXT_SEARCH": #Try to answer from conversation context
        context = retrieve_kb_context(query,CONTEXT_SIZE)
        answer = answer_from_context(query,context) # Add a fallback to WEB_SEARCH if answer cannot be found from context

    elif task_class == "WEB_SEARCH":
        results = search_web(query, MAX_SEARCH_HITS) # Search results are too broad and not optimized. Maybe constrain search to a website for corporate annual reports like SEC EDGAR?
        for doc in results:
            upload_to_knowledge_base(doc) #add a control on document size to avoid ingesting documents that are too large

        if not results: # No results from DDG
            answer = f"I could not find web results for your query. Try rephrasing your question."
            response = {"query": query, "task_type": task_class, "answer": answer}
            return response

        context = retrieve_kb_context(query,CONTEXT_SIZE)
        answer = answer_from_context(query,context)
    
    save_interaction(query,answer,context)
    return {"query": query, "task_type": task_class, "answer": answer}
