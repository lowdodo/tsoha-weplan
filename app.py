from flask import Flask
from flask import render_template, request, redirect, session
from os import getenv

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

#First page we see, later we'll make this real pretty alright
@app.route("/")
def index():
    return render_template("index.html")

#login????
@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    #todo: checking the username and password
    session["username"] = username
    return redirect("/")
#logout
@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")    

#We dont currently use this that much sorry
@app.route("/allplans")
def allplans():
    return "Here we will have the list of all active plans"

@app.route("/allplans/test")
def test():
    return "This is a page within a page"

# @app.route("/form")
# def form():
#     return render_template("form.html")

# @app.route("/result", methods=["POST"])
# def result():
#     return render_template("result.html", name=request.form["name"])
