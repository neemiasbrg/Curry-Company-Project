# Cury Company - Análise de KPIs Estratégicos

## 1. Problema de Negócio

A Cury Company é uma empresa de tecnologia que desenvolveu um aplicativo que conecta restaurantes, entregadores e clientes. O aplicativo permite a realização de pedidos em qualquer restaurante cadastrado e sua entrega através de entregadores também registrados. A empresa gera uma grande quantidade de dados sobre entregas, tipos de pedidos, condições climáticas, avaliações dos entregadores, entre outros.

Apesar do crescimento constante nas entregas, o CEO não tem visibilidade completa dos KPIs estratégicos de crescimento da empresa. Como Cientista de Dados, seu desafio é criar uma solução que organize os principais KPIs em uma única ferramenta para auxiliar o CEO na tomada de decisões importantes.

### Modelo de Negócio

O modelo de negócio da Cury Company é baseado em um Marketplace, intermedindo negócios entre três clientes principais:
- Restaurantes
- Entregadores
- Clientes (pessoas compradoras)

Para acompanhar o crescimento, o CEO gostaria de visualizar as seguintes métricas:

#### Do lado da empresa:
1. Quantidade de pedidos por dia.
2. Quantidade de pedidos por semana.
3. Distribuição dos pedidos por tipo de tráfego.
4. Comparação do volume de pedidos por cidade e tipo de tráfego.
5. Quantidade de pedidos por entregador por semana.
6. Localização central de cada cidade por tipo de tráfego.

#### Do lado dos entregadores:
1. Menor e maior idade dos entregadores.
2. Pior e melhor condição dos veículos.
3. Avaliação média por entregador.
4. Avaliação média e desvio padrão por tipo de tráfego.
5. Avaliação média e desvio padrão por condições climáticas.
6. Top 10 entregadores mais rápidos por cidade.
7. Top 10 entregadores mais lentos por cidade.

#### Do lado dos restaurantes:
1. Quantidade de entregadores únicos.
2. Distância média entre restaurantes e locais de entrega.
3. Tempo médio e desvio padrão de entrega por cidade.
4. Tempo médio e desvio padrão de entrega por cidade e tipo de pedido.
5. Tempo médio e desvio padrão de entrega por cidade e tipo de tráfego.
6. Tempo médio de entrega durante festivais.

## 2. Premissas Assumidas para a Análise

1. A análise foi realizada com dados entre 11/02/2022 e 06/04/2022.
2. O modelo de negócio considerado foi o Marketplace.
3. As três principais visões do negócio são: Visão de transações de pedidos, visão de restaurantes e visão de entregadores.

## 3. Estratégia da Solução

O painel estratégico foi desenvolvido com base nas seguintes visões e métricas:

### Visão do Crescimento da Empresa
1. Pedidos por dia.
2. Porcentagem de pedidos por condições de trânsito.
3. Quantidade de pedidos por tipo e por cidade.
4. Pedidos por semana.
5. Quantidade de pedidos por tipo de entrega.
6. Quantidade de pedidos por condições de trânsito e tipo de cidade.

### Visão do Crescimento dos Restaurantes
1. Quantidade de pedidos únicos.
2. Distância média percorrida.
3. Tempo médio de entrega durante festivais e dias normais.
4. Desvio padrão do tempo de entrega durante festivais e dias normais.
5. Tempo médio de entrega por cidade.
6. Distribuição do tempo médio de entrega por cidade.
7. Tempo médio de entrega por tipo de pedido.

### Visão do Crescimento dos Entregadores
1. Idade do entregador mais velho e do mais novo.
2. Avaliação do melhor e do pior veículo.
3. Avaliação média por entregador.
4. Avaliação média por condições de trânsito.
5. Avaliação média por condições climáticas.
6. Tempo médio dos entregadores mais rápidos.
7. Tempo médio dos entregadores mais rápidos por cidade.

## 4. Top 3 Insights de Dados

1. A sazonalidade da quantidade de pedidos é diária, com uma variação de aproximadamente 10% entre dias consecutivos.
2. Cidades do tipo Semi-Urban não apresentam condições baixas de trânsito.
3. As maiores variações no tempo de entrega ocorrem durante o clima ensolarado.

## 5. Produto Final do Projeto

O produto final é um painel online hospedado em nuvem, acessível a partir de qualquer dispositivo conectado à internet. O painel pode ser acessado através do seguinte link: [Painel Cury Company](https://project-currycompany.streamlit.app/)

## 6. Conclusão

O objetivo do projeto foi criar um conjunto de gráficos e tabelas que exibem as métricas de forma clara e útil para o CEO. Observou-se que o número de pedidos cresceu entre a semana 06 e a semana 13 do ano de 2022.

## 7. Próximos Passos

1. Reduzir o número de métricas.
2. Criar novos filtros.
3. Adicionar novas visões de negócio.
