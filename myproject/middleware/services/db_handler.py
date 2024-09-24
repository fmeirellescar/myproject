# services/db_handler.py
from pymongo import MongoClient
from config import MONGODB_URI

class MongoDBHandler:
    def __init__(self):
        self.client = MongoClient(MONGODB_URI)
        self.db = self.client["transport_db"]

    def insert_data(self, collection, data):
        col = self.db[collection]
        col.insert_one(data)

    def get_data(self, collection, query):
        col = self.db[collection]
        return col.find(query)

# Example usage:
# db = MongoDBHandler()
# db.insert_data("passengers", {"vehicle_id": "123", "count": 45})

