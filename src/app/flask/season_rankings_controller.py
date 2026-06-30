from typing import List

from flask import Blueprint, render_template, request, url_for, redirect, Response, session

from app import injector
from app.data.models.league import League
from app.data.repositories.league_repository import LeagueRepository
from app.data.repositories.season_rankings_repository import SeasonRankingsRepository
from app.data.repositories.season_repository import SeasonRepository
from app.data.repositories.team_season_repository import TeamSeasonRepository

blueprint = Blueprint('season_rankings', __name__)

RANKING_TYPES = ['Offense', 'Defense', 'Total']


@blueprint.route('/')
def index() -> str:
    if 'seasons' in session:
        seasons = session.get('seasons')
    else:
        season_repository = injector.get(SeasonRepository)
        seasons = season_repository.get_seasons()
        session['seasons'] = [s.to_dict() for s in seasons]

    if 'selected_season_year' in session:
        selected_season_year = int(session.get('selected_season_year'))
    else:
        selected_season_year = -1
        session['selected_season_year'] = selected_season_year

    leagues_active_in_selected_season = _get_leagues_active_in_selected_season(selected_season_year)
    session['leagues'] = [l.to_dict() for l in leagues_active_in_selected_season]

    if 'selected_league_name' in session:
        selected_league_name = session.get('selected_league_name')
    else:
        selected_league_name = ''
        session['selected_league_name'] = selected_league_name

    selected_type = None

    return render_template(
        'season_rankings/index.html',
        seasons=seasons, selected_season_year=selected_season_year,
        leagues=session.get('leagues'), selected_league_name=selected_league_name,
        types=RANKING_TYPES, selected_type=selected_type, season_rankings=None
    )


@blueprint.route('select_season', methods=['POST'])
def select_season() -> str:
    selected_season_year = int(request.form.get('season_dropdown'))
    session['selected_season_year'] = selected_season_year

    leagues_active_in_selected_season = _get_leagues_active_in_selected_season(selected_season_year)
    session['leagues'] = [l.to_dict() for l in leagues_active_in_selected_season]

    return render_template(
        'season_rankings/index.html',
        seasons=session.get('seasons'), selected_season_year=selected_season_year,
        leagues=leagues_active_in_selected_season, selected_league_name=None,
        types=RANKING_TYPES, selected_type=None, season_rankings=None
    )


def _get_leagues_active_in_selected_season(selected_season_year: int = None) -> List[League]:
    league_repository = injector.get(LeagueRepository)
    leagues = league_repository.get_leagues()
    leagues_active_in_selected_season = [
        l for l in leagues
        if selected_season_year >= l.first_season_id and (
                l.last_season_id is None or selected_season_year <= l.last_season_id
        )
    ]
    return leagues_active_in_selected_season


@blueprint.route('select_league', methods=['POST'])
def select_league() -> str:
    selected_league_name = str(request.form.get('league_dropdown'))  # Fetch the selected league.
    session['selected_league_name'] = selected_league_name

    selected_season_year = session.get('selected_season_year')

    team_season_repository = injector.get(TeamSeasonRepository)
    team_seasons = team_season_repository.get_team_seasons_by_season(season_id=selected_season_year)
    team_seasons = [ts for ts in team_seasons if ts.league.short_name == selected_league_name]
    session['team_seasons'] = [ts.to_dict() for ts in team_seasons]

    return render_template(
        'season_rankings/index.html',
        seasons=session.get('seasons'), selected_year=session.get('selected_season_year'),
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
    selected_season_year = session.get('selected_season_year')
    season_rankings = season_rankings_repository.get_offensive_rankings_by_season(season_id=selected_season_year)

    return _render_rankings_template(
        'offense',
        selected_season_year=selected_season_year, season_rankings=season_rankings
    )


@blueprint.route('/defense')
def defense() -> str:
    season_rankings_repository = injector.get(SeasonRankingsRepository)
    selected_season_year = session.get('selected_season_year')
    season_rankings = season_rankings_repository.get_defensive_rankings_by_season(season_id=selected_season_year)

    return _render_rankings_template(
        'defense',
        selected_season_year=selected_season_year, season_rankings=season_rankings
    )


@blueprint.route('/total')
def total() -> str:
    season_rankings_repository = injector.get(SeasonRankingsRepository)
    selected_season_year = session.get('selected_season_year')
    season_rankings = season_rankings_repository.get_total_rankings_by_season(season_id=selected_season_year)

    return _render_rankings_template(
        'total',
        selected_season_year=selected_season_year, season_rankings=season_rankings
    )


def _render_rankings_template(rankings_type: str, selected_season_year: int, season_rankings: list) -> str:
    return render_template(
        f'season_rankings/{rankings_type}.html',
        seasons=session.get('seasons'), selected_season_year=selected_season_year,
        leagues=session.get('leagues'), selected_league_name=session.get('selected_league_name'),
        types=RANKING_TYPES, selected_type=session.get('selected_type'), season_rankings=season_rankings
    )
