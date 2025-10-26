from flask import Blueprint, render_template, request

from app.data.repositories.season_standings_repository import SeasonStandingsRepository
from app.flask.season_controller import season_repository

blueprint = Blueprint('season_standings', __name__)

season_standings_repository = SeasonStandingsRepository()

seasons = None
selected_year = None


@blueprint.route('/')
def index():
    global seasons
    global selected_year

    seasons = season_repository.get_seasons()
    season_standings = []
    return render_template(
        'season_standings/index.html',
        seasons=seasons, selected_year=selected_year, season_standings=season_standings
    )


@blueprint.route('/select_season', methods=['POST'])
def select_season():
    global seasons
    global selected_year

    selected_year = int(request.form.get('season_dropdown'))  # Fetch the selected season.
    season_standings = season_standings_repository.get_season_standings_by_season_year(season_year=selected_year)
    return render_template(
        'season_standings/index.html',
        seasons=seasons, selected_year=selected_year, season_standings=season_standings
    )
