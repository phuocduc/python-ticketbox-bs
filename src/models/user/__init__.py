from flask_login import UserMixin,current_user
from src import db
from werkzeug.security import generate_password_hash,check_password_hash

class User(UserMixin,db.Model):
   
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(120),nullable=False)
    def set_password(self,password):
        self.password = generate_password_hash(password)
    def check_password(self,password):
        return check_password_hash(self.password,password)
    def check_user(self):
        return User.query.filter_by(email=self.email).first()
    