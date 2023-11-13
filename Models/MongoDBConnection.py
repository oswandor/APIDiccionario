from pymongo import MongoClient

class MongoDBConnection:
    def __init__(self, uri):
        self.uri = uri
        self.client = None
        self.collection = None

    def connect(self, db_name, collection_name):
        try:
            self.client = MongoClient(self.uri)
            db = self.client[db_name]
            self.collection = db[collection_name]
        except Exception as e:
            print(e)

    def perform_query(self, query={}):
        try:
            return self.collection.find_one(query)
        except Exception as e:
            print(e)

    def perform_queryall(self): 
        try:
            return self.collection.find()
        except Exception as e: 
            print(e) 

    def aggregate_query(self, pipeline):
        try:
            return list(self.collection.aggregate(pipeline))
        except Exception as e:
            print(e)

    def disconnect(self):
        if self.client is not None:
            self.client.close()
            print("Disconnected from MongoDB.")
