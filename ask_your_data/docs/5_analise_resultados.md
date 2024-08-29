# Etapa 5 - ANÁLISE DOS RESULTADOS

## Visão Geral

Na quinta etapa do projeto "ASK YOUR DATA", o foco é a análise detalhada dos resultados obtidos a partir dos diferentes modelos de aprendizado de máquina aplicados para melhorar o sistema de recuperação de informações em documentos PDF. Esta análise tem como objetivo interpretar as métricas de desempenho dos modelos, identificar os fatores que mais impactam a qualidade das respostas e determinar as melhores práticas para otimizar o sistema.

## Objetivo

O principal objetivo desta etapa é compreender como os diferentes modelos de embeddings (OpenAI e BERT) e os parâmetros do sistema de recuperação de informações influenciam nos resultados. A análise inclui a interpretação de métricas como **similaridade semântica** e **tempo médio de resposta** para avaliar a eficácia dos modelos implementados. O intuito é identificar o modelo que melhor performa no contexto do projeto, garantindo que o sistema esteja otimizado para fornecer respostas precisas e relevantes.

## Etapas do Processo

### 1. **Obtenção das Métricas de Desempenho**

Após a implementação dos modelos de embeddings e a execução de experimentos de recuperação de informações, coletamos as seguintes métricas para avaliar o desempenho do sistema:

- **Similaridade (%)**: Esta métrica avalia o quão semelhantes as respostas dos dois modelos (OpenAI e BERT) são em termos semânticos. A similaridade é calculada com base na **similaridade de cosseno** entre os vetores de respostas dos modelos. Um valor alto indica que as respostas dos modelos são muito semelhantes em termos de conteúdo semântico.

- **Tempo Médio de Resposta**: Mede o tempo médio que cada modelo leva para gerar uma resposta às consultas. Esta métrica é importante para avaliar a eficiência do modelo, especialmente em cenários onde a rapidez de resposta é crucial.

### 2. **Interpretação dos Resultados**

Nesta etapa, analisamos as métricas coletadas para compreender o desempenho dos modelos:

- **Similaridade (%)**: Comparamos os valores de similaridade entre as respostas dos modelos OpenAI e BERT para identificar qual deles gera respostas mais semanticamente semelhantes.
  
- **Tempo Médio de Resposta**: Comparamos o tempo médio de resposta entre os dois modelos para identificar qual deles oferece respostas mais rápidas sem comprometer a precisão semântica.

### 3. **Exploração das Variáveis de Entrada**

A análise também incluiu a exploração de como diferentes variáveis de entrada (como o tipo de documento, o contexto da pergunta, etc.) impactam os resultados dos modelos:

- **Identificação das Variáveis mais Relevantes**: Analisamos quais variáveis de entrada influenciam mais as respostas dos modelos, ajudando a entender em quais contextos cada modelo performa melhor.

- **Ajuste de Parâmetros**: Com base nas variáveis mais influentes, ajustamos os parâmetros dos modelos de recuperação para otimizar o desempenho.

### 4. **Comparação entre Modelos de Embeddings**

Realizamos uma comparação direta entre os modelos de embeddings (OpenAI e BERT), levando em consideração as métricas coletadas e a interpretação dos resultados:

- **Desempenho dos Modelos**: Avaliamos qual dos modelos de embeddings proporcionou o melhor equilíbrio entre similaridade semântica e tempo de resposta.

- **Robustez dos Modelos**: Além da similaridade, consideramos como cada modelo se comportou em diferentes cenários, incluindo variações no tipo de perguntas e na complexidade dos documentos.

### 5. **Documentação dos Resultados**

Toda a documentação dos resultados, incluindo gráficos de comparação, tabelas de métricas e a análise detalhada da similaridade entre os modelos, foi organizada para facilitar a revisão e o refinamento contínuo do sistema.

- **Introdução aos Modelos Testados**: Explicamos a escolha dos modelos OpenAI e BERT, destacando suas principais características e diferenças.
- **Metodologia de Avaliação**: Detalhamos o processo experimental, incluindo as perguntas utilizadas e as métricas aplicadas para avaliar o desempenho dos modelos.
- **Resultados**: Apresentamos os resultados dos experimentos, utilizando gráficos e análises detalhadas para demonstrar o desempenho de cada modelo.
- **Discussão**: Analisamos os resultados, identificando os trade-offs e justificando a escolha final do modelo mais adequado.

### 6. **Considerações Finais**

As conclusões tiradas nesta etapa fornecem uma base sólida para a implementação final do sistema "ASK YOUR DATA". A partir dos resultados obtidos, continuaremos a refinar o modelo selecionado, garantindo que o sistema ofereça respostas precisas e relevantes para os usuários.

### Resultados e Análises Visuais

#### Tabela de Métricas

![Tabela de Métricas](/ask_your_data/assets/images/result1.png)

#### Gráficos de Comparação

![Gráficos de Comparação](/ask_your_data/assets/images/result2.png)

---

### **Notas Finais**

Esta etapa foi fundamental para consolidar os aprendizados obtidos ao longo do projeto e fornecer uma visão clara sobre o desempenho dos diferentes modelos de embeddings e seus impactos no sistema de recuperação de informações. As conclusões tiradas aqui irão guiar os próximos passos, assegurando que o sistema esteja bem preparado para atender às necessidades dos usuários.