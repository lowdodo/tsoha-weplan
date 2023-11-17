from flask import Flask, session, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import users
from app import app

#First page we see, later we'll make this real pretty alright
@app.route("/")
def index():
    return render_template("index.html")

#login todo: check the name n pw
@app.route("/login", methods=["POST"])
def login():
    name = request.form["name"]
    password = request.form["password"]
    # todo: checking the name and password
    session["name"] = name
    value = session["name"]
    return redirect("/")

#logout
@app.route("/logout")
def logout():
    del session["name"]
    del session["user_id"]
    return redirect("/") 

#register:
@app.route("/register", methods=["GET","POST"])
def register():
    #user gets registeration form
    if request.method == "GET":
        return render_template("register.html")
    #register user to server
    if request.method == "POST":
        name = request.form["name"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]

        if password1 != password2:
            return render_template("error.html", message="passwords differ")

        if users.register(name, password1):
            if users.login(name, password1):
                return redirect("/")
        

        return render_template("error.html", message="registeration failed")

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
if __name__ == "__main__":
    app.run(debug=True)