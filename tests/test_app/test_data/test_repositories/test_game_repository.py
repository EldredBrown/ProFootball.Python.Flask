from unittest.mock import patch, call

import pytest

from sqlalchemy.exc import IntegrityError

from app import sqla
from instance.test_db import db_init
from test_app import create_app

from app.data.models.season import Season
from app.data.models.game import Game
from app.data.models.league_season import LeagueSeason
from app.data.models.team_season import TeamSeason
from app.data.repositories.game_repository import GameRepository


@pytest.fixture
def test_app():
    return create_app()


def test_get_games_should_get_games(test_app):
    with test_app.app_context():
        # Arrange
        db_init.init_db()

        games_in = [
            Game(
                season_year=1920,
                week=1,
                guest_name="St. Paul Ideals",
                guest_score=0,
                host_name="Rock Island Independents",
                host_score=48,
                is_playoff=False
            ),
            Game(
                season_year=1920,
                week=2,
                guest_name="Wheeling Stogies",
                guest_score=0,
                host_name="Akron Pros",
                host_score=43,
                is_playoff=False
            ),
            Game(
                season_year=1920,
                week=2,
                guest_name="Muncie Flyers",
                guest_score=0,
                host_name="Rock Island Independents",
                host_score=45,
                is_playoff=False
            ),
        ]
        for game in games_in:
            sqla.session.add(game)
        sqla.session.commit()

        # Act
        test_repo = GameRepository()
        games_out = test_repo.get_games()

    # Assert
    assert games_out == games_in


def test_get_games_by_season_year_when_season_year_arg_is_none_should_return_empty_list(test_app):
    with test_app.app_context():
        # Arrange
        db_init.init_db()

        games_in = [
            Game(
                season_year=1920,
                week=1,
                guest_name="St. Paul Ideals",
                guest_score=0,
                host_name="Rock Island Independents",
                host_score=48,
                is_playoff=False
            ),
            Game(
                season_year=1920,
                week=2,
                guest_name="Wheeling Stogies",
                guest_score=0,
                host_name="Akron Pros",
                host_score=43,
                is_playoff=False
            ),
            Game(
                season_year=1920,
                week=2,
                guest_name="Muncie Flyers",
                guest_score=0,
                host_name="Rock Island Independents",
                host_score=45,
                is_playoff=False
            ),
            Game(
                season_year=1921,
                week=1,
                guest_name="St. Paul Ideals",
                guest_score=0,
                host_name="Rock Island Independents",
                host_score=48,
                is_playoff=False
            ),
            Game(
                season_year=1921,
                week=2,
                guest_name="Wheeling Stogies",
                guest_score=0,
                host_name="Akron Pros",
                host_score=43,
                is_playoff=False
            ),
            Game(
                season_year=1921,
                week=2,
                guest_name="Muncie Flyers",
                guest_score=0,
                host_name="Rock Island Independents",
                host_score=45,
                is_playoff=False
            ),
            Game(
                season_year=1922,
                week=1,
                guest_name="St. Paul Ideals",
                guest_score=0,
                host_name="Rock Island Independents",
                host_score=48,
                is_playoff=False
            ),
            Game(
                season_year=1922,
                week=2,
                guest_name="Wheeling Stogies",
                guest_score=0,
                host_name="Akron Pros",
                host_score=43,
                is_playoff=False
            ),
            Game(
                season_year=1922,
                week=2,
                guest_name="Muncie Flyers",
                guest_score=0,
                host_name="Rock Island Independents",
                host_score=45,
                is_playoff=False
            ),
        ]
        for game in games_in:
            sqla.session.add(game)
        sqla.session.commit()

        # Act
        filter_year = 1921
        test_repo = GameRepository()
        games_out = test_repo.get_games_by_season_year(None)

    # Assert
    assert games_out == []


