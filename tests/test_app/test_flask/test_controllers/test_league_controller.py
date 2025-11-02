from unittest.mock import patch

import pytest

from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound

import app.flask.league_controller as mod

from app.data.models.league import League
from test_app import create_app


@pytest.fixture()
def test_app():
    return create_app()


@patch('app.flask.league_controller.render_template')
@patch('app.flask.league_controller.league_repository')
def test_index_should_render_league_index_template(fake_league_repository, fake_render_template):
    # Act
    result = mod.index()

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
        fake_render_template, fake_delete_league_form, fake_league_repository
):
    # Arrange
    id = 1

    # Act
    result = mod.details(id)

    # Assert
    fake_delete_league_form.assert_called_once()
    fake_league_repository.get_league.assert_called_once_with(id)
    fake_render_template.assert_called_once_with(
        'leagues/details.html',
        league=fake_league_repository.get_league.return_value,
        form=fake_delete_league_form.return_value
    )
    assert result == fake_render_template.return_value


@patch('app.flask.league_controller.league_repository')
@patch('app.flask.league_controller.DeleteLeagueForm')
def test_details_when_league_not_found_should_abort_with_404_error(
        fake_delete_league_form, fake_league_repository
):
    # Arrange
    fake_league_repository.get_league.side_effect = IndexError()

    # Act
    with pytest.raises(NotFound):
        result = mod.details(1)


@patch('app.flask.league_controller.render_template')
@patch('app.flask.league_controller.flash')
@patch('app.flask.league_controller.NewLeagueForm')
def test_create_when_form_not_submitted_and_no_form_errors_should_render_create_template(
        fake_new_league_form, fake_flash, fake_render_template
):
    # Arrange
    fake_new_league_form.return_value.validate_on_submit.return_value = False
    fake_new_league_form.return_value.errors = None

    # Act
    result = mod.create()

    # Assert
    fake_flash.assert_not_called()
    fake_render_template('leagues/create.html', form=fake_new_league_form.return_value)
    assert result is fake_render_template.return_value


@patch('app.flask.league_controller.render_template')
@patch('app.flask.league_controller.flash')
@patch('app.flask.league_controller.NewLeagueForm')
def test_create_when_form_not_submitted_and_form_errors_should_flash_errors_and_render_create_template(
        fake_new_league_form, fake_flash, fake_render_template
):
    # Arrange
    fake_new_league_form.return_value.validate_on_submit.return_value = False

    errors = 'errors'
    fake_new_league_form.return_value.errors = errors

    # Act
    result = mod.create()

    # Assert
    fake_flash.assert_called_once_with(f"{errors}", 'danger')
    fake_render_template('leagues/create.html', form=fake_new_league_form.return_value)
    assert result is fake_render_template.return_value


@patch('app.flask.league_controller.redirect')
@patch('app.flask.league_controller.url_for')
@patch('app.flask.league_controller.flash')
@patch('app.flask.league_controller.league_repository')
@patch('app.flask.league_controller.league_factory')
@patch('app.flask.league_controller.NewLeagueForm')
def test_create_when_form_submitted_and_no_errors_caught_should_flash_success_message_and_redirect_to_league_index(
        fake_new_league_form, fake_league_factory, fake_league_repository, fake_flash, fake_url_for,
        fake_redirect
):
    # Arrange
    fake_new_league_form.return_value.validate_on_submit.return_value = True
    fake_new_league_form.return_value.short_name.data = "L"
    fake_new_league_form.return_value.long_name.data = "League"
    fake_new_league_form.return_value.first_season_year.data = 1
    fake_new_league_form.return_value.last_season_year.data = 2

    kwargs = {
        'short_name': "L",
        'long_name': "League",
        'first_season_year': 1,
        'last_season_year': 2,
    }
    league = League(**kwargs)
    fake_league_factory.create_league.return_value = league

    # Act
    result = mod.create()

    # Assert
    fake_league_factory.create_league.assert_called_once_with(**kwargs)
    fake_league_repository.add_league.assert_called_once_with(league)
    fake_flash(f"Item {league.short_name} has been successfully submitted.", 'success')
    fake_url_for.assert_called_once_with('league.index')
    fake_redirect.assert_called_once_with(fake_url_for.return_value)
    assert result is fake_redirect.return_value


