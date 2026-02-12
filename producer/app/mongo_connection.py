from pymongo import MongoClient
import os 
import json

MONGO_URI = os.getenv('MONGO_URI',"mongodb://localhost:27017")
MONGO_DB = os.getenv('MONGO_DB',"test")
MONGO_COLLECTION = os.getenv('MONGO_COLLECTION',"coll")

class ManagerMongo():
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[MONGO_DB]
        self.collection = self.db[MONGO_COLLECTION]
    
    def init_collection(self):
        with open('suspicious_customers_orders.json', 'r') as file:
            data = json.load(file)
            try: 
                self.collection.insert_many(data)
            except Exception as e:
                print(f"error init collection {e}")
