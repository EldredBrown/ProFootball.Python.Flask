from unittest.mock import patch, MagicMock

import pytest

from werkzeug.exceptions import NotFound

import app.flask.season_controller as mod

from app.data.models.season import Season
from app.data.repositories.season_repository import SeasonRepository
from test_app import create_app


@pytest.fixture()
def test_app():
    return create_app()


@patch('app.flask.season_controller.render_template')
@patch('app.flask.season_controller.injector')
def test_index_should_render_season_index_template(fake_injector, fake_render_template):
    # Arrange
    fake_season_repository = MagicMock(SeasonRepository)
    fake_injector.get.return_value = fake_season_repository

    # Act
    result = mod.index()

    # Assert
    fake_injector.get.assert_called_once_with(SeasonRepository)
    fake_season_repository.get_seasons.assert_called_once()
    fake_render_template.assert_called_once_with(
        'seasons/index.html', seasons=fake_season_repository.get_seasons.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.season_controller.render_template')
@patch('app.flask.season_controller.injector')
@patch('app.flask.season_controller.DeleteSeasonForm')
def test_details_when_season_found_should_render_season_details_template(
        fake_form, fake_injector, fake_render_template
):
    # Arrange
    year = 1920

    fake_season_repository = MagicMock(SeasonRepository)
    fake_injector.get.return_value = fake_season_repository

    # Act
    result = mod.details(year)

    # Assert
    fake_form.assert_called_once()
    fake_injector.get.assert_called_once_with(SeasonRepository)
    fake_season_repository.get_season.assert_called_once_with(year)
    fake_render_template.assert_called_once_with(
        'seasons/details.html',
        season=fake_season_repository.get_season.return_value,
        form=fake_form.return_value
    )
    assert result == fake_render_template.return_value


@patch('app.flask.season_controller.injector')
@patch('app.flask.season_controller.DeleteSeasonForm')
def test_details_when_season_not_found_should_abort_with_404_error(fake_form, fake_injector):
    # Arrange
    fake_season_repository = MagicMock(SeasonRepository)
    fake_season_repository.get_season.side_effect = IndexError()
    fake_injector.get.return_value = fake_season_repository

    # Act
    with pytest.raises(NotFound):
        result = mod.details(1920)


@patch('app.flask.season_controller.render_template')
@patch('app.flask.season_controller.flash')
@patch('app.flask.season_controller.NewSeasonForm')
def test_create_when_form_not_submitted_and_no_form_errors_should_render_create_template(
        fake_form, fake_flash, fake_render_template
):
    # Arrange
    fake_form.return_value.validate_on_submit.return_value = False
    fake_form.return_value.errors = None

    # Act
    result = mod.create()

    # Assert
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    fake_flash.assert_not_called()
    fake_render_template('seasons/create.html', form=fake_form.return_value)
    assert result is fake_render_template.return_value


@patch('app.flask.season_controller.render_template')
@patch('app.flask.season_controller.flash')
@patch('app.flask.season_controller.NewSeasonForm')
def test_create_when_form_not_submitted_and_form_errors_should_flash_errors_and_render_create_template(
        fake_form, fake_flash, fake_render_template
):
    # Arrange
    fake_form.return_value.validate_on_submit.return_value = False

    errors = 'errors'
    fake_form.return_value.errors = errors

    # Act
    result = mod.create()

    # Assert
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    fake_flash.assert_called_once_with(f"{errors}", 'danger')
    fake_render_template('seasons/create.html', form=fake_form.return_value)
    assert result is fake_render_template.return_value


@patch('app.flask.season_controller.redirect')
@patch('app.flask.season_controller.url_for')
@patch('app.flask.season_controller.flash')
@patch('app.flask.season_controller.injector')
@patch('app.flask.season_controller.season_factory')
@patch('app.flask.season_controller.NewSeasonForm')
def test_create_when_form_submitted_and_no_errors_caught_should_flash_success_message_and_redirect_to_season_index(
        fake_form, fake_season_factory, fake_injector, fake_flash,
        fake_url_for, fake_redirect
):
    # Arrange
    year = 1920

    fake_form.return_value.validate_on_submit.return_value = True
    fake_form.return_value.year.data = year

    kwargs = {
        'year': year,
    }
    season = Season(**kwargs)
    fake_season_factory.create_season.return_value = season

    fake_season_repository = MagicMock(SeasonRepository)
    fake_injector.get.return_value = fake_season_repository

    # Act
    result = mod.create()

    # Assert
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    fake_season_factory.create_season.assert_called_once_with(None, **kwargs)
    fake_injector.get.assert_called_once_with(SeasonRepository)
    fake_season_repository.add_season.assert_called_once_with(season)
    fake_flash(f"Item {season.year} has been successfully submitted.", 'success')
    fake_url_for.assert_called_once_with('season.index')
    fake_redirect.assert_called_once_with(fake_url_for.return_value)
    assert result is fake_redirect.return_value


@patch('app.flask.season_controller.render_template')
@patch('app.flask.season_controller.flash')
@patch('app.flask.season_controller.injector')
@patch('app.flask.season_controller.season_factory')
@patch('app.flask.season_controller.NewSeasonForm')
def test_create_when_form_submitted_and_value_error_caught_should_flash_error_message_and_render_create_template(
        fake_form, fake_season_factory, fake_injector,
        fake_flash, fake_render_template
):
    # Arrange
    year = 1920

    fake_form.return_value.validate_on_submit.return_value = True
    fake_form.return_value.year.data = year

    kwargs = {
        'year': year,
    }
    season = Season(**kwargs)
    fake_season_factory.create_season.return_value = season

    fake_season_repository = MagicMock(SeasonRepository)
    err = ValueError()
    fake_season_repository.add_season.side_effect = err
    fake_injector.get.return_value = fake_season_repository

    # Act
    result = mod.create()

    # Assert
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    fake_season_factory.create_season.assert_called_once_with(None, **kwargs)
    fake_injector.get.assert_called_once_with(SeasonRepository)
    fake_season_repository.add_season.assert_called_once_with(season)
    fake_flash.assert_called_once_with(str(err), 'danger')
    fake_render_template.assert_called_once_with(
        'seasons/create.html', season=None, form=fake_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.season_controller.injector')
def test_delete_when_season_not_found_should_abort_with_404_error(
        fake_injector, test_app
):
    # Arrange
    year = 1

    fake_season_repository = MagicMock(SeasonRepository)
    fake_season_repository.get_season.return_value = None
    fake_injector.get.return_value = fake_season_repository

    # Act
    with test_app.test_request_context(
            f'/seasons/delete?year={year}',
            method='POST'
    ):
        with pytest.raises(NotFound):
            result = mod.delete(year)

    # Assert
    fake_injector.get.assert_called_once_with(SeasonRepository)
    fake_season_repository.get_season.assert_called_once_with(year)


@patch('app.flask.season_controller.render_template')
@patch('app.flask.season_controller.injector')
@patch('app.flask.season_controller.DeleteSeasonForm')
def test_delete_when_request_method_is_get_should_render_delete_template(
        fake_form, fake_injector,
        fake_render_template, test_app
):
    # Arrange
    fake_season_repository = MagicMock(SeasonRepository)
    season = Season()
    fake_season_repository.get_season.return_value = season
    fake_injector.get.return_value = fake_season_repository

    year = 1

    # Act
    with test_app.test_request_context(
            f'/seasons/delete?year={year}',
            method='GET'
    ):
        result = mod.delete(year)

    # Assert
    fake_form.assert_called_once()
    fake_injector.get.assert_called_once_with(SeasonRepository)
    fake_season_repository.get_season.assert_called_once_with(year)
    fake_render_template.assert_called_once_with('seasons/delete.html', season=season,
                                                 form=fake_form.return_value)
    assert result is fake_render_template.return_value


@patch('app.flask.season_controller.redirect')
@patch('app.flask.season_controller.url_for')
@patch('app.flask.season_controller.flash')
@patch('app.flask.season_controller.injector')
def test_delete_when_request_method_is_post_and_season_found_should_flash_success_message_and_redirect_to_seasons_index(
        fake_injector, fake_flash, fake_url_for,
        fake_redirect, test_app
):
    # Arrange
    year = 1

    fake_season_repository = MagicMock(SeasonRepository)
    season = Season()
    fake_season_repository.get_season.return_value = season
    fake_injector.get.return_value = fake_season_repository

    # Act
    with test_app.test_request_context(
            f'/seasons/delete?year={year}',
            method='POST'
    ):
        result = mod.delete(year)

    # Assert
    fake_injector.get.assert_called_once_with(SeasonRepository)
    fake_season_repository.get_season.assert_called_once_with(year)
    fake_season_repository.delete_season.assert_called_once_with(year)
    fake_flash.assert_called_once_with(f"Season {season.year} has been successfully deleted.", 'success')
    fake_url_for.assert_called_once_with('season.index')
    fake_redirect.assert_called_once_with(fake_url_for.return_value)
    assert result is fake_redirect.return_value


@patch('app.flask.season_controller.injector')
def test_delete_when_request_method_is_post_and_index_error_is_caught_should_abort_with_404_error(
        fake_injector, test_app
):
    # Arrange
    id = 1

    fake_season_repository = MagicMock(SeasonRepository)
    season = Season()
    fake_season_repository.get_season.return_value = season
    fake_season_repository.delete_season.side_effect = IndexError()
    fake_injector.get.return_value = fake_season_repository

    # Act
    with test_app.test_request_context(
            f'/seasons/delete?id={id}',
            method='POST'
    ):
        with pytest.raises(NotFound):
            result = mod.delete(id)

    # Assert
    fake_injector.get.assert_called_once_with(SeasonRepository)
    fake_season_repository.get_season.assert_called_once_with(id)