def test_get_games_by_season_year_when_season_year_arg_is_not_none_should_return_games_for_specified_season_year(
        test_app
):
    with test_app.app_context():
        # Arrange
        db_init.init_db()

        games_in = [
            Game(
                season_year=1920,
                week=1,
                guest_name="St. Paul Ideals",
                guest_score=0,
                host_name="Rock Island Independents",
                host_score=48,
                is_playoff=False
            ),
            Game(
                season_year=1920,
                week=2,
                guest_name="Wheeling Stogies",
                guest_score=0,
                host_name="Akron Pros",
                host_score=43,
                is_playoff=False
            ),
            Game(
                season_year=1920,
                week=2,
                guest_name="Muncie Flyers",
                guest_score=0,
                host_name="Rock Island Independents",
                host_score=45,
                is_playoff=False
            ),
            Game(
                season_year=1921,
                week=1,
                guest_name="St. Paul Ideals",
                guest_score=0,
                host_name="Rock Island Independents",
                host_score=48,
                is_playoff=False
            ),
            Game(
                season_year=1921,
                week=2,
                guest_name="Wheeling Stogies",
                guest_score=0,
                host_name="Akron Pros",
                host_score=43,
                is_playoff=False
            ),
            Game(
                season_year=1921,
                week=2,
                guest_name="Muncie Flyers",
                guest_score=0,
                host_name="Rock Island Independents",
                host_score=45,
                is_playoff=False
            ),
            Game(
                season_year=1922,
                week=1,
                guest_name="St. Paul Ideals",
                guest_score=0,
                host_name="Rock Island Independents",
                host_score=48,
                is_playoff=False
            ),
            Game(
                season_year=1922,
                week=2,
                guest_name="Wheeling Stogies",
                guest_score=0,
                host_name="Akron Pros",
                host_score=43,
                is_playoff=False
            ),
            Game(
                season_year=1922,
                week=2,
                guest_name="Muncie Flyers",
                guest_score=0,
                host_name="Rock Island Independents",
                host_score=45,
                is_playoff=False
            ),
        ]
        for game in games_in:
            sqla.session.add(game)
        sqla.session.commit()

        # Act
        filter_year = 1921
        test_repo = GameRepository()
        games_out = test_repo.get_games_by_season_year(filter_year)

    # Assert
    for game in games_out:
        assert game.season_year == filter_year


def test_get_games_by_season_year_and_week_when_season_year_arg_is_none_should_return_empty_list(
        test_app
):
    with test_app.app_context():
        # Arrange
        db_init.init_db()

        games_in = [
            Game(
                season_year=1920,
                week=1,
                guest_name="St. Paul Ideals",
                guest_score=0,
                host_name="Rock Island Independents",
                host_score=48,
                is_playoff=False
            ),
            Game(
                season_year=1920,
                week=2,
                guest_name="Wheeling Stogies",
                guest_score=0,
                host_name="Akron Pros",
                host_score=43,
                is_playoff=False
            ),
            Game(
                season_year=1920,
                week=3,
                guest_name="Muncie Flyers",
                guest_score=0,
                host_name="Rock Island Independents",
                host_score=45,
                is_playoff=False
            ),
            Game(
                season_year=1921,
                week=1,
                guest_name="St. Paul Ideals",
                guest_score=0,
                host_name="Rock Island Independents",
                host_score=48,
                is_playoff=False
            ),
            Game(
                season_year=1921,
                week=2,
                guest_name="Wheeling Stogies",
                guest_score=0,
                host_name="Akron Pros",
                host_score=43,
                is_playoff=False
            ),
            Game(
                season_year=1921,
                week=3,
                guest_name="Muncie Flyers",
                guest_score=0,
                host_name="Rock Island Independents",
                host_score=45,
                is_playoff=False
            ),
            Game(
                season_year=1922,
                week=1,
                guest_name="St. Paul Ideals",
                guest_score=0,
                host_name="Rock Island Independents",
                host_score=48,
                is_playoff=False
            ),
            Game(
                season_year=1922,
                week=2,
                guest_name="Wheeling Stogies",
                guest_score=0,
                host_name="Akron Pros",
                host_score=43,
                is_playoff=False
            ),
            Game(
                season_year=1922,
                week=3,
                guest_name="Muncie Flyers",
                guest_score=0,
                host_name="Rock Island Independents",
                host_score=45,
                is_playoff=False
            ),
        ]
        for game in games_in:
            sqla.session.add(game)
        sqla.session.commit()

        # Act
        filter_year = None
        filter_week = 2
        test_repo = GameRepository()
        games_out = test_repo.get_games_by_season_year_and_week(filter_year, filter_week)

    # Assert
    assert games_out == []


