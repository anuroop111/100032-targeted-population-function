import random
import json
import requests
import pprint
import pandas
import random
import pymongo
from datetime import date, datetime, timedelta

from samplingrule.samplingrule import dowellsamplingrule
from distribution.distribution import dowelldistribution

HOST = "mongodb://user1:Test12345@cluster0-shard-00-00.n2ih9.mongodb.net:27017,cluster0-shard-00-01.n2ih9.mongodb.net:27017,cluster0-shard-00-02.n2ih9.mongodb.net:27017/Banglore?authSource=admin&replicaSet=atlas-heuz5b-shard-0&retryWrites=true&ssl=true&w=majority"


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
    print("rows")
    print(rows)
    bd_event_ids = []
    for row in rows:
        if 'event_id' in row:
            bd_event_ids.append(row['event_id'])

    event_database = client['Bangalore']
    event_collection = event_database['events']
    events_response = event_collection.find(
        {'eventId': {'$in': bd_event_ids}, 'dowell_time': {'$gte': start_point, '$lte': end_point}})

    # events_response = event_collection.find({'dowell_time':{'$lte':end_point, '$gte':start_point} } )
    event_ids = []
    for row in events_response:
        event_ids.append(row['eventId'])

    print(event_ids)
    print("here")

    response = collection.find({'event_id': {'$in': event_ids}}, projection)
    rows = []

    for row in response:
        rows.append(row)
    client.close()

    return rows


# query = [
#     {
#         "$match" : {
#             "C/10001": { "$exists": True },
#
#         }
#     }
# ]
# database='exhibitor_details'
# collection='exhibitor_details'
# fields={'_id','BDEvent_ID','brand_name', 'Timestamp'}
# fetch_fields_from_db(fields,database,collection)


def get_date(period):

    print("period.........", period)
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
        print("today - timedelta(days=365)", today - timedelta(days=365))
        return today - timedelta(days=365)


def populate_db_query(database, stage_input_list):
    query = [
        {
            "$match": {
                "C/10001": {"$exists": True},

            }
        }
    ]

    and_array = []
    condition_less = {}
    condition_greater = {}
    for stage in stage_input_list:
        if stage['d'] == 1:
            condition_less = {"C/10001": {"$lte": float(stage['end_point'])}}
            condition_greater = {"C/10001": {"$gte": float(stage['start_point'])}}
        elif stage['d'] == 2:
            condition_less = {"B/10002": {"$lte": float(stage['end_point'])}}
            condition_greater = {"B/10002": {"$gte": float(stage['start_point'])}}
        elif stage['d'] == 3:
            condition_less = {"C/10003": {"$lte": float(stage['end_point'])}}
            condition_greater = {"C/10003": {"$gte": float(stage['start_point'])}}
        elif stage['d'] == 4:
            condition_less = {"D/10004": {"$lte": float(stage['end_point'])}}
            condition_greater = {"D/10004": {"$gte": float(stage['start_point'])}}

        elif stage['d'] == 5:
            if stage['period'] == 'custom':
                start_point_date = datetime.strptime(stage['start_point'], '%Y/%m/%d')
                end_point_point_date = datetime.strptime(stage['end_point'], '%Y/%m/%d')
            elif stage['period'] == 'life_time':
                and_array.append({'Date': {"$lte": datetime.now()}})
                continue
            else:
                end_point_point_date = datetime.now()
                start_point_date = get_date(stage['period'])

            condition_less = {"Date": {"$lte": end_point_point_date}}
            condition_greater = {"Date": {"$gte": start_point_date}}

        elif stage['d'] == 0:
            break

        and_array.append(condition_greater)
        and_array.append(condition_less)
    query[0]["$match"]['$and'] = and_array

    return query


def call_dowellconnection_with_query(query, collection, database):
    client = pymongo.MongoClient(HOST)
    database = client[database]
    collection = database[collection]
    response = collection.aggregate(query)
    rows = []

    for row in response:
        rows.append(row)
    client.close()
    print("aggregate result")
    print(rows)
    return rows


def filter_lot_database(df, stage):
    proportion_selection = stage['p_r_selection']
    first_position = stage['first_position']
    last_position = stage['last_position']
    dataframe_size = len(df.index)

    if proportion_selection == "proportion":
        lot_size = int(dataframe_size * stage['proportion'] / 100)
        if first_position + lot_size - 1 <= dataframe_size:
            df = df[first_position - 1:lot_size]
            return df
        else:
            return pandas.DataFrame([])
    else:

        random_lot_size = random.randint(0, dataframe_size)
        if first_position + random_lot_size - 1 > dataframe_size:
            return pandas.DataFrame([])
        else:
            df = df[first_position - 1:random_lot_size]
            return df


