import asyncio
from aiohttp import ClientSession, TCPConnector
import datetime as dt
import fire
import json
from uuid import uuid4 as uuid

# superbad error if you're running this on a mac
# https://github.com/Cog-Creators/Red-DiscordBot/issues/581

def make_url(sleep_time=1, uniq_id="none"):
    return f"https://l9bvun2xk5.execute-api.eu-west-1.amazonaws.com/api/sleep/{sleep_time}/{uniq_id}"

async def fetch(url, session):
    async with session.get(url) as response:
        return await response.read()

async def run(n, sleep_time=1):
    tasks = []
    # Fetch all responses within one Client session,
    # keep connection alive for all requests.
    async with ClientSession(connector=TCPConnector(limit=None), read_timeout=30000, conn_timeout=30000) as session:
        for args in range(n):
            task = asyncio.ensure_future(fetch(make_url(sleep_time, str(uuid())[:8]), session))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)
        # you now have all response bodies in this variable
        return responses

def run_batch(n=50, sleep_time=1):
    batch_id = str(uuid())[:8]
    start = dt.datetime.now()
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(run(n, sleep_time))
    results = loop.run_until_complete(future)
    for result in results:
        r = json.loads(result)
        try:
            print(f"{len(results)},{(dt.datetime.now() - start).total_seconds()},{r['hostname']},{r['starttime']},{r['endtime']},{r['uniq_id']},{batch_id}")
        except:
            print(f",{(dt.datetime.now() - start).total_seconds()},fail,,,,{batch_id}")


def run_batches(min_requests=100, max_requests=1000, stepsize=25, sleep_time=1):
    for i in range(min_requests, max_requests, stepsize):
        run_batch(n=i, sleep_time=sleep_time)


def ping(sleep_time=1):
    start = dt.datetime.now()
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(run(1, sleep_time))
    results = loop.run_until_complete(future)
    print(f"i am trying this endpoint: {make_url(1, str(uuid())[:8])}")
    print(f"ping back took {(dt.datetime.now() - start).total_seconds()}s")
    print(f"this is what we got back:\n{results[0]}")


if __name__ == "__main__":
    fire.Fire({
        'ping': ping,
        'run-batch': run_batch,
        'run-batches': run_batches
    })