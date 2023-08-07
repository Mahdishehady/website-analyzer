from pymongo import MongoClient


def count_eachDoc():
    client = MongoClient('mongodb://localhost:27017')
    db = client['news_db']
    collection = db['my_database']

    # Aggregation pipeline
    pipeline = [
        {
            "$group": {
                "_id": "$_id",
                "count": {"$sum": 1}
            }
        }
    ]

    # Execute the aggregation query
    result = collection.aggregate(pipeline)
    get_dup = []
    # Print the aggregation result
    for entry in result:
        if entry['count'] == 2:
            get_dup.append(entry)
    print(get_dup)
    # Close the connection
    client.close()


count_eachDoc()
