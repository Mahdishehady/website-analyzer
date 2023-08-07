from pymongo import MongoClient


def count_eachDoc():
    client = MongoClient('mongodb://localhost:27017')
    db = client['news_db']
    collection = db['my_database']

    # Aggregation pipeline
    pipeline = [
        {
            "$group": {
                "_id": "$postID",
                "count": {"$sum": 1}
            }
        }
    ]

    # Execute the aggregation query
    result = collection.aggregate(pipeline)

    # Print the aggregation result
    for entry in result:
        print(entry)

    # Close the connection
    client.close()


count_eachDoc()
