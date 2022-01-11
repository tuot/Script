import asyncio
import time
from concurrent.futures import (ProcessPoolExecutor, ThreadPoolExecutor,
                                as_completed)

# from __future__ import print_function


def do_thing(a, b):
    time.sleep(1)
    return a*b


async def do_thing2(a, b):
    await asyncio.sleep(1)
    return a*b


def test_thread():
    res = []
    start = time.time()
    with ThreadPoolExecutor(max_workers=10) as executor:
        obj_list = []
        for i in range(20):
            t = executor.submit(do_thing, i, i)
            obj_list.append(t)
        for future in as_completed(obj_list):
            res.append(future.result())
    print(time.time() - start)


def test_process():
    res = []
    start = time.time()
    with ProcessPoolExecutor(max_workers=10) as executor:
        data = ((i, i) for i in range(20))
        for future in executor.map(do_thing, *zip(*data)):
            res.append(future)
    print(time.time() - start)


async def test_coroutine():
    start = time.time()
    task_list = []
    for i in range(200):
        task_list.append(do_thing2(i, i))
    res = await asyncio.gather(*task_list)
    print(time.time() - start)
    return res


async def test_coroutine2():
    start = time.time()
    task_list = []
    for i in range(200):
        task_list.append(do_thing2(i, i))
    res = []
    for future in asyncio.as_completed(task_list):
        result = await future
        res.append(result)
    print(time.time() - start)
    return res


def test_async_io():
    res = asyncio.run(test_coroutine())
    print(res)
    res = asyncio.run(test_coroutine2())
    print(res)


test_thread()
test_process()
test_async_io()
