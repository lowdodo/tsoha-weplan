from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "WEPLAN"
@app.route("/allplans")
def allplans():
    return "Here we will have the list of all active plans"

@app.route("/allplans/test")
def test():
    return "This is a page within a page"
