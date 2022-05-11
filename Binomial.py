#call eventfunctionreport()
import random
test_data = random.sample(range(0,10000), 100)
split_variable = int(input("Input number of variables to split into: "))

split_choice = ""
def binomial(test_sample, N, split_choice):  
           # Function for  success or failure condition
            def condition(list_a, cond):
                            if cond:
                                for k in list_a:
                                    count = sum(cond(elem) for elem in k)
                                    print(str(count)+ " successes")
                            else:
                                count = len(k)
                            return count                   
           
           #Function splitting my data 
            def make_splits(data, SIZE): 
                    for i in range(0, len(data), SIZE):
                        yield data[i:i + SIZE] 
           
           #function for user_choice after choosing to split
            def choice(User_choice, SIZE):  
                    for i in range(len(z)):
                        if len(z[i]) != SIZE:
                            incomplete = (z[i])                        
                            if User_choice == "Eliminate":
                                new_list = z.remove(incomplete)
                                print(z) 
                                print(str(len(z)) + " splits made from elimination")
                                display = input("Pick a choice for operation <, > or =: ")
                                if display == "<":
                                    user_choice_num = int(input("Pick < than: "))
                                    condition(z, cond= lambda x: x <=user_choice_num)
                                    for i in range(len(z)):
                                        for j in range(len(z[i])):
                                            a = z[i][j]
                                            if a <= user_choice_num:
                                                print(str(a) + ' is a success')
                                            else:
                                                print(str(a) + ' is a failure')
                                elif display == ">":
                                    user_choice_num = int(input("Pick > than: "))
                                    condition(z, cond= lambda x: x >=user_choice_num)
                                    for i in range(len(z)):
                                        for j in range(len(z[i])):
                                            a = z[i][j]
                                            if a >= user_choice_num:
                                                print(str(a) + ' is a success')
                                            else:
                                                print(str(a) + ' is a failure')
                                elif display == "=":
                                    user_choice_num = int(input("Pick = to: "))
                                    condition(z, cond= lambda x: x ==user_choice_num)
                                    for i in range(len(z)):
                                        for j in range(len(z[i])):
                                            a = z[i][j]
                                            if a == user_choice_num:
                                                print(str(a) + ' is a success')
                                            else:
                                                print(str(a) + ' is a failure')
                                
                                
                                
                            elif User_choice == "Check Accuracy":
                                E = (float(input("Allowable Error in percentage: "))/100)
                                if len(z[i]) >= (SIZE - (E*SIZE)) and len(z[i]) <= (SIZE + (E*SIZE)):
                                    print(z)
                                    print(str(len(z)) + " splits made by checking accuracy")
                                    
                                    display = input("Pick a choice for operation <, > or =: ")
                                    if display == "<":
                                        user_choice_num = int(input("Pick < than: "))
                                        condition(z, cond= lambda x: x <=user_choice_num)
                                        for i in range(len(z)):
                                            for j in range(len(z[i])):
                                                a = z[i][j]
                                                if a <= user_choice_num:
                                                    print(str(a) + ' is a success')
                                                else:
                                                    print(str(a) + ' is a failure')
                                    elif display == ">":
                                        user_choice_num = int(input("Pick > than: "))
                                        condition(z, cond= lambda x: x >=user_choice_num)
                                        for i in range(len(z)):
                                            for j in range(len(z[i])):
                                                a = z[i][j]
                                                if a >= user_choice_num:
                                                    print(str(a) + ' is a success')
                                                else:
                                                    print(str(a) + ' is a failure')
                                    elif display == "=":
                                        user_choice_num = int(input("Pick = to: "))
                                        condition(z, cond= lambda x: x ==user_choice_num)
                                        for i in range(len(z)):
                                            for j in range(len(z[i])):
                                                a = z[i][j]
                                                if a == user_choice_num:
                                                    print(str(a) + ' is a success')
                                                else:
                                                    print(str(a) + ' is a failure')
                                else:
                                    User_choice == "Eliminate"
                                    new_list = z.remove(incomplete)
                                    print(z) 
                                    print(str(len(z)) + " splits made from elimination")
                                    display = input("Pick a choice for operation <, > or =: ")
                                    if display == "<":
                                        user_choice_num = int(input("Pick < than: "))
                                        condition(z, cond= lambda x: x <=user_choice_num)
                                        for i in range(len(z)):
                                            for j in range(len(z[i])):
                                                a = z[i][j]
                                                if a <= user_choice_num:
                                                    print(str(a) + ' is a success')
                                                else:
                                                    print(str(a) + ' is a failure')
                                    elif display == ">":
                                        user_choice_num = int(input("Pick > than: "))
                                        condition(z, cond= lambda x: x >=user_choice_num)
                                        for i in range(len(z)):
                                            for j in range(len(z[i])):
                                                a = z[i][j]
                                                if a >= user_choice_num:
                                                    print(str(a) + ' is a success')
                                                else:
                                                    print(str(a) + ' is a failure')
                                    elif display == "=":
                                        user_choice_num = int(input("Pick = to: "))
                                        condition(z, cond= lambda x: x ==user_choice_num)
                                        for i in range(len(z)):
                                            for j in range(len(z[i])):
                                                a = z[i][j]
                                                if a == user_choice_num:
                                                    print(str(a) + ' is a success')
                                                else:
                                                    print(str(a) + ' is a failure')
                   
                    
            
                    
            splitted_data = make_splits(test_sample, N)
            precise_split = list(splitted_data)
            
            if len(precise_split[0]) == len(precise_split[-1]):
                print(precise_split)
                print(str(len(precise_split)) + " splits made")
                display = input("Pick a choice for operation <, > or =: ")
                if display == "<":
                    user_choice_num = int(input("Pick < than: "))
                    condition(precise_split, cond= lambda x: x <=user_choice_num)
                    for i in range(len(precise_split)):
                        for j in range(len(precise_split[i])):
                            a = precise_split[i][j]
                            if a <= user_choice_num:
                                print(str(a) + ' is a success')
                            else:
                                print(str(a) + ' is a failure')
                elif display == ">":
                    user_choice_num = int(input("Pick > than: "))
                    condition(precise_split, cond= lambda x: x >=user_choice_num)
                    for i in range(len(precise_split)):
                        for j in range(len(precise_split[i])):
                            a = precise_split[i][j]
                            if a >= user_choice_num:
                                print(str(a) + ' is a success')
                            else:
                                print(str(a) + ' is a failure')
                elif display == "=":
                    user_choice_num = int(input("Pick = to: "))
                    condition(precise_split, cond= lambda x: x ==user_choice_num)
                    for i in range(len(precise_split)):
                        for j in range(len(precise_split[i])):
                            a = precise_split[i][j]
                            if a == user_choice_num:
                                print(str(a) + ' is a success')
                            else:
                                print(str(a) + ' is a failure')
            
            else:
                split_choice = input("calculated or simple split: ")
                if split_choice == "simple": 
                    size = N 
                    y = make_splits(test_sample, size)
                    split_decision = input("Eliminate or Check Accuracy: ")
                    z = list(y)
                    print(z)
                    print(str(len(z)) + " splits made")
                    choice(User_choice=split_decision, SIZE=N )       
            
                elif split_choice == "calculated":
                    y = len(test_sample)
                    e = float(input("input marginal error: " ))
                    n = y / (1 + (y*(e**2)))  #slovens formula for calculating n
                    size = round(n)
                    y = make_splits(test_sample, size)
                    z = list(y)
                    print(z)
                    split_decision = input("Eliminate or Check Accuracy: ")
                    choice(User_choice=split_decision, SIZE=size )
            

binomial(test_sample=test_data, N = split_variable, split_choice= split_choice)