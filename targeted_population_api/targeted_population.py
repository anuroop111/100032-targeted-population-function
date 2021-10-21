import json
import requests
def targeted_population(database, n_stage, number_of_variables, stage_input_list):
    url = 'http://127.0.0.1:5000/api/targeted_population/app'
    request_data={
        'database':database,
        'n_stage':n_stage,
        'number_of_variable':number_of_variables,
        'stages':stage_input_list,

    }
    headers = {'content-type': 'application/json'}

    response = requests.post(url, json=request_data,headers=headers)

    return response.text

