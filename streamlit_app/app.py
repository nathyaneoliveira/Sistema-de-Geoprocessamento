import streamlit as st
import pandas as pd

from utils import query_sqlite

# Certifique-se de ter importado query_sqlite, find_pois e pois_within_radius

# Painel principal: seleção e visualização
st.header('Consultar e visualizar')
cols = st.columns([1, 2])

with cols[0]:
    st.subheader('Escolha cidade / filtros')
    cidades = query_sqlite(
        'SELECT c.id, c.nome as cidade, e.nome as estado FROM cidades c JOIN estados e ON c.estado_id = e.id')

    if cidades:
        df = pd.DataFrame(cidades)
        cidade_sel = st.selectbox('Cidade', df['cidade'] + ' - ' + df['estado'])
    else:
        st.info('Nenhuma cidade cadastrada no SQLite')
        cidade_sel = None

radius = st.slider('Raio (metros)', min_value=100, max_value=50000, value=5000, step=100)
st.write('Raio atual:', radius, 'm')

with cols[1]:
    st.subheader('Mapa dos pontos')

    if cidade_sel:
        # extrair nome da cidade
        cidade_nome = cidade_sel.split(' - ')[0]
        pois = find_pois({'cidade': cidade_nome}, limit=1000)
        st.write(f'{len(pois)} pontos encontrados em {cidade_nome}')

        # se houver pontos e cidades com coordenadas salvas no SQLite
        cidade_row = query_sqlite('SELECT latitude, longitude FROM cidades WHERE nome = ?', (cidade_nome,))
        if cidade_row and cidade_row[0].get('latitude') and cidade_row[0].get('longitude'):
            lat0 = cidade_row[0]['latitude']
            lon0 = cidade_row[0]['longitude']
        elif pois:
            lat0 = pois[0]['coordenadas']['latitude']
            lon0 = pois[0]['coordenadas']['longitude']
        else:
            lat0 = -15.788497
            lon0 = -47.879873

        pois_radius = pois_within_radius(pois, lat0, lon0, radius)

        # preparar dataframe para st.map
        map_df = pd.DataFrame([
            {
                'lat': p['coordenadas']['latitude'],
                'lon': p['coordenadas']['longitude'],
                'name': p.get('nome_local'),
                'dist_m': p.get('_distance_m')
            } for p in pois_radius
        ])

        if not map_df.empty:
            st.map(map_df[['lat', 'lon']])
            st.dataframe(map_df)
        else:
            st.info('Nenhum ponto dentro do raio selecionado.')
    else:
        st.info('Selecione uma cidade à esquerda')
