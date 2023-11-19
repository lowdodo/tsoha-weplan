from db import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

def get_allplans():
    sql = text("SELECT id, name FROM plans WHERE visible=1 ORDER BY name")
    return db.session.execute(sql).fetchall()

def choose_plan(plan_id):
    sql = text("SELECT plan.name, user.name, plan.description FROM plans, users WHERE plan.id = :plan_id AND plan.creator_id = user.user_id")
    return db.session.execute(sql, {"plan_id": plan_id}).fetchone()

def add_plan(creator_id, name, description, newsubplans):
    sql = text("INSERT INTO plans (creator_id, name, description, visible) VALUES (:creator_id, :name, :description, 1) RETURNING id")
    plan_id = db.session.execute(sql, {"creator_id": creator_id, "name": name, "description": description}).fetchone()[0]

    if newsubplans:
        for subplan in newsubplans:
            sql = text("INSERT INTO subplans (plan_id, subplan) VALUES (:plan_id, :subplan)")
            db.session.execute(sql, {"plan_id": plan_id, "subplan": subplan})

    db.session.commit()
    return plan_id

def remove_plan(plan_id, user_id):
    sql = text("UPDATE plans SET visible=0 WHERE id=:plan_id AND creator_id=:user_id")
    db.session.execute(sql, {"plan_id": plan_id, "user_id": user_id})
    db.session.commit()

def remove_subplan(subplan_id, user_id):
    sql = text("UPDATE subplans SET visible=0 WHERE id=:subplan_id AND creator_id=:user_id")
    db.session.execute(sql, {"subplan_id": subplan_id, "user_id": user_id})
    db.session.commit()

def get_plan_info(plan_id):
    sql = text("SELECT creator_id, name, description FROM plans WHERE id=:plan_id")
    return db.session.execute(sql, {"plan_id": plan_id}).fetchone()
