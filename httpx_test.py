import asyncio
import threading
import time

import httpx


async def async_main(url, sign):
    async with httpx.AsyncClient() as client:
        response = await client.get(url, timeout=10)
    status_code = response.status_code
    print(f'async_main: {threading.current_thread()}: {sign}:{status_code}')
    return sign


async def main():
    tasks = [
        async_main(
            url='https://www.tuicool.com/articles/iEJNrmy',
            sign=i) for i in range(20)
    ]
    async_start = time.time()
    res = await asyncio.gather(*tasks)
    async_end = time.time()
    print(async_end - async_start)
    print(res)


asyncio.run(main(), debug=True)
