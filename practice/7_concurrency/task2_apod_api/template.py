import asyncio
import requests
import aiohttp
from pathlib import Path
import os

from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("API_KEY")
APOD_ENDPOINT = 'https://api.nasa.gov/planetary/apod'
OUTPUT_IMAGES = './practice/7_concurrency/task2_apod_api/output'


async def download_url(session, url: str) -> None:
    '''Download file at url to OUTPUT_IMAGES directory'''
    async with session.get(url) as response:
        filename = Path(OUTPUT_IMAGES) / url.split('/')[-1]
        with open(filename, 'wb') as f:
            f.write(await response.read())
        print(f"Downloaded and saved: {filename}")


async def download_apod_images(query_params: dict[str, str]) -> None:
    '''Download images from APOD with given query params'''
    res = requests.get(APOD_ENDPOINT, query_params)
    assert res.status_code == 200
    content = res.json()

    urls = [i["hdurl"] for i in content if i['media_type'] == 'image']

    async with aiohttp.ClientSession() as session:
        return await asyncio.gather(*(download_url(session, url) for url in urls))

if __name__ == '__main__':

    APOD_query_params = {
        'start_date': '2021-08-01',
        'end_date': '2021-08-10',
        'api_key': API_KEY,
    }

    asyncio.run(download_apod_images(APOD_query_params))
