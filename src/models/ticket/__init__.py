from src import db


class Ticket(db.Model):
    __tablename__ = "tickets"
    id = db.Column(db.Integer, primary_key=True)
    # event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    # order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    ticket_type= db.Column(db.String(255), nullable=False)
    