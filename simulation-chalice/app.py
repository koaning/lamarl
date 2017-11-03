from chalice import Chalice
import datetime as dt 
import time
import socket
import random

app = Chalice(app_name='simulation-chalice')


@app.route('/')
def index():
    return {'hello': 'world'}


@app.route('/simulate/{scale}/{times}')
def simulate(scale, times):
    start = dt.datetime.now()
    s = 0
    for i in range(int(times)):
        s += random.random()*int(scale)
    return {'scale': int(scale), 'times': int(times), 'sum': s, 'mean': s/int(times), 'time': str(dt.datetime.now() - start)}


@app.route('/sleep/{seconds}')
def sleep(seconds):
    start = dt.datetime.now()
    time.sleep(float(seconds))
    return {"seconds": seconds, "starttime": str(start), "endtime": str(dt.datetime.now()), "hostname": socket.gethostname()}


@app.lambda_function(name='sleeper')
def sleeper(event, context):
    start = dt.datetime.now()
    time.sleep(event['seconds'])
    return {"seconds": event['seconds'], "starttime": str(start), "endtime": str(dt.datetime.now()), "hostname": socket.gethostname()}


# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#
