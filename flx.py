from flask import Flask, render_template, make_response, render_template_string
from flask import request
import pandas
import json
from targeted_population import dowelltargetedpopulation
app = Flask(__name__)


@app.route('/')
def index():
   return render_template('index.html')


@app.route('/api/targeted_population',methods = ['GET', 'POST'])
def hello_name():
    if request.method == 'POST':
        stages_form_data = request.form.to_dict(flat=False)
        S = int(stages_form_data['n_stage'][0])
        stage_input_list=[]
        for i in range(0,S):
            stage = {}
            d = int(stages_form_data['datatype'][i])
            if d == 0:
                break
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
        targeted_population = dowelltargetedpopulation('mongodb', S, stage_input_list)
        if isinstance(targeted_population, pandas.DataFrame):
            #targeted_population.loc["Sum"]=targeted_population.sum()
            df_html = targeted_population.to_html()
            describe_html = targeted_population.agg({'C/10001':['sum','mean','std'],'B/10002':['sum','mean','std',],'C/10003':['sum','mean','std',],'D/10004':['sum','mean','std',]}).to_html()
            resp = make_response(render_template_string(df_html+'<br><br>'+describe_html))
            return resp
        return targeted_population

if __name__ == '__main__':
   app.run(debug = True)
