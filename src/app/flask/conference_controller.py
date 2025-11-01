from typing import Any

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from sqlalchemy.exc import IntegrityError

from app.data.factories import conference_factory
from app.data.models.conference import Conference
from app.data.repositories.conference_repository import ConferenceRepository
from app.flask.forms.conference_forms import NewConferenceForm, EditConferenceForm, DeleteConferenceForm, ConferenceForm

blueprint = Blueprint('conference', __name__)

conference_repository = ConferenceRepository()


@blueprint.route('/')
def index():
    global conference_repository

    conferences = conference_repository.get_conferences()
    return render_template('conferences/index.html', conferences=conferences)


@blueprint.route('/details/<int:id>')
def details(id: int):
    global conference_repository

    try:
        delete_conference_form = DeleteConferenceForm()
        conference = conference_repository.get_conference(id)
        return render_template('conferences/details.html',
                               conference=conference, delete_conference_form=delete_conference_form)
    except IndexError:
        abort(404)


@blueprint.route('/create', methods=['GET', 'POST'])
def create():
    global conference_repository

    form = NewConferenceForm()
    if form.validate_on_submit():
        kwargs = {
            'short_name': str(form.short_name.data),
            'long_name': str(form.long_name.data),
            'league_name': str(form.league_name.data),
            'first_season_year': int(form.first_season_year.data),
            'last_season_year': int(form.last_season_year.data),
        }
        conference = conference_factory.create_conference(**kwargs)
        try:
            conference_repository.add_conference(conference)
            flash(f"Item {form.short_name.data} has been successfully submitted.", 'success')
            return redirect(url_for('conference.index'))
        except ValueError as err:
            return _handle_error(err, 'conferences/create.html', form)
        except IntegrityError as err:
            return _handle_error(err, 'conferences/create.html', form)
    else:
        if form.errors:
            flash(f"{form.errors}", 'danger')

        return render_template('conferences/create.html', form=form)


@blueprint.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id: int):
    global conference_repository

    old_conference = conference_repository.get_conference(id)
    if old_conference:
        form = EditConferenceForm()
        if form.validate_on_submit():
            new_conference = _get_conference_from_form(form, id)
            try:
                conference_repository.update_conference(new_conference)
                flash(f"Item {form.short_name.data} has been successfully updated.", 'success')
                return redirect(url_for('conference.details', id=id))
            except ValueError as err:
                return _handle_error(err, 'conferences/edit.html', form, conference=old_conference)
            except IntegrityError as err:
                return _handle_error(err, 'conferences/edit.html', form, conference=old_conference)
        else:
            _get_form_data_from_conference(form, old_conference)
            if form.errors:
                flash(f"{form.errors}", 'danger')

            return render_template('conferences/edit.html', conference=old_conference, form=form)
    else:
        abort(404)


def _get_conference_from_form(form: ConferenceForm, id: int=None) -> Conference:
    kwargs = _get_kwargs_from_form(form, id)
    conference = conference_factory.create_conference(**kwargs)
    return conference


def _get_kwargs_from_form(form: ConferenceForm, id: int=None) -> dict[str, Any]:
    kwargs = {
        'short_name': str(form.short_name.data),
        'long_name': str(form.long_name.data),
        'league_name': str(form.league_name.data),
        'first_season_year': int(form.first_season_year.data),
        'last_season_year': int(form.last_season_year.data),
    }
    if id:
        kwargs['id'] = id
    return kwargs


def _get_form_data_from_conference(form: ConferenceForm, conference: Conference) -> None:
    form.short_name.data = conference.short_name
    form.long_name.data = conference.long_name
    form.league_name.data = conference.league_name
    form.first_season_year.data = conference.first_season_year
    form.last_season_year.data = conference.last_season_year


@blueprint.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id: int):
    global conference_repository

    conference = conference_repository.get_conference(id)
    try:
        if request.method == 'POST':
            conference_repository.delete_conference(id)
            flash(f"Conference {conference.short_name} has been successfully deleted.", 'success')
            return redirect(url_for('conference.index'))
        else:
            return render_template('conferences/delete.html', conference=conference)
    except IndexError:
        abort(404)


def _handle_error(err, template_name_or_list, form, conference=None):
    flash(str(err), 'danger')
    return render_template(template_name_or_list, conference=conference, form=form)
