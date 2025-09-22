from math import radians, sin, cos, sqrt, atan2
from pymongo import MongoClient
import os
import sqlite3
from pathlib import Path

MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
client = MongoClient(MONGO_URI)
db = client['cidades']  # nome do banco
pois_col = db['pontos_interesse']

def find_pois(filter_dict=None, limit=1000):
    """
    Consulta pontos de interesse no MongoDB.
    """
    if filter_dict is None:
        filter_dict = {}
    pois = list(pois_col.find(filter_dict).limit(limit))
    return pois

DB_PATH = Path(__file__).parent / 'data' / 'app.db'

def query_sqlite(query, params=()):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query, params)
    rows = [dict(row) for row in cur.fetchall()]
    conn.close()
    return rows

# Haversine para distância aproximada entre dois pontos (em metros)
def haversine(lat1, lon1, lat2, lon2):
    R = 6371000  # raio da Terra em metros
    phi1 = radians(lat1)
    phi2 = radians(lat2)
    dphi = radians(lat2 - lat1)
    dlambda = radians(lon2 - lon1)

    a = sin(dphi / 2) ** 2 + cos(phi1) * cos(phi2) * sin(dlambda / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c


def pois_within_radius(pois_list, center_lat, center_lon, radius_meters):
    result = []
    for poi in pois_list:
        coord = poi.get('coordenadas') or poi.get('location')
        if not coord:
            continue
        lat = coord.get('latitude')
        lon = coord.get('longitude')
        if lat is None or lon is None:
            continue
        dist = haversine(center_lat, center_lon, lat, lon)
        if dist <= radius_meters:
            poi['_distance_m'] = dist
            result.append(poi)
    # ordenar por distância
    result.sort(key=lambda x: x['_distance_m'])
    return result
