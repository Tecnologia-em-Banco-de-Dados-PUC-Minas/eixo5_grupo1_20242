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

load_dotenv(".env")
qdrant_api_key = os.environ.get("OPENAI_API_KEY")
qdrant_url = os.environ.get("QDRANT_URL")
qdrant_api_key = os.environ.get("QDRANT_API_KEY")

st.set_page_config(page_title="Pergunte ao seu PDF!", page_icon=":books:")


# Inicializações apenas uma vez, evitando recarregamento em cada interação
@st.cache_resource
def init_components(local=True):
    if local:
        # Criação da coleção Qdrant Local
        client = QdrantClient(host="localhost", port=6333)
        create_collection("openai_collection", 1536)
    else:
        # Criação da coleção Qdrant Cloud
        client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
        create_collection_cloud("openai_collection", 1536)

    # Inicialização do processo de embedding
    vectorstore = initialize_embeddings("openai_collection", client)

    # Armazenando o vectorstore no estado da sessão
    st.session_state.vectorstore = vectorstore
    st.session_state.qa = create_retrieval_qa(vectorstore)

    return vectorstore, st.session_state.qa


# Botão para selecionar entre Qdrant Local e Cloud
use_cloud = st.sidebar.checkbox("Usar Qdrant Cloud")

# Verifique se o vectorstore já foi inicializado
if "vectorstore" not in st.session_state:
    vectorstore, qa = init_components(local=not use_cloud)
else:
    vectorstore = st.session_state.vectorstore
    qa = st.session_state.qa

# Título da barra lateral
st.sidebar.title("Bem vindo ao AskYourPDF")

# File uploader na barra lateral
uploaded_files = st.sidebar.file_uploader(
    "Escolha um novo arquivo para analisar.", type=["pdf"], accept_multiple_files=True
)

# Caminho da pasta onde os arquivos serão salvos
save_path = "assets/pdf"  # Substitua pelo caminho desejado

# Verifica se a pasta existe, se não, cria a pasta
if not os.path.exists(save_path):
    os.makedirs(save_path)

# Processa cada arquivo carregado
for uploaded_file in uploaded_files:
    if uploaded_file is not None:
        # Constrói o caminho completo para salvar o arquivo
        file_path = os.path.join(save_path, uploaded_file.name)

        # Salva o arquivo na pasta especificada
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Define o nome do arquivo .txt
        txt_file_name = uploaded_file.name.replace(".pdf", "") + ".txt"
        txt_file_path = os.path.join("assets/txt/", txt_file_name)

        # Chama a função para extrair texto do PDF e salvá-lo em um arquivo .txt
        try:
            result = extract_text_from_pdf(file_path, txt_file_path)
            st.sidebar.write(f"Arquivo salvo com sucesso!")
        except Exception as e:
            st.sidebar.write(f"Erro ao processar o arquivo: {e}")

st.header("Converse com o seu PDF")

with st.sidebar:

    if st.button("Processar dados"):
        st.info("Iniciando o processamento...")

        # Criação da barra de progresso
        progress_bar = st.progress(0)
        progress_status = st.empty()

        # Passo 1: Criação da coleção Qdrant
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

        # Passo 2: Inicialização do processo de embedding
        vectorstore = initialize_embeddings("openai_collection", client)
        st.success("Vectorstore inicializado com sucesso.")
        progress_bar.progress(75)
        progress_status.text("Vectorstore inicializado.")

        # Passo 3: Carregando e processando o texto
        with open(txt_file_path, encoding="utf-8") as f:
            raw_text = f.read()

        texts = get_chunks(raw_text)
        st.success("Textos carregados com sucesso.")
        progress_bar.progress(90)
        progress_status.text("Textos carregados.")

        # Passo 4: Adicionando textos ao banco de dados
        vectorstore.add_texts(texts)
        st.success("Textos adicionados ao vectorstore com sucesso!")
        progress_bar.progress(100)
        progress_status.text("Processamento concluído!")

        st.success("Processo concluído com sucesso!!!")

# Inicializa o histórico de conversação se ainda não existir
if "historico_conversa" not in st.session_state:
    st.session_state.historico_conversa = []

# Campo de entrada para a pergunta
user_input = st.text_input("Digite sua pergunta:", key="input")

# Ao pressionar Enter ou clicar no botão Enviar
if st.button("Enviar"):
    # Verifica se o input não está vazio
    if user_input:
        # Adiciona a pergunta do usuário ao histórico
        st.session_state.historico_conversa.append(
            {"message": user_input, "is_user": True}
        )

        # Verifica se vectorstore não é None
        if vectorstore is not None:
            response = qa.run(user_input)

        # Adiciona a resposta ao histórico de conversação
        st.session_state.historico_conversa.append(
            {"message": response, "is_user": False}
        )

    # Exibe o histórico de conversação
    for i, chat in enumerate(st.session_state.historico_conversa):
        message(chat["message"], is_user=chat["is_user"], key=f"msg_{i}")
