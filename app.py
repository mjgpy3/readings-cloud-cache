#!/usr/bin/env python

from flask import Flask, request
from flask.ext.cors import cross_origin
from sys import argv
import pg8000
import urlparse
import os
import json
import urllib
import hashlib
app = Flask(__name__)

UNSAFE_STRS = ['/*', "'", ' ', '\n', '\r', '\t']

def assert_safe_url(url):
    assert ((url.startswith('http://') or url.startswith('https://')) and
           sum(1 for i in UNSAFE_STRS if i in url) == 0)

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

@app.route('/read', methods=['GET'])
def get_read_all():
    connection = make_connection()
    cursor = connection.cursor()

    cursor.execute('SELECT url FROM read ORDER BY created_at desc LIMIT 10;')

    urls = cursor.fetchall()
    result = '<ol>%s</ol>' % ''.join('<li>' + url[0] + '</li>' for url in urls)

    connection.commit()

    return result

@app.route('/read', methods=['POST', 'OPTIONS'])
@cross_origin()
def create_read():
    data = json.loads(request.data)
    auth(data.get('key', ''))
    assert_safe_url(data['url'])

    connection = make_connection()
    cursor = connection.cursor()

    cursor.execute('INSERT INTO read (url, created_at) VALUES (\'%s\', now())' % data['url'])

    connection.commit()

    return 'create read'

if __name__ == '__main__':
    app.run(debug=True)
