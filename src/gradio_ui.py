import gradio as gr
import requests
import os

API_URL = 'https://xemcclumj8.execute-api.us-east-1.amazonaws.com/internet_search_assistant/internet-search-assistant'
api_key = os.environ.get("ISA_API_KEY")
headers = {"api-key": api_key}

def chat_fn(user_message,history):
    """Route queries and replies"""
    r = requests.post(API_URL, headers=headers, json={"query": user_message})
    response = r.json().get("answer", "Error")
    answer = response.get("answer")
    history.append((user_message, answer))
    return history,history

with gr.Blocks() as demo:
    """Define Gradio App"""
    gr.Markdown("# Internet Search Assistant")
    chatbot = gr.Chatbot()
    msg = gr.Textbox(placeholder="Ask something...")
    msg.submit(chat_fn, [msg, chatbot], [chatbot, chatbot])
    chatbot.like(None)

if __name__ == "__main__":
    demo.launch(share=True)