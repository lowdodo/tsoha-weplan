from flask import session, render_template, request, redirect
import users, plans
from users import user_id_forname
from app import app

#First page we see, later we'll make this real pretty alright
@app.route("/")
def index():
    return render_template("index.html", plans=plans.get_allplans())

#login todo: check the name n pw
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template("index.html")
    
    if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]
    if not users.login(name, password):
        return render_template("error.html", message="Incorrect login information")
    return redirect("/")

#logout
@app.route("/logout")
def logout():
    users.logout()
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

                session["user_id"] = user_id_forname(name)
                session["name"] = name
                return redirect("/")
        

        return render_template("error.html", message="registeration failed")


@app.route("/addplan", methods=["GET", "POST"])
def add_plan():
    if request.method == "GET":
        return render_template("add.html")
    
    if request.method == "POST":
        name = request.form["name"]
        if len(name) < 1 or len(name) > 20:
            return render_template("error.html", message="Name should be 1-20 characters long")
        description = request.form["description"]
        if len(description) > 1000:
            return render_template("error.html", message="use shorter description")
        creator_id = session.get("user_id")
        plan_id = plans.add_plan(creator_id, name, description, newsubplans=None)
        return redirect("/plan/"+str(plan_id))

@app.route("/plan/<int:plan_id>")
def show_plan(plan_id):
    description = plans.get_plan_info(plan_id)[2]
    name = plans.get_plan_info(plan_id)[1]

    return render_template("plan.html", id=plan_id, description=description, name=name)

# @app.route("/result", methods=["POST"])
# def result():
#     return render_template("result.html", name=request.form["name"])
if __name__ == "__main__":
    app.run(debug=True)