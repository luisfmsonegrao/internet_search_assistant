from task_classifier import classify_task
from web_searcher import search_web
from context_answer import answer_from_context
from llm_caller import call_llm
from interaction_saver import save_interaction
from interaction_loader import load_interactions
from doc_ingester import upload_to_knowledge_base
from knowledgebase_retriever import retrieve_kb_context
from state_saver import update_state
from config import HISTORY_CONTEXT_SIZE, RELEVANCE_CONTEXT_SIZE, MAX_SEARCH_HITS


def orchestrate(query,session_id):
    """Agent orchestration logic"""
    update_state(session_id,"LOADING INTERACTION HISTORY")
    history = load_interactions(HISTORY_CONTEXT_SIZE)#ToDo: recency-based context seems unreliable. change to relevance-based context
    update_state(session_id, "CLASSIFYING TASK TYPE")
    task = classify_task(query,history)
    task_class = task.get("task")
    if task_class == "NO_SEARCH": 
        prompt = f"Answer concisely: {query}"
        update_state(session_id,"ANSWERING QUESTION FROM LLM KNOWLEDGE")
        answer = call_llm(prompt)
        response = {"query": query, "task_type": task_class, "answer": answer}
        return response

    if task_class == "CONTEXT_SEARCH": #Try to answer from conversation context
        update_state(session_id,"RETRIEVING CONTEXT INFORMATION RELEVANT FOR QUESTION")
        context = retrieve_kb_context(query,RELEVANCE_CONTEXT_SIZE)
        update_state(session_id,"ANSWERING QUESTION FROM RELEVANT KNOWLEDGE BASE CONTEXT")
        answer = answer_from_context(query,context) # Add a fallback to WEB_SEARCH if answer cannot be found from context

    elif task_class == "WEB_SEARCH":
        update_state(session_id,"SEARCHING WEB FOR RELEVANT CONTEXT INFORMATION")
        results = search_web(query, MAX_SEARCH_HITS) # Search results are too broad and not optimized. Maybe constrain search to a website for corporate annual reports like SEC EDGAR?
        update_state(session_id,"INGESTING DOCUMENTS RETRIEVED FROM WEB SEARCH INTO KNOWLEDGE BASE")
        for doc in results:
            upload_to_knowledge_base(doc) #add a control on document size to avoid ingesting documents that are too large

        if not results: # No results from DDG
            answer = f"I could not find web results for your query. Try rephrasing your question."
            response = {"query": query, "task_type": task_class, "answer": answer}
            return response
        
        update_state(session_id,"RETRIEVING CONTEXT INFORMATION RELEVANT FOR QUESTION")
        context = retrieve_kb_context(query,RELEVANCE_CONTEXT_SIZE)
        update_state(session_id,"ANSWERING QUESTION BASED ON CONTEXT INFORMATION RETRIEVED FROM WEB")
        answer = answer_from_context(query,context)
    
    update_state(session_id,"SAVING INTERACTION")
    save_interaction(query,answer,context)
    update_state(session_id,"WAITING FOR NEXT QUESTION")
    return {"query": query, "task_type": task_class, "answer": answer}
