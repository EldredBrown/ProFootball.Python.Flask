import copy
from typing import Any, Optional

from flask import Blueprint, Response, abort, flash, redirect, render_template, request, session, url_for
from sqlalchemy.exc import IntegrityError

from app import injector
from app.data.factories import game_factory
from app.data.models.association import Association
from app.data.models.game import Game
from app.data.models.season import Season
from app.data.repositories.association_repository import AssociationRepository
from app.data.repositories.league_season_repository import LeagueSeasonRepository
from app.data.repositories.season_repository import SeasonRepository
from app.data.repositories.game_repository import GameRepository
from app.flask.forms.game_forms import NewGameForm, EditGameForm, DeleteGameForm, GameForm
from app.services.game_service.game_service import GameService


blueprint = Blueprint('game', __name__)


@blueprint.route('/')
def index() -> str:
    seasons, selected_season_year = _get_seasons_and_selected_season_year()
    active_leagues, selected_league = _get_leagues_and_selected_league(selected_season_year)
    weeks, selected_week = _get_weeks_and_selected_week(selected_season_year, selected_league)
    games = _get_games(selected_season_year, selected_league, selected_week)

    return render_template(
        'games/index.html',
        seasons=seasons, selected_season_year=selected_season_year,
        leagues=active_leagues, selected_league_name=selected_league.short_name,
        weeks=weeks, selected_week=selected_week,
        games=games
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


def _get_weeks_and_selected_week(selected_season_year: int, selected_league: Association) \
        -> tuple[list[int | None], int | None]:
    weeks = _get_weeks(selected_league, selected_season_year)

    selected_week = session.get('selected_week')

    return weeks, selected_week


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
        selected_season_year = session.get('selected_season_year')
        form.season_year.data = selected_season_year if selected_season_year >= 1920 else -1
        form.league_name.data = session.get('selected_league_name')
        form.week.data = session.get('selected_week')

    if form.validate_on_submit():
        try:
            new_game = _get_model_from_form(form)
            game_service = injector.get(GameService)
            game_service.add_game(new_game)

            flash(f"Game for season={form.season_year.data}, league={form.league_name.data}, week={form.week.data}, with guest={form.guest_name.data} and host={form.host_name.data} has been successfully submitted.", 'success')

            session['week'] = form.week.data
            return redirect(url_for('game.create'))
        except ValueError as err:
            return _handle_value_error(err, 'games/create.html', form)
        except IntegrityError as err:
            return _handle_integrity_error(err, 'INSERT', 'games/create.html', form)
    else:
        if form.errors:
            flash(f"{form.errors}", 'danger')

        return render_template('games/create.html', form=form)


@blueprint.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id: int) -> Response | str:
    game_repository = injector.get(GameRepository)
    game = game_repository.get_game(id)
    old_game = copy.deepcopy(game)
    if old_game:
        form = EditGameForm()
        if form.validate_on_submit():
            try:
                new_game = _get_model_from_form(form, id)
                game_service = injector.get(GameService)
                game_service.update_game(new_game, old_game)
                flash(f"Game for season={form.season_year.data}, league={form.league_name.data}, and week={form.week.data} with guest={form.guest_name.data} and host={form.host_name.data} has been successfully updated.", 'success')
                return redirect(url_for('game.details', id=id))
            except ValueError as err:
                return _handle_value_error(err, 'games/edit.html', form, game=old_game)
            except IntegrityError as err:
                return _handle_integrity_error(err, 'UPDATE', 'games/edit.html', form, game=old_game)
            except IndexError:
                abort(404)
        else:
            _get_form_data_from_model(form, old_game)

            if form.errors:
                flash(f"{form.errors}", 'danger')

            return render_template('games/edit.html', game=old_game, form=form)
    else:
        abort(404)


def _get_model_from_form(form: GameForm, id: int=None) -> Game:
    kwargs = _get_kwargs_from_form(form, id)
    game = game_factory.create_game(**kwargs)
    return game


def _handle_value_error(err: Any, template_name: str, form: GameForm, game: Game=None) -> str:
    flash(str(err), 'danger')
    return render_template(template_name, game=game, form=form)


def _handle_integrity_error(err: Any, sql_operation: str, template_name: str, form: GameForm, game: Game=None) -> str:
    if str(err.args[0]).find("Violation of PRIMARY KEY constraint") != -1:
        err_msg = "A game with the same id already exists."
    elif str(err.args[0]).find("Violation of UNIQUE KEY constraint") != -1:
        err_msg = "A game with the same season, league, week, guest, and host already exists."
    elif str(err.args[0]).find(f"The {sql_operation} statement conflicted with the FOREIGN KEY constraint 'FK_Game_Season_SeasonYear'") != -1:
        err_msg = "FOREIGN KEY constraint violation on season year."
    elif str(err.args[0]).find(f"The {sql_operation} statement conflicted with the FOREIGN KEY constraint 'FK_Game_Association_LeagueId'") != -1:
        err_msg = "FOREIGN KEY constraint violation on league name."
    else:
        err_msg = "An unexpected error occurred."

    flash(err_msg, 'danger')
    return render_template(template_name, game=game, form=form)


