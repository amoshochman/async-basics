import asyncio
import os
import shutil
import time

import aiohttp

from concurrent_downloads.peps import peps

my_dict = {}

results = {}

class MyTask:
    def __init__(self):
        self.text = None
        self.waiter_task = None
        self.downloads = 0


async def download_page(pep_number: int) -> bytes:
    print("tasks num:" + str(len(asyncio.all_tasks())))
    url = f"https://www.python.org/dev/peps/pep-{pep_number}/"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            content = await resp.read()
            return content


async def write_to_file(pep_number: int, content: bytes) -> None:
    print("tasks num:" + str(len(asyncio.all_tasks())))
    filename = f"async_{pep_number}.html"
    with open("data/" + filename, "wb") as pep_file:
        pep_file.write(content)


async def web_scrape_task(pep_number: int, n: int) -> None:
    print("tasks num:" + str(len(asyncio.all_tasks())))
    if pep_number in my_dict:
        await my_dict[pep_number]
        filename = f"async_{pep_number}.html"
        with open("data/" + filename) as pep_file:
            content = pep_file.read()
    else:
        my_dict[pep_number] = asyncio.current_task()
        content = await download_page(pep_number)
        await write_to_file(pep_number, content)
    results[(pep_number, n)] = content[n]

async def gather_with_concurrency(n, *coros):
    semaphore = asyncio.Semaphore(n)
    async def sem_coro(coro):
        async with semaphore:
            return await coro
    return await asyncio.gather(*(sem_coro(c) for c in coros))


async def main() -> None:
    print("tasks num:" + str(len(asyncio.all_tasks())))
    #await gather_with_concurrency(10, *(web_scrape_task(pep, n) for (pep, n) in peps))
    tasks = [web_scrape_task(pep, n) for (pep, n) in peps]
    await gather_with_concurrency(10, *tasks)
    print("after the gather... tasks num:" + str(len(asyncio.all_tasks())))


if __name__ == "__main__":
    s = time.perf_counter()
    shutil.rmtree("data", ignore_errors=True)
    os.mkdir("data")
    asyncio.run(main())

    elapsed = time.perf_counter() - s
    print(f"Execution time: {elapsed:0.2f} seconds.")
