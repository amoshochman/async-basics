import asyncio
import os
import shutil

import aiohttp

from concurrent_downloads.data.peps import peps

OUTPUT_FOLDER = "data_output"

my_dict = {}

results = {}

TASKS_NUM = 10


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


async def download(pep_number: int, n: int) -> None:
    print("tasks num:" + str(len(asyncio.all_tasks())))
    if pep_number in my_dict:
        await my_dict[pep_number]
        filename = get_filename(pep_number)
        with open(get_output_filepath(filename)) as pep_file:
            content = pep_file.read()
    else:
        my_dict[pep_number] = asyncio.current_task()
        content = await download_page(pep_number)
        filename = get_filename(pep_number)
        with open(get_output_filepath(filename), "wb") as pep_file:
            pep_file.write(content)
    results[(pep_number, n)] = content[n]


def get_output_filepath(filename):
    return OUTPUT_FOLDER + "/" + filename


def get_filename(pep_number):
    filename = f"async_{pep_number}.html"
    return filename


async def main() -> None:
    print("before the gather tasks num:" + str(len(asyncio.all_tasks())))
    tasks = [download(pep, n) for (pep, n) in peps]
    pending = set()
    for task in tasks:
        pending.add(asyncio.ensure_future(task))
        if len(pending) >= TASKS_NUM:
            done, pending = await asyncio.wait(pending)  # , return_when=asyncio.FIRST_COMPLETED)
    if pending:
        await asyncio.wait(pending)
    print("after the gather... tasks num:" + str(len(asyncio.all_tasks())))


if __name__ == '__main__':
    shutil.rmtree(OUTPUT_FOLDER, ignore_errors=True)
    os.mkdir(OUTPUT_FOLDER)
    asyncio.run(main())
