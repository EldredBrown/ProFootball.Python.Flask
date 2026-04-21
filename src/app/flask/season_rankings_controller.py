from flask import Blueprint, render_template, request, url_for, redirect, flash, Response, session

from app import injector
from app.data.repositories.league_repository import LeagueRepository
from app.data.repositories.season_rankings_repository import SeasonRankingsRepository
from app.data.repositories.season_repository import SeasonRepository
from app.services.weekly_update_service.weekly_update_service import WeeklyUpdateService

blueprint = Blueprint('season_rankings', __name__)

RANKING_TYPES = ['Offense', 'Defense', 'Total']


@blueprint.route('/')
def index() -> str:
    season_repository = injector.get(SeasonRepository)
    seasons = [s.to_dict() for s in season_repository.get_seasons()]
    session['seasons'] = seasons

    selected_year = None
    leagues = []
    selected_league_name = None
    selected_type = None

    return render_template(
        'season_rankings/index.html',
        seasons=seasons, selected_year=selected_year,
        leagues=leagues, selected_league_name=selected_league_name,
        types=RANKING_TYPES, selected_type=selected_type, season_rankings=None
    )


@blueprint.route('select_season', methods=['POST'])
def select_season() -> str:
    selected_year = int(request.form.get('season_dropdown'))  # Fetch the selected season.
    session['selected_year'] = selected_year

    leagues = session.get('leagues')
    leagues_active_in_selected_year = [
        l for l in leagues
        if selected_year >= l['first_season_year'] and (
                l['last_season_year'] is None or selected_year <= l['last_season_year']
        )
    ]

    return render_template(
        'season_rankings/index.html',
        seasons=session.get('seasons'), selected_year=selected_year,
        leagues=leagues_active_in_selected_year, selected_league_name=None,
        types=RANKING_TYPES, selected_type=None, season_rankings=None
    )


@blueprint.route('select_league', methods=['POST'])
def select_league() -> str:
    selected_league_name = str(request.form.get('league_dropdown'))  # Fetch the selected league.
    session['selected_league_name'] = selected_league_name

    return render_template(
        'season_rankings/index.html',
        seasons=session.get('seasons'), selected_year=session.get('selected_year'),
        leagues=session.get('leagues'), selected_league_name=selected_league_name,
        types=RANKING_TYPES, selected_type=None, season_rankings=None
    )


@blueprint.route('select_type', methods=['POST'])
def select_type() -> Response | str:
    templates = {
        'Offense': 'season_rankings.offense',
        'Defense': 'season_rankings.defense',
        'Total': 'season_rankings.total',
    }
    selected_type = str(request.form.get('ranking_type_dropdown'))
    session['selected_type'] = selected_type

    # Fetch the selected type.
    if selected_type in RANKING_TYPES:
        return redirect(url_for(templates[selected_type]))
    else:
        raise TypeError('Invalid ranking type')


@blueprint.route('/offense')
def offense() -> str:
    season_rankings_repository = injector.get(SeasonRankingsRepository)
    selected_year = session.get('selected_year')
    season_rankings = season_rankings_repository.get_offensive_rankings_by_season_year(selected_year)

    return _render_rankings_template('offense',
                                     selected_year=selected_year, season_rankings=season_rankings)


@blueprint.route('/defense')
def defense() -> str:
    season_rankings_repository = injector.get(SeasonRankingsRepository)
    selected_year = session.get('selected_year')
    season_rankings = season_rankings_repository.get_defensive_rankings_by_season_year(selected_year)

    return _render_rankings_template('defense',
                                     selected_year=selected_year, season_rankings=season_rankings)


@blueprint.route('/total')
def total() -> str:
    season_rankings_repository = injector.get(SeasonRankingsRepository)
    selected_year = session.get('selected_year')
    season_rankings = season_rankings_repository.get_total_rankings_by_season_year(selected_year)

    return _render_rankings_template('total',
                                     selected_year=selected_year, season_rankings=season_rankings)


def _render_rankings_template(rankings_type: str, selected_year: int, season_rankings: list) -> str:
    return render_template(
        f'season_rankings/{rankings_type}.html',
        seasons=session.get('seasons'), selected_year=selected_year,
        leagues=session.get('leagues'), selected_league_name=session.get('selected_league_name'),
        types=RANKING_TYPES, selected_type=session.get('selected_type'), season_rankings=season_rankings
    )


@blueprint.route('weekly_update', methods=['POST'])
def run_weekly_update():
    weekly_update_service = injector.get(WeeklyUpdateService)
    selected_league_name = session.get('selected_league_name')
    selected_year = session.get('selected_year')
    weekly_update_service.run_weekly_update(selected_league_name, selected_year)

    flash(
        f"The weekly update has been successfully completed for the '{selected_league_name}' in {selected_year}.",
        'success'
    )
    return render_template(
        'season_rankings/index.html',
        seasons=session.get('seasons'), selected_year=selected_year,
        leagues=session.get('leagues'), selected_league_name=selected_league_name,
        types=RANKING_TYPES, selected_type=session.get('selected_type'), season_rankings=None
    )
