from unittest.mock import patch, Mock

import pytest

from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound

import app.flask.division_controller as mod

from app.data.models.division import Division
from app.data.repositories.division_repository import DivisionRepository
from test_app import create_app


@pytest.fixture()
def test_app():
    return create_app()


@patch('app.flask.division_controller.render_template')
@patch('app.flask.division_controller.injector')
def test_index_should_render_division_index_template(fake_injector, fake_render_template):
    # Arrange
    fake_division_repository = Mock(DivisionRepository)
    fake_injector.get.return_value = fake_division_repository

    # Act
    result = mod.index()

    # Assert
    fake_injector.get.assert_called_once_with(DivisionRepository)
    fake_division_repository.get_divisions.assert_called_once()
    fake_render_template.assert_called_once_with(
        'divisions/index.html', divisions=fake_division_repository.get_divisions.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.division_controller.injector')
@patch('app.flask.division_controller.DeleteDivisionForm')
@patch('app.flask.division_controller.render_template')
def test_details_when_division_found_should_render_division_details_template(
        fake_render_template, fake_delete_division_form, fake_injector
):
    # Arrange
    id = 1

    fake_division_repository = Mock(DivisionRepository)
    fake_injector.get.return_value = fake_division_repository

    # Act
    result = mod.details(id)

    # Assert
    fake_delete_division_form.assert_called_once()
    fake_injector.get.assert_called_once_with(DivisionRepository)
    fake_division_repository.get_division.assert_called_once_with(id)
    fake_render_template.assert_called_once_with(
        'divisions/details.html',
        division=fake_division_repository.get_division.return_value,
        form=fake_delete_division_form.return_value
    )
    assert result == fake_render_template.return_value


@patch('app.flask.division_controller.injector')
@patch('app.flask.division_controller.DeleteDivisionForm')
def test_details_when_division_not_found_should_abort_with_404_error(fake_delete_division_form, fake_injector):
    # Arrange
    fake_division_repository = Mock(DivisionRepository)
    fake_division_repository.get_division.side_effect = IndexError()
    fake_injector.get.return_value = fake_division_repository

    # Act
    with pytest.raises(NotFound):
        result = mod.details(1)


@patch('app.flask.division_controller.render_template')
@patch('app.flask.division_controller.flash')
@patch('app.flask.division_controller.injector')
@patch('app.flask.division_controller.NewDivisionForm')
def test_create_when_form_not_submitted_and_no_form_errors_should_render_create_template(
        fake_new_division_form, fake_injector, fake_flash, fake_render_template
):
    # Arrange
    fake_new_division_form.return_value.validate_on_submit.return_value = False
    fake_new_division_form.return_value.errors = None

    fake_division_repository = Mock(DivisionRepository)
    fake_injector.get.return_value = fake_division_repository

    # Act
    result = mod.create()

    # Assert
    fake_injector.get.assert_not_called()
    fake_division_repository.get_division.assert_not_called()
    fake_flash.assert_not_called()
    fake_render_template('divisions/create.html', form=fake_new_division_form.return_value)
    assert result is fake_render_template.return_value


@patch('app.flask.division_controller.render_template')
@patch('app.flask.division_controller.flash')
@patch('app.flask.division_controller.injector')
@patch('app.flask.division_controller.NewDivisionForm')
def test_create_when_form_not_submitted_and_form_errors_should_flash_errors_and_render_create_template(
        fake_new_division_form, fake_injector, fake_flash, fake_render_template
):
    # Arrange
    fake_new_division_form.return_value.validate_on_submit.return_value = False

    errors = 'errors'
    fake_new_division_form.return_value.errors = errors

    fake_division_repository = Mock(DivisionRepository)
    fake_injector.get.return_value = fake_division_repository

    # Act
    result = mod.create()

    # Assert
    fake_injector.get.assert_not_called()
    fake_division_repository.get_division.assert_not_called()
    fake_flash.assert_called_once_with(f"{errors}", 'danger')
    fake_render_template('divisions/create.html', form=fake_new_division_form.return_value)
    assert result is fake_render_template.return_value


@patch('app.flask.division_controller.redirect')
@patch('app.flask.division_controller.url_for')
@patch('app.flask.division_controller.flash')
@patch('app.flask.division_controller.injector')
@patch('app.flask.division_controller.division_factory')
@patch('app.flask.division_controller.NewDivisionForm')
def test_create_when_form_submitted_and_no_errors_caught_should_flash_success_message_and_redirect_to_division_index(
        fake_new_division_form, fake_division_factory, fake_injector, fake_flash, fake_url_for, fake_redirect
):
    # Arrange
    fake_new_division_form.return_value.validate_on_submit.return_value = True
    fake_new_division_form.return_value.name.data = "Division"
    fake_new_division_form.return_value.league_name.data = "L"
    fake_new_division_form.return_value.conference_name.data = "C"
    fake_new_division_form.return_value.first_season_year.data = 1
    fake_new_division_form.return_value.last_season_year.data = 2

    kwargs = {
        'name': "Division",
        'league_name': "L",
        'conference_name': "C",
        'first_season_year': 1,
        'last_season_year': 2,
    }
    division = Division(**kwargs)
    fake_division_factory.create_division.return_value = division

    fake_division_repository = Mock(DivisionRepository)
    fake_injector.get.return_value = fake_division_repository

    # Act
    result = mod.create()

    # Assert
    fake_division_factory.create_division.assert_called_once_with(**kwargs)
    fake_injector.get.assert_called_once_with(DivisionRepository)
    fake_division_repository.add_division.assert_called_once_with(division)
    fake_flash(f"Item {division.name} has been successfully submitted.", 'success')
    fake_url_for.assert_called_once_with('division.index')
    fake_redirect.assert_called_once_with(fake_url_for.return_value)
    assert result is fake_redirect.return_value


@patch('app.flask.division_controller.render_template')
@patch('app.flask.division_controller.flash')
@patch('app.flask.division_controller.injector')
@patch('app.flask.division_controller.division_factory')
@patch('app.flask.division_controller.NewDivisionForm')
def test_create_when_form_submitted_and_value_error_caught_should_flash_error_message_and_render_create_template(
        fake_new_division_form, fake_division_factory, fake_injector, fake_flash, fake_render_template
):
    # Arrange
    fake_new_division_form.return_value.validate_on_submit.return_value = True
    fake_new_division_form.return_value.name.data = "Division"
    fake_new_division_form.return_value.league_name.data = "L"
    fake_new_division_form.return_value.conference_name.data = "C"
    fake_new_division_form.return_value.first_season_year.data = 1
    fake_new_division_form.return_value.last_season_year.data = 2

    kwargs = {
        'name': "Division",
        'league_name': "L",
        'conference_name': "C",
        'first_season_year': 1,
        'last_season_year': 2,
    }
    division = Division(**kwargs)
    fake_division_factory.create_division.return_value = division

    fake_division_repository = Mock(DivisionRepository)
    err = ValueError()
    fake_division_repository.add_division.side_effect = err
    fake_injector.get.return_value = fake_division_repository

    # Act
    result = mod.create()

    # Assert
    fake_division_factory.create_division.assert_called_once_with(**kwargs)
    fake_injector.get.assert_called_once_with(DivisionRepository)
    fake_division_repository.add_division.assert_called_once_with(division)
    fake_flash.assert_called_once_with(str(err), 'danger')
    fake_render_template.assert_called_once_with(
        'divisions/create.html', division=None, form=fake_new_division_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.division_controller.render_template')
@patch('app.flask.division_controller.flash')
@patch('app.flask.division_controller.injector')
@patch('app.flask.division_controller.division_factory')
@patch('app.flask.division_controller.NewDivisionForm')
def test_create_when_form_submitted_and_integrity_error_caught_should_flash_error_message_and_render_create_template(
        fake_new_division_form, fake_division_factory, fake_injector, fake_flash, fake_render_template
):
    # Arrange
    fake_new_division_form.return_value.validate_on_submit.return_value = True
    fake_new_division_form.return_value.name.data = "Division"
    fake_new_division_form.return_value.league_name.data = "L"
    fake_new_division_form.return_value.conference_name.data = "C"
    fake_new_division_form.return_value.first_season_year.data = 1
    fake_new_division_form.return_value.last_season_year.data = 2

    kwargs = {
        'name': "Division",
        'league_name': "L",
        'conference_name': "C",
        'first_season_year': 1,
        'last_season_year': 2,
    }
    division = Division(**kwargs)
    fake_division_factory.create_division.return_value = division

    fake_division_repository = Mock(DivisionRepository)
    err = IntegrityError('statement', 'params', Exception())
    fake_division_repository.add_division.side_effect = err
    fake_injector.get.return_value = fake_division_repository

    # Act
    result = mod.create()

    # Assert
    fake_division_factory.create_division.assert_called_once_with(**kwargs)
    fake_injector.get.assert_called_once_with(DivisionRepository)
    fake_division_repository.add_division.assert_called_once_with(division)
    fake_flash.assert_called_once_with(str(err), 'danger')
    fake_render_template.assert_called_once_with(
        'divisions/create.html', division=None, form=fake_new_division_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.division_controller.injector')
def test_edit_when_division_not_found_should_abort_with_404_error(fake_injector):
    # Arrange
    id = 1

    fake_division_repository = Mock(DivisionRepository)
    old_division = None
    fake_division_repository.get_division.return_value = old_division
    fake_injector.get.return_value = fake_division_repository

    # Act
    with pytest.raises(NotFound):
        result = mod.edit(id)

    # Assert
    fake_injector.get.assert_called_once_with(DivisionRepository)
    fake_division_repository.get_division.assert_called_once_with(id)


@patch('app.flask.division_controller.render_template')
@patch('app.flask.division_controller.flash')
@patch('app.flask.division_controller.EditDivisionForm')
@patch('app.flask.division_controller.injector')
def test_edit_when_division_found_and_form_not_submitted_and_no_form_errors_should_render_edit_template(
        fake_injector, fake_edit_division_form, fake_flash, fake_render_template
):
    # Arrange
    id = 1

    fake_division_repository = Mock(DivisionRepository)
    old_division = Division(
        name="Division",
        league_name="L",
        conference_name="C",
        first_season_year=1,
        last_season_year=2
    )
    fake_division_repository.get_division.return_value = old_division
    fake_injector.get.return_value = fake_division_repository

    fake_edit_division_form.return_value.validate_on_submit.return_value = False
    fake_edit_division_form.return_value.errors = None

    # Act
    result = mod.edit(id)

    # Assert
    fake_injector.get.assert_called_once_with(DivisionRepository)
    fake_division_repository.get_division.assert_called_once_with(id)
    assert fake_edit_division_form.return_value.name.data == old_division.name
    assert fake_edit_division_form.return_value.league_name.data == old_division.league_name
    assert fake_edit_division_form.return_value.conference_name.data == old_division.conference_name
    assert fake_edit_division_form.return_value.first_season_year.data == old_division.first_season_year
    assert fake_edit_division_form.return_value.last_season_year.data == old_division.last_season_year
    fake_flash.assert_not_called()
    fake_render_template.assert_called_once_with(
        'divisions/edit.html', division=old_division, form=fake_edit_division_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.division_controller.render_template')
@patch('app.flask.division_controller.flash')
@patch('app.flask.division_controller.EditDivisionForm')
@patch('app.flask.division_controller.injector')
def test_edit_when_division_found_and_form_not_submitted_and_form_errors_should_flash_errors_and_render_edit_template(
        fake_injector, fake_edit_division_form, fake_flash, fake_render_template
):
    # Arrange
    id = 1

    fake_division_repository = Mock(DivisionRepository)
    old_division = Division(
        name="Division",
        league_name="L",
        conference_name="C",
        first_season_year=1,
        last_season_year=2
    )
    fake_division_repository.get_division.return_value = old_division
    fake_injector.get.return_value = fake_division_repository

    fake_edit_division_form.return_value.validate_on_submit.return_value = False
    fake_edit_division_form.return_value.errors = None

    errors = 'errors'
    fake_edit_division_form.return_value.errors = errors

    # Act
    result = mod.edit(id)

    # Assert
    fake_injector.get.assert_called_once_with(DivisionRepository)
    fake_division_repository.get_division.assert_called_once_with(id)
    assert fake_edit_division_form.return_value.name.data == old_division.name
    assert fake_edit_division_form.return_value.league_name.data == old_division.league_name
    assert fake_edit_division_form.return_value.conference_name.data == old_division.conference_name
    assert fake_edit_division_form.return_value.first_season_year.data == old_division.first_season_year
    assert fake_edit_division_form.return_value.last_season_year.data == old_division.last_season_year
    fake_flash.assert_called_once_with(f"{errors}", 'danger')
    fake_render_template.assert_called_once_with(
        'divisions/edit.html', division=old_division, form=fake_edit_division_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.division_controller.redirect')
@patch('app.flask.division_controller.url_for')
@patch('app.flask.division_controller.flash')
@patch('app.flask.division_controller.division_factory')
@patch('app.flask.division_controller.EditDivisionForm')
@patch('app.flask.division_controller.injector')
def test_edit_when_division_found_and_form_submitted_and_no_errors_caught_should_flash_success_message_and_redirect_to_division_details(
        fake_injector, fake_edit_division_form, fake_division_factory, fake_flash, fake_url_for, fake_redirect
):
    # Arrange
    id = 1

    fake_division_repository = Mock(DivisionRepository)
    old_division = Division(
        id=id,
        name="Division 1",
        league_name="L",
        conference_name="C",
        first_season_year=1,
        last_season_year=2
    )
    fake_division_repository.get_division.return_value = old_division
    fake_injector.get.return_value = fake_division_repository

    fake_edit_division_form.return_value.validate_on_submit.return_value = True
    fake_edit_division_form.return_value.name.data = "Division 2"
    fake_edit_division_form.return_value.league_name.data = "L"
    fake_edit_division_form.return_value.conference_name.data = "C"
    fake_edit_division_form.return_value.first_season_year.data = 3
    fake_edit_division_form.return_value.last_season_year.data = 4

    kwargs = {
        'id': id,
        'name': "Division 2",
        'league_name': "L",
        'conference_name': "C",
        'first_season_year': 3,
        'last_season_year': 4,
    }
    new_division = Division(**kwargs)
    fake_division_factory.create_division.return_value = new_division

    # Act
    result = mod.edit(id)

    # Assert
    fake_injector.get.assert_called_once_with(DivisionRepository)
    fake_division_repository.get_division.assert_called_once_with(id)
    fake_division_factory.create_division.assert_called_once_with(**kwargs)
    fake_division_repository.update_division.assert_called_once_with(new_division)
    fake_flash.assert_called_once_with(
        f"Item {fake_edit_division_form.return_value.name.data} has been successfully updated.", 'success'
    )
    fake_url_for.assert_called_once_with('division.details', id=id)
    fake_redirect.assert_called_once_with(fake_url_for.return_value)
    assert result is fake_redirect.return_value


@patch('app.flask.division_controller.render_template')
@patch('app.flask.division_controller.flash')
@patch('app.flask.division_controller.division_factory')
@patch('app.flask.division_controller.EditDivisionForm')
@patch('app.flask.division_controller.injector')
def test_edit_when_division_found_and_form_submitted_and_value_error_caught_should_flash_error_message_and_render_edit_template(
        fake_injector, fake_edit_division_form, fake_division_factory, fake_flash, fake_render_template
):
    # Arrange
    id = 1

    fake_division_repository = Mock(DivisionRepository)
    old_division = Division(
        id=id,
        name="Division 1",
        league_name="L",
        conference_name="C",
        first_season_year=1,
        last_season_year=2
    )
    fake_division_repository.get_division.return_value = old_division
    err = ValueError()
    fake_division_repository.update_division.side_effect = err
    fake_injector.get.return_value = fake_division_repository

    fake_edit_division_form.return_value.validate_on_submit.return_value = True
    fake_edit_division_form.return_value.name.data = "Division 2"
    fake_edit_division_form.return_value.league_name.data = "L"
    fake_edit_division_form.return_value.conference_name.data = "C"
    fake_edit_division_form.return_value.first_season_year.data = 3
    fake_edit_division_form.return_value.last_season_year.data = 4

    kwargs = {
        'id': id,
        'name': "Division 2",
        'league_name': "L",
        'conference_name': "C",
        'first_season_year': 3,
        'last_season_year': 4,
    }
    new_division = Division(**kwargs)
    fake_division_factory.create_division.return_value = new_division

    # Act
    result = mod.edit(id)

    # Assert
    fake_injector.get.assert_called_once_with(DivisionRepository)
    fake_division_repository.get_division.assert_called_once_with(id)
    fake_division_factory.create_division.assert_called_once_with(**kwargs)
    fake_flash.assert_called_once_with(str(err), 'danger')
    fake_render_template.assert_called_once_with(
        'divisions/edit.html', division=old_division, form=fake_edit_division_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.division_controller.render_template')
@patch('app.flask.division_controller.flash')
@patch('app.flask.division_controller.division_factory')
@patch('app.flask.division_controller.EditDivisionForm')
@patch('app.flask.division_controller.injector')
def test_edit_when_division_found_and_form_submitted_and_integrity_error_caught_should_flash_error_message_and_render_edit_template(
        fake_injector, fake_edit_division_form, fake_division_factory, fake_flash, fake_render_template
):
    # Arrange
    id = 1

    fake_division_repository = Mock(DivisionRepository)
    old_division = Division(
        id=id,
        name="Division 1",
        league_name="L",
        conference_name="C",
        first_season_year=1,
        last_season_year=2
    )
    fake_division_repository.get_division.return_value = old_division
    err = IntegrityError('statement', 'params', Exception())
    fake_division_repository.update_division.side_effect = err
    fake_injector.get.return_value = fake_division_repository

    fake_edit_division_form.return_value.validate_on_submit.return_value = True
    fake_edit_division_form.return_value.name.data = "Division 2"
    fake_edit_division_form.return_value.league_name.data = "L"
    fake_edit_division_form.return_value.conference_name.data = "C"
    fake_edit_division_form.return_value.first_season_year.data = 3
    fake_edit_division_form.return_value.last_season_year.data = 4

    kwargs = {
        'id': id,
        'name': "Division 2",
        'league_name': "L",
        'conference_name': "C",
        'first_season_year': 3,
        'last_season_year': 4,
    }
    new_division = Division(**kwargs)
    fake_division_factory.create_division.return_value = new_division

    # Act
    result = mod.edit(id)

    # Assert
    fake_injector.get.assert_called_once_with(DivisionRepository)
    fake_division_repository.get_division.assert_called_once_with(id)
    fake_division_factory.create_division.assert_called_once_with(**kwargs)
    fake_flash.assert_called_once_with(str(err), 'danger')
    fake_render_template.assert_called_once_with(
        'divisions/edit.html', division=old_division, form=fake_edit_division_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.division_controller.render_template')
@patch('app.flask.division_controller.flash')
@patch('app.flask.division_controller.division_factory')
@patch('app.flask.division_controller.EditDivisionForm')
@patch('app.flask.division_controller.url_for')
@patch('app.flask.division_controller.redirect')
@patch('app.flask.division_controller.injector')
def test_edit_when_division_found_and_form_submitted_and_index_error_caught_should_abort_with_404_error(
        fake_injector, fake_redirect, fake_url_for, fake_edit_division_form, fake_division_factory, fake_flash,
        fake_render_template
):
    # Arrange
    id = 1

    fake_division_repository = Mock(DivisionRepository)
    old_division = Division(
        id=id,
        name="Division 1",
        league_name="L",
        conference_name="C",
        first_season_year=1,
        last_season_year=2
    )
    fake_division_repository.get_division.return_value = old_division
    fake_injector.get.return_value = fake_division_repository

    fake_edit_division_form.return_value.validate_on_submit.return_value = True
    fake_edit_division_form.return_value.name.data = "Division 2"
    fake_edit_division_form.return_value.league_name.data = "L"
    fake_edit_division_form.return_value.conference_name.data = "C"
    fake_edit_division_form.return_value.first_season_year.data = 3
    fake_edit_division_form.return_value.last_season_year.data = 4

    kwargs = {
        'id': id,
        'name': "Division 2",
        'league_name': "L",
        'conference_name': "C",
        'first_season_year': 3,
        'last_season_year': 4,
    }

    err = IndexError()
    fake_url_for.side_effect = err

    # Act
    with pytest.raises(NotFound):
        result = mod.edit(id)

    # Assert
    fake_injector.get.assert_called_once_with(DivisionRepository)
    fake_division_repository.get_division.assert_called_once_with(id)
    fake_edit_division_form.assert_called_once()
    fake_edit_division_form.return_value.validate_on_submit.assert_called_once()
    fake_division_factory.create_division.assert_called_once_with(**kwargs)


@patch('app.flask.division_controller.injector')
def test_delete_when_game_not_found_should_abort_with_404_error(fake_injector, test_app):
    # Arrange
    id = 1

    fake_division_repository = Mock(DivisionRepository)
    fake_division_repository.get_division.return_value = None
    fake_injector.get.return_value = fake_division_repository

    # Act
    with test_app.test_request_context(
            f'/divisions/delete?id={id}',
            method='POST'
    ):
        with pytest.raises(NotFound):
            result = mod.delete(id)

    # Assert
    fake_injector.get.assert_called_once_with(DivisionRepository)
    fake_division_repository.get_division.assert_called_once_with(id)


@patch('app.flask.division_controller.render_template')
@patch('app.flask.division_controller.injector')
def test_delete_when_request_method_is_get_should_render_delete_template(fake_injector, fake_render_template, test_app):
    # Arrange
    id = 1

    fake_division_repository = Mock(DivisionRepository)
    division = Division()
    fake_division_repository.get_division.return_value = division
    fake_injector.get.return_value = fake_division_repository

    # Act
    with test_app.test_request_context(
            f'/divisions/delete?id={id}',
            method='GET'
    ):
        result = mod.delete(id)

    # Assert
    fake_injector.get.assert_called_once_with(DivisionRepository)
    fake_division_repository.get_division.assert_called_once_with(id)
    fake_render_template.assert_called_once_with('divisions/delete.html', division=division)
    assert result is fake_render_template.return_value


@patch('app.flask.division_controller.redirect')
@patch('app.flask.division_controller.url_for')
@patch('app.flask.division_controller.flash')
@patch('app.flask.division_controller.injector')
def test_delete_when_request_method_is_post_and_division_found_should_flash_success_message_and_redirect_to_divisions_index(
        fake_injector, fake_flash, fake_url_for, fake_redirect, test_app
):
    # Arrange
    id = 1

    fake_division_repository = Mock(DivisionRepository)
    division = Division()
    fake_division_repository.get_division.return_value = division
    fake_injector.get.return_value = fake_division_repository

    # Act
    with test_app.test_request_context(
            f'/divisions/delete?id={id}',
            method='POST'
    ):
        result = mod.delete(id)

    # Assert
    fake_injector.get.assert_called_once_with(DivisionRepository)
    fake_division_repository.get_division.assert_called_once_with(id)
    fake_division_repository.delete_division.assert_called_once_with(id)
    fake_flash.assert_called_once_with(f"Division {division.name} has been successfully deleted.", 'success')
    fake_url_for.assert_called_once_with('division.index')
    fake_redirect.assert_called_once_with(fake_url_for.return_value)
    assert result is fake_redirect.return_value


@patch('app.flask.division_controller.injector')
def test_delete_when_request_method_is_post_and_division_not_found_should_abort_with_404_error(fake_injector, test_app):
    # Arrange
    id = 1

    fake_division_repository = Mock(DivisionRepository)
    division = Division()
    fake_division_repository.get_division.return_value = division
    fake_division_repository.delete_division.side_effect = IndexError()
    fake_injector.get.return_value = fake_division_repository

    # Act
    with test_app.test_request_context(
            f'/divisions/delete?id={id}',
            method='POST'
    ):
        with pytest.raises(NotFound):
            result = mod.delete(id)

    # Assert
    fake_injector.get.assert_called_once_with(DivisionRepository)
    fake_division_repository.get_division.assert_called_once_with(id)