def test_get_games_by_season_year_and_week_when_week_arg_is_none_should_return_empty_list(
        test_app
):
    with test_app.app_context():
        # Arrange
        db_init.init_db()

        games_in = [
            Game(
                season_year=1920,
                week=1,
                guest_name="St. Paul Ideals",
                guest_score=0,
                host_name="Rock Island Independents",
                host_score=48,
                is_playoff=False
            ),
            Game(
                season_year=1920,
                week=2,
                guest_name="Wheeling Stogies",
                guest_score=0,
                host_name="Akron Pros",
                host_score=43,
                is_playoff=False
            ),
            Game(
                season_year=1920,
                week=3,
                guest_name="Muncie Flyers",
                guest_score=0,
                host_name="Rock Island Independents",
                host_score=45,
                is_playoff=False
            ),
            Game(
                season_year=1921,
                week=1,
                guest_name="St. Paul Ideals",
                guest_score=0,
                host_name="Rock Island Independents",
                host_score=48,
                is_playoff=False
            ),
            Game(
                season_year=1921,
                week=2,
                guest_name="Wheeling Stogies",
                guest_score=0,
                host_name="Akron Pros",
                host_score=43,
                is_playoff=False
            ),
            Game(
                season_year=1921,
                week=3,
                guest_name="Muncie Flyers",
                guest_score=0,
                host_name="Rock Island Independents",
                host_score=45,
                is_playoff=False
            ),
            Game(
                season_year=1922,
                week=1,
                guest_name="St. Paul Ideals",
                guest_score=0,
                host_name="Rock Island Independents",
                host_score=48,
                is_playoff=False
            ),
            Game(
                season_year=1922,
                week=2,
                guest_name="Wheeling Stogies",
                guest_score=0,
                host_name="Akron Pros",
                host_score=43,
                is_playoff=False
            ),
            Game(
                season_year=1922,
                week=3,
                guest_name="Muncie Flyers",
                guest_score=0,
                host_name="Rock Island Independents",
                host_score=45,
                is_playoff=False
            ),
        ]
        for game in games_in:
            sqla.session.add(game)
        sqla.session.commit()

        # Act
        filter_year = 1921
        filter_week = None
        test_repo = GameRepository()
        games_out = test_repo.get_games_by_season_year_and_week(filter_year, filter_week)

    # Assert
    assert games_out == []


def test_get_games_by_season_year_and_week_when_args_are_not_none_should_return_games_for_specified_season_year_and_week(
        test_app
):
    with test_app.app_context():
        # Arrange
        db_init.init_db()

        games_in = [
            Game(
                season_year=1920,
                week=1,
                guest_name="St. Paul Ideals",
                guest_score=0,
                host_name="Rock Island Independents",
                host_score=48,
                is_playoff=False
            ),
            Game(
                season_year=1920,
                week=2,
                guest_name="Wheeling Stogies",
                guest_score=0,
                host_name="Akron Pros",
                host_score=43,
                is_playoff=False
            ),
            Game(
                season_year=1920,
                week=3,
                guest_name="Muncie Flyers",
                guest_score=0,
                host_name="Rock Island Independents",
                host_score=45,
                is_playoff=False
            ),
            Game(
                season_year=1921,
                week=1,
                guest_name="St. Paul Ideals",
                guest_score=0,
                host_name="Rock Island Independents",
                host_score=48,
                is_playoff=False
            ),
            Game(
                season_year=1921,
                week=2,
                guest_name="Wheeling Stogies",
                guest_score=0,
                host_name="Akron Pros",
                host_score=43,
                is_playoff=False
            ),
            Game(
                season_year=1921,
                week=3,
                guest_name="Muncie Flyers",
                guest_score=0,
                host_name="Rock Island Independents",
                host_score=45,
                is_playoff=False
            ),
            Game(
                season_year=1922,
                week=1,
                guest_name="St. Paul Ideals",
                guest_score=0,
                host_name="Rock Island Independents",
                host_score=48,
                is_playoff=False
            ),
            Game(
                season_year=1922,
                week=2,
                guest_name="Wheeling Stogies",
                guest_score=0,
                host_name="Akron Pros",
                host_score=43,
                is_playoff=False
            ),
            Game(
                season_year=1922,
                week=3,
                guest_name="Muncie Flyers",
                guest_score=0,
                host_name="Rock Island Independents",
                host_score=45,
                is_playoff=False
            ),
        ]
        for game in games_in:
            sqla.session.add(game)
        sqla.session.commit()

        # Act
        filter_year = 1921
        filter_week = 2
        test_repo = GameRepository()
        games_out = test_repo.get_games_by_season_year_and_week(filter_year, filter_week)

    # Assert
    for game in games_out:
        assert game.season_year == filter_year and game.week == filter_week


