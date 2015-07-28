# _*_ coding=utf-8 _*_
import re
import requests

__author__ = 'patrick'

from flask import Flask, render_template

app = Flask(__name__)

username = "110863"
password = "PW_654321"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/getPassword")
def get_integration_password():
    s = requests.Session()
    login_url = "http://login.dooioo.org/login?usercode=%s&password=%s" % (username, password)
    r = s.post(login_url, verify=False)
    get_password_url = "https://login.dooioo.org/rootPassword/get"
    login_cookie = r.cookies
    r = s.get(get_password_url, cookies=login_cookie, verify=False)
    pattern = re.compile(r'【(.*)】')
    match = pattern.findall(r.content)
    if(len(match)<=0):return "获取万能密码失败。。。。。。。"
    return match[0]

@app.route("/setUserCode/<user_code>")
def set_user_code(user_code):
    username = user_code
    return username


@app.route("/setpw/<pwd>")
def set_password(pwd):
    password = pwd
    return password

@app.route("/init/usercode/<user_code>/password/<pwd>")
def init(user_code,pwd):
    username=user_code
    password=pwd
    return username+":"+password

if __name__ == '__main__':
    app.run(debug=True)