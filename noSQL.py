import datetime

from pymongo import MongoClient


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


# count_documents_by_published_date(published_date)


def get_topics():
    client = MongoClient('mongodb://localhost:27017')
    db = client['news_db']
    collection = db['my_database']

    # Query the collection and retrieve the "keywords" field
    topics_list = collection.distinct('topics')

    return topics_list


# print(get_topics())


def news_by_dates(get_start_date, get_end_date):
    data = {}
    while not str(get_start_date.date()) == str(get_end_date.date()):
        data[str(get_start_date.date())] = count_documents_by_published_date(str(get_start_date.date()))
        get_start_date = get_start_date + datetime.timedelta(days=1)

    return data


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


count_topics()
