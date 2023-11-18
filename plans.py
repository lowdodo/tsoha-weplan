from db import db

#plans should be added to the main page while session.name 
#maybe change the order later on butletssee
def get_allplans():
    sql = text("SELECT id, name FROM plans ORDER BY name")
    return db.session.execute(sql).fetchall()


#choosing one plan to look into. The plan creator still amiss
def choose_plan(plan_id):
    sql = """SELECT plan.name, user.name FROM palns, users WHERE plan.id =: plan_id AND plan.creator_id = user.id"""
    return db.session.execute(sql, {"plan_id":plan_id}).fetchone()