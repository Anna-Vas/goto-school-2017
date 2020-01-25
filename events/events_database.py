from pymongo import MongoClient

connection = MongoClient("mongodb://eventmajor:morefun@ds161471.mlab.com:61471/events_server")
database = connection['events_server']
events_collection = database['events']

events = [
            {"id": 1, "name": "Spiderman: Homecoming", "date": "July 6, 2017", "description": " Peter Parker balances his life as an ordinary high school student in Queens with his superhero alter-ego Spider-Man, and finds himself on the trail of a new menace prowling the skies of New York City.", "visitors": []},
            {"id": 2, "name": "Thor: Ragnarok", "date": "November 2, 2017", "description": "Imprisoned on the planet Sakaar, Thor must race against time to return to Asgard and stop Ragnarök, the destruction of his world, at the hands of the powerful and ruthless villain Hela.", "visitors": []},
            {"id": 3, "name": "Avengers: Infinity War", "date": "May 3, 2018", "description": " The Avengers and their allies must be willing to sacrifice all in an attempt to defeat the powerful Thanos before his blitz of devastation and ruin puts an end to the universe.", "visitors": []},
        ]

events_collection.insert_many(events)
