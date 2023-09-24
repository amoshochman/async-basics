# async-basics

## concurrent_downloads


Asynchronously downloading webpages while ensuring no one is downloaded twice. </br>
Instructions: run main.py - optional parameter: n, where n is the number of sites to download.

Currently we're achieving the limit on the number of downloads through the creation of a new task:

`data[url].waiter_task = asyncio.create_task(waiter(event))` 

An issue with this is that it's hard to verify the total number of tasks actually working.
Another option would be to make the task enter a loop where for every iteration, it sleeps for some time and then it checks whether the needed task finished already.



