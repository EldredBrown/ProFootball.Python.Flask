from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from sqlalchemy.exc import IntegrityError

from app.data.repositories.conference_repository import ConferenceRepository
from app.flask.forms.conference import NewConferenceForm, EditConferenceForm, DeleteConferenceForm

blueprint = Blueprint('conference', __name__)

conference_repository = ConferenceRepository()


@blueprint.route('/')
def index():
    conferences = conference_repository.get_conferences()
    return render_template('conferences/index.html', conferences=conferences)


@blueprint.route('/details/<int:id>')
def details(id: int):
    try:
        delete_conference_form = DeleteConferenceForm()
        conference = conference_repository.get_conference(id)
        return render_template('conferences/details.html',
                               conference=conference, delete_conference_form=delete_conference_form)
    except IndexError:
        abort(404)


@blueprint.route('/create', methods=['GET', 'POST'])
def create():
    form = NewConferenceForm()
    if form.validate_on_submit():
        kwargs = {
            'short_name': str(form.short_name.data),
            'long_name': str(form.long_name.data),
            'first_season_year': int(form.first_season_year.data),
            'last_season_year': form.last_season_year.data,
        }
        try:
            conference_repository.add_conference(**kwargs)
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
    conference = conference_repository.get_conference(id)
    if conference:
        form = EditConferenceForm()
        if form.validate_on_submit():
            kwargs = {
                'id': id,
                'short_name': str(form.short_name.data),
                'long_name': str(form.long_name.data),
                'league_name': str(form.league_name.data),
                'first_season_year': int(form.first_season_year.data),
                'last_season_year': form.last_season_year.data,
            }
            try:
                conference_repository.update_conference(**kwargs)
                flash(f"Item {form.year.data} has been successfully updated.", 'success')
                return redirect(url_for('conference.details', id=id))
            except ValueError as err:
                return _handle_error(err, 'conferences/edit.html', form, conference=conference)
            except IntegrityError as err:
                return _handle_error(err, 'conferences/edit.html', form, conference=conference)
        else:
            form.short_name.data = conference.short_name
            form.long_name.data = conference.long_name
            form.league_name.data = conference.league_name
            form.first_season_year.data = conference.first_season_year
            form.last_season_year.data = conference.last_season_year

            if form.errors:
                flash(f"{form.errors}", 'danger')

            return render_template('conferences/edit.html', conference=conference, form=form)
    else:
        abort(404)


@blueprint.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id: int):
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
