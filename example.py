

"""
number of variable should the equal to the length of stage_input_list
here,
'd' is datatype
'start_point' is start point
'm_or_A_selction' can be 'maximum_point'/'population_average'
'error' is error percent allowed,
'r' is range
'a' number of selected input  in each range

when d=5, only need to specify start point and end point
when d=7, need to specify the below
'p_r_selection' can be 'proportion' or 'random_generation'
'proportion' proportion value
'first_position' is first position
'last_position' is last_position, note: need to specify but has no effect now

The function will return,
{
    'data':"dictionary of response data",
    'isError': True
    'sampling_status':"string about sampling rule function output"
}

For more details understanding look onto the example below

"""

#import the targeted topulation function
from targeted_population_api.targeted_population import targeted_population


#name of details
database_name='mongodb'
database='Bangalore'
collection='day001'

#number of stage
n_stage = 3
#number of variables
number_of_variables = 1
#stage input list
stage_input_list = [
    {   'd':5, ##data type of first stage is always 5
        'start_point': '2021/01/08',
        'end_point': '2021/01/25',
    },
    {
        'd':1,
        'm_or_A_selction':'maximum_point',
        'm_or_A_value': 700,
        'error':20,
        'r':100,
        'start_point': 0,
        'end_point': 700,
        'a': 2,
     },
    {
        'd':7,
        'p_r_selection':'proportion',
        'proportion':20,
        'first_position':1,
        'last_position':2,

    }
]

#call the function
data=targeted_population(database_name, n_stage, number_of_variables, stage_input_list, collection, database)
print(data)
