import gradio as gr
from transformers import pipeline

pip install gradio transformers
python gradio_chatbot.py

# 파이프라인 로드 (처음 로드 시 오래 걸릴 수 있음)
chatbot = pipeline("conversational", model="facebook/blenderbot-400M-distill")

def respond(message, chat_history):
    from transformers import Conversation
    conv = Conversation(message)
    response = chatbot(conv)
    return response.generated_responses[-1], chat_history + [(message, response.generated_responses[-1])]

with gr.Blocks() as demo:
    chat_history = gr.State([])
    txt = gr.Textbox(label="영어로 입력하세요")
    chatbot_ui = gr.Chatbot()

    txt.submit(respond, inputs=[txt, chat_history], outputs=[chatbot_ui, chat_history])

demo.launch()
