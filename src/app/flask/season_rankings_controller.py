from typing import List, Any

from flask import Blueprint, render_template, request, url_for, redirect, Response, session

from app import injector
from app.data.models.association import Association
from app.data.models.season import Season
from app.data.repositories.association_repository import AssociationRepository
from app.data.repositories.season_rankings_repository import SeasonRankingsRepository
from app.data.repositories.season_repository import SeasonRepository

blueprint = Blueprint('season_rankings', __name__)

RANKING_TYPES = ['Offense', 'Defense', 'Total']


@blueprint.route('/')
def index() -> str:
    seasons, selected_season_year = _get_seasons_and_selected_season_year()
    active_leagues, selected_league = _get_leagues_and_selected_league(selected_season_year)

    selected_type = None

    return render_template(
        'season_rankings/index.html',
        seasons=seasons, selected_season_year=selected_season_year,
        leagues=active_leagues, selected_league_name=selected_league.short_name,
        types=RANKING_TYPES, selected_type=selected_type, season_rankings=None
    )


def _get_seasons_and_selected_season_year() -> tuple[list[Season], int]:
    seasons = _get_seasons()

    selected_season = seasons[0]

    selected_season_year = session.get('selected_season_year')
    if selected_season_year is None:
        selected_season_year = selected_season.year
        session['selected_season_year'] = selected_season_year

    return seasons, selected_season_year


def _get_seasons() -> list[Season]:
    season_repository = injector.get(SeasonRepository)
    seasons = season_repository.get_seasons()
    seasons.sort(key=lambda s: s.year, reverse=True)
    session['seasons'] = [s.to_dict() for s in seasons]

    return seasons


def _get_leagues_and_selected_league(selected_season_year: int) -> tuple[list[Association], Association]:
    active_leagues, selected_league = _get_leagues(selected_season_year)

    selected_league_name = session.get('selected_league_name')
    if selected_league_name is None or selected_league_name == '':
        session['selected_league_name'] = selected_league.short_name

    return active_leagues, selected_league


@blueprint.route('select_season', methods=['POST'])
def select_season() -> str:
    selected_season_year = int(request.form.get('season_dropdown'))

    seasons = session.get('seasons')
    session['selected_season_year'] = selected_season_year

    active_leagues, selected_league = _get_leagues_and_set_selected_league(selected_season_year)

    return render_template(
        'season_rankings/index.html',
        seasons=seasons, selected_season_year=selected_season_year,
        leagues=active_leagues, selected_league_name=None,
        types=RANKING_TYPES, selected_type=None, season_rankings=None
    )


def _get_leagues_and_set_selected_league(selected_season_year: Any) -> tuple[list[Association], Association]:
    active_leagues, selected_league = _get_leagues(selected_season_year)

    session['selected_league_name'] = selected_league.short_name

    return active_leagues, selected_league


def _get_leagues(selected_season_year: int) -> tuple[list[Association], Association]:
    association_repository = injector.get(AssociationRepository)
    associations = association_repository.get_associations()
    leagues = [a for a in associations if a.parent_id is None]
    active_leagues = [l for l in leagues if l.first_season_year <= selected_season_year
                      and (l.last_season is None or selected_season_year <= l.last_season_year)]
    active_leagues.sort(key=lambda l: l.id, reverse=True)
    session['leagues'] = [l.to_dict() for l in active_leagues]

    selected_league = active_leagues[0]

    return active_leagues, selected_league


@blueprint.route('select_league', methods=['POST'])
def select_league() -> str:
    selected_league_name = str(request.form.get('league_dropdown'))  # Fetch the selected league.

    seasons = session.get('seasons')
    selected_season_year = int(session.get('selected_season_year'))

    active_leagues = session.get('leagues')
    session['selected_league_name'] = selected_league_name

    kwargs = [l for l in active_leagues if l['short_name'] == selected_league_name][0]
    selected_league = Association(**kwargs)

    return render_template(
        'season_rankings/index.html',
        seasons=seasons, selected_year=selected_season_year,
        leagues=active_leagues, selected_league_name=selected_league.short_name,
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
    season_rankings = season_rankings_repository.get_offensive_rankings_by_season(season_year=selected_season_year)

    return _render_rankings_template(
        'offense',
        selected_season_year=selected_season_year, season_rankings=season_rankings
    )


@blueprint.route('/defense')
def defense() -> str:
    season_rankings_repository = injector.get(SeasonRankingsRepository)
    selected_season_year = session.get('selected_season_year')
    season_rankings = season_rankings_repository.get_defensive_rankings_by_season(season_year=selected_season_year)

    return _render_rankings_template(
        'defense',
        selected_season_year=selected_season_year, season_rankings=season_rankings
    )


@blueprint.route('/total')
def total() -> str:
    season_rankings_repository = injector.get(SeasonRankingsRepository)
    selected_season_year = session.get('selected_season_year')
    season_rankings = season_rankings_repository.get_total_rankings_by_season(season_year=selected_season_year)

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
