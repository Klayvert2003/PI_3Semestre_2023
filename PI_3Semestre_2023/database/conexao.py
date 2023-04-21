import pymongo

class ConexaoMongoDB():
    def __init__(self, locations=False):
        self.my_client = pymongo.MongoClient('mongodb://localhost:27017')
        self.db_name = 'Locations' if locations else 'Users'
        self.collection_name = 'Address' if locations else 'Credentials'
        self.collection = self.my_client[self.db_name][self.collection_name]