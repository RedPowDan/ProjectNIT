import asyncio
from time import time


async def get_user():
    start_time = time()
    print("Begin get_user")
    await asyncio.sleep(4)
    print(f"End get_user in {time() - start_time} sec")


async def get_payload():
    start_time = time()
    print("Begin get_payload")
    await asyncio.sleep(3)
    print(f"End get_payload in {time() - start_time} sec")


async def main():
    task1 = asyncio.create_task(get_user())
    task2 = asyncio.create_task(get_payload())

    await task1
    await task2


if __name__ == '__main__':
    main_start_time = time()
    asyncio.run(main())
    print(f'Total time: {time() - main_start_time} sec')
