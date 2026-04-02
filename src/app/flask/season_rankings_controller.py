from flask import Blueprint, render_template, request, url_for, redirect, flash, Response, session
from injector import inject

from app.data.repositories.league_repository import LeagueRepository
from app.data.repositories.season_rankings_repository import SeasonRankingsRepository
from app.data.repositories.season_repository import SeasonRepository
from app.services.weekly_update_service.weekly_update_service import WeeklyUpdateService

blueprint = Blueprint('season_rankings', __name__)

RANKING_TYPES = ['Offense', 'Defense', 'Total']


@blueprint.route('/')
@inject
def index(season_repository: SeasonRepository, league_repository: LeagueRepository) -> str:
    session['seasons'] = season_repository.get_seasons()
    session['leagues'] = league_repository.get_leagues()

    return render_template(
        'season_rankings/index.html',
        seasons=session.get('seasons'), selected_year=session.get('selected_year'),
        leagues=session.get('leagues'), selected_league_name=session.get('selected_league_name'),
        types=RANKING_TYPES, selected_type=session.get('selected_type'), season_rankings=None
    )


@blueprint.route('select_season', methods=['POST'])
def select_season():
    session['selected_year'] = int(request.form.get('season_dropdown'))  # Fetch the selected season.
    return render_template(
        'season_rankings/index.html',
        seasons=session.get('seasons'), selected_year=session.get('selected_year'),
        leagues=session.get('leagues'), selected_league_name=session.get('selected_league_name'),
        types=RANKING_TYPES, selected_type=session.get('selected_type'), season_rankings=None
    )


@blueprint.route('select_league', methods=['POST'])
def select_league():
    session['selected_league_name'] = str(request.form.get('league_dropdown'))  # Fetch the selected league.
    return render_template(
        'season_rankings/index.html',
        seasons=session.get('seasons'), selected_year=session.get('selected_year'),
        leagues=session.get('leagues'), selected_league_name=session.get('selected_league_name'),
        types=RANKING_TYPES, selected_type=session.get('selected_type'), season_rankings=None
    )


@blueprint.route('select_type', methods=['POST'])
def select_type() -> Response | str:
    templates = {
        'Offense': 'season_rankings.offense',
        'Defense': 'season_rankings.defense',
        'Total': 'season_rankings.total',
    }
    session['selected_type'] = str(request.form.get('ranking_type_dropdown'))
    # Fetch the selected type.
    selected_type = session.get('selected_type')
    if selected_type in RANKING_TYPES:
        return redirect(url_for(templates[selected_type]))
    else:
        raise TypeError('Invalid ranking type')


@blueprint.route('weekly_update', methods=['POST'])
@inject
def run_weekly_update(weekly_update_service: WeeklyUpdateService):
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


@blueprint.route('/offense')
@inject
def offense(season_rankings_repository: SeasonRankingsRepository):
    selected_year = session.get('selected_year')
    season_rankings = season_rankings_repository.get_offensive_rankings_by_season_year(selected_year)
    return render_template(
        'season_rankings/offense.html',
        seasons=session.get('seasons'), selected_year=selected_year,
        leagues=session.get('leagues'), selected_league_name=session.get('selected_league_name'),
        types=RANKING_TYPES, selected_type=session.get('selected_type'), season_rankings=season_rankings
    )


@blueprint.route('/defense')
@inject
def defense(season_rankings_repository: SeasonRankingsRepository):
    selected_year = session.get('selected_year')
    season_rankings = season_rankings_repository.get_defensive_rankings_by_season_year(selected_year)
    return render_template(
        'season_rankings/defense.html',
        seasons=session.get('seasons'), selected_year=selected_year,
        leagues=session.get('leagues'), selected_league_name=session.get('selected_league_name'),
        types=RANKING_TYPES, selected_type=session.get('selected_type'), season_rankings=season_rankings
    )


@blueprint.route('/total')
@inject
def total(season_rankings_repository: SeasonRankingsRepository):
    selected_year = session.get('selected_year')
    season_rankings = season_rankings_repository.get_total_rankings_by_season_year(selected_year)
    return render_template(
        'season_rankings/total.html',
        seasons=session.get('seasons'), selected_year=selected_year,
        leagues=session.get('leagues'), selected_league_name=session.get('selected_league_name'),
        types=RANKING_TYPES, selected_type=session.get('selected_type'), season_rankings=season_rankings
    )