@patch('app.data.repositories.game_repository.Game')
def test_get_game_when_games_is_empty_should_return_none(fake_game, test_app):
    with test_app.app_context():
        # Arrange
        games_in = []
        fake_game.query.all.return_value = games_in

        # Act
        test_repo = GameRepository()
        game_out = test_repo.get_game(1)

    # Assert
    assert game_out is None


@patch('app.data.repositories.game_repository.Game')
def test_get_game_when_games_is_not_empty_and_game_is_not_found_should_return_none(fake_game, test_app):
    with test_app.app_context():
        # Arrange
        games_in = [
            Game(
                season_year=1920,
                week=1,
                guest_name="St. Paul Ideals",
                guest_score=0,
                host_name="Rock Island Independents",
                host_score=48,
                is_playoff=False
            ),
            Game(
                season_year=1920,
                week=2,
                guest_name="Wheeling Stogies",
                guest_score=0,
                host_name="Akron Pros",
                host_score=43,
                is_playoff=False
            ),
            Game(
                season_year=1920,
                week=2,
                guest_name="Muncie Flyers",
                guest_score=0,
                host_name="Rock Island Independents",
                host_score=45,
                is_playoff=False
            ),
        ]
        fake_game.query.all.return_value = games_in
        fake_game.query.get.return_value = None

        # Act
        test_repo = GameRepository()

        id = len(games_in) + 1
        game_out = test_repo.get_game(id)

    # Assert
    assert game_out is None


@patch('app.data.repositories.game_repository.Game')
def test_get_game_when_games_is_not_empty_and_game_is_found_should_return_game(fake_game, test_app):
    with test_app.app_context():
        # Arrange
        games_in = [
            Game(
                season_year=1920,
                week=1,
                guest_name="St. Paul Ideals",
                guest_score=0,
                host_name="Rock Island Independents",
                host_score=48,
                is_playoff=False
            ),
            Game(
                season_year=1920,
                week=2,
                guest_name="Wheeling Stogies",
                guest_score=0,
                host_name="Akron Pros",
                host_score=43,
                is_playoff=False
            ),
            Game(
                season_year=1920,
                week=2,
                guest_name="Muncie Flyers",
                guest_score=0,
                host_name="Rock Island Independents",
                host_score=45,
                is_playoff=False
            ),
        ]
        fake_game.query.all.return_value = games_in

        id = len(games_in) - 1
        fake_game.query.get.return_value = games_in[id]

        # Act
        test_repo = GameRepository()
        game_out = test_repo.get_game(id)

    # Assert
    assert game_out is games_in[id]


@patch('app.data.repositories.game_repository.sqla')
@patch('app.data.repositories.game_repository.game_factory')
def test_add_game_when_no_integrity_error_caught_should_add_game(fake_game_factory, fake_sqla, test_app):
    with test_app.app_context():
        # Arrange
        game_in = Game(
            season_year=1920,
            week=1,
            guest_name="St. Paul Ideals",
            guest_score=0,
            host_name="Rock Island Independents",
            host_score=48,
            is_playoff=False
        )
        fake_game_factory.create_game.return_value = game_in

        # Act
        test_repo = GameRepository()
        kwargs = {
            'season_year': 1920,
            'week': 1,
            'guest_name': "St. Paul Ideals",
            'guest_score': 0,
            'host_name': "Rock Island Independents",
            'host_score': 48,
            'is_playoff': False,
        }
        game_out = test_repo.add_game(**kwargs)

    # Assert
    fake_sqla.session.add.assert_called_once_with(game_in)
    fake_sqla.session.commit.assert_called_once()
    assert game_out is game_in


