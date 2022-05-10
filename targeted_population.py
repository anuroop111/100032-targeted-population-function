from get_data_tools import get_data_for_distribution
from normal_distribution import normal_distribution
from poisson_distribution import poisson_distribution


def targeted_population(distribution_input, database_details, time_input, number_of_variable, stage_input_list):
    data, start_dowell_time, end_dowell_time = get_data_for_distribution(time_input,
                                                                         stage_input_list, database_details)
    distribution_results = {}

    if distribution_input['normal'] == 1:
        distribution_results['normal'] = normal_distribution(data, stage_input_list, number_of_variable)

    if distribution_input['poisson'] == 1:
        distribution_results['poisson'] = poisson_distribution(data, start_dowell_time, end_dowell_time,
                                                               stage_input_list, number_of_variable)

    if distribution_input['binomial'] == 1:
        distribution_results['binomial'] = "work in progress"

    if distribution_input['bernoulli'] == 1:
        distribution_results['bernoulli'] = "work in progress"

    return distribution_results
