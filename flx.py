from flask import Flask
from flask import request
import json
from bson import ObjectId
from datetime import date, datetime

from get_data_tools import fetch_fields_from_db
from targeted_population import targeted_population

app = Flask(__name__)


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
        database_details = request_data['database_details']
        number_of_variable = request_data['number_of_variable']
        stage_input_list = request_data['stages']
        time_input = request_data['time_input']

        distribution_input = request_data['distribution_input']

        result = targeted_population(distribution_input, database_details, time_input, number_of_variable,
                                     stage_input_list)

        return JSONEncoder().encode(result)


if __name__ == '__main__':
    app.run(debug=True)
