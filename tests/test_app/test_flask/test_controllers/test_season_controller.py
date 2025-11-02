from unittest.mock import patch

import pytest

from werkzeug.exceptions import NotFound

import app.flask.season_controller as mod

from app.data.models.season import Season
from test_app import create_app


@pytest.fixture()
def test_app():
    return create_app()


@patch('app.flask.season_controller.render_template')
@patch('app.flask.season_controller.season_repository')
def test_index_should_render_season_index_template(fake_season_repository, fake_render_template):
    # Act
    result = mod.index()

    # Assert
    fake_season_repository.get_seasons.assert_called_once()
    fake_render_template.assert_called_once_with(
        'seasons/index.html', seasons=fake_season_repository.get_seasons.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.season_controller.season_repository')
@patch('app.flask.season_controller.DeleteSeasonForm')
@patch('app.flask.season_controller.render_template')
def test_details_when_season_found_should_render_season_details_template(
        fake_render_template, fake_delete_season_form, fake_season_repository
):
    # Arrange
    id = 1

    # Act
    result = mod.details(id)

    # Assert
    fake_delete_season_form.assert_called_once()
    fake_season_repository.get_season.assert_called_once_with(id)
    fake_render_template.assert_called_once_with(
        'seasons/details.html',
        season=fake_season_repository.get_season.return_value,
        form=fake_delete_season_form.return_value
    )
    assert result == fake_render_template.return_value


@patch('app.flask.season_controller.season_repository')
@patch('app.flask.season_controller.DeleteSeasonForm')
def test_details_when_season_not_found_should_abort_with_404_error(
        fake_delete_season_form, fake_season_repository
):
    # Arrange
    fake_season_repository.get_season.side_effect = IndexError()

    # Act
    with pytest.raises(NotFound):
        result = mod.details(1)


@patch('app.flask.season_controller.render_template')
@patch('app.flask.season_controller.flash')
@patch('app.flask.season_controller.NewSeasonForm')
def test_create_when_form_not_submitted_and_no_form_errors_should_render_create_template(
        fake_new_season_form, fake_flash, fake_render_template
):
    # Arrange
    fake_new_season_form.return_value.validate_on_submit.return_value = False
    fake_new_season_form.return_value.errors = None

    # Act
    result = mod.create()

    # Assert
    fake_flash.assert_not_called()
    fake_render_template('seasons/create.html', form=fake_new_season_form.return_value)
    assert result is fake_render_template.return_value


@patch('app.flask.season_controller.render_template')
@patch('app.flask.season_controller.flash')
@patch('app.flask.season_controller.NewSeasonForm')
def test_create_when_form_not_submitted_and_form_errors_should_flash_errors_and_render_create_template(
        fake_new_season_form, fake_flash, fake_render_template
):
    # Arrange
    fake_new_season_form.return_value.validate_on_submit.return_value = False

    errors = 'errors'
    fake_new_season_form.return_value.errors = errors

    # Act
    result = mod.create()

    # Assert
    fake_flash.assert_called_once_with(f"{errors}", 'danger')
    fake_render_template('seasons/create.html', form=fake_new_season_form.return_value)
    assert result is fake_render_template.return_value


@patch('app.flask.season_controller.redirect')
@patch('app.flask.season_controller.url_for')
@patch('app.flask.season_controller.flash')
@patch('app.flask.season_controller.season_repository')
@patch('app.flask.season_controller.season_factory')
@patch('app.flask.season_controller.NewSeasonForm')
def test_create_when_form_submitted_and_no_errors_caught_should_flash_success_message_and_redirect_to_season_index(
        fake_new_season_form, fake_season_factory, fake_season_repository, fake_flash, fake_url_for,
        fake_redirect
):
    # Arrange
    fake_new_season_form.return_value.validate_on_submit.return_value = True
    fake_new_season_form.return_value.year.data = 1
    fake_new_season_form.return_value.num_of_weeks_scheduled.data = 0
    fake_new_season_form.return_value.num_of_weeks_completed.data = 0

    kwargs = {
        'year': 1,
        'num_of_weeks_scheduled': 0,
        'num_of_weeks_completed': 0,
    }
    season = Season(**kwargs)
    fake_season_factory.create_season.return_value = season

    # Act
    result = mod.create()

    # Assert
    fake_season_factory.create_season.assert_called_once_with(**kwargs)
    fake_season_repository.add_season.assert_called_once_with(season)
    fake_flash(f"Item {season.year} has been successfully submitted.", 'success')
    fake_url_for.assert_called_once_with('season.index')
    fake_redirect.assert_called_once_with(fake_url_for.return_value)
    assert result is fake_redirect.return_value


@patch('app.flask.season_controller.render_template')
@patch('app.flask.season_controller.flash')
@patch('app.flask.season_controller.season_repository')
@patch('app.flask.season_controller.season_factory')
@patch('app.flask.season_controller.NewSeasonForm')
def test_create_when_form_submitted_and_value_error_caught_should_flash_error_message_and_render_create_template(
        fake_new_season_form, fake_season_factory, fake_season_repository, fake_flash, fake_render_template
):
    # Arrange
    fake_new_season_form.return_value.validate_on_submit.return_value = True
    fake_new_season_form.return_value.year.data = 1
    fake_new_season_form.return_value.num_of_weeks_scheduled.data = 0
    fake_new_season_form.return_value.num_of_weeks_completed.data = 0

    kwargs = {
        'year': 1,
        'num_of_weeks_scheduled': 0,
        'num_of_weeks_completed': 0,
    }
    season = Season(**kwargs)
    fake_season_factory.create_season.return_value = season

    err = ValueError()
    fake_season_repository.add_season.side_effect = err

    # Act
    result = mod.create()

    # Assert
    fake_season_factory.create_season.assert_called_once_with(**kwargs)
    fake_season_repository.add_season.assert_called_once_with(season)
    fake_flash.assert_called_once_with(str(err), 'danger')
    fake_render_template.assert_called_once_with(
        'seasons/create.html', season=None, form=fake_new_season_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.season_controller.season_repository')
def test_edit_when_season_not_found_should_abort_with_404_error(fake_season_repository):
    # Arrange
    old_season = None
    fake_season_repository.get_season.return_value = old_season

    # Act
    with pytest.raises(NotFound):
        result = mod.edit(1)


@patch('app.flask.season_controller.render_template')
@patch('app.flask.season_controller.flash')
@patch('app.flask.season_controller.EditSeasonForm')
@patch('app.flask.season_controller.season_repository')
def test_edit_when_season_found_and_form_not_submitted_and_no_form_errors_should_render_edit_template(
        fake_season_repository, fake_edit_season_form, fake_flash, fake_render_template
):
    # Arrange
    old_season = Season(
        year=1,
        num_of_weeks_scheduled=0,
        num_of_weeks_completed=0
    )
    fake_season_repository.get_season.return_value = old_season

    fake_edit_season_form.return_value.validate_on_submit.return_value = False
    fake_edit_season_form.return_value.errors = None

    # Act
    result = mod.edit(1)

    # Assert
    assert fake_edit_season_form.return_value.year.data == old_season.year
    assert fake_edit_season_form.return_value.num_of_weeks_scheduled.data == old_season.num_of_weeks_scheduled
    assert fake_edit_season_form.return_value.num_of_weeks_completed.data == old_season.num_of_weeks_completed
    fake_flash.assert_not_called()
    fake_render_template.assert_called_once_with(
        'seasons/edit.html', season=old_season, form=fake_edit_season_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.season_controller.render_template')
@patch('app.flask.season_controller.flash')
@patch('app.flask.season_controller.EditSeasonForm')
@patch('app.flask.season_controller.season_repository')
def test_edit_when_season_found_and_form_not_submitted_and_form_errors_should_flash_errors_and_render_edit_template(
        fake_season_repository, fake_edit_season_form, fake_flash, fake_render_template
):
    # Arrange
    old_season = Season(
        year=1,
        num_of_weeks_scheduled=0,
        num_of_weeks_completed=0
    )
    fake_season_repository.get_season.return_value = old_season

    fake_edit_season_form.return_value.validate_on_submit.return_value = False
    fake_edit_season_form.return_value.errors = None

    errors = 'errors'
    fake_edit_season_form.return_value.errors = errors

    # Act
    result = mod.edit(1)

    # Assert
    assert fake_edit_season_form.return_value.year.data == old_season.year
    assert fake_edit_season_form.return_value.num_of_weeks_scheduled.data == old_season.num_of_weeks_scheduled
    assert fake_edit_season_form.return_value.num_of_weeks_completed.data == old_season.num_of_weeks_completed
    fake_flash.assert_called_once_with(f"{errors}", 'danger')
    fake_render_template.assert_called_once_with(
        'seasons/edit.html', season=old_season, form=fake_edit_season_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.season_controller.redirect')
@patch('app.flask.season_controller.url_for')
@patch('app.flask.season_controller.flash')
@patch('app.flask.season_controller.season_factory')
@patch('app.flask.season_controller.EditSeasonForm')
@patch('app.flask.season_controller.season_repository')
def test_edit_when_season_found_and_form_submitted_and_no_errors_caught_should_flash_success_message_and_redirect_to_season_details(
        fake_season_repository, fake_edit_season_form, fake_season_factory, fake_flash, fake_url_for,
        fake_redirect
):
    # Arrange
    id = 1

    old_season = Season(
        id=id,
        year=1,
        num_of_weeks_scheduled=0,
        num_of_weeks_completed=0
    )
    fake_season_repository.get_season.return_value = old_season

    fake_edit_season_form.return_value.validate_on_submit.return_value = True
    fake_edit_season_form.return_value.year.data = 2
    fake_edit_season_form.return_value.num_of_weeks_scheduled.data = 1
    fake_edit_season_form.return_value.num_of_weeks_completed.data = 1

    kwargs = {
        'id': id,
        'year': 2,
        'num_of_weeks_scheduled': 1,
        'num_of_weeks_completed': 1,
    }
    new_season = Season(**kwargs)
    fake_season_factory.create_season.return_value = new_season

    # Act
    result = mod.edit(id)

    # Assert
    fake_season_factory.create_season.assert_called_once_with(**kwargs)
    fake_season_repository.update_season.assert_called_once_with(new_season)
    fake_flash.assert_called_once_with(
        f"Item {fake_edit_season_form.return_value.year.data} has been successfully updated.", 'success'
    )
    fake_url_for.assert_called_once_with('season.details', id=id)
    fake_redirect.assert_called_once_with(fake_url_for.return_value)
    assert result is fake_redirect.return_value


@patch('app.flask.season_controller.render_template')
@patch('app.flask.season_controller.flash')
@patch('app.flask.season_controller.season_factory')
@patch('app.flask.season_controller.EditSeasonForm')
@patch('app.flask.season_controller.season_repository')
def test_edit_when_season_found_and_form_submitted_and_value_error_caught_should_flash_error_message_and_render_edit_template(
        fake_season_repository, fake_edit_season_form, fake_season_factory, fake_flash,
        fake_render_template
):
    id = 1

    old_season = Season(
        id=id,
        year=1,
        num_of_weeks_scheduled=0,
        num_of_weeks_completed=0
    )
    fake_season_repository.get_season.return_value = old_season

    fake_edit_season_form.return_value.validate_on_submit.return_value = True
    fake_edit_season_form.return_value.year.data = 2
    fake_edit_season_form.return_value.num_of_weeks_scheduled.data = 1
    fake_edit_season_form.return_value.num_of_weeks_completed.data = 1

    kwargs = {
        'id': id,
        'year': 2,
        'num_of_weeks_scheduled': 1,
        'num_of_weeks_completed': 1,
    }
    new_season = Season(**kwargs)
    fake_season_factory.create_season.return_value = new_season

    err = ValueError()
    fake_season_repository.update_season.side_effect = err

    # Act
    result = mod.edit(id)

    # Assert
    fake_season_factory.create_season.assert_called_once_with(**kwargs)
    fake_season_repository.update_season.assert_called_once_with(new_season)
    fake_flash.assert_called_once_with(str(err), 'danger')
    fake_render_template.assert_called_once_with(
        'seasons/edit.html', season=old_season, form=fake_edit_season_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.season_controller.render_template')
@patch('app.flask.season_controller.season_repository')
def test_delete_when_request_method_is_get_should_render_delete_template(
        fake_season_repository, fake_render_template, test_app
):
    # Arrange
    season = Season()
    fake_season_repository.get_season.return_value = season

    # Act
    with test_app.test_request_context(
            '/seasons/delete?id=1',
            method='GET'
    ):
        with test_app.app_context():
            result = mod.delete(1)

    # Assert
    fake_season_repository.get_season.assert_called_once_with(1)
    fake_render_template.assert_called_once_with('seasons/delete.html', season=season)
    assert result is fake_render_template.return_value


@patch('app.flask.season_controller.redirect')
@patch('app.flask.season_controller.url_for')
@patch('app.flask.season_controller.flash')
@patch('app.flask.season_controller.season_repository')
def test_delete_when_request_method_is_post_and_season_found_should_flash_success_message_and_redirect_to_seasons_index(
        fake_season_repository, fake_flash, fake_url_for, fake_redirect, test_app
):
    # Arrange
    season = Season()
    fake_season_repository.get_season.return_value = season

    # Act
    id = 1
    with test_app.test_request_context(
            '/seasons/delete?id=1',
            method='POST'
    ):
        with test_app.app_context():
            result = mod.delete(id)

    # Assert
    fake_season_repository.delete_season.assert_called_once_with(id)
    fake_flash.assert_called_once_with(f"Season {season.year} has been successfully deleted.", 'success')
    fake_url_for.assert_called_once_with('season.index')
    fake_redirect.assert_called_once_with(fake_url_for.return_value)
    assert result is fake_redirect.return_value


@patch('app.flask.season_controller.season_repository')
def test_delete_when_request_method_is_post_and_season_not_found_should_abort_with_404_error(
        fake_season_repository, test_app
):
    # Arrange
    season = Season()
    fake_season_repository.get_season.return_value = season
    fake_season_repository.delete_season.side_effect = IndexError()

    # Act
    with test_app.test_request_context(
            '/seasons/delete?id=1',
            method='POST'
    ):
        with test_app.app_context():
            with pytest.raises(NotFound):
                result = mod.delete(1)
