from unittest.mock import patch

import pytest

from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound

import app.flask.conference_controller as mod

from app.data.models.conference import Conference
from test_app import create_app


@pytest.fixture()
def test_app():
    return create_app()


@patch('app.flask.conference_controller.render_template')
@patch('app.flask.conference_controller.conference_repository')
def test_index_should_render_conference_index_template(fake_conference_repository, fake_render_template):
    # Act
    result = mod.index()

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
        fake_render_template, fake_delete_conference_form, fake_conference_repository
):
    # Arrange
    id = 1

    # Act
    result = mod.details(id)

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
        fake_delete_conference_form, fake_conference_repository
):
    # Arrange
    fake_conference_repository.get_conference.side_effect = IndexError()

    # Act
    with pytest.raises(NotFound):
        result = mod.details(1)


@patch('app.flask.conference_controller.render_template')
@patch('app.flask.conference_controller.flash')
@patch('app.flask.conference_controller.NewConferenceForm')
def test_create_when_form_not_submitted_and_no_form_errors_should_render_create_template(
        fake_new_conference_form, fake_flash, fake_render_template
):
    # Arrange
    fake_new_conference_form.return_value.validate_on_submit.return_value = False
    fake_new_conference_form.return_value.errors = None

    # Act
    result = mod.create()

    # Assert
    fake_flash.assert_not_called()
    fake_render_template('conferences/create.html', form=fake_new_conference_form.return_value)
    assert result is fake_render_template.return_value


@patch('app.flask.conference_controller.render_template')
@patch('app.flask.conference_controller.flash')
@patch('app.flask.conference_controller.NewConferenceForm')
def test_create_when_form_not_submitted_and_form_errors_should_flash_errors_and_render_create_template(
        fake_new_conference_form, fake_flash, fake_render_template
):
    # Arrange
    fake_new_conference_form.return_value.validate_on_submit.return_value = False

    errors = 'errors'
    fake_new_conference_form.return_value.errors = errors

    # Act
    result = mod.create()

    # Assert
    fake_flash.assert_called_once_with(f"{errors}", 'danger')
    fake_render_template('conferences/create.html', form=fake_new_conference_form.return_value)
    assert result is fake_render_template.return_value


@patch('app.flask.conference_controller.redirect')
@patch('app.flask.conference_controller.url_for')
@patch('app.flask.conference_controller.flash')
@patch('app.flask.conference_controller.conference_repository')
@patch('app.flask.conference_controller.conference_factory')
@patch('app.flask.conference_controller.NewConferenceForm')
def test_create_when_form_submitted_and_no_errors_caught_should_flash_success_message_and_redirect_to_conference_index(
        fake_new_conference_form, fake_conference_factory, fake_conference_repository, fake_flash, fake_url_for,
        fake_redirect
):
    # Arrange
    fake_new_conference_form.return_value.validate_on_submit.return_value = True
    fake_new_conference_form.return_value.short_name.data = "C"
    fake_new_conference_form.return_value.long_name.data = "Conference"
    fake_new_conference_form.return_value.league_name.data = "L"
    fake_new_conference_form.return_value.first_season_year.data = 1
    fake_new_conference_form.return_value.last_season_year.data = 2

    kwargs = {
        'short_name': "C",
        'long_name': "Conference",
        'league_name': "L",
        'first_season_year': 1,
        'last_season_year': 2,
    }
    conference = Conference(**kwargs)
    fake_conference_factory.create_conference.return_value = conference

    # Act
    result = mod.create()

    # Assert
    fake_conference_factory.create_conference.assert_called_once_with(**kwargs)
    fake_conference_repository.add_conference.assert_called_once_with(conference)
    fake_flash(f"Item {conference.short_name} has been successfully submitted.", 'success')
    fake_url_for.assert_called_once_with('conference.index')
    fake_redirect.assert_called_once_with(fake_url_for.return_value)
    assert result is fake_redirect.return_value


