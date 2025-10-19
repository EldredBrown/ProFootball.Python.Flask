from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return "Welcome to my Pro Football application!"


@app.route('/privacy')
def privacy():
    return "This is your privacy policy."
