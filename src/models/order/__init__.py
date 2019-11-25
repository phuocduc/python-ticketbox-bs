from src import db

class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    order_type=db.Column(db.String(255), nullable=False)
    # ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.id'))
    # ticket = db.relationship('Ticket', backref="ticketsId", lazy=True)