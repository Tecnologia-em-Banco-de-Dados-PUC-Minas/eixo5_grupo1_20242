# Documentação de Contexto

![Projeto: AskYourData](/ask_your_data/assets/images/project_ask_your_data.png)

## [Lang-chain Overview](/ask_your_data/docs/langchain.md)


# Visão Geral

O projeto "Ask Your Data" foi desenvolvido como parte do curso de Arquitetura de Dados em Nuvem, com o objetivo de proporcionar uma solução prática e eficiente para consulta e processamento de documentos em formato PDF. Este projeto integra uma interface amigável desenvolvida em Streamlit, onde os usuários podem fazer upload de documentos, que serão processados para extração de texto e criação de embeddings. Esses dados vetoriais são então armazenados em um banco de dados vetorial (Qdrant), permitindo a consulta eficiente por similaridade utilizando um modelo de linguagem natural (LLM).

![Projeto: AskYourData](/ask_your_data/assets/images/image2.png)


## Objetivo do Projeto

O objetivo principal deste projeto é simplificar a interação do usuário com grandes volumes de documentos, permitindo que perguntas sejam feitas diretamente na interface e que as respostas sejam geradas com base no conteúdo contextualizado dos documentos carregados. Isso é alcançado através do processamento de texto e da utilização de técnicas avançadas de embeddings e busca por similaridade.


## Requisitos

Antes de começar, certifique-se de que seu sistema atende aos seguintes requisitos:

- **Windows Subsystem for Linux (WSL)**: Este projeto foi desenvolvido e testado utilizando o WSL, permitindo um ambiente Linux dentro do Windows.
  - [Guia de Instalação do WSL](https://docs.microsoft.com/pt-br/windows/wsl/install)

- **Python 3.11.5 ou superior**: O projeto requer o Python 3.11.5 ou uma versão superior para funcionar corretamente. Certifique-se de que essa versão do Python está instalada e ativa no seu ambiente.
  - [Download Python](https://www.python.org/downloads/)

- **Poetry**: Para gerenciamento de dependências e ambientes virtuais.
  - [Guia de Instalação do Poetry](https://python-poetry.org/docs/#installation)

- **Docker e Docker Compose**: Para configurar e executar o Qdrant em um contêiner.
  - [Guia de Instalação do Docker](https://docs.docker.com/get-docker/)
  - [Guia de Instalação do Docker Compose](https://docs.docker.com/compose/install/)

- **Git**: Para clonar o repositório do projeto.
  - [Guia de Instalação do Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)


## Instruções de Instalação

Siga os passos abaixo para configurar e executar o projeto na seção de [instalação](/ask_your_data/docs/instalacao.md).

---

## Tecnologias Utilizadas

- **Streamlit**: Ferramenta de criação de aplicações web interativas para permitir o upload e a interação com documentos PDF.
- **LangChain**: Framework utilizado para processamento de linguagem natural e geração de embeddings dos textos extraídos dos documentos.
- **Qdrant**: Vectorbase utilizado para armazenar e gerenciar os dados vetoriais gerados a partir dos embeddings, facilitando a busca por similaridade.
- **Python**: Linguagem de programação principal utilizada para o desenvolvimento do backend e integração das tecnologias mencionadas.

## Arquitetura do Sistema

A arquitetura do sistema é projetada para ser modular e eficiente, conforme ilustrado na figura anexada. Abaixo está um resumo dos principais componentes:

1. **Interface de Usuário (Streamlit)**: A interface permite que o usuário faça o upload de documentos PDF. Uma vez carregado, o documento é processado para extração de texto.

2. **Processamento e Embedding (LangChain)**: Após a extração do texto, o conteúdo é transformado em embeddings utilizando o LangChain. Esses embeddings são representações vetoriais dos textos, que preservam o contexto semântico.

3. **Armazenamento Vetorial (Qdrant)**: Os embeddings gerados são armazenados em um vectorbase Qdrant, que oferece consultas rápidas e eficientes por similaridade.

4. **Modelo de Busca (LLM)**: O modelo de linguagem (LLM) realiza a busca por similaridade nos embeddings armazenados, retornando a resposta que melhor corresponde ao contexto da pergunta feita pelo usuário na interface.

## Benefícios do Projeto

- **Facilidade de Uso**: A interface amigável permite que usuários com pouca experiência técnica possam interagir com o sistema de forma intuitiva.
- **Eficiência na Busca de Informação**: A utilização de embeddings e busca por similaridade proporciona respostas rápidas e contextualmente relevantes.
- **Flexibilidade e Escalabilidade**: O sistema é escalável, podendo ser facilmente adaptado para lidar com grandes volumes de documentos e consultas complexas.

## Conclusão

O projeto "Ask Your Data" oferece uma solução robusta para a consulta e processamento de documentos PDF em ambientes de dados, combinando a simplicidade de uso com tecnologias avançadas de processamento de linguagem natural. Com isso, atende às necessidades de usuários que precisam extrair informações valiosas de grandes volumes de documentos de maneira eficiente e precisa.