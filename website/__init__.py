from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from werkzeug.utils import secure_filename

db = SQLAlchemy()
DB_NAME = "database.db"
UPLOAD_FOLDER = "/UploadFolder/"
ALLOWED_EXTENSIONs = ["mkv", "MP4"]

def createApp():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "YoutubeClone"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    from .models import User, Comment, Video
    if not path.exists('website/instance' + DB_NAME):
        with app.app_context():
            db.create_all()
            print("Created Database")
    
    return app