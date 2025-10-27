import gradio as gr
import requests
import os
from simple_ui import check_assistant_state, call_assistant
from orchestrator import orchestrate

AGENT_API_URL = 'https://xemcclumj8.execute-api.us-east-1.amazonaws.com/internet_search_assistant/internet-search-assistant'
STATE_API_URL = 'https://2e8gd55dkh.execute-api.us-east-1.amazonaws.com/state/state'
api_key = os.environ.get("ISA_API_KEY")
headers = {"api-key": api_key}

session_id = "1234"

def chat_fn(user_message,history):
    """Route queries and replies"""
    answer = call_assistant(user_message)
    history.append((user_message, answer))
    return history,history

with gr.Blocks() as demo:
    """Define Gradio App"""
    gr.Markdown("# Internet Search Assistant")
    chatbot = gr.Chatbot()
    msg = gr.Textbox(placeholder="Ask something...")
    msg.submit(chat_fn, [msg, chatbot], [chatbot, chatbot])

    state_btn = gr.Button("Check Assistant State")
    state_box = gr.Textbox(label="Assistant State", interactive=False)
    state_btn.click(check_assistant_state, [], state_box)

    chatbot.like(None)

if __name__ == "__main__":
    demo.launch(share=True)