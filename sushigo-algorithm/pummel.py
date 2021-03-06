import asyncio
from aiohttp import ClientSession, TCPConnector
import datetime as dt
import fire
import random
from evol import Population
from evol.helpers.pickers import pick_random
import json
from uuid import uuid4 as uuid
import numpy as np
import async_timeout
from pprint import pprint


# superbad error if you're running this on a mac
# https://github.com/Cog-Creators/Red-DiscordBot/issues/581

def make_url(n_sim=1):
    return f"https://7rlli5d2lj.execute-api.eu-west-1.amazonaws.com/api/sim/{n_sim}"

async def fetch(url, json_body, session):
    # TODO WHAT IS THE TIMEOUT?!?!
    with async_timeout.timeout(160):
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
        "order": ["maki-1", "maki-2", "maki-3", "sashimi",
                  "egg", "salmon", "squid", "wasabi", "pudding",
                  "tempura", "dumpling", "tofu", "eel", "temaki"]
    }
    print(f"i am trying this endpoint now: {make_url(n_sim=n_sim)}")
    print(f"i will send along standard json payload:\n{json_body}")

    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(run(json_bodies=[json_body], n_sim=n_sim))
    results = loop.run_until_complete(future)
    print(f"ping back took {(dt.datetime.now() - start).total_seconds()} seconds")
    print(f"this is what we got back:\n{results[0]}")

def random_population(n_population=10, n_sim=1000):
    init_order = ["maki-1", "maki-2", "maki-3", "sashimi",
                  "egg", "salmon", "squid", "wasabi", "pudding",
                  "tempura", "dumpling", "tofu", "eel", "temaki"]
    json_bodies = []
    random.shuffle(init_order)
    for i in range(n_population):
        json_bodies.append({"order": init_order})

    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(run(json_bodies=json_bodies, n_sim=n_sim))
    results = loop.run_until_complete(future)
    loop.close()
    print(f"i just parsed {len(json_bodies)} sequences")
    return [(results[i], json_bodies[i]) for i,c in enumerate(json_bodies)]

def score_population(json_bodies, n_sim=1000):
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(run(json_bodies=json_bodies, n_sim=n_sim))
    results = loop.run_until_complete(future)
    return [(results[i], body) for i, body in enumerate(json_bodies)]

def make_random_switch(order):
    idx1, idx2 = random.choices([i for i in range(len(order))], k=2)
    order[idx1], order[idx2] = order[idx2], order[idx1]
    return order

def swapper(order, **kwargs):
    order = list(order)
    idx1 = random.randint(0, len(order) - 2)
    idx2 = random.randint(idx1 + 1, len(order) - 1)
    if ('maki-1' in order[idx1]) and ('maki-2' in order[idx2]):
        return swapper(order)
    if ('maki-1' in order[idx1]) and ('maki-3' in order[idx2]):
        return swapper(order)
    if ('maki-2' in order[idx1]) and ('maki-3' in order[idx2]):
        return swapper(order)
    if ('egg' in order[idx1]) and ('salmon' in order[idx2]):
        return swapper(order)
    if ('egg' in order[idx1]) and ('squid' in order[idx2]):
        return swapper(order)
    if ('salmon' in order[idx1]) and ('squid' in order[idx2]):
        return swapper(order)
    order[idx1], order[idx2] = order[idx2], order[idx1]
    return order

def apply_search(n_rounds=10, n_population=10, n_sim=1000):
    init_order = ["maki-1", "maki-2", "maki-3", "sashimi",
                  "egg", "salmon", "squid", "wasabi", "pudding",
                  "tempura", "dumpling", "tofu", "eel", "temaki"]
    json_bodies = []
    for i in range(n_population):
        random.shuffle(init_order)
        json_bodies.append({"order": init_order[:]})

    for i in range(n_rounds):
        start = dt.datetime.now()
        scores = score_population(json_bodies=json_bodies, n_sim=n_sim)
        scores = sorted(scores, key = lambda x: int(x[0]))
        score_dict = {tuple(k['order']):int(v) for v,k in scores}
        pop = Population([k for k,v in score_dict.items()], lambda k: score_dict[k])
        pop = pop.survive(fraction=0.1).breed(pick_random, swapper, n_parents=1, population_size=n_population)
        print(f"round: {str(i+1).zfill(4)} best score: {max(score_dict.values())} time: {(dt.datetime.now() - start).total_seconds()}s")
        print(",".join([s[0:3]+s[-1] for s in scores[-1][1]['order']]))
        json_bodies = [{"order": i.chromosome} for i in pop]


if __name__ == "__main__":
    fire.Fire({
        'ping': ping,
        'random-search': random_population,
        'evolve': apply_search
    })