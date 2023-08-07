import json
from pymongo import MongoClient

"""
client = MongoClient('mongodb://localhost:27017')
db = client['news_db']
collection = db['my_database']

with open('meta_data.json', 'r', encoding="utf8") as json_file:
    data = json.load(json_file)

# Check if data is a list of documents (multiple dictionaries)
if isinstance(data, list):
    collection.insert_many(data)
else:
    # If data is a single document (a single dictionary)
    collection.insert_one(data)

client.close()
"""


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

