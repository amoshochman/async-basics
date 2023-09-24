import my_async
import sys

if __name__ == '__main__':
    #my_sync_results = my_sync.my_sync_main()
    my_async_results = my_async.my_async_main(int(sys.argv[1]) if 1 < len(sys.argv) else None)
    #assert my_async_results == my_sync_results
