from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Video, Comment
from . import db, ALLOWED_EXTENSIONS, UPLOAD_FOLDER
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
from datetime import date
from .forms import CommentForm
import os
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
                login_user(user, remember=True)
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
    return redirect(url_for('views.home'))

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
    return render_template("register.html", user=current_user)

#check if the extension of the file is allow
def allowedFiles(filename):
    return "." in filename and \
        filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
        
@auth.route("/upload", methods = ["GET", "POST"])
@login_required
def uploadFile():
    if request.method == "POST":
        title = request.form.get("title")
        desc = request.form.get("desc")
        if "file" not in request.files:
            flash("No file part!", category="error")
            return redirect(request.url)
        upFile = request.files["file"]
        if upFile.filename == "":
            flash("No selected file!", category="error")
        if upFile and allowedFiles(upFile.filename):
            filename = secure_filename(upFile.filename)
        if upFile == "":
            flash("No selected file!", category="error")
        if not upFile and ALLOWED_EXTENSIONS(upFile):
            flash("No correct standart!", category="error")
        else:
            upFile.save(os.path.join(UPLOAD_FOLDER, upFile.filename))
            newVideo = Video(title=title, desc=desc, uploadPath="/UploadFolder/" + upFile.filename,linkPath="", userId=current_user.id)
            db.session.add(newVideo)
            db.session.commit()
    return render_template("upload.html", user=current_user)

@auth.route('/video/<int:videoId>', methods = ["GET", "POST"])
def video(videoId):
    findVideo = Video.query.get_or_404(videoId)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(text=form.content.data, date=date.today() ,userId = current_user.id, videoId=videoId)
        db.session.add(comment)
        db.session.commit()
        flash('Comment added!', 'success')
        return redirect(url_for('auth.video', videoId=videoId))
    return render_template("video.html", user=current_user, video=findVideo, form=form)

@auth.route("/myVideos")
@login_required
def myVideos():
    return render_template("myVideos.html", user=current_user)

@auth.route("/deleteVideo", methods=["POST"])
def deleteVideo():
    video = json.loads(request.data)
    videoId = video["videoId"]
    video = Video.query.get(videoId)
    if video:
        if video.userId == current_user.id:
            db.session.delete(video)
            db.session.commit()
    
    return jsonify({})