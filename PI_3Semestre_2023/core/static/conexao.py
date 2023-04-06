import pymongo

class ConexaoMongoDB():
    my_client = pymongo.MongoClient('mongodb://localhost:27017')
    db_name = my_client['Users']
    collection = db_name['Credentials']