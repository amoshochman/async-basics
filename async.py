import os
import shutil
from collections import defaultdict

import aiohttp
import asyncio
from urls import sites
import time

saving_dict = defaultdict(int)


async def download(url, n):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()
            filename = unique_filename(url)
            with open('data/' + filename, 'w') as file:
                saving_dict[filename] += 1
                file.write(html)
            print("The requested char is " + html[n])


def unique_filename(url):
    url_without_protocol = url.replace('http://', '').replace('https://', '')
    sanitized_url = url_without_protocol.replace('/', '_').replace('.', '_')
    filename = sanitized_url + '.html'

    return filename


async def main():
    await asyncio.gather(*(download(url, n) for url, n in sites))


if __name__ == '__main__':
    folder = 'data'
    shutil.rmtree(folder)
    os.mkdir(folder)
    s = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - s
    print("max times a url was saved: " + str(max(saving_dict.values())))
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
