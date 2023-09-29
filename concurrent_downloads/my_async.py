from collections import defaultdict

import aiohttp
import asyncio
from concurrent_downloads.data.sites import sites

from timer import timer

TASKS_NUM = 10


class MyTask:
    def __init__(self):
        self.text = None
        self.waiter_task = None
        self.downloads = 0


data = defaultdict(MyTask)

results = {}


async def waiter(event):
    await event.wait()


async def download(url, n):
    print("tasks num:" + str(len(asyncio.all_tasks())))
    async with aiohttp.ClientSession() as session:
        event = asyncio.Event()
        if url not in data:
            data[url].waiter_task = asyncio.create_task(waiter(event))
            async with session.get(url) as response:
                data[url].downloads += 1
                data[url].text = await response.text()
                event.set()
        elif not data[url].text:
            await data[url].waiter_task
        results[(url, n)] = data[url].text[n]



async def main(sites_num):
    await asyncio.gather(*(download(url, n) for url, n in sites[:sites_num]))
    assert set(elem.downloads for elem in data.values()) == {1}
    return results


@timer
def my_async_main(sites_num):
    print("sites num: " + str(sites_num))
    return asyncio.run(main(sites_num))