def filter_df_population_average(df, column_name, stage):
    newpanda = df.sort_values(by=[column_name])
    # print('main data:')
    # print(newpanda)
    # print('------------'+ str(stage['d'])+"----------------")

    start = float(stage['start_point'])
    r = stage['r']
    range_end = start + r
    end = float(stage['end_point'])
    population_average = stage['m_or_A_value']
    a = stage['a']
    error_percent = stage['error']
    population_average_min = population_average - population_average * error_percent / 100
    population_average_max = population_average + population_average * error_percent / 100
    taken = 0
    summation = 0

    sum_of_taken_numbers = 0
    taken_number_count = 0

    for index, row in newpanda.iterrows():
        try:
            current_mean = sum_of_taken_numbers / taken_number_count
        except:
            current_mean = 0

        if current_mean == population_average:
            newpanda.drop(newpanda.index[index:], inplace=True)
            break
        if current_mean >= population_average_max or row[column_name] > end:
            newpanda.drop(newpanda.index[index:], inplace=True)
            break

        if start < row[column_name] and row[column_name] < range_end:
            if taken >= a:
                newpanda.drop(index, inplace=True)
            else:
                expected_sum_of_taken_numnbers = sum_of_taken_numbers + row[column_name]
                expected_taken_number_count = taken_number_count + 1
                expected_mean = expected_sum_of_taken_numnbers / expected_taken_number_count

                if expected_mean <= population_average_max:
                    taken = taken + 1
                    taken_number_count = expected_taken_number_count
                    sum_of_taken_numbers = expected_sum_of_taken_numnbers
                else:
                    newpanda.drop(index, inplace=True)
        else:
            while True:
                taken = 0
                start = range_end
                range_end = start + r

                if start < row[column_name] and row[column_name] < range_end:
                    expected_sum_of_taken_numnbers = sum_of_taken_numbers + row[column_name]
                    expected_taken_number_count = taken_number_count + 1
                    expected_mean = expected_sum_of_taken_numnbers / expected_taken_number_count

                    if expected_mean <= population_average_max:
                        taken = taken + 1
                        taken_number_count = expected_taken_number_count
                        sum_of_taken_numbers = expected_sum_of_taken_numnbers
                    else:
                        newpanda.drop(index, inplace=True)
                    break
                if range_end > end:
                    newpanda.drop(index, inplace=True)
                    break

    try:
        current_mean = sum_of_taken_numbers / taken_number_count
    except:
        current_mean = 0

    # print(newpanda)
    # print("population_average ",population_average, population_average_min, population_average_max)
    # print("current_mean", current_mean)
    # print("------filtered: "+str(stage['d'])+"--------------")

    if current_mean >= population_average_min and current_mean <= population_average_max:
        return newpanda
    else:
        return pandas.DataFrame([])


def filter_df_max_point(df, column_name, stage):
    newpanda = df.sort_values(by=[column_name])
    # print('main data:')
    # print(newpanda)
    # print('------------'+ str(stage['d'])+"----------------")

    start = float(stage['start_point'])
    r = stage['r']
    range_end = start + r
    end = float(stage['end_point'])
    error_percent = stage['error']
    max_sum = stage['m_or_A_value']

    max_sum_min = max_sum - max_sum * error_percent / 100
    max_sum_max = max_sum + max_sum * error_percent / 100
    a = stage['a']

    taken = 0
    summation = 0

    for index, row in newpanda.iterrows():
        if summation >= max_sum_max or row[column_name] > end:
            newpanda.drop(index, inplace=True)
            continue

        if start < row[column_name] and row[column_name] < range_end:
            if taken >= a:
                newpanda.drop(index, inplace=True)
            else:
                if summation + row[column_name] < max_sum_max:
                    taken = taken + 1
                    summation = summation + row[column_name]
                else:
                    newpanda.drop(index, inplace=True)
        else:
            while True:
                taken = 0
                start = range_end
                range_end = start + r
                if start < row[column_name] and row[column_name] < range_end:
                    if summation + row[column_name] < max_sum_max:
                        taken = taken + 1
                        summation = summation + row[column_name]
                    else:
                        newpanda.drop(index, inplace=True)
                    break
                if range_end > end:
                    newpanda.drop(index, inplace=True)
                    break

    # print('stage :d=1, start=0, end =1000, r=100, a=2')
    # print(newpanda)
    # print("------filtered: "+str(stage['d'])+"--------------")

    if summation >= max_sum_min and summation <= max_sum_max:
        return newpanda
    else:
        return pandas.DataFrame([])


