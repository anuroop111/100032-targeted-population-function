from pymongo.mongo_client import MongoClient
from datetime import date, datetime, timedelta


HOST = "mongodb://user1:Test12345@cluster0-shard-00-00.n2ih9.mongodb.net:27017,cluster0-shard-00-01.n2ih9.mongodb.net:27017,cluster0-shard-00-02.n2ih9.mongodb.net:27017/Banglore?authSource=admin&replicaSet=atlas-heuz5b-shard-0&retryWrites=true&ssl=true&w=majority"


client = MongoClient(HOST)
database = client['license']
collection = database['licenses']
#today = datetime.now()
#
#for i in range(0, 10):
#    response = collection.insert({"Date" : today-timedelta(days=i)})
#    print(response)

query = [{'$match': {'Date': {'$exists': True}, '$and': [{'Date': {'$lte': datetime(2022, 3, 11, 9, 25, 53, 676971)}}]}}]

response = collection.aggregate(query)
rows = []

for row in response:
    rows.append(row)
client.close()
print("aggregate result")
print(rows)
