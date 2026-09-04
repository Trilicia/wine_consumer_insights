# PIWI Consumer Insights

Projeto de análise de dados sobre o comportamento de consumidores de vinho e a percepção de sustentabilidade em vinhos produzidos com uvas PIWI.

## Problema de negócio

Como transformar a sustentabilidade em uma proposta de valor relevante para consumidores de vinho, considerando seus perfis, hábitos de consumo, critérios de compra e canais de aquisição?

## Objetivo

Investigar como o perfil dos consumidores, os hábitos de consumo, os critérios de compra e os canais de aquisição podem contribuir para uma estratégia de posicionamento de vinhos sustentáveis.

## Tecnologias utilizadas

* Python
* Pandas
* Matplotlib
* Seaborn
* SQL
* SQLite
* HTML
* CSS
* JavaScript
* Git e GitHub

## Etapas do projeto

* [x] Estruturação do projeto
* [x] Carregamento da base
* [x] Auditoria inicial
* [x] Limpeza e padronização
* [x] Tratamento das perguntas de múltipla escolha
* [x] Criação de variáveis analíticas
* [x] Modelagem do banco SQLite
* [x] Criação de views e consultas SQL
* [x] Testes de qualidade dos dados
* [ ] Análise exploratória
* [ ] Criação dos gráficos
* [ ] Construção do dashboard interativo
* [ ] Elaboração das recomendações finais

## Base de dados

A base contém 261 respostas anônimas de uma pesquisa sobre:

* perfil sociodemográfico;
* frequência de consumo de vinho;
* nível de conhecimento sobre vinhos;
* tipos de vinho preferidos;
* canais de aquisição;
* fatores considerados na compra;
* atributos valorizados em vinhos sustentáveis;
* importância da comunicação de sustentabilidade no rótulo.

O arquivo original é mantido em:

```text
data/raw/dados_piwi.xlsx
```

A base original não é alterada durante o processamento.

## Estrutura do projeto

```text
piwi_consumer_insights/
├── dashboard/
├── data/
│   ├── processed/
│   └── raw/
│       └── dados_piwi.xlsx
├── reports/
├── sql/
│   ├── 01_create_views.sql
│   ├── 02_business_queries.sql
│   └── 03_quality_checks.sql
├── src/
│   ├── 01_data_audit.py
│   ├── 02_data_cleaning.py
│   ├── 03_multiselect_processing.py
│   ├── 04_feature_engineering.py
│   ├── 05_database_load.py
│   ├── 06_sql_analysis.py
│   └── 07_exploratory_analysis.py
├── .gitignore
├── README.md
└── requirements.txt
```

## Pipeline de dados

O projeto foi dividido em etapas independentes e reproduzíveis.

### 1. Auditoria inicial

O arquivo `01_data_audit.py` verifica:

* dimensões da base;
* nomes das colunas;
* tipos dos dados;
* valores nulos;
* registros duplicados;
* datas inválidas;
* período da coleta;
* consentimento dos participantes;
* quantidade de valores únicos.

### 2. Limpeza e padronização

O arquivo `02_data_cleaning.py` realiza:

* padronização dos nomes das colunas;
* tratamento das datas;
* remoção de espaços indesejados;
* validação do consentimento;
* remoção de duplicatas;
* padronização do perfil do consumidor;
* criação de um identificador anônimo.

O resultado é exportado para:

```text
data/processed/respondents_clean.csv
```

### 3. Tratamento das múltiplas escolhas

O arquivo `03_multiselect_processing.py` transforma as perguntas de múltipla escolha em tabelas ponte.

A separação não utiliza apenas `split(",")`, porque algumas alternativas possuem vírgulas no próprio texto, como:

```text
Recomendação (amigos, especialistas, avaliações)
```

O processamento utiliza um catálogo controlado com as alternativas oficiais e preserva respostas livres para revisão.

São geradas as seguintes tabelas:

```text
bridge_wine_types.csv
bridge_purchase_channels.csv
bridge_purchase_factors.csv
bridge_sustainable_attributes.csv
unclassified_answers.csv
```

