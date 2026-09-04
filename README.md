# Wine Consumer Insights

Projeto end-to-end de análise de dados sobre o comportamento do
consumidor de vinhos, desenvolvido desde a auditoria e o tratamento
da base até a construção de indicadores e a publicação de um
dashboard interativo.

O projeto contempla limpeza e padronização dos dados, controle de
qualidade, tratamento de respostas de múltipla escolha, engenharia
de variáveis, segmentação de consumidores, modelagem SQL, análise
exploratória e visualização interativa.

Para preservar o ineditismo da pesquisa original, perguntas,
variáveis e resultados específicos foram omitidos, anonimizados,
agregados ou substituídos por informações demonstrativas.

## Dashboard interativo

[🔗 Acessar o dashboard PIWI Consumer Insights](https://trilicia.github.io/piwi_consumer_insights/dashboard/)

O dashboard permite explorar os resultados por região, faixa etária, perfil de consumo, frequência e escolaridade. Os filtros atualizam automaticamente os indicadores e gráficos.

## Problema de negócio

Como transformar a sustentabilidade em uma proposta de valor relevante para consumidores de vinho, considerando seus perfis, hábitos de consumo, critérios de compra e canais de aquisição?

## Objetivo

Investigar como o perfil dos consumidores, os hábitos de consumo, os critérios de compra e os canais de aquisição podem contribuir para uma estratégia de posicionamento de vinhos sustentáveis.

Além da análise, o projeto busca demonstrar competências profissionais em:

* estruturação e gestão de projetos de dados;
* auditoria e qualidade de dados;
* tratamento e padronização;
* engenharia de variáveis;
* modelagem relacional;
* consultas SQL;
* análise exploratória;
* visualização de dados;
* comunicação de resultados para o negócio.

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
* Git
* GitHub

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
* [x] Análise exploratória
* [x] Criação dos gráficos
* [x] Construção do dashboard interativo
* [x] Elaboração das recomendações finais

## Sobre a base de dados

Os dados utilizados neste projeto fazem parte de uma pesquisa científica mais ampla. Para preservar o escopo e a integridade do estudo original, foi utilizado apenas um recorte anonimizado da base.

A planilha disponibilizada para este projeto de portfólio não contém todas as perguntas e colunas do instrumento de pesquisa. Foram selecionadas somente as variáveis necessárias para a análise do comportamento dos consumidores de vinho e da percepção de sustentabilidade associada aos vinhos PIWI.

Portanto, este projeto apresenta uma análise complementar e independente, desenvolvida para demonstrar competências em tratamento, modelagem, análise e visualização de dados. Ele não substitui, reproduz integralmente ou antecipa os resultados da pesquisa científica original.

O recorte utilizado contém 261 respostas anônimas e 16 variáveis relacionadas a:

* perfil sociodemográfico;
* frequência de consumo de vinho;
* nível de conhecimento sobre vinhos;
* tipos de vinho preferidos;
* canais de aquisição;
* fatores considerados na compra;
* atributos valorizados em vinhos sustentáveis;
* importância da comunicação de sustentabilidade no rótulo.

O arquivo original utilizado no projeto é mantido em:

```text
data/raw/dados_piwi.xlsx
```

A base original não é alterada durante o processamento. Todas as transformações são realizadas em arquivos separados dentro de `data/processed`.

## Estrutura do projeto

```text
piwi_consumer_insights/
├── dashboard/
├── data/
│   ├── processed/
│   └── raw/
│       └── dados_piwi.xlsx
├── reports/
│   └── figures/
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

O projeto foi estruturado em etapas independentes e reproduzíveis.

### 1. Auditoria inicial

O arquivo `01_data_audit.py` realiza uma análise inicial da base e verifica:

* quantidade de linhas e colunas;
* nomes das variáveis;
* tipos dos dados;
* valores nulos;
* registros duplicados;
* datas inválidas;
* período da coleta;
* consentimento dos participantes;
* quantidade de valores únicos.

Essa etapa permite conhecer a estrutura dos dados antes de qualquer transformação.

### 2. Limpeza e padronização

O arquivo `02_data_cleaning.py` realiza:

* padronização dos nomes das colunas;
* tratamento das datas;
* remoção de espaços indesejados;
* validação do consentimento;
* remoção de duplicatas;
* padronização do perfil do consumidor;
* criação de um identificador anônimo;
* validações após a limpeza.

O resultado é exportado para:

```text
data/processed/respondents_clean.csv
```

### 3. Tratamento das perguntas de múltipla escolha

O arquivo `03_multiselect_processing.py` transforma as perguntas de múltipla escolha em tabelas ponte.

A separação não utiliza apenas `split(",")`, porque algumas alternativas possuem vírgulas dentro do próprio texto, como:

```text
Recomendação (amigos, especialistas, avaliações)
```

Uma separação simples por vírgulas dividiria incorretamente essa alternativa.

O processamento utiliza um catálogo controlado com as alternativas oficiais. As respostas livres ou não reconhecidas são preservadas em uma tabela específica para revisão.

São gerados os seguintes arquivos:

```text
bridge_wine_types.csv
bridge_purchase_channels.csv
bridge_purchase_factors.csv
bridge_sustainable_attributes.csv
unclassified_answers.csv
```

### 4. Engenharia de variáveis

O arquivo `04_feature_engineering.py` transforma respostas categóricas em variáveis apropriadas para análises e segmentações.

São criadas as seguintes variáveis:

* frequência mensal estimada;
* intensidade de consumo;
* pontuação de importância do rótulo;
* indicador de alta importância;
* nível de conhecimento do consumidor;
* segmento estratégico.

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
* índices para otimização das consultas;
* validações de unicidade;
* verificações de integridade referencial.

O arquivo do banco é gerado em:

```text
data/processed/piwi_consumer_insights.db
```

Como o banco pode ser reconstruído pelo pipeline, o arquivo com extensão `.db` não é enviado ao GitHub.

### 6. Análise SQL

O arquivo `06_sql_analysis.py` cria e consulta as views analíticas do projeto.

As consultas respondem a perguntas como:

* Quais são os principais indicadores da pesquisa?
* Quais fatores são mais considerados na compra de vinho?
* Quais atributos são mais valorizados em vinhos sustentáveis?
* Quais são os canais de aquisição mais utilizados?
* Como a importância da sustentabilidade no rótulo varia entre os perfis?
* Quais são os segmentos estratégicos prioritários?
* Quais canais são utilizados pelo público mais interessado em sustentabilidade?

Os resultados são exportados como arquivos CSV para a pasta `reports`.

### 7. Análise exploratória

O arquivo `07_exploratory_analysis.py` utiliza os dados processados e os resultados das consultas SQL para criar:

* gráficos dos fatores de compra;
* gráficos dos atributos de vinhos sustentáveis;
* distribuição da importância da sustentabilidade no rótulo;
* distribuição dos segmentos estratégicos;
* indicadores resumidos;
* sumário executivo.

Os gráficos são salvos em:

```text
reports/figures/
```

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

Um participante pode selecionar vários fatores, e cada fator pode ser selecionado por vários participantes.

Essa estrutura:

* evita duplicações na tabela principal;
* reduz o risco de dupla contagem;
* facilita consultas SQL;
* permite calcular percentuais com participantes distintos;
* prepara os dados para o dashboard interativo.

## Qualidade dos dados

O projeto inclui verificações para identificar:

* valores nulos;
* registros duplicados;
* identificadores duplicados;
* datas inválidas;
* valores fora dos domínios esperados;
* pontuações de importância inválidas;
* indicadores binários inválidos;
* registros órfãos nas tabelas ponte;
* respostas livres ou não classificadas.

As respostas não reconhecidas são preservadas para revisão e não são descartadas silenciosamente.

## Como executar o projeto

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

Os arquivos devem ser executados na seguinte ordem:

```powershell
python src/01_data_audit.py
python src/02_data_cleaning.py
python src/03_multiselect_processing.py
python src/04_feature_engineering.py
python src/05_database_load.py
python src/06_sql_analysis.py
python src/07_exploratory_analysis.py
```

Cada etapa utiliza os arquivos produzidos pela etapa anterior.

## Visualização local do dashboard

Para executar o dashboard localmente:

```powershell
python -m http.server 8000 --directory dashboard

## Resultados preliminares

Os resultados iniciais indicam que:

* 82,4% dos participantes consideram muito ou extremamente importante comunicar sustentabilidade no rótulo;
* a qualidade sensorial é o atributo mais valorizado em vinhos sustentáveis;
* o preço é o principal fator geral considerado na compra;
* clareza e transparência das informações no rótulo apresentam relevância para a escolha de produtos sustentáveis;
* existe uma possível diferença entre a valorização declarada da sustentabilidade e sua influência espontânea na decisão de compra.

A recomendação preliminar é posicionar os vinhos PIWI por meio da combinação entre:

* qualidade sensorial;
* preço competitivo;
* clareza das informações;
* sustentabilidade ambiental comprovada.

A sustentabilidade deve complementar a proposta de valor do produto, e não substituir atributos tradicionais como qualidade e preço.

## Limitações

A base utilizada representa apenas um recorte de uma pesquisa científica mais ampla. Algumas perguntas e variáveis foram intencionalmente omitidas para preservar o estudo original. Portanto, as conclusões deste projeto estão limitadas às informações presentes na planilha disponibilizada.

A pesquisa utiliza uma amostra de conveniência, com concentração de participantes:

* residentes na Região Sul;
* moradores de zona urbana;
* com escolaridade elevada.

Os resultados descrevem os participantes da pesquisa e não devem ser generalizados automaticamente para toda a população brasileira.

A importância declarada da sustentabilidade também não representa necessariamente um comportamento real de compra.

As estimativas de frequência mensal foram criadas exclusivamente para fins analíticos e não representam medições exatas do consumo individual.

## Ética e privacidade

A base utilizada no projeto não contém nomes, e-mails ou outros identificadores pessoais diretos.

As informações demográficas são analisadas somente de forma agregada. Grupos com poucos participantes não devem ser utilizados para conclusões individuais ou generalizações.

O consentimento dos participantes é validado antes do processamento dos dados.

O conjunto disponibilizado neste repositório representa apenas um recorte anonimizado. A base completa e as demais perguntas da pesquisa científica original não fazem parte deste projeto.

## Autoria

Projeto desenvolvido por **Trilícia Margarida Gomes**, integrando formação científica, análise de dados e gestão orientada a resultados.
