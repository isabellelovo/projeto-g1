# Análise Climática e Eventos Extremos no Brasil

Projeto acadêmico desenvolvido para a disciplina de **Linguagens de
Programação**, com foco em análise e visualização de dados climáticos e
construção de um dashboard interativo.

## Identificação

**Discente:** Isabelle Pinheiro Lovo\
**RA:** 1016112\
**Disciplina:** Linguagens de Programação\
**Docente:** Alexandre Neves Louzada

## Tema

**Análise Climática e Eventos Extremos no Brasil**

O projeto utiliza uma base de dados com informações climáticas de
diferentes regiões, estados e cidades brasileiras, entre os anos de
**2015 e 2024**.

A análise considera dados de temperatura, chuva, umidade, velocidade do
vento, eventos extremos e níveis de alerta.

## Objetivo

O objetivo é analisar as condições climáticas do Brasil entre 2015 e
2024, identificando variações ao longo do tempo e diferenças entre
regiões e cidades, com foco na ocorrência de eventos extremos e nos
níveis de alerta registrados.

As principais análises realizadas são:

-   comparação das condições climáticas entre regiões;
-   evolução dos eventos extremos ao longo dos anos;
-   quantidade de eventos extremos por região;
-   médias de temperatura e volume de chuva;
-   percentual de registros com eventos extremos;
-   relação entre temperatura, chuva, umidade, vento e eventos extremos.

## Tecnologias utilizadas

-   Python
-   Pandas
-   NumPy
-   Matplotlib
-   Seaborn
-   Plotly
-   Streamlit
-   Jupyter Notebook
-   GitHub

## Estrutura do projeto

``` text
projeto-g1/
│
├── app.py
├── requirements.txt
├── README.md
├── index.html
│
├── dados/
│   └── simulacao_clima_brasil.csv
│
└── notebooks/
    └── analise_clima.ipynb
```

## Indicadores utilizados

  -----------------------------------------------------------------------
  Indicador                           Descrição
  ----------------------------------- -----------------------------------
  Temperatura média                   Média da temperatura nos dados
                                      selecionados

  Chuva média                         Média do volume de chuva registrado

  Eventos extremos                    Total de eventos extremos
                                      registrados

  Registros com eventos               Percentual de registros que
                                      apresentam eventos extremos
  -----------------------------------------------------------------------

## Funcionalidades do dashboard

O dashboard desenvolvido em **Streamlit** permite:

-   filtrar os dados por ano, região e nível de alerta;
-   acompanhar os principais indicadores;
-   comparar temperatura, chuva e eventos extremos entre regiões;
-   visualizar a evolução dos eventos extremos ao longo dos anos;
-   comparar a ocorrência de eventos extremos entre regiões;
-   analisar a correlação entre as principais variáveis climáticas.

Os indicadores, tabelas e gráficos são atualizados de acordo com os
filtros selecionados.

## Como executar o projeto

Instale as dependências:

``` bash
pip install -r requirements.txt
```

Em seguida, execute o dashboard:

``` bash
streamlit run app.py
```

Para consultar a análise completa, abra o notebook:

``` text
notebooks/analise_clima.ipynb
```

## Etapas da análise

O desenvolvimento do projeto envolveu a leitura e preparação dos dados,
tratamento dos tipos das variáveis, criação de novos atributos, análise
exploratória, cálculo de indicadores e criação de visualizações.

Os resultados foram organizados em um dashboard para facilitar a
comparação entre diferentes períodos e regiões e tornar a interpretação
dos dados mais simples.

## Conclusão

O projeto permite analisar e comparar informações climáticas de
diferentes regiões e períodos do Brasil. Os indicadores e gráficos
ajudam a observar variações de temperatura e chuva, além da ocorrência
de eventos extremos e possíveis relações entre as variáveis analisadas.

O dashboard reúne as principais informações em uma interface interativa,
permitindo explorar diferentes recortes dos dados por meio dos filtros
disponíveis.
