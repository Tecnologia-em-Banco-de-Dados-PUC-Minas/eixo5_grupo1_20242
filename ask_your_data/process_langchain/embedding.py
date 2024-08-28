from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_community.vectorstores import Qdrant


def initialize_embeddings(collection_name: str, client) -> Qdrant:
    """
    Inicializa o armazenamento vetorial com embeddings do OpenAI para uma coleção específica no Qdrant.

    Parâmetros:
    -----------
    collection_name : str
        O nome da coleção no Qdrant onde os embeddings serão armazenados e acessados.
    client :
        Instância do cliente Qdrant, usada para interagir com o banco de dados vetorial.

    Retorna:
    --------
    Qdrant
        Um objeto Qdrant configurado para armazenar e recuperar embeddings vetoriais.

    Descrição:
    ----------
    Esta função inicializa um sistema de armazenamento vetorial utilizando embeddings do OpenAI.
    O armazenamento vetorial é associado a uma coleção específica no Qdrant, que é identificada
    pelo nome fornecido. A função utiliza o cliente Qdrant fornecido para se conectar e operar
    no banco de dados vetorial.

    O módulo `OpenAIEmbeddings` é utilizado para gerar embeddings vetoriais a partir de texto,
    e esses embeddings são então armazenados e gerenciados no Qdrant.

    Exemplo de uso:
    ---------------
    client = QdrantClient(host="localhost", port=6333)
    vectorstore = initialize_embeddings(collection_name="minha_colecao", client=client)
    """
    embeddings = OpenAIEmbeddings()
    vectorstore = Qdrant(
        client=client, collection_name=collection_name, embeddings=embeddings
    )
    return vectorstore