@patch('app.flask.conference_controller.render_template')
@patch('app.flask.conference_controller.flash')
@patch('app.flask.conference_controller.conference_repository')
@patch('app.flask.conference_controller.conference_factory')
@patch('app.flask.conference_controller.NewConferenceForm')
def test_create_when_form_submitted_and_value_error_caught_should_flash_error_message_and_render_create_template(
        fake_new_conference_form, fake_conference_factory, fake_conference_repository, fake_flash, fake_render_template
):
    # Arrange
    fake_new_conference_form.return_value.validate_on_submit.return_value = True
    fake_new_conference_form.return_value.short_name.data = "C"
    fake_new_conference_form.return_value.long_name.data = "Conference"
    fake_new_conference_form.return_value.league_name.data = "L"
    fake_new_conference_form.return_value.first_season_year.data = 1
    fake_new_conference_form.return_value.last_season_year.data = 2

    kwargs = {
        'short_name': "C",
        'long_name': "Conference",
        'league_name': "L",
        'first_season_year': 1,
        'last_season_year': 2,
    }
    conference = Conference(**kwargs)
    fake_conference_factory.create_conference.return_value = conference

    err = ValueError()
    fake_conference_repository.add_conference.side_effect = err

    # Act
    result = mod.create()

    # Assert
    fake_conference_factory.create_conference.assert_called_once_with(**kwargs)
    fake_conference_repository.add_conference.assert_called_once_with(conference)
    fake_flash.assert_called_once_with(str(err), 'danger')
    fake_render_template.assert_called_once_with(
        'conferences/create.html', conference=None, form=fake_new_conference_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.conference_controller.render_template')
@patch('app.flask.conference_controller.flash')
@patch('app.flask.conference_controller.conference_repository')
@patch('app.flask.conference_controller.conference_factory')
@patch('app.flask.conference_controller.NewConferenceForm')
def test_create_when_form_submitted_and_integrity_error_caught_should_flash_error_message_and_render_create_template(
        fake_new_conference_form, fake_conference_factory, fake_conference_repository, fake_flash, fake_render_template
):
    # Arrange
    fake_new_conference_form.return_value.validate_on_submit.return_value = True
    fake_new_conference_form.return_value.short_name.data = "C"
    fake_new_conference_form.return_value.long_name.data = "Conference"
    fake_new_conference_form.return_value.league_name.data = "L"
    fake_new_conference_form.return_value.first_season_year.data = 1
    fake_new_conference_form.return_value.last_season_year.data = 2

    kwargs = {
        'short_name': "C",
        'long_name': "Conference",
        'league_name': "L",
        'first_season_year': 1,
        'last_season_year': 2,
    }
    conference = Conference(**kwargs)
    fake_conference_factory.create_conference.return_value = conference

    err = IntegrityError('statement', 'params', Exception())
    fake_conference_repository.add_conference.side_effect = err

    # Act
    result = mod.create()

    # Assert
    fake_conference_factory.create_conference.assert_called_once_with(**kwargs)
    fake_conference_repository.add_conference.assert_called_once_with(conference)
    fake_flash.assert_called_once_with(str(err), 'danger')
    fake_render_template.assert_called_once_with(
        'conferences/create.html', conference=None, form=fake_new_conference_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.conference_controller.conference_repository')
def test_edit_when_conference_not_found_should_abort_with_404_error(fake_conference_repository):
    # Arrange
    old_conference = None
    fake_conference_repository.get_conference.return_value = old_conference

    # Act
    with pytest.raises(NotFound):
        result = mod.edit(1)


@patch('app.flask.conference_controller.render_template')
@patch('app.flask.conference_controller.flash')
@patch('app.flask.conference_controller.EditConferenceForm')
@patch('app.flask.conference_controller.conference_repository')
def test_edit_when_conference_found_and_form_not_submitted_and_no_form_errors_should_render_edit_template(
        fake_conference_repository, fake_edit_conference_form, fake_flash, fake_render_template
):
    # Arrange
    old_conference = Conference(
        short_name="C",
        long_name="Conference",
        league_name="L",
        first_season_year=1,
        last_season_year=2
    )
    fake_conference_repository.get_conference.return_value = old_conference

    fake_edit_conference_form.return_value.validate_on_submit.return_value = False
    fake_edit_conference_form.return_value.errors = None

    # Act
    result = mod.edit(1)

    # Assert
    assert fake_edit_conference_form.return_value.short_name.data == old_conference.short_name
    assert fake_edit_conference_form.return_value.long_name.data == old_conference.long_name
    assert fake_edit_conference_form.return_value.league_name.data == old_conference.league_name
    assert fake_edit_conference_form.return_value.first_season_year.data == old_conference.first_season_year
    assert fake_edit_conference_form.return_value.last_season_year.data == old_conference.last_season_year
    fake_flash.assert_not_called()
    fake_render_template.assert_called_once_with(
        'conferences/edit.html', conference=old_conference, form=fake_edit_conference_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.conference_controller.render_template')
@patch('app.flask.conference_controller.flash')
@patch('app.flask.conference_controller.EditConferenceForm')
@patch('app.flask.conference_controller.conference_repository')
def test_edit_when_conference_found_and_form_not_submitted_and_form_errors_should_flash_errors_and_render_edit_template(
        fake_conference_repository, fake_edit_conference_form, fake_flash, fake_render_template
):
    # Arrange
    old_conference = Conference(
        short_name="C",
        long_name="Conference",
        league_name="L",
        first_season_year=1,
        last_season_year=2
    )
    fake_conference_repository.get_conference.return_value = old_conference

    fake_edit_conference_form.return_value.validate_on_submit.return_value = False
    fake_edit_conference_form.return_value.errors = None

    errors = 'errors'
    fake_edit_conference_form.return_value.errors = errors

    # Act
    result = mod.edit(1)

    # Assert
    assert fake_edit_conference_form.return_value.short_name.data == old_conference.short_name
    assert fake_edit_conference_form.return_value.long_name.data == old_conference.long_name
    assert fake_edit_conference_form.return_value.league_name.data == old_conference.league_name
    assert fake_edit_conference_form.return_value.first_season_year.data == old_conference.first_season_year
    assert fake_edit_conference_form.return_value.last_season_year.data == old_conference.last_season_year
    fake_flash.assert_called_once_with(f"{errors}", 'danger')
    fake_render_template.assert_called_once_with(
        'conferences/edit.html', conference=old_conference, form=fake_edit_conference_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.conference_controller.redirect')
@patch('app.flask.conference_controller.url_for')
@patch('app.flask.conference_controller.flash')
@patch('app.flask.conference_controller.conference_factory')
@patch('app.flask.conference_controller.EditConferenceForm')
@patch('app.flask.conference_controller.conference_repository')
def test_edit_when_conference_found_and_form_submitted_and_no_errors_caught_should_flash_success_message_and_redirect_to_conference_details(
        fake_conference_repository, fake_edit_conference_form, fake_conference_factory, fake_flash, fake_url_for,
        fake_redirect
):
    # Arrange
    id = 1

    old_conference = Conference(
        id=id,
        short_name="C1",
        long_name="Conference 1",
        league_name="L",
        first_season_year=1,
        last_season_year=2
    )
    fake_conference_repository.get_conference.return_value = old_conference

    fake_edit_conference_form.return_value.validate_on_submit.return_value = True
    fake_edit_conference_form.return_value.short_name.data = "C2"
    fake_edit_conference_form.return_value.long_name.data = "Conference 2"
    fake_edit_conference_form.return_value.league_name.data = "L"
    fake_edit_conference_form.return_value.first_season_year.data = 3
    fake_edit_conference_form.return_value.last_season_year.data = 4

    kwargs = {
        'id': id,
        'short_name': "C2",
        'long_name': "Conference 2",
        'league_name': "L",
        'first_season_year': 3,
        'last_season_year': 4,
    }
    new_conference = Conference(**kwargs)
    fake_conference_factory.create_conference.return_value = new_conference

    # Act
    result = mod.edit(id)

    # Assert
    fake_conference_factory.create_conference.assert_called_once_with(**kwargs)
    fake_conference_repository.update_conference.assert_called_once_with(new_conference)
    fake_flash.assert_called_once_with(
        f"Item {fake_edit_conference_form.return_value.short_name.data} has been successfully updated.", 'success'
    )
    fake_url_for.assert_called_once_with('conference.details', id=id)
    fake_redirect.assert_called_once_with(fake_url_for.return_value)
    assert result is fake_redirect.return_value


@patch('app.flask.conference_controller.render_template')
@patch('app.flask.conference_controller.flash')
@patch('app.flask.conference_controller.conference_factory')
@patch('app.flask.conference_controller.EditConferenceForm')
@patch('app.flask.conference_controller.conference_repository')
def test_edit_when_conference_found_and_form_submitted_and_value_error_caught_should_flash_error_message_and_render_edit_template(
        fake_conference_repository, fake_edit_conference_form, fake_conference_factory, fake_flash,
        fake_render_template
):
    # Arrange
    id = 1

    old_conference = Conference(
        id=id,
        short_name="C1",
        long_name="Conference 1",
        league_name="L",
        first_season_year=1,
        last_season_year=2
    )
    fake_conference_repository.get_conference.return_value = old_conference

    fake_edit_conference_form.return_value.validate_on_submit.return_value = True
    fake_edit_conference_form.return_value.short_name.data = "C2"
    fake_edit_conference_form.return_value.long_name.data = "Conference 2"
    fake_edit_conference_form.return_value.league_name.data = "L"
    fake_edit_conference_form.return_value.first_season_year.data = 3
    fake_edit_conference_form.return_value.last_season_year.data = 4

    kwargs = {
        'id': id,
        'short_name': "C2",
        'long_name': "Conference 2",
        'league_name': "L",
        'first_season_year': 3,
        'last_season_year': 4,
    }
    new_conference = Conference(**kwargs)
    fake_conference_factory.create_conference.return_value = new_conference

    err = ValueError()
    fake_conference_repository.update_conference.side_effect = err

    # Act
    result = mod.edit(id)

    # Assert
    fake_conference_factory.create_conference.assert_called_once_with(**kwargs)
    fake_conference_repository.update_conference.assert_called_once_with(new_conference)
    fake_flash.assert_called_once_with(str(err), 'danger')
    fake_render_template.assert_called_once_with(
        'conferences/edit.html', conference=old_conference, form=fake_edit_conference_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.conference_controller.render_template')
@patch('app.flask.conference_controller.flash')
@patch('app.flask.conference_controller.conference_factory')
@patch('app.flask.conference_controller.EditConferenceForm')
@patch('app.flask.conference_controller.conference_repository')
def test_edit_when_conference_found_and_form_submitted_and_integrity_error_caught_should_flash_error_message_and_render_edit_template(
        fake_conference_repository, fake_edit_conference_form, fake_conference_factory, fake_flash,
        fake_render_template
):
    # Arrange
    id = 1

    old_conference = Conference(
        id=id,
        short_name="C1",
        long_name="Conference 1",
        league_name="L",
        first_season_year=1,
        last_season_year=2
    )
    fake_conference_repository.get_conference.return_value = old_conference

    fake_edit_conference_form.return_value.validate_on_submit.return_value = True
    fake_edit_conference_form.return_value.short_name.data = "C2"
    fake_edit_conference_form.return_value.long_name.data = "Conference 2"
    fake_edit_conference_form.return_value.league_name.data = "L"
    fake_edit_conference_form.return_value.first_season_year.data = 3
    fake_edit_conference_form.return_value.last_season_year.data = 4

    kwargs = {
        'id': id,
        'short_name': "C2",
        'long_name': "Conference 2",
        'league_name': "L",
        'first_season_year': 3,
        'last_season_year': 4,
    }
    new_conference = Conference(**kwargs)
    fake_conference_factory.create_conference.return_value = new_conference

    err = IntegrityError('statement', 'params', Exception())
    fake_conference_repository.update_conference.side_effect = err

    # Act
    result = mod.edit(id)

    # Assert
    fake_conference_factory.create_conference.assert_called_once_with(**kwargs)
    fake_conference_repository.update_conference.assert_called_once_with(new_conference)
    fake_flash.assert_called_once_with(str(err), 'danger')
    fake_render_template.assert_called_once_with(
        'conferences/edit.html', conference=old_conference, form=fake_edit_conference_form.return_value
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
            result = mod.delete(1)

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
            result = mod.delete(id)

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
                result = mod.delete(1)
