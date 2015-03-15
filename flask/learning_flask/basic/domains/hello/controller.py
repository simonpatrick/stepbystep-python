#!/usr/bin/env python
# encoding: utf-8

from flask import Blueprint,render_template,request
from domains.hello.models import MESSAGES

ho = Blueprint('hello',__name__)

@ho.route('/')
@ho.route('/hello/')
def hello():
    user=request.args.get('user','patrick')
    return render_template('index.html',user=user)

@ho.route('/show/<key>')
def show(key):
    return MESSAGES.get(key) or "%s not found !" % key

@ho.route('/add/<key>/<value>')
def add_or_update(key,value):
    MESSAGES[key]=value
    return "%s added/updated" % key
