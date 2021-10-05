
import random
import json
import requests
import pprint
import pandas
import datetime
import random

from samplingrule.samplingrule import dowellsamplingrule
from distribution.distribution import dowelldistribution

def populate_db_query(database,stage_input_list):
    query = [
        {
            "$match" : {
                "C/10001": { "$exists": True },

            }
        }
    ]

    and_array = []
    condition_less={}
    condition_greater={}
    for stage in stage_input_list:
        if stage['d'] == 1:
           condition_less = {"C/10001" : {"$lte" : float(stage['end_point'])}}
           condition_greater = {"C/10001" : {"$gte" : float(stage['start_point'])}}
        elif stage['d']==2:
           condition_less = {"B/10002" : {"$lte" : float(stage['end_point'])}}
           condition_greater = {"B/10002" : {"$gte" : float(stage['start_point'])}}
        elif stage['d']==3:
           condition_less = {"C/10003" : {"$lte" : float(stage['end_point'])}}
           condition_greater = {"C/10003" : {"$gte" : float(stage['start_point'])}}
        elif stage['d']==4:
           condition_less = {"D/10004" : {"$lte" : float(stage['end_point'])}}
           condition_greater = {"D/10004" : {"$gte" : float(stage['start_point'])}}

        elif stage['d']==5:
            condition_less = {"Date" : {"$lte" :stage['end_point']}}
            condition_greater = {"Date" : {"$gte" : stage['start_point']}}
#        elif stage['d']==6:
#           condition_less = {"C/10001" : {"$lte" : stage['start_point']},
#           condition_greater = {"C/10001" : {"$gte" : stage['end_point']},
#        elif stage['d']==7:
#            pass
        elif stage['d']==0:
            break

        and_array.append(condition_greater)
        and_array.append(condition_less)
    query[0]["$match"]['$and'] = and_array

    return query

def call_dowellconnection_with_query(query):

    url = 'http://100002.pythonanywhere.com/'
    data={
      "cluster": "FB",
      "database": "mongodb",
      "collection": "day001",
      "document": "day001",
      "team_member_ID": "12345432",
      "function_ID": "ABCDE",
      "command": "aggregate",
      "field": {
        "name":"Joy update",

          },
      'update_field':{
        "name": "Joy update",
        "phone": "123456",
        "age": "26",
        "language": "Englis",

       },
      "platform": "Bangalore",
      "query":query
    }
    headers = {'content-type': 'application/json'}

    response = requests.post(url, json =data,headers=headers)
    data=response.text
    print('response')
    print(data)

    return data

def filter_lot_database(df,stage ):
    proportion_selection = stage['p_r_selection']
    first_position = stage['first_position']
    last_position = stage['last_position']



    if proportion_selection == "proportion":
        proportion=stage['proportion']
        if proportion == (last_position-first_position+1):
            df=df[first_position-1:last_position]
            return df
        else:
            return pandas.DataFrame([])
    else:
        dataframe_size = len(df.index)
        random_lot_size = random.randint(0, dataframe_size)
        if first_position+random_lot_size-1>dataframe_size:
            return pandas.DataFrame([])
        else:
            df=df[first_position-1:random_lot_size]
            return df



def filter_df_population_average(df, column_name,stage ):
    newpanda= df.sort_values(by=[column_name])
    print('main data:')
    print(newpanda)
    print('------------'+ str(stage['d'])+"----------------")

    start = float(stage['start_point'])
    r=stage['r']
    range_end =start + r
    end = float(stage['end_point'])
    population_average = stage['m_or_A_value']
    a=stage['a']
    error_percent = stage['error']
    population_average_min = population_average - population_average*error_percent/100
    population_average_max = population_average + population_average*error_percent/100
    taken = 0
    summation =0

    sum_of_taken_numbers = 0
    taken_number_count = 0

    for index, row in newpanda.iterrows():
        try:
            current_mean = sum_of_taken_numbers/taken_number_count
        except:
            current_mean=0

        if current_mean == population_average:
            newpanda.drop(newpanda.index[index:], inplace=True)
            break
        if current_mean >= population_average_max or row[column_name]>end:
            newpanda.drop(newpanda.index[index:], inplace=True)
            break

        if start < row[column_name] and row[column_name] < range_end:
            if taken >=a:
                newpanda.drop(index, inplace=True)
            else:
                expected_sum_of_taken_numnbers =sum_of_taken_numbers+row[column_name]
                expected_taken_number_count=taken_number_count+1
                expected_mean = expected_sum_of_taken_numnbers/expected_taken_number_count

                if expected_mean <= population_average_max:
                    taken = taken+1
                    taken_number_count = expected_taken_number_count
                    sum_of_taken_numbers = expected_sum_of_taken_numnbers
                else:
                    newpanda.drop(index, inplace=True)
        else:
            while True:
                taken = 0
                start = range_end
                range_end = start + r

                if start < row[column_name] and row[column_name] < range_end:
                    expected_sum_of_taken_numnbers =sum_of_taken_numbers+row[column_name]
                    expected_taken_number_count=taken_number_count+1
                    expected_mean = expected_sum_of_taken_numnbers/expected_taken_number_count

                    if expected_mean <= population_average_max:
                        taken = taken+1
                        taken_number_count = expected_taken_number_count
                        sum_of_taken_numbers = expected_sum_of_taken_numnbers
                    else:
                        newpanda.drop(index, inplace=True)
                    break
                if range_end > end:
                    newpanda.drop(index, inplace=True)
                    break

    try:
        current_mean = sum_of_taken_numbers/taken_number_count
    except:
        current_mean=0

    print(newpanda)
    print("population_average ",population_average, population_average_min, population_average_max)
    print("current_mean", current_mean)
    print("------filtered: "+str(stage['d'])+"--------------")

    if current_mean>=population_average_min and current_mean<=population_average_max:
        return newpanda
    else:
        return pandas.DataFrame([])




