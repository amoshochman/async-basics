import threading
import time

computation_is_done = False

def my_computation(computation_done_event):
    time.sleep(10)
    computation_done_event.set()

def print_working(computation_done_event):
    while not computation_done_event.is_set():
        print("Still working")
        time.sleep(5)

if __name__ == "__main__":
    computation_done_event = threading.Event()

    computation_thread = threading.Thread(target=my_computation, args=(computation_done_event,))
    print_thread = threading.Thread(target=print_working, args=(computation_done_event,))

    computation_thread.start()
    print_thread.start()

    computation_thread.join()
