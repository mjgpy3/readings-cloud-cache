#!/usr/bin/env python

from flask import Flask, request
from sys import argv
import pg8000
import urlparse
import os
import json
import urllib
import hashlib
app = Flask(__name__)

def auth(key):
    m = hashlib.md5()
    m.update(key + os.environ['KEY_SALT'])
    d = m.hexdigest()

    if d != os.environ['CORRECT_KEY']:
        raise Exception, 'Auth failed!'

def make_connection():
    return build_connection(pg8000, os.environ['DATABASE_URL'])

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

@app.route('/read', methods=['POST'])
def create_read():
    data = json.loads(request.data)
    auth(data.get('key', ''))

    connection = make_connection()
    cursor = connection.cursor()
    url = urllib.unquote(data['url'])


    cursor.execute('INSERT INTO read (url, created_at) VALUES (\'%s\', now())' % data['url'])

    connection.commit()

    return 'create read'

if __name__ == '__main__':
    app.run(debug=True)
