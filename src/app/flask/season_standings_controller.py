from typing import Any

from flask import Blueprint, render_template, request, session

from app import injector
from app.data.models.association import Association
from app.data.models.season import Season
from app.data.repositories import season_standings_repository
from app.data.repositories.association_repository import AssociationRepository
from app.data.repositories.season_repository import SeasonRepository

blueprint = Blueprint('season_standings', __name__)


@blueprint.route('/')
def index() -> str:
    seasons, selected_season_year = _get_seasons_and_selected_season_year()
    active_leagues, selected_league = _get_leagues_and_selected_league(selected_season_year)

    season_standings = []
    return render_template(
        'season_standings/index.html',
        seasons=seasons, selected_season_year=selected_season_year,
        leagues=active_leagues, selected_league_name=selected_league.short_name,
        season_standings=season_standings
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


@blueprint.route('/select_season', methods=['POST'])
def select_season() -> str:
    selected_season_year = int(request.form.get('season_dropdown'))

    seasons = session.get('seasons')
    session['selected_season_year'] = selected_season_year

    active_leagues, selected_league = _get_leagues_and_set_selected_league(selected_season_year)

    return render_template(
        'season_standings/index.html',
        seasons=seasons, selected_season_year=selected_season_year,
        leagues=active_leagues, selected_league_name=selected_league.short_name,
        season_standings=[]
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


@blueprint.route('/select_league', methods=['POST'])
def select_league() -> str:
    selected_league_name = str(request.form.get('league_dropdown'))  # Fetch the selected league.

    seasons = session.get('seasons')
    selected_season_year = session.get('selected_season_year')

    active_leagues = session.get('leagues')
    session['selected_league_name'] = selected_league_name

    kwargs = [l for l in active_leagues if l['short_name'] == selected_league_name][0]
    selected_league = Association(**kwargs)

    season_standings = season_standings_repository.get_season_standings(
        season_year=selected_season_year, league_id=selected_league.id
    )

    return render_template(
        'season_standings/index.html',
        seasons=seasons, selected_season_year=selected_season_year,
        leagues=active_leagues, selected_league_name=selected_league.short_name,
        season_standings=season_standings
    )
