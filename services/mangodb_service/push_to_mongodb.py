import json
from pymongo import MongoClient


# push data to mongodb
def push_data(data):
    client = MongoClient('mongodb://localhost:27017')
    db = client['news_db']
    collection = db['my_database']
    if isinstance(data, list):
        collection.insert_many(data)
    else:
        # If data is a single document (a single dictionary)
        collection.insert_one(data)
    client.close()


# Select data from mongodb
def select_data():
    client = MongoClient('mongodb://localhost:27017')
    db = client['news_db']
    collection = db['my_database']
    # Retrieve data using find method
    cursor = collection.find({})  # Empty query retrieves all documents
    # {} inside the find, everything its like select * from

    for document in cursor:
        print(document)
        print("--------------------------------------------")
    client.close()
