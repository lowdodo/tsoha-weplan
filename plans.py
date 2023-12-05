from db import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

def get_allplans():
    sql = text("SELECT plan_id, name FROM plans WHERE visible=1 ORDER BY name")
    return db.session.execute(sql).fetchall()

def get_all_subplans(plan_id):
    sql = text("SELECT subplans_id, name, description, is_done FROM subplans WHERE plan_id=:plan_id AND visible=1")
    return db.session.execute(sql, {"plan_id": plan_id}).fetchall()

def choose_plan(plan_id):
    sql = text("SELECT plan.name, user.name, plan.description FROM plans, users WHERE plan.id = :plan_id AND plan.creator_name = user.name")
    return db.session.execute(sql, {"plan_id": plan_id}).fetchone()

def add_plan(creator_id, creator_name, name, description, is_done):
    sql = text("INSERT INTO plans (creator_id, creator_name, name, description, visible, is_done) VALUES (:creator_id, :creator_name, :name, :description, 1, False) RETURNING plan_id")
    plan_id = db.session.execute(sql, {"creator_id": creator_id, "creator_name": creator_name, "name": name, "description": description}).fetchone()[0]
    db.session.commit()
    return plan_id


def add_subplan(creator_id, creator_name, plan_id, name, description, is_done):
    sql = text("INSERT INTO subplans (plan_id, creator_id, creator_name, name, description, visible, is_done) VALUES (:plan_id, :creator_id, :creator_name, :name, :description, 1, False) RETURNING subplans_id")
    subplans_id = db.session.execute(sql, {"plan_id": plan_id, "creator_id": creator_id, "creator_name": creator_name, "name": name, "description": description}).fetchone()[0]
    db.session.commit()
    return subplans_id


def remove_plan(plan_id, user_id):
    sql_remove_plan = text("UPDATE plans SET visible=0 WHERE plan_id=:plan_id AND creator_id=:user_id")
    sql_remove_subplans = text("UPDATE subplans SET visible=0 WHERE plan_id=:plan_id AND creator_id=:user_id")

    db.session.execute(sql_remove_plan, {"plan_id": plan_id, "user_id": user_id})
    db.session.execute(sql_remove_subplans, {"plan_id": plan_id, "user_id": user_id})

    db.session.commit()


def remove_subplan(subplans_id, user_id, mainplan_creator):
    sql = text("UPDATE subplans SET visible=0 WHERE (subplans_id=:subplans_id AND creator_id=:mainplan_creator) OR (subplans_id=:subplans_id AND creator_id=:user_id)")
    db.session.execute(sql, {"subplans_id": subplans_id, "user_id": user_id, "mainplan_creator": mainplan_creator})
    db.session.commit()

def get_plan_info(plan_id):
    sql = text("SELECT creator_id, creator_name, name, description, is_done FROM plans WHERE plan_id=:plan_id")
    result = db.session.execute(sql, {"plan_id": plan_id}).fetchone()
    print(result)
    return result

def get_subplan_info(plan_id):
    sql = text("SELECT creator_id, creator_name, name, description, subplans_id, is_done FROM subplans WHERE plan_id=:plan_id AND visible=1")
    subresult = db.session.execute(sql, {"plan_id": plan_id}).fetchall()
    return subresult

def get_subinfo_byid(subplans_id):
    sql = text("SELECT creator_id, creator_name, name, description, is_done FROM subplans WHERE subplans_id=:subplans_id AND visible=1")
    subresult = db.session.execute(sql, {"subplans_id": subplans_id}).fetchall()
    return subresult

def update_planstatus(plan_id, new_status, user_id):
    sql = text("UPDATE plans SET is_done=:new_status WHERE plan_id=:plan_id AND creator_id=:user_id")
    db.session.execute(sql, {"plan_id":plan_id, "new_status":new_status, "user_id":user_id})
    db.session.commit()

def update_subplanstatus(subplans_id, new_status, user_id):
    sql = text("UPDATE subplans SET is_done=:new_status")
    db.session.execute(sql, {"subplans_id":subplans_id, "new_status":new_status, "user_id":user_id})
    db.session.commit()