# 👥 Integrantes do Projeto

| Nome               | Função / Responsabilidade          |
| ------------------ | ---------------------------------- |
| *Allan Vitor*      | Extração e integração com API      |
| *Heloisa Costa*    | Transformação e modelagem de dados |
| *Walison Brandão*  | Dashboard Streamlit                |
| *Emerson Costa*    | Documentação e testes              |


# 🦠 Projeto ETL COVID-19

Este projeto tem como objetivo realizar um **processo ETL (Extract, Transform, Load)** utilizando dados da pandemia de COVID-19 fornecidos pela API [disease.sh](https://disease.sh).  
O pipeline coleta dados históricos de casos, mortes e recuperações por país, realiza transformações estatísticas e gera arquivos CSV que podem ser analisados ou visualizados por meio de dashboards interativos no **Streamlit**.

---

## 🧩 Estrutura do Projeto

ETL_COVID/
├── src/
│ ├── ETL/
│ │ │ ├── extract.py # Extração de dados (API)
│ │ │ ├── transform.py # Transformação de dados
│ │ │ └── load.py # Salvamento dos CSVs
│ ├── utils/ # Funções auxiliares (se houver)
│ └── main.py # Arquivo principal para rodar a ETL
│
├── output/ # CSVs gerados pela ETL
│ ├── covid_brazil.csv
│ ├── covid_vietnam.csv
│ └── ...
│
├── streamlit_app/ # Dashboard interativo (opcional)
│ └── app.py
│
├── requirements.txt
└── README.md


---
### 🧰 1. Instalar dependências
Crie um ambiente virtual e instale os pacotes necessários:
```bash
python -m venv .venv
pip install -r requirements.txt
---

---
▶️ 2. Rodar o pipeline ETL

Para executar o fluxo completo de extração, transformação e carga:

python -m src.main


Isso irá:

Buscar os dados da COVID-19 (por exemplo, do Vietnã ou Brasil)

Processar e calcular indicadores

Gerar o arquivo CSV em output/covid_<país>.csv


📊 3. Executar o Dashboard (opcional)

Após gerar os CSVs, você pode visualizar os dados no Streamlit:

python -m streamlit run streamlit_app/app.py


O dashboard permitirá aplicar filtros por país, período e indicador, além de visualizar gráficos, tabelas e métricas-chave.