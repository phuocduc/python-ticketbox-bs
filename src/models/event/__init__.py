from src import db
from sqlalchemy.sql import func


class Event(db.Model):
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255))
    address = db.Column(db.String(255), nullable=False)
    img_pic = db.Column(db.String(255))   
    time = db.Column(db.Date, nullable = False)
    active = db.Column(db.Boolean, default = False) 
    event_type = db.Column(db.String(255), nullable=False)
    ticket = db.relationship('Ticket', backref='event', lazy=True)
    rating = db.relationship('Rating', backref='event', lazy='dynamic')

    def add(self, user):
        user.event.append(self)
        db.session.commit()

    def get_rating(self):
        sumcount= self.ratings.with_entities(func.sum(Rating.stars), func.count(Rating.stars)).first()
        return (sumcount[0]/sumcount[1],sumcount[1])

class Rating(db.Model):
    __tablename__= 'ratings'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), primary_key=True)
    stars = db.Column(db.Integer, nullable=False)


class Ticket(db.Model):
    __tablename__ = 'tickets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable= False)    

    def add(self):
        db.session.add(self)
        db.session.commit()
