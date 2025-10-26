from unittest.mock import patch

import pytest

from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound

import app.flask.game_controller as game_controller

from app.data.models.season import Season
from app.data.models.game import Game
from app.data.models.league_season import LeagueSeason
from app.data.models.team_season import TeamSeason

from test_app import create_app


@pytest.fixture()
def test_app():
    return create_app()


@patch('app.flask.game_controller.selected_season')
@patch('app.flask.game_controller.render_template')
@patch('app.flask.game_controller.game_repository')
@patch('app.flask.game_controller.season_repository')
def test_index_should_render_game_index_template(
        fake_season_repository, fake_game_repository, fake_render_template, fake_selected_season, test_app
):
    # Act
    with test_app.app_context():
        result = game_controller.index()

    # Assert
    fake_season_repository.get_seasons.assert_called_once()
    fake_game_repository.get_games_by_season_year.assert_called_once_with(season_year=None)
    fake_render_template.assert_called_once_with(
        'games/index.html',
        seasons=fake_season_repository.get_seasons.return_value,
        selected_season=fake_selected_season,
        selected_week=0, games=fake_game_repository.get_games_by_season_year.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.game_controller.game_repository')
@patch('app.flask.game_controller.DeleteGameForm')
@patch('app.flask.game_controller.render_template')
def test_details_when_game_found_should_render_game_details_template(
        fake_render_template, fake_delete_game_form, fake_game_repository, test_app
):
    # Arrange
    id = 1

    # Act
    with test_app.app_context():
        result = game_controller.details(id)

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
        fake_delete_game_form, fake_game_repository, test_app
):
    # Arrange
    fake_game_repository.get_game.side_effect = IndexError()

    # Act
    with test_app.app_context():
        with pytest.raises(NotFound):
            result = game_controller.details(1)


@patch('app.flask.game_controller.render_template')
@patch('app.flask.game_controller.flash')
@patch('app.flask.game_controller.NewGameForm')
def test_create_when_form_not_submitted_and_no_form_errors_should_render_create_template(
        fake_new_game_form, fake_flash, fake_render_template, test_app
):
    # Arrange
    fake_new_game_form.return_value.validate_on_submit.return_value = False
    fake_new_game_form.return_value.errors = None

    # Act
    with test_app.app_context():
        result = game_controller.create()

    # Assert
    fake_flash.assert_not_called()
    fake_render_template('games/create.html', form=fake_new_game_form.return_value)
    assert result is fake_render_template.return_value


@patch('app.flask.game_controller.render_template')
@patch('app.flask.game_controller.flash')
@patch('app.flask.game_controller.NewGameForm')
def test_create_when_form_not_submitted_and_form_errors_should_flash_errors_and_render_create_template(
        fake_new_game_form, fake_flash, fake_render_template, test_app
):
    # Arrange
    fake_new_game_form.return_value.validate_on_submit.return_value = False

    errors = 'errors'
    fake_new_game_form.return_value.errors = errors

    # Act
    with test_app.app_context():
        result = game_controller.create()

    # Assert
    fake_flash.assert_called_once_with(f"{errors}", 'danger')
    fake_render_template('games/create.html', form=fake_new_game_form.return_value)
    assert result is fake_render_template.return_value


@patch('app.flask.game_controller.url_for')
@patch('app.flask.game_controller.flash')
@patch('app.flask.game_controller.game_repository')
@patch('app.flask.game_controller.redirect')
@patch('app.flask.game_controller.NewGameForm')
def test_create_when_form_submitted_and_no_errors_caught_should_flash_success_message_and_redirect_to_game_index(
        fake_new_game_form, fake_redirect, fake_game_repository, fake_flash, fake_url_for, test_app
):
    # Arrange
    fake_new_game_form.return_value.validate_on_submit.return_value = True
    fake_new_game_form.return_value.season_year.data = 1920
    fake_new_game_form.return_value.week.data = 1
    fake_new_game_form.return_value.guest_name.data = "St. Paul Ideals"
    fake_new_game_form.return_value.guest_score.data = 0
    fake_new_game_form.return_value.host_name.data = "Rock Island Independents"
    fake_new_game_form.return_value.host_score.data = 48
    fake_new_game_form.return_value.is_playoff.data = False
    fake_new_game_form.return_value.notes.data = None

    kwargs = {
        'season_year': 1920,
        'week': 1,
        'guest_name': "St. Paul Ideals",
        'guest_score': 0,
        'host_name': "Rock Island Independents",
        'host_score': 48,
        'is_playoff': False,
        'notes': None,
    }

    # Act
    with test_app.app_context():
        result = game_controller.create()

    # Assert
    fake_game_repository.add_game.assert_called_once_with(**kwargs)
    fake_flash(f"Game for season={kwargs['season_year']} with guest={kwargs['guest_name']} and host={kwargs['host_name']} has been successfully submitted.", 'success')
    fake_url_for.assert_called_once_with('game.index')
    fake_redirect.assert_called_once_with(fake_url_for.return_value)
    assert result is fake_redirect.return_value


