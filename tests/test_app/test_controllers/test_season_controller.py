from unittest.mock import patch

import pytest

from werkzeug.exceptions import NotFound

import app.flask.season_controller as season_controller
from app.data.models.season import Season

from test_app import create_app


@pytest.fixture()
def test_app():
    test_app = create_app()
    return test_app


@patch('app.flask.season_controller.render_template')
@patch('app.flask.season_controller.season_repository')
def test_index_should_render_seasons_index(fake_season_repository, fake_render_template, test_app):
    # Act
    with test_app.app_context():
        result = season_controller.index()

    # Assert
    fake_season_repository.get_seasons.assert_called_once()
    fake_render_template.assert_called_once_with(
        'seasons/index.html', seasons=fake_season_repository.get_seasons.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.season_controller.season_repository')
@patch('app.flask.season_controller.DeleteSeasonForm')
@patch('app.flask.season_controller.render_template')
def test_details_when_season_found_should_render_season_details(
        fake_render_template, fake_delete_season_form, fake_season_repository, test_app
):
    # Arrange
    id = 1

    # Act
    with test_app.app_context():
        result = season_controller.details(id)

    # Assert
    fake_delete_season_form.assert_called_once()
    fake_season_repository.get_season.assert_called_once_with(id)
    fake_render_template.assert_called_once_with(
        'seasons/details.html',
        season=fake_season_repository.get_season.return_value, delete_season_form=fake_delete_season_form.return_value
    )
    assert result == fake_render_template.return_value


@patch('app.flask.season_controller.season_repository')
@patch('app.flask.season_controller.DeleteSeasonForm')
def test_details_when_season_not_found_should_abort_with_404_error(
        fake_delete_season_form, fake_season_repository, test_app
):
    # Arrange
    fake_season_repository.get_season.side_effect = IndexError()

    # Act
    with test_app.app_context():
        with pytest.raises(NotFound):
            result = season_controller.details(1)


@patch('app.flask.season_controller.render_template')
@patch('app.flask.season_controller.flash')
@patch('app.flask.season_controller.NewSeasonForm')
def test_create_when_http_method_is_get_and_there_are_no_form_errors_should_render_create_template(
        fake_new_season_form, fake_flash, fake_render_template, test_app
):
    # Arrange
    fake_new_season_form.return_value.validate_on_submit.return_value = False
    fake_new_season_form.return_value.errors = None

    # Act
    with test_app.app_context():
        result = season_controller.create()

    # Assert
    fake_flash.assert_not_called()
    fake_render_template('seasons/create.html', form=fake_new_season_form.return_value)
    assert result is fake_render_template.return_value


@patch('app.flask.season_controller.render_template')
@patch('app.flask.season_controller.flash')
@patch('app.flask.season_controller.NewSeasonForm')
def test_create_when_http_method_is_get_and_there_are_form_errors_should_flash_errors_and_render_create_template(
        fake_new_season_form, fake_flash, fake_render_template, test_app
):
    # Arrange
    fake_new_season_form.return_value.validate_on_submit.return_value = False
    errors = 'errors'
    fake_new_season_form.return_value.errors = errors

    # Act
    with test_app.app_context():
        result = season_controller.create()

    # Assert
    fake_flash.assert_called_once_with(f"{errors}", 'danger')
    fake_render_template('seasons/create.html', form=fake_new_season_form.return_value)
    assert result is fake_render_template.return_value


@patch('app.flask.season_controller.url_for')
@patch('app.flask.season_controller.flash')
@patch('app.flask.season_controller.season_repository')
@patch('app.flask.season_controller.redirect')
@patch('app.flask.season_controller.NewSeasonForm')
def test_create_when_http_method_is_post_and_no_value_error_caught_should_flash_success_message_and_redirect_to_seasons_index(
        fake_new_season_form, fake_redirect, fake_season_repository, fake_flash, fake_url_for, test_app
):
    # Arrange
    fake_new_season_form.return_value.validate_on_submit.return_value = True
    fake_new_season_form.return_value.year.data = 1920
    fake_new_season_form.return_value.num_of_weeks_scheduled.data = 13
    fake_new_season_form.return_value.num_of_weeks_completed.data = 13

    kwargs = {
        'year': 1920,
        'num_of_weeks_scheduled': 13,
        'num_of_weeks_completed': 13
    }

    # Act
    with test_app.app_context():
        result = season_controller.create()

    # Assert
    fake_season_repository.add_season.assert_called_once_with(**kwargs)
    fake_flash(f"Item {kwargs['year']} has been successfully submitted.", 'success')
    fake_url_for.assert_called_once_with('season.index')
    fake_redirect.assert_called_once_with(fake_url_for.return_value)
    assert result is fake_redirect.return_value


@patch('app.flask.season_controller.render_template')
@patch('app.flask.season_controller.flash')
@patch('app.flask.season_controller.season_repository')
@patch('app.flask.season_controller.NewSeasonForm')
def test_create_when_http_method_is_post_and_value_error_caught_should_flash_error_message_and_render_create_template(
        fake_new_season_form, fake_season_repository, fake_flash, fake_render_template, test_app
):
    # Arrange
    fake_new_season_form.return_value.validate_on_submit.return_value = True
    fake_new_season_form.return_value.year.data = 1920
    fake_new_season_form.return_value.num_of_weeks_scheduled.data = 13
    fake_new_season_form.return_value.num_of_weeks_completed.data = 13

    err = ValueError()
    fake_season_repository.add_season.side_effect = err

    kwargs = {
        'year': 1920,
        'num_of_weeks_scheduled': 13,
        'num_of_weeks_completed': 13
    }

    # Act
    with test_app.app_context():
        result = season_controller.create()

    # Assert
    fake_season_repository.add_season.assert_called_once_with(**kwargs)
    fake_flash.assert_called_once_with(str(err), 'danger')
    fake_render_template.assert_called_once_with('seasons/create.html', form=fake_new_season_form.return_value)
    assert result is fake_render_template.return_value


@patch('app.flask.season_controller.season_repository')
def test_edit_when_season_not_found_should_abort_with_404_error(fake_season_repository, test_app):
    # Arrange
    season = None
    fake_season_repository.get_season.return_value = season

    # Act
    with test_app.app_context():
        with pytest.raises(NotFound):
            result = season_controller.edit(1)


@patch('app.flask.season_controller.render_template')
@patch('app.flask.season_controller.flash')
@patch('app.flask.season_controller.EditSeasonForm')
@patch('app.flask.season_controller.season_repository')
def test_edit_when_season_is_found_and_http_method_is_get_and_there_are_no_form_errors_should_render_edit_template(
        fake_season_repository, fake_edit_season_form, fake_flash, fake_render_template, test_app
):
    # Arrange
    season = Season(
        year=1920,
        num_of_weeks_scheduled=13,
        num_of_weeks_completed=13
    )
    fake_season_repository.get_season.return_value = season

    fake_edit_season_form.return_value.validate_on_submit.return_value = False
    fake_edit_season_form.return_value.errors = None

    # Act
    with test_app.app_context():
        result = season_controller.edit(1)

    # Assert
    assert fake_edit_season_form.return_value.year.data == season.year
    assert fake_edit_season_form.return_value.num_of_weeks_scheduled.data == season.num_of_weeks_scheduled
    assert fake_edit_season_form.return_value.num_of_weeks_completed.data == season.num_of_weeks_completed
    fake_flash.assert_not_called()
    fake_render_template.assert_called_once_with(
        'seasons/edit.html', season=season, form=fake_edit_season_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.season_controller.render_template')
@patch('app.flask.season_controller.flash')
@patch('app.flask.season_controller.EditSeasonForm')
@patch('app.flask.season_controller.season_repository')
def test_edit_when_season_is_found_and_http_method_is_get_and_there_are_form_errors_should_flash_errors_and_render_edit_template(
        fake_season_repository, fake_edit_season_form, fake_flash, fake_render_template, test_app
):
    # Arrange
    season = Season(
        year=1920,
        num_of_weeks_scheduled=13,
        num_of_weeks_completed=13
    )
    fake_season_repository.get_season.return_value = season

    fake_edit_season_form.return_value.validate_on_submit.return_value = False
    errors = 'errors'
    fake_edit_season_form.return_value.errors = errors

    # Act
    with test_app.app_context():
        result = season_controller.edit(1)

    # Assert
    assert fake_edit_season_form.return_value.year.data == season.year
    assert fake_edit_season_form.return_value.num_of_weeks_scheduled.data == season.num_of_weeks_scheduled
    assert fake_edit_season_form.return_value.num_of_weeks_completed.data == season.num_of_weeks_completed
    fake_flash.assert_called_once_with(f"{errors}", 'danger')
    fake_render_template.assert_called_once_with(
        'seasons/edit.html', season=season, form=fake_edit_season_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.season_controller.url_for')
@patch('app.flask.season_controller.flash')
@patch('app.flask.season_controller.redirect')
@patch('app.flask.season_controller.EditSeasonForm')
@patch('app.flask.season_controller.season_repository')
def test_edit_when_season_is_found_and_http_method_is_post_and_no_value_error_caught_should_flash_success_message_and_redirect_to_season_details(
        fake_season_repository, fake_edit_season_form, fake_redirect, fake_flash, fake_url_for, test_app
):
    # Arrange
    season = Season(
        year=1920,
        num_of_weeks_scheduled=13,
        num_of_weeks_completed=13
    )
    fake_season_repository.get_season.return_value = season

    fake_edit_season_form.return_value.validate_on_submit.return_value = True
    fake_edit_season_form.return_value.year.data = 1921
    fake_edit_season_form.return_value.num_of_weeks_scheduled.data = 0
    fake_edit_season_form.return_value.num_of_weeks_completed.data = 0

    id = 1
    kwargs = {
        'id': id,
        'year': 1921,
        'num_of_weeks_scheduled': 0,
        'num_of_weeks_completed': 0
    }

    # Act
    with test_app.app_context():
        result = season_controller.edit(id)

    # Assert
    fake_season_repository.update_season.assert_called_once_with(**kwargs)
    fake_flash.assert_called_once_with(
        f"Item {fake_edit_season_form.return_value.year.data} has been successfully updated.", 'success'
    )
    fake_url_for.assert_called_once_with('season.details', id=id)
    fake_redirect.assert_called_once_with(fake_url_for.return_value)
    assert result is fake_redirect.return_value


@patch('app.flask.season_controller.flash')
@patch('app.flask.season_controller.render_template')
@patch('app.flask.season_controller.EditSeasonForm')
@patch('app.flask.season_controller.season_repository')
def test_edit_when_season_is_found_and_http_method_is_post_and_value_error_caught_should_flash_error_message_and_render_edit_template(
        fake_season_repository, fake_edit_season_form, fake_render_template, fake_flash, test_app
):
    # Arrange
    season = Season(
        year=1920,
        num_of_weeks_scheduled=13,
        num_of_weeks_completed=13
    )
    fake_season_repository.get_season.return_value = season

    fake_edit_season_form.return_value.validate_on_submit.return_value = True
    fake_edit_season_form.return_value.year.data = 1921
    fake_edit_season_form.return_value.num_of_weeks_scheduled.data = 0
    fake_edit_season_form.return_value.num_of_weeks_completed.data = 0

    err = ValueError()
    fake_season_repository.update_season.side_effect = err

    id = 1
    kwargs = {
        'id': id,
        'year': 1921,
        'num_of_weeks_scheduled': 0,
        'num_of_weeks_completed': 0
    }

    # Act
    with test_app.app_context():
        result = season_controller.edit(id)

    # Assert
    fake_season_repository.update_season.assert_called_once_with(**kwargs)
    fake_flash.assert_called_once_with(str(err), 'danger')
    fake_render_template.assert_called_once_with(
        'seasons/edit.html', season=season, form=fake_edit_season_form.return_value
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
            result = season_controller.delete(1)

    # Assert
    fake_season_repository.get_season.assert_called_once_with(1)
    fake_render_template.assert_called_once_with('seasons/delete.html', season=season)
    assert result is fake_render_template.return_value


@patch('app.flask.season_controller.redirect')
@patch('app.flask.season_controller.url_for')
@patch('app.flask.season_controller.flash')
@patch('app.flask.season_controller.season_repository')
def test_delete_when_request_method_is_post_and_season_is_found_should_flash_success_message_and_redirect_to_seasons_index(
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
            result = season_controller.delete(id)

    # Assert
    fake_season_repository.delete_season.assert_called_once_with(id)
    fake_flash.assert_called_once_with(f"Season {season.year} has been successfully deleted.", 'success')
    fake_url_for.assert_called_once_with('season.index')
    fake_redirect.assert_called_once_with(fake_url_for.return_value)
    assert result is fake_redirect.return_value


@patch('app.flask.season_controller.redirect')
@patch('app.flask.season_controller.url_for')
@patch('app.flask.season_controller.flash')
@patch('app.flask.season_controller.season_repository')
def test_delete_when_request_method_is_post_and_season_is_not_found_should_abort_with_404_error(
        fake_season_repository, fake_flash, fake_url_for, fake_redirect, test_app
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
                result = season_controller.delete(1)
