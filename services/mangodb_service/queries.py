import datetime

from pymongo import MongoClient


# 1 get count of news each day and check for duplication
def count_eachDoc():
    client = MongoClient('mongodb://localhost:27017')
    db = client['news_db']
    collection = db['my_database']

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
    # Close the connection
    client.close()


# count_eachDoc()

# 2 function that takes a day and return the count news in that day
def count_documents_by_published_date(date):
    client = MongoClient('mongodb://localhost:27017')
    db = client['news_db']
    collection = db['my_database']

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
    # Close the connection
    client.close()

    return doc_add


published_date = "2023-07-20"


# 3 get all topics about the news
def get_topics():
    client = MongoClient('mongodb://localhost:27017')
    db = client['news_db']
    collection = db['my_database']

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
    client = MongoClient('mongodb://localhost:27017')
    db = client['news_db']
    collection = db['my_database']
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
    client = MongoClient('mongodb://localhost:27017')
    db = client['news_db']
    collection = db['my_database']
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
    client = MongoClient('mongodb://localhost:27017')
    db = client['news_db']
    collection = db['my_database']
    dic = {}
    total_count = collection.count_documents({})
    dic['total'] = total_count

    return dic


# 8 get all the keywords from mongodb
def get_Keywords():
    client = MongoClient('mongodb://localhost:27017')
    db = client['news_db']
    collection = db['my_database']

    # Query the collection and retrieve the "keywords" field
    keywords_list = collection.distinct('keywords')

    return keywords_list


# function that returns a dictionary of each keyword occurrence
def count_each_topic():
    keywords = get_Keywords()
    data_count = {}
    client = MongoClient('mongodb://localhost:27017')
    db = client['news_db']
    collection = db['my_database']
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
