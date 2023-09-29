import multiprocessing
import time

computation_is_done = False


def heavy_computation(computation_done_event):
    result = 0
    for i in range(10 ** 9):
        result += i
    computation_done_event.set()


def constant_print_update(computation_done_event):
    while not computation_done_event.is_set():
        print("Still working")
        time.sleep(5)


def my_test(package, entity):
    print("testing " + str(entity))
    computation_done_event = multiprocessing.Event()
    start = time.time()
    p1 = multiprocessing.Process(target=heavy_computation, args=(computation_done_event,))
    p = multiprocessing.Process(target=constant_print_update, args=(computation_done_event,))
    p1.start()
    p.start()
    p1.join()
    p.join()
    print("time passed: " + str(round(time.time() - start, 2)))


if __name__ == "__main__":
    my_test(multiprocessing, multiprocessing.Process)