@patch('app.data.repositories.game_repository.sqla')
@patch('app.data.repositories.game_repository.game_factory')
def test_add_game_when_integrity_error_caught_should_rollback_transaction_and_reraise_error(
        fake_game_factory, fake_sqla, test_app
):
    with test_app.app_context():
        # Arrange
        game_in = Game(
            season_year=1920,
            week=1,
            guest_name="St. Paul Ideals",
            guest_score=0,
            host_name="Rock Island Independents",
            host_score=48,
            is_playoff=False
        )
        fake_game_factory.create_game.return_value = game_in
        fake_sqla.session.commit.side_effect = IntegrityError('statement', 'params', Exception())

        # Act
        test_repo = GameRepository()
        kwargs = {
            'season_year': 1920,
            'week': 1,
            'guest_name': "St. Paul Ideals",
            'guest_score': 0,
            'host_name': "Rock Island Independents",
            'host_score': 48,
            'is_playoff': False,
        }
        with pytest.raises(IntegrityError):
            game_out = test_repo.add_game(**kwargs)

    # Assert
    fake_sqla.session.rollback.assert_called_once()


@patch('app.data.repositories.game_repository.sqla')
def test_add_games_when_games_arg_is_empty_should_add_no_games(fake_sqla, test_app):
    # Arrange
    with test_app.app_context():
        # Act
        test_repo = GameRepository()

        game_args = ()
        games_out = test_repo.add_games(game_args)

    # Assert
    fake_sqla.session.add.assert_not_called()
    fake_sqla.session.commit.assert_called_once()
    assert games_out == []


@patch('app.data.repositories.game_repository.sqla')
@patch('app.data.repositories.game_repository.game_factory')
def test_add_games_when_games_arg_is_not_empty_and_no_integrity_error_caught_should_add_games(
        fake_game_factory, fake_sqla, test_app
):
    with test_app.app_context():
        # Arrange
        games_in = [
            Game(
                season_year=1920,
                week=1,
                guest_name="St. Paul Ideals",
                guest_score=0,
                host_name="Rock Island Independents",
                host_score=48,
                is_playoff=False
            ),
            Game(
                season_year=1920,
                week=2,
                guest_name="Wheeling Stogies",
                guest_score=0,
                host_name="Akron Pros",
                host_score=43,
                is_playoff=False
            ),
            Game(
                season_year=1920,
                week=2,
                guest_name="Muncie Flyers",
                guest_score=0,
                host_name="Rock Island Independents",
                host_score=45,
                is_playoff=False
            ),
        ]
        fake_game_factory.create_game.side_effect = games_in

        # Act
        test_repo = GameRepository()

        game_args = (
            {
                'season_year': 1920,
                'week': 1,
                'guest_name': "St. Paul Ideals",
                'guest_score': 0,
                'host_name': "Rock Island Independents",
                'host_score': 48,
                'is_playoff': False
            },
            {
                'season_year': 1920,
                'week': 2,
                'guest_name': "Wheeling Stogies",
                'guest_score': 0,
                'host_name': "Akron Pros",
                'host_score': 43,
                'is_playoff': False
            },
            {
                'season_year': 1920,
                'week': 2,
                'guest_name': "Muncie Flyers",
                'guest_score': 0,
                'host_name': "Rock Island Independents",
                'host_score': 45,
                'is_playoff': False
            },
        )
        games_out = test_repo.add_games(game_args)

    # Assert
    fake_sqla.session.add.assert_has_calls([
        call(games_in[0]),
        call(games_in[1]),
        call(games_in[2]),
    ])
    fake_sqla.session.commit.assert_called_once()
    assert games_out == games_in


