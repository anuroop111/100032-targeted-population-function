import json

import requests

import time


def bernoulli_distribution(error_size, test_number, selection_start_point, items_to_be_selected, data):
    # shuffle data by passing the data from the db through the API
    start_time = time.time()
    po = selection_start_point
    n = items_to_be_selected
    data_items = []
    for i in range(len(data)):
        data_items.append(i + 1)

    data_items_s = [str(i) for i in data_items]

    items = " ".join(data_items_s)
    items_list = items.replace(" ", ",")
    params = {
        "deck": len(data),  # enter any number more than 100
        "error": error_size,  # any float number
        "test_num": test_number,  # integer number
        "deck_items": items_list
    }
    url = "http://100072.pythonanywhere.com/api"
    post_response = requests.post(url, params)
    data = post_response.text
    parse_json = json.loads(data)
    # use the shuffled original data
    series = parse_json['OptimumSeries']
    data_spr = series.replace('\n', ',')
    db_data = data_spr.split(',')
    db_data.pop()

    deck_data = list(map(int, db_data))

    def Convert(lst):
        res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
        return res_dct

    dict_data = Convert(deck_data)
    shuffledList = list(dict_data.values())

    # get the maximum and the minimum value of the data provided
    max_value = (max(shuffledList))
    min_value = (min(shuffledList))

    # ask the user to enter the position where the selection is supposed to start
    # po = input("Start Point:\n")
    # Check whether the value entered by the user lies within the range of the available items

    if min_value <= po < max_value:
        # prompt the user to enter the number of items to be picked from the starting point of selection
        # get the count of the number of the items between the selection and the maximum value item
        items_count = 0
        for i in shuffledList:
            if po <= i <= max_value:
                items_count += 1
        # get the items from the specified index until the number of items required is met
        if int(n) <= items_count:
            data_items = shuffledList[int(po): int(po) + int(n)]
            selected_data_items = [data[i] for i in data_items]
        else:
            print("Beyond available values")
            return "Enter value within the available values"

    else:
        print("The value entered is not in range of the available data, Please enter a different value")
        return "Enter Value within the range of the data"

    end_time = time.time()

    process_time = end_time - start_time

    return "StartingPosition:", po, "NumberOfItemsToBeSelected:", n, "ItemsSelected:", selected_data_items, "RunningTime", process_time
