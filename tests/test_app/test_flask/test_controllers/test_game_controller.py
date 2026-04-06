from unittest.mock import patch, Mock, call

import pytest
from flask import session

from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound

import app.flask.game_controller as mod

from app.data.models.season import Season
from app.data.models.game import Game
from app.data.repositories.game_repository import GameRepository
from app.data.repositories.season_repository import SeasonRepository
from app.services.game_service.game_service import GameService

from test_app import create_app


@pytest.fixture()
def test_app():
    return create_app()


@patch('app.flask.game_controller.render_template')
@patch('app.flask.game_controller.injector')
def test_index_should_render_game_index_template(fake_injector, fake_render_template, test_app):
    # Arrange
    fake_season_repository = Mock(SeasonRepository)
    fake_game_repository = Mock(GameRepository)
    fake_injector.get.side_effect = [fake_season_repository, fake_game_repository]

    seasons = []
    selected_season = 1
    selected_week = 1

    with test_app.test_request_context(
            '/games/',
            method='GET'
    ):
        # Act
        session['seasons'] = seasons
        session['selected_season'] = selected_season
        session['selected_week'] = selected_week

        result = mod.index()

        # Assert
        fake_injector.get.assert_has_calls([
            call(SeasonRepository),
            call(GameRepository),
        ])
        fake_season_repository.get_seasons.assert_called_once()
        fake_game_repository.get_games_by_season_year.assert_called_once_with(season_year=None)
        fake_render_template.assert_called_once_with(
            'games/index.html',
            seasons=fake_season_repository.get_seasons.return_value, selected_season=selected_season,
            selected_week=selected_week, games=fake_game_repository.get_games_by_season_year.return_value
        )
        assert result is fake_render_template.return_value


@patch('app.flask.game_controller.render_template')
@patch('app.flask.game_controller.injector')
@patch('app.flask.game_controller.DeleteGameForm')
def test_details_when_game_found_should_render_game_details_template(
        fake_delete_game_form, fake_injector, fake_render_template
):
    # Arrange
    id = 1

    fake_game_repository = Mock(GameRepository)
    fake_injector.get.return_value = fake_game_repository

    # Act
    result = mod.details(id)

    # Assert
    fake_delete_game_form.assert_called_once()
    fake_injector.get.assert_called_once_with(GameRepository)
    fake_game_repository.get_game.assert_called_once_with(id)
    fake_render_template.assert_called_once_with(
        'games/details.html',
        game=fake_game_repository.get_game.return_value,
        form=fake_delete_game_form.return_value
    )
    assert result == fake_render_template.return_value


@patch('app.flask.game_controller.injector')
@patch('app.flask.game_controller.DeleteGameForm')
def test_details_when_game_not_found_should_abort_with_404_error(fake_delete_game_form, fake_injector):
    # Arrange
    fake_game_repository = Mock(GameRepository)
    fake_game_repository.get_game.side_effect = IndexError()
    fake_injector.get.return_value = fake_game_repository

    # Act
    with pytest.raises(NotFound):
        result = mod.details(1)


@patch('app.flask.game_controller.render_template')
@patch('app.flask.game_controller.flash')
@patch('app.flask.game_controller.injector')
@patch('app.flask.game_controller.NewGameForm')
def test_create_when_form_not_submitted_and_selected_season_year_is_less_than_1920_and_no_form_errors_should_render_create_template(
        fake_new_game_form, fake_injector, fake_flash, fake_render_template, test_app
):
    # Arrange
    fake_new_game_form.return_value.validate_on_submit.return_value = False
    fake_new_game_form.return_value.errors = None

    fake_game_service = Mock(GameService)
    fake_injector.get.return_value = fake_game_service

    # Act
    with test_app.test_request_context(
            '/games/create',
            method='GET'
    ):
        session['selected_season'] = Season(year=1919)
        result = mod.create()

    # Assert
    fake_new_game_form.assert_called_once()
    assert fake_new_game_form.return_value.season_year.data == 0
    fake_new_game_form.return_value.validate_on_submit.assert_called_once()
    fake_injector.get.assert_not_called()
    fake_game_service.add_game.assert_not_called()
    fake_flash.assert_not_called()
    fake_render_template('games/create.html', form=fake_new_game_form.return_value)
    assert result is fake_render_template.return_value


