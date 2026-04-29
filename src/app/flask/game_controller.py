import copy
from typing import Any

from flask import Blueprint, Response, abort, flash, redirect, render_template, request, session, url_for
from sqlalchemy.exc import IntegrityError

from app import injector
from app.data.factories import game_factory
from app.data.models.game import Game
from app.data.models.season import Season
from app.data.repositories.season_repository import SeasonRepository
from app.data.repositories.game_repository import GameRepository
from app.flask.forms.game_forms import NewGameForm, EditGameForm, DeleteGameForm, GameForm
from app.services.game_service.game_service import GameService

blueprint = Blueprint('game', __name__)


@blueprint.route('/')
def index() -> str:
    season_repository = injector.get(SeasonRepository)

    seasons = season_repository.get_seasons()
    session['seasons'] = [s.to_dict() for s in seasons]

    selected_year = 0
    session['selected_year'] = selected_year

    selected_season = Season(year=selected_year, num_of_weeks_scheduled=0, num_of_weeks_completed=0).to_dict()
    session['selected_season'] = selected_season

    selected_week = 0
    session['selected_week'] = selected_week

    game_repository = injector.get(GameRepository)
    games = game_repository.get_games_by_season_year(season_year=None)
    session['games'] = [g.to_dict() for g in games]

    return render_template(
        'games/index.html',
        seasons=seasons, selected_season=selected_season, selected_week=selected_week, games=games
    )


@blueprint.route('/details/<int:id>')
def details(id: int) -> str:
    form = DeleteGameForm()
    try:
        game_repository = injector.get(GameRepository)
        game = game_repository.get_game(id)
        return render_template('games/details.html', game=game, form=form)
    except IndexError:
        abort(404)


@blueprint.route('/create', methods=['GET', 'POST'])
def create() -> Response | str:
    form = NewGameForm()
    if request.method == 'GET':
        selected_season = session.get('selected_season')
        form.season_year.data = selected_season['year'] if selected_season['year'] >= 1920 else 0

    if form.validate_on_submit():
        new_game = _get_game_from_form(form)
        try:
            game_service = injector.get(GameService)
            game_service.add_game(new_game)
            flash(f"Game for season={form.season_year.data} with guest={form.guest_name.data} and host={form.host_name} has been successfully submitted.", 'success')
            return redirect(url_for('game.index'))
        except ValueError as err:
            return _handle_error(err, 'games/create.html', form)
        except IntegrityError as err:
            return _handle_error(err, 'games/create.html', form)
    else:
        if form.errors:
            flash(f"{form.errors}", 'danger')

        return render_template('games/create.html', form=form)


@blueprint.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id: int) -> Response | str:
    game_repository = injector.get(GameRepository)
    old_game = copy.deepcopy(game_repository.get_game(id))
    if old_game:
        form = EditGameForm()
        if form.validate_on_submit():
            new_game = _get_game_from_form(form, id)
            try:
                game_service = injector.get(GameService)
                game_service.update_game(new_game, old_game)
                flash(f"Game for season={form.season_year.data} with guest={form.guest_name.data} and host={form.host_name.data} has been successfully updated.", 'success')
                return redirect(url_for('game.details', id=id))
            except ValueError as err:
                return _handle_error(err, 'games/edit.html', form, game=old_game)
            except IntegrityError as err:
                return _handle_error(err, 'games/edit.html', form, game=old_game)
            except IndexError:
                abort(404)
        else:
            _get_form_data_from_game(form, old_game)

            if form.errors:
                flash(f"{form.errors}", 'danger')

            return render_template('games/edit.html', game=old_game, form=form)
    else:
        abort(404)


def _get_game_from_form(form: GameForm, id: int=None) -> Game:
    kwargs = _get_kwargs_from_form(form, id)
    game = game_factory.create_game(**kwargs)
    return game


def _get_kwargs_from_form(form: GameForm, id: int=None) -> dict[str, Any]:
    kwargs = {
        'season_year': int(form.season_year.data),
        'week': int(form.week.data),
        'guest_name': str(form.guest_name.data),
        'guest_score': int(form.guest_score.data),
        'host_name': str(form.host_name.data),
        'host_score': int(form.host_score.data),
        'is_playoff': form.is_playoff.data,
        'notes': form.notes.data,
    }
    if id:
        kwargs['id'] = id
    return kwargs


def _get_form_data_from_game(form: GameForm, game) -> None:
    form.season_year.data = game.season_year
    form.week.data = game.week
    form.guest_name.data = game.guest_name
    form.guest_score.data = game.guest_score
    form.host_name.data = game.host_name
    form.host_score.data = game.host_score
    form.is_playoff.data = game.is_playoff
    form.notes.data = game.notes


@blueprint.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id: int) -> Response | str:
    try:
        game_repository = injector.get(GameRepository)
        game = game_repository.get_game(id)
        if not game:
            abort(404)

        if request.method == 'POST':
            game_service = injector.get(GameService)
            game_service.delete_game(id)
            flash(f"Game for season={game.season_year} with guest={game.guest_name} and host={game.host_name} has been successfully deleted.", 'success')
            return redirect(url_for('game.index'))
        else:
            return render_template('games/delete.html', game=game)
    except IndexError:
        abort(404)


@blueprint.route('/select_season', methods=['POST'])
def select_season() -> str:
    selected_year = int(request.form.get('season_dropdown'))  # Fetch the selected season.
    session['selected_year'] = selected_year

    season_repository = injector.get(SeasonRepository)
    selected_season = season_repository.get_season_by_year(selected_year)
    session['selected_season'] = selected_season.to_dict()

    selected_week = 0
    session['selected_week'] = selected_week

    game_repository = injector.get(GameRepository)
    games = game_repository.get_games_by_season_year(season_year=selected_year)

    return render_template(
        'games/index.html',
        seasons=session.get('seasons'), selected_season=selected_season, selected_week=selected_week, games=games
    )


@blueprint.route('/select_week', methods=['POST'])
def select_week() -> str:
    selected_week = int(request.form.get('week_dropdown'))  # Fetch the selected week.
    session['selected_week'] = selected_week

    selected_season = session.get('selected_season')

    game_repository = injector.get(GameRepository)
    games = game_repository.get_games_by_season_year_and_week(season_year=selected_season['year'], week=selected_week)

    return render_template(
        'games/index.html',
        seasons=session.get('seasons'), selected_season=selected_season, selected_week=selected_week, games=games
    )


def _handle_error(err: Any, template_name: str, form: GameForm, game: Game=None) -> str:
    flash(str(err), 'danger')
    return render_template(template_name, form=form, game=game)
