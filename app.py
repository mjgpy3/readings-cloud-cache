#!/usr/bin/env python

from flask import Flask
from sys import argv
import pg8000
import urlparse
import os
app = Flask(__name__)

# TODO: Wire with
# pg8000.connect
# os.environ["DATABASE_URL"]
def build_connection(connector, pg_url):
    urlparse.uses_netloc.append("postgres")
    url = urlparse.urlparse(pg_url)

    conn = connector.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )

    return conn

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    print "HELLO WORLD"
    print argv
    app.run()
