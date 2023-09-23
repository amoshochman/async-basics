from collections import defaultdict

import aiohttp
import asyncio
from sites import sites
import time


class MyTask:
    def __init__(self):
        self.text = None
        self.waiter_task = None
        self.downloads = 0


saving_dict = defaultdict(MyTask)


async def waiter(event):
    await event.wait()


async def download(url, n):
    async with aiohttp.ClientSession() as session:
        event = asyncio.Event()
        if url in saving_dict:
            await saving_dict[url].waiter_task
        else:
            saving_dict[url].waiter_task = asyncio.create_task(waiter(event))
            async with session.get(url) as response:
                html = await response.text()
                saving_dict[url].downloads += 1
                saving_dict[url].text = html
                event.set()
        print("The requested char is " + saving_dict[url].text[n])


async def main():
    await asyncio.gather(*(download(url, n) for url, n in sites))


if __name__ == '__main__':
    s = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - s
    downloads = (elem.downloads for elem in saving_dict.values())
    print("max times a url was saved: " + str(max(downloads)))
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
