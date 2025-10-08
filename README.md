# 🧠 Tech Challenge Fase 03 — Agrupamento de Vendedores (Clustering)

Este projeto tem como objetivo **identificar padrões de comportamento entre vendedores** com base na **proporção da receita bruta por categoria de produto vendido**, utilizando **técnicas de machine learning não supervisionado (clustering)**.  

A aplicação final foi construída em **Streamlit**, permitindo **visualização interativa dos clusters**, além de gráficos de evolução temporal e análise das principais variáveis que diferenciam cada grupo.

Fonte dos dados: [Olist - Brazilian Ecommerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

![Schema dos Dados](data/04_img/ollist_schema.png)

---

## 📂 Estrutura do Projeto

```
tech_challenge_fase_03/
│
├── data/                             # Diretório principal de dados
│   ├── 00_raw/                       # Dados originais
│   ├── 01_interim/                   # Dados intermediários
│   ├── 02_processed/                 # Dados tratados
│   └── 03_model/                     # Dados utilizados no modelo (ex: clustering_output.csv)
│
├── notebooks/                        # Notebooks de desenvolvimento e experimentação
│   ├── 01_eda.ipynb                  # Análise exploratória dos dados
│   ├── 02_etl.ipynb                  # Limpeza e transformação
│   ├── 03_feature_engineering.ipynb  # Criação de variáveis
│   ├── 04_model_agg_clustering.ipynb # Modelo Agglomerative Clustering
│   └── 04_model_kmeans.ipynb         # Modelo K-Means
│
├── src/                              # Código-fonte principal
│   ├── app.py                        # Aplicação Streamlit
│   └── models/                       # Modelos salvos (se aplicável)
│
├── requirements.txt                  # Dependências do projeto
├── pyproject.toml / uv.lock          # Configurações do ambiente com UV
└── README.md                         # Este arquivo
```

---

## 🚀 Como executar o projeto localmente

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/tech_challenge_fase_03.git
cd tech_challenge_fase_03
```

### 2. Crie o ambiente virtual com **UV** (recomendado)
```bash
uv venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
```

### 3. Instale as dependências
```bash
uv pip install -r requirements.txt
```
ou
```bash
pip install -r requirements.txt
```

---

## 🧩 Estrutura de dados

O projeto utiliza um dataset consolidado contendo as métricas de receita bruta por categoria e por vendedor.

Arquivo principal:
```
data/03_model/clustering_output.csv
```

> ⚠️ Certifique-se de que este arquivo está disponível localmente ou no repositório antes de rodar o app.

---

## 🖥️ Executando a aplicação Streamlit

Na raiz do projeto (onde está o `app.py`):

```bash
streamlit run tech_challenge_fase_03/src/app.py
```
ou se já estiver dentro da pasta `src` para deixar a aplicação rodando em segundo plano sem bloquear o terminal:
```bash
streamlit run app.py &
```

Acesse o endereço exibido no terminal, geralmente:
```
http://localhost:8501
```

---

## 🌐 Deploy no Streamlit Cloud

1. Crie um repositório no **GitHub** e envie todos os arquivos do projeto.
2. Vá até [https://share.streamlit.io](https://share.streamlit.io).
3. Conecte sua conta do GitHub e selecione o repositório.
4. Configure o caminho do app:
   ```
   tech_challenge_fase_03/src/app.py
   ```
5. Clique em **Deploy** 🚀

---

## 📊 Funcionalidades do Dashboard

- **📆 Filtro de data:** seleção de mês de referência  
- **📈 Evolução temporal:** linha mostrando o número de vendedores por cluster  
- **🔥 Distribuição vendedores por cluster:** quantidade de vendedores em cada cluster
- **🔍 PCA (redução de dimensionalidade):** visualização 2D dos agrupamentos  
- **🔥 Heatmap interativo:** comparação média das principais features por cluster baseada nas variáveis mais relevantes via árvore de decisão  
- **🔍 Tabela receita média::** receita média dos clusters em cada categoria para auxiliar na análise junto ao heatmap
---

## 🧠 Tecnologias utilizadas

| Categoria | Tecnologias |
|------------|--------------|
| Linguagem | Python 3.11 |
| Visualização | Streamlit, Plotly, Seaborn |
| Machine Learning | scikit-learn |
| Manipulação de dados | Pandas, NumPy |
| Ambiente | UV, Virtualenv |