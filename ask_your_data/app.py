import streamlit as st
from streamlit_chat import message
from process_qdrant.manager import create_collection, create_collection_cloud
from process_langchain.embedding import initialize_embeddings
from process_langchain.retrieval_qa import create_retrieval_qa
from utils.text_processing import get_chunks
from utils.extract_data_pdf import extract_text_from_pdf
from qdrant_client import QdrantClient
from dotenv import load_dotenv
import os


# Carrega variáveis de ambiente
def load_env_variables():
    load_dotenv(".env")
    qdrant_api_key = os.environ.get("OPENAI_API_KEY")
    qdrant_url = os.environ.get("QDRANT_URL")
    qdrant_api_key = os.environ.get("QDRANT_API_KEY")
    return qdrant_url, qdrant_api_key


# Inicializações apenas uma vez, evitando recarregamento em cada interação
@st.cache_resource
def init_components(local=True, qdrant_url=None, qdrant_api_key=None):
    if local:
        client = QdrantClient(host="localhost", port=6333)
        create_collection("openai_collection", 1536)
    else:
        client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
        create_collection_cloud("openai_collection", 1536)

    vectorstore = initialize_embeddings("openai_collection", client)
    st.session_state.vectorstore = vectorstore
    st.session_state.qa = create_retrieval_qa(vectorstore)
    return vectorstore, st.session_state.qa


# Processa os arquivos PDF carregados e salva o texto extraído
def process_uploaded_files(uploaded_files, save_path):
    txt_file_path = None  # Inicializa a variável
    for uploaded_file in uploaded_files:
        if uploaded_file is not None:
            file_path = os.path.join(save_path, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            txt_file_name = uploaded_file.name.replace(".pdf", "") + ".txt"
            txt_file_path = os.path.join("assets/txt/", txt_file_name)

            try:
                extract_text_from_pdf(file_path, txt_file_path)
                st.sidebar.write(f"Arquivo salvo com sucesso!")
            except Exception as e:
                st.sidebar.write(f"Erro ao processar o arquivo: {e}")

    return txt_file_path


# Executa o processamento dos dados
def process_data(txt_file_path, use_cloud, qdrant_url, qdrant_api_key):
    st.info("Iniciando o processamento...")

    progress_bar = st.progress(0)
    progress_status = st.empty()

    client = QdrantClient(
        host="localhost" if not use_cloud else qdrant_url,
        port=6333 if not use_cloud else None,
        api_key=None if not use_cloud else qdrant_api_key,
    )
    st.success("Cliente Qdrant criado com sucesso.")
    progress_bar.progress(25)
    progress_status.text("Cliente Qdrant criado.")

    if use_cloud:
        st.info("Usando Qdrant Cloud")
        create_collection_cloud("openai_collection", 1536)
    else:
        st.info("Usando Qdrant Local")
        create_collection("openai_collection", 1536)

    progress_bar.progress(50)
    progress_status.text("Coleção criada com sucesso.")

    vectorstore = initialize_embeddings("openai_collection", client)
    st.success("Vectorstore inicializado com sucesso.")
    progress_bar.progress(75)
    progress_status.text("Vectorstore inicializado.")

    with open(txt_file_path, encoding="utf-8") as f:
        raw_text = f.read()

    texts = get_chunks(raw_text)
    st.success("Textos carregados com sucesso.")
    progress_bar.progress(90)
    progress_status.text("Textos carregados.")

    vectorstore.add_texts(texts)
    st.success("Textos adicionados ao vectorstore com sucesso!")
    progress_bar.progress(100)
    progress_status.text("Processamento concluído!")

    st.success("Processo concluído com sucesso!!!")
    return vectorstore


# Inicializa o histórico de conversação
def initialize_conversation_history():
    if "historico_conversa" not in st.session_state:
        st.session_state.historico_conversa = []


# Processa a pergunta do usuário e obtém a resposta
def process_user_input(user_input, qa):
    if user_input:
        st.session_state.historico_conversa.append(
            {"message": user_input, "is_user": True}
        )
        response = qa.run(user_input)
        st.session_state.historico_conversa.append(
            {"message": response, "is_user": False}
        )

    for i, chat in enumerate(st.session_state.historico_conversa):
        message(chat["message"], is_user=chat["is_user"], key=f"msg_{i}")


# Configura a página inicial
def configure_page():
    st.set_page_config(
        page_title="Pergunte ao seu PDF!",
        page_icon=":books:",
        # layout="wide",
        initial_sidebar_state="expanded",
    )


# Função de login
def login():
    st.title("Login")
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if (
            username == "admin" and password == "admin"
        ):  # Substitua por um método de autenticação real
            st.session_state["logged_in"] = True
            st.query_params["logged_in"] = "True"
        else:
            st.error("Usuário ou senha incorretos")


# Função principal
def main():
    configure_page()

    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if not st.session_state["logged_in"]:
        login()
    else:
        qdrant_url, qdrant_api_key = load_env_variables()

        use_cloud = st.sidebar.checkbox("Usar Qdrant Cloud")

        if "vectorstore" not in st.session_state:
            vectorstore, qa = init_components(
                local=not use_cloud,
                qdrant_url=qdrant_url,
                qdrant_api_key=qdrant_api_key,
            )
        else:
            vectorstore = st.session_state.vectorstore
            qa = st.session_state.qa

        st.sidebar.title("Bem vindo ao AskYourPDF")

        uploaded_files = st.sidebar.file_uploader(
            "Escolha um novo arquivo para analisar.",
            type=["pdf"],
            accept_multiple_files=True,
        )

        save_path = "assets/pdf"
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        txt_file_path = process_uploaded_files(uploaded_files, save_path)

        if st.sidebar.button("Processar dados"):
            if txt_file_path:  # Verifica se um arquivo foi processado
                process_data(txt_file_path, use_cloud, qdrant_url, qdrant_api_key)
            else:
                st.warning("Nenhum arquivo foi carregado ou processado.")

        st.header("Converse com o seu PDF")

        initialize_conversation_history()

        user_input = st.text_input("Digite sua pergunta:", key="input")

        if st.button("Enviar"):
            process_user_input(user_input, qa)


if __name__ == "__main__":
    main()
