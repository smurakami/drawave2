from bottle import route, run, template, static_file, response, request, TEMPLATE_PATH, default_app

import bottle
import json
import os
import requests
import sys

# from predict import predict

import numpy as np
import time


TEMPLATE_PATH.insert(0, os.path.abspath(os.path.dirname(__file__)))

class Params:
    pass
params = Params()

@route('/')
def index():
    return template('./ui/index')

@route('/draw')
def draw():
    return template('./ui/draw')

@route('/<filepath:path>')
def assets(filepath):
    return static_file(filepath, root='./ui')

@route('/wave', method='POST')
def wave():
    paths = json.loads(request.params.get('data'))

    json.dump(paths, open('./ui/data/paths.json', 'w'))
    print(paths)

    json.dump({"timestamp": time.time()}, open('./ui/data/timestamp.json', 'w'))

    # params = predict(paths)
    # print(params)
    # np.save('midi/params.npy', params)

    return {'success': True}


if __name__ == '__main__':
    run(host='0.0.0.0', port=8888, debug=True)
else:
    application = default_app()


