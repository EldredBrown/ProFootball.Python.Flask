from flask import Blueprint, render_template, flash, request, session, jsonify

from app import injector
from app.data.repositories.season_repository import SeasonRepository
from app.data.repositories.team_season_repository import TeamSeasonRepository
from app.services.game_predictor_service.game_predictor_service import GamePredictorService

blueprint = Blueprint('game_predictor', __name__)


@blueprint.route('/')
def index() -> str:
    season_repository = injector.get(SeasonRepository)

    seasons = [s.to_dict() for s in season_repository.get_seasons()]

    session['guest_seasons'] = seasons

    selected_guest_season_year = None
    session['selected_guest_season_year'] = selected_guest_season_year

    selected_guest_name = None
    session['selected_guest_name'] = selected_guest_name

    session['host_seasons'] = seasons

    selected_host_season_year = None
    session['selected_host_season_year'] = selected_host_season_year

    selected_host_name = None
    session['selected_host_name'] = selected_host_name

    return render_template(
        'game_predictor/index.html',
        guest_seasons=seasons, selected_guest_season_year=selected_guest_season_year,
        guests=[], selected_guest_name=selected_guest_name,
        host_seasons=seasons, selected_host_season_year=selected_host_season_year,
        hosts=[], selected_host_name=selected_host_name
    )


@blueprint.route('/select_guest_season', methods=['POST'])
def select_guest_season() -> str:
    selected_guest_season_year = int(request.form.get('guest_season_dropdown')) # Fetch the selected guest season.
    session['selected_guest_season_year'] = selected_guest_season_year

    team_season_repository = injector.get(TeamSeasonRepository)

    guests = team_season_repository.get_team_seasons_by_season(season_year=selected_guest_season_year)

    selected_host_season_year = session.get('selected_host_season_year')
    hosts = team_season_repository.get_team_seasons_by_season(season_year=selected_host_season_year)

    return render_template(
        'game_predictor/index.html',
        guest_seasons=session.get('guest_seasons'), selected_guest_season_year=selected_guest_season_year,
        guests=guests, selected_guest_name=None,
        host_seasons=session.get('host_seasons'), selected_host_season_year=selected_host_season_year,
        hosts=hosts, selected_host_name=session.get('selected_host_name')
    )


@blueprint.route('/select_guest', methods=['POST'])
def select_guest():
    selected_guest_name = str(request.form.get('guest_dropdown'))
    session['selected_guest_name'] = selected_guest_name

    team_season_repository = injector.get(TeamSeasonRepository)

    selected_guest_season_year = session.get('selected_guest_season_year')
    guests = team_season_repository.get_team_seasons_by_season(season_year=selected_guest_season_year)

    selected_host_season_year = session.get('selected_host_season_year')
    hosts = team_season_repository.get_team_seasons_by_season(season_year=selected_host_season_year)

    return render_template(
        'game_predictor/index.html',
        guest_seasons=session.get('guest_seasons'), selected_guest_season_year=selected_guest_season_year,
        guests=guests, selected_guest_name=selected_guest_name,
        host_seasons=session.get('host_seasons'), selected_host_season_year=selected_host_season_year,
        hosts=hosts, selected_host_name=session.get('selected_host_name')
    )


@blueprint.route('/select_host_season', methods=['POST'])
def select_host_season() -> str:
    selected_host_season_year = int(request.form.get('host_season_dropdown')) # Fetch the selected guest season.
    session['selected_host_season_year'] = selected_host_season_year

    team_season_repository = injector.get(TeamSeasonRepository)

    selected_guest_season_year = session.get('selected_guest_season_year')
    guests = team_season_repository.get_team_seasons_by_season(season_year=selected_guest_season_year)

    hosts = team_season_repository.get_team_seasons_by_season(season_year=selected_host_season_year)

    return render_template(
        'game_predictor/index.html',
        guest_seasons=session.get('guest_seasons'), selected_guest_season_year=selected_guest_season_year,
        guests=guests, selected_guest_name=session.get('selected_guest_name'),
        host_seasons=session.get('host_seasons'), selected_host_season_year=selected_host_season_year,
        hosts=hosts, selected_host_name=None
    )


