from typing import Optional
from unittest.mock import patch, MagicMock

import pytest

from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound

import app.flask.association_controller as mod

from app.data.models.association import Association
from app.data.models.season import Season
from app.data.repositories.association_repository import AssociationRepository
from test_app import create_app


@pytest.fixture()
def test_app():
    return create_app()


@patch('app.flask.association_controller.render_template')
@patch('app.flask.association_controller.injector')
def test_index_should_render_association_index_template(fake_injector, fake_render_template):
    # Arrange
    fake_association_repository = _set_up_index_and_details(fake_injector)

    # Act
    result = mod.index()

    # Assert
    fake_injector.get.assert_called_once_with(AssociationRepository)
    fake_association_repository.get_associations.assert_called_once()
    fake_render_template.assert_called_once_with(
        'associations/index.html', associations=fake_association_repository.get_associations.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.association_controller.render_template')
@patch('app.flask.association_controller.injector')
@patch('app.flask.association_controller.DeleteAssociationForm')
def test_details_when_association_found_should_render_association_details_template(
        fake_form, fake_injector, fake_render_template
):
    # Arrange
    fake_association_repository = _set_up_index_and_details(fake_injector)

    # Act
    id = 1
    result = mod.details(id)

    # Assert
    fake_form.assert_called_once()
    fake_injector.get.assert_called_once_with(AssociationRepository)
    fake_association_repository.get_association.assert_called_once_with(id)
    fake_render_template.assert_called_once_with(
        'associations/details.html',
        association=fake_association_repository.get_association.return_value,
        form=fake_form.return_value
    )
    assert result == fake_render_template.return_value


@patch('app.flask.association_controller.injector')
@patch('app.flask.association_controller.DeleteAssociationForm')
def test_details_when_association_not_found_should_abort_with_404_error(fake_form, fake_injector):
    # Arrange
    err = IndexError()
    _ = _set_up_index_and_details(fake_injector, err=err)

    # Act
    with pytest.raises(NotFound):
        _ = mod.details(1)


def _set_up_index_and_details(fake_injector, err: Optional[Exception]=None) -> MagicMock:
    fake_association_repository = MagicMock(AssociationRepository)
    fake_association_repository.get_association.side_effect = err
    fake_injector.get.return_value = fake_association_repository

    return fake_association_repository


@patch('app.flask.association_controller.render_template')
@patch('app.flask.association_controller.flash')
@patch('app.flask.association_controller.NewAssociationForm')
def test_create_when_form_not_submitted_and_no_form_errors_should_render_create_template(
        fake_form, fake_flash, fake_render_template
):
    # Arrange
    _set_up_create_get(fake_form)

    # Act
    result = mod.create()

    # Assert
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    fake_flash.assert_not_called()
    fake_render_template('associations/create.html', form=fake_form.return_value)
    assert result is fake_render_template.return_value


@patch('app.flask.association_controller.render_template')
@patch('app.flask.association_controller.flash')
@patch('app.flask.association_controller.NewAssociationForm')
def test_create_when_form_not_submitted_and_form_errors_should_flash_errors_and_render_create_template(
        fake_form, fake_flash, fake_render_template
):
    # Arrange
    errors = 'errors'
    _set_up_create_get(fake_form, errors=errors)

    # Act
    result = mod.create()

    # Assert
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    fake_flash.assert_called_once_with(f"{errors}", 'danger')
    fake_render_template('associations/create.html', form=fake_form.return_value)
    assert result is fake_render_template.return_value


def _set_up_create_get(fake_form, errors: Optional[str]=None) -> None:
    form = fake_form.return_value
    form.validate_on_submit.return_value = False
    form.errors = errors


@patch('app.flask.association_controller.redirect')
@patch('app.flask.association_controller.url_for')
@patch('app.flask.association_controller.flash')
@patch('app.flask.association_controller.injector')
@patch('app.flask.association_controller.association_factory')
@patch('app.flask.association_controller.NewAssociationForm')
def test_create_when_form_submitted_and_no_errors_caught_should_flash_success_message_and_redirect_to_association_index(
        fake_form, fake_association_factory, fake_injector,
        fake_flash, fake_url_for, fake_redirect
):
    # Arrange
    association, fake_association_repository = _set_up_create_post(fake_injector, fake_form, fake_association_factory)

    # Act
    result = mod.create()

    # Assert
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    view_kwargs = {
        'long_name': association.long_name,
        'short_name': association.short_name,
        'parent_name': association.parent.short_name,
        'first_season_year': association.first_season_year,
        'last_season_year': association.last_season_year,
    }
    fake_association_factory.create_association.assert_called_once_with(**view_kwargs)
    fake_injector.get.assert_called_once_with(AssociationRepository)
    fake_association_repository.add_association.assert_called_once_with(association)
    fake_flash(f"Item {association.short_name} has been successfully submitted.", 'success')
    fake_url_for.assert_called_once_with('association.index')
    fake_redirect.assert_called_once_with(fake_url_for.return_value)
    assert result is fake_redirect.return_value


@patch('app.flask.association_controller.render_template')
@patch('app.flask.association_controller.flash')
@patch('app.flask.association_controller.injector')
@patch('app.flask.association_controller.association_factory')
@patch('app.flask.association_controller.NewAssociationForm')
def test_create_when_form_submitted_and_value_error_caught_should_flash_error_message_and_render_create_template(
        fake_form, fake_association_factory, fake_injector,
        fake_flash, fake_render_template
):
    # Arrange
    err = ValueError()
    association, fake_association_repository = (
        _set_up_create_post(fake_injector, fake_form, fake_association_factory, err=err)
    )

    # Act
    result = mod.create()

    # Assert
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    kwargs = {
        'long_name': association.long_name,
        'short_name': association.short_name,
        'parent_name': association.parent.short_name,
        'first_season_year': association.first_season_year,
        'last_season_year': association.last_season_year,
    }
    fake_association_factory.create_association.assert_called_once_with(**kwargs)
    fake_injector.get.assert_called_once_with(AssociationRepository)
    fake_association_repository.add_association.assert_called_once_with(association)
    fake_flash.assert_called_once_with(str(err), 'danger')
    fake_render_template.assert_called_once_with(
        'associations/create.html', association=None, form=fake_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.association_controller.render_template')
@patch('app.flask.association_controller.flash')
@patch('app.flask.association_controller.injector')
@patch('app.flask.association_controller.association_factory')
@patch('app.flask.association_controller.NewAssociationForm')
def test_create_when_form_submitted_and_integrity_error_caught_for_primary_key_constraint_violation_on_id_should_flash_error_message_and_render_create_template(
        fake_form, fake_association_factory, fake_injector,
        fake_flash, fake_render_template, test_app
):
    # Arrange
    err = IntegrityError(
        'statement', 'params',
        Exception("Violation of PRIMARY KEY constraint")
    )
    association, fake_association_repository = (
        _set_up_create_post(fake_injector, fake_form, fake_association_factory, err=err)
    )

    # Act
    with test_app.test_request_context('/associations/create', method='POST'):
        result = mod.create()

    # Assert
    kwargs = {
        'long_name': "Association",
        'short_name': "A",
        'parent_name': "P",
        'first_season_year': 1920,
        'last_season_year': 1922,
    }

    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    fake_association_factory.create_association.assert_called_once_with(**kwargs)
    fake_injector.get.assert_called_once_with(AssociationRepository)
    fake_association_repository.add_association.assert_called_once_with(association)
    fake_flash.assert_called_once_with("An association with the same id already exists.", 'danger')
    fake_render_template.assert_called_once_with(
        'associations/create.html', form=fake_form.return_value, association=None
    )
    assert result is fake_render_template.return_value


@patch('app.flask.association_controller.render_template')
@patch('app.flask.association_controller.flash')
@patch('app.flask.association_controller.injector')
@patch('app.flask.association_controller.association_factory')
@patch('app.flask.association_controller.NewAssociationForm')
def test_create_when_form_submitted_and_integrity_error_caught_for_unique_key_constraint_violation_on_long_name_should_flash_error_message_and_render_create_template(
        fake_form, fake_association_factory, fake_injector,
        fake_flash, fake_render_template, test_app
):
    # Arrange
    err = IntegrityError(
        'statement', 'params',
        Exception("Violation of UNIQUE KEY constraint 'UQ_Association_LongName'")
    )
    association, fake_association_repository = (
        _set_up_create_post(fake_injector, fake_form, fake_association_factory, err=err)
    )

    # Act
    with test_app.test_request_context('/associations/create', method='POST'):
        result = mod.create()

    # Assert
    kwargs = {
        'long_name': "Association",
        'short_name': "A",
        'parent_name': "P",
        'first_season_year': 1920,
        'last_season_year': 1922,
    }

    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    fake_association_factory.create_association.assert_called_once_with(**kwargs)
    fake_injector.get.assert_called_once_with(AssociationRepository)
    fake_association_repository.add_association.assert_called_once_with(association)
    fake_flash.assert_called_once_with(
        "An association with the same long name already exists.", 'danger'
    )
    fake_render_template.assert_called_once_with(
        'associations/create.html', form=fake_form.return_value, association=None
    )
    assert result is fake_render_template.return_value


@patch('app.flask.association_controller.render_template')
@patch('app.flask.association_controller.flash')
@patch('app.flask.association_controller.injector')
@patch('app.flask.association_controller.association_factory')
@patch('app.flask.association_controller.NewAssociationForm')
def test_create_when_form_submitted_and_integrity_error_caught_for_unique_key_constraint_violation_on_short_name_should_flash_error_message_and_render_create_template(
        fake_form, fake_association_factory, fake_injector,
        fake_flash, fake_render_template, test_app
):
    # Arrange
    err = IntegrityError(
        'statement', 'params',
        Exception("Violation of UNIQUE KEY constraint 'UQ_Association_ShortName'")
    )
    association, fake_association_repository = (
        _set_up_create_post(fake_injector, fake_form, fake_association_factory, err=err)
    )

    # Act
    with test_app.test_request_context('/associations/create', method='POST'):
        result = mod.create()

    # Assert
    kwargs = {
        'long_name': "Association",
        'short_name': "A",
        'parent_name': "P",
        'first_season_year': 1920,
        'last_season_year': 1922,
    }

    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    fake_association_factory.create_association.assert_called_once_with(**kwargs)
    fake_injector.get.assert_called_once_with(AssociationRepository)
    fake_association_repository.add_association.assert_called_once_with(association)
    fake_flash.assert_called_once_with(
        "An association with the same short name already exists.", 'danger'
    )
    fake_render_template.assert_called_once_with(
        'associations/create.html', form=fake_form.return_value, association=None
    )
    assert result is fake_render_template.return_value


@patch('app.flask.association_controller.render_template')
@patch('app.flask.association_controller.flash')
@patch('app.flask.association_controller.injector')
@patch('app.flask.association_controller.association_factory')
@patch('app.flask.association_controller.NewAssociationForm')
def test_create_when_form_submitted_and_integrity_error_caught_for_conflict_with_foreign_key_constraint_on_season_year_should_flash_error_message_and_render_create_template(
        fake_form, fake_association_factory, fake_injector,
        fake_flash, fake_render_template, test_app
):
    # Arrange
    err = IntegrityError(
        'statement', 'params',
        Exception("The INSERT statement conflicted with the FOREIGN KEY constraint 'FK_Association_Season_FirstSeasonYear'")
    )
    association, fake_association_repository = (
        _set_up_create_post(fake_injector, fake_form, fake_association_factory, err=err)
    )

    # Act
    with test_app.test_request_context('/associations/create', method='POST'):
        result = mod.create()

    # Assert
    kwargs = {
        'long_name': "Association",
        'short_name': "A",
        'parent_name': "P",
        'first_season_year': 1920,
        'last_season_year': 1922,
    }

    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    fake_association_factory.create_association.assert_called_once_with(**kwargs)
    fake_injector.get.assert_called_once_with(AssociationRepository)
    fake_association_repository.add_association.assert_called_once_with(association)
    fake_flash.assert_called_once_with("FOREIGN KEY constraint violation on first season year.", 'danger')
    fake_render_template.assert_called_once_with(
        'associations/create.html', form=fake_form.return_value, association=None
    )
    assert result is fake_render_template.return_value


@patch('app.flask.association_controller.render_template')
@patch('app.flask.association_controller.flash')
@patch('app.flask.association_controller.injector')
@patch('app.flask.association_controller.association_factory')
@patch('app.flask.association_controller.NewAssociationForm')
def test_create_when_form_submitted_and_integrity_error_caught_for_something_else_should_flash_error_message_and_render_create_template(
        fake_form, fake_association_factory, fake_injector,
        fake_flash, fake_render_template, test_app
):
    # Arrange
    err = IntegrityError(
        'statement', 'params',
        Exception("Something else")
    )
    association, fake_association_repository = (
        _set_up_create_post(fake_injector, fake_form, fake_association_factory, err=err)
    )

    # Act
    with test_app.test_request_context('/associations/create', method='POST'):
        result = mod.create()

    # Assert
    kwargs = {
        'long_name': "Association",
        'short_name': "A",
        'parent_name': "P",
        'first_season_year': 1920,
        'last_season_year': 1922,
    }

    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    fake_association_factory.create_association.assert_called_once_with(**kwargs)
    fake_injector.get.assert_called_once_with(AssociationRepository)
    fake_association_repository.add_association.assert_called_once_with(association)
    fake_flash.assert_called_once_with("An unexpected error occurred.", 'danger')
    fake_render_template.assert_called_once_with(
        'associations/create.html', form=fake_form.return_value, association=None
    )
    assert result is fake_render_template.return_value


def _set_up_create_post(
        fake_injector, fake_form, fake_association_factory,
        err: Optional[Exception]=None
) -> tuple[Association, MagicMock]:
    association = Association(
        id=2,
        long_name="Association",
        short_name="A",
        parent_id=1,
        parent=Association(id=1, long_name="Parent", short_name="P", parent_id=None),
        first_season_year=1920,
        last_season_year=1922,
    )

    form = fake_form.return_value
    form.validate_on_submit.return_value = True
    form.long_name.data = "Association"
    form.short_name.data = "A"
    form.parent_name.data = "P"
    form.first_season_year.data = 1920
    form.last_season_year.data = 1922

    fake_association_factory.create_association.return_value = association

    fake_association_repository = MagicMock(AssociationRepository)
    fake_association_repository.add_association.side_effect = err
    fake_injector.get.return_value = fake_association_repository

    return association, fake_association_repository


@patch('app.flask.association_controller.copy')
@patch('app.flask.association_controller.injector')
def test_edit_when_association_not_found_should_abort_with_404_error(fake_injector, fake_copy):
    # Arrange
    old_association_copy = None
    old_association, fake_association_repository = (
        _set_up_edit(fake_injector, fake_copy, old_association_copy=old_association_copy)
    )

    # Act
    id = 1
    with pytest.raises(NotFound):
        result = mod.edit(id)

    # Assert
    fake_injector.get.assert_called_once_with(AssociationRepository)
    fake_association_repository.get_association.assert_called_once_with(id)
    fake_copy.deepcopy.assert_called_once_with(old_association)


@patch('app.flask.association_controller.render_template')
@patch('app.flask.association_controller.flash')
@patch('app.flask.association_controller.EditAssociationForm')
@patch('app.flask.association_controller.copy')
@patch('app.flask.association_controller.injector')
def test_edit_when_association_found_and_form_not_submitted_and_no_form_errors_should_render_edit_template(
        fake_injector, fake_copy, fake_form, fake_flash,
        fake_render_template
):
    # Arrange
    old_association, old_association_copy, fake_association_repository = (
        _set_up_edit_get(fake_injector, fake_copy, fake_form)
    )

    # Act
    id = 1
    result = mod.edit(id)

    # Assert
    fake_injector.get.assert_called_once_with(AssociationRepository)
    fake_association_repository.get_association.assert_called_once_with(id)
    fake_copy.deepcopy.assert_called_once_with(old_association)
    fake_form.assert_called_once()
    assert fake_form.return_value.long_name.data == old_association_copy.long_name
    assert fake_form.return_value.short_name.data == old_association_copy.short_name
    assert fake_form.return_value.parent_name.data == old_association_copy.parent.short_name
    assert fake_form.return_value.first_season_year.data == old_association_copy.first_season_year
    assert fake_form.return_value.last_season_year.data == old_association_copy.last_season_year
    fake_form.return_value.validate_on_submit.assert_called_once()
    fake_flash.assert_not_called()
    fake_render_template.assert_called_once_with(
        'associations/edit.html', association=old_association_copy, form=fake_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.association_controller.render_template')
@patch('app.flask.association_controller.flash')
@patch('app.flask.association_controller.EditAssociationForm')
@patch('app.flask.association_controller.copy')
@patch('app.flask.association_controller.injector')
def test_edit_when_association_found_and_form_not_submitted_and_form_errors_should_flash_errors_and_render_edit_template(
        fake_injector, fake_copy, fake_form, fake_flash,
        fake_render_template
):
    # Arrange
    errors = 'errors'
    old_association, old_association_copy, fake_association_repository = (
        _set_up_edit_get(fake_injector, fake_copy, fake_form, errors=errors)
    )

    # Act
    id = 1
    result = mod.edit(id)

    # Assert
    fake_injector.get.assert_called_once_with(AssociationRepository)
    fake_association_repository.get_association.assert_called_once_with(id)
    fake_copy.deepcopy.assert_called_once_with(old_association)
    fake_form.assert_called_once()
    assert fake_form.return_value.long_name.data == old_association_copy.long_name
    assert fake_form.return_value.short_name.data == old_association_copy.short_name
    assert fake_form.return_value.parent_name.data == old_association_copy.parent.short_name
    assert fake_form.return_value.first_season_year.data == old_association_copy.first_season_year
    assert fake_form.return_value.last_season_year.data == old_association_copy.last_season_year
    fake_form.return_value.validate_on_submit.assert_called_once()
    fake_flash.assert_called_once_with(f"{errors}", 'danger')
    fake_render_template.assert_called_once_with(
        'associations/edit.html', association=old_association_copy, form=fake_form.return_value
    )
    assert result is fake_render_template.return_value


def _set_up_edit_get(
        fake_injector, fake_copy, fake_form, errors: Optional[str]=None
) -> tuple[Association, Association, MagicMock]:
    old_association_copy = Association(
        id=2,
        long_name="Old Association",
        short_name="OA",
        parent_id=1,
        parent=Association(id=1, long_name="Parent", short_name="P", parent_id=None),
        first_season_year=1920,
        first_season=Season(year=1920),
        last_season_year=1922,
        last_season=Season(year=1922)
    )
    old_association, fake_association_repository = (
        _set_up_edit(fake_injector, fake_copy, old_association_copy=old_association_copy)
    )

    form = fake_form.return_value
    form.validate_on_submit.return_value = False
    form.errors = errors

    return old_association, old_association_copy, fake_association_repository


@patch('app.flask.association_controller.redirect')
@patch('app.flask.association_controller.url_for')
@patch('app.flask.association_controller.flash')
@patch('app.flask.association_controller.association_factory')
@patch('app.flask.association_controller.EditAssociationForm')
@patch('app.flask.association_controller.copy')
@patch('app.flask.association_controller.injector')
def test_edit_when_association_found_and_form_submitted_and_no_errors_caught_should_flash_success_message_and_redirect_to_association_details(
        fake_injector, fake_copy, fake_form,
        fake_association_factory, fake_flash,
        fake_url_for, fake_redirect
):
    # Arrange
    old_association, old_association_copy, new_association, fake_association_repository = (
        _set_up_edit_post(fake_injector, fake_copy, fake_form, fake_association_factory)
    )

    # Act
    id = 1
    result = mod.edit(id)

    # Assert
    fake_injector.get.assert_called_once_with(AssociationRepository)
    fake_association_repository.get_association.assert_called_once_with(id)
    fake_copy.deepcopy.assert_called_once_with(old_association)
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    kwargs = {
        'id': id,
        'long_name': new_association.long_name,
        'short_name': new_association.short_name,
        'parent_name': new_association.parent.short_name,
        'first_season_year': new_association.first_season_year,
        'last_season_year': new_association.last_season_year,
    }
    fake_association_factory.create_association.assert_called_once_with(**kwargs)
    fake_association_repository.update_association.assert_called_once_with(new_association)
    fake_flash.assert_called_once_with(
        f"Item {fake_form.return_value.short_name.data} has been successfully updated.", 'success'
    )
    fake_url_for.assert_called_once_with('association.details', id=id)
    fake_redirect.assert_called_once_with(fake_url_for.return_value)
    assert result is fake_redirect.return_value


@patch('app.flask.association_controller.render_template')
@patch('app.flask.association_controller.flash')
@patch('app.flask.association_controller.association_factory')
@patch('app.flask.association_controller.EditAssociationForm')
@patch('app.flask.association_controller.copy')
@patch('app.flask.association_controller.injector')
def test_edit_when_association_found_and_form_submitted_and_value_error_caught_should_flash_error_message_and_render_edit_template(
        fake_injector, fake_copy, fake_form,
        fake_association_factory, fake_flash,
        fake_render_template
):
    # Arrange
    err = ValueError()
    old_association, old_association_copy, new_association, fake_association_repository = (
        _set_up_edit_post(fake_injector, fake_copy, fake_form, fake_association_factory, err=err)
    )

    # Act
    id = 1
    result = mod.edit(id)

    # Assert
    fake_injector.get.assert_called_once_with(AssociationRepository)
    fake_association_repository.get_association.assert_called_once_with(id)
    fake_copy.deepcopy.assert_called_once_with(old_association)
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    kwargs = {
        'id': id,
        'long_name': new_association.long_name,
        'short_name': new_association.short_name,
        'parent_name': new_association.parent.short_name,
        'first_season_year': new_association.first_season_year,
        'last_season_year': new_association.last_season_year,
    }
    fake_association_factory.create_association.assert_called_once_with(**kwargs)
    fake_flash.assert_called_once_with(str(err), 'danger')
    fake_render_template.assert_called_once_with(
        'associations/edit.html', association=old_association_copy, form=fake_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.association_controller.render_template')
@patch('app.flask.association_controller.flash')
@patch('app.flask.association_controller.association_factory')
@patch('app.flask.association_controller.EditAssociationForm')
@patch('app.flask.association_controller.copy')
@patch('app.flask.association_controller.injector')
def test_edit_when_association_found_and_form_submitted_and_integrity_error_caught_for_unique_key_constraint_violation_on_long_name_should_flash_error_message_and_render_edit_template(
        fake_injector, fake_copy, fake_form,
        fake_association_factory, fake_flash,
        fake_render_template
):
    # Arrange
    err = IntegrityError(
        'statement', 'params',
        Exception("Violation of UNIQUE KEY constraint 'UQ_Association_LongName'")
    )
    old_association, old_association_copy, new_association, fake_association_repository = (
        _set_up_edit_post(fake_injector, fake_copy, fake_form, fake_association_factory, err=err)
    )

    # Act
    id = 1
    result = mod.edit(id)

    # Assert
    fake_injector.get.assert_called_once_with(AssociationRepository)
    fake_association_repository.get_association.assert_called_once_with(id)
    fake_copy.deepcopy.assert_called_once_with(old_association)
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    kwargs = {
        'id': id,
        'long_name': new_association.long_name,
        'short_name': new_association.short_name,
        'parent_name': new_association.parent.short_name,
        'first_season_year': new_association.first_season_year,
        'last_season_year': new_association.last_season_year,
    }
    fake_association_factory.create_association.assert_called_once_with(**kwargs)
    fake_flash.assert_called_once_with("An association with the same long name already exists.", 'danger')
    fake_render_template.assert_called_once_with(
        'associations/edit.html', association=old_association_copy, form=fake_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.association_controller.render_template')
@patch('app.flask.association_controller.flash')
@patch('app.flask.association_controller.association_factory')
@patch('app.flask.association_controller.EditAssociationForm')
@patch('app.flask.association_controller.copy')
@patch('app.flask.association_controller.injector')
def test_edit_when_association_found_and_form_submitted_and_integrity_error_caught_for_unique_key_constraint_violation_on_short_name_should_flash_error_message_and_render_edit_template(
        fake_injector, fake_copy, fake_form,
        fake_association_factory, fake_flash,
        fake_render_template
):
    # Arrange
    err = IntegrityError(
        'statement', 'params',
        Exception("Violation of UNIQUE KEY constraint 'UQ_Association_ShortName'")
    )
    old_association, old_association_copy, new_association, fake_association_repository = (
        _set_up_edit_post(fake_injector, fake_copy, fake_form, fake_association_factory, err=err)
    )

    # Act
    id = 1
    result = mod.edit(id)

    # Assert
    fake_injector.get.assert_called_once_with(AssociationRepository)
    fake_association_repository.get_association.assert_called_once_with(id)
    fake_copy.deepcopy.assert_called_once_with(old_association)
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    kwargs = {
        'id': id,
        'long_name': new_association.long_name,
        'short_name': new_association.short_name,
        'parent_name': new_association.parent.short_name,
        'first_season_year': new_association.first_season_year,
        'last_season_year': new_association.last_season_year,
    }
    fake_association_factory.create_association.assert_called_once_with(**kwargs)
    fake_flash.assert_called_once_with("An association with the same short name already exists.", 'danger')
    fake_render_template.assert_called_once_with(
        'associations/edit.html', association=old_association_copy, form=fake_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.association_controller.render_template')
@patch('app.flask.association_controller.flash')
@patch('app.flask.association_controller.association_factory')
@patch('app.flask.association_controller.EditAssociationForm')
@patch('app.flask.association_controller.copy')
@patch('app.flask.association_controller.injector')
def test_edit_when_association_found_and_form_submitted_and_integrity_error_caught_for_conflict_with_foreign_key_constraint_on_first_season_year_should_flash_error_message_and_render_edit_template(
        fake_injector, fake_copy, fake_form,
        fake_association_factory, fake_flash,
        fake_render_template
):
    # Arrange
    err = IntegrityError(
        'statement', 'params',
        Exception("The UPDATE statement conflicted with the FOREIGN KEY constraint 'FK_Association_Season_FirstSeasonYear'")
    )
    old_association, old_association_copy, new_association, fake_association_repository = (
        _set_up_edit_post(fake_injector, fake_copy, fake_form, fake_association_factory, err=err)
    )

    # Act
    id = 1
    result = mod.edit(id)

    # Assert
    fake_injector.get.assert_called_once_with(AssociationRepository)
    fake_association_repository.get_association.assert_called_once_with(id)
    fake_copy.deepcopy.assert_called_once_with(old_association)
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    kwargs = {
        'id': id,
        'long_name': new_association.long_name,
        'short_name': new_association.short_name,
        'parent_name': new_association.parent.short_name,
        'first_season_year': new_association.first_season_year,
        'last_season_year': new_association.last_season_year,
    }
    fake_association_factory.create_association.assert_called_once_with(**kwargs)
    fake_flash.assert_called_once_with("FOREIGN KEY constraint violation on first season year.", 'danger')
    fake_render_template.assert_called_once_with(
        'associations/edit.html', association=old_association_copy, form=fake_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.association_controller.render_template')
@patch('app.flask.association_controller.flash')
@patch('app.flask.association_controller.association_factory')
@patch('app.flask.association_controller.EditAssociationForm')
@patch('app.flask.association_controller.copy')
@patch('app.flask.association_controller.injector')
def test_edit_when_association_found_and_form_submitted_and_integrity_error_caught_for_something_else_should_flash_error_message_and_render_edit_template(
        fake_injector, fake_copy, fake_form,
        fake_association_factory, fake_flash,
        fake_render_template
):
    # Arrange
    err = IntegrityError(
        'statement', 'params',
        Exception("Something else")
    )
    old_association, old_association_copy, new_association, fake_association_repository = (
        _set_up_edit_post(fake_injector, fake_copy, fake_form, fake_association_factory, err=err)
    )

    # Act
    id = 1
    result = mod.edit(id)

    # Assert
    fake_injector.get.assert_called_once_with(AssociationRepository)
    fake_association_repository.get_association.assert_called_once_with(id)
    fake_copy.deepcopy.assert_called_once_with(old_association)
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    kwargs = {
        'id': id,
        'long_name': new_association.long_name,
        'short_name': new_association.short_name,
        'parent_name': new_association.parent.short_name,
        'first_season_year': new_association.first_season_year,
        'last_season_year': new_association.last_season_year,
    }
    fake_association_factory.create_association.assert_called_once_with(**kwargs)
    fake_flash.assert_called_once_with("An unexpected error occurred.", 'danger')
    fake_render_template.assert_called_once_with(
        'associations/edit.html', association=old_association_copy, form=fake_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.association_controller.association_factory')
@patch('app.flask.association_controller.EditAssociationForm')
@patch('app.flask.association_controller.copy')
@patch('app.flask.association_controller.injector')
def test_edit_when_association_found_and_form_submitted_and_index_error_caught_should_abort_with_404_error(
        fake_injector, fake_copy, fake_form,
        fake_association_factory
):
    # Arrange
    err = IndexError()
    old_association, old_association_copy, new_association, fake_association_repository = (
        _set_up_edit_post(fake_injector, fake_copy, fake_form, fake_association_factory, err=err)
    )

    # Act
    id = 1
    with pytest.raises(NotFound):
        _ = mod.edit(id)

    # Assert
    fake_injector.get.assert_called_once_with(AssociationRepository)
    fake_association_repository.get_association.assert_called_once_with(id)
    fake_copy.deepcopy.assert_called_once_with(old_association)
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    kwargs = {
        'id': id,
        'long_name': new_association.long_name,
        'short_name': new_association.short_name,
        'parent_name': new_association.parent.short_name,
        'first_season_year': new_association.first_season.year,
        'last_season_year': new_association.last_season.year,
    }
    fake_association_factory.create_association.assert_called_once_with(**kwargs)


def _set_up_edit_post(
        fake_injector, fake_copy, fake_form, fake_association_factory,
        err: Optional[Exception]=None
) -> tuple[Association, Association, Association, MagicMock]:
    old_association_copy = Association(
        id=2,
        long_name="Old Association",
        short_name="OA",
        parent_id=1,
        parent=Association(id=1, long_name="Parent", short_name="P", parent_id=None),
        first_season_year=1920,
        first_season=Season(year=1920),
        last_season_year=1922,
        last_season=Season(year=1922)
    )
    old_association, fake_association_repository = (
        _set_up_edit(fake_injector, fake_copy, old_association_copy=old_association_copy, err=err)
    )

    new_association = Association(
        id=2,
        long_name="New Association",
        short_name="NA",
        parent_id=1,
        parent=Association(id=1, long_name="Parent", short_name="P", parent_id=None),
        first_season_year=1920,
        first_season=Season(year=1920),
        last_season_year=1922,
        last_season=Season(year=1922)
    )
    form = fake_form.return_value
    form.long_name.data = new_association.long_name
    form.short_name.data = new_association.short_name
    form.parent_name.data = new_association.parent.short_name
    form.first_season_year.data = new_association.first_season.year
    form.last_season_year.data = new_association.last_season.year
    form.validate_on_submit.return_value = True

    fake_association_factory.create_association.return_value = new_association

    return old_association, old_association_copy, new_association, fake_association_repository


@patch('app.flask.association_controller.injector')
def test_delete_when_association_not_found_should_abort_with_404_error(fake_injector, test_app):
    # Arrange
    fake_association_repository = _set_up_delete(fake_injector)

    # Act
    id = 1
    with test_app.test_request_context(f'/associations/delete?id={id}', method='POST'):
        with pytest.raises(NotFound):
            _ = mod.delete(id)

    # Assert
    fake_injector.get.assert_called_once_with(AssociationRepository)
    fake_association_repository.get_association.assert_called_once_with(id)


@patch('app.flask.association_controller.render_template')
@patch('app.flask.association_controller.DeleteAssociationForm')
@patch('app.flask.association_controller.injector')
def test_delete_when_request_method_is_get_should_render_delete_template(
        fake_injector, fake_form, fake_render_template, test_app
):
    # Arrange
    association = Association()
    fake_association_repository = _set_up_delete(fake_injector, association=association)

    # Act
    id = 1
    with test_app.test_request_context(f'/associations/delete?id={id}', method='GET'):
        result = mod.delete(id)

    # Assert
    fake_form.assert_called_once()
    fake_injector.get.assert_called_once_with(AssociationRepository)
    fake_association_repository.get_association.assert_called_once_with(id)
    fake_render_template.assert_called_once_with(
        'associations/delete.html', association=association, form=fake_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.association_controller.redirect')
@patch('app.flask.association_controller.url_for')
@patch('app.flask.association_controller.flash')
@patch('app.flask.association_controller.injector')
def test_delete_when_request_method_is_post_and_association_found_should_flash_success_message_and_redirect_to_associations_index(
        fake_injector, fake_flash, fake_url_for,
        fake_redirect, test_app
):
    # Arrange
    id = 1
    association = Association(
        id=id,
        long_name="Association",
        short_name="A",
        parent_id=1,
        parent=Association(id=1, long_name="Parent", short_name="P", parent_id=None),
        first_season_year=1920,
        first_season=Season(year=1920),
        last_season_year=1922,
        last_season=Season(year=1922)
    )
    fake_association_repository = _set_up_delete(fake_injector, association=association)

    # Act
    with test_app.test_request_context('/associations/delete?id=1', method='POST'):
        result = mod.delete(id)

    # Assert
    fake_injector.get.assert_called_once_with(AssociationRepository)
    fake_association_repository.get_association.assert_called_once_with(id)
    fake_association_repository.delete_association.assert_called_once_with(id)
    fake_flash.assert_called_once_with(
        f"Association {association.short_name} has been successfully deleted.", 'success'
    )
    fake_url_for.assert_called_once_with('association.index')
    fake_redirect.assert_called_once_with(fake_url_for.return_value)
    assert result is fake_redirect.return_value


@patch('app.flask.association_controller.injector')
def test_delete_when_request_method_is_post_and_index_error_is_caught_should_abort_with_404_error(
        fake_injector, test_app
):
    # Arrange
    association = Association()
    err = IndexError()
    fake_association_repository = _set_up_delete(fake_injector, association=association, err=err)

    # Act
    id = 1
    with test_app.test_request_context(f'/associations/delete?id={id}', method='POST'):
        with pytest.raises(NotFound):
            _ = mod.delete(id)

    # Assert
    fake_injector.get.assert_called_once_with(AssociationRepository)
    fake_association_repository.get_association.assert_called_once_with(id)


def _set_up_delete(fake_injector, association: Optional[Association]=None, err: Optional[Exception]=None) \
        -> MagicMock:
    fake_association_repository = MagicMock(AssociationRepository)
    fake_association_repository.get_association.return_value = association
    fake_association_repository.delete_association.side_effect = err
    fake_injector.get.return_value = fake_association_repository

    return fake_association_repository


def _set_up_edit(
        fake_injector, fake_copy, old_association_copy: Optional[Association]=None,
        err: Optional[Exception]=None
) -> tuple[MagicMock, Association]:
    fake_association_repository = MagicMock(AssociationRepository)
    old_association = Association()
    fake_association_repository.get_association.return_value = old_association
    fake_association_repository.update_association.side_effect = err
    fake_injector.get.return_value = fake_association_repository

    fake_copy.deepcopy.return_value = old_association_copy

    return old_association, fake_association_repository
