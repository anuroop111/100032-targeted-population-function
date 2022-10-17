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
    print("spilleddddd", len(splatted_data))

    # try:
    result = []
    for field in fields:
        single_field_result = poisson_split(splatted_data, stage_inputs, 0, field, number_of_variable)
        result.append(single_field_result)


    return_data = {
        "is_error": False,
        "data": result,
    }

    # except Exception as e:
    #     return_data = {
    #         "is_error": True,
    #         "error_text": str(e),
    #     }

    return return_data


def poisson_split(splatted_array, stage_inputs, current_stage, field, number_of_variable):
    if current_stage == len(stage_inputs):
        return splatted_array

    m_or_a_selection = stage_inputs[current_stage]['m_or_A_selction']
    m_or_a_value = stage_inputs[current_stage]['m_or_A_value']

    if stage_inputs[current_stage]['data_type'] == 0:
        return splatted_array

    if stage_inputs[current_stage]['data_type'] == '7':
        pass

    print("splatted array len ", len(splatted_array))

    result = []
    for array in splatted_array:
        array_result = normal_distribution(array, stage_inputs, [field], number_of_variable)
        # if m_or_a_selection == 'maximum_point':
        #     new_spatted_array = generate_split_for_data_type_by_max_sum(m_or_a_value, array, field,
        #                                                                 stage_inputs[current_stage]['error'])
        # else:
        #     new_spatted_array = generate_split_for_data_type_by_population_average(m_or_a_value,
        #                                                                            array, field,
        #                                                                            stage_inputs[current_stage]['error'])
        # r = poisson_split(new_spatted_array, stage_inputs, current_stage + 1, field)
        # if r:
        #     result.append(r)

        if not array_result['is_error']:

            r = {
                'data': array_result['data'][0],
                'sampling_rule': array_result['sampling_rule'][field]
            }
            result.append(r)

    return result


def generate_split_for_data_type_by_population_average(population_average, array, column_name, error_percent):
    result_list_for_stage = []
    population_average_min = population_average - population_average * error_percent / 100
    population_average_max = population_average + population_average * error_percent / 100

    list_up_to_pa = []
    summation = 0
    taken = 0
    for d in array:

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

    ranges = []
    result_array = []
    for i in range(start_point, end_point, split):
        range_start_point = i
        range_end_point = i + split
        sr = (range_start_point, range_end_point)
        ranges.append(sr)
        result_array.append([])

    for d in data:
        for i in range(0, len(ranges)):
            if ranges[i][0] <= event_id_key_dict[d['eventId']] < ranges[i][1]:
                result_array[i].append(d)
                break


    return result_array


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
