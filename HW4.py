import requests
import os
import time
import threading
import multiprocessing
import asyncio
import argparse
import aiohttp
from pathlib import Path


images = []
with open('images.txt', 'r') as f:
    for image in f.readlines():
        images.append(image.strip())

PATH = Path('downloads')

# Image downloader
def img_downloader(url, dir_path=PATH):
    start_time = time.time()
    response = requests.get(url)
    filename = str(url).split('/')[-1]

    with open(dir_path / filename, 'wb') as file:
        for data in response.iter_content(1024):
            file.write(data)
    print(f'Download complete in {start_time - time.time():.2f} sec.')


def cmd_parser():
    parser = argparse.ArgumentParser(description='URL parser')
    parser.add_argument('-u', '--urls', default=images, nargs='*', type=str, help='Url list')
    return parser.parse_args()


def threaded_downloader(urls):
    threads = []
    start_time = time.time()

    for url in urls:
        thread = threading.Thread(target=img_downloader, args=(url,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print(f'Threaded download complete in {start_time - time.time():.2f} sec.')


def multiprocess_downloader(urls):
    procs = []
    start_time = time.time()

    for url in urls:
        process = multiprocessing.Process(target=img_downloader, args=(url,))
        procs.append(process)
        process.start()

    for process in procs:
        process.join()

    print(f'Multiprocessing download complete in {start_time - time.time():.2f} sec.')


async def aiohttp_downloader(url, dir_path=PATH):
    start_time = time.time()
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            item = await response.read()
            filename = url.split('/')[-1]
            with open(dir_path / filename, 'wb') as f:
                f.write(item)
    print(f'Download complete in {start_time - time.time():.2f} sec.')


async def main(urls):
    start_time = time.time()
    tasks = [asyncio.create_task(aiohttp_downloader(url)) for url in urls]
    await asyncio.gather(*tasks)
    print(f'Asynchronous download complete in {start_time - time.time():.2f} sec.')

if __name__ == '__main__':
    urls = cmd_parser().urls

    if not PATH.exists():
        PATH.mkdir()

    print(f'Multithreaded download of {len(urls)} images started:')
    threaded_downloader(urls)

    print(f'Multiprocess download of {len(urls)} images started:')
    multiprocess_downloader(urls)

    print(f'Asynchronous download of {len(urls)} images started:')
    asyncio.run(main(urls))
