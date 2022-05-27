import time

DOWELL_TIME_EPOCH = 1609459200


def dowell_time_now():
    current_time = time.time()
    dt = current_time - DOWELL_TIME_EPOCH
    return int(dt)


def dowell_time(a_date_time):
    dtime_stamp = a_date_time.timestamp()
    current_time = int(round(dtime_stamp))
    dt = current_time - DOWELL_TIME_EPOCH
    return dt


def time_stump_from_days(days):
    return days * 24 * 60 * 60
