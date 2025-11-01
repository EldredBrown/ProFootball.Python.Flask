from typing import Any

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from werkzeug import Response

from app.data.factories import season_factory
from app.data.models.season import Season
from app.data.repositories.season_repository import SeasonRepository
from app.flask.forms.season_forms import NewSeasonForm, EditSeasonForm, DeleteSeasonForm, SeasonForm

blueprint = Blueprint('season', __name__)


@blueprint.route('/')
def index(season_repository: SeasonRepository) -> str:
    seasons = season_repository.get_seasons()
    return render_template('seasons/index.html', seasons=seasons)


@blueprint.route('/details/<int:id>')
def details(id: int, season_repository: SeasonRepository) -> str:
    try:
        delete_season_form = DeleteSeasonForm()
        season = season_repository.get_season(id)
        return render_template('seasons/details.html',
                               season=season, delete_season_form=delete_season_form)
    except IndexError:
        abort(404)


@blueprint.route('/create', methods=['GET', 'POST'])
def create(season_repository: SeasonRepository) -> Response | str:
    form = NewSeasonForm()
    if form.validate_on_submit():
        season = _get_season_from_form(form)
        try:
            season_repository.add_season(season)
            flash(f"Item {form.year.data} has been successfully submitted.", 'success')
            return redirect(url_for('season.index'))
        except ValueError as err:
            return _handle_error(err, 'seasons/create.html', form)
    else:
        if form.errors:
            flash(f"{form.errors}", 'danger')

        return render_template('seasons/create.html', form=form)


@blueprint.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id: int, season_repository: SeasonRepository) -> Response | str:
    old_season = season_repository.get_season(id)
    if old_season:
        form = EditSeasonForm()
        if form.validate_on_submit():
            new_season = _get_season_from_form(form, id)
            try:
                season_repository.update_season(new_season)
                flash(f"Item {form.year.data} has been successfully updated.", 'success')
                return redirect(url_for('season.details', id=id))
            except ValueError as err:
                return _handle_error(err, 'seasons/edit.html', form, season=old_season)
        else:
            _get_form_data_from_season(form, old_season)

            if form.errors:
                flash(f"{form.errors}", 'danger')

            return render_template('seasons/edit.html', season=old_season, form=form)
    else:
        abort(404)


def _get_season_from_form(form: SeasonForm, id: int=None) -> Season:
    kwargs = _get_kwargs_from_form(form, id)
    season = season_factory.create_season(**kwargs)
    return season


def _get_kwargs_from_form(form: SeasonForm, id: int=None) -> dict[str, Any]:
    kwargs = {
        'year': int(form.year.data),
        'num_of_weeks_scheduled': int(form.num_of_weeks_scheduled.data),
        'num_of_weeks_completed': int(form.num_of_weeks_completed.data),
    }
    if id:
        kwargs['id'] = id
    return kwargs


def _get_form_data_from_season(form: SeasonForm, season: Season) -> None:
    form.year.data = season.year
    form.num_of_weeks_scheduled.data = season.num_of_weeks_scheduled
    form.num_of_weeks_completed.data = season.num_of_weeks_completed


@blueprint.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id: int, season_repository: SeasonRepository) -> Response | str:
    season = season_repository.get_season(id)
    try:
        if request.method == 'POST':
            season_repository.delete_season(id)
            flash(f"Season {season.year} has been successfully deleted.", 'success')
            return redirect(url_for('season.index'))
        else:
            return render_template('seasons/delete.html', season=season)
    except IndexError:
        abort(404)


def _handle_error(err: Any, template_name: str, form: SeasonForm, season: Season=None) -> str:
    flash(str(err), 'danger')
    return render_template(template_name, form=form, season=season)
