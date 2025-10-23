from unittest.mock import patch

import pytest

from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound

import app.flask.team_controller as team_controller

from app.data.models.season import Season
from app.data.models.team import Team
from app.data.models.game import Game
from app.data.models.league_season import LeagueSeason
from app.data.models.team_season import TeamSeason

from test_app import create_app


@pytest.fixture()
def test_app():
    return create_app()


@patch('app.flask.team_controller.render_template')
@patch('app.flask.team_controller.team_repository')
def test_index_should_render_team_index_template(fake_team_repository, fake_render_template, test_app):
    # Act
    with test_app.app_context():
        result = team_controller.index()

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
        fake_render_template, fake_delete_team_form, fake_team_repository, test_app
):
    # Arrange
    id = 1

    # Act
    with test_app.app_context():
        result = team_controller.details(id)

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
        fake_delete_team_form, fake_team_repository, test_app
):
    # Arrange
    fake_team_repository.get_team.side_effect = IndexError()

    # Act
    with test_app.app_context():
        with pytest.raises(NotFound):
            result = team_controller.details(1)


@patch('app.flask.team_controller.render_template')
@patch('app.flask.team_controller.flash')
@patch('app.flask.team_controller.NewTeamForm')
def test_create_when_form_not_submitted_and_no_form_errors_should_render_create_template(
        fake_new_team_form, fake_flash, fake_render_template, test_app
):
    # Arrange
    fake_new_team_form.return_value.validate_on_submit.return_value = False
    fake_new_team_form.return_value.errors = None

    # Act
    with test_app.app_context():
        result = team_controller.create()

    # Assert
    fake_flash.assert_not_called()
    fake_render_template('teams/create.html', form=fake_new_team_form.return_value)
    assert result is fake_render_template.return_value


@patch('app.flask.team_controller.render_template')
@patch('app.flask.team_controller.flash')
@patch('app.flask.team_controller.NewTeamForm')
def test_create_when_form_not_submitted_and_form_errors_should_flash_errors_and_render_create_template(
        fake_new_team_form, fake_flash, fake_render_template, test_app
):
    # Arrange
    fake_new_team_form.return_value.validate_on_submit.return_value = False

    errors = 'errors'
    fake_new_team_form.return_value.errors = errors

    # Act
    with test_app.app_context():
        result = team_controller.create()

    # Assert
    fake_flash.assert_called_once_with(f"{errors}", 'danger')
    fake_render_template('teams/create.html', form=fake_new_team_form.return_value)
    assert result is fake_render_template.return_value


@patch('app.flask.team_controller.url_for')
@patch('app.flask.team_controller.flash')
@patch('app.flask.team_controller.team_repository')
@patch('app.flask.team_controller.redirect')
@patch('app.flask.team_controller.NewTeamForm')
def test_create_when_form_submitted_and_no_errors_caught_should_flash_success_message_and_redirect_to_team_index(
        fake_new_team_form, fake_redirect, fake_team_repository, fake_flash, fake_url_for, test_app
):
    # Arrange
    fake_new_team_form.return_value.validate_on_submit.return_value = True
    fake_new_team_form.return_value.name.data = "Chicago Cardinals"

    kwargs = {
        'name': "Chicago Cardinals",
    }

    # Act
    with test_app.app_context():
        result = team_controller.create()

    # Assert
    fake_team_repository.add_team.assert_called_once_with(**kwargs)
    fake_flash(f"Item {kwargs['name']} has been successfully submitted.", 'success')
    fake_url_for.assert_called_once_with('team.index')
    fake_redirect.assert_called_once_with(fake_url_for.return_value)
    assert result is fake_redirect.return_value


