import asyncio
import aiohttp
import aiofiles
import zipfile
import io
from urllib.parse import urljoin
import uuid


URL_TEMPLATE = urljoin(
    "http://bpp-api.westeurope.cloudapp.azure.com:8000", "price/{}/download"
)
URL_TEMPLATE = urljoin("http://127.0.0.1:8005", "download/{}")

STREAM_CHUNK_SIZE = 1024


async def download_zipped(session, url) -> io.BytesIO:
    print(f"blasting {url}")
    async with session.get(url) as response:
        buffer = io.BytesIO()
        async for chunk in response.content.iter_chunked(STREAM_CHUNK_SIZE):
            buffer.write(chunk)
        return buffer


async def extract_from_zip(zip_handle, source_name):
    data = zip_handle.read(source_name)
    async with aiofiles.open(f"{source_name}-{uuid.uuid1()}.csv", "wb") as fd:
        await fd.write(data)


async def unzip(buffer: io.BytesIO):
    with zipfile.ZipFile(buffer, "r") as handle:
        await extract_from_zip(handle, handle.namelist()[-1])


async def save(buffer: io.BytesIO):
    filename = f"{uuid.uuid4()}.zip"
    async with aiofiles.open(filename, "wb") as fout:
        await fout.write(buffer.getbuffer())


async def task(url):
    async with aiohttp.ClientSession() as session:
        buffer = await download_zipped(session, url)
    await unzip(buffer)


async def run_tasks(urls):
    tasks = [task(url) for url in urls]
    await asyncio.gather(*tasks)


async def run(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [download_zipped(session, url) for url in urls]
        await asyncio.gather(*tasks)


def make_urls(ids):
    return [URL_TEMPLATE.format(i) for i in ids]


if __name__ == "__main__":
    urls = make_urls(range(1, 50))
    asyncio.run(run_tasks(urls))