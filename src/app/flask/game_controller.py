from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from sqlalchemy.exc import IntegrityError

from app.data.factories import game_factory
from app.data.repositories.game_repository import GameRepository
from app.flask.forms.game_forms import NewGameForm, EditGameForm, DeleteGameForm

blueprint = Blueprint('game', __name__)

game_repository = GameRepository()


@blueprint.route('/')
def index():
    global game_repository

    games = game_repository.get_games()
    return render_template('games/index.html', games=games)


@blueprint.route('/details/<int:id>')
def details(id: int):
    global game_repository

    try:
        delete_game_form = DeleteGameForm()
        game = game_repository.get_game(id)
        return render_template('games/details.html',
                               game=game, delete_game_form=delete_game_form)
    except IndexError:
        abort(404)


@blueprint.route('/create', methods=['GET', 'POST'])
def create():
    global game_repository

    form = NewGameForm()
    if form.validate_on_submit():
        kwargs = {
            'season_year': int(form.season_year.data),
            'week': int(form.week.data),
            'guest_name': str(form.guest_name.data),
            'guest_score': int(form.guest_score.data),
            'host_name': str(form.host_name.data),
            'host_score': int(form.host_score.data),
            'is_playoff': bool(form.is_playoff.data),
        }
        try:
            game = game_factory.create_game(**kwargs)
            game_repository.add_game(game)
            flash(
                f"Game with season_year={game.season_year}, week={game.week}, "
                f"guest_name={game.guest_name}, and host_name={game.host_name} "
                f"has been successfully submitted.", 'success'
            )
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
def edit(id: int):
    global game_repository

    old_game = game_repository.get_game(id)
    if old_game:
        form = EditGameForm()
        if form.validate_on_submit():
            kwargs = {
                'id': id,
                'season_year': int(form.season_year.data),
                'week': int(form.week.data),
                'guest_name': str(form.guest_name.data),
                'guest_score': int(form.guest_score.data),
                'host_name': str(form.host_name.data),
                'host_score': int(form.host_score.data),
                'is_playoff': bool(form.is_playoff.data),
            }
            try:
                new_game = game_factory.create_game(**kwargs)
                game_repository.update_game(new_game)
                flash(
                    f"Game with season_year={form.season_year.data}, week={form.week.data}, "
                    f"guest_name={form.guest_name.data}, and host_name={form.host_name.data} "
                    f"has been successfully updated.", 'success'
                )
                return redirect(url_for('game.details', id=id))
            except ValueError as err:
                return _handle_error(err, 'games/edit.html', form, game=old_game)
            except IntegrityError as err:
                return _handle_error(err, 'games/edit.html', form, game=old_game)
        else:
            form.season_year.data = old_game.season_year
            form.week.data = old_game.week
            form.guest_name.data = old_game.guest_name
            form.guest_score.data = old_game.guest_score
            form.host_name.data = old_game.host_name
            form.host_score.data = old_game.host_score
            form.is_playoff.data = old_game.is_playoff

            if form.errors:
                flash(f"{form.errors}", 'danger')

            return render_template('games/edit.html', game=old_game, form=form)
    else:
        abort(404)


@blueprint.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id: int):
    global game_repository

    game = game_repository.get_game(id)
    try:
        if request.method == 'POST':
            game_repository.delete_game(id)
            flash(
                f"Game with season_year={game.season_year}, week={game.week}, "
                f"guest_name={game.guest_name}, and host_name={game.host_name} "
                f"has been successfully deleted.", 'success'
            )
            return redirect(url_for('game.index'))
        else:
            return render_template('games/delete.html', game=game)
    except IndexError:
        abort(404)


def _handle_error(err, template_name_or_list, form, game=None):
    flash(str(err), 'danger')
    return render_template(template_name_or_list, game=game, form=form)
