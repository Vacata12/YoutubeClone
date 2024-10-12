from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db
import json

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template("login.html")

@auth.route('/register', methods = ["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        confirmPassword = request.form.get("confirmPassword")
        
        #check if there's already user with such email.
        user = User.query.filter_by(email=email).first()
        if user:
            flash("Account with that email address already exist!", category="error")
        elif len(email) < 4:
            flash ("Email address is too short!", category="error")
        elif password != confirmPassword:
            flash ("Two passwords don't match!", category="error")
        elif password == None or len(password) <= 7:
            flash ("Password must be longer!", category="error")
        else:
            newUser = User(email=email, username = username, password = generate_password_hash(password))
            db.session.add(newUser)
            db.session.commit()
            flash("Account created", category="success")
            return redirect(url_for("views.home"))
    elif request.method == "GET":
        print("Ivan Glupak")    
    return render_template("register.html")