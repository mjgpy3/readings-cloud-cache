#!/usr/bin/env python

from flask import Flask
from sys import argv
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run(port=argv[1])
