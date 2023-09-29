import asyncio

global_counter = 0

async def count():
    print("tasks num:" + str(len(asyncio.all_tasks())))
    print("One")
    await asyncio.sleep(5)
    global global_counter
    global_counter += 1
    await asyncio.sleep(global_counter * 2)
    # if global_counter in [1,2,3]:
    #     await asyncio.sleep(10)
    # else:
    #    await asyncio.sleep(1)
    print("Two")


async def main():
    tasks = [count() for i in range(6)]
    pending = set()
    for task in tasks:
        pending.add(asyncio.ensure_future(task))
        if len(pending) >= 3:
            done, pending = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)
    if pending:
        await asyncio.wait(pending)


if __name__ == "__main__":
    import time

    s = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
