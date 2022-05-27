import random
from samplingrule.samplingrule import dowellsamplingrule


def normal_distribution(data, stage_input_list, fields, number_of_variable):
    if not fields:
        result = {
            "is_error": True,
            "error_text": "The fields is empty",
        }
        return result

    if not data:
        result = {
            "is_error": True,
            "error_text": "There is no matching data into that date range",
        }
        return result

    df = data
    try:
        for data_key in fields:
            # df = df.astype({'C/10001': 'float64', 'B/10002': 'float64', 'C/10003': 'float64', 'D/10004': 'float64'})
            # filter for all stages
            for stage in stage_input_list:
                d = stage['data_type']

                if d == 0:
                    break
                if d == 7:
                    df = filter_lot_database(df, stage, data_key)
                    if not df:
                        raise Exception('selection is not matching the required lot size')
                    continue

                if stage['m_or_A_selction'] == 'population_average':
                    df = filter_df_population_average(df, data_key, stage)
                else:
                    df = filter_df_max_point(df, data_key, stage)
                if not df:
                    raise Exception("not matched for datatype " + str(data_key))

        n = len(df)

        if number_of_variable == -1:
            status = "Not expected"
            is_acceptable = False
        else:
            is_acceptable, sample_size, status = dowellsamplingrule(n, 1, number_of_variable)

        result = {
            "is_error": False,
            "data": df,
            "sampling_status": is_acceptable,
            "sampling_status_text": status,
        }

    except Exception as e:
        result = {
            "is_error": True,
            "error_text": str(e),
        }

    return result


def filter_lot_database(df, stage, data_key):
    proportion_selection = stage['p_r_selection']
    first_position = stage['first_position']
    last_position = stage['last_position']
    dataframe_size = len(df)

    if proportion_selection == "proportion":
        lot_size = int(dataframe_size * stage['proportion'] / 100)
        if first_position + lot_size - 1 <= dataframe_size:
            df = df[first_position - 1:lot_size]
            return df
        else:
            return []
    else:

        random_lot_size = random.randint(0, dataframe_size)
        if first_position + random_lot_size - 1 > dataframe_size:
            return []
        else:
            df = df[first_position - 1:random_lot_size]
            return df


def filter_df_population_average(df, column_name, stage):
    start = float(stage['start_point'])
    r = stage['r']
    range_end = start + r
    end = float(stage['end_point'])
    population_average = stage['m_or_A_value']
    a = stage['a']
    error_percent = stage['error']
    population_average_min = population_average - population_average * error_percent / 100
    population_average_max = population_average + population_average * error_percent / 100
    taken = 0

    sum_of_taken_numbers = 0
    taken_number_count = 0
    result = []

    for index in range(0, len(df)):
        try:
            current_mean = sum_of_taken_numbers / taken_number_count
        except Exception:
            current_mean = 0

        if current_mean == population_average or (
                current_mean >= population_average_max or df[index][column_name] > end):
            break

        if start < df[index][column_name] < range_end:
            if taken >= a:
                continue
            else:
                expected_sum_of_taken_numbers = sum_of_taken_numbers + df[index][column_name]
                expected_taken_number_count = taken_number_count + 1
                expected_mean = expected_sum_of_taken_numbers / expected_taken_number_count

                if expected_mean <= population_average_max:
                    taken = taken + 1
                    taken_number_count = expected_taken_number_count
                    sum_of_taken_numbers = expected_sum_of_taken_numbers
                    result.append(df[index])
        else:
            while True:
                taken = 0
                start = range_end
                range_end = start + r

                if start < df[index][column_name] < range_end:
                    expected_sum_of_taken_numbers = sum_of_taken_numbers + df[index][column_name]
                    expected_taken_number_count = taken_number_count + 1
                    expected_mean = expected_sum_of_taken_numbers / expected_taken_number_count

                    if expected_mean <= population_average_max:
                        taken = taken + 1
                        taken_number_count = expected_taken_number_count
                        sum_of_taken_numbers = expected_sum_of_taken_numbers
                        result.append(df[index])
                    break
                if range_end > end:
                    break

    try:
        current_mean = sum_of_taken_numbers / taken_number_count
    except:
        current_mean = 0

    if population_average_min <= current_mean <= population_average_max:
        return result
    else:
        return []


def filter_df_max_point(df, column_name, stage):
    newpanda = df.sort_values(by=[column_name])
    start = float(stage['start_point'])
    r = stage['r']
    range_end = start + r
    end = float(stage['end_point'])
    error_percent = stage['error']
    max_sum = stage['m_or_A_value']

    max_sum_min = max_sum - max_sum * error_percent / 100
    max_sum_max = max_sum + max_sum * error_percent / 100
    a = stage['a']

    taken = 0
    summation = 0

    result = []

    for index in range(0, len(df)):
        if summation >= max_sum_max or df[index][column_name] > end:
            continue

        if start < df[index][column_name] < range_end:
            if taken >= a:
                continue
            else:
                if summation + df[index][column_name] < max_sum_max:
                    taken = taken + 1
                    summation = summation + df[index][column_name]
                    result.append(df[index][column_name])
                else:
                    continue
        else:
            while True:
                taken = 0
                start = range_end
                range_end = start + r
                if start < df[index][column_name] < range_end:
                    if summation + df[index][column_name] < max_sum_max:
                        taken = taken + 1
                        summation = summation + df[index][column_name]
                        result.append(df[index][column_name])
                    else:
                        continue
                    break
                if range_end > end:
                    break

    if max_sum_min <= summation <= max_sum_max:
        return result
    else:
        return []
