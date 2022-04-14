import json
import requests

url = 'http://127.0.0.1:5000/api/targeted_population/'

# database name
database_name = 'mongodb'

collection = "licenses"
database = "license"

#database='Bangalore'
#collection='day001'

# number of variables for sampling rule
number_of_variables = 1

# for first stage it's mandatory to have d=5
# period can be 'custom' or 'last_1_day' or 'last_30_days' or 'last_90_days' or 'last_180_days' or 'last_1_year' or 'life_time'
# if custom is given then need to specify start_point and end_point
# for others datatpe 'm_or_A_selction' can be 'maximum_point' or 'population_average'
# the the value of that selection in 'm_or_A_value'
# error is the error allowed in percentage


time_input = {
    'column_name': 'Date',
    'period': 'last_30_days',
    'start_point': '2021/01/08',
    'end_point': '2021/01/25',
}

stage_input_list = []

# distribution input

distribution_input={
    'normal': 1,
    'poisson':1,
    'binomial':0,
    'bernoulli':1
    
}


request_data={
    'distribution_input': distribution_input,
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

########## example response ######

#{
#  "bernoulli": {
#    "error": "not implemented yet", 
#    "isError": true
#  }, 
#  "normal": {
#    "data": "{\"_id\": {\"6\": \"61432d8cb65e9b5c90a52abd\"}, \"Date\": {\"6\": \"2021-01-18T18:30:00\"}, \"C/10001\": {\"6\": 23.0}, \"B/10002\": {\"6\": 489.0}, \"C/10003\": {\"6\": 672.0}, \"D/10004\": {\"6\": 876.0}, \"Event Array\": {\"6\": \"[14,10blr000160505661e0b9b354e134006e]\"}, \"Process_id\": {\"6\": 1234}}", 
#    "isError": false, 
#    "sampling_status": "sample size is not adequate, univariate, 1<=1*10"
#  }, 
#  "poisson": {
#    "error": "not implemented yet", 
#    "isError": true
#  }
#}
########## example response ######

