from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from dotenv import load_dotenv


load_dotenv()


MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
client = MongoClient(MONGO_URI)
db = client['cidades']
pois = db['pontos_interesse']


def insert_poi(document: dict) -> str:
    res = pois.insert_one(document)
    return str(res.inserted_id)


def find_pois(filter_query: dict = None, limit: int = 100):

    if filter_query is None: filter_query = {}
    return list(pois.find(filter_query).limit(limit))

def find_poi_by_id(id_str: str):
    return pois.find_one({'_id': ObjectId(id_str)})

def delete_poi(id_str: str):
    return pois.delete_one({'_id': ObjectId(id_str)})
