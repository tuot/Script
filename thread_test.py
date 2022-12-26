import asyncio
import time
from concurrent.futures import (ProcessPoolExecutor, ThreadPoolExecutor,
                                as_completed)

# from __future__ import print_function


CNT = 100
MAX_WORKER = 20


def log_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        print(time.time() - start)
        return res
    return wrapper


def do_thing(a, b):
    time.sleep(1)
    return a*b


async def do_thing2(a, b):
    await asyncio.sleep(1)
    if a*b == 25:
        raise Exception
    return a*b


@log_time
def test_thread():
    res = []
    with ThreadPoolExecutor(max_workers=MAX_WORKER) as executor:
        obj_list = []
        for i in range(CNT):
            t = executor.submit(do_thing, i, i)
            obj_list.append(t)
        for future in as_completed(obj_list): # no order
            res.append(future.result())
    print(res)

@log_time
def test_thread2():
    res = []
    with ThreadPoolExecutor(max_workers=MAX_WORKER) as executor:
        obj_list = []
        for i in range(CNT):
            t = executor.submit(do_thing, i, i)
            obj_list.append(t)
        for future in obj_list: # has order
            res.append(future.result())
    print(res)

@log_time
def test_process():
    res = []
    with ProcessPoolExecutor(max_workers=MAX_WORKER) as executor:
        data = ((i, i) for i in range(CNT))
        for future in executor.map(do_thing, *zip(*data)):
            res.append(future)


async def test_coroutine():
    task_list = []
    for i in range(CNT):
        task_list.append(do_thing2(i, i))
    res = await asyncio.gather(*task_list, return_exceptions=True)
    return res


async def test_coroutine2():
    task_list = []
    for i in range(CNT):
        task_list.append(do_thing2(i, i))
    res = []
    for future in asyncio.as_completed(task_list):
        try:
            result = await future
            res.append(result)
        except Exception as e:
            print(f'{e} happened while processing')

    return res


@log_time
def test_async_io():
    res = asyncio.run(test_coroutine())


@log_time
def test_async_io2():
    res = asyncio.run(test_coroutine2())


test_thread()
test_thread2()
# test_process()
# test_async_io()
# test_async_io2()
