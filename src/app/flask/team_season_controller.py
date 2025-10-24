from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from sqlalchemy.exc import IntegrityError

from app.data.repositories.team_season_repository import TeamSeasonRepository

blueprint = Blueprint('team_season', __name__)

team_season_repository = TeamSeasonRepository()


@blueprint.route('/')
def index():
    team_seasons = team_season_repository.get_team_seasons()
    return render_template('team_seasons/index.html', team_seasons=team_seasons)


@blueprint.route('/details/<int:id>')
def details(id: int):
    try:
        team_season = team_season_repository.get_team_season(id)
        return render_template('team_seasons/details.html', team_season=team_season)
    except IndexError:
        abort(404)
