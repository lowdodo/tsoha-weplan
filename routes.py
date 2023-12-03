from flask import session, render_template, request, redirect, flash
import users, plans
from users import user_id_forname
from app import app

#First page we see, later we'll make this real pretty alright
@app.route("/")
def index():
    return render_template("index.html", session=session, plans=plans.get_allplans())

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
        plan_id = plans.add_plan(creator_id, name, description)
        flash("new plan added")
        return redirect("/")

@app.route("/addsub/<int:plan_id>", methods=["GET", "POST"])
def add_subplan(plan_id):
    if request.method == "GET":
        num_subplans = 2
        return render_template("addsub.html", plan_id=plan_id, num_subplans=num_subplans)

    if request.method == "POST":
        num_subplans = int(request.form.get("num_subplans", 1))
        creator_id = session.get("user_id")

        for i in range(num_subplans):
            name = request.form[f"name{i}"]
            description = request.form[f"description{i}"]

            if len(name) < 1 or len(name) > 20:
                return render_template("error.html", message=f"Name of subplan {i+1} should be 1-20 characters long")

            if len(description) > 1000:
                return render_template("error.html", message=f"Use a shorter description for subplan {i+1}")

            plans.add_subplan(creator_id, plan_id, name, description)

        flash("new subplans added")
        return redirect(f"/plan/{plan_id}")
    
@app.route("/plan/<int:plan_id>")
def show_plan(plan_id):
    print("hsow pö'sij")
    plan_info = plans.get_plan_info(plan_id)
    description = plan_info[2]
    name = plan_info[1]
    creator = plan_info[0]

    print("pääsin tänne asti plan infopn")
    #is there subplans?
    subplans_info = plans.get_subplan_info(plan_id)
    print("TÄSSÄ subinfo", subplans_info)
    if subplans_info:
        subdescription = subplans_info[2]
        subname = subplans_info[1]
    else:
        subdescription = None
        subname = None
    return render_template("plan.html", plan_id=plan_id, description=description, name=name, creator_id=creator, subplans_info=subplans_info)


@app.route("/removeplan/<int:plan_id>")
def remove_plan(plan_id):
    #later add "are you sure you want to remove" before actually removing
    user_id = session.get("user_id")
    creator_id = plans.get_plan_info(plan_id)[0] 
    if user_id != creator_id:
        return render_template("error.html", message="You dont have permission to remove this plan.")
    plans.remove_plan(plan_id, user_id)
    print("poisto onnistui")
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)