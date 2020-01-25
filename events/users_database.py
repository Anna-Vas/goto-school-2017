from pymongo import MongoClient

connection = MongoClient("mongodb://eventmajor:morefun@ds161471.mlab.com:61471/events_server")
database = connection['events_server']
users_collection = database['users']

users = [
            {"name": "Athena", "email": "athena@vig-vam.com", "password": "12345"},
            {"name": "April", "email": "april.ryan@gmail.com", "password": "67890"},
        ]

users_collection.insert_many(users)
