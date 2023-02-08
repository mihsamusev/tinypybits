import io
import asyncio

import aiohttp
import pandas as pd


async def get_csv_async(client, url):
    # Send a request.
    async with client.get(url) as response:
        # Read entire resposne text and convert to file-like using StringIO().
        with io.StringIO(await response.text()) as text_io:
            return pd.read_csv(text_io)


async def get_all_csvs_async(urls):
    async with aiohttp.ClientSession() as client:
        # First create all futures at once.
        futures = [get_csv_async(client, url) for url in urls]
        # Then wait for all the futures to complete.
        return await asyncio.gather(*futures)


urls = [
    # Some random CSV urls from the internet
    "https://people.sc.fsu.edu/~jburkardt/data/csv/hw_25000.csv",
    "https://people.sc.fsu.edu/~jburkardt/data/csv/addresses.csv",
    "https://people.sc.fsu.edu/~jburkardt/data/csv/airtravel.csv",
]

if "__main__" == __name__:
    # Run event loop
    # can just do `csvs = asyncio.run(get_all_csvs_async(urls))` in python 3.7+
    csvs = asyncio.get_event_loop().run_until_complete(get_all_csvs_async(urls))

    for csv in csvs:
        print(csv)
