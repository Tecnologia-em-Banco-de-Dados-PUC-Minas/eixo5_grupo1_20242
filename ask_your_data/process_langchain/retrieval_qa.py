from langchain_openai import OpenAI
from langchain.chains import RetrievalQA


def create_retrieval_qa(vectorstore) -> RetrievalQA:
    """
    Cria uma cadeia de perguntas e respostas (QA) baseada em recuperação de informações, utilizando embeddings vetoriais.

    Parâmetros:
    -----------
    vectorstore : Qdrant
        O armazenamento vetorial (vectorstore) configurado para recuperação de informações, utilizado para buscar
        e recuperar embeddings relevantes em resposta a perguntas.

    Retorna:
    --------
    RetrievalQA
        Um objeto de cadeia de perguntas e respostas (`RetrievalQA`) que utiliza um modelo de linguagem e um
        sistema de recuperação de informações para fornecer respostas.

    Descrição:
    ----------
    Esta função cria uma cadeia de perguntas e respostas utilizando o módulo `RetrievalQA` da biblioteca LangChain.
    O `RetrievalQA` é configurado para utilizar o modelo de linguagem OpenAI (`llm=OpenAI()`) em conjunto com um
    retriever, que é derivado do armazenamento vetorial (`vectorstore`). O tipo de cadeia especificado é "stuff",
    que determina como as respostas serão geradas a partir das informações recuperadas.

    A função assume que o `vectorstore` fornecido já está configurado para recuperar embeddings vetoriais relevantes
    para as consultas realizadas pelo modelo de linguagem.

    Exemplo de uso:
    ---------------
    vectorstore = initialize_embeddings(collection_name="minha_colecao", client=client)
    qa_system = create_retrieval_qa(vectorstore=vectorstore)
    resposta = qa_system.run("Qual é a capital da França?")
    """
    qa = RetrievalQA.from_chain_type(
        llm=OpenAI(), chain_type="stuff", retriever=vectorstore.as_retriever()
    )
    return qa
