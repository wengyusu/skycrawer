from bs4 import BeautifulSoup
import requests
# import aiohttp
import asyncio
import json
import functools
import time
# import logging
# PYTHONASYNCIODEBUG=1
# logging.basicConfig(level=logging.DEBUG)
# start=time.time()
# count = 0
tasks = []
q = asyncio.Queue()
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}

async def req(url):
    future1 = loop.run_in_executor(None,functools.partial(requests.get, url,headers=headers))
    r = await future1
    return r.content

async def dlc(q):
    while True:
        if not q.empty():
            url1 = await q.get()
        else:
            # q.task_done()
            break
        d = await req(url1)
        # async with aiohttp.request('GET', url1, headers=headers) as d:
            # d = await d.text()
        # print(sku)
        # d = requests.get(url1, headers=headers)
        # d = d.text
        soup1 = BeautifulSoup(d, 'lxml')
        result1 = soup1.find_all("a", attrs={"data-pid": True})
        # print(url1)
        for i in result1:
            # global count
            datam = json.loads(i['data-m'])
            # if i['data-pid'] == 'state of decay 2 preorder':
                # pass
            #     print(url1)
            #     print(datam['cS'])
            #     print(datam['cS'] == 'DisplayCatalog')
            if datam['cS'] == 'DisplayCatalog':
                # count = count + 1
                # print(i['data-pid']) #dlc名字
                print(datam['pid'].lower()) #dlc id
            # print(datam['cS'])
                # if i is result1[-1]:
                #     # loop.close()
        q.task_done()

async def fetch(q):
    fetch_tasks=[]
    for j in range(5):
        fetch_tasks.append(asyncio.ensure_future(dlc(q)))
    url = 'https://www.microsoft.com/en-us/store/coming-soon/games/xbox'
    pre = 'https://www.microsoft.com'
    # async with aiohttp.request('GET', url, headers=headers) as r:
    #     r = await r.text()
    r = requests.get(url, headers=headers)
    r=r.text
    soup = BeautifulSoup(r, 'lxml')
    # print(r.text)
    result = soup.find_all("a", attrs={"data-pid": True})
    # print(len(result))
    for i in result:
        print(i['data-pid']) #游戏id
        # print(i['href'])   #详情url
        # if i is result[-1]:
        #     asyncio.ensure_future(dlc(pre + i['href'], last=True), loop=loop)
        #     # loop.close()
        # else:
        # tasks.append(dlc(pre + i['href'],i['data-pid']))
        q.put_nowait(pre+i['href'])
        # asyncio.ensure_future(dlc(pre + i['href'], i['data-pid'], q))
    await q.join()
    # for w in fetch_tasks:
    #     w.cancel()
    loop.stop()
    
loop = asyncio.get_event_loop()
# tasks = [
#     await (fetch(q))
# ]
asyncio.ensure_future(fetch(q))
loop.run_forever()
# loop.run_until_complete(asyncio.ensure_future(fetch(q)))
# print(count)
loop.close()
# end = time.time()
# print(end-start)
