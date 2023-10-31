from pymongo import MongoClient

from configs import MONGODB_CONNECTION, MONGODB_DATABASE, MONGODB_POSTS_COLLECTION


class MongoHelper:
    mongo_client = None

    @staticmethod
    def get_mongodb_posts_collection():
        if MongoHelper.mongo_client is None:
            MongoHelper.mongo_client = MongoClient(MONGODB_CONNECTION)

        db = MongoHelper.mongo_client[MONGODB_DATABASE]
        return db[MONGODB_POSTS_COLLECTION]


