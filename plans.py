from db import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

def get_allplans():
    sql = text("SELECT plan_id, name FROM plans WHERE visible=1 ORDER BY name")
    return db.session.execute(sql).fetchall()

def get_all_subplans(plan_id):
    sql = text("SELECT subplans_id, name, description FROM subplans WHERE plan_id=:plan_id AND visible=1")
    return db.session.execute(sql, {"plan_id": plan_id}).fetchall()

def choose_plan(plan_id):
    sql = text("SELECT plan.name, user.name, plan.description FROM plans, users WHERE plan.id = :plan_id AND plan.creator_name = user.name")
    return db.session.execute(sql, {"plan_id": plan_id}).fetchone()

def add_plan(creator_id, name, description, newsubplans, new):
    if new:
        sql = text("INSERT INTO plans (creator_id, name, description, visible) VALUES (:creator_id, :name, :description, 1) RETURNING plan_id")
        plan_id = db.session.execute(sql, {"creator_id": creator_id, "name": name, "description": description}).fetchone()[0]

    if not new and newsubplans:
        for subplan in newsubplans:
            sql = text("INSERT INTO subplans (plan_id, subplan) VALUES (:plan_id, :subplan) RETURNING subplans_id")
            subplans_id = db.session.execute(sql, {"plan_id": plan_id, "subplan": subplan}).fetchone()[0]

    db.session.commit()

    if not new:
        return subplans_id
    return plan_id


def remove_plan(plan_id, user_id):
    sql_remove_plan = text("UPDATE plans SET visible=0 WHERE plan_id=:plan_id AND creator_id=:user_id")
    sql_remove_subplans = text("UPDATE subplans SET visible=0 WHERE plan_id=:plan_id AND creator_id=:user_id")
    db.session.execute(sql_remove_plan, {"plan_id": plan_id, "user_id": user_id})
    db.session.execute(sql_remove_subplans, {"plan_id": plan_id, "user_id": user_id})

    db.session.commit()


def remove_subplan(subplans_id, user_id):
    sql = text("UPDATE subplans SET visible=0 WHERE id=:subplans_id AND creator_id=:user_id")
    db.session.execute(sql, {"subplans_id": subplans_id, "user_id": user_id})
    db.session.commit()

def get_plan_info(plan_id):
    sql = text("SELECT creator_id, name, description FROM plans WHERE plan_id=:plan_id")
    return db.session.execute(sql, {"plan_id": plan_id}).fetchone()

def get_subplan_info(plan_id):
    sql = text("SELECT creator_id, name, description, subplans_id FROM subplans WHERE plan_id=:plan_id AND visible=1")
    return db.session.execute(sql, {"plan_id": plan_id}).fetchone()
