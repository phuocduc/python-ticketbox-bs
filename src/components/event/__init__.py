from flask import Blueprint, render_template, request, redirect,url_for, flash
from flask_login import login_required, current_user
from src.models.event import Event, Ticket
from src import db

event_blueprint = Blueprint('event',__name__, template_folder='../../templates')


@event_blueprint.route('/home')
@login_required
def home_page():
    events = Event.query.all()

    return render_template('home/home.html', events = events)

@event_blueprint.route('/event', methods=['GET','POST'])
@login_required
def show_create_event():
    if request.method == "POST":
        print('create event')
        new_events = Event(event_name = request.form['event_name'], user_id = current_user.id, location = request.form['event_location'], address= request.form['event_address'], event_type=request.form.get('event_dropdown'), img_pic = request.form['event_img'], time = request.form['event_date'])
        db.session.add(new_events)
        db.session.commit()
        return redirect(url_for('event.render_event', id = new_events.id))
    return render_template('event/create_event.html')


@event_blueprint.route('/event/<id>/ticket', methods=['GET', 'POST'])
def show_ticket_page(id):
    if request.method == "POST":
        print('created ticket')
        new_ticket = Ticket(name = request.form['ticket_name'], price=request.form['ticket_price'], stock= request.form['ticket_stock'], event_id = id)
        db.session.add(new_ticket)
        db.session.commit()
        return redirect(url_for('event.render_event'))
    return render_template('event/create_ticket.html', event_id = id)


@event_blueprint.route('/render/<id>', methods=['GET', 'POST'])
def delete_event(id):
    event = Event.query.filter_by(id = id).first()
    db.session.delete(event)
    db.session.commit()
    return render_template('user/profile.html')


@event_blueprint.route('/event/<event_id>/tickets/<ticket_id>', methods=['GET', 'POST'])
def delete_ticket(event_id, ticket_id):
    
    ticket = Ticket.query.filter_by(id = ticket_id).first()
    if not ticket:
        flash("fucking delete to you")
        return redirect(url_for('event.render_event'))
    if ticket:
        db.session.delete(ticket)
        db.session.commit()
        return redirect(url_for('event.render_event'))
    return render_template('event/show_ticket.html')


@event_blueprint.route('/active/<event_id>', methods=['POST','GET'])
def active_event(event_id):

    event = Event.query.get(event_id)
    if event.active == True:
        event.active = False
    else:
        event.active = True
    db.session.commit()
    return render_template('user/profile.html')



@event_blueprint.route('/render')
def render_event():
    events = Event.query.all()
    return render_template('user/profile.html',events = events)


@event_blueprint.route('/event/<id>/tickets')
def render_ticket(id):
    tickets = Ticket.query.filter_by(event_id = id).all()
    return render_template('event/show_ticket.html', tickets= tickets)