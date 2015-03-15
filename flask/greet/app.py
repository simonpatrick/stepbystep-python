# _*_ coding=utf-8 _*_
from flask import Flask

__author__ = 'patrick'

app = Flask(__name__)


@app.route('/')
def hello_flask():
    return 'Hello to the flask world!'


if __name__ == '__main__':
    app.run(debug=True)