@blueprint.route('/select_host', methods=['POST'])
def select_host():
    selected_host_name = str(request.form.get('host_dropdown'))
    session['selected_host_name'] = selected_host_name

    team_season_repository = injector.get(TeamSeasonRepository)

    selected_guest_season_year = session.get('selected_guest_season_year')
    guests = team_season_repository.get_team_seasons_by_season(season_year=selected_guest_season_year)

    selected_host_season_year = session.get('selected_host_season_year')
    hosts = team_season_repository.get_team_seasons_by_season(season_year=selected_host_season_year)

    return render_template(
        'game_predictor/index.html',
        guest_seasons=session.get('guest_seasons'), selected_guest_season_year=selected_guest_season_year,
        guests=guests, selected_guest_name=session.get('selected_guest_name'),
        host_seasons=session.get('host_seasons'), selected_host_season_year=selected_host_season_year,
        hosts=hosts, selected_host_name=selected_host_name
    )


@blueprint.route('/predict_game')
def predict_game() -> str:
    team_season_repository = injector.get(TeamSeasonRepository)

    guest_seasons = session.get('guest_seasons')
    selected_guest_season_year = session.get('selected_guest_season_year')
    guests = team_season_repository.get_team_seasons_by_season(season_year=selected_guest_season_year)
    selected_guest_name = session.get('selected_guest_name')

    host_seasons = session.get('host_seasons')
    selected_host_season_year = session.get('selected_host_season_year')
    hosts = team_season_repository.get_team_seasons_by_season(season_year=selected_host_season_year)
    selected_host_name = session.get('selected_host_name')

    if selected_guest_season_year is None:
        return _handle_error(message="Please select one guest season.")
    if selected_guest_name is None:
        return _handle_error(message="Please select one guest name.")
    if selected_host_season_year is None:
        return _handle_error(message="Please select one host season.")
    if selected_host_name is None:
        return _handle_error(message="Please select one host name.")

    game_predictor_service = injector.get(GamePredictorService)
    try:
        guest_score, host_score = game_predictor_service.predict_game_score(
            selected_guest_name, selected_guest_season_year, selected_host_name, selected_host_season_year
        )
    except:
        flash("A prediction could not be calculated.", "danger")

        return render_template(
            'game_predictor/index.html',
            guest_seasons=guest_seasons, selected_guest_season_year=selected_guest_season_year,
            guests=guests, selected_guest_name=selected_guest_name,
            host_seasons=host_seasons, selected_host_season_year=selected_host_season_year,
            hosts=hosts, selected_host_name=selected_host_name
        )

    flash(
        f"Game score predicted successfully. "
        f"{selected_guest_name} - {round(guest_score, 0)}, {selected_host_name} - {round(host_score, 0)}",
        'success'
    )

    return render_template(
        'game_predictor/index.html',
        guest_seasons=guest_seasons, selected_guest_season_year=selected_guest_season_year,
        guests=guests, selected_guest_name=selected_guest_name,
        host_seasons=host_seasons, selected_host_season_year=selected_host_season_year,
        hosts=hosts, selected_host_name=selected_host_name
    )


def _handle_error(message: str) -> str:
    flash(message, 'danger')
    return render_template(
        'game_predictor/index.html',
        guest_seasons=session.get('guest_seasons'), selected_guest_season_year=session.get('selected_guest_season_year'),
        guests=session.get('guests'), selected_guest_name=session.get('selected_guest_name'),
        host_seasons=session.get('host_seasons'), selected_host_season_year=session.get('selected_host_season_year'),
        hosts=session.get('hosts'), selected_host_name=session.get('selected_host_name')
    )