@patch('app.flask.game_controller.render_template')
@patch('app.flask.game_controller.flash')
@patch('app.flask.game_controller.injector')
@patch('app.flask.game_controller.NewGameForm')
def test_create_when_form_not_submitted_and_selected_season_year_is_equal_to_1920_and_no_form_errors_should_render_create_template(
        fake_new_game_form, fake_injector, fake_flash, fake_render_template, test_app
):
    # Arrange
    fake_new_game_form.return_value.validate_on_submit.return_value = False
    fake_new_game_form.return_value.errors = None

    fake_game_service = Mock(GameService)
    fake_injector.get.return_value = fake_game_service

    # Act
    with test_app.test_request_context(
            '/games/create',
            method='GET'
    ):
        session['selected_season'] = Season(year=1920)
        result = mod.create()

    # Assert
    fake_new_game_form.assert_called_once()
    assert fake_new_game_form.return_value.season_year.data == 1920
    fake_new_game_form.return_value.validate_on_submit.assert_called_once()
    fake_injector.get.assert_not_called()
    fake_game_service.add_game.assert_not_called()
    fake_flash.assert_not_called()
    fake_render_template('games/create.html', form=fake_new_game_form.return_value)
    assert result is fake_render_template.return_value


@patch('app.flask.game_controller.render_template')
@patch('app.flask.game_controller.flash')
@patch('app.flask.game_controller.injector')
@patch('app.flask.game_controller.NewGameForm')
def test_create_when_form_not_submitted_and_selected_season_year_is_greater_than_1920_and_no_form_errors_should_render_create_template(
        fake_new_game_form, fake_injector, fake_flash, fake_render_template, test_app
):
    # Arrange
    fake_new_game_form.return_value.validate_on_submit.return_value = False
    fake_new_game_form.return_value.errors = None

    fake_game_service = Mock(GameService)
    fake_injector.get.return_value = fake_game_service

    # Act
    with test_app.test_request_context(
            '/games/create',
            method='GET'
    ):
        session['selected_season'] = Season(year=1921)
        result = mod.create()

    # Assert
    fake_new_game_form.assert_called_once()
    assert fake_new_game_form.return_value.season_year.data == 1921
    fake_new_game_form.return_value.validate_on_submit.assert_called_once()
    fake_injector.get.assert_not_called()
    fake_game_service.add_game.assert_not_called()
    fake_flash.assert_not_called()
    fake_render_template('games/create.html', form=fake_new_game_form.return_value)
    assert result is fake_render_template.return_value


@patch('app.flask.game_controller.render_template')
@patch('app.flask.game_controller.flash')
@patch('app.flask.game_controller.injector')
@patch('app.flask.game_controller.NewGameForm')
def test_create_when_form_not_submitted_and_form_errors_should_flash_errors_and_render_create_template(
        fake_new_game_form, fake_injector, fake_flash, fake_render_template, test_app
):
    # Arrange
    fake_new_game_form.return_value.validate_on_submit.return_value = False

    errors = 'errors'
    fake_new_game_form.return_value.errors = errors

    fake_game_service = Mock(GameService)
    fake_injector.get.return_value = fake_game_service

    # Act
    with test_app.test_request_context(
            '/games/create',
            method='GET'
    ):
        session['selected_season'] = Season(year=1921)
        result = mod.create()

    # Assert
    fake_new_game_form.assert_called_once()
    fake_new_game_form.return_value.validate_on_submit.assert_called_once()
    fake_injector.get.assert_not_called()
    fake_game_service.add_game.assert_not_called()
    fake_flash.assert_called_once_with(f"{errors}", 'danger')
    fake_render_template('games/create.html', form=fake_new_game_form.return_value)
    assert result is fake_render_template.return_value


