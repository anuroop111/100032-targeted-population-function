from flask import Flask, render_template
from flask import request

import json
from bson import ObjectId
from datetime import date, datetime

from targeted_population import targeted_population

app = Flask(__name__)


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)

        if isinstance(o, (datetime, date)):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)


@app.route('/api/targeted_population/', methods=['POST', ])
def targeted_population_json_response():
    if request.method == 'POST':
        request_data = request.get_json()
        database_details = request_data['database_details']
        number_of_variable = request_data['number_of_variable']
        stage_input_list = request_data['stages']
        time_input = request_data['time_input']
        distribution_input = request_data['distribution_input']
        bernoulli = request_data.get('bernoulli', "")

        result = targeted_population(distribution_input, database_details, time_input, number_of_variable,
                                     stage_input_list, bernoulli)

        return JSONEncoder().encode(result)


@app.route('/', methods=["GET"])
def frontend_event_create():
    if request.method == "GET":
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
