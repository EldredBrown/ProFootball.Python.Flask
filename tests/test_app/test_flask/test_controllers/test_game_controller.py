from unittest.mock import patch

import pytest

from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound

import app.flask.game_controller as mod

from app.data.models.game import Game
from test_app import create_app


@pytest.fixture()
def test_app():
    return create_app()


@patch('app.flask.game_controller.render_template')
@patch('app.flask.game_controller.game_repository')
def test_index_should_render_game_index_template(fake_game_repository, fake_render_template):
    # Act
    result = mod.index()

    # Assert
    fake_game_repository.get_games.assert_called_once()
    fake_render_template.assert_called_once_with(
        'games/index.html', games=fake_game_repository.get_games.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.game_controller.game_repository')
@patch('app.flask.game_controller.DeleteGameForm')
@patch('app.flask.game_controller.render_template')
def test_details_when_game_found_should_render_game_details_template(
        fake_render_template, fake_delete_game_form, fake_game_repository
):
    # Arrange
    id = 1

    # Act
    result = mod.details(id)

    # Assert
    fake_delete_game_form.assert_called_once()
    fake_game_repository.get_game.assert_called_once_with(id)
    fake_render_template.assert_called_once_with(
        'games/details.html',
        game=fake_game_repository.get_game.return_value,
        delete_game_form=fake_delete_game_form.return_value
    )
    assert result == fake_render_template.return_value


@patch('app.flask.game_controller.game_repository')
@patch('app.flask.game_controller.DeleteGameForm')
def test_details_when_game_not_found_should_abort_with_404_error(
        fake_delete_game_form, fake_game_repository
):
    # Arrange
    fake_game_repository.get_game.side_effect = IndexError()

    # Act
    with pytest.raises(NotFound):
        result = mod.details(1)


@patch('app.flask.game_controller.render_template')
@patch('app.flask.game_controller.flash')
@patch('app.flask.game_controller.NewGameForm')
def test_create_when_form_not_submitted_and_no_form_errors_should_render_create_template(
        fake_new_game_form, fake_flash, fake_render_template
):
    # Arrange
    fake_new_game_form.return_value.validate_on_submit.return_value = False
    fake_new_game_form.return_value.errors = None

    # Act
    result = mod.create()

    # Assert
    fake_flash.assert_not_called()
    fake_render_template('games/create.html', form=fake_new_game_form.return_value)
    assert result is fake_render_template.return_value


@patch('app.flask.game_controller.render_template')
@patch('app.flask.game_controller.flash')
@patch('app.flask.game_controller.NewGameForm')
def test_create_when_form_not_submitted_and_form_errors_should_flash_errors_and_render_create_template(
        fake_new_game_form, fake_flash, fake_render_template
):
    # Arrange
    fake_new_game_form.return_value.validate_on_submit.return_value = False

    errors = 'errors'
    fake_new_game_form.return_value.errors = errors

    # Act
    result = mod.create()

    # Assert
    fake_flash.assert_called_once_with(f"{errors}", 'danger')
    fake_render_template('games/create.html', form=fake_new_game_form.return_value)
    assert result is fake_render_template.return_value


@patch('app.flask.game_controller.redirect')
@patch('app.flask.game_controller.url_for')
@patch('app.flask.game_controller.flash')
@patch('app.flask.game_controller.game_repository')
@patch('app.flask.game_controller.game_factory')
@patch('app.flask.game_controller.NewGameForm')
def test_create_when_form_submitted_and_no_errors_caught_should_flash_success_message_and_redirect_to_game_index(
        fake_new_game_form, fake_game_factory, fake_game_repository, fake_flash, fake_url_for,
        fake_redirect
):
    # Arrange
    fake_new_game_form.return_value.validate_on_submit.return_value = True
    fake_new_game_form.return_value.season_year.data = 1
    fake_new_game_form.return_value.week.data = 1
    fake_new_game_form.return_value.guest_name.data = "Guest"
    fake_new_game_form.return_value.guest_score.data = 1
    fake_new_game_form.return_value.host_name.data = "Host"
    fake_new_game_form.return_value.host_score.data = 2
    fake_new_game_form.return_value.is_playoff.data = False

    kwargs = {
        'season_year': 1,
        'week': 1,
        'guest_name': "Guest",
        'guest_score': 1,
        'host_name': "Host",
        'host_score': 2,
        'is_playoff': False,
    }
    game = Game(**kwargs)
    fake_game_factory.create_game.return_value = game

    # Act
    result = mod.create()

    # Assert
    fake_game_factory.create_game.assert_called_once_with(**kwargs)
    fake_game_repository.add_game.assert_called_once_with(game)
    fake_flash.assert_called_once_with(
        f"Game with season_year={game.season_year}, week={game.week}, "
        f"guest_name={game.guest_name}, and host_name={game.host_name} "
        f"has been successfully submitted.", 'success'
    )
    fake_url_for.assert_called_once_with('game.index')
    fake_redirect.assert_called_once_with(fake_url_for.return_value)
    assert result is fake_redirect.return_value


@patch('app.flask.game_controller.render_template')
@patch('app.flask.game_controller.flash')
@patch('app.flask.game_controller.game_repository')
@patch('app.flask.game_controller.game_factory')
@patch('app.flask.game_controller.NewGameForm')
def test_create_when_form_submitted_and_value_error_caught_should_flash_error_message_and_render_create_template(
        fake_new_game_form, fake_game_factory, fake_game_repository, fake_flash, fake_render_template
):
    # Arrange
    fake_new_game_form.return_value.validate_on_submit.return_value = True
    fake_new_game_form.return_value.season_year.data = 1
    fake_new_game_form.return_value.week.data = 1
    fake_new_game_form.return_value.guest_name.data = "Guest"
    fake_new_game_form.return_value.guest_score.data = 1
    fake_new_game_form.return_value.host_name.data = "Host"
    fake_new_game_form.return_value.host_score.data = 2
    fake_new_game_form.return_value.is_playoff.data = False

    kwargs = {
        'season_year': 1,
        'week': 1,
        'guest_name': "Guest",
        'guest_score': 1,
        'host_name': "Host",
        'host_score': 2,
        'is_playoff': False,
    }
    game = Game(**kwargs)
    fake_game_factory.create_game.return_value = game

    err = ValueError()
    fake_game_repository.add_game.side_effect = err

    # Act
    result = mod.create()

    # Assert
    fake_game_factory.create_game.assert_called_once_with(**kwargs)
    fake_game_repository.add_game.assert_called_once_with(game)
    fake_flash.assert_called_once_with(str(err), 'danger')
    fake_render_template.assert_called_once_with(
        'games/create.html', game=None, form=fake_new_game_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.game_controller.render_template')
@patch('app.flask.game_controller.flash')
@patch('app.flask.game_controller.game_repository')
@patch('app.flask.game_controller.game_factory')
@patch('app.flask.game_controller.NewGameForm')
def test_create_when_form_submitted_and_integrity_error_caught_should_flash_error_message_and_render_create_template(
        fake_new_game_form, fake_game_factory, fake_game_repository, fake_flash, fake_render_template
):
    # Arrange
    fake_new_game_form.return_value.validate_on_submit.return_value = True
    fake_new_game_form.return_value.season_year.data = 1
    fake_new_game_form.return_value.week.data = 1
    fake_new_game_form.return_value.guest_name.data = "Guest"
    fake_new_game_form.return_value.guest_score.data = 1
    fake_new_game_form.return_value.host_name.data = "Host"
    fake_new_game_form.return_value.host_score.data = 2
    fake_new_game_form.return_value.is_playoff.data = False

    kwargs = {
        'season_year': 1,
        'week': 1,
        'guest_name': "Guest",
        'guest_score': 1,
        'host_name': "Host",
        'host_score': 2,
        'is_playoff': False,
    }
    game = Game(**kwargs)
    fake_game_factory.create_game.return_value = game

    err = IntegrityError('statement', 'params', Exception())
    fake_game_repository.add_game.side_effect = err

    # Act
    result = mod.create()

    # Assert
    fake_game_factory.create_game.assert_called_once_with(**kwargs)
    fake_game_repository.add_game.assert_called_once_with(game)
    fake_flash.assert_called_once_with(str(err), 'danger')
    fake_render_template.assert_called_once_with(
        'games/create.html', game=None, form=fake_new_game_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.game_controller.game_repository')
def test_edit_when_game_not_found_should_abort_with_404_error(fake_game_repository):
    # Arrange
    old_game = None
    fake_game_repository.get_game.return_value = old_game

    # Act
    with pytest.raises(NotFound):
        result = mod.edit(1)


@patch('app.flask.game_controller.render_template')
@patch('app.flask.game_controller.flash')
@patch('app.flask.game_controller.EditGameForm')
@patch('app.flask.game_controller.game_repository')
def test_edit_when_game_found_and_form_not_submitted_and_no_form_errors_should_render_edit_template(
        fake_game_repository, fake_edit_game_form, fake_flash, fake_render_template
):
    # Arrange
    old_game = Game(
        season_year=1,
        week=1,
        guest_name="Guest",
        guest_score=1,
        host_name="Host",
        host_score=2,
        is_playoff=False
    )
    fake_game_repository.get_game.return_value = old_game

    fake_edit_game_form.return_value.validate_on_submit.return_value = False
    fake_edit_game_form.return_value.errors = None

    # Act
    result = mod.edit(1)

    # Assert
    assert fake_edit_game_form.return_value.season_year.data == old_game.season_year
    assert fake_edit_game_form.return_value.week.data == old_game.week
    assert fake_edit_game_form.return_value.guest_name.data == old_game.guest_name
    assert fake_edit_game_form.return_value.guest_score.data == old_game.guest_score
    assert fake_edit_game_form.return_value.host_name.data == old_game.host_name
    assert fake_edit_game_form.return_value.host_score.data == old_game.host_score
    assert fake_edit_game_form.return_value.is_playoff.data == old_game.is_playoff
    fake_flash.assert_not_called()
    fake_render_template.assert_called_once_with(
        'games/edit.html', game=old_game, form=fake_edit_game_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.game_controller.render_template')
@patch('app.flask.game_controller.flash')
@patch('app.flask.game_controller.EditGameForm')
@patch('app.flask.game_controller.game_repository')
def test_edit_when_game_found_and_form_not_submitted_and_form_errors_should_flash_errors_and_render_edit_template(
        fake_game_repository, fake_edit_game_form, fake_flash, fake_render_template
):
    # Arrange
    old_game = Game(
        season_year=1,
        week=1,
        guest_name="Guest",
        guest_score=1,
        host_name="Host",
        host_score=2,
        is_playoff=False
    )
    fake_game_repository.get_game.return_value = old_game

    fake_edit_game_form.return_value.validate_on_submit.return_value = False

    errors = 'errors'
    fake_edit_game_form.return_value.errors = errors

    # Act
    result = mod.edit(1)

    # Assert
    assert fake_edit_game_form.return_value.season_year.data == old_game.season_year
    assert fake_edit_game_form.return_value.week.data == old_game.week
    assert fake_edit_game_form.return_value.guest_name.data == old_game.guest_name
    assert fake_edit_game_form.return_value.guest_score.data == old_game.guest_score
    assert fake_edit_game_form.return_value.host_name.data == old_game.host_name
    assert fake_edit_game_form.return_value.host_score.data == old_game.host_score
    assert fake_edit_game_form.return_value.is_playoff.data == old_game.is_playoff
    fake_flash.assert_called_once_with(f"{errors}", 'danger')
    fake_render_template.assert_called_once_with(
        'games/edit.html', game=old_game, form=fake_edit_game_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.game_controller.redirect')
@patch('app.flask.game_controller.url_for')
@patch('app.flask.game_controller.flash')
@patch('app.flask.game_controller.game_factory')
@patch('app.flask.game_controller.EditGameForm')
@patch('app.flask.game_controller.game_repository')
def test_edit_when_game_found_and_form_submitted_and_no_errors_caught_should_flash_success_message_and_redirect_to_game_details(
        fake_game_repository, fake_edit_game_form, fake_game_factory, fake_flash, fake_url_for,
        fake_redirect
):
    # Arrange
    id = 1

    old_game = Game(
        id=id,
        season_year=1,
        week=1,
        guest_name="Guest",
        guest_score=1,
        host_name="Host",
        host_score=2,
        is_playoff=False
    )
    fake_game_repository.get_game.return_value = old_game

    fake_edit_game_form.return_value.validate_on_submit.return_value = True
    fake_edit_game_form.return_value.season_year.data = 2
    fake_edit_game_form.return_value.week.data = 2
    fake_edit_game_form.return_value.guest_name.data = "Guest 2"
    fake_edit_game_form.return_value.guest_score.data = 2
    fake_edit_game_form.return_value.host_name.data = "Host 2"
    fake_edit_game_form.return_value.host_score.data = 1
    fake_edit_game_form.return_value.is_playoff.data = True

    kwargs = {
        'id': id,
        'season_year': 2,
        'week': 2,
        'guest_name': "Guest 2",
        'guest_score': 2,
        'host_name': "Host 2",
        'host_score': 1,
        'is_playoff': True,
    }
    new_game = Game(**kwargs)
    fake_game_factory.create_game.return_value = new_game

    # Act
    result = mod.edit(id)

    # Assert
    fake_game_factory.create_game.assert_called_once_with(**kwargs)
    fake_game_repository.update_game.assert_called_once_with(new_game)
    fake_flash.assert_called_once_with(
        f"Game with season_year={new_game.season_year}, week={new_game.week}, "
        f"guest_name={new_game.guest_name}, and host_name={new_game.host_name} "
        f"has been successfully updated.", 'success'
    )
    fake_url_for.assert_called_once_with('game.details', id=id)
    fake_redirect.assert_called_once_with(fake_url_for.return_value)
    assert result is fake_redirect.return_value


@patch('app.flask.game_controller.render_template')
@patch('app.flask.game_controller.flash')
@patch('app.flask.game_controller.game_factory')
@patch('app.flask.game_controller.EditGameForm')
@patch('app.flask.game_controller.game_repository')
def test_edit_when_game_found_and_form_submitted_and_value_error_caught_should_flash_error_message_and_render_edit_template(
        fake_game_repository, fake_edit_game_form, fake_game_factory, fake_flash,
        fake_render_template
):
    # Arrange
    id = 1

    old_game = Game(
        id=id,
        season_year=1,
        week=1,
        guest_name="Guest",
        guest_score=1,
        host_name="Host",
        host_score=2,
        is_playoff=False
    )
    fake_game_repository.get_game.return_value = old_game

    fake_edit_game_form.return_value.validate_on_submit.return_value = True
    fake_edit_game_form.return_value.season_year.data = 2
    fake_edit_game_form.return_value.week.data = 2
    fake_edit_game_form.return_value.guest_name.data = "Guest 2"
    fake_edit_game_form.return_value.guest_score.data = 2
    fake_edit_game_form.return_value.host_name.data = "Host 2"
    fake_edit_game_form.return_value.host_score.data = 1
    fake_edit_game_form.return_value.is_playoff.data = True

    kwargs = {
        'id': id,
        'season_year': 2,
        'week': 2,
        'guest_name': "Guest 2",
        'guest_score': 2,
        'host_name': "Host 2",
        'host_score': 1,
        'is_playoff': True,
    }
    new_game = Game(**kwargs)
    fake_game_factory.create_game.return_value = new_game

    err = ValueError()
    fake_game_repository.update_game.side_effect = err

    # Act
    result = mod.edit(id)

    # Assert
    fake_game_factory.create_game.assert_called_once_with(**kwargs)
    fake_game_repository.update_game.assert_called_once_with(new_game)
    fake_flash.assert_called_once_with(str(err), 'danger')
    fake_render_template.assert_called_once_with(
        'games/edit.html', game=old_game, form=fake_edit_game_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.game_controller.render_template')
@patch('app.flask.game_controller.flash')
@patch('app.flask.game_controller.game_factory')
@patch('app.flask.game_controller.EditGameForm')
@patch('app.flask.game_controller.game_repository')
def test_edit_when_game_found_and_form_submitted_and_integrity_error_caught_should_flash_error_message_and_render_edit_template(
        fake_game_repository, fake_edit_game_form, fake_game_factory, fake_flash,
        fake_render_template
):
    # Arrange
    id = 1

    old_game = Game(
        id=id,
        season_year=1,
        week=1,
        guest_name="Guest",
        guest_score=1,
        host_name="Host",
        host_score=2,
        is_playoff=False
    )
    fake_game_repository.get_game.return_value = old_game

    fake_edit_game_form.return_value.validate_on_submit.return_value = True
    fake_edit_game_form.return_value.season_year.data = 2
    fake_edit_game_form.return_value.week.data = 2
    fake_edit_game_form.return_value.guest_name.data = "Guest 2"
    fake_edit_game_form.return_value.guest_score.data = 2
    fake_edit_game_form.return_value.host_name.data = "Host 2"
    fake_edit_game_form.return_value.host_score.data = 1
    fake_edit_game_form.return_value.is_playoff.data = True

    kwargs = {
        'id': id,
        'season_year': 2,
        'week': 2,
        'guest_name': "Guest 2",
        'guest_score': 2,
        'host_name': "Host 2",
        'host_score': 1,
        'is_playoff': True,
    }
    new_game = Game(**kwargs)
    fake_game_factory.create_game.return_value = new_game

    err = IntegrityError('statement', 'params', Exception())
    fake_game_repository.update_game.side_effect = err

    # Act
    result = mod.edit(id)

    # Assert
    fake_game_factory.create_game.assert_called_once_with(**kwargs)
    fake_game_repository.update_game.assert_called_once_with(new_game)
    fake_flash.assert_called_once_with(str(err), 'danger')
    fake_render_template.assert_called_once_with(
        'games/edit.html', game=old_game, form=fake_edit_game_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.game_controller.render_template')
@patch('app.flask.game_controller.game_repository')
def test_delete_when_request_method_is_get_should_render_delete_template(
        fake_game_repository, fake_render_template, test_app
):
    # Arrange
    game = Game()
    fake_game_repository.get_game.return_value = game

    # Act
    with test_app.test_request_context(
            '/games/delete?id=1',
            method='GET'
    ):
        with test_app.app_context():
            result = mod.delete(1)

    # Assert
    fake_game_repository.get_game.assert_called_once_with(1)
    fake_render_template.assert_called_once_with('games/delete.html', game=game)
    assert result is fake_render_template.return_value


@patch('app.flask.game_controller.redirect')
@patch('app.flask.game_controller.url_for')
@patch('app.flask.game_controller.flash')
@patch('app.flask.game_controller.game_repository')
def test_delete_when_request_method_is_post_and_game_found_should_flash_success_message_and_redirect_to_games_index(
        fake_game_repository, fake_flash, fake_url_for, fake_redirect, test_app
):
    # Arrange
    game = Game()
    fake_game_repository.get_game.return_value = game

    # Act
    id = 1
    with test_app.test_request_context(
            '/games/delete?id=1',
            method='POST'
    ):
        with test_app.app_context():
            result = mod.delete(id)

    # Assert
    fake_game_repository.delete_game.assert_called_once_with(id)
    fake_flash.assert_called_once_with(
        f"Game with season_year={game.season_year}, week={game.week}, "
        f"guest_name={game.guest_name}, and host_name={game.host_name} "
        f"has been successfully deleted.", 'success'
    )
    fake_url_for.assert_called_once_with('game.index')
    fake_redirect.assert_called_once_with(fake_url_for.return_value)
    assert result is fake_redirect.return_value


@patch('app.flask.game_controller.game_repository')
def test_delete_when_request_method_is_post_and_game_not_found_should_abort_with_404_error(
        fake_game_repository, test_app
):
    # Arrange
    game = Game()
    fake_game_repository.get_game.return_value = game
    fake_game_repository.delete_game.side_effect = IndexError()

    # Act
    with test_app.test_request_context(
            '/games/delete?id=1',
            method='POST'
    ):
        with test_app.app_context():
            with pytest.raises(NotFound):
                result = mod.delete(1)
