# concurrent-downloads

Asynchronously downloads webpages while ensuring no one is downloaded twice. </br>
Instructions: run python my_async.py

Takeaways:

- It can be achieved through threading but asyncio gives better performance often, and we basically don't need to deal
with lockings, as there is only one thread.
- When we print the number of running tasks, (i.e. length of asyncio.all_tasks()), we can see that the number
gets to be ~ twice the value of TASKS_NUM. The reason for that is session.get(url), which creates a task.