@patch('app.flask.league_controller.render_template')
@patch('app.flask.league_controller.flash')
@patch('app.flask.league_controller.league_repository')
@patch('app.flask.league_controller.league_factory')
@patch('app.flask.league_controller.NewLeagueForm')
def test_create_when_form_submitted_and_value_error_caught_should_flash_error_message_and_render_create_template(
        fake_new_league_form, fake_league_factory, fake_league_repository, fake_flash, fake_render_template
):
    # Arrange
    fake_new_league_form.return_value.validate_on_submit.return_value = True
    fake_new_league_form.return_value.short_name.data = "L"
    fake_new_league_form.return_value.long_name.data = "League"
    fake_new_league_form.return_value.first_season_year.data = 1
    fake_new_league_form.return_value.last_season_year.data = 2

    kwargs = {
        'short_name': "L",
        'long_name': "League",
        'first_season_year': 1,
        'last_season_year': 2,
    }
    league = League(**kwargs)
    fake_league_factory.create_league.return_value = league

    err = ValueError()
    fake_league_repository.add_league.side_effect = err

    # Act
    result = mod.create()

    # Assert
    fake_league_factory.create_league.assert_called_once_with(**kwargs)
    fake_league_repository.add_league.assert_called_once_with(league)
    fake_flash.assert_called_once_with(str(err), 'danger')
    fake_render_template.assert_called_once_with(
        'leagues/create.html', league=None, form=fake_new_league_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.league_controller.render_template')
@patch('app.flask.league_controller.flash')
@patch('app.flask.league_controller.league_repository')
@patch('app.flask.league_controller.league_factory')
@patch('app.flask.league_controller.NewLeagueForm')
def test_create_when_form_submitted_and_integrity_error_caught_should_flash_error_message_and_render_create_template(
        fake_new_league_form, fake_league_factory, fake_league_repository, fake_flash, fake_render_template
):
    # Arrange
    fake_new_league_form.return_value.validate_on_submit.return_value = True
    fake_new_league_form.return_value.short_name.data = "L"
    fake_new_league_form.return_value.long_name.data = "League"
    fake_new_league_form.return_value.first_season_year.data = 1
    fake_new_league_form.return_value.last_season_year.data = 2

    kwargs = {
        'short_name': "L",
        'long_name': "League",
        'first_season_year': 1,
        'last_season_year': 2,
    }
    league = League(**kwargs)
    fake_league_factory.create_league.return_value = league

    err = IntegrityError('statement', 'params', Exception())
    fake_league_repository.add_league.side_effect = err

    # Act
    result = mod.create()

    # Assert
    fake_league_factory.create_league.assert_called_once_with(**kwargs)
    fake_league_repository.add_league.assert_called_once_with(league)
    fake_flash.assert_called_once_with(str(err), 'danger')
    fake_render_template.assert_called_once_with(
        'leagues/create.html', league=None, form=fake_new_league_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.league_controller.league_repository')
def test_edit_when_league_not_found_should_abort_with_404_error(fake_league_repository):
    # Arrange
    old_league = None
    fake_league_repository.get_league.return_value = old_league

    # Act
    with pytest.raises(NotFound):
        result = mod.edit(1)


@patch('app.flask.league_controller.render_template')
@patch('app.flask.league_controller.flash')
@patch('app.flask.league_controller.EditLeagueForm')
@patch('app.flask.league_controller.league_repository')
def test_edit_when_league_found_and_form_not_submitted_and_no_form_errors_should_render_edit_template(
        fake_league_repository, fake_edit_league_form, fake_flash, fake_render_template
):
    # Arrange
    old_league = League(
        short_name="L",
        long_name="League",
        first_season_year=1,
        last_season_year=2
    )
    fake_league_repository.get_league.return_value = old_league

    fake_edit_league_form.return_value.validate_on_submit.return_value = False
    fake_edit_league_form.return_value.errors = None

    # Act
    result = mod.edit(1)

    # Assert
    assert fake_edit_league_form.return_value.short_name.data == old_league.short_name
    assert fake_edit_league_form.return_value.long_name.data == old_league.long_name
    assert fake_edit_league_form.return_value.first_season_year.data == old_league.first_season_year
    assert fake_edit_league_form.return_value.last_season_year.data == old_league.last_season_year
    fake_flash.assert_not_called()
    fake_render_template.assert_called_once_with(
        'leagues/edit.html', league=old_league, form=fake_edit_league_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.league_controller.render_template')
@patch('app.flask.league_controller.flash')
@patch('app.flask.league_controller.EditLeagueForm')
@patch('app.flask.league_controller.league_repository')
def test_edit_when_league_found_and_form_not_submitted_and_form_errors_should_flash_errors_and_render_edit_template(
        fake_league_repository, fake_edit_league_form, fake_flash, fake_render_template
):
    # Arrange
    old_league = League(
        short_name="L",
        long_name="League",
        first_season_year=1,
        last_season_year=2
    )
    fake_league_repository.get_league.return_value = old_league

    fake_edit_league_form.return_value.validate_on_submit.return_value = False
    fake_edit_league_form.return_value.errors = None

    errors = 'errors'
    fake_edit_league_form.return_value.errors = errors

    # Act
    result = mod.edit(1)

    # Assert
    assert fake_edit_league_form.return_value.short_name.data == old_league.short_name
    assert fake_edit_league_form.return_value.long_name.data == old_league.long_name
    assert fake_edit_league_form.return_value.first_season_year.data == old_league.first_season_year
    assert fake_edit_league_form.return_value.last_season_year.data == old_league.last_season_year
    fake_flash.assert_called_once_with(f"{errors}", 'danger')
    fake_render_template.assert_called_once_with(
        'leagues/edit.html', league=old_league, form=fake_edit_league_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.league_controller.redirect')
@patch('app.flask.league_controller.url_for')
@patch('app.flask.league_controller.flash')
@patch('app.flask.league_controller.league_factory')
@patch('app.flask.league_controller.EditLeagueForm')
@patch('app.flask.league_controller.league_repository')
def test_edit_when_league_found_and_form_submitted_and_no_errors_caught_should_flash_success_message_and_redirect_to_league_details(
        fake_league_repository, fake_edit_league_form, fake_league_factory, fake_flash, fake_url_for,
        fake_redirect
):
    # Arrange
    id = 1

    old_league = League(
        id=id,
        short_name="L1",
        long_name="League 1",
        first_season_year=1,
        last_season_year=2
    )
    fake_league_repository.get_league.return_value = old_league

    fake_edit_league_form.return_value.validate_on_submit.return_value = True
    fake_edit_league_form.return_value.short_name.data = "L2"
    fake_edit_league_form.return_value.long_name.data = "League 2"
    fake_edit_league_form.return_value.first_season_year.data = 3
    fake_edit_league_form.return_value.last_season_year.data = 4

    kwargs = {
        'id': id,
        'short_name': "L2",
        'long_name': "League 2",
        'first_season_year': 3,
        'last_season_year': 4,
    }
    new_league = League(**kwargs)
    fake_league_factory.create_league.return_value = new_league

    # Act
    result = mod.edit(id)

    # Assert
    fake_league_factory.create_league.assert_called_once_with(**kwargs)
    fake_league_repository.update_league.assert_called_once_with(new_league)
    fake_flash.assert_called_once_with(
        f"Item {fake_edit_league_form.return_value.short_name.data} has been successfully updated.", 'success'
    )
    fake_url_for.assert_called_once_with('league.details', id=id)
    fake_redirect.assert_called_once_with(fake_url_for.return_value)
    assert result is fake_redirect.return_value


@patch('app.flask.league_controller.render_template')
@patch('app.flask.league_controller.flash')
@patch('app.flask.league_controller.league_factory')
@patch('app.flask.league_controller.EditLeagueForm')
@patch('app.flask.league_controller.league_repository')
def test_edit_when_league_found_and_form_submitted_and_value_error_caught_should_flash_error_message_and_render_edit_template(
        fake_league_repository, fake_edit_league_form, fake_league_factory, fake_flash,
        fake_render_template
):
    # Arrange
    id = 1

    old_league = League(
        id=id,
        short_name="L1",
        long_name="League 1",
        first_season_year=1,
        last_season_year=2
    )
    fake_league_repository.get_league.return_value = old_league

    fake_edit_league_form.return_value.validate_on_submit.return_value = True
    fake_edit_league_form.return_value.short_name.data = "L2"
    fake_edit_league_form.return_value.long_name.data = "League 2"
    fake_edit_league_form.return_value.first_season_year.data = 3
    fake_edit_league_form.return_value.last_season_year.data = 4

    kwargs = {
        'id': id,
        'short_name': "L2",
        'long_name': "League 2",
        'first_season_year': 3,
        'last_season_year': 4,
    }
    new_league = League(**kwargs)
    fake_league_factory.create_league.return_value = new_league

    err = ValueError()
    fake_league_repository.update_league.side_effect = err

    # Act
    result = mod.edit(id)

    # Assert
    fake_league_factory.create_league.assert_called_once_with(**kwargs)
    fake_league_repository.update_league.assert_called_once_with(new_league)
    fake_flash.assert_called_once_with(str(err), 'danger')
    fake_render_template.assert_called_once_with(
        'leagues/edit.html', league=old_league, form=fake_edit_league_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.league_controller.render_template')
@patch('app.flask.league_controller.flash')
@patch('app.flask.league_controller.league_factory')
@patch('app.flask.league_controller.EditLeagueForm')
@patch('app.flask.league_controller.league_repository')
def test_edit_when_league_found_and_form_submitted_and_integrity_error_caught_should_flash_error_message_and_render_edit_template(
        fake_league_repository, fake_edit_league_form, fake_league_factory, fake_flash,
        fake_render_template
):
    # Arrange
    id = 1

    old_league = League(
        id=id,
        short_name="L1",
        long_name="League 1",
        first_season_year=1,
        last_season_year=2
    )
    fake_league_repository.get_league.return_value = old_league

    fake_edit_league_form.return_value.validate_on_submit.return_value = True
    fake_edit_league_form.return_value.short_name.data = "L2"
    fake_edit_league_form.return_value.long_name.data = "League 2"
    fake_edit_league_form.return_value.first_season_year.data = 3
    fake_edit_league_form.return_value.last_season_year.data = 4

    kwargs = {
        'id': id,
        'short_name': "L2",
        'long_name': "League 2",
        'first_season_year': 3,
        'last_season_year': 4,
    }
    new_league = League(**kwargs)
    fake_league_factory.create_league.return_value = new_league

    err = IntegrityError('statement', 'params', Exception())
    fake_league_repository.update_league.side_effect = err

    # Act
    result = mod.edit(id)

    # Assert
    fake_league_factory.create_league.assert_called_once_with(**kwargs)
    fake_league_repository.update_league.assert_called_once_with(new_league)
    fake_flash.assert_called_once_with(str(err), 'danger')
    fake_render_template.assert_called_once_with(
        'leagues/edit.html', league=old_league, form=fake_edit_league_form.return_value
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
            result = mod.delete(1)

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
            result = mod.delete(id)

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
                result = mod.delete(1)
