import requests
from sites import sites
from timer import timer

results = {}

def download_site(url, n, session):
    with session.get(url) as response:
        html = response.content.decode('utf-8')
        results[(url, n)] = html[n]


def download_all_sites(sites):
    with requests.Session() as session:
        for url, n in sites:
            download_site(url, n, session)

@timer
def my_sync_main():
    download_all_sites(sites)
    return results

