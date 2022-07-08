from get_data_tools import get_data_for_distribution
from normal_distribution import normal_distribution
from poisson_distribution import poisson_distribution
from binomial_distribution import binomial_distribution
from bernoulli_distribution import bernoulli_distribution


def targeted_population(distribution_input, database_details, time_input, number_of_variable, stage_input_list):
    data, start_dowell_time, end_dowell_time = get_data_for_distribution(time_input, database_details)
    distribution_results = {}
    fields = database_details['fields']
    split = time_input['split']

    """
    don't change the above lines
    ----------------------------------
    example of the function parameter datatype
    ----------------------------------
    distribution_input={
    'normal': 1,
    'poisson':0,
    'binomial':0,
    'bernoulli':0
    }
    -----------------------------------
    time_input = {
    'column_name': 'Date',
    'split': 'week',
    'period': 'last_30_days',
    'start_point': '2021/01/01',
    'end_point': '2022/01/25',
    }
    -------------------------------------
    'fields':['eventId', 'dowell_time']
    -------------------------------------
    number_of_variable is an integer value
    --------------------------------------
    stage_input_list = [
    ]
    --------------------------------------
    distribution_input, database_details, time_input, number_of_variable, stage_input_list
    """

    if distribution_input['normal'] == 1:
        distribution_results['normal'] = normal_distribution(data, stage_input_list, fields, number_of_variable)

    if distribution_input['poisson'] == 1:
        distribution_results['poisson'] = poisson_distribution(data, start_dowell_time, end_dowell_time,
                                                               split, stage_input_list, fields, number_of_variable)

    if distribution_input['binomial'] == 1:
        split_variable = 5
        split_choice = "simple"
        distribution_results['binomial'] = binomial_distribution(data, split_variable, split_choice)

    if distribution_input['bernoulli'] == 1:
        test_number=23
        error=7
        distribution_results['bernoulli'] = bernoulli_distribution(test_number, error)

    return distribution_results
