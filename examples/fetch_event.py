import pymongo

HOST="mongodb://user1:Test12345@cluster0-shard-00-00.n2ih9.mongodb.net:27017,cluster0-shard-00-01.n2ih9.mongodb.net:27017,cluster0-shard-00-02.n2ih9.mongodb.net:27017/Banglore?authSource=admin&replicaSet=atlas-heuz5b-shard-0&retryWrites=true&ssl=true&w=majority"


client =  pymongo.MongoClient(HOST)
database=client['Bangalore']
collection=database['userdetails']
response=collection.find({})
rows = []

for row in response:
    rows.append(row)
#response=response._id
client.close()
# print("aggregate result")
print(rows)

