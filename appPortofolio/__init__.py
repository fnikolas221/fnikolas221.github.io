from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_manager
from .config import Config

db = SQLAlchemy()


def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)
    
    #DATABASE
    db.init_app(app)
    
    login_manager = LoginManager()

        #Login view Location For Admin 
    login_manager.login_view = 'admin.login'
    login_manager.init_app(app)

    from .models import Admin
    @login_manager.user_loader
    def load_user(admin_id):
        return Admin.query.get(int(admin_id))
    
    #blueprint for admin
    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)

    #blueprint for the rest
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # #for error handling
    # from .errors import errors as error_blueprint
    # app.register_blueprint(error_blueprint)

    return app
