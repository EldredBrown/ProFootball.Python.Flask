from unittest.mock import patch, Mock

import pytest

from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound

import app.flask.league_controller as mod

from app.data.models.league import League
from app.data.repositories.league_repository import LeagueRepository
from test_app import create_app


@pytest.fixture()
def test_app():
    return create_app()


@patch('app.flask.league_controller.render_template')
@patch('app.flask.league_controller.injector')
def test_index_should_render_league_index_template(fake_injector, fake_render_template):
    # Arrange
    fake_league_repository = Mock(LeagueRepository)
    fake_injector.get.return_value = fake_league_repository

    # Act
    result = mod.index()

    # Assert
    fake_injector.get.assert_called_once_with(LeagueRepository)
    fake_league_repository.get_leagues.assert_called_once()
    fake_render_template.assert_called_once_with(
        'leagues/index.html', leagues=fake_league_repository.get_leagues.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.league_controller.render_template')
@patch('app.flask.league_controller.injector')
@patch('app.flask.league_controller.DeleteLeagueForm')
def test_details_when_league_found_should_render_league_details_template(
        fake_delete_league_form, fake_injector, fake_render_template
):
    # Arrange
    id = 1

    fake_league_repository = Mock(LeagueRepository)
    fake_injector.get.return_value = fake_league_repository

    # Act
    result = mod.details(id)

    # Assert
    fake_delete_league_form.assert_called_once()
    fake_injector.get.assert_called_once_with(LeagueRepository)
    fake_league_repository.get_league.assert_called_once_with(id)
    fake_render_template.assert_called_once_with(
        'leagues/details.html',
        league=fake_league_repository.get_league.return_value,
        form=fake_delete_league_form.return_value
    )
    assert result == fake_render_template.return_value


@patch('app.flask.league_controller.injector')
@patch('app.flask.league_controller.DeleteLeagueForm')
def test_details_when_league_not_found_should_abort_with_404_error(fake_delete_league_form, fake_injector):
    # Arrange
    fake_league_repository = Mock(LeagueRepository)
    fake_league_repository.get_league.side_effect = IndexError()
    fake_injector.get.return_value = fake_league_repository

    # Act
    with pytest.raises(NotFound):
        result = mod.details(1)


@patch('app.flask.league_controller.render_template')
@patch('app.flask.league_controller.flash')
@patch('app.flask.league_controller.injector')
@patch('app.flask.league_controller.NewLeagueForm')
def test_create_when_form_not_submitted_and_no_form_errors_should_render_create_template(
        fake_new_league_form, fake_injector, fake_flash, fake_render_template
):
    # Arrange
    fake_new_league_form.return_value.validate_on_submit.return_value = False
    fake_new_league_form.return_value.errors = None

    fake_league_repository = Mock(LeagueRepository)
    fake_injector.get.return_value = fake_league_repository

    # Act
    result = mod.create()

    # Assert
    fake_injector.get.assert_not_called()
    fake_league_repository.add_league.assert_not_called()
    fake_flash.assert_not_called()
    fake_render_template('leagues/create.html', form=fake_new_league_form.return_value)
    assert result is fake_render_template.return_value


@patch('app.flask.league_controller.render_template')
@patch('app.flask.league_controller.flash')
@patch('app.flask.league_controller.injector')
@patch('app.flask.league_controller.NewLeagueForm')
def test_create_when_form_not_submitted_and_form_errors_should_flash_errors_and_render_create_template(
        fake_new_league_form, fake_injector, fake_flash, fake_render_template
):
    # Arrange
    fake_new_league_form.return_value.validate_on_submit.return_value = False

    errors = 'errors'
    fake_new_league_form.return_value.errors = errors

    fake_league_repository = Mock(LeagueRepository)
    fake_injector.get.return_value = fake_league_repository

    # Act
    result = mod.create()

    # Assert
    fake_injector.get.assert_not_called()
    fake_league_repository.add_league.assert_not_called()
    fake_flash.assert_called_once_with(f"{errors}", 'danger')
    fake_render_template('leagues/create.html', form=fake_new_league_form.return_value)
    assert result is fake_render_template.return_value


@patch('app.flask.league_controller.redirect')
@patch('app.flask.league_controller.url_for')
@patch('app.flask.league_controller.flash')
@patch('app.flask.league_controller.injector')
@patch('app.flask.league_controller.league_factory')
@patch('app.flask.league_controller.NewLeagueForm')
def test_create_when_form_submitted_and_no_errors_caught_should_flash_success_message_and_redirect_to_league_index(
        fake_new_league_form, fake_league_factory, fake_injector, fake_flash, fake_url_for, fake_redirect
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

    fake_league_repository = Mock(LeagueRepository)
    fake_injector.get.return_value = fake_league_repository

    # Act
    result = mod.create()

    # Assert
    fake_league_factory.create_league.assert_called_once_with(**kwargs)
    fake_injector.get.assert_called_once_with(LeagueRepository)
    fake_league_repository.add_league.assert_called_once_with(league)
    fake_flash(f"Item {league.short_name} has been successfully submitted.", 'success')
    fake_url_for.assert_called_once_with('league.index')
    fake_redirect.assert_called_once_with(fake_url_for.return_value)
    assert result is fake_redirect.return_value


@patch('app.flask.league_controller.render_template')
@patch('app.flask.league_controller.flash')
@patch('app.flask.league_controller.injector')
@patch('app.flask.league_controller.league_factory')
@patch('app.flask.league_controller.NewLeagueForm')
def test_create_when_form_submitted_and_value_error_caught_should_flash_error_message_and_render_create_template(
        fake_new_league_form, fake_league_factory, fake_injector, fake_flash, fake_render_template
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

    fake_league_repository = Mock(LeagueRepository)
    err = ValueError()
    fake_league_repository.add_league.side_effect = err
    fake_injector.get.return_value = fake_league_repository

    # Act
    result = mod.create()

    # Assert
    fake_league_factory.create_league.assert_called_once_with(**kwargs)
    fake_injector.get.assert_called_once_with(LeagueRepository)
    fake_league_repository.add_league.assert_called_once_with(league)
    fake_flash.assert_called_once_with(str(err), 'danger')
    fake_render_template.assert_called_once_with(
        'leagues/create.html', league=None, form=fake_new_league_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.league_controller.render_template')
@patch('app.flask.league_controller.flash')
@patch('app.flask.league_controller.injector')
@patch('app.flask.league_controller.league_factory')
@patch('app.flask.league_controller.NewLeagueForm')
def test_create_when_form_submitted_and_integrity_error_caught_should_flash_error_message_and_render_create_template(
        fake_new_league_form, fake_league_factory, fake_injector, fake_flash, fake_render_template
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

    fake_league_repository = Mock(LeagueRepository)
    err = IntegrityError('statement', 'params', Exception())
    fake_league_repository.add_league.side_effect = err
    fake_injector.get.return_value = fake_league_repository

    # Act
    result = mod.create()

    # Assert
    fake_league_factory.create_league.assert_called_once_with(**kwargs)
    fake_injector.get.assert_called_once_with(LeagueRepository)
    fake_league_repository.add_league.assert_called_once_with(league)
    fake_flash.assert_called_once_with(str(err), 'danger')
    fake_render_template.assert_called_once_with(
        'leagues/create.html', league=None, form=fake_new_league_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.league_controller.copy')
@patch('app.flask.league_controller.injector')
def test_edit_when_league_not_found_should_abort_with_404_error(fake_injector, fake_copy):
    # Arrange
    id = 1

    fake_league_repository = Mock(LeagueRepository)
    old_league = Mock(League)
    fake_league_repository.get_league.return_value = old_league
    fake_injector.get.return_value = fake_league_repository

    old_league_copy = None
    fake_copy.deepcopy.return_value = old_league_copy

    # Act
    with pytest.raises(NotFound):
        result = mod.edit(id)

    # Assert
    fake_injector.get.assert_called_once_with(LeagueRepository)
    fake_league_repository.get_league.assert_called_once_with(id)
    fake_copy.deepcopy.assert_called_once_with(old_league)


@patch('app.flask.league_controller.render_template')
@patch('app.flask.league_controller.flash')
@patch('app.flask.league_controller.EditLeagueForm')
@patch('app.flask.league_controller.copy')
@patch('app.flask.league_controller.injector')
def test_edit_when_league_found_and_form_not_submitted_and_no_form_errors_should_render_edit_template(
        fake_injector, fake_copy, fake_edit_league_form, fake_flash, fake_render_template
):
    # Arrange
    id = 1

    fake_league_repository = Mock(LeagueRepository)
    old_league = Mock(League)
    fake_league_repository.get_league.return_value = old_league
    fake_injector.get.return_value = fake_league_repository

    old_league_copy = Mock(League)
    old_league_copy.short_name = "L"
    old_league_copy.long_name = "League"
    old_league_copy.first_season_year = 1
    old_league_copy.last_season_year = 2
    fake_copy.deepcopy.return_value = old_league_copy

    fake_edit_league_form.return_value.validate_on_submit.return_value = False
    fake_edit_league_form.return_value.errors = None

    # Act
    result = mod.edit(id)

    # Assert
    fake_injector.get.assert_called_once_with(LeagueRepository)
    fake_league_repository.get_league.assert_called_once_with(id)
    fake_copy.deepcopy.assert_called_once_with(old_league)
    assert fake_edit_league_form.return_value.short_name.data == old_league_copy.short_name
    assert fake_edit_league_form.return_value.long_name.data == old_league_copy.long_name
    assert fake_edit_league_form.return_value.first_season_year.data == old_league_copy.first_season_year
    assert fake_edit_league_form.return_value.last_season_year.data == old_league_copy.last_season_year
    fake_flash.assert_not_called()
    fake_render_template.assert_called_once_with(
        'leagues/edit.html', league=old_league_copy, form=fake_edit_league_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.league_controller.render_template')
@patch('app.flask.league_controller.flash')
@patch('app.flask.league_controller.EditLeagueForm')
@patch('app.flask.league_controller.copy')
@patch('app.flask.league_controller.injector')
def test_edit_when_league_found_and_form_not_submitted_and_form_errors_should_flash_errors_and_render_edit_template(
        fake_injector, fake_copy, fake_edit_league_form, fake_flash, fake_render_template
):
    # Arrange
    id = 1

    fake_league_repository = Mock(LeagueRepository)
    old_league = Mock(League)
    fake_league_repository.get_league.return_value = old_league
    fake_injector.get.return_value = fake_league_repository

    fake_edit_league_form.return_value.validate_on_submit.return_value = False
    fake_edit_league_form.return_value.errors = None

    old_league_copy = Mock(League)
    old_league_copy.short_name = "L"
    old_league_copy.long_name = "League"
    old_league_copy.first_season_year = 1
    old_league_copy.last_season_year = 2
    fake_copy.deepcopy.return_value = old_league_copy

    errors = 'errors'
    fake_edit_league_form.return_value.errors = errors

    # Act
    result = mod.edit(id)

    # Assert
    fake_injector.get.assert_called_once_with(LeagueRepository)
    fake_league_repository.get_league.assert_called_once_with(id)
    fake_copy.deepcopy.assert_called_once_with(old_league)
    assert fake_edit_league_form.return_value.short_name.data == old_league_copy.short_name
    assert fake_edit_league_form.return_value.long_name.data == old_league_copy.long_name
    assert fake_edit_league_form.return_value.first_season_year.data == old_league_copy.first_season_year
    assert fake_edit_league_form.return_value.last_season_year.data == old_league_copy.last_season_year
    fake_flash.assert_called_once_with(f"{errors}", 'danger')
    fake_render_template.assert_called_once_with(
        'leagues/edit.html', league=old_league_copy, form=fake_edit_league_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.league_controller.redirect')
@patch('app.flask.league_controller.url_for')
@patch('app.flask.league_controller.flash')
@patch('app.flask.league_controller.league_factory')
@patch('app.flask.league_controller.EditLeagueForm')
@patch('app.flask.league_controller.copy')
@patch('app.flask.league_controller.injector')
def test_edit_when_league_found_and_form_submitted_and_no_errors_caught_should_flash_success_message_and_redirect_to_league_details(
        fake_injector, fake_copy, fake_edit_league_form, fake_league_factory, fake_flash, fake_url_for, fake_redirect
):
    # Arrange
    id = 1

    fake_league_repository = Mock(LeagueRepository)
    old_league = Mock(League)
    fake_league_repository.get_league.return_value = old_league
    fake_injector.get.return_value = fake_league_repository

    old_league_copy = Mock(League)
    old_league_copy.short_name = "L1"
    old_league_copy.long_name = "League 1"
    old_league_copy.first_season_year = 1
    old_league_copy.last_season_year = 2
    fake_copy.deepcopy.return_value = old_league_copy

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
    fake_injector.get.assert_called_once_with(LeagueRepository)
    fake_league_repository.get_league.assert_called_once_with(id)
    fake_copy.deepcopy.assert_called_once_with(old_league)
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
@patch('app.flask.league_controller.copy')
@patch('app.flask.league_controller.injector')
def test_edit_when_league_found_and_form_submitted_and_value_error_caught_should_flash_error_message_and_render_edit_template(
        fake_injector, fake_copy, fake_edit_league_form, fake_league_factory, fake_flash, fake_render_template
):
    # Arrange
    id = 1

    fake_league_repository = Mock(LeagueRepository)
    old_league = Mock(League)
    fake_league_repository.get_league.return_value = old_league
    err = ValueError()
    fake_league_repository.update_league.side_effect = err
    fake_injector.get.return_value = fake_league_repository

    old_league_copy = Mock(League)
    old_league_copy.short_name = "L1"
    old_league_copy.long_name = "League 1"
    old_league_copy.first_season_year = 1
    old_league_copy.last_season_year = 2
    fake_copy.deepcopy.return_value = old_league_copy

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
    fake_injector.get.assert_called_once_with(LeagueRepository)
    fake_league_repository.get_league.assert_called_once_with(id)
    fake_copy.deepcopy.assert_called_once_with(old_league)
    fake_league_factory.create_league.assert_called_once_with(**kwargs)
    fake_flash.assert_called_once_with(str(err), 'danger')
    fake_render_template.assert_called_once_with(
        'leagues/edit.html', league=old_league_copy, form=fake_edit_league_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.league_controller.render_template')
@patch('app.flask.league_controller.flash')
@patch('app.flask.league_controller.league_factory')
@patch('app.flask.league_controller.EditLeagueForm')
@patch('app.flask.league_controller.copy')
@patch('app.flask.league_controller.injector')
def test_edit_when_league_found_and_form_submitted_and_integrity_error_caught_should_flash_error_message_and_render_edit_template(
        fake_injector, fake_copy, fake_edit_league_form, fake_league_factory, fake_flash, fake_render_template
):
    # Arrange
    id = 1

    fake_league_repository = Mock(LeagueRepository)
    old_league = Mock(League)
    fake_league_repository.get_league.return_value = old_league
    err = IntegrityError('statement', 'params', Exception())
    fake_league_repository.update_league.side_effect = err
    fake_injector.get.return_value = fake_league_repository

    old_league_copy = Mock(League)
    old_league_copy.short_name = "L1"
    old_league_copy.long_name = "League 1"
    old_league_copy.first_season_year = 1
    old_league_copy.last_season_year = 2
    fake_copy.deepcopy.return_value = old_league_copy

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
    fake_injector.get.assert_called_once_with(LeagueRepository)
    fake_league_repository.get_league.assert_called_once_with(id)
    fake_copy.deepcopy.assert_called_once_with(old_league)
    fake_league_factory.create_league.assert_called_once_with(**kwargs)
    fake_flash.assert_called_once_with(str(err), 'danger')
    fake_render_template.assert_called_once_with(
        'leagues/edit.html', league=old_league_copy, form=fake_edit_league_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.league_controller.flash')
@patch('app.flask.league_controller.league_factory')
@patch('app.flask.league_controller.EditLeagueForm')
@patch('app.flask.league_controller.url_for')
@patch('app.flask.league_controller.redirect')
@patch('app.flask.league_controller.copy')
@patch('app.flask.league_controller.injector')
def test_edit_when_league_found_and_form_submitted_and_index_error_caught_should_abort_with_404_error(
        fake_injector, fake_copy, fake_redirect, fake_url_for, fake_edit_league_form, fake_league_factory, fake_flash
):
    # Arrange
    id = 1

    fake_league_repository = Mock(LeagueRepository)
    old_league = Mock(League)
    fake_league_repository.get_league.return_value = old_league
    fake_injector.get.return_value = fake_league_repository

    old_league_copy = Mock(League)
    old_league_copy.short_name = "L1"
    old_league_copy.long_name = "League 1"
    old_league_copy.first_season_year = 1
    old_league_copy.last_season_year = 2
    fake_copy.deepcopy.return_value = old_league_copy

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

    err = IndexError()
    fake_url_for.side_effect = err

    # Act
    with pytest.raises(NotFound):
        result = mod.edit(id)

    # Assert
    fake_injector.get.assert_called_once_with(LeagueRepository)
    fake_league_repository.get_league.assert_called_once_with(id)
    fake_copy.deepcopy.assert_called_once_with(old_league)
    fake_edit_league_form.assert_called_once()
    fake_edit_league_form.return_value.validate_on_submit.assert_called_once()
    fake_league_factory.create_league.assert_called_once_with(**kwargs)


@patch('app.flask.league_controller.injector')
def test_delete_when_league_not_found_should_abort_with_404_error(fake_injector, test_app):
    # Arrange
    id = 1

    fake_league_repository = Mock(LeagueRepository)
    fake_league_repository.get_league.return_value = None
    fake_injector.get.return_value = fake_league_repository

    # Act
    with test_app.test_request_context(
            f'/leagues/delete?id={id}',
            method='POST'
    ):
        with pytest.raises(NotFound):
            result = mod.delete(id)

    # Assert
    fake_injector.get.assert_called_once_with(LeagueRepository)
    fake_league_repository.get_league.assert_called_once_with(id)


@patch('app.flask.league_controller.render_template')
@patch('app.flask.league_controller.injector')
def test_delete_when_request_method_is_get_should_render_delete_template(fake_injector, fake_render_template, test_app):
    # Arrange
    id = 1

    fake_league_repository = Mock(LeagueRepository)
    league = League()
    fake_league_repository.get_league.return_value = league
    fake_injector.get.return_value = fake_league_repository

    # Act
    with test_app.test_request_context(
            f'/leagues/delete?id={id}',
            method='GET'
    ):
        result = mod.delete(id)

    # Assert
    fake_injector.get.assert_called_once_with(LeagueRepository)
    fake_league_repository.get_league.assert_called_once_with(id)
    fake_render_template.assert_called_once_with('leagues/delete.html', league=league)
    assert result is fake_render_template.return_value


@patch('app.flask.league_controller.redirect')
@patch('app.flask.league_controller.url_for')
@patch('app.flask.league_controller.flash')
@patch('app.flask.league_controller.injector')
def test_delete_when_request_method_is_post_and_league_found_should_flash_success_message_and_redirect_to_leagues_index(
        fake_injector, fake_flash, fake_url_for, fake_redirect, test_app
):
    # Arrange
    id = 1

    fake_league_repository = Mock(LeagueRepository)
    league = League()
    fake_league_repository.get_league.return_value = league
    fake_injector.get.return_value = fake_league_repository

    # Act
    with test_app.test_request_context(
            '/leagues/delete?id=1',
            method='POST'
    ):
        result = mod.delete(id)

    # Assert
    fake_injector.get.assert_called_once_with(LeagueRepository)
    fake_league_repository.get_league.assert_called_once_with(id)
    fake_league_repository.delete_league.assert_called_once_with(id)
    fake_flash.assert_called_once_with(f"League {league.short_name} has been successfully deleted.", 'success')
    fake_url_for.assert_called_once_with('league.index')
    fake_redirect.assert_called_once_with(fake_url_for.return_value)
    assert result is fake_redirect.return_value


@patch('app.flask.league_controller.injector')
def test_delete_when_request_method_is_post_and_index_error_is_caught_should_abort_with_404_error(
        fake_injector, test_app
):
    # Arrange
    id = 1

    fake_league_repository = Mock(LeagueRepository)
    league = League()
    fake_league_repository.get_league.return_value = league
    fake_league_repository.delete_league.side_effect = IndexError()
    fake_injector.get.return_value = fake_league_repository

    # Act
    with test_app.test_request_context(
            f'/leagues/delete?id={id}',
            method='POST'
    ):
        with pytest.raises(NotFound):
            result = mod.delete(id)

    # Assert
    fake_injector.get.assert_called_once_with(LeagueRepository)
    fake_league_repository.get_league.assert_called_once_with(id)
