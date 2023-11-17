import os
from db import db
import users
from flask_sqlalchemy import SQLAlchemy

from flask import abort, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text

#lets do the login of the users, for now, this is from example
def login(name, password):
    sql = text("SELECT password, userid FROM users WHERE name=:name")
    result = db.session.execute(sql, {"name":name})
    user = result.fetchone()
    if not user:
        return False
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            session["user_id"] = user.userid
            session["user_name"] = name
            return True

#loggin out
def logout():
    del session["user_id"]
    del session["user_name"]

#lets register first without roles:
def register(name, password):
    #later we could add safer password recommendations.
    hash_value = generate_password_hash(password)
    try:
        sql = text("INSERT INTO users (name, password) VALUES (:name, :password)")
        db.session.execute(sql, {"name":name, "password":hash_value})
        db.session.commit()
        return True
    except:
        db.session.rollback()
        return False
    
    #return login(name, password)

#getting the user_id:
def user_id():
    return session.get("user_id", 0)

def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
