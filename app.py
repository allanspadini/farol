from litellm import completion
import os
from dotenv import load_dotenv
import gradio as gr

load_dotenv()

# Função para chamar a API com LiteLLM usando o modelo gemini
def call_gemini_api(messages, model="gemini/gemini-pro"):
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    response = completion(
        model=model,
        messages=messages,
        api_key=GEMINI_API_KEY,
    )
    return response.choices[0].message.content

# Função de resposta para o chatbot
def response(message, history):
    messages = [{"role": "system", "content": """
    Você é o Farol e responde em português brasileiro
    perguntas sobre concursos público ajudando candidatos nos estudos.
    """}]

    # Adicionar o histórico de mensagens
    for user_msg, bot_msg in history:
        messages.append({"role": "user", "content": user_msg})
        messages.append({"role": "assistant", "content": bot_msg})

    # Adicionar a nova mensagem do usuário
    messages.append({"role": "user", "content": message})

    # Obter a resposta do modelo
    return call_gemini_api(messages)

# Interface Gradio atualizada com o CSS para ocultar o rodapé
with gr.Blocks() as demo:
    # CSS para ocultar o "Feito com Gradio"
    gr.HTML("<style>footer {display: none !important;}</style>")
    
    # Chat Interface
    gr.ChatInterface(
        fn=response,
        type="messages",  # Atualização para o novo formato de mensagens
        title='☀️ Farol'
    )

#demo.launch(auth=[('user','admin'),('allan','spadini')],auth_message='Entre seu e-mail e senha', share=True,show_api=False)
demo.launch(share=True,show_api=False)
