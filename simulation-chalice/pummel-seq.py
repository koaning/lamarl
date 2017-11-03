import itertools as it 
import requests as rq 
import async_timeout

def make_url(scale, times):
    return f'https://kh2oatxvkk.execute-api.eu-west-1.amazonaws.com/api/simulate/{scale}/{times}/'

pummel_args = it.product(range(1, 10), range(1, 10))

if __name__ == '__main__':
    for args in pummel_args:
        resp = rq.get(make_url(*args))
        print(resp.json())