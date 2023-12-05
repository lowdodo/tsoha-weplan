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
        print("eka sesisom", session)
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
        print(session)
        creator_id = session.get("user_id")
        creator_name = session.get("name")
        plan_id = plans.add_plan(creator_id, creator_name, name, description)
        flash("new plan added")
        return redirect("/")

@app.route("/addsub/<int:plan_id>", methods=["GET", "POST"])
def add_subplan(plan_id):
    if request.method == "GET":
        return render_template("addsub.html", plan_id=plan_id)

    if request.method == "POST":
        creator_id = session.get("user_id")
        creator_name = session.get("name")


        name = request.form["name"]
        description = request.form[f"description"]

        if len(name) < 1 or len(name) > 20:
            return render_template("error.html", message=f"Name of subplan should be 1-20 characters long")

        if len(description) > 1000:
            return render_template("error.html", message=f"Use a shorter description")

        plans.add_subplan(creator_id, creator_name, plan_id, name, description)

        flash("new subplan added")
        return redirect(f"/plan/{plan_id}")
    
@app.route("/plan/<int:plan_id>")
def show_plan(plan_id):
    plan_info = plans.get_plan_info(plan_id)
    main_plan = {
        "creator": plan_info.creator_name,
        "name": plan_info.name,
        "description": plan_info.description,
    }

    #are there subplans?
    subplans_info = plans.get_subplan_info(plan_id)

    subplans = []
    for subplan_info in subplans_info:
        creator_name = subplan_info.creator_name
        name = subplan_info.name
        description = subplan_info.description
        id = subplan_info.subplans_id
        subplans.append({
            "creator": creator_name,
            "name": name,
            "description": description,
            "id": id
        })

    return render_template("plan.html", plan_id=plan_id, main_plan=main_plan, subplans_info=subplans)

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

@app.route("/removesubplan/<int:plan_id>/<int:subplans_id>")
def remove_subplan(subplans_id, plan_id):
    #later add "are you sure you want to remove" before actually removing
    user_id = session.get("user_id")
    mainplan_creator = plans.get_plan_info(plan_id)[0]
    print("tässä on mainvcer", mainplan_creator)
    creator = plans.get_subinfo_byid(subplans_id)[0][0]
    print("tässä on creator", creator) 
    print("tässä on user", user_id)
    if user_id != creator or user_id != mainplan_creator:
        return render_template("error.html", message="You dont have permission to remove this plan.")
    plans.remove_subplan(subplans_id, user_id, mainplan_creator)
    print("poisto onnistui")
    return redirect(f"/plan/{plan_id}")


if __name__ == "__main__":
    app.run(debug=True)