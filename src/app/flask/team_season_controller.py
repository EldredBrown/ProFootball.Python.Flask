from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from sqlalchemy.exc import IntegrityError

from app.data.repositories.team_season_repository import TeamSeasonRepository
from app.flask.season_controller import season_repository

blueprint = Blueprint('team_season', __name__)

team_season_repository = TeamSeasonRepository()

seasons = None


@blueprint.route('/')
def index():
    global seasons
    seasons = season_repository.get_seasons()
    team_seasons = team_season_repository.get_team_seasons()
    return render_template('team_seasons/index.html', seasons=seasons, team_seasons=team_seasons)


@blueprint.route('/details/<int:id>')
def details(id: int):
    try:
        team_season = team_season_repository.get_team_season(id)
        return render_template('team_seasons/details.html', team_season=team_season)
    except IndexError:
        abort(404)


@blueprint.route('/submit', methods=['POST'])
def submit():
    global seasons
    selected_value = int(request.form.get('season_dropdown'))  # Fetch the selected season.
    team_seasons = team_season_repository.get_team_seasons_by_season_year(season_year=selected_value)
    return render_template('team_seasons/index.html', seasons=seasons, team_seasons=team_seasons)
