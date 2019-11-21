from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user

app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy(app)

from src.models.user import User

migrate = Migrate(app,db)


login_manager = LoginManager(app)
login_manager.login_view="users.login"

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)




from src.components.user import user_blueprint
app.register_blueprint(user_blueprint, url_prefix="/")

# from src.components.event import event_blueprint
# app.register_blueprint(event_blueprint, url_prefix="/event")


# @app.route('/')
# def root():
#     return "OK"