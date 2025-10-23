from unittest.mock import patch

import pytest

from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound

import app.flask.division_controller as division_controller

from app.data.models.season import Season
from app.data.models.division import Division
from app.data.models.game import Game
from app.data.models.league_season import LeagueSeason
from app.data.models.team_season import TeamSeason

from test_app import create_app


@pytest.fixture()
def test_app():
    return create_app()


@patch('app.flask.division_controller.render_template')
@patch('app.flask.division_controller.division_repository')
def test_index_should_render_division_index_template(fake_division_repository, fake_render_template, test_app):
    # Act
    with test_app.app_context():
        result = division_controller.index()

    # Assert
    fake_division_repository.get_divisions.assert_called_once()
    fake_render_template.assert_called_once_with(
        'divisions/index.html', divisions=fake_division_repository.get_divisions.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.division_controller.division_repository')
@patch('app.flask.division_controller.DeleteDivisionForm')
@patch('app.flask.division_controller.render_template')
def test_details_when_division_found_should_render_division_details_template(
        fake_render_template, fake_delete_division_form, fake_division_repository, test_app
):
    # Arrange
    id = 1

    # Act
    with test_app.app_context():
        result = division_controller.details(id)

    # Assert
    fake_delete_division_form.assert_called_once()
    fake_division_repository.get_division.assert_called_once_with(id)
    fake_render_template.assert_called_once_with(
        'divisions/details.html',
        division=fake_division_repository.get_division.return_value,
        delete_division_form=fake_delete_division_form.return_value
    )
    assert result == fake_render_template.return_value


@patch('app.flask.division_controller.division_repository')
@patch('app.flask.division_controller.DeleteDivisionForm')
def test_details_when_division_not_found_should_abort_with_404_error(
        fake_delete_division_form, fake_division_repository, test_app
):
    # Arrange
    fake_division_repository.get_division.side_effect = IndexError()

    # Act
    with test_app.app_context():
        with pytest.raises(NotFound):
            result = division_controller.details(1)


@patch('app.flask.division_controller.render_template')
@patch('app.flask.division_controller.flash')
@patch('app.flask.division_controller.NewDivisionForm')
def test_create_when_form_not_submitted_and_no_form_errors_should_render_create_template(
        fake_new_division_form, fake_flash, fake_render_template, test_app
):
    # Arrange
    fake_new_division_form.return_value.validate_on_submit.return_value = False
    fake_new_division_form.return_value.errors = None

    # Act
    with test_app.app_context():
        result = division_controller.create()

    # Assert
    fake_flash.assert_not_called()
    fake_render_template('divisions/create.html', form=fake_new_division_form.return_value)
    assert result is fake_render_template.return_value


@patch('app.flask.division_controller.render_template')
@patch('app.flask.division_controller.flash')
@patch('app.flask.division_controller.NewDivisionForm')
def test_create_when_form_not_submitted_and_form_errors_should_flash_errors_and_render_create_template(
        fake_new_division_form, fake_flash, fake_render_template, test_app
):
    # Arrange
    fake_new_division_form.return_value.validate_on_submit.return_value = False

    errors = 'errors'
    fake_new_division_form.return_value.errors = errors

    # Act
    with test_app.app_context():
        result = division_controller.create()

    # Assert
    fake_flash.assert_called_once_with(f"{errors}", 'danger')
    fake_render_template('divisions/create.html', form=fake_new_division_form.return_value)
    assert result is fake_render_template.return_value


@patch('app.flask.division_controller.url_for')
@patch('app.flask.division_controller.flash')
@patch('app.flask.division_controller.division_repository')
@patch('app.flask.division_controller.redirect')
@patch('app.flask.division_controller.NewDivisionForm')
def test_create_when_form_submitted_and_no_errors_caught_should_flash_success_message_and_redirect_to_division_index(
        fake_new_division_form, fake_redirect, fake_division_repository, fake_flash, fake_url_for, test_app
):
    # Arrange
    fake_new_division_form.return_value.validate_on_submit.return_value = True
    fake_new_division_form.return_value.name.data = "NFC East"
    fake_new_division_form.return_value.league_name.data = "NFL"
    fake_new_division_form.return_value.conference_name.data = "NFC"
    fake_new_division_form.return_value.first_season_year.data = 1970
    fake_new_division_form.return_value.last_season_year.data = None

    kwargs = {
        'name': "NFC East",
        'league_name': "NFL",
        'conference_name': "NFC",
        'first_season_year': 1970,
        'last_season_year': None
    }

    # Act
    with test_app.app_context():
        result = division_controller.create()

    # Assert
    fake_division_repository.add_division.assert_called_once_with(**kwargs)
    fake_flash(f"Item {kwargs['name']} has been successfully submitted.", 'success')
    fake_url_for.assert_called_once_with('division.index')
    fake_redirect.assert_called_once_with(fake_url_for.return_value)
    assert result is fake_redirect.return_value


@patch('app.flask.division_controller.render_template')
@patch('app.flask.division_controller.flash')
@patch('app.flask.division_controller.division_repository')
@patch('app.flask.division_controller.NewDivisionForm')
def test_create_when_form_submitted_and_value_error_caught_should_flash_error_message_and_render_create_template(
        fake_new_division_form, fake_division_repository, fake_flash, fake_render_template, test_app
):
    # Arrange
    fake_new_division_form.return_value.validate_on_submit.return_value = True
    fake_new_division_form.return_value.name.data = "NFC East"
    fake_new_division_form.return_value.league_name.data = "NFL"
    fake_new_division_form.return_value.conference_name.data = "NFC"
    fake_new_division_form.return_value.first_season_year.data = 1970
    fake_new_division_form.return_value.last_season_year.data = None

    err = ValueError()
    fake_division_repository.add_division.side_effect = err

    kwargs = {
        'name': "NFC East",
        'league_name': "NFL",
        'conference_name': "NFC",
        'first_season_year': 1970,
        'last_season_year': None
    }

    # Act
    with test_app.app_context():
        result = division_controller.create()

    # Assert
    fake_division_repository.add_division.assert_called_once_with(**kwargs)
    fake_flash.assert_called_once_with(str(err), 'danger')
    fake_render_template.assert_called_once_with(
        'divisions/create.html', division=None, form=fake_new_division_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.division_controller.render_template')
@patch('app.flask.division_controller.flash')
@patch('app.flask.division_controller.division_repository')
@patch('app.flask.division_controller.NewDivisionForm')
def test_create_when_form_submitted_and_integrity_error_caught_should_flash_error_message_and_render_create_template(
        fake_new_division_form, fake_division_repository, fake_flash, fake_render_template, test_app
):
    # Arrange
    fake_new_division_form.return_value.validate_on_submit.return_value = True
    fake_new_division_form.return_value.name.data = "NFC East"
    fake_new_division_form.return_value.league_name.data = "NFL"
    fake_new_division_form.return_value.conference_name.data = "NFC"
    fake_new_division_form.return_value.first_season_year.data = 1970
    fake_new_division_form.return_value.last_season_year.data = None

    err = IntegrityError('statement', 'params', Exception())
    fake_division_repository.add_division.side_effect = err
    fake_division_repository.add_division.side_effect = err

    kwargs = {
        'name': "NFC East",
        'league_name': "NFL",
        'conference_name': "NFC",
        'first_season_year': 1970,
        'last_season_year': None
    }

    # Act
    with test_app.app_context():
        result = division_controller.create()

    # Assert
    fake_division_repository.add_division.assert_called_once_with(**kwargs)
    fake_flash.assert_called_once_with(str(err), 'danger')
    fake_render_template.assert_called_once_with(
        'divisions/create.html', division=None, form=fake_new_division_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.division_controller.division_repository')
def test_edit_when_division_not_found_should_abort_with_404_error(fake_division_repository, test_app):
    # Arrange
    division = None
    fake_division_repository.get_division.return_value = division

    # Act
    with test_app.app_context():
        with pytest.raises(NotFound):
            result = division_controller.edit(1)


@patch('app.flask.division_controller.render_template')
@patch('app.flask.division_controller.flash')
@patch('app.flask.division_controller.EditDivisionForm')
@patch('app.flask.division_controller.division_repository')
def test_edit_when_division_found_and_form_not_submitted_and_no_form_errors_should_render_edit_template(
        fake_division_repository, fake_edit_division_form, fake_flash, fake_render_template, test_app
):
    with test_app.app_context():
        # Arrange
        division = Division(
            name="NFC East",
            league_name="NFL",
            conference_name="NFC",
            first_season_year=1970,
            last_season_year=None
        )
        fake_division_repository.get_division.return_value = division

        fake_edit_division_form.return_value.validate_on_submit.return_value = False
        fake_edit_division_form.return_value.errors = None

        # Act
        result = division_controller.edit(1)

    # Assert
    assert fake_edit_division_form.return_value.name.data == division.name
    assert fake_edit_division_form.return_value.league_name.data == division.league_name
    assert fake_edit_division_form.return_value.conference_name.data == division.conference_name
    assert fake_edit_division_form.return_value.first_season_year.data == division.first_season_year
    assert fake_edit_division_form.return_value.last_season_year.data == division.last_season_year
    fake_flash.assert_not_called()
    fake_render_template.assert_called_once_with(
        'divisions/edit.html', division=division, form=fake_edit_division_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.division_controller.render_template')
@patch('app.flask.division_controller.flash')
@patch('app.flask.division_controller.EditDivisionForm')
@patch('app.flask.division_controller.division_repository')
def test_edit_when_division_found_and_form_not_submitted_and_form_errors_should_flash_errors_and_render_edit_template(
        fake_division_repository, fake_edit_division_form, fake_flash, fake_render_template, test_app
):
    with test_app.app_context():
        # Arrange
        division = Division(
            name="NFC East",
            league_name="NFL",
            conference_name="NFC",
            first_season_year=1970,
            last_season_year=None
        )
        fake_division_repository.get_division.return_value = division

        fake_edit_division_form.return_value.validate_on_submit.return_value = False

        errors = 'errors'
        fake_edit_division_form.return_value.errors = errors

        # Act
        result = division_controller.edit(1)

    # Assert
    assert fake_edit_division_form.return_value.name.data == division.name
    assert fake_edit_division_form.return_value.league_name.data == division.league_name
    assert fake_edit_division_form.return_value.conference_name.data == division.conference_name
    assert fake_edit_division_form.return_value.first_season_year.data == division.first_season_year
    assert fake_edit_division_form.return_value.last_season_year.data == division.last_season_year
    fake_flash.assert_called_once_with(f"{errors}", 'danger')
    fake_render_template.assert_called_once_with(
        'divisions/edit.html', division=division, form=fake_edit_division_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.division_controller.url_for')
@patch('app.flask.division_controller.flash')
@patch('app.flask.division_controller.redirect')
@patch('app.flask.division_controller.EditDivisionForm')
@patch('app.flask.division_controller.division_repository')
def test_edit_when_division_found_and_form_submitted_and_no_errors_caught_should_flash_success_message_and_redirect_to_division_details(
        fake_division_repository, fake_edit_division_form, fake_redirect, fake_flash, fake_url_for, test_app
):
    with test_app.app_context():
        # Arrange
        division = Division(
            name="NFC East",
            league_name="NFL",
            conference_name="NFC",
            first_season_year=1970,
            last_season_year=None
        )
        fake_division_repository.get_division.return_value = division

        fake_edit_division_form.return_value.validate_on_submit.return_value = True
        fake_edit_division_form.return_value.name.data = "AFC West"
        fake_edit_division_form.return_value.league_name.data = "NFL"
        fake_edit_division_form.return_value.conference_name.data = "AFC"
        fake_edit_division_form.return_value.first_season_year.data = 1970
        fake_edit_division_form.return_value.last_season_year.data = None

        id = 1
        kwargs = {
            'id': id,
            'name': "AFC West",
            'league_name': "NFL",
            'conference_name': "AFC",
            'first_season_year': 1970,
            'last_season_year': None
        }

        # Act
        result = division_controller.edit(id)

    # Assert
    fake_division_repository.update_division.assert_called_once_with(**kwargs)
    fake_flash.assert_called_once_with(
        f"Item {fake_edit_division_form.return_value.name.data} has been successfully updated.", 'success'
    )
    fake_url_for.assert_called_once_with('division.details', id=id)
    fake_redirect.assert_called_once_with(fake_url_for.return_value)
    assert result is fake_redirect.return_value


@patch('app.flask.division_controller.flash')
@patch('app.flask.division_controller.render_template')
@patch('app.flask.division_controller.EditDivisionForm')
@patch('app.flask.division_controller.division_repository')
def test_edit_when_division_found_and_form_submitted_and_value_error_caught_should_flash_error_message_and_render_edit_template(
        fake_division_repository, fake_edit_division_form, fake_render_template, fake_flash, test_app
):
    with test_app.app_context():
        # Arrange
        division = Division(
            name="NFC East",
            league_name="NFL",
            conference_name="NFC",
            first_season_year=1970,
            last_season_year=None
        )
        fake_division_repository.get_division.return_value = division

        fake_edit_division_form.return_value.validate_on_submit.return_value = True
        fake_edit_division_form.return_value.name.data = "AFC West"
        fake_edit_division_form.return_value.league_name.data = "NFL"
        fake_edit_division_form.return_value.conference_name.data = "AFC"
        fake_edit_division_form.return_value.first_season_year.data = 1970
        fake_edit_division_form.return_value.last_season_year.data = None

        err = ValueError()
        fake_division_repository.update_division.side_effect = err

        id = 1
        kwargs = {
            'id': id,
            'name': "AFC West",
            'league_name': "NFL",
            'conference_name': "AFC",
            'first_season_year': 1970,
            'last_season_year': None
        }

        # Act
        result = division_controller.edit(id)

    # Assert
    fake_division_repository.update_division.assert_called_once_with(**kwargs)
    fake_flash.assert_called_once_with(str(err), 'danger')
    fake_render_template.assert_called_once_with(
        'divisions/edit.html', division=division, form=fake_edit_division_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.division_controller.flash')
@patch('app.flask.division_controller.render_template')
@patch('app.flask.division_controller.EditDivisionForm')
@patch('app.flask.division_controller.division_repository')
def test_edit_when_division_found_and_form_submitted_and_integrity_error_caught_should_flash_error_message_and_render_edit_template(
        fake_division_repository, fake_edit_division_form, fake_render_template, fake_flash, test_app
):
    with test_app.app_context():
        # Arrange
        # Arrange
        division = Division(
            name="NFC East",
            league_name="NFL",
            conference_name="NFC",
            first_season_year=1970,
            last_season_year=None
        )
        fake_division_repository.get_division.return_value = division

        fake_edit_division_form.return_value.validate_on_submit.return_value = True
        fake_edit_division_form.return_value.name.data = "AFC West"
        fake_edit_division_form.return_value.league_name.data = "NFL"
        fake_edit_division_form.return_value.conference_name.data = "AFC"
        fake_edit_division_form.return_value.first_season_year.data = 1970
        fake_edit_division_form.return_value.last_season_year.data = None

        err = IntegrityError('statement', 'params', Exception())
        fake_division_repository.update_division.side_effect = err

        id = 1
        kwargs = {
            'id': id,
            'name': "AFC West",
            'league_name': "NFL",
            'conference_name': "AFC",
            'first_season_year': 1970,
            'last_season_year': None
        }

        # Act
        result = division_controller.edit(id)

    # Assert
    fake_division_repository.update_division.assert_called_once_with(**kwargs)
    fake_flash.assert_called_once_with(str(err), 'danger')
    fake_render_template.assert_called_once_with(
        'divisions/edit.html', division=division, form=fake_edit_division_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.division_controller.render_template')
@patch('app.flask.division_controller.division_repository')
def test_delete_when_request_method_is_get_should_render_delete_template(
        fake_division_repository, fake_render_template, test_app
):
    # Arrange
    division = Division()
    fake_division_repository.get_division.return_value = division

    # Act
    with test_app.test_request_context(
            '/divisions/delete?id=1',
            method='GET'
    ):
        with test_app.app_context():
            result = division_controller.delete(1)

    # Assert
    fake_division_repository.get_division.assert_called_once_with(1)
    fake_render_template.assert_called_once_with('divisions/delete.html', division=division)
    assert result is fake_render_template.return_value


@patch('app.flask.division_controller.redirect')
@patch('app.flask.division_controller.url_for')
@patch('app.flask.division_controller.flash')
@patch('app.flask.division_controller.division_repository')
def test_delete_when_request_method_is_post_and_division_found_should_flash_success_message_and_redirect_to_divisions_index(
        fake_division_repository, fake_flash, fake_url_for, fake_redirect, test_app
):
    # Arrange
    division = Division()
    fake_division_repository.get_division.return_value = division

    # Act
    id = 1
    with test_app.test_request_context(
            '/divisions/delete?id=1',
            method='POST'
    ):
        with test_app.app_context():
            result = division_controller.delete(id)

    # Assert
    fake_division_repository.delete_division.assert_called_once_with(id)
    fake_flash.assert_called_once_with(f"Division {division.name} has been successfully deleted.", 'success')
    fake_url_for.assert_called_once_with('division.index')
    fake_redirect.assert_called_once_with(fake_url_for.return_value)
    assert result is fake_redirect.return_value


@patch('app.flask.division_controller.division_repository')
def test_delete_when_request_method_is_post_and_division_not_found_should_abort_with_404_error(
        fake_division_repository, test_app
):
    # Arrange
    division = Division()
    fake_division_repository.get_division.return_value = division
    fake_division_repository.delete_division.side_effect = IndexError()

    # Act
    with test_app.test_request_context(
            '/divisions/delete?id=1',
            method='POST'
    ):
        with test_app.app_context():
            with pytest.raises(NotFound):
                result = division_controller.delete(1)
