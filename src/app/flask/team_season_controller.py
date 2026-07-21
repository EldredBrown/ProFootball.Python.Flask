from typing import List, Any

from flask import Blueprint, abort, render_template, request, session, flash

from app import injector
from app.data.models.association import Association
from app.data.models.season import Season
from app.data.models.team_season import TeamSeason
from app.data.repositories.association_repository import AssociationRepository
from app.data.repositories.season_repository import SeasonRepository
from app.data.repositories.team_season_repository import TeamSeasonRepository
from app.data.repositories.team_season_schedule_repository import TeamSeasonScheduleRepository
from app.services.weekly_update_service.weekly_update_service import WeeklyUpdateService

blueprint = Blueprint('team_season', __name__)

RANKING_TYPES = ['Offense', 'Defense', 'Total']


@blueprint.route('/')
def index() -> str:
    seasons, selected_season_year = _get_seasons_and_selected_season_year()
    active_leagues, selected_league = _get_leagues_and_selected_league(selected_season_year)
    team_seasons = _get_team_seasons(selected_season_year)

    return render_template(
        'team_seasons/index.html',
        seasons=seasons, selected_season_year=selected_season_year,
        leagues=active_leagues, selected_league_name=selected_league.short_name,
        team_seasons=team_seasons
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


@blueprint.route('/details/<int:id>')
def details(id: int) -> str:
    try:
        team_season_repository = injector.get(TeamSeasonRepository)
        team_season = team_season_repository.get_team_season(id)

        team_season_schedule_repository = injector.get(TeamSeasonScheduleRepository)
        team_season_schedule_profile = team_season_schedule_repository.get_team_season_schedule_profile(
            team_season.team_id, team_season.season_year
        )
        team_season_schedule_totals = [team_season_schedule_repository.get_team_season_schedule_totals(
            team_season.team_id, team_season.season_year
        )]
        team_season_schedule_averages = [team_season_schedule_repository.get_team_season_schedule_averages(
            team_season.team_id, team_season.season_year
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
def select_season() -> str:
    selected_season_year = int(request.form.get('season_dropdown'))

    seasons = session.get('seasons')
    session['selected_season_year'] = selected_season_year

    active_leagues, selected_league = _get_leagues_and_set_selected_league(selected_season_year)
    team_seasons = _get_team_seasons(selected_season_year)

    return render_template(
        'team_seasons/index.html',
        seasons=seasons, selected_season_year=selected_season_year,
        leagues=active_leagues, selected_league_name=selected_league.short_name,
        team_seasons=team_seasons
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

    team_seasons = _get_team_seasons(selected_season_year)

    return render_template(
        'team_seasons/index.html',
        seasons=seasons, selected_season_year=selected_season_year,
        leagues=active_leagues, selected_league_name=selected_league.short_name,
        team_seasons=team_seasons
    )


def _get_team_seasons(selected_season_year: int) -> list[TeamSeason]:
    team_season_repository = injector.get(TeamSeasonRepository)
    team_seasons = team_season_repository.get_team_seasons_by_season(season_year=selected_season_year)
    session['team_seasons'] = [ts.to_dict() for ts in team_seasons]
    return team_seasons


@blueprint.route('weekly_update', methods=['POST'])
def run_weekly_update():
    weekly_update_service = injector.get(WeeklyUpdateService)

    seasons = session.get('seasons')
    selected_season_year = int(session.get('selected_season_year'))

    leagues = session.get('leagues')
    selected_league_name = str(session.get('selected_league_name'))

    association_repository = injector.get(AssociationRepository)
    selected_league = association_repository.get_association_by_short_name(selected_league_name)

    team_seasons = session.get('team_seasons')

    weekly_update_service.run_weekly_update(selected_league.id, selected_season_year)

    flash(
        f"The weekly update has been successfully completed for the '{selected_league_name}' in {selected_season_year}.",
        'success'
    )
    return render_template(
        'team_seasons/index.html',
        seasons=seasons, selected_season_year=selected_season_year,
        leagues=leagues, selected_league_name=selected_league_name,
        team_seasons=team_seasons
    )
