import json
import requests
def targeted_population(database_name, n_stage, number_of_variables, stage_input_list, collection, database):
    url = 'http://100032.pythonanywhere.com/api/targeted_population/app'
    request_data={
        'database_name':database_name,
        'n_stage':n_stage,
        'number_of_variable':number_of_variables,
        'stages':stage_input_list,
        'collection':collection,
        'database':database

    }
    headers = {'content-type': 'application/json'}

    response = requests.post(url, json=request_data,headers=headers)
    return response.text


def fetch_fields_from_db(database_name, fields,collection, database, start_point, end_point):
    url = 'http://100032.pythonanywhere.com/api/fetch-fields-from-db'
    request_data={
        'fields':fields,
        'database_name':database_name,
        'collection':collection,
        'database':database,
        'start_point':start_point,
        'end_point':end_point,
    }
    headers = {'content-type': 'application/json'}

    response = requests.post(url, json=request_data,headers=headers)

    return response.text
