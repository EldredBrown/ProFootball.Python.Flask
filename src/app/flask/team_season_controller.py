from flask import Blueprint, abort, render_template, request

from app.data.repositories.season_repository import SeasonRepository
from app.data.repositories.team_season_repository import TeamSeasonRepository
from app.data.repositories.team_season_schedule_repository import TeamSeasonScheduleRepository

blueprint = Blueprint('team_season', __name__)

team_season_repository = TeamSeasonRepository()

seasons = None
selected_year = None


@blueprint.route('/')
def index():
    global seasons
    global selected_year

    season_repository = SeasonRepository()
    seasons = season_repository.get_seasons()
    return render_template(
        'team_seasons/index.html',
        seasons=seasons, selected_year=selected_year, team_seasons=[]
    )


@blueprint.route('/details/<int:id>')
def details(id: int):
    global team_season_repository

    team_season_schedule_repository = TeamSeasonScheduleRepository()

    try:
        team_season = team_season_repository.get_team_season(id)
        team_season_schedule_profile = team_season_schedule_repository.get_team_season_schedule_profile(
            team_season.team_name, team_season.season_year
        )
        team_season_schedule_totals = [team_season_schedule_repository.get_team_season_schedule_totals(
            team_season.team_name, team_season.season_year
        )]
        team_season_schedule_averages = [team_season_schedule_repository.get_team_season_schedule_averages(
            team_season.team_name, team_season.season_year
        )]
        return render_template(
            'team_seasons/details.html',
            team_season=team_season,
            team_season_schedule_profile=team_season_schedule_profile,
            team_season_schedule_totals=team_season_schedule_totals,
            team_season_schedule_averages=team_season_schedule_averages
        )
    except IndexError:
        abort(404)


@blueprint.route('/select_season', methods=['POST'])
def select_season():
    global seasons
    global selected_year
    global team_season_repository

    selected_year = int(request.form.get('season_dropdown'))  # Fetch the selected season.
    team_seasons = team_season_repository.get_team_seasons_by_season_year(season_year=selected_year)
    return render_template(
        'team_seasons/index.html',
        seasons=seasons, selected_year=selected_year, team_seasons=team_seasons
    )
