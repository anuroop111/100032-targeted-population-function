from datetime import datetime, timedelta
import time
import pymongo
from config import HOST


DOWELL_TIME_EPOCH = 1609459200


def fetch_fields_from_db(fields, database, collection, start_point, end_point):
    projection = {'_id': 0}
    for field in fields:
        projection[field] = 1

    client = pymongo.MongoClient(HOST)
    database = client[database]
    collection = database[collection]
    response = collection.find({}, {'event_id': 1})
    rows = []

    for row in response:
        rows.append(row)

    bd_event_ids = []
    for row in rows:
        if 'event_id' in row:
            bd_event_ids.append(row['event_id'])

    event_database = client['Bangalore']
    event_collection = event_database['events']
    events_response = event_collection.find(
        {'eventId': {'$in': bd_event_ids}, 'dowell_time': {'$gte': start_point, '$lte': end_point}})

    event_ids = []
    for row in events_response:
        event_ids.append(row['eventId'])

    response = collection.find({'event_id': {'$in': event_ids}}, projection)
    rows = []

    for row in response:
        rows.append(row)
    client.close()

    return rows


def dowell_time_now():
    current_time = time.time()
    dt = current_time - DOWELL_TIME_EPOCH
    return int(dt)


def dowell_time(a_date_time):
    dtime_stamp = a_date_time.timestamp()
    current_time = int(round(dtime_stamp))
    dt = current_time - DOWELL_TIME_EPOCH
    return dt


def fetch_event_ids_from_db(time_input):
    if time_input['period'] == 'custom':
        start_point_date = datetime.strptime(time_input['start_point'], '%Y/%m/%d')
        end_point_point_date = datetime.strptime(time_input['end_point'], '%Y/%m/%d')

        start_dowell_time = dowell_time(start_point_date)
        end_dowell_time = dowell_time(end_point_point_date)

    elif time_input['period'] == 'life_time':
        start_dowell_time = 0
        end_dowell_time = dowell_time_now()
    else:
        start_point_date = get_date(time_input['period'])
        start_dowell_time = dowell_time(start_point_date)
        end_dowell_time = datetime.now()

    condition = {'dowell_time': {'$gte': start_dowell_time, '$lte': end_dowell_time}}

    client = pymongo.MongoClient(HOST)

    event_database = client['Bangalore']
    event_collection = event_database['events']
    events_response = event_collection.find(condition)

    event_ids = []
    for row in events_response:
        event_ids.append(row['eventId'])

    return event_ids, start_dowell_time, end_dowell_time


def get_date(period):
    today = datetime.now()

    if period == 'last_1_day':
        return today - timedelta(days=1)
    elif period == 'last_7_days':
        return today - timedelta(days=7)
    elif period == 'last_30_days':
        return today - timedelta(days=30)
    elif period == 'last_90_days':
        return today - timedelta(days=90)
    elif period == 'last_180_days':
        return today - timedelta(days=180)
    elif period == 'last_1_year':
        return today - timedelta(days=365)


def populate_db_query(time_input, stage_input_list):
    event_ids, start_dowell_time, end_dowell_time = fetch_event_ids_from_db(time_input)

    query = [
        {
            "$match": {
                time_input['column_name']: {"$exists": True},
                'eventId': {'$in': event_ids},
            }
        }
    ]

    and_array = []
    for stage in stage_input_list:
        if stage['data_type'] == 0:
            break
        elif stage['data_type'] == 'lot':
            continue

        condition_less = {stage['data_type']: {"$lte": float(stage['end_point'])}}
        condition_greater = {stage['data_type']: {"$gte": float(stage['start_point'])}}

        and_array.append(condition_greater)
        and_array.append(condition_less)

    if and_array:
        query[0]["$match"]['$and'] = and_array

    return query, start_dowell_time, end_dowell_time


def fetch_data_with_query(query, collection, database):
    client = pymongo.MongoClient(HOST)
    database = client[database]
    collection = database[collection]
    response = collection.aggregate(query)
    rows = []

    for row in response:
        rows.append(row)
    client.close()
    return rows


def get_data_for_distribution(time_input, stage_input_list, database_details):
    query, start_dowell_time, end_dowell_time = populate_db_query(time_input, stage_input_list)
    data = fetch_data_with_query(query, database_details['collection'], database_details['database'])
    return data, start_dowell_time, end_dowell_time
