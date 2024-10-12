from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import json

auth = Blueprint('auth', __name__)

@auth.route('/login', methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        
        if user:
            if not check_password_hash(user.password, password):
                flash("Wrong password!", category="error")
            else:
                flash("Logged successfully!", category="success")
                login_user = (user)
                return redirect(url_for("views.home"))
        else:
            flash("User does not exist!", category="error")
    else:
        print("it's get")  
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home', user=current_user))

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
            return redirect(url_for("views.home", user=current_user))
    elif request.method == "GET":
        print("Ivan Glupak")    
    return render_template("register.html")