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
    sql_remove_joined = text("UPDATE ownplans SET visible=0 WHERE plan_id=:plan_id")
    db.session.execute(sql_remove_plan, {"plan_id": plan_id, "user_id": user_id})
    db.session.execute(sql_remove_subplans, {"plan_id": plan_id, "user_id": user_id})
    db.session.execute(sql_remove_joined, {"plan_id": plan_id})

    db.session.commit()

def remove_subplan(subplans_id, user_id, mainplan_creator):
    sql = text("UPDATE subplans SET visible=0 WHERE (subplans_id=:subplans_id AND creator_id=:mainplan_creator) OR (subplans_id=:subplans_id AND creator_id=:user_id)")
    db.session.execute(sql, {"subplans_id": subplans_id, "user_id": user_id, "mainplan_creator": mainplan_creator})
    db.session.commit()

def get_plan_info(plan_id):
    sql = text("SELECT creator_id, creator_name, name, description, is_done FROM plans WHERE plan_id=:plan_id")
    result = db.session.execute(sql, {"plan_id": plan_id}).fetchone()
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
    sql = text("UPDATE plans SET is_done =:new_status WHERE plan_id =:plan_id AND creator_id=:user_id")
    db.session.execute(sql, {"plan_id":plan_id, "new_status":new_status, "user_id":user_id})
    db.session.commit()

def update_subplanstatus(subplans_id, new_status, user_id):
    sql = text("UPDATE subplans SET is_done=:new_status WHERE subplans_id=:subplans_id")
    db.session.execute(sql, {"subplans_id":subplans_id, "new_status":new_status, "user_id":user_id})
    db.session.commit()

def add_to_own(user_id, plan_id, creator_name, is_done):
    # #already exists?
    exists = text("SELECT * FROM ownplans WHERE user_id=:user_id AND plan_id=:plan_id")
    result = db.session.execute(exists, {"user_id": user_id, "plan_id": plan_id}).fetchone()
    if result:
        user_plan_id = result[0]
        sql = text("UPDATE ownplans SET visible=1 WHERE user_plan_id=:user_plan_id")
        db.session.execute(sql, {"user_plan_id":user_plan_id})
        db.session.commit()
        return user_plan_id
    else:
        sql = text("INSERT INTO ownplans (user_id, plan_id, creator_name, visible, is_done)VALUES (:user_id, :plan_id, :creator_name, 1, :is_done) RETURNING user_plan_id")
        user_plan_id = db.session.execute(sql, {"user_id":user_id, "plan_id": plan_id, "creator_name": creator_name, "is_done":is_done}).fetchone()[0]
        print("userplanid", user_plan_id)
        db.session.commit()
        return user_plan_id

def get_ownplaninfo(user_id):
    sql = text("SELECT * FROM ownplans WHERE user_id =:user_id AND visible=1")
    own_plans = db.session.execute(sql, {"user_id": user_id}).fetchall()
    return own_plans

def remove_own(user_plan_id, user_id):
    sql = text("UPDATE ownplans SET visible=0 WHERE user_plan_id=:user_plan_id")
    db.session.execute(sql, {"user_plan_id": user_plan_id, "user_id": user_id})
    db.session.commit()
    return True

def statistics():
    sql= text("""SELECT p.plan_id, p.name AS plan_name, p.is_done AS plan_status,
                COUNT(sp.subplans_id) AS total_subplans,
                SUM(CASE WHEN sp.is_done THEN 1 ELSE 0 END) AS completed,
                CASE WHEN COUNT(sp.subplans_id) > 0 THEN
                    ROUND((SUM(CASE WHEN sp.is_done THEN 1 ELSE 0 END) * 100.0) / COUNT(sp.subplans_id), 1)
                    WHEN p.is_done THEN 100 ELSE 0
                END AS completionpros FROM plans p
                LEFT JOIN subplans sp ON p.plan_id = sp.plan_id
                WHERE p.visible = 1
                GROUP BY p.plan_id, p.name, p.is_done;""")

    data = db.session.execute(sql).fetchall()
    return data

def comment(plan_id, username, comment):
    sql = text("INSERT INTO comments (plan_id, username, comment, visible, is_done, created_at) VALUES (:plan_id, :username, :comment, 1, False, NOW()) RETURNING comment_id")
    comment_id = db.session.execute(sql, {"plan_id":plan_id, "username":username, "comment":comment})
    db.session.commit()
    return comment_id

def get_plan_comments(plan_id):
    sql = text("SELECT username, comment, is_done, created_at, comment_id FROM comments WHERE plan_id =:plan_id AND visible=1")
    comments = db.session.execute(sql, {"plan_id":plan_id}).fetchall()
    return comments

def get_commentinfo(comment_id):
    sql = text("SELECT username, plan_id FROM comments WHERE comment_id=:comment_id AND visible=1")
    result = db.session.execute(sql, {"comment_id": comment_id}).fetchone()
    return result

def delete_comment(comment_id):
    sql = text("UPDATE comments SET visible=0 WHERE comment_id=:comment_id")
    db.session.execute(sql, {"comment_id": comment_id})
    db.session.commit()


