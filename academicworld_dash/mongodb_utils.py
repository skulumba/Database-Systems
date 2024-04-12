from pymongo import MongoClient

def mongo_connect_to_database():
    client = MongoClient('localhost', 27017)
    db = client.academicworld
    return db

def mongo_execute_query(query):
    db = mongo_connect_to_database()
    collection = db.faculty
    result = collection.aggregate(query)
    return result


def mongo_update_database(query):
    db = mongo_connect_to_database()
    db.query.update_one(query)
