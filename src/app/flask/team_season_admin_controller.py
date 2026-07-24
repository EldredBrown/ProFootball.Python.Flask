import copy

from typing import Any

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for, Response
from sqlalchemy.exc import IntegrityError

from app import injector
from app.data.factories import team_season_factory
from app.data.models.team_season import TeamSeason
from app.data.repositories.team_season_repository import TeamSeasonRepository
from app.flask.forms.team_season_forms import NewTeamSeasonForm, EditTeamSeasonForm, DeleteTeamSeasonForm, TeamSeasonForm


blueprint = Blueprint('team_season_admin', __name__)


@blueprint.route('/')
def index() -> str:
    team_season_repository = injector.get(TeamSeasonRepository)
    team_seasons = team_season_repository.get_team_seasons()
    return render_template('team_seasons_admin/index.html', team_seasons=team_seasons)


@blueprint.route('/details/<int:id>')
def details(id: int) -> str:
    form = DeleteTeamSeasonForm()
    try:
        team_season_repository = injector.get(TeamSeasonRepository)
        team_season = team_season_repository.get_team_season(id)
        return render_template('team_seasons_admin/details.html', team_season=team_season, form=form)
    except IndexError:
        abort(404)


@blueprint.route('/create', methods=['GET', 'POST'])
def create() -> Response | str:
    form = NewTeamSeasonForm()
    if form.validate_on_submit():
        try:
            new_team_season = _get_model_from_form(form)
            team_season_repository = injector.get(TeamSeasonRepository)
            team_season_repository.add_team_season(new_team_season)
            flash(f"Item {form.team_name.data}, {form.season_year.data} has been successfully submitted.", 'success')
            return redirect(url_for('team_season_admin.index'))
        except ValueError as err:
            return _handle_error(err, 'team_seasons_admin/create.html', form)
        except IntegrityError as err:
            return _handle_error(err, 'team_seasons_admin/create.html', form)
    else:
        if form.errors:
            flash(f"{form.errors}", 'danger')

        return render_template('team_seasons_admin/create.html', form=form)


@blueprint.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id: int) -> Response | str:
    team_season_repository = injector.get(TeamSeasonRepository)
    old_team_season = team_season_repository.get_team_season(id)
    old_team_season_copy = copy.deepcopy(old_team_season)
    if old_team_season_copy:
        form = EditTeamSeasonForm()
        if form.validate_on_submit():
            try:
                new_team_season = _get_model_from_form(form, id)
                team_season_repository.update_team_season(new_team_season)
                flash(
                    f"Item {form.team_name.data}, {form.season_year.data} has been successfully updated.",
                    'success'
                )
                return redirect(url_for('team_season_admin.details', id=id))
            except ValueError as err:
                return _handle_error(err, 'team_seasons_admin/edit.html', form, team_season=old_team_season_copy)
            except IntegrityError as err:
                return _handle_error(err, 'team_seasons_admin/edit.html', form, team_season=old_team_season_copy)
            except IndexError:
                abort(404)
        else:
            _get_form_data_from_model(form, old_team_season_copy)
            if form.errors:
                flash(f"{form.errors}", 'danger')

            return render_template(
                'team_seasons_admin/edit.html', team_season=old_team_season_copy, form=form
            )
    else:
        abort(404)


def _get_model_from_form(form: TeamSeasonForm, id: int=None) -> TeamSeason:
    kwargs = _get_kwargs_from_form(form, id)
    team_season = team_season_factory.create_team_season(**kwargs)
    return team_season


def _get_kwargs_from_form(form: TeamSeasonForm, id: int=None) -> dict[str, Any]:
    kwargs = {
        'team_name': str(form.team_name.data),
        'season_year': int(form.season_year.data),
        'league_name': str(form.league_name.data),
        'conference_name': str(form.conference_name.data),
        'division_name': str(form.division_name.data),
    }
    if id:
        kwargs['id'] = id
    return kwargs


def _get_form_data_from_model(form: TeamSeasonForm, team_season: TeamSeason) -> None:
    form.team_name.data = team_season.team.name
    form.season_year.data = team_season.season.year
    form.league_name.data = team_season.league.short_name
    form.conference_name.data = team_season.conference.short_name if team_season.conference else ''
    form.division_name.data = team_season.division.short_name if team_season.division else ''


def _handle_error(err: Any, template_name: str, form: TeamSeasonForm, team_season: TeamSeason=None) -> str:
    flash(str(err), 'danger')
    return render_template(template_name, form=form, team_season=team_season)


@blueprint.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id: int) -> Response | str:
    form = DeleteTeamSeasonForm()
    try:
        team_season_repository = injector.get(TeamSeasonRepository)
        team_season = team_season_repository.get_team_season(id)
        if not team_season:
            abort(404)

        if request.method == 'POST':
            team_season_repository.delete_team_season(id)
            flash(
                f"TeamSeason {team_season.team.name}. {team_season.season.year} has been successfully deleted.",
                'success'
            )
            return redirect(url_for('team_season_admin.index'))
        else:
            return render_template('team_seasons_admin/delete.html', team_season=team_season, form=form)
    except IndexError:
        abort(404)
