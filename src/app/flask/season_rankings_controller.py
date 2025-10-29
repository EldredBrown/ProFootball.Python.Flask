from flask import Blueprint, render_template, request, url_for, redirect, flash

from app.data.repositories.league_repository import LeagueRepository
from app.data.repositories.season_rankings_repository import SeasonRankingsRepository
from app.data.repositories.season_repository import SeasonRepository
from app.flask.season_controller import season_repository
from app.services.weekly_update_service.weekly_update_service import WeeklyUpdateService

blueprint = Blueprint('season_rankings', __name__)

RANKING_TYPES = ['Offense', 'Defense', 'Total']

season_repository = SeasonRepository()
seasons = None
selected_year = None

league_repository = LeagueRepository()
leagues = None
selected_league_name = None

selected_type = None

season_rankings_repository = SeasonRankingsRepository()


@blueprint.route('/')
def index():
    global seasons
    global selected_year
    global leagues
    global selected_league_name
    global selected_type

    seasons = season_repository.get_seasons()
    leagues = league_repository.get_leagues()
    return render_template(
        'season_rankings/index.html',
        seasons=seasons, selected_year=selected_year, leagues=leagues, selected_league_name=selected_league_name,
        types=RANKING_TYPES, selected_type=selected_type, season_rankings=None
    )


@blueprint.route('select_season', methods=['POST'])
def select_season():
    global seasons
    global selected_year
    global leagues
    global selected_league_name
    global selected_type

    selected_year = int(request.form.get('season_dropdown'))  # Fetch the selected season.
    return render_template(
        'season_rankings/index.html',
        seasons=seasons, selected_year=selected_year, leagues=leagues, selected_league_name=selected_league_name,
        types=RANKING_TYPES, selected_type=selected_type, season_rankings=None
    )


@blueprint.route('select_league', methods=['POST'])
def select_league():
    global seasons
    global selected_year
    global leagues
    global selected_league_name
    global selected_type

    selected_league_name = str(request.form.get('league_dropdown'))  # Fetch the selected league.
    return render_template(
        'season_rankings/index.html',
        seasons=seasons, selected_year=selected_year, leagues=leagues, selected_league_name=selected_league_name,
        types=RANKING_TYPES, selected_type=selected_type, season_rankings=None
    )


@blueprint.route('select_type', methods=['POST'])
def select_type():
    global selected_type

    selected_type = str(request.form.get('ranking_type_dropdown'))  # Fetch the selected type.
    if selected_type == 'Offense':
        return redirect(url_for('season_rankings.offense'))
    elif selected_type == 'Defense':
        return redirect(url_for('season_rankings.defense'))
    elif selected_type == 'Total':
        return redirect(url_for('season_rankings.total'))
    else:
        raise TypeError('Invalid ranking type')


@blueprint.route('weekly_update', methods=['POST'])
def run_weekly_update():
    global seasons
    global selected_year
    global leagues
    global selected_league_name
    global selected_type

    league_name = selected_league_name
    season_year = selected_year
    weekly_update_service = WeeklyUpdateService()
    weekly_update_service.run_weekly_update(league_name, season_year)
    flash(
        f"The weekly update has been successfully completed for the '{league_name}' in {season_year}.",
        'success'
    )
    return render_template(
        'season_rankings/index.html',
        seasons=seasons, selected_year=selected_year, leagues=leagues, selected_league_name=selected_league_name,
        types=RANKING_TYPES, selected_type=selected_type, season_rankings=None
    )


@blueprint.route('/offense')
def offense():
    global selected_year

    season_rankings = season_rankings_repository.get_offensive_rankings_by_season_year(selected_year)
    return render_template(
        'season_rankings/offense.html',
        seasons=seasons, selected_year=selected_year, leagues=leagues, selected_league_name=selected_league_name,
        types=RANKING_TYPES, selected_type=selected_type, season_rankings=season_rankings
    )


@blueprint.route('/defense')
def defense():
    global selected_year

    season_rankings = season_rankings_repository.get_defensive_rankings_by_season_year(selected_year)
    return render_template(
        'season_rankings/defense.html',
        seasons=seasons, selected_year=selected_year, leagues=leagues, selected_league_name=selected_league_name,
        types=RANKING_TYPES, selected_type=selected_type, season_rankings=season_rankings
    )


@blueprint.route('/total')
def total():
    global selected_year

    season_rankings = season_rankings_repository.get_total_rankings_by_season_year(selected_year)
    return render_template(
        'season_rankings/total.html',
        seasons=seasons, selected_year=selected_year, leagues=leagues, selected_league_name=selected_league_name,
        types=RANKING_TYPES, selected_type=selected_type, season_rankings=season_rankings
    )
