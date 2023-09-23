import requests
import time
from urls import sites

total = 0


def download_site(url, n, session):
    with session.get(url) as response:
        html = response.content.decode('utf-8')
        global total
        total += len(html)
        print("The requested char is " + html[n])


def download_all_sites(sites):
    with requests.Session() as session:
        for url, n in sites:
            download_site(url, n, session)


if __name__ == "__main__":
    start_time = time.time()
    download_all_sites(sites)
    duration = time.time() - start_time
    print(f"Downloaded {len(sites)} in {duration} seconds" + ", total=" + str(total))
