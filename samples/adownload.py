import os
import uuid
import time

import aiohttp
import asyncio


def write_file(data: bytes):
    folder = 'download'
    if not os.path.exists(folder):
        os.mkdir(folder)

    file_name = str(uuid.uuid4()) + '.ico'
    file_path = os.path.join(folder, file_name)
    with open(file_path, 'wb') as file:
        file.write(data)


async def download_image(url: str):

    async with aiohttp.ClientSession() as session:
        response = await session.get(url)

    if response.status == 200:
        data = await response.read()
        write_file(data)


async def main():
    tasks = [
        asyncio.create_task(download_image('https://www.google.com/favicon.ico'))
        for _ in range(5)
    ]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    start_time = time.time()
    asyncio.run(main())
    print(f'Total time: {time.time() - start_time} sec')
