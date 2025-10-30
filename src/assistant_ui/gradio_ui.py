import gradio as gr
from src.assistant_api.assistant_api import check_assistant_state, call_assistant


def chat_fn(user_message, history):
    """
    Route queries and replies
    """
    answer = call_assistant(user_message)
    history.append((user_message, answer))
    return history, history


with gr.Blocks() as demo:
    """
    Define Gradio App
    """
    gr.Markdown("# Internet Search Assistant")
    chatbot = gr.Chatbot()
    msg = gr.Textbox(placeholder="Ask something...")
    msg.submit(chat_fn, [msg, chatbot], [chatbot, chatbot])

    state_btn = gr.Button("Check Assistant State")
    state_box = gr.Textbox(label="Assistant State", interactive=False)
    state_btn.click(check_assistant_state, [], state_box)

    chatbot.like(None) # Add feedback to interaction DB for monitoring/tuning

if __name__ == "__main__":
    demo.launch(share=True)
