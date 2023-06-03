import pymongo


def fetch_collections(database):
    my_client = pymongo.MongoClient("some keys")

    my_db = my_client[database]
    return my_db.list_collection_names()


def fetch_databases():
    my_client = pymongo.MongoClient("")

    dbs = my_client.list_database_names()
    return dbs



