from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")

cliente = MongoClient(MONGO_URI)
db = cliente["comerciotech"]

def get_db():
    return db

