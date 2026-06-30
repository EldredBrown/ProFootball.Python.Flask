from unittest.mock import patch, MagicMock

import pytest

from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound

import app.flask.conference_controller as mod

from app.data.models.conference import Conference
from app.data.models.league import League
from app.data.repositories.conference_repository import ConferenceRepository
from test_app import create_app


@pytest.fixture()
def test_app():
    return create_app()


@patch('app.flask.conference_controller.render_template')
@patch('app.flask.conference_controller.injector')
def test_index_should_render_conference_index_template(
        fake_injector, fake_render_template
):
    # Arrange
    fake_conference_repository = MagicMock(ConferenceRepository)
    fake_injector.get.return_value = fake_conference_repository

    # Act
    result = mod.index()

    # Assert
    fake_injector.get.assert_called_once_with(ConferenceRepository)
    fake_conference_repository.get_conferences.assert_called_once()
    fake_render_template.assert_called_once_with(
        'conferences/index.html', conferences=fake_conference_repository.get_conferences.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.conference_controller.render_template')
@patch('app.flask.conference_controller.injector')
@patch('app.flask.conference_controller.DeleteConferenceForm')
def test_details_when_conference_found_should_render_conference_details_template(
        fake_form, fake_injector, fake_render_template
):
    # Arrange
    fake_conference_repository = MagicMock(ConferenceRepository)
    fake_injector.get.return_value = fake_conference_repository

    id = 1

    # Act
    result = mod.details(id)

    # Assert
    fake_form.assert_called_once()
    fake_injector.get.assert_called_once_with(ConferenceRepository)
    fake_conference_repository.get_conference.assert_called_once_with(id)
    fake_render_template.assert_called_once_with(
        'conferences/details.html',
        conference=fake_conference_repository.get_conference.return_value,
        form=fake_form.return_value
    )
    assert result == fake_render_template.return_value


@patch('app.flask.conference_controller.injector')
@patch('app.flask.conference_controller.DeleteConferenceForm')
def test_details_when_conference_not_found_should_abort_with_404_error(fake_form, fake_injector):
    # Arrange
    fake_conference_repository = MagicMock(ConferenceRepository)
    fake_conference_repository.get_conference.side_effect = IndexError()
    fake_injector.get.return_value = fake_conference_repository

    # Act
    with pytest.raises(NotFound):
        result = mod.details(1)


@patch('app.flask.conference_controller.render_template')
@patch('app.flask.conference_controller.flash')
@patch('app.flask.conference_controller.injector')
@patch('app.flask.conference_controller.NewConferenceForm')
def test_create_when_form_not_submitted_and_no_form_errors_should_render_create_template(
        fake_form, fake_injector, fake_flash,
        fake_render_template
):
    # Arrange
    fake_form.return_value.validate_on_submit.return_value = False
    fake_form.return_value.errors = None

    fake_conference_repository = MagicMock(ConferenceRepository)
    fake_injector.get.return_value = fake_conference_repository

    # Act
    result = mod.create()

    # Assert
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    fake_injector.get.assert_not_called()
    fake_conference_repository.add_conference.assert_not_called()
    fake_flash.assert_not_called()
    fake_render_template('conferences/create.html', form=fake_form.return_value)
    assert result is fake_render_template.return_value


@patch('app.flask.conference_controller.render_template')
@patch('app.flask.conference_controller.flash')
@patch('app.flask.conference_controller.injector')
@patch('app.flask.conference_controller.NewConferenceForm')
def test_create_when_form_not_submitted_and_form_errors_should_flash_errors_and_render_create_template(
        fake_form, fake_injector, fake_flash,
        fake_render_template
):
    # Arrange
    fake_form.return_value.validate_on_submit.return_value = False

    errors = 'errors'
    fake_form.return_value.errors = errors

    fake_conference_repository = MagicMock(ConferenceRepository)
    fake_injector.get.return_value = fake_conference_repository

    # Act
    result = mod.create()

    # Assert
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    fake_injector.get.assert_not_called()
    fake_conference_repository.add_conference.assert_not_called()
    fake_flash.assert_called_once_with(f"{errors}", 'danger')
    fake_render_template('conferences/create.html', form=fake_form.return_value)
    assert result is fake_render_template.return_value


@patch('app.flask.conference_controller.redirect')
@patch('app.flask.conference_controller.url_for')
@patch('app.flask.conference_controller.flash')
@patch('app.flask.conference_controller.injector')
@patch('app.flask.conference_controller.conference_factory')
@patch('app.flask.conference_controller.NewConferenceForm')
def test_create_when_form_submitted_and_no_errors_caught_should_flash_success_message_and_redirect_to_conference_index(
        fake_form, fake_conference_factory, fake_injector,
        fake_flash, fake_url_for, fake_redirect
):
    # Arrange
    league_id = 1

    league = League(id=league_id, short_name="L", long_name="League", first_season_id=1920)

    model_kwargs = {
        'short_name': "C",
        'long_name': "Conference",
        'league_id': league_id,
        'first_season_id': 1920,
        'last_season_id': 1921,
    }
    conference = Conference(**model_kwargs)
    conference.league = league

    fake_form.return_value.validate_on_submit.return_value = True
    fake_form.return_value.short_name.data = conference.short_name
    fake_form.return_value.long_name.data = conference.long_name
    fake_form.return_value.league_name.data = conference.league.short_name
    fake_form.return_value.first_season_year.data = conference.first_season_id
    fake_form.return_value.last_season_year.data = conference.last_season_id

    fake_conference_factory.create_conference.return_value = conference

    fake_conference_repository = MagicMock(ConferenceRepository)
    fake_injector.get.return_value = fake_conference_repository

    # Act
    result = mod.create()

    # Assert
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    view_kwargs = {
        'short_name': conference.short_name,
        'long_name': conference.long_name,
        'league_name': conference.league.short_name,
        'first_season_year': conference.first_season_id,
        'last_season_year': conference.last_season_id,
    }
    fake_conference_factory.create_conference.assert_called_once_with(**view_kwargs)
    fake_injector.get.assert_called_once_with(ConferenceRepository)
    fake_conference_repository.add_conference.assert_called_once_with(conference)
    fake_flash(f"Item {conference.short_name} has been successfully submitted.", 'success')
    fake_url_for.assert_called_once_with('conference.index')
    fake_redirect.assert_called_once_with(fake_url_for.return_value)
    assert result is fake_redirect.return_value


@patch('app.flask.conference_controller.render_template')
@patch('app.flask.conference_controller.flash')
@patch('app.flask.conference_controller.injector')
@patch('app.flask.conference_controller.conference_factory')
@patch('app.flask.conference_controller.NewConferenceForm')
def test_create_when_form_submitted_and_value_error_caught_should_flash_error_message_and_render_create_template(
        fake_form, fake_conference_factory, fake_injector,
        fake_flash, fake_render_template
):
    # Arrange
    league_id = 1

    league = League(id=league_id, short_name="L", long_name="League", first_season_id=1920)

    model_kwargs = {
        'short_name': "C",
        'long_name': "Conference",
        'league_id': league_id,
        'first_season_id': 1920,
        'last_season_id': 1921,
    }
    conference = Conference(**model_kwargs)
    conference.league = league

    fake_form.return_value.validate_on_submit.return_value = True
    fake_form.return_value.short_name.data = conference.short_name
    fake_form.return_value.long_name.data = conference.long_name
    fake_form.return_value.league_name.data = conference.league.short_name
    fake_form.return_value.first_season_year.data = conference.first_season_id
    fake_form.return_value.last_season_year.data = conference.last_season_id

    fake_conference_factory.create_conference.return_value = conference

    fake_conference_repository = MagicMock(ConferenceRepository)
    err = ValueError()
    fake_conference_repository.add_conference.side_effect = err
    fake_injector.get.return_value = fake_conference_repository

    # Act
    result = mod.create()

    # Assert
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    view_kwargs = {
        'short_name': conference.short_name,
        'long_name': conference.long_name,
        'league_name': conference.league.short_name,
        'first_season_year': conference.first_season_id,
        'last_season_year': conference.last_season_id,
    }
    fake_conference_factory.create_conference.assert_called_once_with(**view_kwargs)
    fake_injector.get.assert_called_once_with(ConferenceRepository)
    fake_conference_repository.add_conference.assert_called_once_with(conference)
    fake_flash.assert_called_once_with(str(err), 'danger')
    fake_render_template.assert_called_once_with(
        'conferences/create.html', conference=None, form=fake_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.conference_controller.render_template')
@patch('app.flask.conference_controller.flash')
@patch('app.flask.conference_controller.injector')
@patch('app.flask.conference_controller.conference_factory')
@patch('app.flask.conference_controller.NewConferenceForm')
def test_create_when_form_submitted_and_integrity_error_caught_should_flash_error_message_and_render_create_template(
        fake_form, fake_conference_factory, fake_injector,
        fake_flash, fake_render_template
):
    # Arrange
    league_id = 1

    league = League(id=league_id, short_name="L", long_name="League", first_season_id=1920)

    model_kwargs = {
        'short_name': "C",
        'long_name': "Conference",
        'league_id': league_id,
        'first_season_id': 1920,
        'last_season_id': 1921,
    }
    conference = Conference(**model_kwargs)
    conference.league = league

    fake_form.return_value.validate_on_submit.return_value = True
    fake_form.return_value.short_name.data = conference.short_name
    fake_form.return_value.long_name.data = conference.long_name
    fake_form.return_value.league_name.data = conference.league.short_name
    fake_form.return_value.first_season_year.data = conference.first_season_id
    fake_form.return_value.last_season_year.data = conference.last_season_id

    fake_conference_factory.create_conference.return_value = conference

    fake_conference_repository = MagicMock(ConferenceRepository)
    err = IntegrityError('statement', 'params', Exception())
    fake_conference_repository.add_conference.side_effect = err
    fake_injector.get.return_value = fake_conference_repository

    # Act
    result = mod.create()

    # Assert
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    view_kwargs = {
        'short_name': conference.short_name,
        'long_name': conference.long_name,
        'league_name': conference.league.short_name,
        'first_season_year': conference.first_season_id,
        'last_season_year': conference.last_season_id,
    }
    fake_conference_factory.create_conference.assert_called_once_with(**view_kwargs)
    fake_injector.get.assert_called_once_with(ConferenceRepository)
    fake_conference_repository.add_conference.assert_called_once_with(conference)
    fake_flash.assert_called_once_with(str(err), 'danger')
    fake_render_template.assert_called_once_with(
        'conferences/create.html', conference=None, form=fake_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.conference_controller.copy')
@patch('app.flask.conference_controller.injector')
def test_edit_when_conference_not_found_should_abort_with_404_error(fake_injector, fake_copy):
    # Arrange
    fake_conference_repository = MagicMock(ConferenceRepository)
    old_conference = MagicMock(Conference)
    fake_conference_repository.get_conference.return_value = old_conference
    fake_injector.get.return_value = fake_conference_repository

    old_conference_copy = None
    fake_copy.deepcopy.return_value = old_conference_copy

    id = 1

    # Act
    with pytest.raises(NotFound):
        result = mod.edit(id)

    # Assert
    fake_injector.get.assert_called_once_with(ConferenceRepository)
    fake_conference_repository.get_conference.assert_called_once_with(id)
    fake_copy.deepcopy.assert_called_once_with(old_conference)


@patch('app.flask.conference_controller.render_template')
@patch('app.flask.conference_controller.flash')
@patch('app.flask.conference_controller.EditConferenceForm')
@patch('app.flask.conference_controller.copy')
@patch('app.flask.conference_controller.injector')
def test_edit_when_conference_found_and_form_not_submitted_and_no_form_errors_should_render_edit_template(
        fake_injector, fake_copy, fake_form, fake_flash,
        fake_render_template
):
    # Arrange
    fake_conference_repository = MagicMock(ConferenceRepository)
    old_conference = MagicMock(Conference)
    fake_conference_repository.get_conference.return_value = old_conference
    fake_injector.get.return_value = fake_conference_repository

    old_conference_copy = MagicMock(Conference)
    old_conference_copy.short_name = "L"
    old_conference_copy.long_name = "Conference"
    old_conference_copy.league_id = 1
    old_conference_copy.first_season_id = 1920
    old_conference_copy.last_season_id = 1921
    fake_copy.deepcopy.return_value = old_conference_copy

    fake_form.return_value.validate_on_submit.return_value = False
    fake_form.return_value.errors = None

    id = 1

    # Act
    result = mod.edit(id)

    # Assert
    fake_injector.get.assert_called_once_with(ConferenceRepository)
    fake_conference_repository.get_conference.assert_called_once_with(id)
    fake_copy.deepcopy.assert_called_once_with(old_conference)
    fake_form.assert_called_once()
    assert fake_form.return_value.short_name.data == old_conference_copy.short_name
    assert fake_form.return_value.long_name.data == old_conference_copy.long_name
    assert fake_form.return_value.league_name.data == old_conference_copy.league.short_name
    assert fake_form.return_value.first_season_year.data == old_conference_copy.first_season_id
    assert fake_form.return_value.last_season_year.data == old_conference_copy.last_season_id
    fake_form.return_value.validate_on_submit.assert_called_once()
    fake_flash.assert_not_called()
    fake_render_template.assert_called_once_with(
        'conferences/edit.html', conference=old_conference_copy, form=fake_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.conference_controller.render_template')
@patch('app.flask.conference_controller.flash')
@patch('app.flask.conference_controller.EditConferenceForm')
@patch('app.flask.conference_controller.copy')
@patch('app.flask.conference_controller.injector')
def test_edit_when_conference_found_and_form_not_submitted_and_form_errors_should_flash_errors_and_render_edit_template(
        fake_injector, fake_copy, fake_form,
        fake_flash, fake_render_template
):
    # Arrange
    fake_conference_repository = MagicMock(ConferenceRepository)
    old_conference = MagicMock(Conference)
    fake_conference_repository.get_conference.return_value = old_conference
    fake_injector.get.return_value = fake_conference_repository

    fake_form.return_value.validate_on_submit.return_value = False
    fake_form.return_value.errors = None

    old_conference_copy = MagicMock(Conference)
    old_conference_copy.short_name = "C"
    old_conference_copy.long_name = "Conference"
    old_conference_copy.first_season_id = 1920
    old_conference_copy.last_season_id = 1921
    fake_copy.deepcopy.return_value = old_conference_copy

    errors = 'errors'
    fake_form.return_value.errors = errors

    id = 1

    # Act
    result = mod.edit(id)

    # Assert
    fake_injector.get.assert_called_once_with(ConferenceRepository)
    fake_conference_repository.get_conference.assert_called_once_with(id)
    fake_copy.deepcopy.assert_called_once_with(old_conference)
    fake_form.assert_called_once()
    assert fake_form.return_value.short_name.data == old_conference_copy.short_name
    assert fake_form.return_value.long_name.data == old_conference_copy.long_name
    assert fake_form.return_value.first_season_year.data == old_conference_copy.first_season_id
    assert fake_form.return_value.last_season_year.data == old_conference_copy.last_season_id
    fake_form.return_value.validate_on_submit.assert_called_once()
    fake_flash.assert_called_once_with(f"{errors}", 'danger')
    fake_render_template.assert_called_once_with(
        'conferences/edit.html', conference=old_conference_copy, form=fake_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.conference_controller.redirect')
@patch('app.flask.conference_controller.url_for')
@patch('app.flask.conference_controller.flash')
@patch('app.flask.conference_controller.conference_factory')
@patch('app.flask.conference_controller.EditConferenceForm')
@patch('app.flask.conference_controller.copy')
@patch('app.flask.conference_controller.injector')
def test_edit_when_conference_found_and_form_submitted_and_no_errors_caught_should_flash_success_message_and_redirect_to_conference_details(
        fake_injector, fake_copy, fake_form,
        fake_conference_factory, fake_flash,
        fake_url_for, fake_redirect
):
    # Arrange
    league_id = 1
    league = League(id=league_id, short_name="L", long_name="League", first_season_id=1920)

    id = 1
    model_kwargs = {
        'id': id,
        'short_name': "C",
        'long_name': "Conference",
        'league_id': league_id,
        'first_season_id': 1920,
        'last_season_id': 1921,
    }
    new_conference = Conference(**model_kwargs)
    new_conference.league = league

    fake_conference_repository = MagicMock(ConferenceRepository)
    old_conference = MagicMock(Conference)
    fake_conference_repository.get_conference.return_value = old_conference
    fake_injector.get.return_value = fake_conference_repository

    old_conference_copy = MagicMock(Conference)
    old_conference_copy.short_name = "C1"
    old_conference_copy.long_name = "Conference 1"
    old_conference_copy.league_id = league_id,
    old_conference_copy.first_season_id = 1920
    old_conference_copy.last_season_id = 1921
    fake_copy.deepcopy.return_value = old_conference_copy

    fake_form.return_value.validate_on_submit.return_value = True
    fake_form.return_value.short_name.data = new_conference.short_name
    fake_form.return_value.long_name.data = new_conference.long_name
    fake_form.return_value.league_name.data = new_conference.league.short_name
    fake_form.return_value.first_season_year.data = new_conference.first_season_id
    fake_form.return_value.last_season_year.data = new_conference.last_season_id

    fake_conference_factory.create_conference.return_value = new_conference

    # Act
    result = mod.edit(id)

    # Assert
    fake_injector.get.assert_called_once_with(ConferenceRepository)
    fake_conference_repository.get_conference.assert_called_once_with(id)
    fake_copy.deepcopy.assert_called_once_with(old_conference)
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    view_kwargs = {
        'id': id,
        'short_name': new_conference.short_name,
        'long_name': new_conference.long_name,
        'league_name': new_conference.league.short_name,
        'first_season_year': new_conference.first_season_id,
        'last_season_year': new_conference.last_season_id,
    }
    fake_conference_factory.create_conference.assert_called_once_with(**view_kwargs)
    fake_conference_repository.update_conference.assert_called_once_with(new_conference)
    fake_flash.assert_called_once_with(
        f"Item {fake_form.return_value.short_name.data} has been successfully updated.", 'success'
    )
    fake_url_for.assert_called_once_with('conference.details', id=id)
    fake_redirect.assert_called_once_with(fake_url_for.return_value)
    assert result is fake_redirect.return_value


@patch('app.flask.conference_controller.render_template')
@patch('app.flask.conference_controller.flash')
@patch('app.flask.conference_controller.conference_factory')
@patch('app.flask.conference_controller.EditConferenceForm')
@patch('app.flask.conference_controller.copy')
@patch('app.flask.conference_controller.injector')
def test_edit_when_conference_found_and_form_submitted_and_value_error_caught_should_flash_error_message_and_render_edit_template(
        fake_injector, fake_copy, fake_form,
        fake_conference_factory, fake_flash,
        fake_render_template
):
    # Arrange
    league_id = 1
    league = League(id=league_id, short_name="L", long_name="League", first_season_id=1920)

    id = 1
    model_kwargs = {
        'id': id,
        'short_name': "C",
        'long_name': "Conference",
        'league_id': league_id,
        'first_season_id': 1922,
        'last_season_id': 1923,
    }
    new_conference = Conference(**model_kwargs)
    new_conference.league = league

    fake_conference_repository = MagicMock(ConferenceRepository)
    old_conference = MagicMock(Conference)
    fake_conference_repository.get_conference.return_value = old_conference
    err = ValueError()
    fake_conference_repository.update_conference.side_effect = err
    fake_injector.get.return_value = fake_conference_repository

    old_conference_copy = MagicMock(Conference)
    old_conference_copy.short_name = "L1"
    old_conference_copy.long_name = "Conference 1"
    old_conference_copy.league_id = league_id,
    old_conference_copy.first_season_id = 1920
    old_conference_copy.last_season_id = 1921
    fake_copy.deepcopy.return_value = old_conference_copy

    fake_form.return_value.validate_on_submit.return_value = True
    fake_form.return_value.short_name.data = new_conference.short_name
    fake_form.return_value.long_name.data = new_conference.long_name
    fake_form.return_value.league_name.data = new_conference.league.short_name
    fake_form.return_value.first_season_year.data = new_conference.first_season_id
    fake_form.return_value.last_season_year.data = new_conference.last_season_id

    fake_conference_factory.create_conference.return_value = new_conference

    # Act
    result = mod.edit(id)

    # Assert
    fake_injector.get.assert_called_once_with(ConferenceRepository)
    fake_conference_repository.get_conference.assert_called_once_with(id)
    fake_copy.deepcopy.assert_called_once_with(old_conference)
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    view_kwargs = {
        'id': id,
        'short_name': new_conference.short_name,
        'long_name': new_conference.long_name,
        'league_name': new_conference.league.short_name,
        'first_season_year': new_conference.first_season_id,
        'last_season_year': new_conference.last_season_id,
    }
    fake_conference_factory.create_conference.assert_called_once_with(**view_kwargs)
    fake_flash.assert_called_once_with(str(err), 'danger')
    fake_render_template.assert_called_once_with(
        'conferences/edit.html', conference=old_conference_copy, form=fake_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.conference_controller.render_template')
@patch('app.flask.conference_controller.flash')
@patch('app.flask.conference_controller.conference_factory')
@patch('app.flask.conference_controller.EditConferenceForm')
@patch('app.flask.conference_controller.copy')
@patch('app.flask.conference_controller.injector')
def test_edit_when_conference_found_and_form_submitted_and_integrity_error_caught_should_flash_error_message_and_render_edit_template(
        fake_injector, fake_copy, fake_form,
        fake_conference_factory, fake_flash,
        fake_render_template
):
    # Arrange
    league_id = 1
    league = League(id=league_id, short_name="L", long_name="League", first_season_id=1920)

    id = 1
    model_kwargs = {
        'id': id,
        'short_name': "C",
        'long_name': "Conference",
        'league_id': league_id,
        'first_season_id': 1922,
        'last_season_id': 1923,
    }
    new_conference = Conference(**model_kwargs)
    new_conference.league = league

    fake_conference_repository = MagicMock(ConferenceRepository)
    old_conference = MagicMock(Conference)
    fake_conference_repository.get_conference.return_value = old_conference
    err = IntegrityError('statement', 'params', Exception())
    fake_conference_repository.update_conference.side_effect = err
    fake_injector.get.return_value = fake_conference_repository

    old_conference_copy = MagicMock(Conference)
    old_conference_copy.short_name = "L1"
    old_conference_copy.long_name = "Conference 1"
    old_conference_copy.league_id = league_id,
    old_conference_copy.first_season_id = 1920
    old_conference_copy.last_season_id = 1921
    fake_copy.deepcopy.return_value = old_conference_copy

    fake_form.return_value.validate_on_submit.return_value = True
    fake_form.return_value.short_name.data = new_conference.short_name
    fake_form.return_value.long_name.data = new_conference.long_name
    fake_form.return_value.league_name.data = new_conference.league.short_name
    fake_form.return_value.first_season_year.data = new_conference.first_season_id
    fake_form.return_value.last_season_year.data = new_conference.last_season_id

    fake_conference_factory.create_conference.return_value = new_conference

    # Act
    result = mod.edit(id)

    # Assert
    fake_injector.get.assert_called_once_with(ConferenceRepository)
    fake_conference_repository.get_conference.assert_called_once_with(id)
    fake_copy.deepcopy.assert_called_once_with(old_conference)
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    view_kwargs = {
        'id': id,
        'short_name': new_conference.short_name,
        'long_name': new_conference.long_name,
        'league_name': new_conference.league.short_name,
        'first_season_year': new_conference.first_season_id,
        'last_season_year': new_conference.last_season_id,
    }
    fake_conference_factory.create_conference.assert_called_once_with(**view_kwargs)
    fake_flash.assert_called_once_with(str(err), 'danger')
    fake_render_template.assert_called_once_with(
        'conferences/edit.html', conference=old_conference_copy, form=fake_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.conference_controller.flash')
@patch('app.flask.conference_controller.conference_factory')
@patch('app.flask.conference_controller.EditConferenceForm')
@patch('app.flask.conference_controller.url_for')
@patch('app.flask.conference_controller.redirect')
@patch('app.flask.conference_controller.copy')
@patch('app.flask.conference_controller.injector')
def test_edit_when_conference_found_and_form_submitted_and_index_error_caught_should_abort_with_404_error(
        fake_injector, fake_copy, fake_redirect, fake_url_for,
        fake_form, fake_conference_factory, fake_flash
):
    # Arrange
    league_id = 1
    league = League(id=league_id, short_name="L", long_name="League", first_season_id=1920)

    id = 1
    model_kwargs = {
        'id': id,
        'short_name': "C",
        'long_name': "Conference",
        'league_id': league_id,
        'first_season_id': 1922,
        'last_season_id': 1923,
    }
    new_conference = Conference(**model_kwargs)
    new_conference.league = league

    fake_conference_repository = MagicMock(ConferenceRepository)
    old_conference = MagicMock(Conference)
    fake_conference_repository.get_conference.return_value = old_conference
    fake_injector.get.return_value = fake_conference_repository

    old_conference_copy = MagicMock(Conference)
    old_conference_copy.short_name = "L1"
    old_conference_copy.long_name = "Conference 1"
    old_conference_copy.league_id = league_id,
    old_conference_copy.first_season_id = 1920
    old_conference_copy.last_season_id = 1921
    fake_copy.deepcopy.return_value = old_conference_copy

    fake_form.return_value.validate_on_submit.return_value = True
    fake_form.return_value.short_name.data = new_conference.short_name
    fake_form.return_value.long_name.data = new_conference.long_name
    fake_form.return_value.league_name.data = new_conference.league.short_name
    fake_form.return_value.first_season_year.data = new_conference.first_season_id
    fake_form.return_value.last_season_year.data = new_conference.last_season_id

    err = IndexError()
    fake_url_for.side_effect = err

    # Act
    with pytest.raises(NotFound):
        result = mod.edit(id)

    # Assert
    fake_injector.get.assert_called_once_with(ConferenceRepository)
    fake_conference_repository.get_conference.assert_called_once_with(id)
    fake_copy.deepcopy.assert_called_once_with(old_conference)
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    view_kwargs = {
        'id': id,
        'short_name': new_conference.short_name,
        'long_name': new_conference.long_name,
        'league_name': new_conference.league.short_name,
        'first_season_year': new_conference.first_season_id,
        'last_season_year': new_conference.last_season_id,
    }
    fake_conference_factory.create_conference.assert_called_once_with(**view_kwargs)


@patch('app.flask.conference_controller.injector')
def test_delete_when_conference_not_found_should_abort_with_404_error(fake_injector, test_app):
    # Arrange
    id = 1

    fake_conference_repository = MagicMock(ConferenceRepository)
    fake_conference_repository.get_conference.return_value = None
    fake_injector.get.return_value = fake_conference_repository

    # Act
    with test_app.test_request_context(
            f'/conferences/delete?id={id}',
            method='POST'
    ):
        with pytest.raises(NotFound):
            result = mod.delete(id)

    # Assert
    fake_injector.get.assert_called_once_with(ConferenceRepository)
    fake_conference_repository.get_conference.assert_called_once_with(id)


@patch('app.flask.conference_controller.render_template')
@patch('app.flask.conference_controller.DeleteConferenceForm')
@patch('app.flask.conference_controller.injector')
def test_delete_when_request_method_is_get_should_render_delete_template(
        fake_injector, fake_form, fake_render_template, test_app
):
    # Arrange
    id = 1

    fake_conference_repository = MagicMock(ConferenceRepository)
    conference = Conference()
    fake_conference_repository.get_conference.return_value = conference
    fake_injector.get.return_value = fake_conference_repository

    # Act
    with test_app.test_request_context(
            f'/conferences/delete?id={id}',
            method='GET'
    ):
        result = mod.delete(id)

    # Assert
    fake_form.assert_called_once()
    fake_injector.get.assert_called_once_with(ConferenceRepository)
    fake_conference_repository.get_conference.assert_called_once_with(id)
    fake_render_template.assert_called_once_with(
        'conferences/delete.html', conference=conference, form=fake_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.conference_controller.redirect')
@patch('app.flask.conference_controller.url_for')
@patch('app.flask.conference_controller.flash')
@patch('app.flask.conference_controller.injector')
def test_delete_when_request_method_is_post_and_conference_found_should_flash_success_message_and_redirect_to_conferences_index(
        fake_injector, fake_flash, fake_url_for,
        fake_redirect, test_app
):
    # Arrange
    id = 1

    fake_conference_repository = MagicMock(ConferenceRepository)
    conference = Conference()
    fake_conference_repository.get_conference.return_value = conference
    fake_injector.get.return_value = fake_conference_repository

    # Act
    with test_app.test_request_context(
            '/conferences/delete?id=1',
            method='POST'
    ):
        result = mod.delete(id)

    # Assert
    fake_injector.get.assert_called_once_with(ConferenceRepository)
    fake_conference_repository.get_conference.assert_called_once_with(id)
    fake_conference_repository.delete_conference.assert_called_once_with(id)
    fake_flash.assert_called_once_with(f"Conference {conference.short_name} has been successfully deleted.", 'success')
    fake_url_for.assert_called_once_with('conference.index')
    fake_redirect.assert_called_once_with(fake_url_for.return_value)
    assert result is fake_redirect.return_value


@patch('app.flask.conference_controller.injector')
def test_delete_when_request_method_is_post_and_index_error_is_caught_should_abort_with_404_error(
        fake_injector, test_app
):
    # Arrange
    id = 1

    fake_conference_repository = MagicMock(ConferenceRepository)
    conference = Conference()
    fake_conference_repository.get_conference.return_value = conference
    fake_conference_repository.delete_conference.side_effect = IndexError()
    fake_injector.get.return_value = fake_conference_repository

    # Act
    with test_app.test_request_context(
            f'/conferences/delete?id={id}',
            method='POST'
    ):
        with pytest.raises(NotFound):
            result = mod.delete(id)

    # Assert
    fake_injector.get.assert_called_once_with(ConferenceRepository)
    fake_conference_repository.get_conference.assert_called_once_with(id)
