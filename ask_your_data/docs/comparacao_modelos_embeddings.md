# Comparação de Modelos de Embeddings para Busca Contextual

## Introdução

Neste projeto, implementamos uma interface que permite comparar diferentes modelos de embeddings (OpenAI e BERT) para avaliar qual deles oferece o melhor desempenho em tarefas de busca contextual em documentos PDF. A comparação é realizada com base em consultas feitas pelos usuários e na análise das respostas geradas pelos modelos.

## Objetivo

O objetivo principal desta etapa é comparar a eficácia dos modelos de embeddings OpenAI e BERT na tarefa de responder a consultas contextuais. Queremos determinar qual modelo é mais preciso e relevante, considerando a similaridade semântica das respostas geradas.

## Metodologia de Avaliação

### Processamento de Dados

1. **Upload de PDFs:** O sistema permite que os usuários façam upload de arquivos PDF, que são então processados para extrair o texto.
2. **Criação de Embeddings:** O texto extraído dos PDFs é convertido em embeddings utilizando os modelos selecionados (OpenAI ou BERT).
3. **Armazenamento em Vector Store:** Os embeddings são armazenados em um banco de dados vetorial (Qdrant), permitindo a recuperação eficiente de informações.

### Comparação de Modelos

1. **Consultas Baseadas no Histórico:** As consultas feitas pelos usuários durante as interações são registradas e usadas para comparar os modelos.
2. **Similaridade Semântica:** Em vez de comparar as respostas dos modelos diretamente como strings, utilizamos a **similaridade de cosseno** para avaliar o quão semelhantes as respostas são em termos semânticos.
   - **TF-IDF e Cosine Similarity:** As respostas são transformadas em vetores TF-IDF, e a similaridade de cosseno entre as respostas dos dois modelos é calculada.
   - **Limiar de Similaridade:** Considera-se que as respostas são "iguais" se a similaridade de cosseno for maior que 0.8.

### Métricas de Desempenho

As seguintes métricas são calculadas para avaliar o desempenho dos modelos:

1. **Precisão:** Proporção de consultas em que as respostas dos dois modelos são consideradas "similares" com base na similaridade de cosseno.
2. **Relevância:** Neste contexto, a relevância é tratada de maneira semelhante à precisão, pois estamos avaliando a similaridade semântica.
3. **Tempo Médio de Resposta:** O tempo médio que cada modelo leva para gerar uma resposta para as consultas.

### Exibição dos Resultados

- **Respostas Geradas:** As respostas de ambos os modelos são exibidas lado a lado para cada consulta.
- **Similaridade de Cosine:** A similaridade entre as respostas dos dois modelos é mostrada.
- **Métricas:** A precisão e o tempo médio de resposta de cada modelo são calculados e exibidos.

## Resultados

Os resultados mostram como os modelos OpenAI e BERT se comportam em termos de precisão e eficiência. A similaridade de cosseno permite uma avaliação mais robusta das respostas, considerando a similaridade semântica e não apenas a correspondência textual exata.

### Tabela de Métricas

![Tabela de Métricas](file-7sBwzXzjcsMVZsLsj9kotrSU)

### Gráficos de Comparação

![Gráficos de Comparação](file-ueAHlSXCPZR4WMkULNAv929K)

## Discussão

### Análise dos Resultados

- **Trade-offs Identificados:** A similaridade semântica proporciona uma visão mais precisa do desempenho dos modelos em tarefas contextuais, especialmente quando as respostas não são idênticas, mas transmitem a mesma informação.
- **Casos Específicos:** Analisamos situações em que as respostas dos modelos diferem ligeiramente em termos de texto, mas são semanticamente equivalentes. Isso é especialmente importante para tarefas de busca contextual onde sinônimos e reformulações são comuns.

### Justificativa para a Escolha Final

Com base nos resultados da comparação, o modelo que atingir maior precisão sem sacrificar significativamente o tempo de resposta pode ser considerado o mais adequado para o sistema. No entanto, a escolha final pode depender também de outros fatores, como o contexto específico das consultas e as necessidades dos usuários.

## Conclusão

Este projeto demonstra a importância de utilizar métricas de similaridade semântica para comparar modelos de embeddings em tarefas de NLP. A abordagem baseada em Cosine Similarity permite uma avaliação mais precisa do desempenho dos modelos, refletindo a verdadeira qualidade das respostas geradas.

---

Esse README agora inclui as imagens dos gráficos e da tabela de métricas, proporcionando uma visão mais completa dos resultados e da análise. Se precisar de mais alguma coisa, estarei por aqui para ajudar!