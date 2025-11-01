from typing import Any

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from sqlalchemy.exc import IntegrityError

from app.data.factories import division_factory
from app.data.models.division import Division
from app.data.repositories.division_repository import DivisionRepository
from app.flask.forms.division_forms import NewDivisionForm, EditDivisionForm, DeleteDivisionForm, DivisionForm

blueprint = Blueprint('division', __name__)

division_repository = DivisionRepository()


@blueprint.route('/')
def index():
    global division_repository

    divisions = division_repository.get_divisions()
    return render_template('divisions/index.html', divisions=divisions)


@blueprint.route('/details/<int:id>')
def details(id: int):
    global division_repository

    try:
        delete_division_form = DeleteDivisionForm()
        division = division_repository.get_division(id)
        return render_template('divisions/details.html',
                               division=division, delete_division_form=delete_division_form)
    except IndexError:
        abort(404)


@blueprint.route('/create', methods=['GET', 'POST'])
def create():
    global division_repository

    form = NewDivisionForm()
    if form.validate_on_submit():
        division = _get_division_from_form(form)
        try:
            division_repository.add_division(division)
            flash(f"Item {form.name.data} has been successfully submitted.", 'success')
            return redirect(url_for('division.index'))
        except ValueError as err:
            return _handle_error(err, 'divisions/create.html', form)
        except IntegrityError as err:
            return _handle_error(err, 'divisions/create.html', form)
    else:
        if form.errors:
            flash(f"{form.errors}", 'danger')

        return render_template('divisions/create.html', form=form)


@blueprint.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id: int):
    global division_repository

    old_division = division_repository.get_division(id)
    if old_division:
        form = EditDivisionForm()
        if form.validate_on_submit():
            new_division = _get_division_from_form(form, id)
            try:
                division_repository.update_division(new_division)
                flash(f"Item {form.name.data} has been successfully updated.", 'success')
                return redirect(url_for('division.details', id=id))
            except ValueError as err:
                return _handle_error(err, 'divisions/edit.html', form, division=old_division)
            except IntegrityError as err:
                return _handle_error(err, 'divisions/edit.html', form, division=old_division)
        else:
            _get_form_data_from_division(form, old_division)
            if form.errors:
                flash(f"{form.errors}", 'danger')

            return render_template('divisions/edit.html', division=old_division, form=form)
    else:
        abort(404)


def _get_division_from_form(form: DivisionForm, id: int=None) -> Division:
    kwargs = _get_kwargs_from_form(form, id)
    division = division_factory.create_division(**kwargs)
    return division


def _get_kwargs_from_form(form: DivisionForm, id: int=None) -> dict[str, Any]:
    kwargs = {
        'name': str(form.name.data),
        'league_name': str(form.league_name.data),
        'conference_name': str(form.conference_name.data),
        'first_season_year': int(form.first_season_year.data),
        'last_season_year': int(form.last_season_year.data),
    }
    if id:
        kwargs['id'] = id
    return kwargs


def _get_form_data_from_division(form: DivisionForm, division: Division) -> None:
    form.name.data = division.name
    form.league_name.data = division.league_name
    form.conference_name.data = division.conference_name
    form.first_season_year.data = division.first_season_year
    form.last_season_year.data = division.last_season_year


@blueprint.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id: int):
    global division_repository

    division = division_repository.get_division(id)
    try:
        if request.method == 'POST':
            division_repository.delete_division(id)
            flash(f"Division {division.name} has been successfully deleted.", 'success')
            return redirect(url_for('division.index'))
        else:
            return render_template('divisions/delete.html', division=division)
    except IndexError:
        abort(404)


def _handle_error(err, template_name_or_list, form, division=None):
    flash(str(err), 'danger')
    return render_template(template_name_or_list, division=division, form=form)
