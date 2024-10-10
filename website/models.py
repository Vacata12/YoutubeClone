from sqlalchemy import func
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from . import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(1024), unique=True)
    username = db.Column(db.String(256), unique=True)
    password = db.Column(db.String(1024))
    comments = db.relationship('Comment', backref='user', lazy=True)
    videos = db.relationship('Video', backref='user', lazy=True)
    
class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), unique=True)
    desc = db.Column(db.String(1024))
    uploadPath = db.Column(db.String(256), nullable=True)
    linkPath = db.Column(db.String(256), nullable=True)
    userId =  db.Column(db.Integer, db.ForeignKey("user.id"))
    comments = db.relationship('Comment', backref='video', lazy=True)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    userId =  db.Column(db.Integer, db.ForeignKey("user.id"))
    videoId =  db.Column(db.Integer, db.ForeignKey("video.id"))