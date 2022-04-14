import json
import requests

url = 'https://100032.pythonanywhere.com/api/targeted_population/'

# database details
database_name = 'mongodb'
collection = "licenses"
database = "license"

# number of variables for sampling rule
number_of_variables = 1
distribution_type =  'normal'

# period can be 'custom' or 'last_1_day' or 'last_30_days' or 'last_90_days' or 'last_180_days' or 'last_1_year' or 'life_time'
# if custom is given then need to specify start_point and end_point
# for others datatpe 'm_or_A_selction' can be 'maximum_point' or 'population_average'
# the the value of that selection in 'm_or_A_value'
# error is the error allowed in percentage


time_input = {
    'column_name': 'Date',
    'period': 'last_1_year',
    'start_point': '2021/01/08',
    'end_point': '2021/01/25',
}
 
stage_input_list = [
]


request_data={
    'distribution_type': distribution_type,
    'database_name':database_name,
    'number_of_variable':number_of_variables,
    'stages':stage_input_list,
    'collection':collection,
    'database':database,
    'time_input':time_input,
}

headers = {'content-type': 'application/json'}

response = requests.post(url, json=request_data,headers=headers)

print(response.text)
