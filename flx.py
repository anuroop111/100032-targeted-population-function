from flask import Flask, render_template, make_response, render_template_string
from flask import request
import pandas
import json
from bson import ObjectId

from targeted_population import dowelltargetedpopulation, fetch_collections, fetch_databases, fetch_fields_from_db
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
        return json.JSONEncoder.default(self, o)

@app.route('/api/fetch-fields-from-db', methods = ['POST',])
def fetch_fields_from_db_json_response():
    request_data = request.get_json()
    database= request_data['database']
    collection= request_data['collection']
    fields= request_data['fields']
    start_point= request_data['start_point']
    end_point= request_data['end_point']
    data = fetch_fields_from_db(fields,database,collection, start_point, end_point)
    return JSONEncoder().encode(data)

@app.route('/api/targeted_population/app',methods = ['POST',])
def targeted_population_json_response():
    if request.method == 'POST':
        stages_form_data=request.get_json()
        S = stages_form_data['n_stage']
        database= stages_form_data['database']
        collection= stages_form_data['collection']

        number_of_variable = stages_form_data['number_of_variable']
        stage_input_list = stages_form_data['stages']
        targeted_population, status = dowelltargetedpopulation('mongodb', S,number_of_variable, stage_input_list ,collection=collection,database=database)

        if isinstance(targeted_population, pandas.DataFrame):
            return {'isError':False, 'data':targeted_population.to_dict('dict'), 'sampling_status':status}
        return {'isError':True, 'data':targeted_population, 'status':'error'}


@app.route('/api/targeted_population',methods = ['GET', 'POST'])
def hello_name():
    if request.method == 'POST':
        stages_form_data = request.form.to_dict(flat=False)

        database=stages_form_data['database_name'][0]
        print("database", database)
        databases = fetch_databases()
        if database == 'Select database':
            return render_template('index.html', collections=[], databases=databases)

        collection=stages_form_data['collection'][0]
        print("database", collection)
        if collection == "Select collections":
            collections = fetch_collections(database)
            return render_template('index.html', collections=collections, databases=databases)

        S = int(stages_form_data['n_stage'][0])

        print("----------------------", collection)
        number_of_variable = int(stages_form_data['number_of_variable'][0])
        stage_input_list=[]
        for i in range(0,S):
            stage = {}
            d = int(stages_form_data['datatype'][i])
            if d == 0:
                break
            if d == 7:
                stage['d']=7
                stage['p_r_selection']=stages_form_data['p_r_selection'][0]
                stage['proportion']=int(stages_form_data['proportion'][0])
                stage['first_position']=int(stages_form_data['first_position'][0])
                stage['last_position']=int(stages_form_data['last_position'][0])
                stage_input_list.append(stage)
                continue
            stage['d'] = d
            stage['m_or_A_selction']=stages_form_data['max_or_agv'][i]
            stage['m_or_A_value']=float(stages_form_data['max_avg_val'][i])
            stage['error']= float(stages_form_data['error_percent'][i])
            stage['r']=float(stages_form_data['range'][i])
            stage['start_point']= stages_form_data['start_point'][i]
            stage['end_point']= stages_form_data['end_point'][i]
            stage['a']= float(stages_form_data['a'][i])
            stage_input_list.append(stage)

        print("stage input fil",stage_input_list)
        targeted_population, status = dowelltargetedpopulation('mongodb', S,number_of_variable, stage_input_list,collection=collection,database=database)
        status_html = '<p><b>Sampling rule: </b>'+ status + '</p>'
        if isinstance(targeted_population, pandas.DataFrame):
            #targeted_population.loc["Sum"]=targeted_population.sum()
            df_html = targeted_population.to_html()
            describe_html = targeted_population.agg({'C/10001':['sum','mean','std'],'B/10002':['sum','mean','std',],'C/10003':['sum','mean','std',],'D/10004':['sum','mean','std',]}).to_html()
            resp = make_response(render_template_string(df_html+'<br><br>'+describe_html+ '<br><br>'+status_html))
            return resp
        return targeted_population

if __name__ == '__main__':
   app.run(debug = True)
