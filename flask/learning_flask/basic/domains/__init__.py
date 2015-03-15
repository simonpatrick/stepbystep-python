from flask import Flask
from domains.hello.controller import ho

app = Flask(__name__)
app.register_blueprint(ho)


