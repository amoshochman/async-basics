import os
import shutil
from collections import defaultdict

import aiohttp
import asyncio
from urls import sites
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
        filename = unique_filename(url)
        if url not in saving_dict:
            saving_dict[url].waiter_task = asyncio.create_task(waiter(event))
            async with session.get(url) as response:
                html = await response.text()
                with open('data/' + filename, 'w') as file:
                    file.write(html)
                    saving_dict[filename].downloads += 1
                event.set()
                print("The requested char is " + html[n])
        else:
            await saving_dict[url].waiter_task
            with open('data/' + filename) as file:
                kk = file.read()
                print("The requested char is " + kk[n])


def unique_filename(url):
    url_without_protocol = url.replace('http://', '').replace('https://', '')
    sanitized_url = url_without_protocol.replace('/', '_').replace('.', '_')
    return sanitized_url + '.html'


async def main():
    await asyncio.gather(*(download(url, n) for url, n in sites))


if __name__ == '__main__':
    folder = 'data'
    shutil.rmtree(folder)
    os.mkdir(folder)
    s = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - s
    downloads = (elem.downloads for elem in saving_dict.values())
    print("max times a url was saved: " + str(max(downloads)))
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
