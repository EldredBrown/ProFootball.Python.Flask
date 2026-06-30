from typing import List

from flask import Blueprint, abort, render_template, request, session, flash

from app import injector
from app.data.models.league import League
from app.data.repositories.league_repository import LeagueRepository
from app.data.repositories.season_repository import SeasonRepository
from app.data.repositories.team_season_repository import TeamSeasonRepository
from app.data.repositories.team_season_schedule_repository import TeamSeasonScheduleRepository
from app.services.weekly_update_service.weekly_update_service import WeeklyUpdateService

blueprint = Blueprint('team_season', __name__)

RANKING_TYPES = ['Offense', 'Defense', 'Total']


@blueprint.route('/')
def index() -> str:
    if 'seasons' in session:
        seasons = session.get('seasons')
    else:
        season_repository = injector.get(SeasonRepository)
        seasons = [s.to_dict() for s in season_repository.get_seasons()]
        session['seasons'] = seasons

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

    team_season_repository = injector.get(TeamSeasonRepository)
    team_seasons = team_season_repository.get_team_seasons_by_season(season_id=selected_season_year)
    session['team_seasons'] = [ts.to_dict() for ts in team_seasons]

    return render_template(
        'team_seasons/index.html',
        seasons=seasons, selected_season_year=selected_season_year, leagues=session.get('leagues'),
        selected_league_name=selected_league_name, team_seasons=team_seasons
    )


@blueprint.route('/select_season', methods=['POST'])
def select_season() -> str:
    selected_season_year = int(request.form.get('season_dropdown'))
    session['selected_season_year'] = selected_season_year

    leagues_active_in_selected_season = _get_leagues_active_in_selected_season(selected_season_year)
    session['leagues'] = [l.to_dict() for l in leagues_active_in_selected_season]

    team_season_repository = injector.get(TeamSeasonRepository)
    team_seasons = team_season_repository.get_team_seasons_by_season(season_id=selected_season_year)
    session['team_seasons'] = [ts.to_dict() for ts in team_seasons]

    return render_template(
        'team_seasons/index.html',
        seasons=session.get('seasons'), selected_season_year=selected_season_year, leagues=leagues_active_in_selected_season,
        selected_league_name=session.get('selected_league_name'), team_seasons=team_seasons
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
        'team_seasons/index.html',
        seasons=session.get('seasons'), selected_season_year=session.get('selected_season_year'),
        leagues=session.get('leagues'), selected_league_name=selected_league_name, team_seasons=team_seasons
    )


@blueprint.route('/details/<int:id>')
def details(id: int) -> str:
    try:
        team_season_repository = injector.get(TeamSeasonRepository)
        team_season = team_season_repository.get_team_season(id)

        team_season_schedule_repository = injector.get(TeamSeasonScheduleRepository)
        team_season_schedule_profile = team_season_schedule_repository.get_team_season_schedule_profile(
            team_season.team_id, team_season.season_id
        )
        team_season_schedule_totals = [team_season_schedule_repository.get_team_season_schedule_totals(
            team_season.team_id, team_season.season_id
        )]
        team_season_schedule_averages = [team_season_schedule_repository.get_team_season_schedule_averages(
            team_season.team_id, team_season.season_id
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


@blueprint.route('weekly_update', methods=['POST'])
def run_weekly_update():
    weekly_update_service = injector.get(WeeklyUpdateService)

    selected_league_name = session.get('selected_league_name')
    league_repository = injector.get(LeagueRepository)
    selected_league = league_repository.get_league_by_short_name(selected_league_name)

    selected_season_year = session.get('selected_season_year')

    weekly_update_service.run_weekly_update(selected_league.id, selected_season_year)

    flash(
        f"The weekly update has been successfully completed for the '{selected_league_name}' in {selected_season_year}.",
        'success'
    )
    return render_template(
        'team_seasons/index.html',
        seasons=session.get('seasons'), selected_season_year=selected_season_year,
        leagues=session.get('leagues'), selected_league_name=selected_league_name,
        team_seasons=session.get('team_seasons')
    )
