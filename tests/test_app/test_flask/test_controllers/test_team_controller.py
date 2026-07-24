from typing import Optional
from unittest.mock import patch, MagicMock

import pytest

from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound

import app.flask.team_controller as mod

from app.data.models.team import Team
from app.data.repositories.team_repository import TeamRepository
from test_app import create_app


@pytest.fixture()
def test_app():
    return create_app()


@patch('app.flask.team_controller.render_template')
@patch('app.flask.team_controller.injector')
def test_index_should_render_team_index_template(fake_injector, fake_render_template):
    # Arrange
    fake_team_repository = _set_up_index_and_details(fake_injector)

    # Act
    result = mod.index()

    # Assert
    fake_injector.get.assert_called_once_with(TeamRepository)
    fake_team_repository.get_teams.assert_called_once()
    fake_render_template.assert_called_once_with(
        'teams/index.html', teams=fake_team_repository.get_teams.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.team_controller.render_template')
@patch('app.flask.team_controller.injector')
@patch('app.flask.team_controller.DeleteTeamForm')
def test_details_when_team_found_should_render_team_details_template(
        fake_form, fake_injector, fake_render_template
):
    # Arrange
    fake_team_repository = _set_up_index_and_details(fake_injector)

    # Act
    id = 1
    result = mod.details(id)

    # Assert
    fake_form.assert_called_once()
    fake_injector.get.assert_called_once_with(TeamRepository)
    fake_team_repository.get_team.assert_called_once_with(id)
    fake_render_template.assert_called_once_with(
        'teams/details.html',
        team=fake_team_repository.get_team.return_value,
        form=fake_form.return_value
    )
    assert result == fake_render_template.return_value


@patch('app.flask.team_controller.injector')
@patch('app.flask.team_controller.DeleteTeamForm')
def test_details_when_team_not_found_should_abort_with_404_error(fake_form, fake_injector):
    # Arrange
    err = IndexError()
    _ = _set_up_index_and_details(fake_injector, err=err)

    # Act
    with pytest.raises(NotFound):
        _ = mod.details(1)


def _set_up_index_and_details(fake_injector, err: Optional[Exception] = None) -> MagicMock:
    fake_team_repository = MagicMock(TeamRepository)
    fake_team_repository.get_team.side_effect = err
    fake_injector.get.return_value = fake_team_repository

    return fake_team_repository


@patch('app.flask.team_controller.render_template')
@patch('app.flask.team_controller.flash')
@patch('app.flask.team_controller.NewTeamForm')
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
    fake_render_template('teams/create.html', form=fake_form.return_value)
    assert result is fake_render_template.return_value


@patch('app.flask.team_controller.render_template')
@patch('app.flask.team_controller.flash')
@patch('app.flask.team_controller.NewTeamForm')
def test_create_when_form_not_submitted_and_form_errors_should_flash_errors_and_render_create_template(
        fake_form, fake_flash, fake_render_template
):
    # Arrange
    errors = 'errors'
    _set_up_create_get(fake_form, errors)

    # Act
    result = mod.create()

    # Assert
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    fake_flash.assert_called_once_with(f"{errors}", 'danger')
    fake_render_template('teams/create.html', form=fake_form.return_value)
    assert result is fake_render_template.return_value


def _set_up_create_get(fake_form, errors: Optional[str] = None) -> None:
    form = fake_form.return_value
    form.validate_on_submit.return_value = False
    form.errors = errors


@patch('app.flask.team_controller.redirect')
@patch('app.flask.team_controller.url_for')
@patch('app.flask.team_controller.flash')
@patch('app.flask.team_controller.injector')
@patch('app.flask.team_controller.team_factory')
@patch('app.flask.team_controller.NewTeamForm')
def test_create_when_form_submitted_and_no_errors_caught_should_flash_success_message_and_redirect_to_team_index(
        fake_form, fake_team_factory, fake_injector, fake_flash,
        fake_url_for, fake_redirect
):
    # Arrange
    team, fake_team_repository = _set_up_create_post(fake_injector, fake_form, fake_team_factory)

    # Act
    result = mod.create()

    # Assert
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    view_kwargs = {
        'name': team.name,
    }
    fake_team_factory.create_team.assert_called_once_with(**view_kwargs)
    fake_injector.get.assert_called_once_with(TeamRepository)
    fake_team_repository.add_team.assert_called_once_with(team)
    fake_flash(f"Item {team.name} has been successfully submitted.", 'success')
    fake_url_for.assert_called_once_with('team.index')
    fake_redirect.assert_called_once_with(fake_url_for.return_value)
    assert result is fake_redirect.return_value


@patch('app.flask.team_controller.render_template')
@patch('app.flask.team_controller.flash')
@patch('app.flask.team_controller.injector')
@patch('app.flask.team_controller.team_factory')
@patch('app.flask.team_controller.NewTeamForm')
def test_create_when_form_submitted_and_value_error_caught_should_flash_error_message_and_render_create_template(
        fake_form, fake_team_factory, fake_injector,
        fake_flash, fake_render_template
):
    # Arrange
    err = ValueError()
    team, fake_team_repository = _set_up_create_post(fake_injector, fake_form, fake_team_factory, err=err)

    # Act
    result = mod.create()

    # Assert
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    view_kwargs = {
        'name': team.name,
    }
    fake_team_factory.create_team.assert_called_once_with(**view_kwargs)
    fake_injector.get.assert_called_once_with(TeamRepository)
    fake_team_repository.add_team.assert_called_once_with(team)
    fake_flash.assert_called_once_with(str(err), 'danger')
    fake_render_template.assert_called_once_with(
        'teams/create.html', team=None, form=fake_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.team_controller.render_template')
@patch('app.flask.team_controller.flash')
@patch('app.flask.team_controller.injector')
@patch('app.flask.team_controller.team_factory')
@patch('app.flask.team_controller.NewTeamForm')
def test_create_when_form_submitted_and_integrity_error_caught_should_flash_error_message_and_render_create_template(
        fake_form, fake_team_factory, fake_injector,
        fake_flash, fake_render_template
):
    # Arrange
    err = IntegrityError('statement', 'params', Exception())
    team, fake_team_repository = _set_up_create_post(fake_injector, fake_form, fake_team_factory, err=err)

    # Act
    result = mod.create()

    # Assert
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    view_kwargs = {
        'name': team.name,
    }
    fake_team_factory.create_team.assert_called_once_with(**view_kwargs)
    fake_injector.get.assert_called_once_with(TeamRepository)
    fake_team_repository.add_team.assert_called_once_with(team)
    fake_flash.assert_called_once_with(str(err), 'danger')
    fake_render_template.assert_called_once_with(
        'teams/create.html', team=None, form=fake_form.return_value
    )
    assert result is fake_render_template.return_value


def _set_up_create_post(
        fake_injector, fake_form, fake_team_factory, err: Optional[Exception] = None
) -> tuple[Team, MagicMock]:
    team = Team(
        name="Team"
    )

    form = fake_form.return_value
    form.validate_on_submit.return_value = True
    form.name.data = team.name

    fake_team_factory.create_team.return_value = team

    fake_team_repository = MagicMock(TeamRepository)
    fake_team_repository.add_team.side_effect = err
    fake_injector.get.return_value = fake_team_repository

    return team, fake_team_repository


@patch('app.flask.team_controller.copy')
@patch('app.flask.team_controller.injector')
def test_edit_when_team_not_found_should_abort_with_404_error(fake_injector, fake_copy):
    # Arrange
    old_team_copy = None
    old_team, fake_team_repository = _set_up_edit(fake_injector, fake_copy, old_team_copy=old_team_copy)

    # Act
    id = 1
    with pytest.raises(NotFound):
        result = mod.edit(id)

    # Assert
    fake_injector.get.assert_called_once_with(TeamRepository)
    fake_team_repository.get_team.assert_called_once_with(id)
    fake_copy.deepcopy.assert_called_once_with(old_team)


@patch('app.flask.team_controller.render_template')
@patch('app.flask.team_controller.flash')
@patch('app.flask.team_controller.EditTeamForm')
@patch('app.flask.team_controller.copy')
@patch('app.flask.team_controller.injector')
def test_edit_when_team_found_and_form_not_submitted_and_no_form_errors_should_render_edit_template(
        fake_injector, fake_copy, fake_form, fake_flash,
        fake_render_template
):
    # Arrange
    old_team, old_team_copy, fake_team_repository = _set_up_edit_get(fake_injector, fake_copy, fake_form)

    # Act
    id = 1
    result = mod.edit(id)

    # Assert
    fake_injector.get.assert_called_once_with(TeamRepository)
    fake_team_repository.get_team.assert_called_once_with(id)
    fake_copy.deepcopy.assert_called_once_with(old_team)
    fake_form.assert_called_once()
    assert fake_form.return_value.name.data == old_team_copy.name
    fake_form.return_value.validate_on_submit.assert_called_once()
    fake_flash.assert_not_called()
    fake_render_template.assert_called_once_with(
        'teams/edit.html', team=old_team_copy, form=fake_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.team_controller.render_template')
@patch('app.flask.team_controller.flash')
@patch('app.flask.team_controller.EditTeamForm')
@patch('app.flask.team_controller.copy')
@patch('app.flask.team_controller.injector')
def test_edit_when_team_found_and_form_not_submitted_and_form_errors_should_flash_errors_and_render_edit_template(
        fake_injector, fake_copy, fake_form, fake_flash,
        fake_render_template
):
    # Arrange
    errors = 'errors'
    old_team, old_team_copy, fake_team_repository = _set_up_edit_get(fake_injector, fake_copy, fake_form, errors=errors)

    # Act
    id = 1
    result = mod.edit(id)

    # Assert
    fake_injector.get.assert_called_once_with(TeamRepository)
    fake_team_repository.get_team.assert_called_once_with(id)
    fake_copy.deepcopy.assert_called_once_with(old_team)
    fake_form.assert_called_once()
    assert fake_form.return_value.name.data == old_team_copy.name
    fake_form.return_value.validate_on_submit.assert_called_once()
    fake_flash.assert_called_once_with(f"{errors}", 'danger')
    fake_render_template.assert_called_once_with(
        'teams/edit.html', team=old_team_copy, form=fake_form.return_value
    )
    assert result is fake_render_template.return_value


def _set_up_edit_get(
        fake_injector, fake_copy, fake_form, errors: Optional[str] = None
) -> tuple[Team, Team, MagicMock]:
    old_team_copy = Team(
        name = "Old Team"
    )
    old_team, fake_team_repository = (
        _set_up_edit(fake_injector, fake_copy, old_team_copy=old_team_copy)
    )

    form = fake_form.return_value
    form.validate_on_submit.return_value = False
    form.errors = errors

    return old_team, old_team_copy, fake_team_repository


@patch('app.flask.team_controller.redirect')
@patch('app.flask.team_controller.url_for')
@patch('app.flask.team_controller.flash')
@patch('app.flask.team_controller.team_factory')
@patch('app.flask.team_controller.EditTeamForm')
@patch('app.flask.team_controller.copy')
@patch('app.flask.team_controller.injector')
def test_edit_when_team_found_and_form_submitted_and_no_errors_caught_should_flash_success_message_and_redirect_to_team_details(
        fake_injector, fake_copy, fake_form, fake_team_factory,
        fake_flash, fake_url_for, fake_redirect
):
    # Arrange
    old_team, old_team_copy, new_team, fake_team_repository = (
        _set_up_edit_post(fake_injector, fake_copy, fake_form, fake_team_factory)
    )

    # Act
    id = 1
    result = mod.edit(id)

    # Assert
    fake_injector.get.assert_called_once_with(TeamRepository)
    fake_team_repository.get_team.assert_called_once_with(id)
    fake_copy.deepcopy.assert_called_once_with(old_team)
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    kwargs = {
        'id': id,
        'name': new_team.name,
    }
    fake_team_factory.create_team.assert_called_once_with(**kwargs)
    fake_team_repository.update_team.assert_called_once_with(new_team)
    fake_flash.assert_called_once_with(
        f"Item {fake_form.return_value.name.data} has been successfully updated.", 'success'
    )
    fake_url_for.assert_called_once_with('team.details', id=id)
    fake_redirect.assert_called_once_with(fake_url_for.return_value)
    assert result is fake_redirect.return_value


@patch('app.flask.team_controller.render_template')
@patch('app.flask.team_controller.flash')
@patch('app.flask.team_controller.team_factory')
@patch('app.flask.team_controller.EditTeamForm')
@patch('app.flask.team_controller.copy')
@patch('app.flask.team_controller.injector')
def test_edit_when_team_found_and_form_submitted_and_value_error_caught_should_flash_error_message_and_render_edit_template(
        fake_injector, fake_copy, fake_form, fake_team_factory,
        fake_flash, fake_render_template
):
    # Arrange
    err = ValueError()
    old_team, old_team_copy, new_team, fake_team_repository = (
        _set_up_edit_post(fake_injector, fake_copy, fake_form, fake_team_factory, err=err)
    )

    # Act
    id = 1
    result = mod.edit(id)

    # Assert
    fake_injector.get.assert_called_once_with(TeamRepository)
    fake_team_repository.get_team.assert_called_once_with(id)
    fake_copy.deepcopy.assert_called_once_with(old_team)
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    kwargs = {
        'id': id,
        'name': new_team.name,
    }
    fake_team_factory.create_team.assert_called_once_with(**kwargs)
    fake_flash.assert_called_once_with(str(err), 'danger')
    fake_render_template.assert_called_once_with(
        'teams/edit.html', team=old_team_copy, form=fake_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.team_controller.render_template')
@patch('app.flask.team_controller.flash')
@patch('app.flask.team_controller.team_factory')
@patch('app.flask.team_controller.EditTeamForm')
@patch('app.flask.team_controller.copy')
@patch('app.flask.team_controller.injector')
def test_edit_when_team_found_and_form_submitted_and_integrity_error_caught_should_flash_error_message_and_render_edit_template(
        fake_injector, fake_copy, fake_form, fake_team_factory,
        fake_flash, fake_render_template
):
    # Arrange
    err = IntegrityError('statement', 'params', Exception())
    old_team, old_team_copy, new_team, fake_team_repository = (
        _set_up_edit_post(fake_injector, fake_copy, fake_form, fake_team_factory, err=err)
    )

    # Act
    id = 1
    result = mod.edit(id)

    # Assert
    fake_injector.get.assert_called_once_with(TeamRepository)
    fake_team_repository.get_team.assert_called_once_with(id)
    fake_copy.deepcopy.assert_called_once_with(old_team)
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    kwargs = {
        'id': id,
        'name': new_team.name,
    }
    fake_team_factory.create_team.assert_called_once_with(**kwargs)
    fake_flash.assert_called_once_with(str(err), 'danger')
    fake_render_template.assert_called_once_with(
        'teams/edit.html', team=old_team_copy, form=fake_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.team_controller.flash')
@patch('app.flask.team_controller.team_factory')
@patch('app.flask.team_controller.EditTeamForm')
@patch('app.flask.team_controller.url_for')
@patch('app.flask.team_controller.redirect')
@patch('app.flask.team_controller.copy')
@patch('app.flask.team_controller.injector')
def test_edit_when_team_found_and_form_submitted_and_index_error_caught_should_abort_with_404_error(
        fake_injector, fake_copy, fake_redirect, fake_url_for,
        fake_form, fake_team_factory, fake_flash
):
    # Arrange
    err = IndexError()
    old_team, old_team_copy, new_team, fake_team_repository = (
        _set_up_edit_post(fake_injector, fake_copy, fake_form, fake_team_factory, err=err)
    )

    # Act
    id = 1
    with pytest.raises(NotFound):
        _ = mod.edit(id)

    # Assert
    fake_injector.get.assert_called_once_with(TeamRepository)
    fake_team_repository.get_team.assert_called_once_with(id)
    fake_copy.deepcopy.assert_called_once_with(old_team)
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    kwargs = {
        'id': id,
        'name': new_team.name,
    }
    fake_team_factory.create_team.assert_called_once_with(**kwargs)


def _set_up_edit_post(
        fake_injector, fake_copy, fake_form, fake_team_factory,
        err: Optional[Exception] = None
) -> tuple[Team, Team, Team, MagicMock]:
    old_team_copy = Team(
        name = "Old Team"
    )
    old_team, fake_team_repository = (
        _set_up_edit(fake_injector, fake_copy, old_team_copy=old_team_copy, err=err)
    )

    new_team = Team(
        name="New Team"
    )
    form = fake_form.return_value
    form.name.data = new_team.name
    form.validate_on_submit.return_value = True

    fake_team_factory.create_team.return_value = new_team

    return old_team, old_team_copy, new_team, fake_team_repository


@patch('app.flask.team_controller.injector')
def test_delete_when_team_not_found_should_abort_with_404_error(fake_injector, test_app):
    # Arrange
    fake_team_repository = _set_up_delete(fake_injector)

    # Act
    id = 1
    with test_app.test_request_context(f'/teams/delete?id={id}', method='POST'):
        with pytest.raises(NotFound):
            result = mod.delete(id)

    # Assert
    fake_injector.get.assert_called_once_with(TeamRepository)
    fake_team_repository.get_team.assert_called_once_with(id)


@patch('app.flask.team_controller.render_template')
@patch('app.flask.team_controller.DeleteTeamForm')
@patch('app.flask.team_controller.injector')
def test_delete_when_request_method_is_get_should_render_delete_template(
        fake_injector, fake_form, fake_render_template, test_app
):
    # Arrange
    team = Team()
    fake_team_repository = _set_up_delete(fake_injector, team=team)

    # Act
    id = 1
    with test_app.test_request_context(f'/teams/delete?id={id}', method='GET'):
        result = mod.delete(id)

    # Assert
    fake_form.assert_called_once()
    fake_injector.get.assert_called_once_with(TeamRepository)
    fake_team_repository.get_team.assert_called_once_with(id)
    fake_render_template.assert_called_once_with('teams/delete.html', team=team, form=fake_form.return_value)
    assert result is fake_render_template.return_value


@patch('app.flask.team_controller.redirect')
@patch('app.flask.team_controller.url_for')
@patch('app.flask.team_controller.flash')
@patch('app.flask.team_controller.injector')
def test_delete_when_request_method_is_post_and_team_found_should_flash_success_message_and_redirect_to_teams_index(
        fake_injector, fake_flash, fake_url_for,
        fake_redirect, test_app
):
    # Arrange
    id = 1
    team = Team(id=id, name="Team")
    fake_team_repository = _set_up_delete(fake_injector, team=team)

    # Act
    with test_app.test_request_context('/teams/delete?id=1', method='POST'):
        result = mod.delete(id)

    # Assert
    fake_injector.get.assert_called_once_with(TeamRepository)
    fake_team_repository.get_team.assert_called_once_with(id)
    fake_team_repository.delete_team.assert_called_once_with(id)
    fake_flash.assert_called_once_with(f"Team {team.name} has been successfully deleted.", 'success')
    fake_url_for.assert_called_once_with('team.index')
    fake_redirect.assert_called_once_with(fake_url_for.return_value)
    assert result is fake_redirect.return_value


@patch('app.flask.team_controller.injector')
def test_delete_when_request_method_is_post_and_index_error_is_caught_should_abort_with_404_error(
        fake_injector, test_app
):
    # Arrange
    team = Team()
    err = IndexError()
    fake_team_repository = _set_up_delete(fake_injector, team=team, err=err)

    # Act
    id = 1
    with test_app.test_request_context(f'/teams/delete?id={id}', method='POST'):
        with pytest.raises(NotFound):
            _ = mod.delete(id)

    # Assert
    fake_injector.get.assert_called_once_with(TeamRepository)
    fake_team_repository.get_team.assert_called_once_with(id)


def _set_up_delete(fake_injector, team: Optional[Team] = None, err: Optional[Exception] = None) -> MagicMock:
    fake_team_repository = MagicMock(TeamRepository)
    fake_team_repository.get_team.return_value = team
    fake_team_repository.delete_team.side_effect = err
    fake_injector.get.return_value = fake_team_repository

    return fake_team_repository


def _set_up_edit(
        fake_injector, fake_copy, old_team_copy: Optional[Team] = None, err: Optional[Exception] = None
) -> tuple[MagicMock, Team]:
    fake_team_repository = MagicMock(TeamRepository)
    old_team = Team()
    fake_team_repository.get_team.return_value = old_team
    fake_team_repository.update_team.side_effect = err
    fake_injector.get.return_value = fake_team_repository

    fake_copy.deepcopy.return_value = old_team_copy

    return old_team, fake_team_repository
