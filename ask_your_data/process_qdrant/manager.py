from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from dotenv import load_dotenv
import os

load_dotenv(".ENV")
qdrant_api_key = os.environ.get("QDRANT_API_KEY")
qdrant_url = os.environ.get("QDRANT_URL")


def create_collection(name: str, size: int) -> None:
    """
    Cria uma coleção no banco de dados vetorial Qdrant.

    Parâmetros:
    -----------
    name : str
        Nome da coleção a ser criada.
    size : int
        Número de dimensões dos vetores que serão armazenados na coleção.

    Descrição:
    ----------
    Esta função conecta-se a um servidor Qdrant rodando localmente na porta 6333 e tenta criar
    uma nova coleção com o nome e o tamanho de vetor especificados. A coleção será configurada
    para utilizar a distância cosseno (COSINE) como métrica de similaridade entre os vetores.

    Caso a coleção já exista ou ocorra algum outro erro, a função captura a exceção e exibe
    uma mensagem de erro informando a falha.

    Exemplo de uso:
    ---------------
    create_collection(name="meu_vetor", size=128)
    """
    client = QdrantClient(host="localhost", port=6333)
    try:
        client.create_collection(
            collection_name=name,
            vectors_config=VectorParams(size=size, distance=Distance.COSINE),
        )
        print("Coleção criada com sucesso.")
    except Exception as e:
        print(f"Erro ao criar a coleção (possivelmente já existe): {e}")


def create_collection_cloud(name: str, size: int) -> None:

    # Connect to Qdrant Cloud
    qdrant_client = QdrantClient(
        url=qdrant_url,
        api_key=qdrant_api_key,
    )

    try:
        qdrant_client.create_collection(
            collection_name=name,
            vectors_config=VectorParams(size=size, distance=Distance.COSINE),
        )
        print("Coleção criada com sucesso.")
    except Exception as e:
        print(f"Erro ao criar a coleção (possivelmente já existe): {e}")
