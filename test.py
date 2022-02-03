import json
import requests

url = 'http://localhost:5000/api/targeted_population/app'

database_name = 'mongodb'
collection = "day001"
database = "Bangalore"
n_stage = 1
number_of_variables = 1
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
        'm_or_A_value': 500,
        'error': 10,
    },
]


request_data={
    'distribution_type': 'poisson',
    'database_name':database_name,
    'n_stage':n_stage,
    'number_of_variable':number_of_variables,
    'stages':stage_input_list,
    'collection':collection,
    'database':database

}
headers = {'content-type': 'application/json'}

response = requests.post(url, json=request_data,headers=headers)
print(response.text)