@patch('app.flask.game_controller.render_template')
@patch('app.flask.game_controller.flash')
@patch('app.flask.game_controller.game_repository')
@patch('app.flask.game_controller.NewGameForm')
def test_create_when_form_submitted_and_value_error_caught_should_flash_error_message_and_render_create_template(
        fake_new_game_form, fake_game_repository, fake_flash, fake_render_template, test_app
):
    # Arrange
    fake_new_game_form.return_value.validate_on_submit.return_value = True
    fake_new_game_form.return_value.season_year.data = 1920
    fake_new_game_form.return_value.week.data = 1
    fake_new_game_form.return_value.guest_name.data = "St. Paul Ideals"
    fake_new_game_form.return_value.guest_score.data = 0
    fake_new_game_form.return_value.host_name.data = "Rock Island Independents"
    fake_new_game_form.return_value.host_score.data = 48
    fake_new_game_form.return_value.is_playoff.data = False
    fake_new_game_form.return_value.notes.data = None

    err = ValueError()
    fake_game_repository.add_game.side_effect = err

    kwargs = {
        'season_year': 1920,
        'week': 1,
        'guest_name': "St. Paul Ideals",
        'guest_score': 0,
        'host_name': "Rock Island Independents",
        'host_score': 48,
        'is_playoff': False,
        'notes': None,
    }

    # Act
    with test_app.app_context():
        result = game_controller.create()

    # Assert
    fake_game_repository.add_game.assert_called_once_with(**kwargs)
    fake_flash.assert_called_once_with(str(err), 'danger')
    fake_render_template.assert_called_once_with(
        'games/create.html', game=None, form=fake_new_game_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.game_controller.render_template')
@patch('app.flask.game_controller.flash')
@patch('app.flask.game_controller.game_repository')
@patch('app.flask.game_controller.NewGameForm')
def test_create_when_form_submitted_and_integrity_error_caught_should_flash_error_message_and_render_create_template(
        fake_new_game_form, fake_game_repository, fake_flash, fake_render_template, test_app
):
    # Arrange
    fake_new_game_form.return_value.validate_on_submit.return_value = True
    fake_new_game_form.return_value.season_year.data = 1920
    fake_new_game_form.return_value.week.data = 1
    fake_new_game_form.return_value.guest_name.data = "St. Paul Ideals"
    fake_new_game_form.return_value.guest_score.data = 0
    fake_new_game_form.return_value.host_name.data = "Rock Island Independents"
    fake_new_game_form.return_value.host_score.data = 48
    fake_new_game_form.return_value.is_playoff.data = False
    fake_new_game_form.return_value.notes.data = None

    err = IntegrityError('statement', 'params', Exception())
    fake_game_repository.add_game.side_effect = err
    fake_game_repository.add_game.side_effect = err

    kwargs = {
        'season_year': 1920,
        'week': 1,
        'guest_name': "St. Paul Ideals",
        'guest_score': 0,
        'host_name': "Rock Island Independents",
        'host_score': 48,
        'is_playoff': False,
        'notes': None,
    }

    # Act
    with test_app.app_context():
        result = game_controller.create()

    # Assert
    fake_game_repository.add_game.assert_called_once_with(**kwargs)
    fake_flash.assert_called_once_with(str(err), 'danger')
    fake_render_template.assert_called_once_with(
        'games/create.html', game=None, form=fake_new_game_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.game_controller.game_repository')
def test_edit_when_game_not_found_should_abort_with_404_error(fake_game_repository, test_app):
    # Arrange
    game = None
    fake_game_repository.get_game.return_value = game

    # Act
    with test_app.app_context():
        with pytest.raises(NotFound):
            result = game_controller.edit(1)


@patch('app.flask.game_controller.render_template')
@patch('app.flask.game_controller.flash')
@patch('app.flask.game_controller.EditGameForm')
@patch('app.flask.game_controller.game_repository')
def test_edit_when_game_found_and_form_not_submitted_and_no_form_errors_should_render_edit_template(
        fake_game_repository, fake_edit_game_form, fake_flash, fake_render_template, test_app
):
    with test_app.app_context():
        # Arrange
        game = Game(
            season_year=1920,
            week=1,
            guest_name="St. Paul Ideals",
            guest_score=0,
            host_name="Rock Island Independents",
            host_score=48,
            is_playoff=False,
            notes=None
        )
        fake_game_repository.get_game.return_value = game

        fake_edit_game_form.return_value.validate_on_submit.return_value = False
        fake_edit_game_form.return_value.errors = None

        # Act
        result = game_controller.edit(1)

    # Assert
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
@patch('app.flask.game_controller.game_repository')
def test_edit_when_game_found_and_form_not_submitted_and_form_errors_should_flash_errors_and_render_edit_template(
        fake_game_repository, fake_edit_game_form, fake_flash, fake_render_template, test_app
):
    with test_app.app_context():
        # Arrange
        game = Game(
            season_year=1920,
            week=1,
            guest_name="St. Paul Ideals",
            guest_score=0,
            host_name="Rock Island Independents",
            host_score=48,
            is_playoff=False,
            notes=None
        )
        fake_game_repository.get_game.return_value = game

        fake_edit_game_form.return_value.validate_on_submit.return_value = False

        errors = 'errors'
        fake_edit_game_form.return_value.errors = errors

        # Act
        result = game_controller.edit(1)

    # Assert
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
@patch('app.flask.game_controller.flash')
@patch('app.flask.game_controller.redirect')
@patch('app.flask.game_controller.EditGameForm')
@patch('app.flask.game_controller.game_repository')
def test_edit_when_game_found_and_form_submitted_and_no_errors_caught_should_flash_success_message_and_redirect_to_game_details(
        fake_game_repository, fake_edit_game_form, fake_redirect, fake_flash, fake_url_for, test_app
):
    with test_app.app_context():
        # Arrange
        game = Game(
            season_year=1920,
            week=1,
            guest_name="St. Paul Ideals",
            guest_score=0,
            host_name="Rock Island Independents",
            host_score=48,
            is_playoff=False,
            notes=None
        )
        fake_game_repository.get_game.return_value = game

        fake_edit_game_form.return_value.validate_on_submit.return_value = True
        fake_edit_game_form.return_value.season_year.data = 1920
        fake_edit_game_form.return_value.week.data = 1
        fake_edit_game_form.return_value.guest_name.data = "St. Paul Ideals"
        fake_edit_game_form.return_value.guest_score.data = 0
        fake_edit_game_form.return_value.host_name.data = "Rock Island Independents"
        fake_edit_game_form.return_value.host_score.data = 48
        fake_edit_game_form.return_value.is_playoff.data = False
        fake_edit_game_form.return_value.notes.data = None

        id = 1
        kwargs = {
            'id': id,
            'season_year': 1920,
            'week': 1,
            'guest_name': "St. Paul Ideals",
            'guest_score': 0,
            'host_name': "Rock Island Independents",
            'host_score': 48,
            'is_playoff': False,
            'notes': None,
        }

        # Act
        result = game_controller.edit(id)

    # Assert
    fake_game_repository.update_game.assert_called_once_with(**kwargs)
    fake_flash.assert_called_once_with(
        f"Game for season={fake_edit_game_form.return_value.season_year.data} with guest={fake_edit_game_form.return_value.guest_name.data} and host={fake_edit_game_form.return_value.host_name.data} has been successfully updated.",
        'success'
    )
    fake_url_for.assert_called_once_with('game.details', id=id)
    fake_redirect.assert_called_once_with(fake_url_for.return_value)
    assert result is fake_redirect.return_value


@patch('app.flask.game_controller.flash')
@patch('app.flask.game_controller.render_template')
@patch('app.flask.game_controller.EditGameForm')
@patch('app.flask.game_controller.game_repository')
def test_edit_when_game_found_and_form_submitted_and_value_error_caught_should_flash_error_message_and_render_edit_template(
        fake_game_repository, fake_edit_game_form, fake_render_template, fake_flash, test_app
):
    with test_app.app_context():
        # Arrange
        game = Game(
            season_year=1920,
            week=1,
            guest_name="St. Paul Ideals",
            guest_score=0,
            host_name="Rock Island Independents",
            host_score=48,
            is_playoff=False,
            notes=None
        )
        fake_game_repository.get_game.return_value = game

        fake_edit_game_form.return_value.validate_on_submit.return_value = True
        fake_edit_game_form.return_value.season_year.data = 1920
        fake_edit_game_form.return_value.week.data = 1
        fake_edit_game_form.return_value.guest_name.data = "St. Paul Ideals"
        fake_edit_game_form.return_value.guest_score.data = 0
        fake_edit_game_form.return_value.host_name.data = "Rock Island Independents"
        fake_edit_game_form.return_value.host_score.data = 48
        fake_edit_game_form.return_value.is_playoff.data = False
        fake_edit_game_form.return_value.notes.data = None

        err = ValueError()
        fake_game_repository.update_game.side_effect = err

        id = 1
        kwargs = {
            'id': id,
            'season_year': 1920,
            'week': 1,
            'guest_name': "St. Paul Ideals",
            'guest_score': 0,
            'host_name': "Rock Island Independents",
            'host_score': 48,
            'is_playoff': False,
            'notes': None,
        }

        # Act
        result = game_controller.edit(id)

    # Assert
    fake_game_repository.update_game.assert_called_once_with(**kwargs)
    fake_flash.assert_called_once_with(str(err), 'danger')
    fake_render_template.assert_called_once_with(
        'games/edit.html', game=game, form=fake_edit_game_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.game_controller.flash')
@patch('app.flask.game_controller.render_template')
@patch('app.flask.game_controller.EditGameForm')
@patch('app.flask.game_controller.game_repository')
def test_edit_when_game_found_and_form_submitted_and_integrity_error_caught_should_flash_error_message_and_render_edit_template(
        fake_game_repository, fake_edit_game_form, fake_render_template, fake_flash, test_app
):
    with test_app.app_context():
        # Arrange
        game = Game(
            season_year=1920,
            week=1,
            guest_name="St. Paul Ideals",
            guest_score=0,
            host_name="Rock Island Independents",
            host_score=48,
            is_playoff=False,
            notes=None
        )
        fake_game_repository.get_game.return_value = game

        fake_edit_game_form.return_value.validate_on_submit.return_value = True
        fake_edit_game_form.return_value.season_year.data = 1920
        fake_edit_game_form.return_value.week.data = 1
        fake_edit_game_form.return_value.guest_name.data = "St. Paul Ideals"
        fake_edit_game_form.return_value.guest_score.data = 0
        fake_edit_game_form.return_value.host_name.data = "Rock Island Independents"
        fake_edit_game_form.return_value.host_score.data = 48
        fake_edit_game_form.return_value.is_playoff.data = False
        fake_edit_game_form.return_value.notes.data = None

        err = IntegrityError('statement', 'params', Exception())
        fake_game_repository.update_game.side_effect = err

        id = 1
        kwargs = {
            'id': id,
            'season_year': 1920,
            'week': 1,
            'guest_name': "St. Paul Ideals",
            'guest_score': 0,
            'host_name': "Rock Island Independents",
            'host_score': 48,
            'is_playoff': False,
            'notes': None,
        }

        # Act
        result = game_controller.edit(id)

    # Assert
    fake_game_repository.update_game.assert_called_once_with(**kwargs)
    fake_flash.assert_called_once_with(str(err), 'danger')
    fake_render_template.assert_called_once_with(
        'games/edit.html', game=game, form=fake_edit_game_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.game_controller.render_template')
@patch('app.flask.game_controller.game_repository')
def test_delete_when_request_method_is_get_should_render_delete_template(
        fake_game_repository, fake_render_template, test_app
):
    # Arrange
    game = Game(
        season_year=1920,
        week=1,
        guest_name="St. Paul Ideals",
        guest_score=0,
        host_name="Rock Island Independents",
        host_score=48
    )
    fake_game_repository.get_game.return_value = game

    # Act
    with test_app.test_request_context(
            '/games/delete?id=1',
            method='GET'
    ):
        with test_app.app_context():
            result = game_controller.delete(1)

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
    game = Game(
        season_year=1920,
        week=1,
        guest_name="St. Paul Ideals",
        guest_score=0,
        host_name="Rock Island Independents",
        host_score=48
    )
    fake_game_repository.get_game.return_value = game

    # Act
    id = 1
    with test_app.test_request_context(
            '/games/delete?id=1',
            method='POST'
    ):
        with test_app.app_context():
            result = game_controller.delete(id)

    # Assert
    fake_game_repository.delete_game.assert_called_once_with(id)
    fake_flash.assert_called_once_with(
        f"Game for season={game.season_year} with guest={game.guest_name} and host={game.host_name} has been successfully deleted.",
        'success'
    )
    fake_url_for.assert_called_once_with('game.index')
    fake_redirect.assert_called_once_with(fake_url_for.return_value)
    assert result is fake_redirect.return_value


@patch('app.flask.game_controller.game_repository')
def test_delete_when_request_method_is_post_and_game_not_found_should_abort_with_404_error(
        fake_game_repository, test_app
):
    # Arrange
    game = Game(
        season_year=1920,
        week=1,
        guest_name="St. Paul Ideals",
        guest_score=0,
        host_name="Rock Island Independents",
        host_score=48
    )
    fake_game_repository.get_game.return_value = game
    fake_game_repository.delete_game.side_effect = IndexError()

    # Act
    with test_app.test_request_context(
            '/games/delete?id=1',
            method='POST'
    ):
        with test_app.app_context():
            with pytest.raises(NotFound):
                result = game_controller.delete(1)


@pytest.mark.skip('WIP')
@patch('app.flask.game_controller.render_template')
def test_select_season_should_render_game_index_template_for_selected_season(fake_render_template, test_app):
    with test_app.app_context():
        with test_app.test_request_context(
                '/season_standings/select_season',
                method='POST'
        ):
            # Arrange
            selected_year = 0

            # Act
            result = game_controller.select_season()

    # Assert
    # fake_request.form.get.assert_called_once_with('season_dropdown'))  # Fetch the selected season.
    # selected_season = fake_season_repository.get_season_by_year.assert_called_once_with(
    #     fake_request.form.get.return_value
    # )
    # games = fake_game_repository.get_games_by_season_year.assert_called_once_with(
    #     season_year=fake_request.form.get.return_value
    # )
    # fake_render_template.assert_called_once_with(
    #     'games/index.html',
    #     seasons=seasons, selected_season=selected_season, selected_week=selected_week, games=games
    # )
    assert result is fake_render_template.return_value


@pytest.mark.skip('WIP')
@patch('app.flask.game_controller.render_template')
def test_select_week_should_render_game_index_template_for_selected_season_and_selected_week(
        fake_render_template, test_app
):
    with test_app.app_context():
        with test_app.test_request_context(
                '/season_standings/select_season',
                method='POST'
        ):
            # Arrange
            selected_year = 0

            # Act
            result = game_controller.select_season()

    # Assert
    # fake_request.form.get.assert_called_once_with('week_dropdown'))  # Fetch the selected week.
    # games = fake_game_repository.get_games_by_season_year_and_week.assert_called_once_with(
    #     season_year=selected_season.year, week=selected_week
    # )
    # fake_render_template.assert_called_once_with(
    #     'games/index.html',
    #     seasons=seasons, selected_season=selected_season, selected_week=selected_week, games=games
    # )
    assert result is fake_render_template.return_value
