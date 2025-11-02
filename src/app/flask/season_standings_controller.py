from flask import Blueprint, render_template, request

from app import injector
from app.data.repositories.season_repository import SeasonRepository
from app.data.repositories.season_standings_repository import SeasonStandingsRepository

blueprint = Blueprint('season_standings', __name__)

seasons = []
selected_year = None


@blueprint.route('/')
def index() -> str:
    global seasons
    global selected_year

    season_repository = injector.get(SeasonRepository)
    seasons = season_repository.get_seasons()

    season_standings = []
    return render_template(
        'season_standings/index.html',
        seasons=seasons, selected_year=selected_year, season_standings=season_standings
    )


@blueprint.route('/select_season', methods=['POST'])
def select_season() -> str:
    global seasons
    global selected_year

    selected_year = int(request.form.get('season_dropdown'))  # Fetch the selected season.
    season_standings_repository = injector.get(SeasonStandingsRepository)

    season_standings = season_standings_repository.get_season_standings_by_season_year(season_year=selected_year)
    return render_template(
        'season_standings/index.html',
        seasons=seasons, selected_year=selected_year, season_standings=season_standings
    )