def filter_df_max_point(df, column_name,stage ):
    newpanda= df.sort_values(by=[column_name])
    print('main data:')
    print(newpanda)
    print('------------'+ str(stage['d'])+"----------------")

    start = float(stage['start_point'])
    r=stage['r']
    range_end =start + r
    end = float(stage['end_point'])
    error_percent = stage['error']
    max_sum = stage['m_or_A_value']

    max_sum_min = max_sum - max_sum*error_percent/100
    max_sum_max = max_sum + max_sum*error_percent/100
    a=stage['a']

    taken = 0
    summation =0

    for index, row in newpanda.iterrows():
        if summation >= max_sum_max or row[column_name]>end:
            newpanda.drop(index, inplace=True)
            continue

        if start < row[column_name] and row[column_name] < range_end:
            if taken >=a:
                newpanda.drop(index, inplace=True)
            else:
                if summation+row[column_name]< max_sum_max:
                    taken = taken+1
                    summation=summation+row[column_name]
                else:
                    newpanda.drop(index, inplace=True)
        else:
            while True:
                taken = 0
                start = range_end
                range_end = start + r
                if start < row[column_name] and row[column_name] < range_end:
                    if summation+row[column_name]< max_sum_max:
                        taken = taken+1
                        summation=summation+row[column_name]
                    else:
                        newpanda.drop(index, inplace=True)
                    break
                if range_end > end:
                    newpanda.drop(index, inplace=True)
                    break


    #print('stage :d=1, start=0, end =1000, r=100, a=2')
    print(newpanda)
    print("------filtered: "+str(stage['d'])+"--------------")

    if summation>=max_sum_min and summation<=max_sum_max:
        return newpanda
    else:
        return pandas.DataFrame([])



def dowelltargetedpopulation(database, S, stage_input_list):

    #Define number of stages as variable "S"
    #stage_input_list[0]['d'] = 5
    # print(stage_input_list)
    # print('----------------------------------')
    query = populate_db_query(database,stage_input_list)

    print("query---")
    print(query)
    response_json = call_dowellconnection_with_query(query)
    print("response",response_json)
    print("-----------------------start-----------------------------")
    df = pandas.DataFrame(json.loads(response_json))
    df = df.astype({'C/10001':'float64','B/10002':'float64','C/10003':'float64','D/10004':'float64'})

    #filter for all stages
    for stage in stage_input_list:

        d= stage['d']
        print("here is population_average",d)

        if d==0:
            break
        elif d==1:

            if stage['m_or_A_selction'] == 'population_average':

                df = filter_df_population_average(df, 'C/10001', stage)
            else:
                df = filter_df_max_point(df, 'C/10001', stage)
            if df.empty:
                print("not matched for ",d)
                return "not matched for datatype "+str(d)
        elif d==2:
            if stage['m_or_A_selction'] == 'population_average':
                df = filter_df_population_average(df, 'B/10002', stage)
            else:
                df = filter_df_max_point(df, 'B/10002', stage)
            if df.empty:
                print("not matched for ",d)
                return "not matched for datatype "+str(d)
        elif d==3:
            if stage['m_or_A_selction'] == 'population_average':
                df = filter_df_population_average(df, 'C/10003', stage)
            else:
                df = filter_df_max_point(df, 'C/10003', stage)
            if df.empty:
                print("not matched for ",d)
                return "not matched for datatype "+str(d)
        elif d==4:
            if stage['m_or_A_selction'] == 'population_average':
                df = filter_df_population_average(df, 'D/10004', stage)
            else:
                df = filter_df_max_point(df, 'D/10004', stage)
            if df.empty:
                print("not matched for ",d)
                return "not matched for datatype "+str(d)
        elif d==5:
            continue
        elif d==6:
            continue
        elif d==7:
            print("here")
            df = filter_lot_database(df,stage)
            if df.empty:
                return "selection is not matching the required lot size"
            continue

    return df


#    if database == 'spreadsheet':
#            #=FILTER(Marks!A2:E,Marks!A2:A>date(2021,1,3),Marks!A2:A<date(2021,1,10))
#            query_str = '=FILTER(Marks!A2:E'+ db_query_logic + ')'
#            gSpreadsheet=GSpreadSheet(SPREADSHEET_ID)
#            print(query_str)
#            gSpreadsheet.fetch_data_by_updating_lookup_sheet(query_str)
#
#
#        #dowellsamplingrule()
#        #print("Enter distribution type")
#        #D=int(input())
#        #dowelldistribution(D)
#       #""" yet to implement """
#        #dowellenventcreation()




database='spreadsheet'
stages = 3

stage_input_list = [
    {
        'd':5,
        'm_or_A_selction':'maximum_point',
        'm_or_A_value': 100,
        'error':10,
        'r':2,
        'start_point': '2021/01/08',
        'end_point': '2021/01/25',
        'a': 3,
    },
    {
        'd':1,
        'm_or_A_selction':'population_average',
        'm_or_A_value': 300,
        'error':10,
        'r':100,
        'start_point': 0,
        'end_point': 700,
        'a': 2,
     },
    {
        'd':2,
        'm_or_A_selction':'maximum_point',
        'm_or_A_value': 700,
        'error':30,
        'r':100,
        'start_point': 0,
        'end_point': 1000,
        'a': 1,
    }




]

dowelltargetedpopulation(database, stages, stage_input_list)
