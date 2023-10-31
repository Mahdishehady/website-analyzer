import json
from pymongo import MongoClient


# push data to mongodb
from configs import MONGODB_CONNECTION, MONGODB_POSTS_COLLECTION, MONGODB_DATABASE
from services.mangodb_service.mongodb_connect import MongoHelper


def push_data(data):
    collection = MongoHelper.get_mongodb_posts_collection()
    if isinstance(data, list):
        collection.insert_many(data)
    else:
        # If data is a single document (a single dictionary)
        collection.insert_one(data)


# Select data from mongodb
def select_data():
    collection = MongoHelper.get_mongodb_posts_collection()

    # Retrieve data using find method
    cursor = collection.find({})  # Empty query retrieves all documents
    # {} inside the find, everything its like select * from

    for document in cursor:
        print(document)
        print("--------------------------------------------")
