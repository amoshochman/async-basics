# concurrent-downloads

Asynchronously downloading webpages while ensuring no one is downloaded twice. </br>
Instructions: run my_async.py

Notes:

- if printing the total number of running tasks, that is, length of asyncio.all_tasks(), you will see that the number
passes the value of TASKS_NUM. Actually doubles it. The reason for that is session.get(url), which creates a task.