import json

import requests

import time


def bernoulli_distribution():
    # shuffle data by passing the data from the db through the API
    start_time = time.time()

    url = "http://100072.pythonanywhere.com/api"

    params = {
        "deck": 100,  # user defined value can be change but should be >=100
        "error": 1.67,  # value can change but should be a floating number
        "test_num": 3  # this is the number of times the data given is shuffled
    }
    get_response = requests.get(url, params)
    data = get_response.text
    parse_json = json.loads(data)
    # use the shuffled original data
    series = parse_json['SeriesDataframe']
    data_spr = series.replace('\n', ',')
    db_data = data_spr.split(',')
    # print(db_data)

    # get the maximum and the minimum value of the data provided
    max_value = (max(db_data))
    min_value = (min(db_data))

    # ask the user to enter the position where the selection is supposed to start
    po = input("Start Point:\n")

    # Check whether the value entered by the user lies within the range of the available items
    if min_value <= po < max_value:
        # prompt the user to enter the number of items to be picked from the starting point of selection
        n = input('Items to be selected: \n')
        # get the count of the number of the items between the selection and the maximum value item
        items_count = 0
        for i in db_data:
            if po <= i <= max_value:
                items_count += 1
        # get the items from the specified index until the number of items required is met
        if int(n) <= items_count:
            data_items = db_data[int(po): int(po) + int(n)]
            print(data_items)
        else:
            print("Beyond available values")

    else:
        print("The value entered is not in range of the available data, Please enter a different value")

    end_time = time.time()

    process_time = end_time - start_time

    return "Selection Start Point:" + po, "Number of Selections:" + n, data_items, process_time

# bernoulli_distribution()
