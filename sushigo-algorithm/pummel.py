import asyncio
from aiohttp import ClientSession, TCPConnector
import datetime as dt
import fire
import json
from uuid import uuid4 as uuid

# superbad error if you're running this on a mac
# https://github.com/Cog-Creators/Red-DiscordBot/issues/581

def make_url(n_sim=1):
    return f"https://zblufwr0wi.execute-api.eu-west-1.amazonaws.com/api/sim/{n_sim}"

async def fetch(url, json_body, session):
    async with session.post(url, json=json_body) as response:
        return await response.read()

async def run(json_bodies, n_sim=1000):
    tasks = []
    url = make_url(n_sim=n_sim)
    # Fetch all responses within one Client session,
    # keep connection alive for all requests.
    async with ClientSession(connector=TCPConnector(limit=None), read_timeout=30000, conn_timeout=30000) as session:
        for i, body in enumerate(json_bodies):
            task = asyncio.ensure_future(fetch(url=url, json_body=body, session=session))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)
        # you now have all response bodies in this variable
        return responses
#
# def run_batch(n=50, sleep_time=1):
#     batch_id = str(uuid())[:8]
#     start = dt.datetime.now()
#     loop = asyncio.get_event_loop()
#     future = asyncio.ensure_future(run(n, sleep_time))
#     results = loop.run_until_complete(future)
#     for result in results:
#         r = json.loads(result)
#         try:
#             print(f"{len(results)},{(dt.datetime.now() - start).total_seconds()},{r['hostname']},{r['starttime']},{r['endtime']},{r['uniq_id']},{batch_id}")
#         except:
#             print(f",{(dt.datetime.now() - start).total_seconds()},fail,,,,{batch_id}")
#
#
# def run_batches(min_requests=100, max_requests=1000, stepsize=25, sleep_time=1):
#     for i in range(min_requests, max_requests, stepsize):
#         run_batch(n=i, sleep_time=sleep_time)


def ping(n_sim=1000):
    start = dt.datetime.now()
    json_body = {
        "order": ["maki-1", "maki-2", "maki-3", "sashimi", "egg", "salmon", "squid",
                  "wasabi", "pudding", "tempura", "dumpling"]
    }
    print(f"i am trying this endpoint now: {make_url(n_sim=n_sim)}")
    print(f"i will send along standard json payload:\n{json_body}")

    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(run(json_bodies=[json_body], n_sim=n_sim))
    results = loop.run_until_complete(future)
    print(f"ping back took {(dt.datetime.now() - start).total_seconds()} seconds")
    print(f"this is what we got back:\n{results[0]}")


if __name__ == "__main__":
    fire.Fire({
        'ping': ping
    })