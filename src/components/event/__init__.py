from flask import Blueprint, render_template


event_blueprint = Blueprint('event',__name__, template_folder='../../templates')

@event_blueprint.route('/')
def root():
    return render_template('event/index.html')