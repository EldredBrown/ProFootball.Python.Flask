from flask import Blueprint, render_template, request, url_for, redirect

from app.data.repositories.rankings_repository import RankingsRepository
from app.data.repositories.season_repository import SeasonRepository
from app.flask.season_controller import season_repository

blueprint = Blueprint('rankings', __name__)

season_repository = SeasonRepository()
rankings_repository = RankingsRepository()

RANKING_TYPES = ['Offense', 'Defense', 'Total']

seasons = None
selected_year = None


@blueprint.route('/')
def index():
    global seasons
    global selected_year

    seasons = season_repository.get_seasons()
    return render_template(
        'rankings/index.html',
        seasons=seasons, selected_year=selected_year, types=RANKING_TYPES, selected_type=None, rankings=None
    )


@blueprint.route('select_season', methods=['POST'])
def select_season():
    global seasons
    global selected_year

    selected_year = int(request.form.get('season_dropdown'))  # Fetch the selected season.
    return render_template(
        'rankings/index.html',
        seasons=seasons, selected_year=selected_year, types=RANKING_TYPES, selected_type=None, rankings=None
    )


@blueprint.route('select_type', methods=['POST'])
def select_type():
    global seasons
    global selected_year
    global selected_type

    selected_type = str(request.form.get('ranking_type_dropdown'))  # Fetch the selected type.
    if selected_type == 'Offense':
        return redirect(url_for('rankings.offense'))
    elif selected_type == 'Defense':
        return redirect(url_for('rankings.defense'))
    elif selected_type == 'Total':
        return redirect(url_for('rankings.total'))
    else:
        raise TypeError('Invalid ranking type')


@blueprint.route('/offense')
def offense():
    global seasons
    global selected_year

    seasons = season_repository.get_seasons()
    rankings = rankings_repository.get_offensive_rankings_by_season_year(selected_year)
    return render_template(
        'rankings/offense.html',
        seasons=seasons, selected_year=selected_year,
        types=RANKING_TYPES, selected_type='Offense', rankings=rankings
    )


@blueprint.route('/defense')
def defense():
    global seasons
    global selected_year

    seasons = season_repository.get_seasons()
    rankings = rankings_repository.get_defensive_rankings_by_season_year(selected_year)
    return render_template(
        'rankings/defense.html',
        seasons=seasons, selected_year=selected_year,
        types=RANKING_TYPES, selected_type='Defense', rankings=rankings
    )


@blueprint.route('/total')
def total():
    global seasons
    global selected_year

    seasons = season_repository.get_seasons()
    rankings = rankings_repository.get_total_rankings_by_season_year(selected_year)
    return render_template(
        'rankings/defense.html',
        seasons=seasons, selected_year=selected_year,
        types=RANKING_TYPES, selected_type='Total', rankings=rankings
    )
