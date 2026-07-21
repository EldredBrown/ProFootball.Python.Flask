import copy

from typing import Any

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for, Response
from sqlalchemy.exc import IntegrityError

from app import injector
from app.data.factories import association_factory
from app.data.models.association import Association
from app.data.repositories.association_repository import AssociationRepository
from app.flask.forms.association_forms import NewAssociationForm, EditAssociationForm, DeleteAssociationForm, AssociationForm


blueprint = Blueprint('association', __name__)


@blueprint.route('/')
def index() -> str:
    association_repository = injector.get(AssociationRepository)
    associations = association_repository.get_associations()
    return render_template('associations/index.html', associations=associations)


@blueprint.route('/details/<int:id>')
def details(id: int) -> str:
    form = DeleteAssociationForm()
    try:
        association_repository = injector.get(AssociationRepository)
        association = association_repository.get_association(id)
        return render_template('associations/details.html', association=association, form=form)
    except IndexError:
        abort(404)


@blueprint.route('/create', methods=['GET', 'POST'])
def create() -> Response | str:
    form = NewAssociationForm()
    if form.validate_on_submit():
        try:
            new_association = _get_model_from_form(form)
            association_repository = injector.get(AssociationRepository)
            association_repository.add_association(new_association)
            flash(f"Item {form.short_name.data} has been successfully submitted.", 'success')
            return redirect(url_for('association.index'))
        except ValueError as err:
            return _handle_error(err, 'associations/create.html', form)
        except IntegrityError as err:
            return _handle_error(err, 'associations/create.html', form)
    else:
        if form.errors:
            flash(f"{form.errors}", 'danger')

        return render_template('associations/create.html', form=form)


@blueprint.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id: int) -> Response | str:
    association_repository = injector.get(AssociationRepository)
    association = association_repository.get_association(id)
    old_association = copy.deepcopy(association)
    if old_association:
        form = EditAssociationForm()
        if form.validate_on_submit():
            try:
                new_association = _get_model_from_form(form, id)
                association_repository.update_association(new_association)
                flash(f"Item {form.short_name.data} has been successfully updated.", 'success')
                return redirect(url_for('association.details', id=id))
            except ValueError as err:
                return _handle_error(err, 'associations/edit.html', form, association=old_association)
            except IntegrityError as err:
                return _handle_error(err, 'associations/edit.html', form, association=old_association)
            except IndexError:
                abort(404)
        else:
            _get_form_data_from_model(form, old_association)
            if form.errors:
                flash(f"{form.errors}", 'danger')

            return render_template('associations/edit.html', association=old_association, form=form)
    else:
        abort(404)


@blueprint.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id: int) -> Response | str:
    form = DeleteAssociationForm()
    try:
        association_repository = injector.get(AssociationRepository)
        association = association_repository.get_association(id)
        if not association:
            abort(404)

        if request.method == 'POST':
            association_repository.delete_association(id)
            flash(f"Association {association.short_name} has been successfully deleted.", 'success')
            return redirect(url_for('association.index'))
        else:
            return render_template('associations/delete.html', association=association, form=form)
    except IndexError:
        abort(404)


def _get_form_data_from_model(form: AssociationForm, association: Association) -> None:
    form.long_name.data = association.long_name
    form.short_name.data = association.short_name
    form.parent_name.data = None if association.parent is None else association.parent.short_name
    form.first_season_year.data = association.first_season_year
    form.last_season_year.data = association.last_season_year


def _get_kwargs_from_form(form: AssociationForm, id: int=None) -> dict[str, Any]:
    kwargs = {
        'long_name': str(form.long_name.data),
        'short_name': str(form.short_name.data),
        'parent_name': str(form.parent_name.data),
        'first_season_year': int(form.first_season_year.data),
        'last_season_year': None if form.last_season_year.data is None else int(form.last_season_year.data),
    }
    if id:
        kwargs['id'] = id
    return kwargs


def _get_model_from_form(form: AssociationForm, id: int=None) -> Association:
    kwargs = _get_kwargs_from_form(form, id)
    association = association_factory.create_association(**kwargs)
    return association


def _handle_error(err: Any, template_name: str, form: AssociationForm, association: Association=None) -> str:
    flash(str(err), 'danger')
    return render_template(template_name, form=form, association=association)
