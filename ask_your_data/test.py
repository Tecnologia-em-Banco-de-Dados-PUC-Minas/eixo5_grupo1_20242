from qdrant_client import QdrantClient
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente
load_dotenv(".ENV")
qdrant_url = os.environ.get("QDRANT_URL")
qdrant_api_key = os.environ.get("QDRANT_API_KEY")

print(f"Qdrant URL: {qdrant_url}")
print(f"Qdrant API Key: {qdrant_api_key}")


# Tente conectar ao Qdrant Cloud
try:
    client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
    # Testar a conexão obtendo a lista de coleções
    collections = client.get_collections()
    print("Conexão ao Qdrant Cloud estabelecida com sucesso!")
    print("Coleções disponíveis:", collections)
except Exception as e:
    print(f"Erro ao conectar ao Qdrant Cloud: {e}")
