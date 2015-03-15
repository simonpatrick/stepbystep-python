# _*_ coding=utf-8 _*_
from flask import Flask
from greet.hello.controllers import hello

__author__ = 'patrick'

app = Flask(__name__)
app.register_blueprint(hello)