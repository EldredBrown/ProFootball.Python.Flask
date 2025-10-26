from flask import Blueprint, render_template

from app.flask.season_controller import season_repository

blueprint = Blueprint('home', __name__)


@blueprint.route('/')
def index():
    return render_template('home/index.html')


@blueprint.route('/privacy')
def privacy():
    return render_template('home/privacy.html')
