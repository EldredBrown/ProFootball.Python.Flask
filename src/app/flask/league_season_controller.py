import copy

from typing import Any

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for, Response
from sqlalchemy.exc import IntegrityError

from app import injector
from app.data.factories import league_season_factory
from app.data.models.league_season import LeagueSeason
from app.data.repositories.league_season_repository import LeagueSeasonRepository
from app.flask.forms.league_season_forms import NewLeagueSeasonForm, EditLeagueSeasonForm, DeleteLeagueSeasonForm, LeagueSeasonForm


blueprint = Blueprint('league_season', __name__)


@blueprint.route('/')
def index() -> str:
    league_season_repository = injector.get(LeagueSeasonRepository)
    league_seasons = league_season_repository.get_league_seasons()
    return render_template('league_seasons/index.html', league_seasons=league_seasons)


@blueprint.route('/details/<int:id>')
def details(id: int) -> str:
    form = DeleteLeagueSeasonForm()
    try:
        league_season_repository = injector.get(LeagueSeasonRepository)
        league_season = league_season_repository.get_league_season(id)
        return render_template('league_seasons/details.html', league_season=league_season, form=form)
    except IndexError:
        abort(404)


@blueprint.route('/create', methods=['GET', 'POST'])
def create() -> Response | str:
    form = NewLeagueSeasonForm()
    if form.validate_on_submit():
        try:
            new_league_season = _get_model_from_form(form)
            league_season_repository = injector.get(LeagueSeasonRepository)
            league_season_repository.add_league_season(new_league_season)
            flash(f"Item {form.league_name.data}, {form.season_year.data} has been successfully submitted.", 'success')
            return redirect(url_for('league_season.index'))
        except ValueError as err:
            return _handle_value_error(err, 'league_seasons/create.html', form)
        except IntegrityError as err:
            return _handle_integrity_error(err, 'INSERT', 'league_seasons/create.html', form)
    else:
        if form.errors:
            flash(f"{form.errors}", 'danger')

        return render_template('league_seasons/create.html', form=form)


@blueprint.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id: int) -> Response | str:
    league_season_repository = injector.get(LeagueSeasonRepository)
    old_league_season = league_season_repository.get_league_season(id)
    old_league_season_copy = copy.deepcopy(old_league_season)
    if old_league_season_copy:
        form = EditLeagueSeasonForm()
        if form.validate_on_submit():
            try:
                new_league_season = _get_model_from_form(form, id)
                league_season_repository.update_league_season(new_league_season)
                flash(
                    f"Item {form.league_name.data}, {form.season_year.data} has been successfully updated.",
                    'success'
                )
                return redirect(url_for('league_season.details', id=id))
            except ValueError as err:
                return _handle_value_error(
                    err, 'league_seasons/edit.html', form, league_season=old_league_season_copy
                )
            except IntegrityError as err:
                return _handle_integrity_error(
                    err, 'UPDATE', 'league_seasons/edit.html', form,
                    league_season=old_league_season_copy
                )
            except IndexError:
                abort(404)
        else:
            _get_form_data_from_model(form, old_league_season_copy)
            if form.errors:
                flash(f"{form.errors}", 'danger')

            return render_template(
                'league_seasons/edit.html', league_season=old_league_season_copy, form=form
            )
    else:
        abort(404)


def _get_model_from_form(form: LeagueSeasonForm, id: int=None) -> LeagueSeason:
    kwargs = _get_kwargs_from_form(form, id)
    league_season = league_season_factory.create_league_season(**kwargs)
    return league_season


def _get_kwargs_from_form(form: LeagueSeasonForm, id: int=None) -> dict[str, Any]:
    kwargs = {
        'league_name': str(form.league_name.data),
        'season_year': int(form.season_year.data),
        'num_of_weeks_scheduled': int(form.num_of_weeks_scheduled.data),
        'num_of_weeks_completed': int(form.num_of_weeks_completed.data),
    }
    if id:
        kwargs['id'] = id
    return kwargs


def _handle_value_error(err: Any, template_name: str, form: LeagueSeasonForm, league_season: LeagueSeason=None) -> str:
    flash(str(err), 'danger')
    return render_template(template_name, league_season=league_season, form=form)


def _handle_integrity_error(
        err: Any, sql_operation: str, template_name: str, form: LeagueSeasonForm, league_season: LeagueSeason=None
) -> str:
    if str(err.args[0]).find("Violation of PRIMARY KEY constraint") != -1:
        err_msg = "A LeagueSeason with the same id already exists."
    elif str(err.args[0]).find("Violation of UNIQUE KEY constraint 'UQ_LeagueSeason_League_Season'") != -1:
        err_msg = "A LeagueSeason with the same league_id and season_year already exists."
    elif str(err.args[0]).find(f"The {sql_operation} statement conflicted with the FOREIGN KEY constraint 'FK_LeagueSeason_Association_LeagueId'") != -1:
        err_msg = "FOREIGN KEY constraint violation on league name."
    elif str(err.args[0]).find(f"The {sql_operation} statement conflicted with the FOREIGN KEY constraint 'FK_LeagueSeason_Season_SeasonYear'") != -1:
        err_msg = "FOREIGN KEY constraint violation on season year."
    else:
        err_msg = "An unexpected error occurred."

    flash(err_msg, 'danger')
    return render_template(template_name, league_season=league_season, form=form)


def _get_form_data_from_model(form: LeagueSeasonForm, league_season: LeagueSeason) -> None:
    form.league_name.data = league_season.league.short_name
    form.season_year.data = league_season.season.year
    form.num_of_weeks_scheduled.data = league_season.num_of_weeks_scheduled
    form.num_of_weeks_completed.data = league_season.num_of_weeks_completed


@blueprint.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id: int) -> Response | str:
    form = DeleteLeagueSeasonForm()
    try:
        league_season_repository = injector.get(LeagueSeasonRepository)
        league_season = league_season_repository.get_league_season(id)
        if not league_season:
            abort(404)

        if request.method == 'POST':
            league_season_repository.delete_league_season(id)
            flash(
                f"LeagueSeason {league_season.league.short_name}. {league_season.season.year} has been successfully deleted.",
                'success'
            )
            return redirect(url_for('league_season.index'))
        else:
            return render_template('league_seasons/delete.html', league_season=league_season, form=form)
    except IndexError:
        abort(404)
