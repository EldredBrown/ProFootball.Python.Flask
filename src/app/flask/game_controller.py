from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from sqlalchemy.exc import IntegrityError

from app.data.repositories.game_repository import GameRepository
from app.flask.forms.game_forms import NewGameForm, EditGameForm, DeleteGameForm

blueprint = Blueprint('game', __name__)

game_repository = GameRepository()


@blueprint.route('/')
def index():
    games = game_repository.get_games()
    return render_template('games/index.html', games=games)


@blueprint.route('/details/<int:id>')
def details(id: int):
    try:
        delete_game_form = DeleteGameForm()
        game = game_repository.get_game(id)
        return render_template('games/details.html',
                               game=game, delete_game_form=delete_game_form)
    except IndexError:
        abort(404)


@blueprint.route('/create', methods=['GET', 'POST'])
def create():
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
            'notes': form.notes.data,
        }
        try:
            game_repository.add_game(**kwargs)
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
def edit(id: int):
    game = game_repository.get_game(id)
    if game:
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
                'notes': form.notes.data,
            }
            try:
                game_repository.update_game(**kwargs)
                flash(f"Game for season={form.season_year.data} with guest={form.guest_name.data} and host={form.host_name.data} has been successfully updated.", 'success')
                return redirect(url_for('game.details', id=id))
            except ValueError as err:
                return _handle_error(err, 'games/edit.html', form, game=game)
            except IntegrityError as err:
                return _handle_error(err, 'games/edit.html', form, game=game)
        else:
            form.season_year.data = game.season_year
            form.week.data = game.week
            form.guest_name.data = game.guest_name
            form.guest_score.data = game.guest_score
            form.host_name.data = game.host_name
            form.host_score.data = game.host_score
            form.is_playoff.data = game.is_playoff
            form.notes.data = game.notes

            if form.errors:
                flash(f"{form.errors}", 'danger')

            return render_template('games/edit.html', game=game, form=form)
    else:
        abort(404)


@blueprint.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id: int):
    game = game_repository.get_game(id)
    try:
        if request.method == 'POST':
            game_repository.delete_game(id)
            flash(f"Game for season={game.season_year} with guest={game.guest_name} and host={game.host_name} has been successfully deleted.", 'success')
            return redirect(url_for('game.index'))
        else:
            return render_template('games/delete.html', game=game)
    except IndexError:
        abort(404)


def _handle_error(err, template_name_or_list, form, game=None):
    flash(str(err), 'danger')
    return render_template(template_name_or_list, game=game, form=form)
