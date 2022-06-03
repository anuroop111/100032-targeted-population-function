from samplingrule.samplingrule import dowellsamplingrule


def dowelldistribution(x):
    split = getSplit()

    if x == 0:
        print("normal distribution selected")
    elif x == 1:
        print("poisson distribution is selected")
    elif x == 3:
        selected = selectDistribution()
        if selected == 2:
            print("poisson distribution is selected")

            print("Specify the split for which data to be selected")
            split = getSplit()
            dowellsamplingrule()
            ##Depending on the selected split,fetch the  data from the database within the time limt				

    # return Function output(distribution,split,adequacy of data,required data)


def getSplit():
    return int(input())


def selectDistribution():
    print("Select a dirstibution")

    print("1. Normal distribution")
    print("2. Poission distribution")

    selected = float(input())
    return selected