@patch('app.flask.game_controller.url_for')
@patch('app.flask.game_controller.redirect')
@patch('app.flask.game_controller.flash')
@patch('app.flask.game_controller.injector')
@patch('app.flask.game_controller.game_factory')
@patch('app.flask.game_controller.NewGameForm')
def test_create_when_form_submitted_and_no_errors_caught_should_flash_success_message_and_redirect_to_game_index(
        fake_new_game_form, fake_game_factory, fake_injector, fake_flash, fake_redirect, fake_url_for, test_app
):
    # Arrange
    fake_new_game_form.return_value.validate_on_submit.return_value = True
    fake_new_game_form.return_value.season_year.data = 1
    fake_new_game_form.return_value.week.data = 1
    fake_new_game_form.return_value.guest_name.data = "Guest"
    fake_new_game_form.return_value.guest_score.data = 2
    fake_new_game_form.return_value.host_name.data = "Host"
    fake_new_game_form.return_value.host_score.data = 3
    fake_new_game_form.return_value.is_playoff.data = False
    fake_new_game_form.return_value.notes.data = None

    kwargs = {
        'season_year': 0,
        'week': 1,
        'guest_name': "Guest",
        'guest_score': 2,
        'host_name': "Host",
        'host_score': 3,
        'is_playoff': False,
        'notes': None,
    }

    fake_game_service = Mock(GameService)
    fake_injector.get.return_value = fake_game_service

    # Act
    with test_app.test_request_context(
            '/games/create',
            method='GET'
    ):
        session['selected_season'] = Season(year=0)
        result = mod.create()

    # Assert
    fake_new_game_form.assert_called_once()
    fake_new_game_form.return_value.validate_on_submit.assert_called_once()
    fake_game_factory.create_game.assert_called_once_with(**kwargs)
    fake_injector.get.assert_called_once_with(GameService)
    fake_game_service.add_game.assert_called_once_with(fake_game_factory.create_game.return_value)
    fake_flash(f"Game for season={kwargs['season_year']} with guest={kwargs['guest_name']} and host={kwargs['host_name']} has been successfully submitted.", 'success')
    fake_url_for.assert_called_once_with('game.index')
    fake_redirect.assert_called_once_with(fake_url_for.return_value)
    assert result is fake_redirect.return_value


