#!/usr/bin/env python
# encoding: utf-8

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello Flask World'

if __name__=='__main__':
    app.run()