@patch('app.data.repositories.game_repository.sqla')
@patch('app.data.repositories.game_repository.game_factory')
def test_add_games_when_games_arg_is_not_empty_and_integrity_error_caught_should_rollback_transaction_and_reraise_error(
        fake_game_factory, fake_sqla, test_app
):
    with test_app.app_context():
        # Arrange
        games_in = [
            Game(
                season_year=1920,
                week=1,
                guest_name="St. Paul Ideals",
                guest_score=0,
                host_name="Rock Island Independents",
                host_score=48,
                is_playoff=False
            ),
            Game(
                season_year=1920,
                week=2,
                guest_name="Wheeling Stogies",
                guest_score=0,
                host_name="Akron Pros",
                host_score=43,
                is_playoff=False
            ),
            Game(
                season_year=1920,
                week=2,
                guest_name="Muncie Flyers",
                guest_score=0,
                host_name="Rock Island Independents",
                host_score=45,
                is_playoff=False
            ),
        ]
        fake_game_factory.create_game.side_effect = games_in
        fake_sqla.session.commit.side_effect = IntegrityError('statement', 'params', Exception())

        # Act
        test_repo = GameRepository()

        game_args = (
            {
                'season_year': 1920,
                'week': 1,
                'guest_name': "St. Paul Ideals",
                'guest_score': 0,
                'host_name': "Rock Island Independents",
                'host_score': 48,
                'is_playoff': False
            },
            {
                'season_year': 1920,
                'week': 2,
                'guest_name': "Wheeling Stogies",
                'guest_score': 0,
                'host_name': "Akron Pros",
                'host_score': 43,
                'is_playoff': False
            },
            {
                'season_year': 1920,
                'week': 2,
                'guest_name': "Muncie Flyers",
                'guest_score': 0,
                'host_name': "Rock Island Independents",
                'host_score': 45,
                'is_playoff': False
            },
        )
        with pytest.raises(IntegrityError):
            games_out = test_repo.add_games(game_args)

    # Assert
    fake_sqla.session.rollback.assert_called_once()


@patch('app.data.repositories.game_repository.Game')
def test_game_exists_when_game_does_not_exist_should_return_false(fake_game, test_app):
    with test_app.app_context():
        # Arrange
        games_in = [
            Game(
                season_year=1920,
                week=1,
                guest_name="St. Paul Ideals",
                guest_score=0,
                host_name="Rock Island Independents",
                host_score=48,
                is_playoff=False
            ),
            Game(
                season_year=1920,
                week=2,
                guest_name="Wheeling Stogies",
                guest_score=0,
                host_name="Akron Pros",
                host_score=43,
                is_playoff=False
            ),
            Game(
                season_year=1920,
                week=2,
                guest_name="Muncie Flyers",
                guest_score=0,
                host_name="Rock Island Independents",
                host_score=45,
                is_playoff=False
            ),
        ]
        fake_game.query.all.return_value = games_in
        fake_game.query.get.return_value = None

        # Act
        test_repo = GameRepository()
        game_exists = test_repo.game_exists(id=1)

    # Assert
    assert not game_exists


@patch('app.data.repositories.game_repository.Game')
def test_game_exists_when_game_exists_should_return_true(fake_game, test_app):
    with test_app.app_context():
        # Arrange
        games_in = [
            Game(
                season_year=1920,
                week=1,
                guest_name="St. Paul Ideals",
                guest_score=0,
                host_name="Rock Island Independents",
                host_score=48,
                is_playoff=False
            ),
            Game(
                season_year=1920,
                week=2,
                guest_name="Wheeling Stogies",
                guest_score=0,
                host_name="Akron Pros",
                host_score=43,
                is_playoff=False
            ),
            Game(
                season_year=1920,
                week=2,
                guest_name="Muncie Flyers",
                guest_score=0,
                host_name="Rock Island Independents",
                host_score=45,
                is_playoff=False
            ),
        ]
        fake_game.query.all.return_value = games_in
        fake_game.query.get.return_value = games_in[1]

        # Act
        test_repo = GameRepository()
        game_exists = test_repo.game_exists(id=1)

    # Assert
    assert game_exists


def test_update_game_when_id_not_in_kwargs_should_raise_value_error(test_app):
    # Arrange
    with test_app.app_context():
        # Act
        test_repo = GameRepository()
        kwargs = {
            'season_year': 1920,
            'week': 1,
            'guest_name': "St. Paul Ideals",
            'guest_score': 0,
            'host_name': "Rock Island Independents",
            'host_score': 48,
            'is_playoff': False,
        }
        with pytest.raises(ValueError) as err:
            game_updated = test_repo.update_game(**kwargs)

    # Assert
    assert err.value.args[0] == "ID must be provided for existing Game."


