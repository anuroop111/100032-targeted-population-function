import json
import requests
import pprint
import pandas
import datetime

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
  "query":[{'$match': {'C/10001': {'$exists': True}, '$and': [{'Date': {'$gte': '2021/01/08'}}, {'Date': {'$lte': '2021/01/25'}}, {'C/10001': {'$gte': 0}}, {'C/10001': {'$lte': 1000}}, {'B/10002': {'$gte': 400}}, {'B/10002': {'$lte': 1000}}]}}]

}

headers = {'content-type': 'application/json'}

response = requests.post(url, json =data,headers=headers)

data0=response.text
#print(type(response.text))
print('response')
print(data0)
data=[
    {
        'a':4,
        'b':"[3,2]"
    },
    {
        'a':46,
        'b':"[4,2]"
    }


]

mypanda = pandas.DataFrame(json.loads(response.text))
mypanda = mypanda.astype({'C/10001':'float64','B/10002':'float64'})

newpanda=mypanda.sort_values(by=['C/10001'])
print('main data:')
print(newpanda)
print('------------')

start = 0
r=100
range_end =start + r
end = 700

a=2
taken = 0
summation =0
max_sum = 1500
for index, row in newpanda.iterrows():
    if summation >= max_sum or row['C/10001']>end:
        newpanda.drop(index, inplace=True)
        continue

    if start < row['C/10001'] and row['C/10001'] < range_end:
        if taken >=a:
            newpanda.drop(index, inplace=True)
        else:
            if summation+row['C/10001']< max_sum:
                taken = taken+1
                summation=summation+row['C/10001']
            else:
                newpanda.drop(index, inplace=True)
    else:
        while True:
            taken = 0
            start = range_end
            range_end = start + r
            if start < row['C/10001'] and row['C/10001'] < range_end:
                if summation+row['C/10001']< max_sum:
                    taken = taken+1
                    summation=summation+row['C/10001']
                else:
                    newpanda.drop(index, inplace=True)
                break
            if range_end > end:
                newpanda.drop(index, inplace=True)
                break


print('stage 1:d=1, start=0, end =1000, r=100, a=2')
print(newpanda)
print("---------------")

start = 0
r=100
range_end =start + r
end = 1000

a=1
taken = 0
summation =0
max_sum =1000
newpanda=newpanda.sort_values(by=['B/10002'])

for index, row in newpanda.iterrows():
    if summation >= max_sum or row['B/10002']>end:
        newpanda.drop(index, inplace=True)
        continue

    if start < row['B/10002'] and row['B/10002'] < range_end:
        #print(start,end,row['C/10001'])

        if taken >=a:
            #print('drops',row['C/10001'])
            newpanda.drop(index, inplace=True)
        else:
            #print('taken', row['C/10001'])

            if summation+row['B/10002']< max_sum:
                taken = taken+1
                summation=summation+row['B/10002']
                #print(summation)
            else:
                newpanda.drop(index, inplace=True)

            continue
    else:

        #taken = 0
        #start = end
        #end = start +r

        while True:
            #print('a:', start,range_end,row['C/10001'])
            taken = 0
            start = range_end
            range_end = start + r
            if start < row['B/10002'] and row['B/10002'] < range_end:
                #print(start,end,row['C/10001'])

                #print('taken', row['C/10001'] )

                if summation+row['B/10002']< max_sum:
                    taken = taken+1

                    summation=summation+row['B/10002']
                    #print(summation)
                else:
                    newpanda.drop(index, inplace=True)
                break
            if range_end > end:
                break

print('stage 2:d=2, start=0, end =1000, r=100, a=1')
print(newpanda)

newpanda.to_json('temp.json', orient='records', lines=True)
