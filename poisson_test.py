import json
import requests

url = 'http://100032.pythonanywhere.com/api/targeted_population/app'

# database name
database_name = 'mongodb'
#collection name
collection = "day001"
# name of the database
database = "Bangalore"

#number of stages
n_stage = 2
# number of variables for sampling rule
number_of_variables = 1

##set distribution type 'normal' for normal distribution
distribution_type =  'poisson'

# for first stage it's mandatory to have d=5
# period can be 'custom' or 'last 1 day' or 'last 30 days' or 'last 90 days' or 'last 180 days' or 'last 1 year' or 'life time'
# if custom is given then need to specify start_point and end_point
# for others datatpe 'm_or_A_selction' can be 'maximum_point' or 'population_average'
# the the value of that selection in 'm_or_A_value'
# error is the error allowed in percentage

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
        'm_or_A_selction': 'maximum_point',#'population_average'
        'm_or_A_value': 500,
        'error': 10,
    },
]


request_data={
    'distribution_type': distribution_type,
    'database_name':database_name,
    'n_stage':n_stage,
    'number_of_variable':number_of_variables,
    'stages':stage_input_list,
    'collection':collection,
    'database':database

}
headers = {'content-type': 'application/json'}

response = requests.post(url, json=request_data,headers=headers)

##response will look like this
# {
#    'data':[], #a list of response data
#    'isError':false #boolean value indicates if the result is error or not
# }
print(response.text)

