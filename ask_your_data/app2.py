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
import time
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Configura a página inicial
def configure_page():
    st.set_page_config(
        page_title="Pergunte ao seu PDF!",
        page_icon=":books:",
        initial_sidebar_state="expanded",
    )


# Carrega variáveis de ambiente
def load_env_variables():
    load_dotenv(".env")
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

    try:
        vectorstore = initialize_embeddings("openai_collection", client)
        qa = create_retrieval_qa(vectorstore)
        st.session_state.vectorstore = vectorstore
        st.session_state.qa = qa
        return vectorstore, qa
    except Exception as e:
        st.error(f"Erro ao inicializar componentes: {e}")
        return None, None


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


# Processa a pergunta do usuário e obtém a resposta com o nome do modelo incluído
def process_user_input(user_input, qa, model_name):
    if user_input:
        st.session_state.historico_conversa.append(
            {"message": user_input, "is_user": True}
        )
        response = qa.run(user_input)
        st.session_state.historico_conversa.append(
            {"message": f"{model_name}: {response}", "is_user": False}
        )

    for i, chat in enumerate(st.session_state.historico_conversa):
        message(chat["message"], is_user=chat["is_user"], key=f"msg_{i}")


def calculate_cosine_similarity(text1, text2):
    # Verifique se os textos não são vazios
    if not text1 or not text2:
        return 0.0

    vectorizer = TfidfVectorizer().fit_transform([text1, text2])
    vectors = vectorizer.toarray()
    return cosine_similarity(vectors)[0, 1]


# Função para comparar os modelos de embeddings usando o histórico do chat
def compare_embeddings_models(
    use_cloud, qdrant_url, qdrant_api_key, user_selected_model
):
    if (
        "historico_conversa" not in st.session_state
        or len(st.session_state.historico_conversa) == 0
    ):
        st.warning("Não há histórico de conversas para comparar.")
        return

    # Extrai apenas as perguntas feitas pelo usuário no histórico
    queries = [
        chat["message"]
        for chat in st.session_state.historico_conversa
        if chat["is_user"]
    ]

    if not queries:
        st.warning("Não há perguntas feitas pelo usuário para comparar.")
        return

    results = {
        "OpenAI": {
            "responses": [],
            "times": [],
        },
        "BERT": {
            "responses": [],
            "times": [],
        },
    }

    models_to_compare = (
        ["openai", "bert"]
        if user_selected_model.lower() == "openai"
        else ["bert", "openai"]
    )

    for model in models_to_compare:
        model_key = "OpenAI" if model == "openai" else "BERT"
        vectorstore, qa = init_components(
            local=not use_cloud, qdrant_url=qdrant_url, qdrant_api_key=qdrant_api_key
        )

        if not qa:
            st.error(f"Erro ao inicializar o modelo {model_key}.")
            return

        for query in queries:
            start_time = time.time()
            response = qa.run(query)
            end_time = time.time()

            # Registra a resposta e o tempo
            results[model_key]["responses"].append(response)
            results[model_key]["times"].append(end_time - start_time)

    # Cálculo das métricas comparando a similaridade das respostas entre os dois modelos
    total_queries = len(queries)
    similarity_scores = []

    for i in range(total_queries):
        similarity = calculate_cosine_similarity(
            results["OpenAI"]["responses"][i], results["BERT"]["responses"][i]
        )
        similarity_scores.append(similarity)

    # Considerando respostas similares quando a similaridade for acima de um limiar, por exemplo, 0.8
    threshold = 0.8
    similarity_openai = (
        sum(1 for score in similarity_scores if score > threshold) / total_queries
    )
    similarity_bert = similarity_openai  # Porque a comparação é simétrica

    avg_time_openai = sum(results["OpenAI"]["times"]) / total_queries
    avg_time_bert = sum(results["BERT"]["times"]) / total_queries

    # Exibe os resultados
    st.write("Comparação de Modelos de Embeddings com Base no Histórico de Perguntas")
    for i, query in enumerate(queries):
        st.write(f"**Pergunta:** {query}")
        st.write(f"**Resposta** OpenAI: {results['OpenAI']['responses'][i]}")
        st.write(f"**Resposta** BERT: {results['BERT']['responses'][i]}")
        st.write(f"**Similaridade (Cosine):** {similarity_scores[i]:.2f}")
        st.write("---")

    # Exibe as métricas unificadas
    st.write("**Métricas de Desempenho**")
    st.write(
        f"- Similaridade (comparando as respostas): {similarity_openai * 100:.2f}%"
    )
    st.write(f"- Tempo Médio de Resposta (OpenAI): {avg_time_openai:.2f} segundos")
    st.write(f"- Tempo Médio de Resposta (BERT): {avg_time_bert:.2f} segundos")
    st.write("---")

    # Criação do DataFrame para exibir como tabela
    metrics_data = {
        "Modelo": ["OpenAI", "BERT"],
        "Similaridade (%)": [similarity_openai * 100, similarity_bert * 100],
        "Tempo Médio de Resposta (s)": [avg_time_openai, avg_time_bert],
    }

    df_metrics = pd.DataFrame(metrics_data)

    # Exibe a tabela de métricas
    st.write("### Tabela de Métricas")
    st.dataframe(df_metrics)

    # Criação de gráficos usando matplotlib e seaborn
    st.write("### Gráficos de Comparação")

    fig, ax = plt.subplots(1, 2, figsize=(12, 6))

    sns.barplot(x="Modelo", y="Similaridade (%)", data=df_metrics, ax=ax[0])
    ax[0].set_title("Comparação de Similaridade entre Modelos")

    sns.barplot(x="Modelo", y="Tempo Médio de Resposta (s)", data=df_metrics, ax=ax[1])
    ax[1].set_title("Comparação do Tempo Médio de Resposta entre Modelos")

    st.pyplot(fig)