@patch('app.data.repositories.game_repository.sqla')
@patch('app.data.repositories.game_repository.GameRepository.game_exists')
def test_update_game_when_id_is_in_kwargs_and_no_game_exists_with_id_should_return_game_and_not_update_database(
        fake_game_exists, fake_sqla, test_app
):
    with test_app.app_context():
        # Arrange
        fake_game_exists.return_value = False

        # Act
        test_repo = GameRepository()
        kwargs = {
            'id': 1,
            'season_year': 1920,
            'week': 1,
            'guest_name': "St. Paul Ideals",
            'guest_score': 0,
            'host_name': "Rock Island Independents",
            'host_score': 48,
            'is_playoff': False,
        }
        try:
            game_updated = test_repo.update_game(**kwargs)
        except ValueError as err:
            assert False

    # Assert
    fake_sqla.session.add.assert_not_called()
    fake_sqla.session.commit.assert_not_called()
    assert isinstance(game_updated, Game)
    assert game_updated.id == kwargs['id']
    assert game_updated.season_year == kwargs['season_year']
    assert game_updated.week == kwargs['week']
    assert game_updated.guest_name == kwargs['guest_name']
    assert game_updated.guest_score == kwargs['guest_score']
    assert game_updated.host_name == kwargs['host_name']
    assert game_updated.host_score == kwargs['host_score']
    assert game_updated.is_playoff == kwargs['is_playoff']


@patch('app.data.repositories.game_repository.sqla')
@patch('app.data.repositories.game_repository.game_factory')
@patch('app.data.repositories.game_repository.Game')
@patch('app.data.repositories.game_repository.GameRepository.game_exists')
def test_update_game_when_id_is_in_kwargs_and_game_exists_with_id_and_no_integrity_error_caught_should_return_game_and_update_database(
        fake_game_exists, fake_game, fake_game_factory, fake_sqla, test_app
):
    with test_app.app_context():
        # Arrange
        fake_game_exists.return_value = True

        games = [
            Game(
                id=1,
                season_year=1920,
                week=1,
                guest_name="St. Paul Ideals",
                guest_score=0,
                host_name="Rock Island Independents",
                host_score=48,
                is_playoff=False
            ),
            Game(
                id=2,
                season_year=1920,
                week=2,
                guest_name="Wheeling Stogies",
                guest_score=0,
                host_name="Akron Pros",
                host_score=43,
                is_playoff=False
            ),
            Game(
                id=3,
                season_year=1920,
                week=2,
                guest_name="Muncie Flyers",
                guest_score=0,
                host_name="Rock Island Independents",
                host_score=45,
                is_playoff=False
            ),
        ]
        fake_game.query.all.return_value = games

        old_game = games[1]
        fake_game.query.get.return_value = old_game

        new_game = Game(
            id=2,
            season_year=1920,
            week=2,
            guest_name="Columbus Panhandles",
            guest_score=0,
            host_name="Dayton Triangles",
            host_score=14,
            is_playoff=False
        )

        fake_game_factory.create_game.return_value = new_game

        # Act
        test_repo = GameRepository()
        kwargs = {
            'id': 2,
            'season_year': 1920,
            'week': 2,
            'guest_name': "Columbus Panhandles",
            'guest_score': 0,
            'host_name': "Dayton Triangles",
            'host_score': 14,
            'is_playoff': False,
        }
        try:
            game_updated = test_repo.update_game(**kwargs)
        except ValueError:
            assert False

    # Assert
    fake_sqla.session.add.assert_called_once_with(old_game)
    fake_sqla.session.commit.assert_called_once()
    assert isinstance(game_updated, Game)
    assert game_updated.id == kwargs['id']
    assert game_updated.season_year == kwargs['season_year']
    assert game_updated.week == kwargs['week']
    assert game_updated.guest_name == kwargs['guest_name']
    assert game_updated.guest_score == kwargs['guest_score']
    assert game_updated.host_name == kwargs['host_name']
    assert game_updated.host_score == kwargs['host_score']
    assert game_updated.is_playoff == kwargs['is_playoff']
    assert game_updated is new_game


