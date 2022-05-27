from dowell_time_utils import dowell_time, time_stump_from_days
from samplingrule.samplingrule import dowellsamplingrule


def poisson_distribution(data, start_dowell_time, end_dowell_time, split, stage_inputs, fields, number_of_variable):
    if not fields:
        return_data = {
            "is_error": True,
            "error_text": "The fields is empty",
        }
        return return_data

    if not data:
        return_data = {
            "is_error": True,
            "error_text": "There is no matching data into that date range",
        }
        return return_data

    split_in_dowell_value = get_dowell_time_value_of_split(split)
    splatted_data = split_data(data, start_dowell_time, end_dowell_time, split_in_dowell_value)

    result = splatted_data
    try:
        for field in fields:
            for stage in stage_inputs:
                m_or_a_selection = stage['m_or_A_selction']
                m_or_a_value = stage['m_or_A_value']
                if stage['data_type'] == 0:
                    break
                if stage['data_type'] == '7':
                    pass
                if m_or_a_selection == 'maximum_point':
                    result = generate_split_for_data_type_by_max_sum(m_or_a_value, splatted_data, field)
                else:
                    result = generate_split_for_data_type_by_population_average(m_or_a_value, splatted_data, field,
                                                                                stage['error'])

        n = len(result)

        if number_of_variable == -1:
            status = "Not expected"
            is_acceptable = False
        else:
            is_acceptable, sample_size, status = dowellsamplingrule(n, 1, number_of_variable)

        return_data = {
            "is_error": False,
            "data": result,
            "sampling_status": is_acceptable,
            "sampling_status_text": status,
        }

    except Exception as e:
        return_data = {
            "is_error": True,
            "error_text": str(e),
        }

    return return_data


def generate_split_for_data_type_by_population_average(population_average, splatted_data, column_name, error_percent):
    result_list_for_stage = []
    population_average_min = population_average - population_average * error_percent / 100
    population_average_max = population_average + population_average * error_percent / 100
    for single_split_data in splatted_data:
        new_sub_split_for_data_type = []

        list_up_to_pa = []
        summation = 0
        taken = 0
        for d in single_split_data:
            expected_average = (summation + d[column_name]) / (taken + 1)
            if expected_average <= population_average_min:
                summation = summation + d[column_name]
                taken = taken + 1
                list_up_to_pa.append(d)
            elif population_average_min <= expected_average <= population_average_max:
                summation = summation + d[column_name]
                taken = taken + 1
                list_up_to_pa.append(d)
            else:
                if population_average_min <= summation / taken <= population_average_max:
                    new_sub_split_for_data_type.append(list_up_to_pa)
                    list_up_to_pa = []
                    summation = d[column_name]
                    list_up_to_pa.append(d)
        if new_sub_split_for_data_type:
            result_list_for_stage = result_list_for_stage + new_sub_split_for_data_type

    return result_list_for_stage


def generate_split_for_data_type_by_max_sum(max_sum, splatted_data, column_name):
    result_list_for_stage = []
    for single_split_data in splatted_data:
        new_sub_split_for_data_type = []

        list_up_to_max_sum = []
        summation = 0
        for d in single_split_data:
            if d[column_name] > max_sum:
                print("error violated rules")

            if summation + d[column_name] <= max_sum:
                summation = summation + d[column_name]
                list_up_to_max_sum.append(d)
            else:
                new_sub_split_for_data_type.append(list_up_to_max_sum)
                list_up_to_max_sum = []
                summation = d[column_name]
                list_up_to_max_sum.append(d)
        if new_sub_split_for_data_type:
            result_list_for_stage = result_list_for_stage + new_sub_split_for_data_type

    return result_list_for_stage


def split_data(data, start_point, end_point, split):
    split_results = []

    for i in range(start_point, end_point, split):
        range_start_point = i
        range_end_point = i + end_point
        data_in_range = []
        for d in data:
            if range_start_point <= dowell_time(d['Date']) < range_end_point:
                data_in_range.append(d)
        if data_in_range:
            split_results.append(data_in_range)

    return split_results


def get_dowell_time_value_of_split(split):
    days = 0
    if split == 'week':
        days = 7

    return time_stump_from_days(days)
