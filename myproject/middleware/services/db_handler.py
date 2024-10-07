from pymongo import MongoClient
from bson import ObjectId

class MongoDBHandler:
    def __init__(self, db_name="transport_db"):
        self.client = MongoClient("mongodb://mongodb:27017/")
        self.db = self.client[db_name]

    def insert_data(self, collection_name, data):
        """Insert single or batch data into the MongoDB collection."""
        collection = self.db[collection_name]

        # Check if data is a list (batch insert) or single document
        if isinstance(data, list):
            # Insert multiple documents at once
            collection.insert_many(data)
        else:
            # Insert a single document
            collection.insert_one(data)

    def get_data(self, collection_name, query={}):
        """Retrieve data from a MongoDB collection and convert ObjectId to string."""
        collection = self.db[collection_name]
        data = collection.find(query)
        
        # Convert ObjectId to string for JSON serialization
        result = []
        for document in data:
            document['_id'] = str(document['_id'])  # Convert ObjectId to string
            result.append(document)
        
        return result
