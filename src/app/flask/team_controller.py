from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from sqlalchemy.exc import IntegrityError

from app.data.factories import team_factory
from app.data.repositories.team_repository import TeamRepository
from app.flask.forms.team_forms import NewTeamForm, EditTeamForm, DeleteTeamForm

blueprint = Blueprint('team', __name__)

team_repository = TeamRepository()


@blueprint.route('/')
def index():
    global team_repository

    teams = team_repository.get_teams()
    return render_template('teams/index.html', teams=teams)


@blueprint.route('/details/<int:id>')
def details(id: int):
    global team_repository

    try:
        delete_team_form = DeleteTeamForm()
        team = team_repository.get_team(id)
        return render_template('teams/details.html',
                               team=team, delete_team_form=delete_team_form)
    except IndexError:
        abort(404)


@blueprint.route('/create', methods=['GET', 'POST'])
def create():
    global team_repository

    form = NewTeamForm()
    if form.validate_on_submit():
        kwargs = {
            'name': str(form.name.data),
        }
        try:
            team = team_factory.create_team(**kwargs)
            team_repository.add_team(team)
            flash(f"Item {form.name.data} has been successfully submitted.", 'success')
            return redirect(url_for('team.index'))
        except ValueError as err:
            return _handle_error(err, 'teams/create.html', form)
        except IntegrityError as err:
            return _handle_error(err, 'teams/create.html', form)
    else:
        if form.errors:
            flash(f"{form.errors}", 'danger')

        return render_template('teams/create.html', form=form)


@blueprint.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id: int):
    global team_repository

    old_team = team_repository.get_team(id)
    if old_team:
        form = EditTeamForm()
        if form.validate_on_submit():
            kwargs = {
                'id': id,
                'name': str(form.name.data),
            }
            try:
                new_team = team_factory.create_team(**kwargs)
                team_repository.update_team(new_team)
                flash(f"Item {form.name.data} has been successfully updated.", 'success')
                return redirect(url_for('team.details', id=id))
            except ValueError as err:
                return _handle_error(err, 'teams/edit.html', form, team=old_team)
            except IntegrityError as err:
                return _handle_error(err, 'teams/edit.html', form, team=old_team)
        else:
            form.name.data = old_team.name

            if form.errors:
                flash(f"{form.errors}", 'danger')

            return render_template('teams/edit.html', team=old_team, form=form)
    else:
        abort(404)


@blueprint.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id: int):
    global team_repository

    team = team_repository.get_team(id)
    try:
        if request.method == 'POST':
            team_repository.delete_team(id)
            flash(f"Team {team.name} has been successfully deleted.", 'success')
            return redirect(url_for('team.index'))
        else:
            return render_template('teams/delete.html', team=team)
    except IndexError:
        abort(404)


def _handle_error(err, template_name_or_list, form, team=None):
    flash(str(err), 'danger')
    return render_template(template_name_or_list, team=team, form=form)
