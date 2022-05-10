from datetime import timedelta


def poisson_distribution(data, start_dowell_time, end_dowell_time, stage_inputs, number_of_variable):
    if not data:
        return "not any data within that date range", "Not Success"

    split = stage_inputs[0]['split']
    date_ranges = generate_date_range_list(split, start_dowell_time, end_dowell_time)

    print("split result -----------------")

    split_data = split_by_date_ranges(data, date_ranges)

    for s in split_data:
        print(s)

    print("length::", len(split_data))

    result = []
    for stage in stage_inputs[1:]:
        max_sum = stage['m_or_A_value']
        if stage['d'] == 1:
            column_name = 'C/10001'

        result = result + generate_split_for_data_type(max_sum, split_data, column_name)
        split_data = result
    return result


def generate_split_for_data_type(max_sum, split_data, column_name):
    result_list_for_stage = []
    for single_split_data in split_data:
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

        result_list_for_stage = result_list_for_stage + new_sub_split_for_data_type

    return result_list_for_stage


def generate_date_range_list(split_by, start_date, end_date):
    if split_by == 'day':
        increment_by = timedelta(days=1)
    elif split_by == 'week':
        increment_by = timedelta(days=7)

    i = start_date
    result = []
    while i < end_date:
        result.append((i, i + increment_by))
        i = i + increment_by

    return result


def split_by_date_ranges(data, date_ranges):
    split_results = []

    for range in date_ranges:
        data_in_range = []
        for d in data:
            if range[0] <= d['Date'] < range[1]:
                data_in_range.append(d)

        split_results.append(data_in_range)

    return split_results
