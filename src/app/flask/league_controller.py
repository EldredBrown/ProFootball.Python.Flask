from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

from app.data.models.league import League
from app.data.repositories.league_repository import LeagueRepository
from app.flask.forms.league import NewLeagueForm, EditLeagueForm, DeleteLeagueForm

blueprint = Blueprint('league', __name__)

league_repository = LeagueRepository()


@blueprint.route('/')
def index():
    leagues = league_repository.get_leagues()
    return render_template('leagues/index.html', leagues=leagues)


@blueprint.route('/details/<int:id>')
def details(id: int):
    try:
        delete_league_form = DeleteLeagueForm()
        league = league_repository.get_league(id)
        return render_template('leagues/details.html',
                               league=league, delete_league_form=delete_league_form)
    except IndexError:
        abort(404)


@blueprint.route('/create', methods=['GET', 'POST'])
def create():
    form = NewLeagueForm()
    if form.validate_on_submit():
        league = League(
            short_name=str(form.short_name.data),
            long_name=str(form.long_name.data),
            first_season_year=int(form.first_season_year.data),
            last_season_year=int(form.last_season_year.data)
        )
        league_repository.add_league(league)
        flash(f"Item {form.year.data} has been successfully submitted.", 'success')
        return redirect(url_for('index'))
    else:
        if form.errors:
            flash(f"{form.errors}", 'danger')

        return render_template('leagues/create.html', form=form)


@blueprint.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id: int):
    league = league_repository.get_league(id)
    if league:
        form = EditLeagueForm()

        if form.validate_on_submit():
            new_league = League(
                id=id,
                short_name=form.short_name.data,
                long_name=form.long_name.data,
                first_season_year=form.first_season_year.data,
                last_season_year=form.last_season_year.data
            )
            league_repository.update_league(new_league)
            flash(f"Item {form.year.data} has been successfully updated.", 'success')
            return redirect(url_for('league.details', id=id))
        else:
            form.short_name.data = league.short_name
            form.long_name.data = league.long_name
            form.first_season_year.data = league.first_season_year
            form.last_season_year.data = league.last_season_year

            if form.errors:
                flash(f"{form.errors}", 'danger')

            return render_template('leagues/edit.html', league=league, form=form)
    else:
        abort(404)


@blueprint.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id: int):
    league = league_repository.get_league(id)
    try:
        if request.method == 'POST':
            league_repository.delete_league(id)
            flash(f"League {league.year} has been successfully deleted.", 'success')
            return redirect(url_for('index'))
        else:
            return render_template('leagues/delete.html', league=league)
    except IndexError:
        abort(404)
