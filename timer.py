import time


def timer(func):
    def inner(*args):
        start_time = time.time();
        retval = func(*args)
        print(func.__name__ + ": " + str(round(time.time() - start_time, 2)) + " secs")
        return retval

    return inner
