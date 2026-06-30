from flask import Blueprint, render_template, request, session

from app import injector
from app.data.repositories.season_repository import SeasonRepository
from app.data.repositories.season_standings_repository import SeasonStandingsRepository

blueprint = Blueprint('season_standings', __name__)


@blueprint.route('/')
def index() -> str:
    season_repository = injector.get(SeasonRepository)

    seasons = season_repository.get_seasons()
    session['seasons'] = [s.to_dict() for s in seasons]

    selected_season_id = -1
    season_standings = []
    return render_template(
        'season_standings/index.html',
        seasons=seasons, selected_season_id=selected_season_id, season_standings=season_standings
    )


@blueprint.route('/select_season', methods=['POST'])
def select_season() -> str:
    selected_season_id = int(request.form.get('season_dropdown'))  # Fetch the selected season.

    season_standings_repository = injector.get(SeasonStandingsRepository)
    season_standings = season_standings_repository.get_season_standings_by_season(season_id=selected_season_id)
    return render_template(
        'season_standings/index.html',
        seasons=session.get('seasons'), selected_season_id=selected_season_id, season_standings=season_standings
    )