@patch('app.data.repositories.game_repository.sqla')
@patch('app.data.repositories.game_repository.game_factory')
@patch('app.data.repositories.game_repository.Game')
@patch('app.data.repositories.game_repository.GameRepository.game_exists')
def test_update_game_when_id_is_in_kwargs_and_game_exists_with_id_and_integrity_error_caught_should_rollback_transaction_and_reraise_error(
        fake_game_exists, fake_game, fake_game_factory, fake_sqla, test_app
):
    with test_app.app_context():
        # Arrange
        fake_game_exists.return_value = True

        games = [
            Game(
                id=1,
                season_year=1920,
                week=1,
                guest_name="St. Paul Ideals",
                guest_score=0,
                host_name="Rock Island Independents",
                host_score=48,
                is_playoff=False
            ),
            Game(
                id=2,
                season_year=1920,
                week=2,
                guest_name="Wheeling Stogies",
                guest_score=0,
                host_name="Akron Pros",
                host_score=43,
                is_playoff=False
            ),
            Game(
                id=3,
                season_year=1920,
                week=2,
                guest_name="Muncie Flyers",
                guest_score=0,
                host_name="Rock Island Independents",
                host_score=45,
                is_playoff=False
            ),
        ]
        fake_game.query.all.return_value = games

        old_game = games[1]
        fake_game.query.get.return_value = old_game

        new_game = Game(
            id=2,
            season_year=1920,
            week=2,
            guest_name="Columbus Panhandles",
            guest_score=0,
            host_name="Dayton Triangles",
            host_score=14,
            is_playoff=False
        )
        fake_game_factory.create_game.return_value = new_game

        fake_sqla.session.commit.side_effect = IntegrityError('statement', 'params', Exception())

        # Act
        test_repo = GameRepository()
        kwargs = {
            'id': 2,
            'season_year': 1920,
            'week': 2,
            'guest_name': "Columbus Panhandles",
            'guest_score': 0,
            'host_name': "Dayton Triangles",
            'host_score': 14,
            'is_playoff': False,
        }
        with pytest.raises(IntegrityError):
            game_updated = test_repo.update_game(**kwargs)

    # Assert
    fake_sqla.session.rollback.assert_called_once()


@patch('app.data.repositories.game_repository.sqla')
@patch('app.data.repositories.game_repository.Game')
def test_delete_game_when_game_does_not_exist_should_return_none_and_not_delete_game_from_database(
        fake_game, fake_sqla, test_app
):
    with test_app.app_context():
        # Arrange
        games_in = [
            Game(
                season_year=1920,
                week=1,
                guest_name="St. Paul Ideals",
                guest_score=0,
                host_name="Rock Island Independents",
                host_score=48,
                is_playoff=False
            ),
            Game(
                season_year=1920,
                week=2,
                guest_name="Wheeling Stogies",
                guest_score=0,
                host_name="Akron Pros",
                host_score=43,
                is_playoff=False
            ),
            Game(
                season_year=1920,
                week=2,
                guest_name="Muncie Flyers",
                guest_score=0,
                host_name="Rock Island Independents",
                host_score=45,
                is_playoff=False
            ),
        ]
        fake_game.query.all.return_value = games_in
        fake_game.query.get.return_value = None

        id = 1

        # Act
        test_repo = GameRepository()
        game_deleted = test_repo.delete_game(id)

    # Assert
    assert game_deleted is None
    fake_sqla.session.delete.assert_not_called()
    fake_sqla.session.commit.assert_not_called()


@patch('app.data.repositories.game_repository.sqla')
@patch('app.data.repositories.game_repository.Game')
def test_delete_game_when_game_exists_should_return_game_and_delete_game_from_database(
        fake_game, fake_sqla, test_app
):
    with test_app.app_context():
        # Arrange
        games_in = [
            Game(
                season_year=1920,
                week=1,
                guest_name="St. Paul Ideals",
                guest_score=0,
                host_name="Rock Island Independents",
                host_score=48,
                is_playoff=False
            ),
            Game(
                season_year=1920,
                week=2,
                guest_name="Wheeling Stogies",
                guest_score=0,
                host_name="Akron Pros",
                host_score=43,
                is_playoff=False
            ),
            Game(
                season_year=1920,
                week=2,
                guest_name="Muncie Flyers",
                guest_score=0,
                host_name="Rock Island Independents",
                host_score=45,
                is_playoff=False
            ),
        ]
        fake_game.query.all.return_value = games_in

        id = 1
        fake_game.query.get.return_value = games_in[id]

        # Act
        test_repo = GameRepository()
        game_deleted = test_repo.delete_game(id)

    # Assert
    fake_sqla.session.delete.assert_called_once_with(game_deleted)
    fake_sqla.session.commit.assert_called_once()
    assert game_deleted is games_in[id]
