import os

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from faker import Faker

def connect_to_db():
    client = MongoClient(os.getenv('MONGODB_URI', 'mongodb://localhost:27017/cats_db'))
    db = client.get_default_database('cats_db')
    return db.cats

def seed_db(collection):
    fake = Faker()
    cats = [
        {
            "name": fake.first_name(),
            "age": fake.random_int(min=1, max=15),
            "features": [fake.word() for _ in range(3)]
        } for _ in range(5)
    ]
    collection.insert_many(cats)

def create_cat(collection, name, age, features):
    cat = {
        "name": name,
        "age": age,
        "features": features
    }
    return collection.insert_one(cat)

def find_all_cats(collection):
    return list(collection.find())

def find_cat_by_name(collection, name):
    return collection.find_one({"name": name})

def update_cat_age(collection, name, new_age):
    return collection.update_one(
        {"name": name},
        {"$set": {"age": new_age}}
    )

def add_cat_feature(collection, name, new_feature):
    return collection.update_one(
        {"name": name},
        {"$push": {"features": new_feature}}
    )

def delete_cat_by_name(collection, name):
    return collection.delete_one({"name": name})

def delete_all_cats(collection):
    return collection.delete_many({})

if __name__ == "__main__":
    try:
        cats_collection = connect_to_db()

        seed_db(cats_collection)

        print("Connected to MongoDB successfully!")
    except ConnectionFailure:
        print("Failed to connect to MongoDB")
