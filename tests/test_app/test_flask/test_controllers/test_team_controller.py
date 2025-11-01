from unittest.mock import patch

import pytest

from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound

import app.flask.team_controller as mod

from app.data.models.team import Team
from test_app import create_app


@pytest.fixture()
def test_app():
    return create_app()


@patch('app.flask.team_controller.render_template')
@patch('app.flask.team_controller.team_repository')
def test_index_should_render_team_index_template(fake_team_repository, fake_render_template):
    # Act
    result = mod.index()

    # Assert
    fake_team_repository.get_teams.assert_called_once()
    fake_render_template.assert_called_once_with(
        'teams/index.html', teams=fake_team_repository.get_teams.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.team_controller.team_repository')
@patch('app.flask.team_controller.DeleteTeamForm')
@patch('app.flask.team_controller.render_template')
def test_details_when_team_found_should_render_team_details_template(
        fake_render_template, fake_delete_team_form, fake_team_repository
):
    # Arrange
    id = 1

    # Act
    result = mod.details(id)

    # Assert
    fake_delete_team_form.assert_called_once()
    fake_team_repository.get_team.assert_called_once_with(id)
    fake_render_template.assert_called_once_with(
        'teams/details.html',
        team=fake_team_repository.get_team.return_value,
        delete_team_form=fake_delete_team_form.return_value
    )
    assert result == fake_render_template.return_value


@patch('app.flask.team_controller.team_repository')
@patch('app.flask.team_controller.DeleteTeamForm')
def test_details_when_team_not_found_should_abort_with_404_error(
        fake_delete_team_form, fake_team_repository
):
    # Arrange
    fake_team_repository.get_team.side_effect = IndexError()

    # Act
    with pytest.raises(NotFound):
        result = mod.details(1)


@patch('app.flask.team_controller.render_template')
@patch('app.flask.team_controller.flash')
@patch('app.flask.team_controller.NewTeamForm')
def test_create_when_form_not_submitted_and_no_form_errors_should_render_create_template(
        fake_new_team_form, fake_flash, fake_render_template
):
    # Arrange
    fake_new_team_form.return_value.validate_on_submit.return_value = False
    fake_new_team_form.return_value.errors = None

    # Act
    result = mod.create()

    # Assert
    fake_flash.assert_not_called()
    fake_render_template('teams/create.html', form=fake_new_team_form.return_value)
    assert result is fake_render_template.return_value


@patch('app.flask.team_controller.render_template')
@patch('app.flask.team_controller.flash')
@patch('app.flask.team_controller.NewTeamForm')
def test_create_when_form_not_submitted_and_form_errors_should_flash_errors_and_render_create_template(
        fake_new_team_form, fake_flash, fake_render_template
):
    # Arrange
    fake_new_team_form.return_value.validate_on_submit.return_value = False

    errors = 'errors'
    fake_new_team_form.return_value.errors = errors

    # Act
    result = mod.create()

    # Assert
    fake_flash.assert_called_once_with(f"{errors}", 'danger')
    fake_render_template('teams/create.html', form=fake_new_team_form.return_value)
    assert result is fake_render_template.return_value


@patch('app.flask.team_controller.redirect')
@patch('app.flask.team_controller.url_for')
@patch('app.flask.team_controller.flash')
@patch('app.flask.team_controller.team_repository')
@patch('app.flask.team_controller.team_factory')
@patch('app.flask.team_controller.NewTeamForm')
def test_create_when_form_submitted_and_no_errors_caught_should_flash_success_message_and_redirect_to_team_index(
        fake_new_team_form, fake_team_factory, fake_team_repository, fake_flash, fake_url_for,
        fake_redirect
):
    # Arrange
    fake_new_team_form.return_value.validate_on_submit.return_value = True
    fake_new_team_form.return_value.name.data = "Team"

    kwargs = {
        'name': "Team",
    }
    team = Team(**kwargs)
    fake_team_factory.create_team.return_value = team

    # Act
    result = mod.create()

    # Assert
    fake_team_factory.create_team.assert_called_once_with(**kwargs)
    fake_team_repository.add_team.assert_called_once_with(team)
    fake_flash(f"Item {team.name} has been successfully submitted.", 'success')
    fake_url_for.assert_called_once_with('team.index')
    fake_redirect.assert_called_once_with(fake_url_for.return_value)
    assert result is fake_redirect.return_value


@patch('app.flask.team_controller.render_template')
@patch('app.flask.team_controller.flash')
@patch('app.flask.team_controller.team_repository')
@patch('app.flask.team_controller.team_factory')
@patch('app.flask.team_controller.NewTeamForm')
def test_create_when_form_submitted_and_value_error_caught_should_flash_error_message_and_render_create_template(
        fake_new_team_form, fake_team_factory, fake_team_repository, fake_flash, fake_render_template
):
    # Arrange
    fake_new_team_form.return_value.validate_on_submit.return_value = True
    fake_new_team_form.return_value.name.data = "Team"

    kwargs = {
        'name': "Team",
    }
    team = Team(**kwargs)
    fake_team_factory.create_team.return_value = team

    err = ValueError()
    fake_team_repository.add_team.side_effect = err

    # Act
    result = mod.create()

    # Assert
    fake_team_factory.create_team.assert_called_once_with(**kwargs)
    fake_team_repository.add_team.assert_called_once_with(team)
    fake_flash.assert_called_once_with(str(err), 'danger')
    fake_render_template.assert_called_once_with(
        'teams/create.html', team=None, form=fake_new_team_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.team_controller.render_template')
@patch('app.flask.team_controller.flash')
@patch('app.flask.team_controller.team_repository')
@patch('app.flask.team_controller.team_factory')
@patch('app.flask.team_controller.NewTeamForm')
def test_create_when_form_submitted_and_integrity_error_caught_should_flash_error_message_and_render_create_template(
        fake_new_team_form, fake_team_factory, fake_team_repository, fake_flash, fake_render_template
):
    # Arrange
    fake_new_team_form.return_value.validate_on_submit.return_value = True
    fake_new_team_form.return_value.name.data = "Team"

    kwargs = {
        'name': "Team",
    }
    team = Team(**kwargs)
    fake_team_factory.create_team.return_value = team

    err = IntegrityError('statement', 'params', Exception())
    fake_team_repository.add_team.side_effect = err

    # Act
    result = mod.create()

    # Assert
    fake_team_factory.create_team.assert_called_once_with(**kwargs)
    fake_team_repository.add_team.assert_called_once_with(team)
    fake_flash.assert_called_once_with(str(err), 'danger')
    fake_render_template.assert_called_once_with(
        'teams/create.html', team=None, form=fake_new_team_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.team_controller.team_repository')
def test_edit_when_team_not_found_should_abort_with_404_error(fake_team_repository):
    # Arrange
    old_team = None
    fake_team_repository.get_team.return_value = old_team

    # Act
    with pytest.raises(NotFound):
        result = mod.edit(1)


@patch('app.flask.team_controller.render_template')
@patch('app.flask.team_controller.flash')
@patch('app.flask.team_controller.EditTeamForm')
@patch('app.flask.team_controller.team_repository')
def test_edit_when_team_found_and_form_not_submitted_and_no_form_errors_should_render_edit_template(
        fake_team_repository, fake_edit_team_form, fake_flash, fake_render_template
):
    # Arrange
    old_team = Team(
        name="Team"
    )
    fake_team_repository.get_team.return_value = old_team

    fake_edit_team_form.return_value.validate_on_submit.return_value = False
    fake_edit_team_form.return_value.errors = None

    # Act
    result = mod.edit(1)

    # Assert
    assert fake_edit_team_form.return_value.name.data == old_team.name
    fake_flash.assert_not_called()
    fake_render_template.assert_called_once_with(
        'teams/edit.html', team=old_team, form=fake_edit_team_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.team_controller.render_template')
@patch('app.flask.team_controller.flash')
@patch('app.flask.team_controller.EditTeamForm')
@patch('app.flask.team_controller.team_repository')
def test_edit_when_team_found_and_form_not_submitted_and_form_errors_should_flash_errors_and_render_edit_template(
        fake_team_repository, fake_edit_team_form, fake_flash, fake_render_template
):
    # Arrange
    old_team = Team(
        name="Team"
    )
    fake_team_repository.get_team.return_value = old_team

    fake_edit_team_form.return_value.validate_on_submit.return_value = False

    errors = 'errors'
    fake_edit_team_form.return_value.errors = errors

    # Act
    result = mod.edit(1)

    # Assert
    assert fake_edit_team_form.return_value.name.data == old_team.name
    fake_flash.assert_called_once_with(f"{errors}", 'danger')
    fake_render_template.assert_called_once_with(
        'teams/edit.html', team=old_team, form=fake_edit_team_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.team_controller.redirect')
@patch('app.flask.team_controller.url_for')
@patch('app.flask.team_controller.flash')
@patch('app.flask.team_controller.team_factory')
@patch('app.flask.team_controller.EditTeamForm')
@patch('app.flask.team_controller.team_repository')
def test_edit_when_team_found_and_form_submitted_and_no_errors_caught_should_flash_success_message_and_redirect_to_team_details(
        fake_team_repository, fake_edit_team_form, fake_team_factory, fake_flash, fake_url_for,
        fake_redirect
):
    # Arrange
    id = 1

    old_team = Team(
        id=id,
        name="Team 1"
    )
    fake_team_repository.get_team.return_value = old_team

    fake_edit_team_form.return_value.validate_on_submit.return_value = True
    fake_edit_team_form.return_value.name.data = "Team 2"

    kwargs = {
        'id': id,
        'name': "Team 2",
    }
    new_team = Team(**kwargs)
    fake_team_factory.create_team.return_value = new_team

    # Act
    result = mod.edit(id)

    # Assert
    fake_team_factory.create_team.assert_called_once_with(**kwargs)
    fake_team_repository.update_team.assert_called_once_with(new_team)
    fake_flash.assert_called_once_with(
        f"Item {fake_edit_team_form.return_value.name.data} has been successfully updated.", 'success'
    )
    fake_url_for.assert_called_once_with('team.details', id=id)
    fake_redirect.assert_called_once_with(fake_url_for.return_value)
    assert result is fake_redirect.return_value


@patch('app.flask.team_controller.render_template')
@patch('app.flask.team_controller.flash')
@patch('app.flask.team_controller.team_factory')
@patch('app.flask.team_controller.EditTeamForm')
@patch('app.flask.team_controller.team_repository')
def test_edit_when_team_found_and_form_submitted_and_value_error_caught_should_flash_error_message_and_render_edit_template(
        fake_team_repository, fake_edit_team_form, fake_team_factory, fake_flash,
        fake_render_template
):
    # Arrange
    id = 1

    old_team = Team(
        id=id,
        name="Team 1"
    )
    fake_team_repository.get_team.return_value = old_team

    fake_edit_team_form.return_value.validate_on_submit.return_value = True
    fake_edit_team_form.return_value.name.data = "Team 2"

    kwargs = {
        'id': id,
        'name': "Team 2",
    }
    new_team = Team(**kwargs)
    fake_team_factory.create_team.return_value = new_team

    err = ValueError()
    fake_team_repository.update_team.side_effect = err

    # Act
    result = mod.edit(id)

    # Assert
    fake_team_factory.create_team.assert_called_once_with(**kwargs)
    fake_team_repository.update_team.assert_called_once_with(new_team)
    fake_flash.assert_called_once_with(str(err), 'danger')
    fake_render_template.assert_called_once_with(
        'teams/edit.html', team=old_team, form=fake_edit_team_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.team_controller.render_template')
@patch('app.flask.team_controller.flash')
@patch('app.flask.team_controller.team_factory')
@patch('app.flask.team_controller.EditTeamForm')
@patch('app.flask.team_controller.team_repository')
def test_edit_when_team_found_and_form_submitted_and_integrity_error_caught_should_flash_error_message_and_render_edit_template(
        fake_team_repository, fake_edit_team_form, fake_team_factory, fake_flash,
        fake_render_template
):
    # Arrange
    id = 1

    old_team = Team(
        id=id,
        name="Team 1"
    )
    fake_team_repository.get_team.return_value = old_team

    fake_edit_team_form.return_value.validate_on_submit.return_value = True
    fake_edit_team_form.return_value.name.data = "Team 2"

    kwargs = {
        'id': id,
        'name': "Team 2",
    }
    new_team = Team(**kwargs)
    fake_team_factory.create_team.return_value = new_team

    err = IntegrityError('statement', 'params', Exception())
    fake_team_repository.update_team.side_effect = err

    # Act
    result = mod.edit(id)

    # Assert
    fake_team_factory.create_team.assert_called_once_with(**kwargs)
    fake_team_repository.update_team.assert_called_once_with(new_team)
    fake_flash.assert_called_once_with(str(err), 'danger')
    fake_render_template.assert_called_once_with(
        'teams/edit.html', team=old_team, form=fake_edit_team_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.team_controller.render_template')
@patch('app.flask.team_controller.team_repository')
def test_delete_when_request_method_is_get_should_render_delete_template(
        fake_team_repository, fake_render_template, test_app
):
    # Arrange
    team = Team()
    fake_team_repository.get_team.return_value = team

    # Act
    with test_app.test_request_context(
            '/teams/delete?id=1',
            method='GET'
    ):
        with test_app.app_context():
            result = mod.delete(1)

    # Assert
    fake_team_repository.get_team.assert_called_once_with(1)
    fake_render_template.assert_called_once_with('teams/delete.html', team=team)
    assert result is fake_render_template.return_value


@patch('app.flask.team_controller.redirect')
@patch('app.flask.team_controller.url_for')
@patch('app.flask.team_controller.flash')
@patch('app.flask.team_controller.team_repository')
def test_delete_when_request_method_is_post_and_team_found_should_flash_success_message_and_redirect_to_teams_index(
        fake_team_repository, fake_flash, fake_url_for, fake_redirect, test_app
):
    # Arrange
    team = Team()
    fake_team_repository.get_team.return_value = team

    # Act
    id = 1
    with test_app.test_request_context(
            '/teams/delete?id=1',
            method='POST'
    ):
        with test_app.app_context():
            result = mod.delete(id)

    # Assert
    fake_team_repository.delete_team.assert_called_once_with(id)
    fake_flash.assert_called_once_with(f"Team {team.name} has been successfully deleted.", 'success')
    fake_url_for.assert_called_once_with('team.index')
    fake_redirect.assert_called_once_with(fake_url_for.return_value)
    assert result is fake_redirect.return_value


@patch('app.flask.team_controller.team_repository')
def test_delete_when_request_method_is_post_and_team_not_found_should_abort_with_404_error(
        fake_team_repository, test_app
):
    # Arrange
    team = Team()
    fake_team_repository.get_team.return_value = team
    fake_team_repository.delete_team.side_effect = IndexError()

    # Act
    with test_app.test_request_context(
            '/teams/delete?id=1',
            method='POST'
    ):
        with test_app.app_context():
            with pytest.raises(NotFound):
                result = mod.delete(1)
