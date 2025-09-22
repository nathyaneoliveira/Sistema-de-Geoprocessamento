import streamlit as st
from pymongo import MongoClient
import sqlite3
import pandas as pd
from math import radians, sin, cos, sqrt, atan2
import os
import re
from pathlib import Path
import pydeck as pdk

# Função para converter DMS para decimal
def dms_to_decimal(dms_str, lat_or_lon=None):

    if not isinstance(dms_str, str) or not dms_str.strip():
        raise ValueError("Entrada inválida: string vazia ou não é uma string")

    dms_norm = dms_str.strip()
    dms_norm = dms_norm.replace('’', "'").replace('‘', "'").replace('′', "'")
    dms_norm = dms_norm.replace('“', '"').replace('”', '"').replace('″', '"')
    dms_norm = dms_norm.replace('º', '°')

    pattern = r"(\d+)[°]?\s*(\d*)['']?\s*(\d*(?:\.\d+)?)?[\"]?\s*([NSEWnsew]?)"
    match = re.match(pattern, dms_norm)

    if not match:
        raise ValueError(f"Formato inválido: '{dms_str}'")

    graus = float(match.group(1))
    minutos = float(match.group(2)) if match.group(2) else 0
    segundos = float(match.group(3)) if match.group(3) else 0
    direcao = match.group(4).upper() if match.group(4) else None

    decimal = graus + minutos / 60 + segundos / 3600

    if direcao:
        if direcao in ['S', 'W', 'O']:  # Sul ou Oeste
            decimal = -decimal
    else:
        if lat_or_lon == 'lat':
            decimal = decimal  # Assume Norte positivo
        elif lat_or_lon == 'lon':
            decimal = decimal  # Assume Leste positivo
        else:
            raise ValueError("Direção ausente; especifique lat_or_lon='lat' ou 'lon'")

    return decimal

# --- Conexões MongoDB e SQLite ---
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
client = MongoClient(MONGO_URI)
db = client['cidades']
pois_col = db['pontos_interesse']

DB_PATH = Path.cwd() / 'data' / 'app.db'
DB_PATH.parent.mkdir(parents=True, exist_ok=True)
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS cidades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE
)
''')
conn.commit()

# --- Funções de geoprocessamento ---
def haversine(lat1, lon1, lat2, lon2):
    R = 6371000
    phi1, phi2 = radians(lat1), radians(lat2)
    dphi = radians(lat2 - lat1)
    dlambda = radians(lon2 - lon1)
    a = sin(dphi / 2) ** 2 + cos(phi1) * cos(phi2) * sin(dlambda / 2) ** 2
    return 2 * R * atan2(sqrt(a), sqrt(1 - a))

def pois_within_radius(pois_list, center_lat, center_lon, radius_m):
    result = []
    for poi in pois_list:
        coord = poi.get('coordenadas')
        if not coord:
            continue
        lat, lon = coord.get('latitude'), coord.get('longitude')
        if lat is None or lon is None:
            continue
        dist = haversine(center_lat, center_lon, lat, lon)
        if dist <= radius_m:
            poi['_distance_m'] = dist
            result.append(poi)
    result.sort(key=lambda x: x['_distance_m'])
    return result

# --- Configurações Streamlit ---
st.set_page_config(page_title="Sistema de POIs", page_icon="📍", layout="wide")
st.title("📍 Sistema de Geoprocessamento - Pontos de Interesse")
tabs = st.tabs(["➕ Adicionar POI", "🔍 Consultar POIs"])

# --- Aba Adicionar POI ---
with tabs[0]:
    st.subheader("Adicionar novo ponto de interesse")
    coord_type = st.radio("Formato das coordenadas", ("Decimal", "DMS"), horizontal=True)

    with st.form("form_poi"):
        nome = st.text_input("Nome do local", placeholder="Ex: Museu, Parque...")
        cidade = st.text_input("Cidade", placeholder="Ex: Recife")
        descricao = st.text_area("Descrição", placeholder="Descrição opcional...")

        col1, col2 = st.columns(2)
        if coord_type == "Decimal":
            with col1:
                latitude = st.number_input("Latitude (decimal)", format="%.6f", step=0.000001)
            with col2:
                longitude = st.number_input("Longitude (decimal)", format="%.6f", step=0.000001)
        else:
            with col1:
                latitude_dms = st.text_input("Latitude (DMS)", placeholder="06° 49′ 48″ ou 06 49 48 S")
            with col2:
                longitude_dms = st.text_input("Longitude (DMS)", placeholder="35° 14′ 50″ ou 35 14 50 W")

        submitted = st.form_submit_button("➕ Adicionar")
        if submitted:
            if not nome or not cidade:
                st.warning("Preencha pelo menos o nome e a cidade")
            else:
                try:
                    if coord_type == "Decimal":
                        lat, lon = latitude, longitude
                    else:
                        lat = dms_to_decimal(latitude_dms, lat_or_lon='lat')
                        lon = dms_to_decimal(longitude_dms, lat_or_lon='lon')

                    document = {
                        "nome_local": nome,
                        "cidade": cidade,
                        "coordenadas": {"latitude": lat, "longitude": lon},
                        "descricao": descricao
                    }
                    pois_col.insert_one(document)
                    cursor.execute("INSERT OR IGNORE INTO cidades (nome) VALUES (?)", (cidade,))
                    conn.commit()
                    st.success(f"Ponto de interesse inserido com sucesso! ✅")
                except ValueError as e:
                    st.error(f"Erro na conversão das coordenadas: {e}")

# --- Aba Consultar POIs ---
with tabs[1]:
    st.subheader("Consultar pontos por cidade")
    cursor.execute("SELECT nome FROM cidades")
    cidades = [row[0] for row in cursor.fetchall()]

    if cidades:
        cidade_sel = st.selectbox("Escolha a cidade", cidades)
        if cidade_sel:
            pois = list(pois_col.find({"cidade": cidade_sel}))
            st.info(f"{len(pois)} pontos encontrados em {cidade_sel}")

            if pois:
                lat0, lon0 = pois[0]['coordenadas']['latitude'], pois[0]['coordenadas']['longitude']
                radius = st.slider("Raio de pesquisa (metros)", 100, 50000, 10000, 100)
                pois_radius = pois_within_radius(pois, lat0, lon0, radius)

                if pois_radius:
                    map_df = pd.DataFrame([{
                        'lat': p['coordenadas']['latitude'],
                        'lon': p['coordenadas']['longitude'],
                        'name': p.get('nome_local')
                    } for p in pois_radius])
                    st.pydeck_chart(pdk.Deck(
                        initial_view_state=pdk.ViewState(latitude=lat0, longitude=lon0, zoom=12, pitch=0),
                        layers=[pdk.Layer('ScatterplotLayer', data=map_df,
                                          get_position='[lon, lat]',
                                          get_color='[0, 128, 255, 200]',
                                          get_radius=150,
                                          pickable=True)],
                        tooltip={"text": "{name}"}
                    ))

                    for p in pois_radius:
                        with st.container():
                            cols = st.columns([0.5, 5])
                            with cols[0]: st.markdown("📍")
                            with cols[1]:
                                st.markdown(f"**{p.get('nome_local')}**")
                                st.markdown(f"- Descrição: {p.get('descricao', '-')}")
                                st.markdown(f"- Distância: {p.get('_distance_m'):.1f} m")
                                st.divider()
                else:
                    st.info("Nenhum ponto dentro do raio selecionado")
    else:
        st.info("Nenhuma cidade cadastrada")
