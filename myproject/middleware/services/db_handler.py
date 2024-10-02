# db_handler.py
from pymongo import MongoClient

# Change from localhost to the MongoDB service name 'mongodb'
MONGODB_URI = "mongodb://mongodb:27017"  # Correct the host here
client = MongoClient(MONGODB_URI)

class MongoDBHandler:
    def __init__(self):
        self.db = client["transport_db"]

    def insert_data(self, collection, data):
        col = self.db[collection]
        col.insert_one(data)