# Função para limpar o histórico de conversas
def clear_conversation_history():
    st.session_state.historico_conversa = []


# Página de Chat
def chat_page(use_cloud, qdrant_url, qdrant_api_key, model_name):
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

    # Adiciona um botão para limpar o histórico de conversas
    if st.sidebar.button("Limpar Histórico"):
        clear_conversation_history()
        st.sidebar.write("Histórico de conversa limpo.")

    # Verifica se 'qa' já foi inicializado
    if "qa" not in st.session_state:
        st.warning(
            "O modelo de perguntas e respostas não foi inicializado. Verifique se o processamento foi realizado corretamente."
        )
        return

    user_input = st.text_input("Digite sua pergunta:", key="input")

    if st.button("Enviar"):
        process_user_input(user_input, st.session_state.qa, model_name)


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

        # Adiciona opção para selecionar o modelo de embeddings
        st.sidebar.title("Configurações de Embeddings")
        embedding_model = st.sidebar.selectbox(
            "Escolha o modelo de embeddings", options=["OpenAI", "BERT"]
        )

        if "vectorstore" not in st.session_state or "qa" not in st.session_state:
            vectorstore, qa = init_components(
                local=not use_cloud,
                qdrant_url=qdrant_url,
                qdrant_api_key=qdrant_api_key,
            )
            if not qa:
                st.error(
                    "Falha na inicialização do QA. Verifique os logs para mais detalhes."
                )
                return
        else:
            vectorstore = st.session_state.vectorstore
            qa = st.session_state.qa

        # Navegação de páginas
        st.sidebar.title("Navegação")
        page = st.sidebar.radio("Ir para", ["Chat", "Comparação de Modelos"])

        if page == "Chat":
            chat_page(use_cloud, qdrant_url, qdrant_api_key, embedding_model)
        elif page == "Comparação de Modelos":
            compare_embeddings_models(
                use_cloud, qdrant_url, qdrant_api_key, embedding_model
            )


if __name__ == "__main__":
    main()
