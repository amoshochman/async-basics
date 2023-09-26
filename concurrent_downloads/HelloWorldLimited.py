import asyncio


async def count():
    print("tasks num:" + str(len(asyncio.all_tasks())))
    print("One")
    await asyncio.sleep(1)
    print("Two")


async def limit_concurrency(tasks, limit):
    pending = set()
    for task in tasks:
        pending.add(asyncio.ensure_future(task))
        if len(pending) >= limit:
            done, pending = await asyncio.wait(
                pending, return_when=asyncio.FIRST_COMPLETED
            )

    await asyncio.wait(pending)


async def main():
    tasks = [count(), count(), count()]
    await limit_concurrency(tasks, 2)  # Limit the number of tasks to 2


if __name__ == "__main__":
    import time

    s = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
