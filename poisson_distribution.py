from dowell_time_utils import dowell_time, time_stump_from_days
from samplingrule.samplingrule import dowellsamplingrule
from normal_distribution import normal_distribution


def poisson_distribution(data, start_dowell_time, end_dowell_time, split, stage_inputs, fields, number_of_variable,
                         event_id_key_dict):
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
    splatted_data = split_data(data, start_dowell_time, end_dowell_time, split_in_dowell_value, event_id_key_dict)

    # try:
    result = []
    for field in fields:
        single_field_result = poisson_split(splatted_data, stage_inputs, 0, field)
        result.append(single_field_result)

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

    # except Exception as e:
    #     return_data = {
    #         "is_error": True,
    #         "error_text": str(e),
    #     }

    return return_data


def poisson_split(splatted_array, stage_inputs, current_stage, field):
    if current_stage == len(stage_inputs):
        return splatted_array

    m_or_a_selection = stage_inputs[current_stage]['m_or_A_selction']
    m_or_a_value = stage_inputs[current_stage]['m_or_A_value']

    if stage_inputs[current_stage]['data_type'] == 0:
        return splatted_array

    if stage_inputs[current_stage]['data_type'] == '7':
        pass

    result = []
    for array in splatted_array:
        if m_or_a_selection == 'maximum_point':
            new_spatted_array = generate_split_for_data_type_by_max_sum(m_or_a_value, array, field,
                                                                        stage_inputs[current_stage]['error'])
        else:
            new_spatted_array = generate_split_for_data_type_by_population_average(m_or_a_value,
                                                                                   array, field,
                                                                                   stage_inputs[current_stage]['error'])
        r = poisson_split(new_spatted_array, stage_inputs, current_stage + 1, field)
        if r:
            result.append(r)

    print("result len ", len(result))
    return result


def generate_split_for_data_type_by_population_average(population_average, array, column_name, error_percent):
    result_list_for_stage = []
    population_average_min = population_average - population_average * error_percent / 100
    population_average_max = population_average + population_average * error_percent / 100

    list_up_to_pa = []
    summation = 0
    taken = 0
    for d in array:
        print("list up to pa", list_up_to_pa)
        expected_average = (summation + d[column_name]) / (taken + 1)

        if population_average_min <= expected_average <= population_average_max:
            if list_up_to_pa:
                result_list_for_stage.append(list_up_to_pa)

            summation = 0
            taken = 0
            list_up_to_pa = []

        else:
            summation = summation + d[column_name]
            taken = taken + 1
            list_up_to_pa.append(d)

    return result_list_for_stage


def generate_split_for_data_type_by_max_sum(max_sum, array, column_name, error_percent):
    max_sum_max = max_sum + max_sum * error_percent / 100

    result_list_for_array = []
    summation = 0
    list_up_to_max_sum = []
    for data in array:
        if data[column_name] > max_sum:
            print("error violated rules")
            pass

        if summation + data[column_name] <= max_sum_max:
            summation = summation + data[column_name]
            list_up_to_max_sum.append(data)

        else:
            if list_up_to_max_sum:
                result_list_for_array.append(list_up_to_max_sum)
            list_up_to_max_sum = [data, ]
            summation = data[column_name]

    return result_list_for_array


def split_data(data, start_point, end_point, split, event_id_key_dict):
    split_results = []
    c = 0
    for i in range(start_point, end_point, split):
        c = c + 1

        range_start_point = i
        range_end_point = i + split

        data_in_range = []
        for d in data:
            if range_start_point <= event_id_key_dict[d['eventId']] < range_end_point:
                data_in_range.append(d)

        if data_in_range:
            split_results.append(data_in_range)

    print("split len", len(split_results))
    return split_results


def get_dowell_time_value_of_split(split):
    days = 0
    if split == 'week':
        days = 7
    elif split == 'hour':
        return 3600
    elif split == 'day':
        days = 1
    elif split == 'month':
        days = 30

    return time_stump_from_days(days)
