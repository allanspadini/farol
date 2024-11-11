import os
from dotenv import load_dotenv
import streamlit as st
from litellm import completion

# Carregar as chaves do ambiente
load_dotenv()
chave = os.getenv('chave')
valid_username = os.getenv('USERA')  # Nome de usuário
valid_password = os.getenv('PASSWORD')  # Senha

# Função para autenticação do usuário
def authenticate(username, password):
    return username == valid_username and password == valid_password

# Função para chamar a API com LiteLLM usando o modelo gemini
def call_gemini_api(messages, model="gemini/gemini-pro"):
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    response = completion(
        model=model,
        messages=messages,
        api_key=GEMINI_API_KEY,
    )
    return response.choices[0].message.content

# Configuração inicial do Streamlit
st.set_page_config(page_title="☀️ Farol - Assistente para Concursos Públicos", layout="centered")
st.title("☀️ Farol - Assistente para Concursos Públicos")

# Controle de autenticação usando sessão do Streamlit
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Área de autenticação no menu lateral
with st.sidebar:
    st.subheader("Área de Login")
    if not st.session_state.authenticated:
        username = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")
        
        # Autenticar ao clicar no botão "Entrar"
        if st.button("Entrar"):
            if authenticate(username, password):
                st.session_state.authenticated = True
                st.success("Login bem-sucedido! Bem-vindo(a) ao Farol.")
            else:
                st.error("Nome de usuário ou senha incorretos.")
    else:
        st.write("Você já está autenticado.")
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.experimental_rerun()  # Atualiza a página para remover o chat após logout

# Mostrar o chat apenas se autenticado
if st.session_state.authenticated:

    
    # Inicializar o histórico de mensagens após autenticação
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": """
             Você é o Farol e responde em português brasileiro perguntas sobre concursos públicos ajudando candidatos nos estudos.
             Você é um especialista em concursos públicos, com profundo conhecimento sobre bancas organizadoras, padrões de provas, e perfis de cargos. Seu papel é analisar editais, interpretar os critérios usados pelas bancas, e orientar os usuários em suas jornadas de estudo.
             Passos da conversa:
                1 - Pergunte ao usuário com qual concurso precisa de ajuda;
                2 - Sobre esse concurso pergunte qual os tópicos exigidos no edital e qual ele gostaria de estudar;
                3 - Sugira questões sobre o tópico de interesse e siga incentivando a conversa para que o usuário siga tirando dúvidas sobre o tópico.


             """}
        ]

    # Exibir histórico de mensagens no chat
    for message in st.session_state.messages[1:]:  # Pular a mensagem de sistema inicial
        if message["role"] == "user":
            with st.chat_message("user",avatar=":material/person:"):
                st.markdown(message["content"])
        elif message["role"] == "assistant":
            with st.chat_message("assistant",avatar=":material/smart_toy:"):
                st.markdown(message["content"])

    # Capturar a entrada do usuário
    if user_input := st.chat_input("Digite sua pergunta sobre concursos públicos aqui..."):
        # Exibir a mensagem do usuário
        with st.chat_message("user",avatar=":material/person:"):
            st.markdown(user_input)

        # Adicionar a mensagem do usuário ao histórico
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Criar a mensagem de resposta do modelo
        messages = st.session_state.messages.copy()  # Histórico com as mensagens anteriores
        bot_response = call_gemini_api(messages)

        # Adicionar a resposta do bot ao histórico
        st.session_state.messages.append({"role": "assistant", "content": bot_response})

        # Exibir a resposta do modelo
        with st.chat_message("assistant",avatar=":material/smart_toy:"):
            st.markdown(bot_response)
