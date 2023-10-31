import datetime

from pymongo import MongoClient

import re

# 1 get count of news each day and check for duplication
from services.mangodb_service.mongodb_connect import MongoHelper


def count_eachDoc():
    collection = MongoHelper.get_mongodb_posts_collection()
    # Aggregation pipeline
    pipeline = [
        {
            "$group": {
                "_id": "$publishedDate",
                "count": {"$sum": 1}
            }
        }
    ]

    # Execute the aggregation query
    result = collection.aggregate(pipeline)
    # get_dup = []
    # Print the aggregation result
    for entry in result:
        # if entry['count'] == 2:
        # get_dup.append(entry)
        print(entry)


# count_eachDoc()

# 2 function that takes a day and return the count news in that day
def count_documents_by_published_date(date):
    collection = MongoHelper.get_mongodb_posts_collection()

    # Aggregation pipeline
    pipeline = [
        {
            "$match": {
                "publishedDate": {"$regex": date}
            }
        },
        {
            "$group": {
                "_id": "$publishedDate",
                "count": {"$sum": 1}
            }
        }
    ]

    # Execute the aggregation query
    result = collection.aggregate(pipeline)

    # Print the aggregation result
    list_news = []
    doc_add = 0
    for entry in result:
        list_news.append(entry)
    for x in range(0, len(list_news)):
        doc_add += int(list_news[x]['count'])

    return doc_add


published_date = "2023-07-20"


# 3 get all topics about the news
def get_topics():
    collection = MongoHelper.get_mongodb_posts_collection()

    # Query the collection and retrieve the "keywords" field
    topics_list = collection.distinct('topics')

    return topics_list


# print(get_topics())

# 4 get news between to given dates
def news_by_dates(get_start_date, get_end_date):
    data = {}
    while not str(get_start_date.date()) == str(get_end_date.date()):
        data[str(get_start_date.date())] = count_documents_by_published_date(str(get_start_date.date()))
        get_start_date = get_start_date + datetime.timedelta(days=1)

    return data


# 5
def count_topics():
    collection = MongoHelper.get_mongodb_posts_collection()

    pipeline = [
        {
            "$group": {
                "_id": "$topics",
                "count": {"$sum": 1}
            }
        }
    ]
    result = collection.aggregate(pipeline)

    topic_count_dict = {item["_id"]: item["count"] for item in result}

    # Sort the dictionary by values
    sorted_dict = dict(sorted(topic_count_dict.items(), key=lambda item: item[1]))

    print(sorted_dict)
    return sorted_dict


# count_topics()


# 6 search if news to insert is in mongodb or not
def search_for_occurrence(id):
    collection = MongoHelper.get_mongodb_posts_collection()

    # Perform the query

    count = collection.count_documents({"postID": "id"})
    # Check if any documents were found
    if count > 0:
        print(" documents found.".count)
        return True
    else:
        print("No documents found ,Insert")
        return False


# 7 get the total of articles in the db
def get_total_articles():
    collection = MongoHelper.get_mongodb_posts_collection()

    dic = {}
    total_count = collection.count_documents({})
    dic['total'] = total_count

    return dic


# 8 get all the keywords from mongodb
def get_Keywords():
    collection = MongoHelper.get_mongodb_posts_collection()

    # Query the collection and retrieve the "keywords" field
    keywords_list = collection.distinct('keywords')

    return keywords_list[:10]


# function that returns a dictionary of each keyword occurrence
def count_each_topic():
    keywords = get_Keywords()
    data_count = {}
    collection = MongoHelper.get_mongodb_posts_collection()

    for keyword in keywords:
        # Aggregation pipeline
        pipeline = [
            {
                '$unwind': "$keywords"
            },
            {
                '$match': {
                    'keywords': keyword
                }
            },
            {
                '$group': {
                    '_id': None,
                    'count': {'$sum': 1}
                }
            }]
        # Execute the aggregation query
        result = collection.aggregate(pipeline)
        # data_count[str(keyword)]=
        for entry in result:
            data_count[str(keyword)] = entry['count']
    return data_count


# count_each_topic()

# Get data and arrange them 0-100 ,100-200 ,200-400, >400
def get_Ranged_data():
    collection = MongoHelper.get_mongodb_posts_collection()

    # cursor is a python dictionary
    cursor = collection.find({})
    a = 0
    b = 0
    c = 0
    d = 0
    temp = {}
    for document in cursor:
        if 0 < int(document['wordCount']) < 100 or None:
            a = a + 1
        elif 100 <= int(document['wordCount']) < 200:
            b = b + 1
        elif 200 <= int(document['wordCount']) < 400:
            c = c + 1
        else:
            d = d + 1
    temp['bet0and100'] = a
    temp['bet100and200'] = b
    temp['bet200and400'] = c
    temp['bet400andmore'] = d
    return temp


def searchForSubstring(substring):
    if substring == "":
        return []
    # Connect to MongoDB
    collection = MongoHelper.get_mongodb_posts_collection()

    # Create a regular expression pattern for the substring
    pattern = re.compile(substring, re.IGNORECASE)  # Case-insensitive search

    # Query MongoDB using the regular expression pattern
    query = {"description": {"$regex": pattern}}
    results = collection.find(query)
    data = []

    for index, document in enumerate(results):
        data.append({'description': document['description'],
                     'postID': document['postID'],
                     'wordCount': document['wordCount']
                     })

    return data
