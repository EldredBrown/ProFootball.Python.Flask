from unittest.mock import patch, MagicMock

import pytest

from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound

import app.flask.association_controller as mod

from app.data.models.association import Association
from app.data.repositories.association_repository import AssociationRepository
from test_app import create_app


@pytest.fixture()
def test_app():
    return create_app()


@patch('app.flask.association_controller.render_template')
@patch('app.flask.association_controller.injector')
def test_index_should_render_association_index_template(fake_injector, fake_render_template):
    # Arrange
    fake_association_repository = MagicMock(AssociationRepository)
    fake_injector.get.return_value = fake_association_repository

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
    fake_association_repository = MagicMock(AssociationRepository)
    fake_injector.get.return_value = fake_association_repository

    id = 1

    # Act
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
    fake_association_repository = MagicMock(AssociationRepository)
    fake_association_repository.get_association.side_effect = IndexError()
    fake_injector.get.return_value = fake_association_repository

    # Act
    with pytest.raises(NotFound):
        _ = mod.details(1)


@patch('app.flask.association_controller.render_template')
@patch('app.flask.association_controller.flash')
@patch('app.flask.association_controller.injector')
@patch('app.flask.association_controller.NewAssociationForm')
def test_create_when_form_not_submitted_and_no_form_errors_should_render_create_template(
        fake_form, fake_injector, fake_flash,
        fake_render_template
):
    # Arrange
    fake_form.return_value.validate_on_submit.return_value = False
    fake_form.return_value.errors = None

    fake_association_repository = MagicMock(AssociationRepository)
    fake_injector.get.return_value = fake_association_repository

    # Act
    result = mod.create()

    # Assert
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    fake_injector.get.assert_not_called()
    fake_association_repository.add_association.assert_not_called()
    fake_flash.assert_not_called()
    fake_render_template('associations/create.html', form=fake_form.return_value)
    assert result is fake_render_template.return_value


