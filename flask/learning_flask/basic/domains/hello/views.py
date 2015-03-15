from domains import app
from domains.hello.models import MESSAGES

@app.route('/')
@app.route('/hello/')
def hello():
    return MESSAGES['default']

@app.route('/show/<key>')
def get_message(key):
    return MESSAGES.get(key) or "%s not found" % key

@app.route('/add/<key>/<message>')
def add_or_update(key,message):
    MESSAGES[key]=message
    return "%s Added/Updated" % key

