from unittest.mock import patch

import pytest

from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound

import app.flask.league_controller as league_controller

from app.data.models.season import Season
from app.data.models.league import League
from app.data.models.game import Game
from app.data.models.league_season import LeagueSeason
from app.data.models.team_season import TeamSeason
from test_app import create_app


@pytest.fixture()
def test_app():
    return create_app()


@patch('app.flask.league_controller.render_template')
@patch('app.flask.league_controller.league_repository')
def test_index_should_render_league_index_template(fake_league_repository, fake_render_template, test_app):
    # Act
    with test_app.app_context():
        result = league_controller.index()

    # Assert
    fake_league_repository.get_leagues.assert_called_once()
    fake_render_template.assert_called_once_with(
        'leagues/index.html', leagues=fake_league_repository.get_leagues.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.league_controller.league_repository')
@patch('app.flask.league_controller.DeleteLeagueForm')
@patch('app.flask.league_controller.render_template')
def test_details_when_league_found_should_render_league_details_template(
        fake_render_template, fake_delete_league_form, fake_league_repository, test_app
):
    # Arrange
    id = 1

    # Act
    with test_app.app_context():
        result = league_controller.details(id)

    # Assert
    fake_delete_league_form.assert_called_once()
    fake_league_repository.get_league.assert_called_once_with(id)
    fake_render_template.assert_called_once_with(
        'leagues/details.html',
        league=fake_league_repository.get_league.return_value, delete_league_form=fake_delete_league_form.return_value
    )
    assert result == fake_render_template.return_value


@patch('app.flask.league_controller.league_repository')
@patch('app.flask.league_controller.DeleteLeagueForm')
def test_details_when_league_not_found_should_abort_with_404_error(
        fake_delete_league_form, fake_league_repository, test_app
):
    # Arrange
    fake_league_repository.get_league.side_effect = IndexError()

    # Act
    with test_app.app_context():
        with pytest.raises(NotFound):
            result = league_controller.details(1)


@patch('app.flask.league_controller.render_template')
@patch('app.flask.league_controller.flash')
@patch('app.flask.league_controller.NewLeagueForm')
def test_create_when_form_not_submitted_and_no_form_errors_should_render_create_template(
        fake_new_league_form, fake_flash, fake_render_template, test_app
):
    # Arrange
    fake_new_league_form.return_value.validate_on_submit.return_value = False
    fake_new_league_form.return_value.errors = None

    # Act
    with test_app.app_context():
        result = league_controller.create()

    # Assert
    fake_flash.assert_not_called()
    fake_render_template('leagues/create.html', form=fake_new_league_form.return_value)
    assert result is fake_render_template.return_value


@patch('app.flask.league_controller.render_template')
@patch('app.flask.league_controller.flash')
@patch('app.flask.league_controller.NewLeagueForm')
def test_create_when_form_not_submitted_and_form_errors_should_flash_errors_and_render_create_template(
        fake_new_league_form, fake_flash, fake_render_template, test_app
):
    # Arrange
    fake_new_league_form.return_value.validate_on_submit.return_value = False

    errors = 'errors'
    fake_new_league_form.return_value.errors = errors

    # Act
    with test_app.app_context():
        result = league_controller.create()

    # Assert
    fake_flash.assert_called_once_with(f"{errors}", 'danger')
    fake_render_template('leagues/create.html', form=fake_new_league_form.return_value)
    assert result is fake_render_template.return_value


@patch('app.flask.league_controller.url_for')
@patch('app.flask.league_controller.flash')
@patch('app.flask.league_controller.league_repository')
@patch('app.flask.league_controller.redirect')
@patch('app.flask.league_controller.NewLeagueForm')
def test_create_when_form_submitted_and_no_errors_caught_should_flash_success_message_and_redirect_to_league_index(
        fake_new_league_form, fake_redirect, fake_league_repository, fake_flash, fake_url_for, test_app
):
    # Arrange
    fake_new_league_form.return_value.validate_on_submit.return_value = True
    fake_new_league_form.return_value.short_name.data = "NFL"
    fake_new_league_form.return_value.long_name.data = "National Football League"
    fake_new_league_form.return_value.first_season_year.data = 1922
    fake_new_league_form.return_value.last_season_year.data = None

    kwargs = {
        'short_name': "NFL",
        'long_name': "National Football League",
        'first_season_year': 1922,
        'last_season_year': None
    }

    # Act
    with test_app.app_context():
        result = league_controller.create()

    # Assert
    fake_league_repository.add_league.assert_called_once_with(**kwargs)
    fake_flash(f"Item {kwargs['short_name']} has been successfully submitted.", 'success')
    fake_url_for.assert_called_once_with('league.index')
    fake_redirect.assert_called_once_with(fake_url_for.return_value)
    assert result is fake_redirect.return_value


@patch('app.flask.league_controller.render_template')
@patch('app.flask.league_controller.flash')
@patch('app.flask.league_controller.league_repository')
@patch('app.flask.league_controller.NewLeagueForm')
def test_create_when_form_submitted_and_value_error_caught_should_flash_error_message_and_render_create_template(
        fake_new_league_form, fake_league_repository, fake_flash, fake_render_template, test_app
):
    # Arrange
    fake_new_league_form.return_value.validate_on_submit.return_value = True
    fake_new_league_form.return_value.short_name.data = "NFL"
    fake_new_league_form.return_value.long_name.data = "National Football League"
    fake_new_league_form.return_value.first_season_year.data = 1922
    fake_new_league_form.return_value.last_season_year.data = None

    err = ValueError()
    fake_league_repository.add_league.side_effect = err

    kwargs = {
        'short_name': "NFL",
        'long_name': "National Football League",
        'first_season_year': 1922,
        'last_season_year': None
    }

    # Act
    with test_app.app_context():
        result = league_controller.create()

    # Assert
    fake_league_repository.add_league.assert_called_once_with(**kwargs)
    fake_flash.assert_called_once_with(str(err), 'danger')
    fake_render_template.assert_called_once_with(
        'leagues/create.html', league=None, form=fake_new_league_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.league_controller.render_template')
@patch('app.flask.league_controller.flash')
@patch('app.flask.league_controller.league_repository')
@patch('app.flask.league_controller.NewLeagueForm')
def test_create_when_form_submitted_and_integrity_error_caught_should_flash_error_message_and_render_create_template(
        fake_new_league_form, fake_league_repository, fake_flash, fake_render_template, test_app
):
    # Arrange
    fake_new_league_form.return_value.validate_on_submit.return_value = True
    fake_new_league_form.return_value.short_name.data = "NFL"
    fake_new_league_form.return_value.long_name.data = "National Football League"
    fake_new_league_form.return_value.first_season_year.data = 1922
    fake_new_league_form.return_value.last_season_year.data = None

    err = IntegrityError('statement', 'params', Exception())
    fake_league_repository.add_league.side_effect = err
    fake_league_repository.add_league.side_effect = err

    kwargs = {
        'short_name': "NFL",
        'long_name': "National Football League",
        'first_season_year': 1922,
        'last_season_year': None
    }

    # Act
    with test_app.app_context():
        result = league_controller.create()

    # Assert
    fake_league_repository.add_league.assert_called_once_with(**kwargs)
    fake_flash.assert_called_once_with(str(err), 'danger')
    fake_render_template.assert_called_once_with(
        'leagues/create.html', league=None, form=fake_new_league_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.league_controller.league_repository')
def test_edit_when_league_not_found_should_abort_with_404_error(fake_league_repository, test_app):
    # Arrange
    league = None
    fake_league_repository.get_league.return_value = league

    # Act
    with test_app.app_context():
        with pytest.raises(NotFound):
            result = league_controller.edit(1)


@patch('app.flask.league_controller.render_template')
@patch('app.flask.league_controller.flash')
@patch('app.flask.league_controller.EditLeagueForm')
@patch('app.flask.league_controller.league_repository')
def test_edit_when_league_found_and_form_not_submitted_and_no_form_errors_should_render_edit_template(
        fake_league_repository, fake_edit_league_form, fake_flash, fake_render_template, test_app
):
    with test_app.app_context():
        # Arrange
        league = League(
            short_name="NFL",
            long_name="National Football League",
            first_season_year=1922,
            last_season_year=None
        )
        fake_league_repository.get_league.return_value = league

        fake_edit_league_form.return_value.validate_on_submit.return_value = False
        fake_edit_league_form.return_value.errors = None

        # Act
        result = league_controller.edit(1)

    # Assert
    assert fake_edit_league_form.return_value.short_name.data == league.short_name
    assert fake_edit_league_form.return_value.long_name.data == league.long_name
    assert fake_edit_league_form.return_value.first_season_year.data == league.first_season_year
    assert fake_edit_league_form.return_value.last_season_year.data == league.last_season_year
    fake_flash.assert_not_called()
    fake_render_template.assert_called_once_with(
        'leagues/edit.html', league=league, form=fake_edit_league_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.league_controller.render_template')
@patch('app.flask.league_controller.flash')
@patch('app.flask.league_controller.EditLeagueForm')
@patch('app.flask.league_controller.league_repository')
def test_edit_when_league_found_and_form_not_submitted_and_form_errors_should_flash_errors_and_render_edit_template(
        fake_league_repository, fake_edit_league_form, fake_flash, fake_render_template, test_app
):
    with test_app.app_context():
        # Arrange
        league = League(
            short_name="NFL",
            long_name="National Football League",
            first_season_year=1922,
            last_season_year=None
        )
        fake_league_repository.get_league.return_value = league

        fake_edit_league_form.return_value.validate_on_submit.return_value = False

        errors = 'errors'
        fake_edit_league_form.return_value.errors = errors

        # Act
        result = league_controller.edit(1)

    # Assert
    assert fake_edit_league_form.return_value.short_name.data == league.short_name
    assert fake_edit_league_form.return_value.long_name.data == league.long_name
    assert fake_edit_league_form.return_value.first_season_year.data == league.first_season_year
    assert fake_edit_league_form.return_value.last_season_year.data == league.last_season_year
    fake_flash.assert_called_once_with(f"{errors}", 'danger')
    fake_render_template.assert_called_once_with(
        'leagues/edit.html', league=league, form=fake_edit_league_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.league_controller.url_for')
@patch('app.flask.league_controller.flash')
@patch('app.flask.league_controller.redirect')
@patch('app.flask.league_controller.EditLeagueForm')
@patch('app.flask.league_controller.league_repository')
def test_edit_when_league_found_and_form_submitted_and_no_errors_caught_should_flash_success_message_and_redirect_to_league_details(
        fake_league_repository, fake_edit_league_form, fake_redirect, fake_flash, fake_url_for, test_app
):
    with test_app.app_context():
        # Arrange
        league = League(
            short_name="NFL",
            long_name="National Football League",
            first_season_year=1922,
            last_season_year=None
        )
        fake_league_repository.get_league.return_value = league

        fake_edit_league_form.return_value.validate_on_submit.return_value = True
        fake_edit_league_form.return_value.short_name.data = "AFL"
        fake_edit_league_form.return_value.long_name.data = "American Football League"
        fake_edit_league_form.return_value.first_season_year.data = 1960
        fake_edit_league_form.return_value.last_season_year.data = 1969

        id = 1
        kwargs = {
            'id': id,
            'short_name': "AFL",
            'long_name': "American Football League",
            'first_season_year': 1960,
            'last_season_year': 1969,
        }

        # Act
        result = league_controller.edit(id)

    # Assert
    fake_league_repository.update_league.assert_called_once_with(**kwargs)
    fake_flash.assert_called_once_with(
        f"Item {fake_edit_league_form.return_value.short_name.data} has been successfully updated.", 'success'
    )
    fake_url_for.assert_called_once_with('league.details', id=id)
    fake_redirect.assert_called_once_with(fake_url_for.return_value)
    assert result is fake_redirect.return_value


@patch('app.flask.league_controller.flash')
@patch('app.flask.league_controller.render_template')
@patch('app.flask.league_controller.EditLeagueForm')
@patch('app.flask.league_controller.league_repository')
def test_edit_when_league_found_and_form_submitted_and_value_error_caught_should_flash_error_message_and_render_edit_template(
        fake_league_repository, fake_edit_league_form, fake_render_template, fake_flash, test_app
):
    with test_app.app_context():
        # Arrange
        league = League(
            short_name="NFL",
            long_name="National Football League",
            first_season_year=1922,
            last_season_year=None
        )
        fake_league_repository.get_league.return_value = league

        fake_edit_league_form.return_value.validate_on_submit.return_value = True
        fake_edit_league_form.return_value.short_name.data = "AFL"
        fake_edit_league_form.return_value.long_name.data = "American Football League"
        fake_edit_league_form.return_value.first_season_year.data = 1960
        fake_edit_league_form.return_value.last_season_year.data = 1969

        err = ValueError()
        fake_league_repository.update_league.side_effect = err

        id = 1
        kwargs = {
            'id': id,
            'short_name': "AFL",
            'long_name': "American Football League",
            'first_season_year': 1960,
            'last_season_year': 1969,
        }

        # Act
        result = league_controller.edit(id)

    # Assert
    fake_league_repository.update_league.assert_called_once_with(**kwargs)
    fake_flash.assert_called_once_with(str(err), 'danger')
    fake_render_template.assert_called_once_with(
        'leagues/edit.html', league=league, form=fake_edit_league_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.league_controller.flash')
@patch('app.flask.league_controller.render_template')
@patch('app.flask.league_controller.EditLeagueForm')
@patch('app.flask.league_controller.league_repository')
def test_edit_when_league_found_and_form_submitted_and_integrity_error_caught_should_flash_error_message_and_render_edit_template(
        fake_league_repository, fake_edit_league_form, fake_render_template, fake_flash, test_app
):
    with test_app.app_context():
        # Arrange
        league = League(
            short_name="NFL",
            long_name="National Football League",
            first_season_year=1922,
            last_season_year=None
        )
        fake_league_repository.get_league.return_value = league

        fake_edit_league_form.return_value.validate_on_submit.return_value = True
        fake_edit_league_form.return_value.short_name.data = "AFL"
        fake_edit_league_form.return_value.long_name.data = "American Football League"
        fake_edit_league_form.return_value.first_season_year.data = 1960
        fake_edit_league_form.return_value.last_season_year.data = 1969

        err = IntegrityError('statement', 'params', Exception())
        fake_league_repository.update_league.side_effect = err

        id = 1
        kwargs = {
            'id': id,
            'short_name': "AFL",
            'long_name': "American Football League",
            'first_season_year': 1960,
            'last_season_year': 1969,
        }

        # Act
        result = league_controller.edit(id)

    # Assert
    fake_league_repository.update_league.assert_called_once_with(**kwargs)
    fake_flash.assert_called_once_with(str(err), 'danger')
    fake_render_template.assert_called_once_with(
        'leagues/edit.html', league=league, form=fake_edit_league_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.league_controller.render_template')
@patch('app.flask.league_controller.league_repository')
def test_delete_when_request_method_is_get_should_render_delete_template(
        fake_league_repository, fake_render_template, test_app
):
    # Arrange
    league = League()
    fake_league_repository.get_league.return_value = league

    # Act
    with test_app.test_request_context(
            '/leagues/delete?id=1',
            method='GET'
    ):
        with test_app.app_context():
            result = league_controller.delete(1)

    # Assert
    fake_league_repository.get_league.assert_called_once_with(1)
    fake_render_template.assert_called_once_with('leagues/delete.html', league=league)
    assert result is fake_render_template.return_value


@patch('app.flask.league_controller.redirect')
@patch('app.flask.league_controller.url_for')
@patch('app.flask.league_controller.flash')
@patch('app.flask.league_controller.league_repository')
def test_delete_when_request_method_is_post_and_league_found_should_flash_success_message_and_redirect_to_leagues_index(
        fake_league_repository, fake_flash, fake_url_for, fake_redirect, test_app
):
    # Arrange
    league = League()
    fake_league_repository.get_league.return_value = league

    # Act
    id = 1
    with test_app.test_request_context(
            '/leagues/delete?id=1',
            method='POST'
    ):
        with test_app.app_context():
            result = league_controller.delete(id)

    # Assert
    fake_league_repository.delete_league.assert_called_once_with(id)
    fake_flash.assert_called_once_with(f"League {league.short_name} has been successfully deleted.", 'success')
    fake_url_for.assert_called_once_with('league.index')
    fake_redirect.assert_called_once_with(fake_url_for.return_value)
    assert result is fake_redirect.return_value


@patch('app.flask.league_controller.league_repository')
def test_delete_when_request_method_is_post_and_league_not_found_should_abort_with_404_error(
        fake_league_repository, test_app
):
    # Arrange
    league = League()
    fake_league_repository.get_league.return_value = league
    fake_league_repository.delete_league.side_effect = IndexError()

    # Act
    with test_app.test_request_context(
            '/leagues/delete?id=1',
            method='POST'
    ):
        with test_app.app_context():
            with pytest.raises(NotFound):
                result = league_controller.delete(1)
