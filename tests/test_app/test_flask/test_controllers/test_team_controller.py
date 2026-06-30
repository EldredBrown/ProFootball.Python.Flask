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
    fake_team_repository = MagicMock(TeamRepository)
    fake_injector.get.return_value = fake_team_repository

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
    fake_team_repository = MagicMock(TeamRepository)
    fake_injector.get.return_value = fake_team_repository

    id = 1

    # Act
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
    fake_team_repository = MagicMock(TeamRepository)
    fake_team_repository.get_team.side_effect = IndexError()
    fake_injector.get.return_value = fake_team_repository

    # Act
    with pytest.raises(NotFound):
        result = mod.details(1)


@patch('app.flask.team_controller.render_template')
@patch('app.flask.team_controller.flash')
@patch('app.flask.team_controller.injector')
@patch('app.flask.team_controller.NewTeamForm')
def test_create_when_form_not_submitted_and_no_form_errors_should_render_create_template(
        fake_form, fake_injector, fake_flash, fake_render_template
):
    # Arrange
    fake_form.return_value.validate_on_submit.return_value = False
    fake_form.return_value.errors = None

    fake_team_repository = MagicMock(TeamRepository)
    fake_injector.get.return_value = fake_team_repository

    # Act
    result = mod.create()

    # Assert
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    fake_injector.get.assert_not_called()
    fake_team_repository.add_team.assert_not_called()
    fake_flash.assert_not_called()
    fake_render_template('teams/create.html', form=fake_form.return_value)
    assert result is fake_render_template.return_value


@patch('app.flask.team_controller.render_template')
@patch('app.flask.team_controller.flash')
@patch('app.flask.team_controller.injector')
@patch('app.flask.team_controller.NewTeamForm')
def test_create_when_form_not_submitted_and_form_errors_should_flash_errors_and_render_create_template(
        fake_form, fake_injector, fake_flash,
        fake_render_template
):
    # Arrange
    fake_form.return_value.validate_on_submit.return_value = False

    errors = 'errors'
    fake_form.return_value.errors = errors

    fake_team_repository = MagicMock(TeamRepository)
    fake_injector.get.return_value = fake_team_repository

    # Act
    result = mod.create()

    # Assert
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    fake_injector.get.assert_not_called()
    fake_team_repository.add_team.assert_not_called()
    fake_flash.assert_called_once_with(f"{errors}", 'danger')
    fake_render_template('teams/create.html', form=fake_form.return_value)
    assert result is fake_render_template.return_value


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
    model_kwargs = {
        'name': "Team",
    }
    team = Team(**model_kwargs)

    fake_form.return_value.validate_on_submit.return_value = True
    fake_form.return_value.name.data = team.name

    fake_team_factory.create_team.return_value = team

    fake_team_repository = MagicMock(TeamRepository)
    fake_injector.get.return_value = fake_team_repository

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
    model_kwargs = {
        'name': "Team",
    }
    team = Team(**model_kwargs)

    fake_form.return_value.validate_on_submit.return_value = True
    fake_form.return_value.name.data = team.name

    fake_team_factory.create_team.return_value = team

    fake_team_repository = MagicMock(TeamRepository)
    err = ValueError()
    fake_team_repository.add_team.side_effect = err
    fake_injector.get.return_value = fake_team_repository

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
    model_kwargs = {
        'name': "Team",
    }
    team = Team(**model_kwargs)

    fake_form.return_value.validate_on_submit.return_value = True
    fake_form.return_value.name.data = team.name

    fake_team_factory.create_team.return_value = team

    fake_team_repository = MagicMock(TeamRepository)
    err = IntegrityError('statement', 'params', Exception())
    fake_team_repository.add_team.side_effect = err
    fake_injector.get.return_value = fake_team_repository

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


