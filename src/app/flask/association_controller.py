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
            return _handle_value_error(err, 'associations/create.html', form)
        except IntegrityError as err:
            return _handle_integrity_error(err, 'INSERT', 'associations/create.html', form)
    else:
        if form.errors:
            flash(f"{form.errors}", 'danger')

        return render_template('associations/create.html', form=form)


@blueprint.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id: int) -> Response | str:
    association_repository = injector.get(AssociationRepository)
    old_association = association_repository.get_association(id)
    old_association_copy = copy.deepcopy(old_association)
    if old_association_copy:
        form = EditAssociationForm()
        if form.validate_on_submit():
            try:
                new_association = _get_model_from_form(form, id)
                association_repository.update_association(new_association)
                flash(f"Item {form.short_name.data} has been successfully updated.", 'success')
                return redirect(url_for('association.details', id=id))
            except ValueError as err:
                return _handle_value_error(err, 'associations/edit.html', form, association=old_association_copy)
            except IntegrityError as err:
                return _handle_integrity_error(
                    err, 'UPDATE', 'associations/edit.html', form, association=old_association_copy
                )
            except IndexError:
                abort(404)
        else:
            _get_form_data_from_model(form, old_association_copy)
            if form.errors:
                flash(f"{form.errors}", 'danger')

            return render_template('associations/edit.html', association=old_association_copy, form=form)
    else:
        abort(404)


def _get_model_from_form(form: AssociationForm, id: int=None) -> Association:
    kwargs = _get_kwargs_from_form(form, id)
    association = association_factory.create_association(**kwargs)
    return association


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


def _handle_value_error(err: Any, template_name: str, form: AssociationForm, association: Association=None) -> str:
    flash(str(err), 'danger')
    return render_template(template_name, association=association, form=form)


def _handle_integrity_error(err: Any, sql_operation: str, template_name: str, form: AssociationForm, association: Association=None) -> str:
    if str(err.args[0]).find("Violation of PRIMARY KEY constraint") != -1:
        err_msg = "An association with the same id already exists."
    elif str(err.args[0]).find("Violation of UNIQUE KEY constraint 'UQ_Association_LongName'") != -1:
        err_msg = "An association with the same long name already exists."
    elif str(err.args[0]).find("Violation of UNIQUE KEY constraint 'UQ_Association_ShortName'") != -1:
        err_msg = "An association with the same short name already exists."
    elif str(err.args[0]).find(f"The {sql_operation} statement conflicted with the FOREIGN KEY constraint 'FK_Association_Season_FirstSeasonYear'") != -1:
        err_msg = "FOREIGN KEY constraint violation on first season year."
    else:
        err_msg = "An unexpected error occurred."

    flash(err_msg, 'danger')
    return render_template(template_name, association=association, form=form)


def _get_form_data_from_model(form: AssociationForm, association: Association) -> None:
    form.long_name.data = association.long_name
    form.short_name.data = association.short_name
    form.parent_name.data = None if association.parent is None else association.parent.short_name
    form.first_season_year.data = association.first_season_year
    form.last_season_year.data = association.last_season_year


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