@patch('app.flask.association_controller.render_template')
@patch('app.flask.association_controller.flash')
@patch('app.flask.association_controller.injector')
@patch('app.flask.association_controller.NewAssociationForm')
def test_create_when_form_not_submitted_and_form_errors_should_flash_errors_and_render_create_template(
        fake_form, fake_injector, fake_flash,
        fake_render_template
):
    # Arrange
    fake_form.return_value.validate_on_submit.return_value = False

    errors = 'errors'
    fake_form.return_value.errors = errors

    fake_association_repository = MagicMock(AssociationRepository)
    fake_injector.get.return_value = fake_association_repository

    # Act
    result = mod.create()

    # Assert
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    fake_injector.get.assert_not_called()
    fake_association_repository.add_association.assert_not_called()
    fake_flash.assert_called_once_with(f"{errors}", 'danger')
    fake_render_template('associations/create.html', form=fake_form.return_value)
    assert result is fake_render_template.return_value


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
    model_kwargs = {
        'long_name': "Association",
        'short_name': "A",
        'parent_id': 1,
        'first_season_year': 1920,
        'last_season_year': 1921,
    }
    association = Association(**model_kwargs)
    association.parent = Association(id=1, long_name="Parent", short_name="P")

    fake_form.return_value.validate_on_submit.return_value = True
    fake_form.return_value.long_name.data = association.long_name
    fake_form.return_value.short_name.data = association.short_name
    fake_form.return_value.parent_name.data = association.parent.short_name
    fake_form.return_value.first_season_year.data = association.first_season_year
    fake_form.return_value.last_season_year.data = association.last_season_year

    fake_association_factory.create_association.return_value = association

    fake_association_repository = MagicMock(AssociationRepository)
    fake_injector.get.return_value = fake_association_repository

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
    model_kwargs = {
        'long_name': "Association",
        'short_name': "A",
        'parent_id': 1,
        'first_season_year': 1920,
        'last_season_year': 1921,
    }
    association = Association(**model_kwargs)
    association.parent = Association(id=1, long_name="Parent", short_name="P")

    fake_form.return_value.validate_on_submit.return_value = True
    fake_form.return_value.long_name.data = association.long_name
    fake_form.return_value.short_name.data = association.short_name
    fake_form.return_value.parent_name.data = association.parent.short_name
    fake_form.return_value.first_season_year.data = association.first_season_year
    fake_form.return_value.last_season_year.data = association.last_season_year

    fake_association_factory.create_association.return_value = association

    fake_association_repository = MagicMock(AssociationRepository)
    err = ValueError()
    fake_association_repository.add_association.side_effect = err
    fake_injector.get.return_value = fake_association_repository

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
def test_create_when_form_submitted_and_integrity_error_caught_should_flash_error_message_and_render_create_template(
        fake_form, fake_association_factory, fake_injector,
        fake_flash, fake_render_template
):
    # Arrange
    model_kwargs = {
        'long_name': "Association",
        'short_name': "A",
        'parent_id': 1,
        'first_season_year': 1920,
        'last_season_year': 1921,
    }
    association = Association(**model_kwargs)
    association.parent = Association(id=1, long_name="Parent", short_name="P")

    fake_form.return_value.validate_on_submit.return_value = True
    fake_form.return_value.long_name.data = association.long_name
    fake_form.return_value.short_name.data = association.short_name
    fake_form.return_value.parent_name.data = association.parent.short_name
    fake_form.return_value.first_season_year.data = association.first_season_year
    fake_form.return_value.last_season_year.data = association.last_season_year

    fake_association_factory.create_association.return_value = association

    fake_association_repository = MagicMock(AssociationRepository)
    err = IntegrityError('statement', 'params', Exception())
    fake_association_repository.add_association.side_effect = err
    fake_injector.get.return_value = fake_association_repository

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
    fake_flash.assert_called_once_with(str(err), 'danger')
    fake_render_template.assert_called_once_with(
        'associations/create.html', association=None, form=fake_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.association_controller.copy')
@patch('app.flask.association_controller.injector')
def test_edit_when_association_not_found_should_abort_with_404_error(fake_injector, fake_copy):
    # Arrange
    fake_association_repository = MagicMock(AssociationRepository)
    old_association = MagicMock(Association)
    fake_association_repository.get_association.return_value = old_association
    fake_injector.get.return_value = fake_association_repository

    old_association_copy = None
    fake_copy.deepcopy.return_value = old_association_copy

    id = 1

    # Act
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
    fake_association_repository = MagicMock(AssociationRepository)
    old_association = MagicMock(Association)
    fake_association_repository.get_association.return_value = old_association
    fake_injector.get.return_value = fake_association_repository

    old_association_copy = MagicMock(Association)
    old_association_copy.long_name = "Association"
    old_association_copy.short_name = "A"
    old_association_copy.parent = Association(id=1, long_name="Parent", short_name="P")
    old_association_copy.parent_id = 1
    old_association_copy.first_season_year = 1920
    old_association_copy.last_season_year = 1921
    fake_copy.deepcopy.return_value = old_association_copy

    fake_form.return_value.validate_on_submit.return_value = False
    fake_form.return_value.errors = None

    id = 1

    # Act
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
    fake_association_repository = MagicMock(AssociationRepository)
    old_association = MagicMock(Association)
    fake_association_repository.get_association.return_value = old_association
    fake_injector.get.return_value = fake_association_repository

    fake_form.return_value.validate_on_submit.return_value = False
    fake_form.return_value.errors = None

    old_association_copy = MagicMock(Association)
    old_association_copy.long_name = "Association"
    old_association_copy.short_name = "A"
    old_association_copy.parent = Association(id=1, long_name="Parent", short_name="P")
    old_association_copy.parent_id = 1
    old_association_copy.first_season_year = 1920
    old_association_copy.last_season_year = 1921
    fake_copy.deepcopy.return_value = old_association_copy

    errors = 'errors'
    fake_form.return_value.errors = errors

    id = 1

    # Act
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


@patch('app.flask.association_controller.redirect')
@patch('app.flask.association_controller.url_for')
@patch('app.flask.association_controller.flash')
@patch('app.flask.association_controller.association_factory')
@patch('app.flask.association_controller.EditAssociationForm')
@patch('app.flask.association_controller.copy')
@patch('app.flask.association_controller.injector')
def test_edit_when_association_found_and_form_submitted_and_no_errors_caught_should_flash_success_message_and_redirect_to_association_details(
        fake_injector, fake_copy, fake_form,
        fake_association_factory, fake_flash, fake_url_for,
        fake_redirect
):
    # Arrange
    id = 1
    model_kwargs = {
        'id': id,
        'long_name': "Association 2",
        'short_name': "A2",
        'parent_id': 2,
        'first_season_year': 1922,
        'last_season_year': 1923,
    }
    new_association = Association(**model_kwargs)
    new_association.parent = Association(id=2, long_name="Parent 2", short_name="P2")

    fake_association_repository = MagicMock(AssociationRepository)
    old_association = MagicMock(Association)
    fake_association_repository.get_association.return_value = old_association
    fake_injector.get.return_value = fake_association_repository

    old_association_copy = MagicMock(Association)
    old_association_copy.long_name = "Association 1"
    old_association_copy.short_name = "A1"
    old_association_copy.parent = Association(id=1, long_name="Parent 1", short_name="P1")
    old_association_copy.parent_id = 1
    old_association_copy.first_season_year = 1920
    old_association_copy.last_season_year = 1921
    fake_copy.deepcopy.return_value = old_association_copy

    fake_form.return_value.validate_on_submit.return_value = True
    fake_form.return_value.short_name.data = new_association.short_name
    fake_form.return_value.long_name.data = new_association.long_name
    fake_form.return_value.parent_name.data = new_association.parent.short_name
    fake_form.return_value.first_season_year.data = new_association.first_season_year
    fake_form.return_value.last_season_year.data = new_association.last_season_year

    fake_association_factory.create_association.return_value = new_association

    # Act
    result = mod.edit(id)

    # Assert
    fake_injector.get.assert_called_once_with(AssociationRepository)
    fake_association_repository.get_association.assert_called_once_with(id)
    fake_copy.deepcopy.assert_called_once_with(old_association)
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    view_kwargs = {
        'id': id,
        'long_name': new_association.long_name,
        'short_name': new_association.short_name,
        'parent_name': new_association.parent.short_name,
        'first_season_year': new_association.first_season_year,
        'last_season_year': new_association.last_season_year,
    }
    fake_association_factory.create_association.assert_called_once_with(**view_kwargs)
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
    id = 1
    model_kwargs = {
        'id': id,
        'long_name': "Association 2",
        'short_name': "L2",
        'parent_id': 2,
        'first_season_year': 1922,
        'last_season_year': 1923,
    }
    new_association = Association(**model_kwargs)
    new_association.parent = Association(id=2, long_name="Parent 2", short_name="P2")

    fake_association_repository = MagicMock(AssociationRepository)
    old_association = MagicMock(Association)
    fake_association_repository.get_association.return_value = old_association
    err = ValueError()
    fake_association_repository.update_association.side_effect = err
    fake_injector.get.return_value = fake_association_repository

    old_association_copy = MagicMock(Association)
    old_association_copy.long_name = "Association 1"
    old_association_copy.short_name = "A1"
    old_association_copy.parent = Association(id=1, long_name="Parent 1", short_name="P1")
    old_association_copy.parent_id = 1
    old_association_copy.first_season_year = 1920
    old_association_copy.last_season_year = 1921
    fake_copy.deepcopy.return_value = old_association_copy

    fake_form.return_value.validate_on_submit.return_value = True
    fake_form.return_value.long_name.data = new_association.long_name
    fake_form.return_value.short_name.data = new_association.short_name
    fake_form.return_value.parent_name.data = new_association.parent.short_name
    fake_form.return_value.first_season_year.data = new_association.first_season_year
    fake_form.return_value.last_season_year.data = new_association.last_season_year

    fake_association_factory.create_association.return_value = new_association

    # Act
    result = mod.edit(id)

    # Assert
    fake_injector.get.assert_called_once_with(AssociationRepository)
    fake_association_repository.get_association.assert_called_once_with(id)
    fake_copy.deepcopy.assert_called_once_with(old_association)
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    view_kwargs = {
        'id': id,
        'long_name': new_association.long_name,
        'short_name': new_association.short_name,
        'parent_name': new_association.parent.short_name,
        'first_season_year': new_association.first_season_year,
        'last_season_year': new_association.last_season_year,
    }
    fake_association_factory.create_association.assert_called_once_with(**view_kwargs)
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
def test_edit_when_association_found_and_form_submitted_and_integrity_error_caught_should_flash_error_message_and_render_edit_template(
        fake_injector, fake_copy, fake_form,
        fake_association_factory, fake_flash,
        fake_render_template
):
    # Arrange
    id = 1
    model_kwargs = {
        'id': id,
        'long_name': "Association 2",
        'short_name': "L2",
        'parent_id': 2,
        'first_season_year': 1922,
        'last_season_year': 1923,
    }
    new_association = Association(**model_kwargs)
    new_association.parent = Association(id=2, long_name="Parent 2", short_name="P2")

    fake_association_repository = MagicMock(AssociationRepository)
    old_association = MagicMock(Association)
    fake_association_repository.get_association.return_value = old_association
    err = IntegrityError('statement', 'params', Exception())
    fake_association_repository.update_association.side_effect = err
    fake_injector.get.return_value = fake_association_repository

    old_association_copy = MagicMock(Association)
    old_association_copy.long_name = "Association 1"
    old_association_copy.short_name = "A1"
    old_association_copy.parent = Association(id=1, long_name="Parent 1", short_name="P1")
    old_association_copy.parent_id = 1
    old_association_copy.first_season_year = 1920
    old_association_copy.last_season_year = 1921
    fake_copy.deepcopy.return_value = old_association_copy

    fake_form.return_value.validate_on_submit.return_value = True
    fake_form.return_value.long_name.data = new_association.long_name
    fake_form.return_value.short_name.data = new_association.short_name
    fake_form.return_value.parent_name.data = new_association.parent.short_name
    fake_form.return_value.first_season_year.data = new_association.first_season_year
    fake_form.return_value.last_season_year.data = new_association.last_season_year

    fake_association_factory.create_association.return_value = new_association

    # Act
    result = mod.edit(id)

    # Assert
    fake_injector.get.assert_called_once_with(AssociationRepository)
    fake_association_repository.get_association.assert_called_once_with(id)
    fake_copy.deepcopy.assert_called_once_with(old_association)
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    view_kwargs = {
        'id': id,
        'long_name': new_association.long_name,
        'short_name': new_association.short_name,
        'parent_name': new_association.parent.short_name,
        'first_season_year': new_association.first_season_year,
        'last_season_year': new_association.last_season_year,
    }
    fake_association_factory.create_association.assert_called_once_with(**view_kwargs)
    fake_flash.assert_called_once_with(str(err), 'danger')
    fake_render_template.assert_called_once_with(
        'associations/edit.html', association=old_association_copy, form=fake_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.association_controller.flash')
@patch('app.flask.association_controller.association_factory')
@patch('app.flask.association_controller.EditAssociationForm')
@patch('app.flask.association_controller.url_for')
@patch('app.flask.association_controller.redirect')
@patch('app.flask.association_controller.copy')
@patch('app.flask.association_controller.injector')
def test_edit_when_association_found_and_form_submitted_and_index_error_caught_should_abort_with_404_error(
        fake_injector, fake_copy, fake_redirect, fake_url_for,
        fake_form, fake_association_factory, fake_flash
):
    # Arrange
    id = 1
    model_kwargs = {
        'id': id,
        'long_name': "Association 2",
        'short_name': "A2",
        'parent_id': 2,
        'first_season_year': 1922,
        'last_season_year': 1923,
    }
    new_association = Association(**model_kwargs)
    new_association.parent = Association(id=2, long_name="Parent 2", short_name="P2")

    fake_association_repository = MagicMock(AssociationRepository)
    old_association = MagicMock(Association)
    fake_association_repository.get_association.return_value = old_association
    fake_injector.get.return_value = fake_association_repository

    old_association_copy = MagicMock(Association)
    old_association_copy.long_name = "Association 1"
    old_association_copy.short_name = "A1"
    old_association_copy.parent = Association(id=1, long_name="Parent 1", short_name="P1")
    old_association_copy.parent_id = 1
    old_association_copy.first_season_year = 1920
    old_association_copy.last_season_year = 1921
    fake_copy.deepcopy.return_value = old_association_copy

    fake_form.return_value.validate_on_submit.return_value = True
    fake_form.return_value.long_name.data = new_association.long_name
    fake_form.return_value.short_name.data = new_association.short_name
    fake_form.return_value.parent_name.data = new_association.parent.short_name
    fake_form.return_value.first_season_year.data = new_association.first_season_year
    fake_form.return_value.last_season_year.data = new_association.last_season_year

    err = IndexError()
    fake_url_for.side_effect = err

    # Act
    with pytest.raises(NotFound):
        result = mod.edit(id)

    # Assert
    fake_injector.get.assert_called_once_with(AssociationRepository)
    fake_association_repository.get_association.assert_called_once_with(id)
    fake_copy.deepcopy.assert_called_once_with(old_association)
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    view_kwargs = {
        'id': id,
        'long_name': new_association.long_name,
        'short_name': new_association.short_name,
        'parent_name': new_association.parent.short_name,
        'first_season_year': new_association.first_season_year,
        'last_season_year': new_association.last_season_year,
    }
    fake_association_factory.create_association.assert_called_once_with(**view_kwargs)


@patch('app.flask.association_controller.injector')
def test_delete_when_association_not_found_should_abort_with_404_error(fake_injector, test_app):
    # Arrange
    id = 1

    fake_association_repository = MagicMock(AssociationRepository)
    fake_association_repository.get_association.return_value = None
    fake_injector.get.return_value = fake_association_repository

    # Act
    with test_app.test_request_context(
            f'/associations/delete?id={id}',
            method='POST'
    ):
        with pytest.raises(NotFound):
            result = mod.delete(id)

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
    id = 1

    fake_association_repository = MagicMock(AssociationRepository)
    association = Association()
    fake_association_repository.get_association.return_value = association
    fake_injector.get.return_value = fake_association_repository

    # Act
    with test_app.test_request_context(
            f'/associations/delete?id={id}',
            method='GET'
    ):
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

    fake_association_repository = MagicMock(AssociationRepository)
    association = Association()
    fake_association_repository.get_association.return_value = association
    fake_injector.get.return_value = fake_association_repository

    # Act
    with test_app.test_request_context(
            '/associations/delete?id=1',
            method='POST'
    ):
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
    id = 1

    fake_association_repository = MagicMock(AssociationRepository)
    association = Association()
    fake_association_repository.get_association.return_value = association
    fake_association_repository.delete_association.side_effect = IndexError()
    fake_injector.get.return_value = fake_association_repository

    # Act
    with test_app.test_request_context(
            f'/associations/delete?id={id}',
            method='POST'
    ):
        with pytest.raises(NotFound):
            result = mod.delete(id)

    # Assert
    fake_injector.get.assert_called_once_with(AssociationRepository)
    fake_association_repository.get_association.assert_called_once_with(id)
