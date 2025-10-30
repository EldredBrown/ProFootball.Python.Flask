from flask import Blueprint, render_template, flash, request

from app.data.repositories.season_repository import SeasonRepository
from app.data.repositories.team_season_repository import TeamSeasonRepository
from app.services.game_predictor_service.game_predictor_service import GamePredictorService

blueprint = Blueprint('game_predictor', __name__)

season_repository = SeasonRepository()
team_season_repository = TeamSeasonRepository()

guest_seasons = None
selected_guest_year = None
guests = None
selected_guest_name = None

host_seasons = None
selected_host_year = None
hosts = None
selected_host_name = None


@blueprint.route('/')
def index():
    global guest_seasons
    global selected_guest_year
    global guests
    global selected_guest_name

    global host_seasons
    global selected_host_year
    global hosts
    global selected_host_name

    guest_seasons = season_repository.get_seasons()
    selected_guest_year = None

    guests = []
    selected_guest_name = None

    host_seasons = season_repository.get_seasons()
    selected_host_year = None

    hosts = []
    selected_host_name = None

    return render_template(
        'game_predictor/index.html',
        guest_seasons=guest_seasons, selected_guest_year=selected_guest_year,
        guests=guests, selected_guest_name=selected_guest_name,
        host_seasons=host_seasons, selected_host_year=selected_host_year,
        hosts=hosts, selected_host_name=selected_host_name
    )

@blueprint.route('/select_guest_season', methods=['POST'])
def select_guest_season():
    global guest_seasons
    global selected_guest_year
    global guests
    global selected_guest_name

    global host_seasons
    global selected_host_year
    global hosts
    global selected_host_name

    selected_guest_year = int(request.form.get('guest_season_dropdown'))  # Fetch the selected guest season.
    guests = team_season_repository.get_team_seasons_by_season_year(season_year=selected_guest_year)
    return render_template(
        'game_predictor/index.html',
        guest_seasons=guest_seasons, selected_guest_year=selected_guest_year,
        guests=guests, selected_guest_name=selected_guest_name,
        host_seasons=host_seasons, selected_host_year=selected_host_year,
        hosts=hosts, selected_host_name=selected_host_name
    )


@blueprint.route('/select_guest', methods=['POST'])
def select_guest():
    global guest_seasons
    global selected_guest_year
    global guests
    global selected_guest_name

    global host_seasons
    global selected_host_year
    global hosts
    global selected_host_name

    selected_guest_name = str(request.form.get('guest_dropdown'))
    return render_template(
        'game_predictor/index.html',
        guest_seasons=guest_seasons, selected_guest_year=selected_guest_year,
        guests=guests, selected_guest_name=selected_guest_name,
        host_seasons=host_seasons, selected_host_year=selected_host_year,
        hosts=hosts, selected_host_name=selected_host_name
    )


@blueprint.route('/select_host_season', methods=['POST'])
def select_host_season():
    global guest_seasons
    global selected_guest_year
    global guests
    global selected_guest_name

    global host_seasons
    global selected_host_year
    global hosts
    global selected_host_name

    selected_host_year = int(request.form.get('host_season_dropdown'))  # Fetch the selected host season.
    hosts = team_season_repository.get_team_seasons_by_season_year(season_year=selected_host_year)
    return render_template(
        'game_predictor/index.html',
        guest_seasons=guest_seasons, selected_guest_year=selected_guest_year,
        guests=guests, selected_guest_name=selected_guest_name,
        host_seasons=host_seasons, selected_host_year=selected_host_year,
        hosts=hosts, selected_host_name=selected_host_name
    )


@blueprint.route('/select_host', methods=['POST'])
def select_host():
    global guest_seasons
    global selected_guest_year
    global guests
    global selected_guest_name

    global host_seasons
    global selected_host_year
    global hosts
    global selected_host_name

    selected_host_name = str(request.form.get('host_dropdown'))  # Fetch the selected host season.
    return render_template(
        'game_predictor/index.html',
        guest_seasons=guest_seasons, selected_guest_year=selected_guest_year,
        guests=guests, selected_guest_name=selected_guest_name,
        host_seasons=host_seasons, selected_host_year=selected_host_year,
        hosts=hosts, selected_host_name=selected_host_name
    )


@blueprint.route('/predict_game')
def predict_game():
    global guest_seasons
    global selected_guest_year
    global guests
    global selected_guest_name

    global host_seasons
    global selected_host_year
    global hosts
    global selected_host_name

    if selected_guest_year is None:
        return _handle_error(message="Please select one guest season.")
    if selected_guest_name is None:
        return _handle_error(message="Please select one guest name.")
    if selected_host_year is None:
        return _handle_error(message="Please select one host season.")
    if selected_host_name is None:
        return _handle_error(message="Please select one host name.")

    game_predictor_service = GamePredictorService()
    try:
        guest_score, host_score = game_predictor_service.predict_game_score(
            selected_guest_name, selected_guest_year, selected_host_name, selected_host_year
        )
    except:
        flash("The prediction could not be calculated.", "danger")

        return render_template(
            'game_predictor/index.html',
            guest_seasons=guest_seasons, selected_guest_year=selected_guest_year,
            guests=guests, selected_guest_name=selected_guest_name,
            host_seasons=host_seasons, selected_host_year=selected_host_year,
            hosts=hosts, selected_host_name=selected_host_name
        )

    flash(
        f"Game score predicted successfully. "
        f"{selected_guest_name} - {round(guest_score, 0)}, {selected_host_name} - {round(host_score, 0)}",
        'success'
    )

    return render_template(
        'game_predictor/index.html',
        guest_seasons=guest_seasons, selected_guest_year=selected_guest_year,
        guests=guests, selected_guest_name=selected_guest_name,
        host_seasons=host_seasons, selected_host_year=selected_host_year,
        hosts=hosts, selected_host_name=selected_host_name
    )


def _handle_error(message: str):
    global guest_seasons
    global selected_guest_year
    global guests
    global selected_guest_name

    global host_seasons
    global selected_host_year
    global hosts
    global selected_host_name

    flash(message, 'danger')
    return render_template(
        'game_predictor/index.html',
        guest_seasons=guest_seasons, selected_guest_year=selected_guest_year,
        guests=guests, selected_guest_name=selected_guest_name,
        host_seasons=host_seasons, selected_host_year=selected_host_year,
        hosts=hosts, selected_host_name=selected_host_name
    )