def _get_kwargs_from_form(form: GameForm, id: int=None) -> dict[str, Any]:
    kwargs = {
        'season_year': int(form.season_year.data),
        'league_name': str(form.league_name.data),
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


def _get_form_data_from_model(form: GameForm, game) -> None:
    form.season_year.data = game.season.year
    form.league_name.data = game.league.short_name
    form.week.data = game.week
    form.guest_name.data = game.guest_name
    form.guest_score.data = game.guest_score
    form.host_name.data = game.host_name
    form.host_score.data = game.host_score
    form.is_playoff.data = game.is_playoff
    form.notes.data = game.notes


@blueprint.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id: int) -> Response | str:
    form = DeleteGameForm()
    try:
        game_repository = injector.get(GameRepository)
        game = game_repository.get_game(id)
        if not game:
            abort(404)

        if request.method == 'POST':
            game_service = injector.get(GameService)
            game_service.delete_game(id)
            flash(f"Game for season={game.season.year}, league={game.league.short_name}, and week={game.week} with guest={game.guest_name} and host={game.host_name} has been successfully deleted.", 'success')
            return redirect(url_for('game.index'))
        else:
            return render_template('games/delete.html', game=game, form=form)
    except IndexError:
        abort(404)


@blueprint.route('/select_season', methods=['POST'])
def select_season() -> str:
    selected_season_year = int(request.form.get('season_dropdown'))

    seasons = session.get('seasons')
    session['selected_season_year'] = selected_season_year

    active_leagues, selected_league = _get_leagues_and_set_selected_league(selected_season_year)
    weeks, selected_week = _get_weeks_and_set_selected_week(selected_season_year, selected_league)
    games = _get_games(selected_season_year, selected_league, selected_week)

    return render_template(
        'games/index.html',
        seasons=seasons, selected_season_year=selected_season_year,
        leagues=active_leagues, selected_league_name=selected_league.short_name,
        weeks=weeks, selected_week=selected_week,
        games=games
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
    selected_league_name = str(request.form.get('league_dropdown'))

    seasons = session.get('seasons')
    selected_season_year = session.get('selected_season_year')

    active_leagues = session.get('leagues')
    session['selected_league_name'] = selected_league_name

    kwargs = [l for l in active_leagues if l['short_name'] == selected_league_name][0]
    selected_league = Association(**kwargs)

    weeks, selected_week = _get_weeks_and_set_selected_week(selected_season_year, selected_league)
    games = _get_games(selected_season_year, selected_league, selected_week)

    return render_template(
        'games/index.html',
        seasons=seasons, selected_season_year=selected_season_year,
        leagues=active_leagues, selected_league_name=selected_league_name,
        weeks=weeks, selected_week=selected_week,
        games=games
    )


def _get_weeks_and_set_selected_week(selected_season_year: int, selected_league: Association) \
        -> tuple[list[int | None], int | None]:
    weeks = _get_weeks(selected_league, selected_season_year)

    selected_week = None
    session['selected_week'] = selected_week

    return weeks, selected_week


def _get_weeks(selected_league: Association, selected_season_year: int) -> list[Any]:
    league_season_repository = injector.get(LeagueSeasonRepository)
    selected_league_season = league_season_repository.get_league_season_by_league_and_season(selected_league.id,
                                                                                             selected_season_year)

    weeks = []
    if selected_league_season is not None:
        for i in range(0, selected_league_season.num_of_weeks_scheduled + 1):
            weeks.append(None if i == 0 else i)
    session['weeks'] = weeks
    return weeks


@blueprint.route('/select_week', methods=['POST'])
def select_week() -> str:
    selected_week = request.form.get('week_dropdown')
    if selected_week == 'None':
        selected_week = None
    else:
        selected_week = int(selected_week)

    seasons = session.get('seasons')
    selected_season_year = session.get('selected_season_year')

    active_leagues = session.get('leagues')
    selected_league_name = session.get('selected_league_name')
    kwargs = [l for l in active_leagues if l['short_name'] == selected_league_name][0]
    selected_league = Association(**kwargs)

    weeks = session.get('weeks')
    session['selected_week'] = selected_week

    games = _get_games(selected_season_year, selected_league, selected_week)

    return render_template(
        'games/index.html',
        seasons=seasons, selected_season_year=selected_season_year,
        leagues=active_leagues, selected_league_name=selected_league_name,
        weeks=weeks, selected_week=selected_week,
        games=games
    )


def _get_games(selected_season_year: int, selected_league: Association, selected_week: int | None) -> list[Game]:
    game_repository = injector.get(GameRepository)
    games = game_repository.get_games_by_season_league_and_week(
        season_year=selected_season_year, league_id=selected_league.id, week=selected_week
    )
    return games
