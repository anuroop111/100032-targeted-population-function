# import json
# import requests
#
# url = 'http://127.0.0.1:5000/api/targeted_population/'
# # production api url
# # url = 'http://100032.pythonanywhere.com/api/targeted_population/'
#
# database_details = {
#     'database_name': 'mongodb',
#     'collection': 'licenses',
#     'database': 'license',
#     'fields': ['eventId']
# }
#
# # number of variables for sampling rule
# number_of_variables = -1
#
# # for first stage it's mandatory to have d=5 period can be 'custom' or 'last_1_day' or 'last_30_days' or
# # 'last_90_days' or 'last_180_days' or 'last_1_year' or 'life_time' if custom is given then need to specify
# # start_point and end_point for others datatype 'm_or_A_selection' can be 'maximum_point' or 'population_average' the
# # the value of that selection in 'm_or_A_value' error is the error allowed in percentage
#
#
# time_input = {
#     'column_name': 'Date',
#     'split': 'week',
#     'period': 'last_30_days',
#     'start_point': '2021/01/08',
#     'end_point': '2021/01/25',
# }
#
# stage_input_list = [
#     {
#         'data_type': 1,
#         'm_or_A_selction': 'maximum_point',
#         'm_or_A_value': 700,
#         'error': 20,
#         'r': 100,
#         'start_point': 0,
#         'end_point': 700,
#         'a': 2,
#     }
# ]
#
# # distribution input
# distribution_input = {
#     'normal': 0,
#     'poisson': 0,
#     'binomial': 0,
#     'bernoulli': 1
#
# }
#
# request_data = {
#     'database_details': database_details,
#     'distribution_input': distribution_input,
#     'number_of_variable': number_of_variables,
#     'stages': stage_input_list,
#     'time_input': time_input,
# }
#
# headers = {'content-type': 'application/json'}
#
# response = requests.post(url, json=request_data, headers=headers)
#
# print(response.text)

import json
import requests

url = 'http://127.0.0.1:5000/api/targeted_population/'
## production api url
# url = 'http://100032.pythonanywhere.com/api/targeted_population/'

database_details = {
    'database_name': 'mongodb',
    'collection': 'licenses',
    'database': 'license',
    'fields':['eventId']
}


# number of variables for sampling rule
number_of_variables = -1

# for first stage it's mandatory to have d=5 period can be 'custom' or 'last_1_day' or 'last_30_days' or
# 'last_90_days' or 'last_180_days' or 'last_1_year' or 'life_time' if custom is given then need to specify
# start_point and end_point for others datatpe 'm_or_A_selction' can be 'maximum_point' or 'population_average' the
# the value of that selection in 'm_or_A_value' error is the error allowed in percentage


time_input = {
    'split': 'week',
    'period': 'last_1_day',
    'start_point': '2021/01/08',
    'end_point': '2021/01/25',
}

stage_input_list = [
]

# distribution input
distribution_input = {
    'normal': 0,
    'poisson': 0,
    'binomial': 0,
    "bernoulli": 1

}

bernoulli = {
    'error_size': 0.167,
    'test_number': 7,
    'selection_start_point': 500,
    'items_to_be_selected': 600,
}


request_data = {
    'database_details': database_details,
    'distribution_input': distribution_input,
    'number_of_variable': number_of_variables,
    'stages': stage_input_list,
    'time_input': time_input,
    'bernoulli': bernoulli,
}

headers = {'content-type': 'application/json'}

response = requests.post(url, json=request_data, headers=headers)

print(response.text)
