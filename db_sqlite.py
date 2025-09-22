import sqlite3
from pathlib import Path

# Caminho seguro do banco
DB_PATH = Path.cwd() / 'data' / 'app.db'
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

# Script SQL
SCHEMA = '''
CREATE TABLE IF NOT EXISTS paises (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS estados (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    pais_id INTEGER,
    sigla TEXT,
    FOREIGN KEY (pais_id) REFERENCES paises(id)
);

CREATE TABLE IF NOT EXISTS cidades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    estado_id INTEGER,
    latitude REAL,
    longitude REAL,
    FOREIGN KEY (estado_id) REFERENCES estados(id)
);

CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT UNIQUE
);
'''

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.executescript(SCHEMA)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print('SQLite inicializado em', DB_PATH)
