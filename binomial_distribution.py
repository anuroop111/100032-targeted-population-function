# call eventfunctionreport()
# test_data = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200,
#              210, 220, 230, 240, 250, 260, 270, 280, 290, 300, 310, 320, 330, 340]

# split_variable = int(input("Input number of variables to split into: "))
#
# split_choice = ""


def binomial_distribution(test_sample, N, split_choice):
    def condition(list_a, term, cond):  # Function for  success or failure condition
        for i in range(len(list_a)):
            for j in range(len(list_a[i])):
                a = list_a[i][j]
                if a >= term:
                    print(str(a) + ' is a success')
                else:
                    print(str(a) + ' is a failure')
        if cond:
            for k in list_a:
                count = sum(cond(elem) for elem in k)
                print(str(count) + " successes")
        else:
            count = len(k)
        return count

    def make_splits(data, SIZE):  # Function splitting my data
        for i in range(0, len(data), SIZE):
            yield data[i:i + SIZE]

    def choice(User_choice, SIZE):  # function for user_choice after choosing to split
        for i in range(len(z)):
            if len(z[i]) != SIZE:
                incomplete = (z[i])
                if User_choice == "Eliminate":
                    new_list = z.remove(incomplete)
                    print(z)
                    print(str(len(z)) + " splits made from elimination")
                    condition(z, term=150, cond=lambda x: x >= 150)

                elif User_choice == "Check Accuracy":
                    E = float(input("Allowable Error: "))
                    '''print(SIZE)
                    print(len(z[i]))'''
                    if len(z[i]) > (SIZE - E) and len(z[i]) < (SIZE + E):
                        print(z)
                        print(str(len(z)) + " splits made by checking accuracy")
                        condition(z, term=150, cond=lambda x: x >= 150)

                    else:
                        print("Doesn't meet the requirement, exiting now")

    splitted_data = make_splits(test_sample, N)
    precise_split = list(splitted_data)
    if len(precise_split[0]) == len(precise_split[-1]):
        print(precise_split)
        print(str(len(precise_split)) + " splits made")
        condition(precise_split, term=150, cond=lambda x: x >= 150)
    else:
        split_choice = input("calculated or simple split: ")
        if split_choice == "simple":
            size = N
            y = make_splits(test_sample, size)
            split_decision = input("Eliminate or Check Accuracy: ")
            z = list(y)
            print(z)
            print(str(len(z)) + " splits made")
            choice(User_choice=split_decision, SIZE=N)

        elif split_choice == "calculated":
            y = len(test_sample)
            e = float(input("input marginal error: "))
            n = y / (1 + (y * (e ** 2)))  # slovens formula for calculating n
            size = round(n)
            y = make_splits(test_sample, size)
            z = list(y)
            print(z)
            split_decision = input("Eliminate or Check Accuracy: ")
            choice(User_choice=split_decision, SIZE=size)


# binomial_distribution(test_sample=test_data, N=split_variable, split_choice=split_choice)