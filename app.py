from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")
@app.route("/allplans")
def allplans():
    return "Here we will have the list of all active plans"

@app.route("/allplans/test")
def test():
    return "This is a page within a page"

@app.route("/form")
def form():
    return render_templlate("form.html")

@app.route("/result", methods=["POST"])
def result():
    return render_template("result.html", name=request.form["name"])
