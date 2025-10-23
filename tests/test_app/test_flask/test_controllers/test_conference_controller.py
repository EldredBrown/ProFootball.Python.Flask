from unittest.mock import patch

import pytest

from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound

import app.flask.conference_controller as conference_controller

from app.data.models.season import Season
from app.data.models.conference import Conference
from app.data.models.game import Game
from app.data.models.league_season import LeagueSeason
from app.data.models.team_season import TeamSeason

from test_app import create_app


@pytest.fixture()
def test_app():
    return create_app()


@patch('app.flask.conference_controller.render_template')
@patch('app.flask.conference_controller.conference_repository')
def test_index_should_render_conference_index_template(fake_conference_repository, fake_render_template, test_app):
    # Act
    with test_app.app_context():
        result = conference_controller.index()

    # Assert
    fake_conference_repository.get_conferences.assert_called_once()
    fake_render_template.assert_called_once_with(
        'conferences/index.html', conferences=fake_conference_repository.get_conferences.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.conference_controller.conference_repository')
@patch('app.flask.conference_controller.DeleteConferenceForm')
@patch('app.flask.conference_controller.render_template')
def test_details_when_conference_found_should_render_conference_details_template(
        fake_render_template, fake_delete_conference_form, fake_conference_repository, test_app
):
    # Arrange
    id = 1

    # Act
    with test_app.app_context():
        result = conference_controller.details(id)

    # Assert
    fake_delete_conference_form.assert_called_once()
    fake_conference_repository.get_conference.assert_called_once_with(id)
    fake_render_template.assert_called_once_with(
        'conferences/details.html',
        conference=fake_conference_repository.get_conference.return_value,
        delete_conference_form=fake_delete_conference_form.return_value
    )
    assert result == fake_render_template.return_value


@patch('app.flask.conference_controller.conference_repository')
@patch('app.flask.conference_controller.DeleteConferenceForm')
def test_details_when_conference_not_found_should_abort_with_404_error(
        fake_delete_conference_form, fake_conference_repository, test_app
):
    # Arrange
    fake_conference_repository.get_conference.side_effect = IndexError()

    # Act
    with test_app.app_context():
        with pytest.raises(NotFound):
            result = conference_controller.details(1)


@patch('app.flask.conference_controller.render_template')
@patch('app.flask.conference_controller.flash')
@patch('app.flask.conference_controller.NewConferenceForm')
def test_create_when_form_not_submitted_and_no_form_errors_should_render_create_template(
        fake_new_conference_form, fake_flash, fake_render_template, test_app
):
    # Arrange
    fake_new_conference_form.return_value.validate_on_submit.return_value = False
    fake_new_conference_form.return_value.errors = None

    # Act
    with test_app.app_context():
        result = conference_controller.create()

    # Assert
    fake_flash.assert_not_called()
    fake_render_template('conferences/create.html', form=fake_new_conference_form.return_value)
    assert result is fake_render_template.return_value


@patch('app.flask.conference_controller.render_template')
@patch('app.flask.conference_controller.flash')
@patch('app.flask.conference_controller.NewConferenceForm')
def test_create_when_form_not_submitted_and_form_errors_should_flash_errors_and_render_create_template(
        fake_new_conference_form, fake_flash, fake_render_template, test_app
):
    # Arrange
    fake_new_conference_form.return_value.validate_on_submit.return_value = False

    errors = 'errors'
    fake_new_conference_form.return_value.errors = errors

    # Act
    with test_app.app_context():
        result = conference_controller.create()

    # Assert
    fake_flash.assert_called_once_with(f"{errors}", 'danger')
    fake_render_template('conferences/create.html', form=fake_new_conference_form.return_value)
    assert result is fake_render_template.return_value


@patch('app.flask.conference_controller.url_for')
@patch('app.flask.conference_controller.flash')
@patch('app.flask.conference_controller.conference_repository')
@patch('app.flask.conference_controller.redirect')
@patch('app.flask.conference_controller.NewConferenceForm')
def test_create_when_form_submitted_and_no_errors_caught_should_flash_success_message_and_redirect_to_conference_index(
        fake_new_conference_form, fake_redirect, fake_conference_repository, fake_flash, fake_url_for, test_app
):
    # Arrange
    fake_new_conference_form.return_value.validate_on_submit.return_value = True
    fake_new_conference_form.return_value.short_name.data = "NFC"
    fake_new_conference_form.return_value.long_name.data = "National Football Conference"
    fake_new_conference_form.return_value.league_name.data = "NFL"
    fake_new_conference_form.return_value.first_season_year.data = 1970
    fake_new_conference_form.return_value.last_season_year.data = None

    kwargs = {
        'short_name': "NFC",
        'long_name': "National Football Conference",
        'league_name': "NFL",
        'first_season_year': 1970,
        'last_season_year': None,
    }

    # Act
    with test_app.app_context():
        result = conference_controller.create()

    # Assert
    fake_conference_repository.add_conference.assert_called_once_with(**kwargs)
    fake_flash(f"Item {kwargs['short_name']} has been successfully submitted.", 'success')
    fake_url_for.assert_called_once_with('conference.index')
    fake_redirect.assert_called_once_with(fake_url_for.return_value)
    assert result is fake_redirect.return_value


@patch('app.flask.conference_controller.render_template')
@patch('app.flask.conference_controller.flash')
@patch('app.flask.conference_controller.conference_repository')
@patch('app.flask.conference_controller.NewConferenceForm')
def test_create_when_form_submitted_and_value_error_caught_should_flash_error_message_and_render_create_template(
        fake_new_conference_form, fake_conference_repository, fake_flash, fake_render_template, test_app
):
    # Arrange
    fake_new_conference_form.return_value.validate_on_submit.return_value = True
    fake_new_conference_form.return_value.short_name.data = "NFC"
    fake_new_conference_form.return_value.long_name.data = "National Football Conference"
    fake_new_conference_form.return_value.league_name.data = "NFL"
    fake_new_conference_form.return_value.first_season_year.data = 1970
    fake_new_conference_form.return_value.last_season_year.data = None

    err = ValueError()
    fake_conference_repository.add_conference.side_effect = err

    kwargs = {
        'short_name': "NFC",
        'long_name': "National Football Conference",
        'league_name': "NFL",
        'first_season_year': 1970,
        'last_season_year': None,
    }

    # Act
    with test_app.app_context():
        result = conference_controller.create()

    # Assert
    fake_conference_repository.add_conference.assert_called_once_with(**kwargs)
    fake_flash.assert_called_once_with(str(err), 'danger')
    fake_render_template.assert_called_once_with(
        'conferences/create.html', conference=None, form=fake_new_conference_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.conference_controller.render_template')
@patch('app.flask.conference_controller.flash')
@patch('app.flask.conference_controller.conference_repository')
@patch('app.flask.conference_controller.NewConferenceForm')
def test_create_when_form_submitted_and_integrity_error_caught_should_flash_error_message_and_render_create_template(
        fake_new_conference_form, fake_conference_repository, fake_flash, fake_render_template, test_app
):
    # Arrange
    fake_new_conference_form.return_value.validate_on_submit.return_value = True
    fake_new_conference_form.return_value.short_name.data = "NFC"
    fake_new_conference_form.return_value.long_name.data = "National Football Conference"
    fake_new_conference_form.return_value.league_name.data = "NFL"
    fake_new_conference_form.return_value.first_season_year.data = 1970
    fake_new_conference_form.return_value.last_season_year.data = None

    err = IntegrityError('statement', 'params', Exception())
    fake_conference_repository.add_conference.side_effect = err
    fake_conference_repository.add_conference.side_effect = err

    kwargs = {
        'short_name': "NFC",
        'long_name': "National Football Conference",
        'league_name': "NFL",
        'first_season_year': 1970,
        'last_season_year': None,
    }

    # Act
    with test_app.app_context():
        result = conference_controller.create()

    # Assert
    fake_conference_repository.add_conference.assert_called_once_with(**kwargs)
    fake_flash.assert_called_once_with(str(err), 'danger')
    fake_render_template.assert_called_once_with(
        'conferences/create.html', conference=None, form=fake_new_conference_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.conference_controller.conference_repository')
def test_edit_when_conference_not_found_should_abort_with_404_error(fake_conference_repository, test_app):
    # Arrange
    conference = None
    fake_conference_repository.get_conference.return_value = conference

    # Act
    with test_app.app_context():
        with pytest.raises(NotFound):
            result = conference_controller.edit(1)


@patch('app.flask.conference_controller.render_template')
@patch('app.flask.conference_controller.flash')
@patch('app.flask.conference_controller.EditConferenceForm')
@patch('app.flask.conference_controller.conference_repository')
def test_edit_when_conference_found_and_form_not_submitted_and_no_form_errors_should_render_edit_template(
        fake_conference_repository, fake_edit_conference_form, fake_flash, fake_render_template, test_app
):
    with test_app.app_context():
        # Arrange
        conference = Conference(
            short_name="NFC",
            long_name="National Football Conference",
            league_name="NFL",
            first_season_year=1970,
            last_season_year=None
        )
        fake_conference_repository.get_conference.return_value = conference

        fake_edit_conference_form.return_value.validate_on_submit.return_value = False
        fake_edit_conference_form.return_value.errors = None

        # Act
        result = conference_controller.edit(1)

    # Assert
    assert fake_edit_conference_form.return_value.short_name.data == conference.short_name
    assert fake_edit_conference_form.return_value.long_name.data == conference.long_name
    assert fake_edit_conference_form.return_value.league_name.data == conference.league_name
    assert fake_edit_conference_form.return_value.first_season_year.data == conference.first_season_year
    assert fake_edit_conference_form.return_value.last_season_year.data == conference.last_season_year
    fake_flash.assert_not_called()
    fake_render_template.assert_called_once_with(
        'conferences/edit.html', conference=conference, form=fake_edit_conference_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.conference_controller.render_template')
@patch('app.flask.conference_controller.flash')
@patch('app.flask.conference_controller.EditConferenceForm')
@patch('app.flask.conference_controller.conference_repository')
def test_edit_when_conference_found_and_form_not_submitted_and_form_errors_should_flash_errors_and_render_edit_template(
        fake_conference_repository, fake_edit_conference_form, fake_flash, fake_render_template, test_app
):
    with test_app.app_context():
        # Arrange
        conference = Conference(
            short_name="NFC",
            long_name="National Football Conference",
            league_name="NFL",
            first_season_year=1970,
            last_season_year=None
        )
        fake_conference_repository.get_conference.return_value = conference

        fake_edit_conference_form.return_value.validate_on_submit.return_value = False

        errors = 'errors'
        fake_edit_conference_form.return_value.errors = errors

        # Act
        result = conference_controller.edit(1)

    # Assert
    assert fake_edit_conference_form.return_value.short_name.data == conference.short_name
    assert fake_edit_conference_form.return_value.long_name.data == conference.long_name
    assert fake_edit_conference_form.return_value.league_name.data == conference.league_name
    assert fake_edit_conference_form.return_value.first_season_year.data == conference.first_season_year
    assert fake_edit_conference_form.return_value.last_season_year.data == conference.last_season_year
    fake_flash.assert_called_once_with(f"{errors}", 'danger')
    fake_render_template.assert_called_once_with(
        'conferences/edit.html', conference=conference, form=fake_edit_conference_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.conference_controller.url_for')
@patch('app.flask.conference_controller.flash')
@patch('app.flask.conference_controller.redirect')
@patch('app.flask.conference_controller.EditConferenceForm')
@patch('app.flask.conference_controller.conference_repository')
def test_edit_when_conference_found_and_form_submitted_and_no_errors_caught_should_flash_success_message_and_redirect_to_conference_details(
        fake_conference_repository, fake_edit_conference_form, fake_redirect, fake_flash, fake_url_for, test_app
):
    with test_app.app_context():
        # Arrange
        conference = Conference(
            short_name="NFC",
            long_name="National Football Conference",
            league_name="NFL",
            first_season_year=1970,
            last_season_year=None
        )
        fake_conference_repository.get_conference.return_value = conference

        fake_edit_conference_form.return_value.validate_on_submit.return_value = True
        fake_edit_conference_form.return_value.short_name.data = "AFC"
        fake_edit_conference_form.return_value.long_name.data = "American Football Conference"
        fake_edit_conference_form.return_value.league_name.data = "NFL"
        fake_edit_conference_form.return_value.first_season_year.data = 1970
        fake_edit_conference_form.return_value.last_season_year.data = None

        id = 1
        kwargs = {
            'id': id,
            'short_name': "AFC",
            'long_name': "American Football Conference",
            'league_name': "NFL",
            'first_season_year': 1970,
            'last_season_year': None,
        }

        # Act
        result = conference_controller.edit(id)

    # Assert
    fake_conference_repository.update_conference.assert_called_once_with(**kwargs)
    fake_flash.assert_called_once_with(
        f"Item {fake_edit_conference_form.return_value.short_name.data} has been successfully updated.", 'success'
    )
    fake_url_for.assert_called_once_with('conference.details', id=id)
    fake_redirect.assert_called_once_with(fake_url_for.return_value)
    assert result is fake_redirect.return_value


@patch('app.flask.conference_controller.flash')
@patch('app.flask.conference_controller.render_template')
@patch('app.flask.conference_controller.EditConferenceForm')
@patch('app.flask.conference_controller.conference_repository')
def test_edit_when_conference_found_and_form_submitted_and_value_error_caught_should_flash_error_message_and_render_edit_template(
        fake_conference_repository, fake_edit_conference_form, fake_render_template, fake_flash, test_app
):
    with test_app.app_context():
        # Arrange
        conference = Conference(
            short_name="NFC",
            long_name="National Football Conference",
            league_name="NFL",
            first_season_year=1970,
            last_season_year=None
        )
        fake_conference_repository.get_conference.return_value = conference

        fake_edit_conference_form.return_value.validate_on_submit.return_value = True
        fake_edit_conference_form.return_value.short_name.data = "AFC"
        fake_edit_conference_form.return_value.long_name.data = "American Football Conference"
        fake_edit_conference_form.return_value.league_name.data = "NFL"
        fake_edit_conference_form.return_value.first_season_year.data = 1970
        fake_edit_conference_form.return_value.last_season_year.data = None

        err = ValueError()
        fake_conference_repository.update_conference.side_effect = err

        id = 1
        kwargs = {
            'id': id,
            'short_name': "AFC",
            'long_name': "American Football Conference",
            'league_name': "NFL",
            'first_season_year': 1970,
            'last_season_year': None,
        }

        # Act
        result = conference_controller.edit(id)

    # Assert
    fake_conference_repository.update_conference.assert_called_once_with(**kwargs)
    fake_flash.assert_called_once_with(str(err), 'danger')
    fake_render_template.assert_called_once_with(
        'conferences/edit.html', conference=conference, form=fake_edit_conference_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.conference_controller.flash')
@patch('app.flask.conference_controller.render_template')
@patch('app.flask.conference_controller.EditConferenceForm')
@patch('app.flask.conference_controller.conference_repository')
def test_edit_when_conference_found_and_form_submitted_and_integrity_error_caught_should_flash_error_message_and_render_edit_template(
        fake_conference_repository, fake_edit_conference_form, fake_render_template, fake_flash, test_app
):
    with test_app.app_context():
        # Arrange
        # Arrange
        conference = Conference(
            short_name="NFC",
            long_name="National Football Conference",
            league_name="NFL",
            first_season_year=1970,
            last_season_year=None
        )
        fake_conference_repository.get_conference.return_value = conference

        fake_edit_conference_form.return_value.validate_on_submit.return_value = True
        fake_edit_conference_form.return_value.short_name.data = "AFC"
        fake_edit_conference_form.return_value.long_name.data = "American Football Conference"
        fake_edit_conference_form.return_value.league_name.data = "NFL"
        fake_edit_conference_form.return_value.first_season_year.data = 1970
        fake_edit_conference_form.return_value.last_season_year.data = None

        err = IntegrityError('statement', 'params', Exception())
        fake_conference_repository.update_conference.side_effect = err

        id = 1
        kwargs = {
            'id': id,
            'short_name': "AFC",
            'long_name': "American Football Conference",
            'league_name': "NFL",
            'first_season_year': 1970,
            'last_season_year': None,
        }

        # Act
        result = conference_controller.edit(id)

    # Assert
    fake_conference_repository.update_conference.assert_called_once_with(**kwargs)
    fake_flash.assert_called_once_with(str(err), 'danger')
    fake_render_template.assert_called_once_with(
        'conferences/edit.html', conference=conference, form=fake_edit_conference_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.conference_controller.render_template')
@patch('app.flask.conference_controller.conference_repository')
def test_delete_when_request_method_is_get_should_render_delete_template(
        fake_conference_repository, fake_render_template, test_app
):
    # Arrange
    conference = Conference()
    fake_conference_repository.get_conference.return_value = conference

    # Act
    with test_app.test_request_context(
            '/conferences/delete?id=1',
            method='GET'
    ):
        with test_app.app_context():
            result = conference_controller.delete(1)

    # Assert
    fake_conference_repository.get_conference.assert_called_once_with(1)
    fake_render_template.assert_called_once_with('conferences/delete.html', conference=conference)
    assert result is fake_render_template.return_value


@patch('app.flask.conference_controller.redirect')
@patch('app.flask.conference_controller.url_for')
@patch('app.flask.conference_controller.flash')
@patch('app.flask.conference_controller.conference_repository')
def test_delete_when_request_method_is_post_and_conference_found_should_flash_success_message_and_redirect_to_conferences_index(
        fake_conference_repository, fake_flash, fake_url_for, fake_redirect, test_app
):
    # Arrange
    conference = Conference()
    fake_conference_repository.get_conference.return_value = conference

    # Act
    id = 1
    with test_app.test_request_context(
            '/conferences/delete?id=1',
            method='POST'
    ):
        with test_app.app_context():
            result = conference_controller.delete(id)

    # Assert
    fake_conference_repository.delete_conference.assert_called_once_with(id)
    fake_flash.assert_called_once_with(f"Conference {conference.short_name} has been successfully deleted.", 'success')
    fake_url_for.assert_called_once_with('conference.index')
    fake_redirect.assert_called_once_with(fake_url_for.return_value)
    assert result is fake_redirect.return_value


@patch('app.flask.conference_controller.conference_repository')
def test_delete_when_request_method_is_post_and_conference_not_found_should_abort_with_404_error(
        fake_conference_repository, test_app
):
    # Arrange
    conference = Conference()
    fake_conference_repository.get_conference.return_value = conference
    fake_conference_repository.delete_conference.side_effect = IndexError()

    # Act
    with test_app.test_request_context(
            '/conferences/delete?id=1',
            method='POST'
    ):
        with test_app.app_context():
            with pytest.raises(NotFound):
                result = conference_controller.delete(1)
