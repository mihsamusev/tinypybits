import io
import asyncio
import aiofiles
import pandas as pd
import sys
import os


async def get_csv_async(filepath: str):
    async with aiofiles.open(filepath, "r") as stream:
        with io.StringIO(await stream.read()) as buffer:
            return pd.read_csv(buffer)


async def get_all_csvs_async(filepaths: list):
    futures = [get_csv_async(filepath) for filepath in filepaths]
    return await asyncio.gather(*futures)


def find_by_extension(folder: str, extension: str):
    return [
        os.path.join(folder, file)
        for file in os.listdir(folder)
        if file.endswith(extension)
    ]


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Please submit the contents.json file")
        sys.exit()

    folder = sys.argv[-1]
    csv_paths = find_by_extension(folder, "csv")
    asyncio.get_event_loop().run_until_complete(get_all_csvs_async(csv_paths))
