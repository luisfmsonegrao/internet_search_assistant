from task_classifier import classify_task
from web_searcher import search_web
from context_answer import answer_from_context
from llm_caller import call_llm
from interaction_saver import save_interaction
from interaction_loader import load_interactions
from doc_ingester import upload_to_knowledge_base
from knowledgebase_retriever import retrieve_kb_context
from state_saver import update_state
from src.config import HISTORY_CONTEXT_SIZE, RELEVANCE_CONTEXT_SIZE, MAX_SEARCH_HITS


def orchestrate(query, session_id):
    """
    Agent orchestration logic
    """
    update_state(session_id, "LOADING INTERACTION HISTORY") # Log agent state to DynamoDB
    history = load_interactions(HISTORY_CONTEXT_SIZE)  # Load recent interacion context. ToDo: Add relevance-based historic context
    update_state(session_id, "CLASSIFYING TASK TYPE")
    task = classify_task(query, history) #Decide how to proceed to answer query
    task_class = task.get("task")
    if task_class == "NO_SEARCH": #LLM answers without context
        prompt = f"Answer concisely: {query}"
        update_state(session_id, "ANSWERING QUESTION FROM LLM KNOWLEDGE")
        answer = call_llm(prompt)
        response = {"query": query, "task_type": task_class, "answer": answer}
        return response

    if task_class == "CONTEXT_SEARCH":  # Answer from conversation context and knowledge base
        update_state(session_id, "RETRIEVING CONTEXT INFORMATION RELEVANT FOR QUESTION")
        context = retrieve_kb_context(query, RELEVANCE_CONTEXT_SIZE) #retrieve relevant info from knowledge base
        update_state(session_id, "ANSWERING QUESTION FROM RELEVANT KNOWLEDGE BASE CONTEXT")
        answer = answer_from_context(query, context)  # call claude to answer query from context. ToDo: Add fallback to WEB SEARCH

    elif task_class == "WEB_SEARCH": # ToDo: Agent waits for document ingestion before answering, this takes too long. In the future, should answer first based on summary, then ingest.
        update_state(session_id, "SEARCHING WEB FOR RELEVANT CONTEXT INFORMATION")
        results = search_web(query, MAX_SEARCH_HITS)  # ToDo: Search results are too broad and not optimized. Maybe constrain search to a website for corporate annual reports like SEC EDGAR?
        update_state(session_id,"INGESTING DOCUMENTS RETRIEVED FROM WEB SEARCH INTO KNOWLEDGE BASE")
        for doc in results:
            upload_to_knowledge_base(doc) # ToDo: consider limiting size of documents, or summarizing first, to keep DB size manageable

        if not results:  # No results from WEB search
            answer = "I could not find web results for your query. Try rephrasing your question."
            response = {"query": query, "task_type": task_class, "answer": answer}
            return response

        update_state(session_id, "RETRIEVING CONTEXT INFORMATION RELEVANT FOR QUESTION")
        context = retrieve_kb_context(query, RELEVANCE_CONTEXT_SIZE) # Retrieve relevant info after having ingested web search results
        update_state(session_id,"ANSWERING QUESTION BASED ON CONTEXT INFORMATION RETRIEVED FROM WEB")
        answer = answer_from_context(query, context) # call claude to answer from context

    update_state(session_id, "SAVING INTERACTION")
    save_interaction(query, answer, context) # save current interaction to DynamoDB
    update_state(session_id, "WAITING FOR NEXT QUESTION")
    return {"query": query, "task_type": task_class, "answer": answer}
