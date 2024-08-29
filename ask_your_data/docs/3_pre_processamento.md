# Etapa 3 - PRÉ-PROCESSAMENTO DE DADOS

## Visão Geral

Nesta etapa, focamos na extração e processamento do conteúdo textual de documentos PDF. A funcionalidade central envolve a conversão de arquivos PDF carregados em arquivos de texto (.txt) para facilitar o processamento subsequente e a análise de dados.

## Objetivo

O objetivo desta etapa é transformar documentos PDF, que contêm informações não estruturadas, em arquivos de texto estruturados. Isso permite que o conteúdo dos documentos seja acessado e analisado de forma mais eficiente em etapas posteriores do projeto.

## Processo de Extração

1. **Carregamento de Arquivos PDF:**
   - Os usuários carregam os documentos PDF relevantes através da interface do sistema. Esses documentos podem conter informações críticas, como procedimentos internos de empresas, que precisam ser analisados em detalhe.

2. **Salvamento e Organização dos Arquivos:**
   - Cada arquivo PDF carregado é salvo em um diretório específico. Isso garante que todos os documentos estejam armazenados de forma organizada e acessível.

3. **Extração de Texto:**
   - O conteúdo textual dos PDFs é extraído utilizando ferramentas especializadas. Esse texto extraído é então salvo em arquivos de texto (.txt), um para cada documento PDF. O uso de arquivos de texto facilita a manipulação e análise do conteúdo extraído.

4. **Tratamento Básico dos Dados:**
   - Após a extração, é realizada uma limpeza básica no texto para remover ruídos como caracteres especiais ou quebras de linha desnecessárias. Isso garante que o texto esteja em um formato mais adequado para análise.

## Importância no Contexto do Projeto

A extração de dados dos PDFs é uma etapa crucial no fluxo de trabalho do projeto. Ela permite que informações importantes, anteriormente encapsuladas em documentos não estruturados, sejam transformadas em dados estruturados e acessíveis. Esses dados serão posteriormente utilizados para treinar modelos de aprendizado de máquina, realizar análises contextuais, e fornecer respostas precisas em consultas de busca.

## Ferramentas Utilizadas

- **Bibliotecas de Extração de Texto:** Ferramentas como `PyPDF2` ou `pdfminer` são empregadas para capturar o conteúdo textual dos PDFs.
- **Armazenamento Estruturado:** Os arquivos de texto (.txt) são organizados em diretórios específicos para facilitar o acesso e o processamento nas etapas subsequentes do projeto.

## Resultados Esperados

Com a implementação deste módulo, espera-se que todo o conteúdo relevante dos documentos PDF seja convertido em um formato estruturado e pronto para análise. Esse processo de extração é essencial para garantir que os dados estejam disponíveis para serem utilizados eficazmente nos modelos de aprendizado de máquina e nas análises contextuais que se seguem.