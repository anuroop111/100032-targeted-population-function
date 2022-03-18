from flask import Flask, render_template, make_response, render_template_string
from flask import request
import pandas
import json
from bson import ObjectId
from datetime import date, datetime

from targeted_population import dowelltargetedpopulation, fetch_collections, fetch_databases, fetch_fields_from_db
from targeted_population_poisson_distribution import dowelltargetedpopulation as poisson_distribution

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/mongodb')
def mongodb():
    collections = []
    databases = fetch_databases()
    return render_template('index.html', collections=collections, databases=databases)


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)

        if isinstance(o, (datetime, date)):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)


@app.route('/api/fetch-fields-from-db', methods=['POST', ])
def fetch_fields_from_db_json_response():
    request_data = request.get_json()
    database = request_data['database']
    collection = request_data['collection']
    fields = request_data['fields']
    start_point = request_data['start_point']
    end_point = request_data['end_point']
    data = fetch_fields_from_db(fields, database, collection, start_point, end_point)
    return JSONEncoder().encode(data)


@app.route('/api/targeted_population/', methods=['POST', ])
def targeted_population_json_response():
    if request.method == 'POST':
        request_data = request.get_json()
        database = request_data['database']
        collection = request_data['collection']
        number_of_variable = request_data['number_of_variable']
        stage_input_list = request_data['stages']
        time_input = request_data['time_input']

        # if request_data['distribution_type'] == 'poisson': results = poisson_distribution(database_type='mongodb',
        # time_input=time_input, number_of_variable=number_of_variable, stage_input_list=stage_input_list,
        # collection=collection, database=database) return {'isError': False, 'data': JSONEncoder().encode(results)}

        is_error, targeted_population, status = dowelltargetedpopulation(database_type='mongodb', time_input=time_input,
                                                                         number_of_variable=number_of_variable,
                                                                         stage_input_list=stage_input_list,
                                                                         collection=collection, database=database)

        return {'isError': is_error, 'data': JSONEncoder().encode(targeted_population), 'sampling_status': status}


if __name__ == '__main__':
    app.run(debug=True)
