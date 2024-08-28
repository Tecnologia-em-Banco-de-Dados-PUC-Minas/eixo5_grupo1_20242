from langchain.text_splitter import CharacterTextSplitter
from PyPDF2 import PdfReader


def get_chunks(text: str) -> list:
    """
    Divide o texto em blocos menores (chunks) utilizando um delimitador específico.

    Parâmetros:
    -----------
    text : str
        O texto completo que será dividido em blocos menores.

    Retorna:
    --------
    list
        Uma lista de strings, onde cada string é um bloco (chunk) de texto.

    Descrição:
    ----------
    Esta função utiliza o `CharacterTextSplitter` da biblioteca LangChain para dividir o texto em
    blocos menores. O delimitador para a divisão é uma quebra de linha ("\n"). Cada bloco terá
    um tamanho máximo de 1000 caracteres, com uma sobreposição de 200 caracteres entre blocos consecutivos,
    para garantir que o contexto não se perca entre os blocos.

    Exemplo de uso:
    ---------------
    text = "Seu texto aqui..."
    chunks = get_chunks(text)
    """
    text_splitter = CharacterTextSplitter(
        separator="\n", chunk_size=1000, chunk_overlap=200, length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def process_files(files) -> str:
    """
    Extrai e processa texto de um ou mais arquivos PDF.

    Parâmetros:
    -----------
    files : list[PdfReader] | PdfReader
        Um único objeto `PdfReader` ou uma lista de objetos `PdfReader`, representando os arquivos PDF
        que serão processados.

    Retorna:
    --------
    str
        O texto extraído de todas as páginas dos arquivos PDF, concatenado em uma única string.

    Descrição:
    ----------
    Esta função processa um ou mais arquivos PDF e extrai o texto de cada página. Se `files` contiver um
    único `PdfReader`, ele é automaticamente transformado em uma lista de um item para que o código possa
    processá-lo da mesma forma que faria com múltiplos arquivos.

    Para cada página de cada arquivo PDF, o texto é extraído e concatenado em uma única string, com uma
    quebra de linha adicionada entre o texto de diferentes páginas para manter a legibilidade.

    Exemplo de uso:
    ---------------
    reader = PdfReader("seu_arquivo.pdf")
    text = process_files(reader)
    """
    text = ""

    # Se 'files' for um único PdfReader, transforme-o em uma lista de um item
    if isinstance(files, PdfReader):
        files = [files]

    # Processa cada arquivo PDF
    for file in files:
        for page in file.pages:
            page_text = page.extract_text()
            if page_text:  # Verifica se há texto na página
                text += page_text + "\n"  # Adiciona uma nova linha entre as páginas

    return text
