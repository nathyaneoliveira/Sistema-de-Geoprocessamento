# 🌍 geo_system  

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)  
![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)  
![License](https://img.shields.io/badge/license-acad%C3%AAmico-red)  
![Framework](https://img.shields.io/badge/Framework-Streamlit-ff4b4b?logo=streamlit)  

---

## 📌 Descrição  
O **geo_system** é um projeto acadêmico em **Python** voltado para a disciplina de **Geoprocessamento e Sistemas de Informação Geográfica**.  
Este módulo corresponde ao **Checkpoint 01: Cadastro, Consulta e Visualização de Pontos de Interesse (POIs)**.  

O sistema tem como objetivo:  
- Cadastrar POIs (Pontos de Interesse) em bancos de dados **SQLite** e **MongoDB**.  
- Consultar POIs por cidade ou dentro de um raio definido.  
- Converter coordenadas de **DMS ↔ Decimal**.  
- Calcular distâncias geográficas usando a **fórmula de Haversine**.  
- Exibir os pontos em **mapas interativos** integrados ao **Streamlit**.  

O projeto é parte de um sistema acadêmico em desenvolvimento incremental e possui peso 2 na primeira nota da disciplina.  

---

## 📂 Estrutura do Projeto

│
├── streamlit_app/
│ ├── app.py # Interface principal no Streamlit
│ ├── db_mongo.py # Conexão e operações no MongoDB
│ ├── db_sqlite.py # Conexão e operações no SQLite
│ ├── geo.py # Funções de geoprocessamento (distância, filtros)
│ ├── utils.py # Funções auxiliares (queries SQL, helpers)
│ ├── streamilit.py # Versão alternativa/teste do app
│ └── requerimentos.txt # Dependências do projeto
│
├── data/
│ └── app.db # Banco de dados SQLite
│
└── README.md # Documentação do projeto

markdown
Copiar código

---

## ⚙️ Requisitos  
- Python **3.9+**  
- Dependências no `requerimentos.txt`:  
  - `streamlit`  
  - `pymongo`  
  - `sqlite3`  
  - `pandas`  
  - `geopy`  
  - `folium`  
  - `streamlit-folium`  
  - `python-dotenv`  

Instalação das dependências:  
```bash
pip install -r requerimentos.txt
▶️ Compilação e Execução
Para iniciar o sistema:

bash
Copiar código
cd streamlit_app
streamlit run app.py
🧪 Exemplos de Uso
Entrada de teste (cadastro de POI):
makefile
Copiar código
Nome: Praça da Independência
Cidade: João Pessoa
Coordenadas: -7.11532, -34.861
Descrição: Ponto turístico central da cidade
Saída esperada (consulta):
less
Copiar código
1 ponto encontrado em João Pessoa
- Praça da Independência (Distância: 0.0 m)
Saída no mapa (Streamlit):
Ponto exibido em mapa interativo com zoom automático.

🤝 Contribuição
Este projeto é desenvolvido no contexto acadêmico. Sugestões e melhorias podem ser feitas via GitHub ou discutidas em sala de aula.

📜 Licença
Uso acadêmico restrito à disciplina de Geoprocessamento e SIG.

🚀 Estado
✅ Cadastro de POIs funcionando

✅ Consulta por cidade e por raio implementada

✅ Conversão de DMS → Decimal

✅ Exibição em mapa interativo (Streamlit + Folium)

🚧 Próximos módulos incluirão: relatórios em PDF e integração com APIs externas
