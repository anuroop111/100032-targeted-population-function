# split function
from datetime import datetime
from re import I
import requests


def get_event_id():
    dd = datetime.now()
    time = dd.strftime("%d:%m:%Y,%H:%M:%S")
    url = "https://100003.pythonanywhere.com/event_creation"

    data = {
        "platformcode": "FB",
        "citycode": "101",
        "daycode": "0",
        "dbcode": "pfm",
        "ip_address": "192.168.0.41",
        "login_id": "lav",
        "session_id": "new",
        "processcode": "1",
        "regional_time": time,
        "dowell_time": time,
        "location": "22446576",
        "objectcode": "1",
        "instancecode": "100051",
        "context": "afdafa ",
        "document_id": "3004",
        "rules": "some rules",
        "status": "work",
        "data_type": "learn",
        "purpose_of_usage": "add",
        "colour": "color value",
        "hashtags": "hash tag alue",
        "mentions": "mentions value",
        "emojis": "emojis",

    }

    r = requests.post(url, json=data)
    return r.text

# function to split data according to fields
def make_splits(data_input, SIZE):
    for i in range(0, len(data_input), SIZE):
        yield data_input[i:i + SIZE]

    
#Filters data from database into fields
def data_filter(data, fields,stage_inputs, current_stage):
    """if current_stage == len(stage_inputs):
        return data

    if stage_inputs[current_stage]['data_type'] == 0:
        return data

    if stage_inputs[current_stage]['data_type'] == '7':
        pass"""

    result = []
    for field in data["binomial"]:
        for i in fields:
            if i in fields:
                _id = (field[i])
            result.append({i: _id})
    return result


# Success function
def condition(list_a, cond,field):
    success = []
    if cond:
        for i in field:
            if i in field:
                for k in list_a:
                    try:
                        count = sum(cond(elem[i]) for elem in k)
                        success.append(str(count) + " Successes")
                    except KeyError:
                        continue                   
    else:
        count = len(k)
    return success



# User input for success
def success_condition_logic(data, user_choice, function, field):
    if function is None:
        pass
    else:
        if function == "<":
            return condition(list_a=data,field=field, cond=lambda x: x < user_choice)
        elif function == ">":
            return condition(list_a=data,field=field,cond=lambda x: x > user_choice)
        elif function == "=":
            return condition(list_a=data,field=field,cond=lambda x: x == user_choice)


# Eliminate or Check Accuracy
def split_decision_function(splitted_data, size, split_decision, error, user_choice, function, field):
    for i in range(len(splitted_data)):
        if len(splitted_data[i]) != size:
            incomplete = splitted_data[i]
            if split_decision == "Eliminate":
                splitted_data.remove(incomplete)
                s = success_condition_logic(splitted_data, user_choice=user_choice, function=function, field=field)
                return [splitted_data, s, user_choice]
            elif split_decision == "Check_Accuracy":
                error = float(error)
                if (size - (error * size)) <= len(incomplete) <= (size + (error * size)):
                    s = success_condition_logic(splitted_data, user_choice=user_choice, function=function)
                    return [splitted_data, s, user_choice]
                else:
                    split_decision == "Eliminate"
                    splitted_data.remove(incomplete)
                    s = success_condition_logic(splitted_data, user_choice=user_choice, function=function)
                    return [splitted_data, s, user_choice]
        else:
            if len(splitted_data[-1]) == size:
                s = success_condition_logic(splitted_data, user_choice=user_choice, function=function)
                return [splitted_data, s, user_choice]


def binomial_distribution(datas, number_of_variables, split_choice, error, split_decision, user_choice,stage_input,
                          function, marginal_error, fields):
    event_id = "eventID"
    #{"event_id": get_event_id()}
    binomial = "binomial"
    data = data_filter(data={binomial: datas}, fields=fields, stage_inputs=stage_input, current_stage=0)
    if not fields:
        return_data = {
            "is_error": True,
            "error_text": "The field is empty",
        }
        return return_data

    if not data:
        return_data = {
            "is_error": True,
            "error_text": "There is no matching data into that date range",
        }
        return return_data
    elif split_choice == "simple":
        splitted_data = list(make_splits(data_input=data, SIZE=number_of_variables))
        if split_decision == "Eliminate":
            success = split_decision_function(splitted_data=splitted_data, size=number_of_variables,
                                              split_decision=split_decision, error=0, user_choice=user_choice,
                                              function=function, field=fields)
            return (datas, success, str(len(splitted_data)) + " splits made",event_id)
        elif split_decision == "check_accuracy":
            success = split_decision_function(splitted_data=splitted_data, size=number_of_variables,
                                              split_decision=split_decision, error=error, user_choice=user_choice,
                                              function=function)
            return [datas, success, str(len(splitted_data)) + " splits made",
                    event_id]
    elif split_choice == "calculated":
        data_length = len(data)
        # print(data_length)
        marginal_error = float(marginal_error)
        n = (data_length / (1 + (data_length * (marginal_error ** 2))))  # slovens formula
        calculated_number_of_variables = round(n)
        # print(calculated_number_of_variables)
        splitted_data = list(make_splits(data, calculated_number_of_variables))
        if len(splitted_data[-1]) == len(splitted_data[0]):
            success_count = success_condition_logic(data=splitted_data, user_choice=user_choice, function=function)
            return [datas, splitted_data, user_choice, success_count, str(len(splitted_data)) + " splits made", event_id]
        else:
            if split_decision == "Eliminate":
                return split_decision_function(splitted_data=splitted_data, size=calculated_number_of_variables,
                                               split_decision=split_decision, error=error, user_choice=user_choice,
                                               function=function)
            elif split_decision == "check_accuracy":
                return split_decision_function(splitted_data=splitted_data, size=calculated_number_of_variables,
                                               split_decision=split_decision, error=error, user_choice=user_choice,
                                               function=function)


    else:
        splitted_data = list(make_splits(data, number_of_variables))
        success_count = success_condition_logic(data=splitted_data, user_choice=user_choice, function=function)
        return [datas, data, splitted_data, user_choice, success_count]