@patch('app.flask.team_controller.copy')
@patch('app.flask.team_controller.injector')
def test_edit_when_team_not_found_should_abort_with_404_error(fake_injector, fake_copy):
    # Arrange
    fake_team_repository = MagicMock(TeamRepository)
    old_team = MagicMock(Team)
    fake_team_repository.get_team.return_value = old_team
    fake_injector.get.return_value = fake_team_repository

    old_team_copy = None
    fake_copy.deepcopy.return_value = old_team_copy

    id = 1

    # Act
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
    fake_team_repository = MagicMock(TeamRepository)
    old_team = MagicMock(Team)
    fake_team_repository.get_team.return_value = old_team
    fake_injector.get.return_value = fake_team_repository

    old_team_copy = MagicMock(Team)
    old_team_copy.name = "Team"
    fake_copy.deepcopy.return_value = old_team_copy

    fake_form.return_value.validate_on_submit.return_value = False
    fake_form.return_value.errors = None

    id = 1

    # Act
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
        fake_injector, fake_copy, fake_form, fake_flash, fake_render_template
):
    # Arrange
    fake_team_repository = MagicMock(TeamRepository)
    old_team = MagicMock(Team)
    fake_team_repository.get_team.return_value = old_team
    fake_injector.get.return_value = fake_team_repository

    fake_form.return_value.validate_on_submit.return_value = False
    fake_form.return_value.errors = None

    old_team_copy = MagicMock(Team)
    old_team_copy.name = "Team"
    fake_copy.deepcopy.return_value = old_team_copy

    errors = 'errors'
    fake_form.return_value.errors = errors

    id = 1

    # Act
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
    id = 1
    model_kwargs = {
        'id': id,
        'name': "Team",
    }
    new_team = Team(**model_kwargs)

    fake_team_repository = MagicMock(TeamRepository)
    old_team = MagicMock(Team)
    fake_team_repository.get_team.return_value = old_team
    fake_injector.get.return_value = fake_team_repository

    old_team_copy = MagicMock(Team)
    old_team_copy.name = "Team 1"
    fake_copy.deepcopy.return_value = old_team_copy

    fake_form.return_value.validate_on_submit.return_value = True
    fake_form.return_value.name.data = new_team.name

    fake_team_factory.create_team.return_value = new_team

    # Act
    result = mod.edit(id)

    # Assert
    fake_injector.get.assert_called_once_with(TeamRepository)
    fake_team_repository.get_team.assert_called_once_with(id)
    fake_copy.deepcopy.assert_called_once_with(old_team)
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    view_kwargs = {
        'id': id,
        'name': new_team.name,
    }
    fake_team_factory.create_team.assert_called_once_with(**view_kwargs)
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
    id = 1
    model_kwargs = {
        'id': id,
        'name': "Team",
    }
    new_team = Team(**model_kwargs)

    fake_team_repository = MagicMock(TeamRepository)
    old_team = MagicMock(Team)
    fake_team_repository.get_team.return_value = old_team
    err = ValueError()
    fake_team_repository.update_team.side_effect = err
    fake_injector.get.return_value = fake_team_repository

    old_team_copy = MagicMock(Team)
    old_team_copy.name = "Team 1"
    fake_copy.deepcopy.return_value = old_team_copy

    fake_form.return_value.validate_on_submit.return_value = True
    fake_form.return_value.name.data = new_team.name

    fake_team_factory.create_team.return_value = new_team

    # Act
    result = mod.edit(id)

    # Assert
    fake_injector.get.assert_called_once_with(TeamRepository)
    fake_team_repository.get_team.assert_called_once_with(id)
    fake_copy.deepcopy.assert_called_once_with(old_team)
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    view_kwargs = {
        'id': id,
        'name': new_team.name,
    }
    fake_team_factory.create_team.assert_called_once_with(**view_kwargs)
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
    id = 1
    model_kwargs = {
        'id': id,
        'name': "Team",
    }
    new_team = Team(**model_kwargs)

    fake_team_repository = MagicMock(TeamRepository)
    old_team = MagicMock(Team)
    fake_team_repository.get_team.return_value = old_team
    err = IntegrityError('statement', 'params', Exception())
    fake_team_repository.update_team.side_effect = err
    fake_injector.get.return_value = fake_team_repository

    old_team_copy = MagicMock(Team)
    old_team_copy.name = "Team 1"
    fake_copy.deepcopy.return_value = old_team_copy

    fake_form.return_value.validate_on_submit.return_value = True
    fake_form.return_value.name.data = new_team.name

    fake_team_factory.create_team.return_value = new_team

    # Act
    result = mod.edit(id)

    # Assert
    fake_injector.get.assert_called_once_with(TeamRepository)
    fake_team_repository.get_team.assert_called_once_with(id)
    fake_copy.deepcopy.assert_called_once_with(old_team)
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    view_kwargs = {
        'id': id,
        'name': new_team.name,
    }
    fake_team_factory.create_team.assert_called_once_with(**view_kwargs)
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
    id = 1
    model_kwargs = {
        'id': id,
        'name': "Team",
    }
    new_team = Team(**model_kwargs)

    fake_team_repository = MagicMock(TeamRepository)
    old_team = MagicMock(Team)
    fake_team_repository.get_team.return_value = old_team
    fake_injector.get.return_value = fake_team_repository

    old_team_copy = MagicMock(Team)
    old_team_copy.name = "Team 1"
    fake_copy.deepcopy.return_value = old_team_copy

    fake_form.return_value.validate_on_submit.return_value = True
    fake_form.return_value.name.data = new_team.name

    err = IndexError()
    fake_url_for.side_effect = err

    # Act
    with pytest.raises(NotFound):
        result = mod.edit(id)

    # Assert
    fake_injector.get.assert_called_once_with(TeamRepository)
    fake_team_repository.get_team.assert_called_once_with(id)
    fake_copy.deepcopy.assert_called_once_with(old_team)
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    view_kwargs = {
        'id': id,
        'name': new_team.name,
    }
    fake_team_factory.create_team.assert_called_once_with(**view_kwargs)


