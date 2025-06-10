import os

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.synchronous.database import Database

load_dotenv()


class MongoDB:
    db: Database

    def __init__(self, uri=os.getenv("MONGO_URL"), db_name=os.getenv("MONGO_DB")):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def insert_one(self, collection_name, document):
        collection = self.db[collection_name]
        result = collection.insert_one(document)
        return result.inserted_id
