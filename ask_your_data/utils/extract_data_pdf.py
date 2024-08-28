import fitz  # PyMuPDF
import os


def extract_text_from_pdf(pdf_file: str, txt_file: str) -> str:
    """
    Extrai texto de um arquivo PDF e o salva em um arquivo de texto (.txt).

    Parâmetros:
    -----------
    pdf_file : str
        Caminho do arquivo PDF que você deseja processar.
    txt_file : str
        Caminho do arquivo .txt onde o texto extraído será salvo.

    Retorna:
    --------
    str
        Uma mensagem indicando o sucesso da operação ou detalhando um erro encontrado.

    Descrição:
    ----------
    Esta função abre um arquivo PDF, extrai o texto de cada página e o salva em um arquivo de texto (.txt).
    Ela verifica se o arquivo PDF existe antes de tentar processá-lo e grava o texto à medida que cada página é processada,
    o que é mais eficiente em termos de memória para arquivos grandes. Se ocorrer algum erro durante o processo, a função
    retornará uma mensagem de erro detalhada.

    Exemplo de uso:
    ---------------
    pdf_file = ".assets/pdf/arquivo_pdf.pdf"
    txt_file = ".assets/txt/extracted_text.txt"
    result = extract_text_from_pdf(pdf_file, txt_file)
    print(result)
    """
    try:
        # Verifica se o arquivo PDF existe
        if not os.path.exists(pdf_file):
            return f"Erro: O arquivo PDF {pdf_file} não foi encontrado."

        # Abre o arquivo PDF
        pdf_document = fitz.open(pdf_file)

        # Abre o arquivo .txt para escrita
        with open(txt_file, "w", encoding="utf-8") as file:
            for page_num in range(len(pdf_document)):
                # Carrega cada página e extrai o texto
                page = pdf_document.load_page(page_num)
                page_text = page.get_text()

                # Escreve o texto da página diretamente no arquivo
                file.write(page_text)

        # Fecha o arquivo PDF
        pdf_document.close()

        return f"Texto extraído e salvo em: {txt_file}"

    except Exception as e:
        return f"Erro ao processar o arquivo PDF: {str(e)}"
