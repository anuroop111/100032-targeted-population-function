import pymongo
import pandas
from datetime import date, datetime, timedelta
from targeted_population import populate_db_query, call_dowellconnection_with_query

HOST = "mongodb://user1:Test12345@cluster0-shard-00-00.n2ih9.mongodb.net:27017,cluster0-shard-00-01.n2ih9.mongodb.net:27017,cluster0-shard-00-02.n2ih9.mongodb.net:27017/Banglore?authSource=admin&replicaSet=atlas-heuz5b-shard-0&retryWrites=true&ssl=true&w=majority"


def dowelltargetedpopulation(database_type, n_stage, number_of_variable, stage_input_list, collection="day001",
                             database="Bangalore"):
    date_stage_only_list = stage_input_list[:1]
    query, result_start_date, result_end_date = populate_db_query(database, date_stage_only_list)
    data = call_dowellconnection_with_query(query, collection, database)

    if not data:
        return "not any data within that date range", "Not Success"

    split = stage_input_list[0]['split']
    date_ranges = generate_date_range_list(split, result_start_date, result_end_date)

    print("split result -----------------")

    split_data = split_by_date_ranges(data, date_ranges)

    for s in split_data:
        print(s)

    print("length::", len(split_data))

    result = []
    for stage in stage_input_list[1:]:
        max_sum = stage['m_or_A_value']
        if stage['d'] == 1:
            column_name = 'C/10001'

        result = result + generate_split_for_data_type(max_sum, split_data, column_name)
        split_data = result
    return result


def generate_split_for_data_type(max_sum, split_data, column_name):
    result_list_for_stage = []
    for single_split_data in split_data:
        new_sub_split_for_data_type = []

        list_up_to_max_sum = []
        sum = 0
        for d in single_split_data:
            if d[column_name] > max_sum:
                print("error violated rules")

            if sum + d[column_name] <= max_sum:
                sum = sum + d[column_name]
                list_up_to_max_sum.append(d)
            else:
                new_sub_split_for_data_type.append(list_up_to_max_sum)
                list_up_to_max_sum = []
                sum = d[column_name]
                list_up_to_max_sum.append(d)

        result_list_for_stage = result_list_for_stage + new_sub_split_for_data_type

    return result_list_for_stage


def generate_date_range_list(split_by, start_date, end_date):
    if split_by == 'day':
        increment_by = timedelta(days=1)
    elif split_by == 'week':
        increment_by = timedelta(days=7)

    i = start_date
    result = []
    while i < end_date:
        result.append((i, i + increment_by))
        i = i + increment_by

    return result


def split_by_date_ranges(data, date_ranges):

    split_results = []

    for range in date_ranges:
        data_in_range = []
        for d in data:
            if range[0] <= d['Date'] < range[1]:
                data_in_range.append(d)

        split_results.append(data_in_range)

    return split_results


database_type = 'mongodb'
n_stage = 1
number_of_variable = 1
stage_input_list = [
    {
        'd': 5,
        'split': 'week',
        'period': 'custom',
        'start_point': '2021/01/08',
        'end_point': '2021/01/25',
    },
    {
        'd': 1,
        'm_or_A_selction': 'maximum_point',
        'm_or_A_value': 800,
        'error': 10,
    },
]

result = dowelltargetedpopulation(database_type, n_stage, number_of_variable, stage_input_list, "day001", "Bangalore")

for r in result:
    print('result set --------------')
    print(r)

print('result size: ', len(result))
