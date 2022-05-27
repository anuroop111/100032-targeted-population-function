import pymongo


def fetch_collections(database):
    my_client = pymongo.MongoClient(
        "mongodb://user1:Test12345@cluster0-shard-00-00.n2ih9.mongodb.net:27017,"
        "cluster0-shard-00-01.n2ih9.mongodb.net:27017,"
        "cluster0-shard-00-02.n2ih9.mongodb.net:27017/Banglore?authSource=admin&replicaSet=atlas-heuz5b-shard-0"
        "&retryWrites=true&ssl=true&w=majority")

    my_db = my_client[database]
    return my_db.list_collection_names()


def fetch_databases():
    my_client = pymongo.MongoClient(
        "mongodb://user1:Test12345@cluster0-shard-00-00.n2ih9.mongodb.net:27017,"
        "cluster0-shard-00-01.n2ih9.mongodb.net:27017,"
        "cluster0-shard-00-02.n2ih9.mongodb.net:27017/Banglore?authSource=admin&replicaSet=atlas-heuz5b-shard-0"
        "&retryWrites=true&ssl=true&w=majority")

    dbs = my_client.list_database_names()
    return dbs



