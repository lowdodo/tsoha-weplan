from flask import session, render_template, request, redirect, flash
import users, plans
from users import user_id_forname
from app import app

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
        plan_id = plans.add_plan(creator_id, creator_name, name, description, is_done=False)
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

        if len(name) < 1 or len(name) > 30:
            return render_template("error.html", message=f"Name of subplan should be 1-30 characters long")

        if len(description) > 1000:
            return render_template("error.html", message=f"Use a shorter description")

        plans.add_subplan(creator_id, creator_name, plan_id, name, description, is_done=False)
        return redirect(f"/plan/{plan_id}")
    
@app.route("/plan/<int:plan_id>")
def show_plan(plan_id):
    plan_info = plans.get_plan_info(plan_id)
    main_plan = {
        "creator": plan_info.creator_name,
        "name": plan_info.name,
        "description": plan_info.description,
        "status": plan_info.is_done
    }

    #are there subplans?
    subplans_info = plans.get_subplan_info(plan_id)

    subplans = []
    for subplan_info in subplans_info:
        creator_name = subplan_info.creator_name
        name = subplan_info.name
        description = subplan_info.description
        id = subplan_info.subplans_id
        status = subplan_info.is_done
        subplans.append({
            "creator": creator_name,
            "name": name,
            "description": description,
            "id": id,
            "status":status
        })

    #are there comments?
    plans_comments = plans.get_plan_comments(plan_id)
    comments = []
    for comment in plans_comments:
        username = comment.username
        comment_text = comment.comment
        status = comment.is_done
        created_at = comment.created_at
        comments.append({
            "username":username,
            "comment": comment_text,
            "status":status,
            "created_at":created_at
            })

    return render_template("plan.html", plan_id=plan_id, main_plan=main_plan, subplans_info=subplans, comments=comments)

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
    if user_id != creator and user_id != mainplan_creator:
        return render_template("error.html", message="You dont have permission to remove this plan.")
    plans.remove_subplan(subplans_id, user_id, mainplan_creator)
    print("poisto onnistui")
    return redirect(f"/plan/{plan_id}")

@app.route("/mark_done/<int:plan_id>", methods= ["POST"])
def plandone(plan_id):
    current_status = plans.get_plan_info(plan_id)[4]
    new_status = not current_status
    print("this is current", current_status)
    print("this is new", new_status)
    user_id = session.get("user_id")
    plans.update_planstatus(plan_id, new_status, user_id)
    return redirect("/")

@app.route("/mark_done/<int:plan_id>/<int:subplans_id>", methods=["POST"])
def subplandone(subplans_id, plan_id):
    subplan_info = plans.get_subinfo_byid(subplans_id)
    current_status = subplan_info[0][4]
    new_status = not current_status
    user_id = session.get("user_id")
    plans.update_subplanstatus(subplans_id, new_status, user_id)
    return redirect(f"/plan/{plan_id}")

@app.route("/ownplans/<int:plan_id>", methods=["POST"])
def add_to_own(plan_id):
    print("addtoown routen alussa")
    user_id = session.get("user_id")
    creator_name = plans.get_plan_info(plan_id)[1]
    is_done = plans.get_plan_info(plan_id)[4]
    print("isdone", is_done)
    plans.add_to_own(user_id, plan_id, creator_name, is_done)
    print("selvittiin addtoown routesta")
    return redirect("/")

@app.route("/ownplans/<int:user_id>")
def showown(user_id):
    # user_id = session.get("user_id")
    username = session.get("name")
    own_plans = plans.get_ownplaninfo(user_id)
    print("ownplans", own_plans)
    ownplans = []
    for own_plan in own_plans:
        user_plan_id = own_plan.user_plan_id
        user_id = own_plan.user_id
        plan_id = own_plan.plan_id
        plan_name = plans.get_plan_info(plan_id)[2]
        creator_name = own_plan.creator_name
        status = own_plan.is_done
        ownplans.append({
            "user_plan_id": user_plan_id,
            "user_id": user_id,
            "plan_id": plan_id,
            "name": plan_name,
            "creator_name": creator_name,
            "status": status
        })
    return render_template("ownplans.html", username = username, ownplans = ownplans)

@app.route("/remove_fromown/<int:user_plan_id>")
def remove_fromown(user_plan_id):
    user_id = session.get("user_id")
    plans.remove_own(user_plan_id, user_id)
    return redirect(f"/ownplans/{user_id}")

@app.route("/statistics")
def statistics():
    statistics_data = plans.statistics()
    return render_template("statistics.html", statistics_data=statistics_data)

@app.route("/commentplan/<int:plan_id>", methods=["POST"])
def comment(plan_id):
    username = session.get("name")
    comment_text = request.form.get("comment_text")
    plans.comment(plan_id, username, comment_text)
    return redirect(f"/plan/{plan_id}")


if __name__ == "__main__":
    app.run(debug=True)