### 4. Engenharia de variáveis

O arquivo `04_feature_engineering.py` cria:

* frequência mensal estimada;
* intensidade de consumo;
* pontuação de importância do rótulo;
* indicador de alta importância;
* nível de conhecimento do consumidor;
* segmentos estratégicos.

O resultado é exportado para:

```text
data/processed/respondents_analytical.csv
```

### 5. Banco de dados

O arquivo `05_database_load.py` carrega as tabelas processadas em um banco SQLite.

O banco contém:

* uma tabela principal de respondentes;
* quatro tabelas ponte;
* uma tabela de respostas não classificadas;
* índices para otimizar as consultas;
* validações de unicidade e integridade referencial.

### 6. Análise SQL

O arquivo `06_sql_analysis.py` executa as views analíticas e exporta os resultados para a pasta `reports`.

As consultas respondem perguntas como:

* Quais são os principais fatores considerados na compra?
* Quais atributos são mais valorizados em vinhos sustentáveis?
* Quais canais são mais utilizados?
* Como a importância do rótulo varia por perfil?
* Quais são os segmentos prioritários?
* Quais canais são utilizados pelo público mais interessado em sustentabilidade?

## Modelagem dos dados

A tabela `fact_respondents` possui uma linha por participante.

As perguntas de múltipla escolha foram transformadas em tabelas ponte porque representam relações muitos-para-muitos.

```text
fact_respondents
        │
        ├── bridge_wine_types
        ├── bridge_purchase_channels
        ├── bridge_purchase_factors
        └── bridge_sustainable_attributes
```

Essa estrutura evita dupla contagem e facilita análises com Python, SQL e ferramentas de visualização.

## Qualidade dos dados

O projeto verifica:

* identificadores duplicados;
* valores nulos;
* datas inválidas;
* valores fora dos domínios esperados;
* pontuações inválidas;
* indicadores binários inválidos;
* registros órfãos nas tabelas ponte;
* respostas não classificadas.

As respostas livres são preservadas e não são descartadas silenciosamente.

## Como executar

### 1. Criar o ambiente virtual

```powershell
python -m venv .venv
```

### 2. Ativar o ambiente

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Instalar as bibliotecas

```powershell
python -m pip install -r requirements.txt
```

### 4. Executar o pipeline

Os arquivos devem ser executados na ordem:

```powershell
python src/01_data_audit.py
python src/02_data_cleaning.py
python src/03_multiselect_processing.py
python src/04_feature_engineering.py
python src/05_database_load.py
python src/06_sql_analysis.py
python src/07_exploratory_analysis.py
```

## Resultados preliminares

Os resultados indicam que:

* 82,4% dos participantes consideram muito ou extremamente importante comunicar sustentabilidade no rótulo;
* a qualidade sensorial é o atributo mais valorizado em vinhos sustentáveis;
* o preço é o principal fator geral considerado na compra;
* existe uma possível diferença entre a valorização declarada da sustentabilidade e sua influência espontânea na decisão de compra.

Esses resultados serão aprofundados na análise exploratória e no dashboard interativo.

## Limitações

A pesquisa utiliza uma amostra de conveniência, com concentração de participantes:

* residentes na Região Sul;
* moradores de zona urbana;
* com escolaridade elevada.

Os resultados descrevem os participantes da pesquisa, mas não devem ser generalizados automaticamente para toda a população brasileira.

A importância declarada da sustentabilidade também não representa, necessariamente, comportamento real de compra.

## Ética e privacidade

A base não contém nomes, e-mails ou outros identificadores pessoais diretos.

As informações demográficas são utilizadas somente de forma agregada. Grupos com poucos participantes não serão utilizados para conclusões individuais ou generalizações.

O consentimento é validado antes do processamento dos dados.

## Autoria

Projeto desenvolvido por **Trilícia Margarida Gomes**, integrando formação científica, análise de dados e gestão orientada a resultados.
