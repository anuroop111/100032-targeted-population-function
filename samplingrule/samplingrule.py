def dowellsamplingrule(n,k):
    #n= sample dataframe_size
    #k=  number of category


    if n>k*5:
        return True, 'sample size is adequate'
    else:
        print('sample size is not adequate')
        return False,'sample size is not adequate'

     # elif h==3:
     #    #multi variant search
     #    if n>=10*k:
     #        return True,n
     #    elif n<10*k:
     #        print('sample size is not adequate as per this condition')
     #        return False,n
