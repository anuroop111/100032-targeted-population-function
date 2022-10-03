import json
import requests

url = 'http://127.0.0.1:5000/api/targeted_population/'
## production api url
#url = 'http://100032.pythonanywhere.com/api/targeted_population/'

database_details = {
    'database_name': 'mongodb',
    'collection': 'test',
    'database': 'Bangalore',
    'fields':["LENGTH"]
}


# number of variables for sampling rule
number_of_variables = -1

# for first stage it's mandatory to have d=5
# period can be 'custom' or 'last_1_day' or 'last_30_days' or 'last_90_days' or 'last_180_days' or 'last_1_year' or 'life_time'
# if custom is given then need to specify start_point and end_point
# for others datatpe 'm_or_A_selction' can be 'maximum_point' or 'population_average'
# the the value of that selection in 'm_or_A_value'
# error is the error allowed in percentage


time_input = {
    'column_name': 'Date',
    'split': 'week',
    'period': 'life_time',
    'start_point': '2021/01/08',
    'end_point': '2021/01/25',
}

stage_input_list = [
    {
        'data_type': 1,
        'm_or_A_selction': 'maximum_point',
        'm_or_A_value': 700,
        'error': 20,
        'r': 100,
        'start_point': 0,
        'end_point': 700,
        'a': 2,
    }
]

# distribution input
distribution_input={
    'normal': 0,
    'poisson':0,
    'binomial':1,
    'bernoulli':0
    
}

binomial = {
    'number_of_variable':13,
    'split_choice': 'simple',
    'split_decision': "Eliminate",
    'user_choice_value': 43,
    'function': ">",
    'marginal_error': "0",
    'error': 20,
}


request_data = {
    'database_details': database_details,
    'distribution_input': distribution_input,
    'number_of_variable': number_of_variables,
    'stages': stage_input_list,
    'time_input': time_input,
    'binomial': binomial,
}

headers = {'content-type': 'application/json'}

response = requests.post(url, json=request_data,headers=headers)

print(response.text)


