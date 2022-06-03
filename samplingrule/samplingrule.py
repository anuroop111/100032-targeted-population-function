def dowellsamplingrule(n, k, number_of_variable):
    # n= sample dataframe_size
    # k=  number of category
    h = number_of_variable
    if number_of_variable <= 0:
        status = "number of variable less than 1"
        return False, n, status
    elif h == 1:
        if n > k * 10:
            status = 'sample size is adequate, univariate, ' + str(n) + '>' + str(k) + '*10'
            return True, n, status
        else:
            status = 'sample size is not adequate, univariate, ' + str(n) + '<=' + str(k) + '*10'
            return False, n, status

    elif h == 2:
        if n > k * 5:
            status = 'sample size is adequate, bivariate, ' + str(n) + '>' + str(k) + '*10'
            return True, n, status
        else:
            status = 'sample size is not adequate,  bivariate, ' + str(n) + '<=' + str(k) + '*10'
            return False, n, status

    else:

        if n >= 5 * k:
            status = 'sample size is adequate, multivariate, ' + str(n) + '>' + str(k) + '*5'
            return True, n, status
        elif n < 5 * k:
            status = 'sample size is not adequate,  multivariate, ' + str(n) + '<=' + str(k) + '*5'
            return False, n, status
