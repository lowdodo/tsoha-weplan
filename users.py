import os
from db import db
from flask import abort, request, session
from werkzeug.security import check_password_hash, generate_password_hash

#lets do the login of the users, for now, this is from example
def login(name, password):
    sql = "SELECT password, id FROM users WHERE name=: name"
    result = db.session.execute(sql, {"name":name})
    user = result.fetchone()
    if not user:
        return False
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            session["user_id"] = user.id
            session["user_name"] = name

#loggin out
def logout():
    del session["user_id"]
    del session["user_name"]

#lets register first without roles:
def register(name, password):
    #later we could add safer password recommendations.
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (name, password)  VALUES (:name, :password)"
        db.session.execute(sql, {"name":name, "password":hash_value})
        db.session.commit()
    except:
        return False
    return login(name, password)

#getting the user_id:
def user_id():
    return session.get("user_id", 0)
