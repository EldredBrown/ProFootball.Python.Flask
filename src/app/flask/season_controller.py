from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

from app.data.repositories.season_repository import SeasonRepository
from app.flask.forms.season import NewSeasonForm, EditSeasonForm, DeleteSeasonForm

blueprint = Blueprint('season', __name__)

season_repository = SeasonRepository()


@blueprint.route('/')
def index():
    seasons = season_repository.get_seasons()
    return render_template('seasons/index.html', seasons=seasons)


@blueprint.route('/details/<int:id>')
def details(id: int):
    try:
        delete_season_form = DeleteSeasonForm()
        season = season_repository.get_season(id)
        return render_template('seasons/details.html',
                               season=season, delete_season_form=delete_season_form)
    except IndexError:
        abort(404)


@blueprint.route('/create', methods=['GET', 'POST'])
def create():
    form = NewSeasonForm()
    if form.validate_on_submit():
        kwargs = {
            'year': int(form.year.data),
            'num_of_weeks_scheduled': int(form.num_of_weeks_scheduled.data),
            'num_of_weeks_completed': int(form.num_of_weeks_completed.data),
        }
        try:
            season_repository.add_season(**kwargs)
            flash(f"Item {form.year.data} has been successfully submitted.", 'success')
            return redirect(url_for('season.index'))
        except ValueError as err:
            flash(str(err), 'danger')
            return render_template('seasons/create.html', form=form)
    else:
        if form.errors:
            flash(f"{form.errors}", 'danger')

        return render_template('seasons/create.html', form=form)


@blueprint.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id: int):
    season = season_repository.get_season(id)
    if season:
        form = EditSeasonForm()
        if form.validate_on_submit():
            kwargs = {
                'id': id,
                'year': int(form.year.data),
                'num_of_weeks_scheduled': int(form.num_of_weeks_scheduled.data),
                'num_of_weeks_completed': int(form.num_of_weeks_completed.data)
            }
            try:
                season_repository.update_season(**kwargs)
                flash(f"Item {form.year.data} has been successfully updated.", 'success')
                return redirect(url_for('season.details', id=id))
            except ValueError as err:
                flash(str(err), 'danger')
                return render_template('seasons/edit.html', season=season, form=form)
        else:
            form.year.data = season.year
            form.num_of_weeks_scheduled.data = season.num_of_weeks_scheduled
            form.num_of_weeks_completed.data = season.num_of_weeks_completed

            if form.errors:
                flash(f"{form.errors}", 'danger')

            return render_template('seasons/edit.html', season=season, form=form)
    else:
        abort(404)


@blueprint.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id: int):
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