def dowelltargetedpopulation(database_type, S, number_of_variable, stage_input_list, collection="day001",
                             database="Banglore"):
    # Define number of stages as variable "S"
    # stage_input_list[0]['d'] = 5
    # print(stage_input_list)
    # print('----------------------------------')
    query = populate_db_query(database, stage_input_list)

    print("query---")
    print(query)
    data = call_dowellconnection_with_query(query, collection, database)
    print("response", data)
    if not data:
        return "not any data within that date range", "Not Success"
    # print("-----------------------start-----------------------------")
    df = pandas.DataFrame(data)
    df = df.astype({'C/10001': 'float64', 'B/10002': 'float64', 'C/10003': 'float64', 'D/10004': 'float64'})

    # filter for all stages
    for stage in stage_input_list:

        d = stage['d']
        print("here is population_average", d)

        if d == 0:
            break
        elif d == 1:

            if stage['m_or_A_selction'] == 'population_average':

                df = filter_df_population_average(df, 'C/10001', stage)
            else:
                df = filter_df_max_point(df, 'C/10001', stage)
            if df.empty:
                print("not matched for ", d)
                return "not matched for datatype " + str(d), "Not Success"
        elif d == 2:
            if stage['m_or_A_selction'] == 'population_average':
                df = filter_df_population_average(df, 'B/10002', stage)
            else:
                df = filter_df_max_point(df, 'B/10002', stage)
            if df.empty:
                print("not matched for ", d)
                return "not matched for datatype " + str(d), "Not Success"
        elif d == 3:
            if stage['m_or_A_selction'] == 'population_average':
                df = filter_df_population_average(df, 'C/10003', stage)
            else:
                df = filter_df_max_point(df, 'C/10003', stage)
            if df.empty:
                print("not matched for ", d)
                return "not matched for datatype " + str(d), "Not Success"
        elif d == 4:
            if stage['m_or_A_selction'] == 'population_average':
                df = filter_df_population_average(df, 'D/10004', stage)
            else:
                df = filter_df_max_point(df, 'D/10004', stage)
            if df.empty:
                print("not matched for ", d)
                return "not matched for datatype " + str(d), "Not Success"
        elif d == 5:
            continue
        elif d == 6:
            continue
        elif d == 7:

            df = filter_lot_database(df, stage)
            if df.empty:
                return "selection is not matching the required lot size", "Not Success"
            continue

    # dowellsamplingrule(size of data, number of category)
    n = len(df.index)
    is_acceptable, sample_size, status = dowellsamplingrule(n, 1, number_of_variable)

    return df, status


#    if database == 'spreadsheet':
#            #=FILTER(Marks!A2:E,Marks!A2:A>date(2021,1,3),Marks!A2:A<date(2021,1,10))
#            query_str = '=FILTER(Marks!A2:E'+ db_query_logic + ')'
#            gSpreadsheet=GSpreadSheet(SPREADSHEET_ID)
#            print(query_str)
#            gSpreadsheet.fetch_data_by_updating_lookup_sheet(query_str)
#
#
#        #dowellsamplingrule()
#        #print("Enter distribution type")
#        #D=int(input())
#        #dowelldistribution(D)
#       #""" yet to implement """
#        #dowellenventcreation()


def fetch_collections(database):
    myclient = pymongo.MongoClient(
        "mongodb://user1:Test12345@cluster0-shard-00-00.n2ih9.mongodb.net:27017,cluster0-shard-00-01.n2ih9.mongodb.net:27017,cluster0-shard-00-02.n2ih9.mongodb.net:27017/Banglore?authSource=admin&replicaSet=atlas-heuz5b-shard-0&retryWrites=true&ssl=true&w=majority")

    mydb = myclient[database]

    # list the collections
    print("fetching mongodb")
    for coll in mydb.list_collection_names():
        print(coll)
    return mydb.list_collection_names()


def fetch_databases():
    myclient = pymongo.MongoClient(
        "mongodb://user1:Test12345@cluster0-shard-00-00.n2ih9.mongodb.net:27017,cluster0-shard-00-01.n2ih9.mongodb.net:27017,cluster0-shard-00-02.n2ih9.mongodb.net:27017/Banglore?authSource=admin&replicaSet=atlas-heuz5b-shard-0&retryWrites=true&ssl=true&w=majority")

    dbs = myclient.list_database_names()
    return dbs


database = 'spreadsheet'
stages = 3

stage_input_list = [
    {
        'd': 5,
        'm_or_A_selction': 'maximum_point',
        'm_or_A_value': 100,
        'error': 10,
        'r': 2,
        'start_point': '2021/01/08',
        'end_point': '2021/01/25',
        'a': 3,
    },
    {
        'd': 1,
        'm_or_A_selction': 'population_average',
        'm_or_A_value': 300,
        'error': 10,
        'r': 100,
        'start_point': 0,
        'end_point': 700,
        'a': 2,
    },
    {
        'd': 2,
        'm_or_A_selction': 'maximum_point',
        'm_or_A_value': 700,
        'error': 30,
        'r': 100,
        'start_point': 0,
        'end_point': 1000,
        'a': 1,
    }
]

# dowelltargetedpopulation(database, stages,1, stage_input_list)
