from bottle import route, run, template, static_file, response, request, TEMPLATE_PATH, default_app

import bottle
import json
import os
import requests
import sys


TEMPLATE_PATH.insert(0, os.path.abspath(os.path.dirname(__file__)))

class Params:
    pass
params = Params()

@route('/')
def index():
    return template('index')

@route('/draw')
def draw():
    return template('draw')

@route('/<filepath:path>')
def assets(filepath):
    return static_file(filepath, root='.')

@route('/song', method='get')
def song():
    if params.generator is None:
        params.generator = Generator()

    lyrics, filename =  params.generator.generate()

    return {'lyrics': lyrics, 'filename': filename}


if __name__ == '__main__':
    run(host='0.0.0.0', port=8888, debug=True)
else:
    application = default_app()