@patch('app.flask.team_controller.injector')
def test_delete_when_team_not_found_should_abort_with_404_error(fake_injector, test_app):
    # Arrange
    id = 1

    fake_team_repository = MagicMock(TeamRepository)
    fake_team_repository.get_team.return_value = None
    fake_injector.get.return_value = fake_team_repository

    # Act
    with test_app.test_request_context(
            f'/teams/delete?id={id}',
            method='POST'
    ):
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
    id = 1

    fake_team_repository = MagicMock(TeamRepository)
    team = Team()
    fake_team_repository.get_team.return_value = team
    fake_injector.get.return_value = fake_team_repository

    # Act
    with test_app.test_request_context(
            f'/teams/delete?id={id}',
            method='GET'
    ):
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
        fake_injector, fake_flash, fake_url_for, fake_redirect, test_app
):
    # Arrange
    id = 1

    fake_team_repository = MagicMock(TeamRepository)
    team = Team()
    fake_team_repository.get_team.return_value = team
    fake_injector.get.return_value = fake_team_repository

    # Act
    with test_app.test_request_context(
            '/teams/delete?id=1',
            method='POST'
    ):
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
    id = 1

    fake_team_repository = MagicMock(TeamRepository)
    team = Team()
    fake_team_repository.get_team.return_value = team
    fake_team_repository.delete_team.side_effect = IndexError()
    fake_injector.get.return_value = fake_team_repository

    # Act
    with test_app.test_request_context(
            f'/teams/delete?id={id}',
            method='POST'
    ):
        with pytest.raises(NotFound):
            result = mod.delete(id)

    # Assert
    fake_injector.get.assert_called_once_with(TeamRepository)
    fake_team_repository.get_team.assert_called_once_with(id)
