from typing import Any

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from werkzeug import Response

from app import injector
from app.data.factories import season_factory
from app.data.models.season import Season
from app.data.repositories.season_repository import SeasonRepository
from app.flask.forms.season_forms import NewSeasonForm, EditSeasonForm, DeleteSeasonForm, SeasonForm


blueprint = Blueprint('season', __name__)


@blueprint.route('/')
def index() -> str:
    season_repository = injector.get(SeasonRepository)
    seasons = season_repository.get_seasons()
    return render_template('seasons/index.html', seasons=seasons)


@blueprint.route('/details/<int:year>')
def details(year: int) -> str:
    form = DeleteSeasonForm()
    try:
        season_repository = injector.get(SeasonRepository)
        season = season_repository.get_season(year)
        return render_template('seasons/details.html', season=season, form=form)
    except IndexError:
        abort(404)


@blueprint.route('/create', methods=['GET', 'POST'])
def create() -> Response | str:
    form = NewSeasonForm()
    if form.validate_on_submit():
        try:
            new_season = _get_model_from_form(form)
            season_repository = injector.get(SeasonRepository)
            season_repository.add_season(new_season)
            flash(f"Item {form.year.data} has been successfully submitted.", 'success')
            return redirect(url_for('season.index'))
        except ValueError as err:
            return _handle_error(err, 'seasons/create.html', form)
    else:
        if form.errors:
            flash(f"{form.errors}", 'danger')

        return render_template('seasons/create.html', form=form)


@blueprint.route('/delete/<int:year>', methods=['GET', 'POST'])
def delete(year: int) -> Response | str:
    form = DeleteSeasonForm()
    try:
        season_repository = injector.get(SeasonRepository)
        season = season_repository.get_season(year)
        if not season:
            abort(404)

        if request.method == 'POST':
            season_repository.delete_season(year)
            flash(f"Season {season.year} has been successfully deleted.", 'success')
            return redirect(url_for('season.index'))
        else:
            return render_template('seasons/delete.html', season=season, form=form)
    except IndexError:
        abort(404)


def _get_form_data_from_model(form: SeasonForm, season: Season) -> None:
    form.year.data = season.year


def _get_kwargs_from_form(form: SeasonForm, year: int=None) -> dict[str, Any]:
    kwargs = {
        'year': int(form.year.data),
    }
    if year:
        kwargs['year'] = year
    return kwargs


def _get_model_from_form(form: SeasonForm, year: int=None, old_season: Season=None) -> Season:
    kwargs = _get_kwargs_from_form(form, year)
    season = season_factory.create_season(old_season, **kwargs)
    return season


def _handle_error(err: Any, template_name_or_list: str, form: SeasonForm, season: Season=None) -> str:
    flash(str(err), 'danger')
    return render_template(template_name_or_list, form=form, season=season)
