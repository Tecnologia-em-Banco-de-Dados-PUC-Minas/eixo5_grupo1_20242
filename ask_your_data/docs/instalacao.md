## Instruções de Instalação

Siga os passos abaixo para configurar e executar o projeto:
---

## Configuração e Execução

### Docker Compose para Qdrant

1. Crie um arquivo `docker-compose.yml` com o seguinte conteúdo:

    ```yaml
    version: '3'
    services:
      qdrant:
        image: qdrant/qdrant
        ports:
          - 6333:6333
          - 6334:6334
        volumes:
          - ./qdrant_storage:/qdrant/storage:z
        environment:
          - ENV_VARIABLE=value
    ```

2. Execute o seguinte comando na pasta onde se encontra o projeto:

    ```bash
    docker-compose up
    ```

![qdrant-docker-compose](/ask_your_data/assets/images/qdrant_docker_compose.png)


### Acessar o Dashboard do Qdrant

Após iniciar o Qdrant com Docker, acesse o dashboard no seu navegador através do seguinte endereço:

[http://localhost:6333/dashboard](http://localhost:6333/dashboard)

![qdrant-database](/ask_your_data/assets/images/qdrant.png)

---

## Instalação de Dependências com Poetry

### 1. Instalar Dependências

Com o **Poetry** instalado, rode o seguinte comando para instalar todas as dependências do projeto:

```bash
poetry install
```

### 2. Ativar o Ambiente Virtual

Ative o ambiente virtual criado pelo Poetry com o comando:

```bash
poetry shell
```

### 3. Instalação de Dependências Adicionais

Se houver dependências adicionais, elas devem ser incluídas no arquivo `pyproject.toml`. Para adicionar qualquer uma das bibliotecas listadas, use o comando:

```bash
poetry add nome_da_biblioteca
```

### Aqui estão as bibliotecas utilizadas no projeto:

- **Qdrant Client:** 

    ```bash
    poetry add qdrant-client
    ```

    Esta biblioteca permite a interação com o servidor Qdrant, utilizado como vectorbase para armazenar e buscar dados vetoriais gerados a partir dos embeddings. O Qdrant é essencial para consultas eficientes por similaridade no projeto.

- **LangChain:** 

    ```bash
    poetry add langchain
    ```

    Um framework que facilita o desenvolvimento de aplicativos de linguagem natural, especialmente aqueles que envolvem a manipulação e processamento de grandes quantidades de texto. No projeto, é usado para criar e manipular embeddings a partir do texto extraído dos PDFs.

- **LangChain-Community:** 

    ```bash
    poetry add langchain-community
    ```

    Extensão da LangChain que fornece módulos e funcionalidades adicionais desenvolvidos pela comunidade, complementando o uso básico do LangChain. Pode incluir integrações com outros serviços ou funcionalidades para melhorar o desempenho do processamento de linguagem natural.

- **Python-dotenv:** 

    ```bash
    poetry add python-dotenv
    ```

    Utilizada para carregar variáveis de ambiente a partir de um arquivo `.env`. Facilita a configuração de variáveis sensíveis ou variáveis que variam entre diferentes ambientes, sem precisar codificá-las diretamente no código.

- **OpenAI:** 

    ```bash
    poetry add openai
    ```

    Fornece uma interface para interagir com os modelos de linguagem da OpenAI, como o GPT. No contexto deste projeto, pode ser usada para gerar respostas ou fazer processamento de linguagem natural mais complexo com base nos dados extraídos dos PDFs.

- **TikToken:** 

    ```bash
    poetry add tiktoken
    ```

    Biblioteca usada para tokenização de texto, especialmente útil ao trabalhar com modelos de linguagem que exigem que o texto seja dividido em tokens. Isso é fundamental para processar o texto de maneira eficiente e dentro dos limites de tokens que muitos modelos de linguagem impõem.

- **LangChain-OpenAI:** 

    ```bash
    poetry add langchain-openai
    ```

    Integração específica da LangChain com os serviços da OpenAI. Facilita a utilização dos modelos da OpenAI dentro do framework LangChain, combinando as funcionalidades de ambos para melhorar o fluxo de trabalho no projeto.

- **PyPDF2:** 

    ```bash
    poetry add PyPDF2
    ```

    Biblioteca Python para manipulação de arquivos PDF. No projeto, é usada para extrair texto dos documentos PDF carregados pelos usuários, permitindo que o conteúdo seja processado e transformado em embeddings.

- **PyMuPDF:** 

    ```bash
    poetry add PyMuPDF
    ```

    Outra biblioteca para manipulação de PDFs, oferece funcionalidades avançadas para trabalhar com PDFs e outros formatos de documentos. Pode ser usada em conjunto com o PyPDF2 para extrair texto ou metadados de documentos PDF.

- **Streamlit:** 

    ```bash
    poetry add streamlit
    ```

    Principal biblioteca para criar a interface web do projeto. Permite o desenvolvimento rápido de aplicações web interativas, onde os usuários podem carregar PDFs, visualizar os resultados das consultas e interagir com o sistema.

- **Streamlit Chat:** 

    ```bash
    poetry add streamlit-chat
    ```

    Extensão do Streamlit que adiciona funcionalidades de chat à interface web, permitindo que o usuário interaja de maneira mais natural e conversacional com o sistema. No contexto do projeto, isso é útil para que os usuários possam fazer perguntas e receber respostas diretamente na interface.


## OpenAI API Key

Gere sua API Key da OpenAI acessando [OpenAI Platform](https://platform.openai.com/api-keys). Por questões de segurança, nunca compartilhe sua chave API publicamente.


## Configuração das Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto para armazenar a variável API Key da OpenAI. Aqui está um exemplo de como seu arquivo `.env` pode ser configurado:

```bash
OPENAI_API_KEY='=sua_api_key'
```


## Executando o Projeto

Após a instalação de todas as dependências e a configuração do Qdrant, execute seu aplicativo Streamlit usando:

```bash
streamlit run seu_arquivo_app.py
```

Substitua `seu_arquivo_app.py` pelo nome do seu arquivo principal do Streamlit.


## Acesse a Aplicação

Após iniciar o Streamlit, acesse a aplicação no seu navegador através do seguinte endereço:

```
http://localhost:8501
```


## Estrutura do Projeto

Abaixo está uma visão geral da estrutura do projeto:

```plaintext
ask_your_data/
│
├── .github/                  # Configurações específicas do GitHub
│   └── workflows/            # Workflows do GitHub Actions
│       └── ci.yml            # Arquivo de configuração do workflow de CI
│
├── ask_your_data/            # Diretório principal do aplicativo
│
├── assets/                   # Diretório de recursos
│
├── data/                     # Diretório para armazenamento de dados
│
├── docs/                     # Documentação do projeto
│
├── process_langchain/        # Scripts e funções relacionados ao processamento com LangChain
│
├── process_qdrant/           # Scripts e funções relacionados ao processamento com Qdrant
│
├── qdrant_storage/           # Diretório de armazenamento do Qdrant
│
├── tests/                    # Diretório contendo os testes do projeto
│
├── utils/                    # Funções utilitárias e helpers
│
├── .ENV                      # Arquivo de variáveis de ambiente (note o nome em maiúsculas)
│
├── app.py                    # Arquivo principal para rodar o aplicativo Streamlit
├── docker-compose.yml        # Arquivo de configuração do Docker Compose
├── poetry.lock               # Arquivo de dependências gerado pelo Poetry
├── pyproject.toml            # Arquivo de configuração do Poetry
├── test.py                   # Arquivo de teste (individual)
├── .gitignore                # Arquivo para ignorar arquivos e diretórios no Git
├── .pre-commit-config.yaml   # Configurações para pre-commit hooks
└── README.md                 # Arquivo README do projeto
```


## Tecnologias Utilizadas

- **Streamlit**: Criação da interface web interativa.
- **LangChain**: Processamento de linguagem natural e geração de embeddings.
- **Qdrant**: Armazenamento e gestão dos embeddings vetoriais.
- **Python 3.11.5 ou superior**: Linguagem de programação principal.
- **Poetry**: Gerenciamento de dependências e ambientes virtuais.
- **Docker e Docker Compose**: Configuração e execução do Qdrant em contêineres.


## Contribuições

Contribuições são bem-vindas! Se você deseja melhorar este projeto, sinta-se à vontade para enviar um *pull request* ou abrir uma *issue*.


## Licença

Este projeto é licenciado sob os termos da [MIT License](LICENSE).


## Suporte

Se você encontrar qualquer problema ao configurar ou executar o projeto, sinta-se à vontade para abrir uma *issue* no repositório ou entrar em contato.
