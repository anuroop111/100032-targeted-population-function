# Split function
def make_splits(data_input, SIZE):
    for i in range(0, len(data_input), SIZE):
        yield data_input[i:i + SIZE]

    # Success function


def condition(list_a, cond):
    success = []
    successful_data = []
    if cond:
        for k in list_a:
            count = sum(cond(elem) for elem in k)
            success.append(str(count) + " Successes")
    else:
        count = len(k)
    return success


# User input for success
def success_condition_logic(data, user_choice, function):
    if function == "<":
        return (condition(list_a=data, cond=lambda x: x <= user_choice))
    elif function == ">":
        return condition(list_a=data, cond=lambda x: x >= user_choice)
    elif function == "=":
        return condition(list_a=data, cond=lambda x: x == user_choice)


def split_decision_function(splitted_data, size, split_decision, error, user_choice, function):
    if len(splitted_data) == size:
        pass

    else:
        for i in range(len(splitted_data)):
            if len(splitted_data[i]) != size:
                incomplete = splitted_data[i]
                if split_decision == "Eliminate":
                    splitted_data.remove(incomplete)
                    s = success_condition_logic(splitted_data, user_choice=user_choice, function=function)
                    return [event_id, data, splitted_data, s, function, user_choice]
                elif split_decision == "Check Accuracy":
                    error = float(error)
                    if len(incomplete) >= (size - (error * size)) and len(incomplete) <= (size + (error * size)):
                        s = success_condition_logic(splitted_data, user_choice=user_choice, function=function)
                        return [event_id, data, splitted_data, s, function, user_choice]
                    else:
                        split_decision == "Eliminate"
                        splitted_data.remove(incomplete)
                        s = success_condition_logic(splitted_data, user_choice=user_choice, function=function)
                        return [event_id, data, splitted_data, s, function, user_choice]


def binomial_distribution(event_id, data, number_of_variables, split_choice, error, split_decision, user_choice,
                          function, marginal_error):
    if split_choice == "simple":
        splitted_data = list(make_splits(data, number_of_variables))
        if split_decision == "Eliminate":
            success = split_decision_function(splitted_data=splitted_data, size=number_of_variables,
                                              split_decision=split_decision, error=0, user_choice=user_choice,
                                              function=function)
            return success
        elif split_decision == "Check Accuracy":
            success = split_decision_function(splitted_data=splitted_data, size=number_of_variables,
                                              split_decision=split_decision, error=error, user_choice=user_choice,
                                              function=function)
            return success
        else:
            split_decision_function(splitted_data=splitted_data, size=number_of_variables,
                                    split_decision=split_decision, error=0)
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
            return [event_id, data, splitted_data, function, user_choice, success_count]
        else:
            if split_decision == "Eliminate":
                return split_decision_function(splitted_data=splitted_data, size=calculated_number_of_variables,
                                               split_decision=split_decision, error=error, user_choice=user_choice,
                                               function=function)
            elif split_decision == "Check Accuracy":
                return split_decision_function(splitted_data=splitted_data, size=calculated_number_of_variables,
                                               split_decision=split_decision, error=error, user_choice=user_choice,
                                               function=function)


    else:
        splitted_data = list(make_splits(data, number_of_variables))
        success_count = success_condition_logic(data=splitted_data, user_choice=user_choice, function=function)
        return [event_id, data, splitted_data, function, user_choice, success_count]


import random

data = random.sample(range(0, 10000), 20)
event_id = "event_id"
binomial_distribution(event_id=event_id, data=data, number_of_variables=0, split_choice="calculated", error=0.5,
                      split_decision="Check Accuracy", marginal_error=0.6, user_choice=4000, function="<")
