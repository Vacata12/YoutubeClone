from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from . import db
from .models import Video
import json

views = Blueprint('views', __name__)

@views.route('/')
def home():
    all_videos = Video.query.all()
    return render_template("home.html", user=current_user, videos=all_videos)