@patch('app.flask.team_controller.render_template')
@patch('app.flask.team_controller.flash')
@patch('app.flask.team_controller.team_repository')
@patch('app.flask.team_controller.NewTeamForm')
def test_create_when_form_submitted_and_value_error_caught_should_flash_error_message_and_render_create_template(
        fake_new_team_form, fake_team_repository, fake_flash, fake_render_template, test_app
):
    # Arrange
    fake_new_team_form.return_value.validate_on_submit.return_value = True
    fake_new_team_form.return_value.name.data = "Chicago Cardinals"

    err = ValueError()
    fake_team_repository.add_team.side_effect = err

    kwargs = {
        'name': "Chicago Cardinals",
    }

    # Act
    with test_app.app_context():
        result = team_controller.create()

    # Assert
    fake_team_repository.add_team.assert_called_once_with(**kwargs)
    fake_flash.assert_called_once_with(str(err), 'danger')
    fake_render_template.assert_called_once_with(
        'teams/create.html', team=None, form=fake_new_team_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.team_controller.render_template')
@patch('app.flask.team_controller.flash')
@patch('app.flask.team_controller.team_repository')
@patch('app.flask.team_controller.NewTeamForm')
def test_create_when_form_submitted_and_integrity_error_caught_should_flash_error_message_and_render_create_template(
        fake_new_team_form, fake_team_repository, fake_flash, fake_render_template, test_app
):
    # Arrange
    fake_new_team_form.return_value.validate_on_submit.return_value = True
    fake_new_team_form.return_value.name.data = "Chicago Cardinals"

    err = IntegrityError('statement', 'params', Exception())
    fake_team_repository.add_team.side_effect = err
    fake_team_repository.add_team.side_effect = err

    kwargs = {
        'name': "Chicago Cardinals",
    }

    # Act
    with test_app.app_context():
        result = team_controller.create()

    # Assert
    fake_team_repository.add_team.assert_called_once_with(**kwargs)
    fake_flash.assert_called_once_with(str(err), 'danger')
    fake_render_template.assert_called_once_with(
        'teams/create.html', team=None, form=fake_new_team_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.team_controller.team_repository')
def test_edit_when_team_not_found_should_abort_with_404_error(fake_team_repository, test_app):
    # Arrange
    team = None
    fake_team_repository.get_team.return_value = team

    # Act
    with test_app.app_context():
        with pytest.raises(NotFound):
            result = team_controller.edit(1)


@patch('app.flask.team_controller.render_template')
@patch('app.flask.team_controller.flash')
@patch('app.flask.team_controller.EditTeamForm')
@patch('app.flask.team_controller.team_repository')
def test_edit_when_team_found_and_form_not_submitted_and_no_form_errors_should_render_edit_template(
        fake_team_repository, fake_edit_team_form, fake_flash, fake_render_template, test_app
):
    with test_app.app_context():
        # Arrange
        team = Team(
            name="Chicago Cardinals"
        )
        fake_team_repository.get_team.return_value = team

        fake_edit_team_form.return_value.validate_on_submit.return_value = False
        fake_edit_team_form.return_value.errors = None

        # Act
        result = team_controller.edit(1)

    # Assert
    assert fake_edit_team_form.return_value.name.data == team.name
    fake_flash.assert_not_called()
    fake_render_template.assert_called_once_with(
        'teams/edit.html', team=team, form=fake_edit_team_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.team_controller.render_template')
@patch('app.flask.team_controller.flash')
@patch('app.flask.team_controller.EditTeamForm')
@patch('app.flask.team_controller.team_repository')
def test_edit_when_team_found_and_form_not_submitted_and_form_errors_should_flash_errors_and_render_edit_template(
        fake_team_repository, fake_edit_team_form, fake_flash, fake_render_template, test_app
):
    with test_app.app_context():
        # Arrange
        team = Team(
            name="Chicago Cardinals"
        )
        fake_team_repository.get_team.return_value = team

        fake_edit_team_form.return_value.validate_on_submit.return_value = False

        errors = 'errors'
        fake_edit_team_form.return_value.errors = errors

        # Act
        result = team_controller.edit(1)

    # Assert
    assert fake_edit_team_form.return_value.name.data == team.name
    fake_flash.assert_called_once_with(f"{errors}", 'danger')
    fake_render_template.assert_called_once_with(
        'teams/edit.html', team=team, form=fake_edit_team_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.team_controller.url_for')
@patch('app.flask.team_controller.flash')
@patch('app.flask.team_controller.redirect')
@patch('app.flask.team_controller.EditTeamForm')
@patch('app.flask.team_controller.team_repository')
def test_edit_when_team_found_and_form_submitted_and_no_errors_caught_should_flash_success_message_and_redirect_to_team_details(
        fake_team_repository, fake_edit_team_form, fake_redirect, fake_flash, fake_url_for, test_app
):
    with test_app.app_context():
        # Arrange
        team = Team(
            name="Chicago Cardinals"
        )
        fake_team_repository.get_team.return_value = team

        fake_edit_team_form.return_value.validate_on_submit.return_value = True
        fake_edit_team_form.return_value.name.data = "Chicago Cardinals"

        id = 1
        kwargs = {
            'id': id,
            'name': "Chicago Cardinals",
        }

        # Act
        result = team_controller.edit(id)

    # Assert
    fake_team_repository.update_team.assert_called_once_with(**kwargs)
    fake_flash.assert_called_once_with(
        f"Item {fake_edit_team_form.return_value.name.data} has been successfully updated.", 'success'
    )
    fake_url_for.assert_called_once_with('team.details', id=id)
    fake_redirect.assert_called_once_with(fake_url_for.return_value)
    assert result is fake_redirect.return_value


@patch('app.flask.team_controller.flash')
@patch('app.flask.team_controller.render_template')
@patch('app.flask.team_controller.EditTeamForm')
@patch('app.flask.team_controller.team_repository')
def test_edit_when_team_found_and_form_submitted_and_value_error_caught_should_flash_error_message_and_render_edit_template(
        fake_team_repository, fake_edit_team_form, fake_render_template, fake_flash, test_app
):
    with test_app.app_context():
        # Arrange
        team = Team(
            name="Chicago Cardinals"
        )
        fake_team_repository.get_team.return_value = team

        fake_edit_team_form.return_value.validate_on_submit.return_value = True
        fake_edit_team_form.return_value.name.data = "Chicago Cardinals"

        err = ValueError()
        fake_team_repository.update_team.side_effect = err

        id = 1
        kwargs = {
            'id': id,
            'name': "Chicago Cardinals",
        }

        # Act
        result = team_controller.edit(id)

    # Assert
    fake_team_repository.update_team.assert_called_once_with(**kwargs)
    fake_flash.assert_called_once_with(str(err), 'danger')
    fake_render_template.assert_called_once_with(
        'teams/edit.html', team=team, form=fake_edit_team_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.team_controller.flash')
@patch('app.flask.team_controller.render_template')
@patch('app.flask.team_controller.EditTeamForm')
@patch('app.flask.team_controller.team_repository')
def test_edit_when_team_found_and_form_submitted_and_integrity_error_caught_should_flash_error_message_and_render_edit_template(
        fake_team_repository, fake_edit_team_form, fake_render_template, fake_flash, test_app
):
    with test_app.app_context():
        # Arrange
        team = Team(
            name="Chicago Cardinals"
        )
        fake_team_repository.get_team.return_value = team

        fake_edit_team_form.return_value.validate_on_submit.return_value = True
        fake_edit_team_form.return_value.name.data = "Chicago Cardinals"

        err = IntegrityError('statement', 'params', Exception())
        fake_team_repository.update_team.side_effect = err

        id = 1
        kwargs = {
            'id': id,
            'name': "Chicago Cardinals",
        }

        # Act
        result = team_controller.edit(id)

    # Assert
    fake_team_repository.update_team.assert_called_once_with(**kwargs)
    fake_flash.assert_called_once_with(str(err), 'danger')
    fake_render_template.assert_called_once_with(
        'teams/edit.html', team=team, form=fake_edit_team_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.team_controller.render_template')
@patch('app.flask.team_controller.team_repository')
def test_delete_when_request_method_is_get_should_render_delete_template(
        fake_team_repository, fake_render_template, test_app
):
    # Arrange
    team = Team(name="Chicago Cardinals")
    fake_team_repository.get_team.return_value = team

    # Act
    with test_app.test_request_context(
            '/teams/delete?id=1',
            method='GET'
    ):
        with test_app.app_context():
            result = team_controller.delete(1)

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
    team = Team(name="Chicago Cardinals")
    fake_team_repository.get_team.return_value = team

    # Act
    id = 1
    with test_app.test_request_context(
            '/teams/delete?id=1',
            method='POST'
    ):
        with test_app.app_context():
            result = team_controller.delete(id)

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
    team = Team(name="Chicago Cardinals")
    fake_team_repository.get_team.return_value = team
    fake_team_repository.delete_team.side_effect = IndexError()

    # Act
    with test_app.test_request_context(
            '/teams/delete?id=1',
            method='POST'
    ):
        with test_app.app_context():
            with pytest.raises(NotFound):
                result = team_controller.delete(1)
