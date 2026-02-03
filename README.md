# Teste Técnico – Engenharia de Dados (ANS)

Este projeto foi desenvolvido como solução para o Teste Técnico de Engenharia de Dados, utilizando dados públicos da ANS (Agência Nacional de Saúde Suplementar).

O objetivo é demonstrar capacidade prática de:

- integração com API pública;

- processamento e consolidação de dados heterogêneos;

- análise e modelagem via SQL;

- exposição dos dados por meio de uma API e interface web;
além de documentar decisões técnicas e trade-offs adotados ao longo da solução.

# Tecnologias Utilizadas
# Backend / Dados

Python 3.x

FastAPI

Pandas

Requests

SQL (scripts compatíveis com MySQL 8 / PostgreSQL 10+)

Justificativa das tecnologias:
Python foi escolhido por sua ampla adoção em engenharia de dados e pelo ecossistema maduro para ETL.
FastAPI foi utilizado por oferecer alta performance, tipagem explícita e documentação automática via Swagger, facilitando validação da API.
Pandas foi adotado por ser suficiente para o volume de dados do problema, priorizando simplicidade, legibilidade e rapidez de desenvolvimento.
MySQL foi utilizado para responder perguntas analíticas estruturadas, conforme solicitado no teste.

# Frontend

Vue.js 3

Vite

Chart.js

Justificativa do frontend:
Vue.js foi escolhido por permitir prototipação rápida de interfaces reativas e boa organização de componentes.
Chart.js foi utilizado para visualização clara e objetiva dos indicadores solicitados.

# Organização do Projeto

Teste_joao_pedro_de_lima_teofilo/
├── scripts/
│   ├── extract_ans.py
│   └── transform_data.py
│
├── database/
│   └── queries.sql
│
├── backend/
│   └── main.py
│
├── frontend/
│
├── data/
│   ├── consolidado_despesas.csv
│   └── despesas_agregadas.csv
│
├── requirements.txt
└── README.md


Justificativa da organização:
A estrutura foi organizada por responsabilidade (extração, transformação, análise, backend e frontend), facilitando leitura do código, manutenção e possíveis extensões futuras do pipeline.

- Atendimento aos Requisitos do Teste

- Download automático de dados da ANS: scripts/extract_ans.py

- Processamento de múltiplos formatos: scripts/transform_data.py

- Consolidação de 3 trimestres: data/consolidado_despesas.csv

- Tratamento de inconsistências: documentado neste README

- Agregação de despesas: data/despesas_agregadas.csv

- Queries analíticas em SQL: database/queries.sql

- API REST em Python: backend/main.py

- Interface Web: frontend/

# Como Executar o Projeto (Passo a Passo)

Pré-requisitos:

Python 3.10 ou superior

Node.js 18 ou superior

npm

1 Instalar dependências Python

Na raiz do projeto:

python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

2 Executar o pipeline de dados (opcional)

Os arquivos finais já estão disponíveis na pasta data/.
Esta etapa é necessária apenas caso queira regerar os CSVs.

cd scripts
python extract_ans.py
python transform_data.py

3 Executar o Backend (API)
cd backend
uvicorn main:app --reload


A API ficará disponível em:

http://127.0.0.1:8000

Documentação Swagger: http://127.0.0.1:8000/docs

4 Executar o Frontend (Vue.js)

Em outro terminal:

cd frontend
npm install
npm run dev


O frontend ficará disponível em:

http://localhost:5173

# 1 Integração com API Pública e Consolidação de Dados

Os dados foram obtidos a partir da API de Dados Abertos da ANS, especificamente os arquivos de Demonstrações Contábeis dos últimos três trimestres disponíveis.

Etapas realizadas:

- Identificação automática dos últimos trimestres disponíveis

- Download dos arquivos ZIP

- Extração automática dos arquivos

- Leitura de arquivos em formato CSV

- Identificação dinâmica das colunas relevantes

- Normalização dos dados

- Consolidação em um único arquivo CSV

Trade-off – Processamento dos dados:
Foram avaliadas as abordagens de carregamento completo em memória e processamento incremental.
Foi adotado o processamento incremental, reduzindo consumo de memória e tornando o pipeline mais robusto para arquivos maiores.

Arquivo gerado:
data/consolidado_despesas.csv

- Colunas

- CNPJ

- RazaoSocial

- Ano

- Trimestre

- ValorDespesas

# 2 Tratamento de Inconsistências

Durante a consolidação, foram identificadas inconsistências comuns nos dados da ANS.

- CNPJs duplicados com razões sociais diferentes

Decisão: manter a razão social mais frequente.

Justificativa: reduz ruídos causados por variações de escrita ao longo do tempo.


- Valores zerados ou negativos

Decisão: os registros foram mantidos.

Justificativa: valores negativos podem representar estornos, e valores zerados podem ser válidos dependendo do contexto contábil.


- Formatos inconsistentes de trimestre

Decisão: normalização para o formato Ano + Trimestre (ex.: 2025T2).

Justificativa: facilita agregações e análises temporais.


# 3 Transformação e Agregação de Dados

A partir do arquivo consolidado, foi gerado um segundo CSV contendo dados agregados.

- Operações realizadas

- Agrupamento por Razão Social e UF

- Cálculo do total de despesas por operadora/UF

- Ordenação do maior para o menor valor total

Arquivo gerado:
data/despesas_agregadas.csv


Justificativa do uso de CSV:
Os CSVs consolidados foram mantidos como artefatos intermediários para facilitar auditoria, validação e eventual reprocessamento dos dados.

# 4 Banco de Dados e Análise SQL

O arquivo database/queries.sql contém:

- DDL para criação das tabelas

- Definição de chaves primárias e índices

- Queries analíticas solicitadas no teste, incluindo:

- Crescimento percentual de despesas entre trimestres

- Distribuição de despesas por UF

- Comparação com médias gerais

Trade-off – Modelagem:
Foram consideradas tabelas desnormalizadas e modelos normalizados.
Optou-se por um modelo mais normalizado para melhorar clareza das queries analíticas e facilitar manutenção futura.

# 5 Backend (Python)

O backend foi desenvolvido em FastAPI e expõe os dados processados via API REST.

- Funcionalidades

- Listagem de operadoras

- Consulta por CNPJ

- Histórico de despesas

Estatísticas agregadas

Decisões de escopo:
Funcionalidades como autenticação, cache e paginação avançada não foram implementadas por não fazerem parte dos requisitos do teste.

# 6 Frontend (Vue.js)

O frontend consome a API para visualização dos dados.

- Funcionalidades

- Tabela de operadoras

- Busca por CNPJ ou Razão Social

- Gráfico de distribuição de despesas por UF

O frontend foi desenvolvido priorizando funcionalidade e clareza dos dados, em detrimento de customizações visuais avançadas.