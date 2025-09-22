#  Sistema de Geoprocessamento

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)  
![Status](https://img.shields.io/badge/status-Em%20Desenvolvimento-yellow)  
![License](https://img.shields.io/badge/license-Acad%C3%AAmico-red)  
![Framework](https://img.shields.io/badge/Framework-Streamlit-ff4b4b?logo=streamlit)  

---

##  Descrição  
O **Sistema de Geoprocessamento** é um projeto acadêmico em **Python** voltado para a disciplina de **Tendências em Ciência da Computação**.  

Este módulo corresponde ao **Checkpoint 01: Cadastro, Consulta e Visualização de Pontos de Interesse (POIs)**.  

O sistema tem como objetivo:  
-  Cadastrar POIs (Pontos de Interesse) em bancos de dados **SQLite** e **MongoDB**  
-  Consultar POIs por cidade ou dentro de um raio definido  
-  Converter coordenadas entre **DMS ↔ Decimal**  
-  Calcular distâncias geográficas usando a **fórmula de Haversine**  
-  Exibir os pontos em **mapas interativos** integrados ao **Streamlit**  

---

##  Estrutura do Projeto
```

│
├── streamlit\_app/
│   ├── app.py             # Principal de interface no Streamlit
│   ├── db\_mongo.py        # Conexão e operações no MongoDB
│   ├── db\_sqlite.py       # Conexão e operações no SQLite
│   ├── geo.py             # Funções de geoprocessamento (distância, filtros)
│   ├── utils.py           # Funções auxiliares (queries SQL, helpers)
│   ├── streamilit.py      # Versão alternativa/teste do app
│   └── requerimentos.txt  # Dependências do projeto
│
├── dados/
│   └── app.db             # Banco de dados SQLite
│
└── README.md              # Documentação do projeto

````

---

##  Requisitos  
- Python **3.9+**  
- Dependências no
  - `requerimentos.txt`:  
  - `streamlit`  
  - `pymongo`  
  - `sqlite3`  
  - `pandas`  
  - `geopy`  
  - `folium`  
  - `streamlit-folium`  
  - `python-dotenv`  

### Instalação das dependências  
```bash
pip install -r requerimentos.txt
````

---

##  Compilação e Execução

Para iniciar o sistema:

```bash
cd streamlit_app
streamlit run app.py
```

---

##  Exemplos de Uso

### Entrada de teste (cadastro de POI)

```
Nome: Praça da Independência
Cidade: João Pessoa
Coordenadas: -7.11532, -34.861
Descrição: Ponto turístico central da cidade
```

### Saída esperada (consulta)

```
1 ponto encontrado em João Pessoa
- Praça da Independência (Distância: 0.0 m)
```

### Saída no mapa (Streamlit)

* Ponto exibido em **mapa interativo** com zoom automático

---

##  Contribuição

Este projeto é desenvolvido no contexto acadêmico.
Sugestões e melhorias podem ser feitas via **GitHub** ou discutidas em sala de aula.

---

##  Licença

Uso acadêmico restrito à disciplina de **Tendências em Ciência da Computação**.

---

##  Estado

*  Cadastro de POIs funcionando
*  Consulta por cidade e por raio implementada
*  Conversão de DMS → Decimal
*  Exibição em mapa interativo (Streamlit + Folium)
*  Próximos módulos incluirão: relatórios em PDF e integração com APIs externas
