from pymongo.mongo_client import MongoClient

class MongoDBConnection:
    def __init__(self, uri):
        self.uri = uri
        self.client = None 
        self.collection = None 

    def connect(self):
        try:
            self.client = MongoClient(self.uri)
            db = self.client.dbdiccionario
            self.collection = db.diccionario 
        except Exception as e:
            print(e)

    def perform_query(self, query={}):
        try:
            return self.collection.find_one(query)
        except Exception as e:
            print(e)

    def disconnect(self):
        if self.client is not None:
            self.client.close()
            print("Disconnected from MongoDB.")



