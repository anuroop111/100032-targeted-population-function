# 100032-targeted-population-function

## Full examples of calling the api
```python
import json
import requests

url = 'http://100032.pythonanywhere.com/api/targeted_population/'

database_details = {
    'database_name': 'mongodb',
    'collection': 'day001',
    'database': 'Bangalore',
    'fields':['C/10001']
}


# number of variables for sampling rule
number_of_variables = 1

time_input = {
    'column_name': 'Date',
    'period': 'life_time',
    'start_point': '2021/01/08',
    'end_point': '2021/01/25',
    'split': 'week'
}

stage_input_list = [
]

distribution_input={
    'normal': 1,
    'poisson':0,
    'binomial':0,
    'bernoulli':1
    
}

request_data={
    'database_details': database_details,
    'distribution_input': distribution_input,
    'number_of_variable':number_of_variables,
    'stages':stage_input_list,
    'time_input':time_input,
}

headers = {'content-type': 'application/json'}

response = requests.post(url, json=request_data,headers=headers)

print(response.text)
```
### What are the API request data means
Use when developing in local machines
```shell
url = 'http://127.0.0.1:5000/api/targeted_population/'
```

```python
database_details = {
    'database_name': 'mongodb',
    'collection': 'day001',
    'database': 'Bangalore',
    'fields':['C/10001']
}
```
The fields are those fields on which the distribution logic will be applied.

```python
time_input = {
    'column_name': 'Date',
    'split':'week'
    'period': 'life_time',
    'start_point': '2021/01/08',
    'end_point': '2021/01/25',
}

```
#### For time input
Period can be 'custom' or 'last_1_day' or 'last_30_days' or 'last_90_days' or 'last_180_days' or 'last_1_year' or 'life_time'
if custom is given then need to specify start_point and end_point

'split' value is required for poisson distribution.
Split value can be 'week', 'hour', 'day', 'month',

```python
stage_input_list = [

]
```
#### statge_input_list is a list of stages
#### For  Norml distribution a stage can have
```python
    {
        'd': 1,
        'm_or_A_selction': 'population_average',
        'm_or_A_value': 300,
        'error': 10,
        'r': 100,
        'start_point': 0,
        'end_point': 700,
        'a': 2,
    },
```
* datatype can be 0 to 7.
* 'm_or_A_selction' can be 'maximum_point' or 'population_average'
* 'm_or_A_value' is value of the maximum_point' or 'population_average'
*  error is the error allowed in percentage
*  r is range
*  start_point is the starting value of that stage
*  end_point is the maximum value.
*  a is the number of item that can be taken in a range

```python
distribution_input={
    'normal': 1,
    'poisson':0,
    'binomial':0,
    'bernoulli':1
    
}
```
Give 1 if expecting the output for the respective distribution
Give 0 if not expecting output for that distribution

## Output of the api
###Example output
```python
{
   "normal":{
      "is_error":false,
      "data":[
         {
            "_id":"61432d8cb65e9b5c90a52aba",
            "Date":"2021-01-15T18:30:00",
            "C/10001":142,
            "B/10002":417,
            "C/10003":576,
            "D/10004":510,
            "Event Array":"[11,10blr000160505661e0b9b354e134006e]",
            "Process_id":1234,
            "eventId":"FB1010000000016413653685818675"
         },
         {
            "_id":"61432d8cb65e9b5c90a52ab5",
            "Date":"2021-01-10T18:30:00",
            "C/10001":105,
            "B/10002":168,
            "C/10003":247,
            "D/10004":79,
            "Event Array":"[6,10blr000160505661e0b9b354e134006e]",
            "Process_id":1234,
            "eventId":"FB1010000000016413653685818675"
         },
         {
            "_id":"61432d8cb65e9b5c90a52ab8",
            "Date":"2021-01-13T18:30:00",
            "C/10001":449,
            "B/10002":43,
            "C/10003":225,
            "D/10004":774,
            "Event Array":"[9,10blr000160505661e0b9b354e134006e]",
            "Process_id":1234,
            "eventId":"FB1010000000016413653685818675"
         },
         {
            "_id":"61432d8cb65e9b5c90a52abb",
            "Date":"2021-01-16T18:30:00",
            "C/10001":429,
            "B/10002":424,
            "C/10003":301,
            "D/10004":730,
            "Event Array":"[12,10blr000160505661e0b9b354e134006e]",
            "Process_id":1234,
            "eventId":"FB1010000000016413653685818675"
         }
      ],
      "sampling_status":false,
      "sampling_status_text":"sample size is not adequate, univariate, 4<=1*10"
   },
   "bernoulli":"work in progress"
}
```
### what is the output data means

