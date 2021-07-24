def dowellsamplingrule():
    #Define sample size as variable "n"	
    n=dowellsamplesize()					

	#Define number of categories as variable "k"								
    #Input from frontend programmer or user
    k=input_number_of_category()
    #Define number of variables as variable "h"
    h=number_of_variable()

    if h<=0:
        print("there should be at least one variable")
    #if h=1,then univariate research	
    #if h=2,then bivariate	
    elif h==1 or h==2:
       if k>=1:
            if n>k*30:
                return True, n
            else:
                print('sample size is not adequate')
                return False,n
           
       else:
            print('sample size is not adequate')
            return False,n
    elif h==3:
        #multi variant search
        if n>=10*k:
            return True,n
        elif n<10*k:
            print('sample size is not adequate as per this condition')
            return False,n

    
        
        
        




def dowellsamplesize():
    return int(input())


def input_number_of_category():

    return int(input())

def number_of_variable():
    return int(input())