@patch('app.flask.game_controller.render_template')
@patch('app.flask.game_controller.flash')
@patch('app.flask.game_controller.injector')
@patch('app.flask.game_controller.game_factory')
@patch('app.flask.game_controller.NewGameForm')
def test_create_when_form_submitted_and_value_error_caught_should_flash_error_message_and_render_create_template(
        fake_new_game_form, fake_game_factory, fake_injector, fake_flash, fake_render_template, test_app
):
    # Arrange
    fake_new_game_form.return_value.validate_on_submit.return_value = True
    fake_new_game_form.return_value.season_year.data = 1
    fake_new_game_form.return_value.week.data = 1
    fake_new_game_form.return_value.guest_name.data = "Guest"
    fake_new_game_form.return_value.guest_score.data = 2
    fake_new_game_form.return_value.host_name.data = "Host"
    fake_new_game_form.return_value.host_score.data = 3
    fake_new_game_form.return_value.is_playoff.data = False
    fake_new_game_form.return_value.notes.data = None

    kwargs = {
        'season_year': 0,
        'week': 1,
        'guest_name': "Guest",
        'guest_score': 2,
        'host_name': "Host",
        'host_score': 3,
        'is_playoff': False,
        'notes': None,
    }

    fake_game_service = Mock(GameService)
    err = ValueError()
    fake_game_service.add_game.side_effect = err
    fake_injector.get.return_value = fake_game_service

    # Act
    with test_app.test_request_context(
            '/games/create',
            method='GET'
    ):
        session['selected_season'] = Season(year=0)
        result = mod.create()

    # Assert
    fake_new_game_form.assert_called_once()
    fake_new_game_form.return_value.validate_on_submit.assert_called_once()
    fake_game_factory.create_game.assert_called_once_with(**kwargs)
    fake_injector.get.assert_called_once_with(GameService)
    fake_game_service.add_game.assert_called_once_with(fake_game_factory.create_game.return_value)
    fake_flash.assert_called_once_with(str(err), 'danger')
    fake_render_template.assert_called_once_with(
        'games/create.html', game=None, form=fake_new_game_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.game_controller.render_template')
@patch('app.flask.game_controller.flash')
@patch('app.flask.game_controller.injector')
@patch('app.flask.game_controller.game_factory')
@patch('app.flask.game_controller.NewGameForm')
def test_create_when_form_submitted_and_integrity_error_caught_should_flash_error_message_and_render_create_template(
        fake_new_game_form, fake_game_factory, fake_injector, fake_flash, fake_render_template, test_app
):
    # Arrange
    fake_new_game_form.return_value.validate_on_submit.return_value = True
    fake_new_game_form.return_value.season_year.data = 1
    fake_new_game_form.return_value.week.data = 1
    fake_new_game_form.return_value.guest_name.data = "Guest"
    fake_new_game_form.return_value.guest_score.data = 2
    fake_new_game_form.return_value.host_name.data = "Host"
    fake_new_game_form.return_value.host_score.data = 3
    fake_new_game_form.return_value.is_playoff.data = False
    fake_new_game_form.return_value.notes.data = None

    kwargs = {
        'season_year': 0,
        'week': 1,
        'guest_name': "Guest",
        'guest_score': 2,
        'host_name': "Host",
        'host_score': 3,
        'is_playoff': False,
        'notes': None,
    }

    fake_game_service = Mock(GameService)
    err = IntegrityError('statement', 'params', Exception())
    fake_game_service.add_game.side_effect = err
    fake_injector.get.return_value = fake_game_service

    # Act
    with test_app.test_request_context(
            '/games/create',
            method='GET'
    ):
        session['selected_season'] = Season(year=0)
        result = mod.create()

    # Assert
    fake_new_game_form.assert_called_once()
    fake_new_game_form.return_value.validate_on_submit.assert_called_once()
    fake_game_factory.create_game.assert_called_once_with(**kwargs)
    fake_injector.get.assert_called_once_with(GameService)
    fake_game_service.add_game.assert_called_once_with(fake_game_factory.create_game.return_value)
    fake_flash.assert_called_once_with(str(err), 'danger')
    fake_render_template.assert_called_once_with(
        'games/create.html', game=None, form=fake_new_game_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.game_controller.injector')
def test_edit_when_game_not_found_should_abort_with_404_error(fake_injector):
    # Arrange
    fake_game_repository = Mock(GameRepository)
    game = None
    fake_game_repository.get_game.return_value = game

    fake_game_service = Mock(GameService)
    fake_injector.get.side_effect = [fake_game_repository, fake_game_service]

    # Act
    with pytest.raises(NotFound):
        result = mod.edit(1)

    # Assert
    fake_injector.get.assert_called_once_with(GameRepository)
    fake_game_repository.get_game.assert_called_once()
    fake_game_service.update_game.assert_not_called()


@patch('app.flask.game_controller.render_template')
@patch('app.flask.game_controller.flash')
@patch('app.flask.game_controller.EditGameForm')
@patch('app.flask.game_controller.injector')
def test_edit_when_game_found_and_form_not_submitted_and_no_form_errors_should_render_edit_template(
        fake_injector, fake_edit_game_form, fake_flash, fake_render_template
):
    # Arrange
    fake_game_repository = Mock(GameRepository)
    game = Game(
        season_year=1,
        week=1,
        guest_name="Guest",
        guest_score=2,
        host_name="Host",
        host_score=3,
        is_playoff=False,
        notes=None
    )
    fake_game_repository.get_game.return_value = game

    fake_game_service = Mock(GameService)
    fake_injector.get.side_effect = [fake_game_repository, fake_game_service]

    fake_edit_game_form.return_value.validate_on_submit.return_value = False
    fake_edit_game_form.return_value.errors = None

    # Act
    result = mod.edit(1)

    # Assert
    fake_injector.get.assert_called_once_with(GameRepository)
    fake_game_repository.get_game.assert_called_once()
    fake_edit_game_form.assert_called_once()
    fake_edit_game_form.return_value.validate_on_submit.assert_called_once()
    fake_game_service.update_game.assert_not_called()
    assert fake_edit_game_form.return_value.season_year.data == game.season_year
    assert fake_edit_game_form.return_value.week.data == game.week
    assert fake_edit_game_form.return_value.guest_name.data == game.guest_name
    assert fake_edit_game_form.return_value.guest_score.data == game.guest_score
    assert fake_edit_game_form.return_value.host_name.data == game.host_name
    assert fake_edit_game_form.return_value.host_score.data == game.host_score
    assert fake_edit_game_form.return_value.is_playoff.data == game.is_playoff
    assert fake_edit_game_form.return_value.notes.data == game.notes
    fake_flash.assert_not_called()
    fake_render_template.assert_called_once_with(
        'games/edit.html', game=game, form=fake_edit_game_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.game_controller.render_template')
@patch('app.flask.game_controller.flash')
@patch('app.flask.game_controller.EditGameForm')
@patch('app.flask.game_controller.injector')
def test_edit_when_game_found_and_form_not_submitted_and_form_errors_should_flash_errors_and_render_edit_template(
        fake_injector, fake_edit_game_form, fake_flash, fake_render_template
):
    # Arrange
    fake_game_repository = Mock(GameRepository)
    game = Game(
        season_year=1,
        week=1,
        guest_name="Guest",
        guest_score=2,
        host_name="Host",
        host_score=3,
        is_playoff=False,
        notes=None
    )
    fake_game_repository.get_game.return_value = game

    fake_game_service = Mock(GameService)
    fake_injector.get.side_effect = [fake_game_repository, fake_game_service]

    fake_edit_game_form.return_value.validate_on_submit.return_value = False
    fake_edit_game_form.return_value.errors = None

    errors = 'errors'
    fake_edit_game_form.return_value.errors = errors

    # Act
    result = mod.edit(1)

    # Assert
    fake_injector.get.assert_called_once_with(GameRepository)
    fake_game_repository.get_game.assert_called_once()
    fake_edit_game_form.assert_called_once()
    fake_edit_game_form.return_value.validate_on_submit.assert_called_once()
    fake_game_service.update_game.assert_not_called()
    assert fake_edit_game_form.return_value.season_year.data == game.season_year
    assert fake_edit_game_form.return_value.week.data == game.week
    assert fake_edit_game_form.return_value.guest_name.data == game.guest_name
    assert fake_edit_game_form.return_value.guest_score.data == game.guest_score
    assert fake_edit_game_form.return_value.host_name.data == game.host_name
    assert fake_edit_game_form.return_value.host_score.data == game.host_score
    assert fake_edit_game_form.return_value.is_playoff.data == game.is_playoff
    assert fake_edit_game_form.return_value.notes.data == game.notes
    fake_flash.assert_called_once_with(f"{errors}", 'danger')
    fake_render_template.assert_called_once_with(
        'games/edit.html', game=game, form=fake_edit_game_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.game_controller.url_for')
@patch('app.flask.game_controller.redirect')
@patch('app.flask.game_controller.flash')
@patch('app.flask.game_controller.game_factory')
@patch('app.flask.game_controller.EditGameForm')
@patch('app.flask.game_controller.injector')
def test_edit_when_game_found_and_form_submitted_and_no_errors_caught_should_flash_success_message_and_redirect_to_game_details(
        fake_injector, fake_edit_game_form, fake_game_factory, fake_flash, fake_redirect, fake_url_for
):
    # Arrange
    id = 1

    fake_game_repository = Mock(GameRepository)
    old_game = Game(
        id=id,
        season_year=1,
        week=1,
        guest_name="Guest 1",
        guest_score=2,
        host_name="Host 1",
        host_score=3,
        is_playoff=False,
        notes=None
    )
    fake_game_repository.get_game.return_value = old_game

    fake_game_service = Mock(GameService)
    fake_injector.get.side_effect = [fake_game_repository, fake_game_service]

    fake_edit_game_form.return_value.validate_on_submit.return_value = True
    fake_edit_game_form.return_value.season_year.data = 2
    fake_edit_game_form.return_value.week.data = 2
    fake_edit_game_form.return_value.guest_name.data = "Guest 2"
    fake_edit_game_form.return_value.guest_score.data = 3
    fake_edit_game_form.return_value.host_name.data = "Host 2"
    fake_edit_game_form.return_value.host_score.data = 2
    fake_edit_game_form.return_value.is_playoff.data = True
    fake_edit_game_form.return_value.notes.data = "Notes"

    kwargs = {
        'id': id,
        'season_year': 2,
        'week': 2,
        'guest_name': "Guest 2",
        'guest_score': 3,
        'host_name': "Host 2",
        'host_score': 2,
        'is_playoff': True,
        'notes': "Notes",
    }

    # Act
    result = mod.edit(id)

    # Assert
    fake_injector.get.assert_has_calls([
        call(GameRepository),
        call(GameService),
    ])
    fake_game_repository.get_game.assert_called_once()
    fake_edit_game_form.assert_called_once()
    fake_edit_game_form.return_value.validate_on_submit.assert_called_once()
    fake_game_factory.create_game.assert_called_once_with(**kwargs)
    fake_game_service.update_game.assert_called_once_with(fake_game_factory.create_game.return_value, old_game)
    fake_flash.assert_called_once_with(
        f"Game for season={fake_edit_game_form.return_value.season_year.data} with guest={fake_edit_game_form.return_value.guest_name.data} and host={fake_edit_game_form.return_value.host_name.data} has been successfully updated.",
        'success'
    )
    fake_url_for.assert_called_once_with('game.details', id=id)
    fake_redirect.assert_called_once_with(fake_url_for.return_value)
    assert result is fake_redirect.return_value


@patch('app.flask.game_controller.render_template')
@patch('app.flask.game_controller.flash')
@patch('app.flask.game_controller.game_factory')
@patch('app.flask.game_controller.EditGameForm')
@patch('app.flask.game_controller.injector')
def test_edit_when_game_found_and_form_submitted_and_value_error_caught_should_flash_error_message_and_render_edit_template(
        fake_injector, fake_edit_game_form, fake_game_factory, fake_flash, fake_render_template
):
    # Arrange
    id = 1

    fake_game_repository = Mock(GameRepository)
    old_game = Game(
        id=id,
        season_year=1,
        week=1,
        guest_name="Guest 1",
        guest_score=2,
        host_name="Host 1",
        host_score=3,
        is_playoff=False,
        notes=None
    )
    fake_game_repository.get_game.return_value = old_game

    fake_game_service = Mock(GameService)
    fake_injector.get.side_effect = [fake_game_repository, fake_game_service]

    fake_edit_game_form.return_value.validate_on_submit.return_value = True
    fake_edit_game_form.return_value.season_year.data = 2
    fake_edit_game_form.return_value.week.data = 2
    fake_edit_game_form.return_value.guest_name.data = "Guest 2"
    fake_edit_game_form.return_value.guest_score.data = 3
    fake_edit_game_form.return_value.host_name.data = "Host 2"
    fake_edit_game_form.return_value.host_score.data = 2
    fake_edit_game_form.return_value.is_playoff.data = True
    fake_edit_game_form.return_value.notes.data = "Notes"

    kwargs = {
        'id': id,
        'season_year': 2,
        'week': 2,
        'guest_name': "Guest 2",
        'guest_score': 3,
        'host_name': "Host 2",
        'host_score': 2,
        'is_playoff': True,
        'notes': "Notes",
    }

    err = ValueError()
    fake_game_service.update_game.side_effect = err

    # Act
    result = mod.edit(id)

    # Assert
    fake_injector.get.assert_has_calls([
        call(GameRepository),
        call(GameService),
    ])
    fake_game_repository.get_game.assert_called_once()
    fake_edit_game_form.assert_called_once()
    fake_edit_game_form.return_value.validate_on_submit.assert_called_once()
    fake_game_factory.create_game.assert_called_once_with(**kwargs)
    fake_flash.assert_called_once_with(str(err), 'danger')
    fake_render_template.assert_called_once_with(
        'games/edit.html', game=old_game, form=fake_edit_game_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.game_controller.render_template')
@patch('app.flask.game_controller.flash')
@patch('app.flask.game_controller.game_factory')
@patch('app.flask.game_controller.EditGameForm')
@patch('app.flask.game_controller.injector')
def test_edit_when_game_found_and_form_submitted_and_integrity_error_caught_should_flash_error_message_and_render_edit_template(
        fake_injector, fake_edit_game_form, fake_game_factory, fake_flash, fake_render_template
):
    # Arrange
    id = 1

    fake_game_repository = Mock(GameRepository)
    old_game = Game(
        id=id,
        season_year=1,
        week=1,
        guest_name="Guest 1",
        guest_score=2,
        host_name="Host 1",
        host_score=3,
        is_playoff=False,
        notes=None
    )
    fake_game_repository.get_game.return_value = old_game

    fake_game_service = Mock(GameService)
    err = IntegrityError('statement', 'params', Exception())
    fake_game_service.update_game.side_effect = err
    fake_injector.get.side_effect = [fake_game_repository, fake_game_service]

    fake_edit_game_form.return_value.validate_on_submit.return_value = True
    fake_edit_game_form.return_value.season_year.data = 2
    fake_edit_game_form.return_value.week.data = 2
    fake_edit_game_form.return_value.guest_name.data = "Guest 2"
    fake_edit_game_form.return_value.guest_score.data = 3
    fake_edit_game_form.return_value.host_name.data = "Host 2"
    fake_edit_game_form.return_value.host_score.data = 2
    fake_edit_game_form.return_value.is_playoff.data = True
    fake_edit_game_form.return_value.notes.data = "Notes"

    kwargs = {
        'id': id,
        'season_year': 2,
        'week': 2,
        'guest_name': "Guest 2",
        'guest_score': 3,
        'host_name': "Host 2",
        'host_score': 2,
        'is_playoff': True,
        'notes': "Notes",
    }

    # Act
    result = mod.edit(id)

    # Assert
    fake_injector.get.assert_has_calls([
        call(GameRepository),
        call(GameService),
    ])
    fake_game_repository.get_game.assert_called_once()
    fake_edit_game_form.assert_called_once()
    fake_edit_game_form.return_value.validate_on_submit.assert_called_once()
    fake_game_factory.create_game.assert_called_once_with(**kwargs)
    fake_flash.assert_called_once_with(str(err), 'danger')
    fake_render_template.assert_called_once_with(
        'games/edit.html', game=old_game, form=fake_edit_game_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.game_controller.render_template')
@patch('app.flask.game_controller.flash')
@patch('app.flask.game_controller.game_factory')
@patch('app.flask.game_controller.EditGameForm')
@patch('app.flask.game_controller.url_for')
@patch('app.flask.game_controller.redirect')
@patch('app.flask.game_controller.injector')
def test_edit_when_game_found_and_form_submitted_and_index_error_caught_should_abort_with_404_error(
        fake_injector, fake_redirect, fake_url_for, fake_edit_game_form, fake_game_factory, fake_flash,
        fake_render_template
):
    # Arrange
    id = 1

    fake_game_repository = Mock(GameRepository)
    old_game = Game(
        id=id,
        season_year=1,
        week=1,
        guest_name="Guest 1",
        guest_score=2,
        host_name="Host 1",
        host_score=3,
        is_playoff=False,
        notes=None
    )
    fake_game_repository.get_game.return_value = old_game

    fake_game_service = Mock(GameService)
    fake_injector.get.side_effect = [fake_game_repository, fake_game_service]

    fake_edit_game_form.return_value.validate_on_submit.return_value = True
    fake_edit_game_form.return_value.season_year.data = 2
    fake_edit_game_form.return_value.week.data = 2
    fake_edit_game_form.return_value.guest_name.data = "Guest 2"
    fake_edit_game_form.return_value.guest_score.data = 3
    fake_edit_game_form.return_value.host_name.data = "Host 2"
    fake_edit_game_form.return_value.host_score.data = 2
    fake_edit_game_form.return_value.is_playoff.data = True
    fake_edit_game_form.return_value.notes.data = "Notes"

    kwargs = {
        'id': id,
        'season_year': 2,
        'week': 2,
        'guest_name': "Guest 2",
        'guest_score': 3,
        'host_name': "Host 2",
        'host_score': 2,
        'is_playoff': True,
        'notes': "Notes",
    }

    err = IndexError()
    fake_url_for.side_effect = err

    # Act
    with pytest.raises(NotFound):
        result = mod.edit(1)

    # Assert
    fake_injector.get.assert_has_calls([
        call(GameRepository),
        call(GameService),
    ])
    fake_game_repository.get_game.assert_called_once_with(id)
    fake_edit_game_form.assert_called_once()
    fake_edit_game_form.return_value.validate_on_submit.assert_called_once()
    fake_game_factory.create_game.assert_called_once_with(**kwargs)


@patch('app.flask.game_controller.injector')
def test_delete_when_game_not_found_should_abort_with_404_error(fake_injector, test_app):
    # Arrange
    id = 1

    fake_game_repository = Mock(GameRepository)
    fake_game_repository.get_game.return_value = None

    fake_game_service = Mock(GameService)
    fake_injector.get.side_effect = [fake_game_repository, fake_game_service]

    # Act
    with test_app.test_request_context(
            f'/games/delete?id={id}',
            method='POST'
    ):
        with pytest.raises(NotFound):
            result = mod.delete(id)

    # Assert
    fake_injector.get.assert_called_once_with(GameRepository)
    fake_game_repository.get_game.assert_called_once_with(id)
    fake_game_service.delete_game.assert_not_called()


@patch('app.flask.game_controller.render_template')
@patch('app.flask.game_controller.injector')
def test_delete_when_request_method_is_get_should_render_delete_template(fake_injector, fake_render_template, test_app):
    # Arrange
    id = 1

    fake_game_repository = Mock(GameRepository)
    game = Game(
        season_year=1,
        week=1,
        guest_name="Guest",
        guest_score=2,
        host_name="Host",
        host_score=3
    )
    fake_game_repository.get_game.return_value = game

    fake_game_service = Mock(GameService)
    fake_injector.get.side_effect = [fake_game_repository, fake_game_service]

    # Act
    with test_app.test_request_context(
            f'/games/delete?id={id}',
            method='GET'
    ):
        result = mod.delete(id)

    # Assert
    fake_injector.get.assert_called_once_with(GameRepository)
    fake_game_repository.get_game.assert_called_once_with(id)
    fake_game_service.delete_game.assert_not_called()
    fake_render_template.assert_called_once_with('games/delete.html', game=game)
    assert result is fake_render_template.return_value


@patch('app.flask.game_controller.redirect')
@patch('app.flask.game_controller.url_for')
@patch('app.flask.game_controller.flash')
@patch('app.flask.game_controller.injector')
def test_delete_when_request_method_is_post_and_game_found_should_delete_game_and_flash_success_message_and_redirect_to_games_index(
        fake_injector, fake_flash, fake_url_for, fake_redirect, test_app
):
    # Arrange
    id = 1

    fake_game_repository = Mock(GameRepository)
    game = Game(
        season_year=1,
        week=1,
        guest_name="Guest",
        guest_score=2,
        host_name="Host",
        host_score=3
    )
    fake_game_repository.get_game.return_value = game

    fake_game_service = Mock(GameService)
    fake_injector.get.side_effect = [fake_game_repository, fake_game_service]

    # Act
    with test_app.test_request_context(
            '/games/delete?id=1',
            method='POST'
    ):
        result = mod.delete(id)

    # Assert
    fake_injector.get.assert_has_calls([
        call(GameRepository),
        call(GameService),
    ])
    fake_game_repository.get_game.assert_called_once_with(id)
    fake_game_service.delete_game.assert_called_once_with(id)
    fake_flash.assert_called_once_with(
        f"Game for season={game.season_year} with guest={game.guest_name} and host={game.host_name} has been successfully deleted.",
        'success'
    )
    fake_url_for.assert_called_once_with('game.index')
    fake_redirect.assert_called_once_with(fake_url_for.return_value)
    assert result is fake_redirect.return_value


@patch('app.flask.game_controller.injector')
def test_delete_when_request_method_is_post_and_index_error_is_caught_should_abort_with_404_error(
        fake_injector, test_app
):
    # Arrange
    id = 1

    fake_game_repository = Mock(GameRepository)
    game = Game(
        season_year=1,
        week=1,
        guest_name="Guest",
        guest_score=2,
        host_name="Host",
        host_score=3
    )
    fake_game_repository.get_game.return_value = game

    fake_game_service = Mock(GameService)
    fake_game_service.delete_game.side_effect = IndexError()

    fake_injector.get.side_effect = [fake_game_repository, fake_game_service]

    # Act
    with test_app.test_request_context(
            f'/games/delete?id={id}',
            method='POST'
    ):
        with pytest.raises(NotFound):
            result = mod.delete(id)

    # Assert
    fake_injector.get.assert_has_calls([
        call(GameRepository),
        call(GameService),
    ])
    fake_game_repository.get_game.assert_called_once_with(id)
    fake_game_service.delete_game.assert_called_once_with(id)


@pytest.mark.skip('WIP')
@patch('app.flask.game_controller.render_template')
@patch('app.flask.game_controller.GameRepository')
@patch('app.flask.game_controller.injector')
def test_select_season_should_render_game_index_template_for_selected_season(
        fake_injector, fake_render_template, test_app
):
    with test_app.test_request_context(
            '/season_standings/select_season',
            method='POST'
    ):
        # Arrange
        fake_season_repository = Mock(SeasonRepository)
        fake_game_repository = Mock(GameRepository)
        fake_injector.get.side_effect = [fake_season_repository, fake_game_repository]

        # session['selected_season'] = Season(year=0)
        fake_request.form.return_value.get.return_value = Season(year=0)

        # Act
        result = mod.select_season()

        # Assert
        fake_request.form.get.assert_called_once_with('season_dropdown')
        fake_injector.get.assert_has_calls([
            call(SeasonRepository),
            call(GameRepository),
        ])
        fake_season_repository.get_season_by_year.assert_called_once_with(
            fake_request.form.get.return_value
        )
        games = fake_game_repository.get_games_by_season_year.assert_called_once_with(
            season_year=fake_request.form.get.return_value
        )
        fake_render_template.assert_called_once_with(
            'games/index.html',
            seasons=session.get('seasons'), selected_season=fake_season_repository.get_season_by_year.return_value,
            selected_week=session.get('selected_week'), games=games
        )
        assert result is fake_render_template.return_value


@pytest.mark.skip('WIP')
@patch('app.flask.game_controller.render_template')
@patch('app.flask.game_controller.injector')
def test_select_week_should_render_game_index_template_for_selected_season_and_selected_week(
        fake_injector, fake_render_template, test_app
):
    with test_app.test_request_context(
            '/season_standings/select_season',
            method='POST'
    ):
        # Arrange
        fake_game_repository = Mock(GameRepository)
        fake_injector.get.return_value = fake_game_repository

        selected_year = 0

        # Act
        result = mod.select_week()

    # Assert
    fake_request.form.get.assert_called_once_with('week_dropdown')  # Fetch the selected week.
    fake_injector.get.assert_called_once_with(GameRepository)

    selected_season = session.get('selected_season')
    selected_week = session.get('selected_week')
    fake_game_repository.get_games_by_season_year_and_week.assert_called_once_with(
        season_year=selected_season.year, week=selected_week
    )

    fake_render_template.assert_called_once_with(
        'games/index.html',
        seasons=session.get('seasons'), selected_season=selected_season, selected_week=selected_week,
        games=fake_game_repository.get_games_by_season_year_and_week.return_value
    )
    assert result is fake_render_template.return_value
