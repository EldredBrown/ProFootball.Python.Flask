from unittest.mock import patch, call

import pytest

from sqlalchemy.exc import IntegrityError

from app import sqla
from instance.test_db import db_init
from test_app import create_app

from app.data.models.game import Game
from app.data.repositories.game_repository import GameRepository


@pytest.fixture
def test_app():
    return create_app()


@pytest.fixture
def test_repo():
    return GameRepository()


def test_get_games_should_get_games(test_app, test_repo):
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
        games_out = test_repo.get_games()

    # Assert
    assert games_out == games_in


def test_get_games_by_season_when_season_year_arg_is_none_should_return_empty_list(test_app, test_repo):
    with test_app.app_context():
        # Arrange
        db_init.init_db()

        games_in = (
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
        )
        for game in games_in:
            sqla.session.add(game)
        sqla.session.commit()

        # Act
        filter_year = None
        games_out = test_repo.get_games_by_season(filter_year)

    # Assert
    assert games_out == []


def test_get_games_by_season_when_season_year_arg_is_not_none_should_return_games_for_specified_season_year(
        test_app, test_repo
):
    with test_app.app_context():
        # Arrange
        db_init.init_db()

        games_in = (
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
        )
        for game in games_in:
            sqla.session.add(game)
        sqla.session.commit()

        # Act
        filter_year = 1921
        games_out = test_repo.get_games_by_season(filter_year)

    # Assert
    for game in games_out:
        assert game.season_year == filter_year


def test_get_games_by_season_league_and_week_when_args_are_none_should_return_empty_list(
        test_app, test_repo
):
    with test_app.app_context():
        # Arrange
        db_init.init_db()

        games_in = []
        for s in range(1920, 1923):
            for l in range(1, 4):
                for w in range(1, 4):
                    for t in range(1, 4):
                        game = Game(
                            season_year=s,
                            league_id=l,
                            week=w,
                            guest_name=f"Guest {t}",
                            guest_score=0,
                            host_name=f"Guest {t}",
                            host_score=0
                        )
                        games_in.append(game)
                        sqla.session.add(game)
        sqla.session.commit()

        # Act
        season_year = None
        league_id = None
        filter_week = None
        games_out = test_repo.get_games_by_season_league_and_week(season_year, league_id, filter_week)

    # Assert
    assert games_out == []


def test_get_games_by_season_league_and_week_when_season_year_arg_is_not_none_should_return_all_games_for_matching_season(
        test_app, test_repo
):
    with test_app.app_context():
        # Arrange
        db_init.init_db()

        games_in = []
        for s in range(1920, 1923):
            for l in range(1, 4):
                for w in range(1, 4):
                    for t in range(1, 4):
                        game = Game(
                            season_year=s,
                            league_id=l,
                            week=w,
                            guest_name=f"Guest {t}",
                            guest_score=0,
                            host_name=f"Guest {t}",
                            host_score=0
                        )
                        games_in.append(game)
                        sqla.session.add(game)
        sqla.session.commit()

        # Act
        season_year = 1922
        league_id = None
        filter_week = None
        games_out = test_repo.get_games_by_season_league_and_week(season_year, league_id, filter_week)

        # Assert
        assert games_out == [
            g for g in games_in if g.season_year == season_year
        ]


def test_get_games_by_season_league_and_week_when_season_year_and_league_id_args_are_not_none_should_return_all_games_for_matching_season_and_league(
        test_app, test_repo
):
    with test_app.app_context():
        # Arrange
        db_init.init_db()

        games_in = []
        for s in range(1920, 1923):
            for l in range(1, 4):
                for w in range(1, 4):
                    for t in range(1, 4):
                        game = Game(
                            season_year=s,
                            league_id=l,
                            week=w,
                            guest_name=f"Guest {t}",
                            guest_score=0,
                            host_name=f"Guest {t}",
                            host_score=0
                        )
                        games_in.append(game)
                        sqla.session.add(game)
        sqla.session.commit()

        # Act
        season_year = 1922
        league_id = 3
        filter_week = None
        games_out = test_repo.get_games_by_season_league_and_week(season_year, league_id, filter_week)

        # Assert
        assert games_out == [
            g for g in games_in if g.season_year == season_year and g.league_id == league_id
        ]


def test_get_games_by_season_league_and_week_when_all_args_are_not_none_should_return_all_games_for_matching_season_and_league_and_week(
        test_app, test_repo
):
    with test_app.app_context():
        # Arrange
        db_init.init_db()

        games_in = []
        for s in range(1920, 1923):
            for l in range(1, 4):
                for w in range(1, 4):
                    for t in range(1, 4):
                        game = Game(
                            season_year=s,
                            league_id=l,
                            week=w,
                            guest_name=f"Guest {t}",
                            guest_score=0,
                            host_name=f"Guest {t}",
                            host_score=0
                        )
                        games_in.append(game)
                        sqla.session.add(game)
        sqla.session.commit()

        # Act
        season_year = 1922
        league_id = 3
        filter_week = 1
        games_out = test_repo.get_games_by_season_league_and_week(season_year, league_id, filter_week)

        # Assert
        assert games_out == [
            g for g in games_in if g.season_year == season_year and g.league_id == league_id and g.week == filter_week
        ]


def test_get_game_when_games_is_empty_should_return_none(test_app, test_repo):
    with test_app.app_context():
        # Arrange
        db_init.init_db()

        # Act
        game_out = test_repo.get_game(1)

    # Assert
    assert game_out is None


def test_get_game_when_games_is_not_empty_and_game_is_not_found_should_return_none(test_app, test_repo):
    with test_app.app_context():
        # Arrange
        db_init.init_db()

        games_in = (
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
        )
        for game in games_in:
            sqla.session.add(game)
        sqla.session.commit()

        # Act
        game_out = test_repo.get_game(id=-1)

    # Assert
    assert game_out is None


def test_get_game_when_game_is_found_should_return_game(test_app, test_repo):
    with test_app.app_context():
        # Arrange
        db_init.init_db()

        games_in = (
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
        )
        for game in games_in:
            sqla.session.add(game)
        sqla.session.commit()

        # Act
        game_out = test_repo.get_game(id=3)

    # Assert
    assert game_out is games_in[2]


def test_get_game_by_season_week_guest_and_host_when_games_is_empty_should_return_none(
        test_app, test_repo
):
    with test_app.app_context():
        # Arrange
        db_init.init_db()

        # Act
        game_out = test_repo.get_game_by_season_week_guest_and_host(1920, 1, "Guest", "Host")

    # Assert
    assert game_out is None


def test_get_game_by_season_week_guest_and_host_when_games_is_not_empty_and_game_is_not_found_should_return_none(
        test_app, test_repo
):
    with test_app.app_context():
        # Arrange
        db_init.init_db()

        games_in = (
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
        )
        for game in games_in:
            sqla.session.add(game)
        sqla.session.commit()

        # Act
        game_out = test_repo.get_game_by_season_week_guest_and_host(1920, 2, "Guest", "Host")

    # Assert
    assert game_out is None


def test_get_game_by_season_week_guest_and_host_when_game_is_found_should_return_game(test_app, test_repo):
    with test_app.app_context():
        # Arrange
        db_init.init_db()

        games_in = (
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
        )
        for game in games_in:
            sqla.session.add(game)
        sqla.session.commit()

        # Act
        game_out = test_repo.get_game_by_season_week_guest_and_host(
            1920, 2, "Wheeling Stogies", "Akron Pros"
        )

    # Assert
    assert game_out is games_in[1]


@patch('app.data.repositories.game_repository.try_commit')
@patch('app.data.repositories.game_repository.sqla')
def test_add_game_when_no_integrity_error_caught_should_add_game(
        fake_sqla, fake_try_commit, test_app, test_repo
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

        # Act
        game_out = test_repo.add_game(game_in)

    # Assert
    fake_sqla.session.add.assert_called_once_with(game_in)
    fake_try_commit.assert_called_once()
    assert game_out is game_in


@patch('app.data.repositories.game_repository.try_commit')
@patch('app.data.repositories.game_repository.sqla')
def test_add_game_when_integrity_error_caught_should_rollback_transaction_and_reraise_error(
        fake_sqla, fake_try_commit, test_app, test_repo
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
        fake_try_commit.side_effect = IntegrityError('statement', 'params', Exception())

        # Act
        with pytest.raises(IntegrityError):
            game_out = test_repo.add_game(game_in)

    # Assert
    fake_sqla.session.add.assert_called_once_with(game_in)
    fake_try_commit.assert_called_once()


@patch('app.data.repositories.game_repository.try_commit')
@patch('app.data.repositories.game_repository.sqla')
def test_add_games_when_games_arg_is_empty_should_add_no_games(
        fake_sqla, fake_try_commit, test_app, test_repo
):
    with test_app.app_context():
        # Arrange
        games_in = ()

        # Act
        games_out = test_repo.add_games(games_in)

    # Assert
    fake_sqla.session.add.assert_not_called()
    fake_try_commit.assert_called_once()
    assert games_out == tuple()


@patch('app.data.repositories.game_repository.try_commit')
@patch('app.data.repositories.game_repository.sqla')
def test_add_games_when_games_arg_is_not_empty_and_no_integrity_error_caught_should_add_games(
        fake_sqla, fake_try_commit, test_app, test_repo
):
    with test_app.app_context():
        # Arrange
        games_in = (
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
        )

        # Act
        games_out = test_repo.add_games(games_in)

    # Assert
    fake_sqla.session.add.assert_has_calls([
        call(games_in[0]),
        call(games_in[1]),
        call(games_in[2]),
    ])
    fake_try_commit.assert_called_once()
    assert games_out == games_in


@patch('app.data.repositories.game_repository.try_commit')
@patch('app.data.repositories.game_repository.sqla')
def test_add_games_when_integrity_error_caught_should_rollback_transaction_and_reraise_error(
        fake_sqla, fake_try_commit, test_app, test_repo
):
    with test_app.app_context():
        # Arrange
        games_in = (
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
        )
        fake_try_commit.side_effect = IntegrityError('statement', 'params', Exception())

        # Act
        with pytest.raises(IntegrityError):
            games_out = test_repo.add_games(games_in)

    # Assert
    fake_sqla.session.add.assert_has_calls([
        call(games_in[0]),
        call(games_in[1]),
        call(games_in[2]),
    ])
    fake_try_commit.assert_called_once()


def test_game_exists_when_game_does_not_exist_should_return_false(test_app, test_repo):
    with test_app.app_context():
        # Arrange
        db_init.init_db()

        games_in = (
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
        )
        for game in games_in:
            sqla.session.add(game)
        sqla.session.commit()

        id = -1

        # Act
        game_exists = test_repo.game_exists(id)

    # Assert
    assert not game_exists


def test_game_exists_when_game_exists_should_return_true(test_app, test_repo):
    with test_app.app_context():
        # Arrange
        db_init.init_db()

        games_in = (
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
        )
        for game in games_in:
            sqla.session.add(game)
        sqla.session.commit()

        id = 1

        # Act
        game_exists = test_repo.game_exists(id)

    # Assert
    assert game_exists


@patch('app.data.repositories.game_repository.try_commit')
@patch('app.data.repositories.game_repository.sqla')
@patch('app.data.repositories.game_repository.GameRepository.game_exists')
def test_update_game_when_no_game_exists_with_id_should_return_game_and_not_update_database(
        fake_game_exists, fake_sqla, fake_try_commit, test_app,
        test_repo
):
    with test_app.app_context():
        # Arrange
        fake_game_exists.return_value = False

        # Act
        game = Game(
            id=1,
            season_year=1920,
            week=1,
            guest_name="St. Paul Ideals",
            guest_score=0,
            host_name="Rock Island Independents",
            host_score=48,
            is_playoff=False,
        )
        try:
            game_updated = test_repo.update_game(game)
        except ValueError:
            assert False

    # Assert
    fake_sqla.session.add.assert_not_called()
    fake_try_commit.assert_not_called()
    assert isinstance(game_updated, Game)
    assert game_updated.id == game.id
    assert game_updated.season_year == game.season_year
    assert game_updated.week == game.week
    assert game_updated.guest_name == game.guest_name
    assert game_updated.guest_score == game.guest_score
    assert game_updated.host_name == game.host_name
    assert game_updated.host_score == game.host_score
    assert game_updated.winner_name == game.winner_name
    assert game_updated.winner_score == game.winner_score
    assert game_updated.loser_name == game.loser_name
    assert game_updated.loser_score == game.loser_score
    assert game_updated.is_playoff == game.is_playoff


@patch('app.data.repositories.game_repository.try_commit')
@patch('app.data.repositories.game_repository.sqla')
@patch('app.data.repositories.game_repository.GameRepository.game_exists')
def test_update_game_when_game_exists_with_id_and_no_integrity_error_caught_should_return_game_and_update_database(
        fake_game_exists, fake_sqla, fake_try_commit, test_app, test_repo
):
    with test_app.app_context():
        # Arrange
        fake_game_exists.return_value = True

        db_init.init_db()

        games = (
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
        )
        for game in games:
            sqla.session.add(game)
        sqla.session.commit()

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

        # Act
        try:
            game_updated = test_repo.update_game(new_game)
        except IntegrityError:
            assert False

    # Assert
    old_game = games[1]
    fake_sqla.session.add.assert_called_once_with(old_game)
    fake_try_commit.assert_called_once()
    assert isinstance(game_updated, Game)
    assert game_updated.id == new_game.id
    assert game_updated.season_year == new_game.season_year
    assert game_updated.week == new_game.week
    assert game_updated.guest_name == new_game.guest_name
    assert game_updated.guest_score == new_game.guest_score
    assert game_updated.host_name == new_game.host_name
    assert game_updated.host_score == new_game.host_score
    assert game_updated.winner_name == new_game.winner_name
    assert game_updated.winner_score == new_game.winner_score
    assert game_updated.loser_name == new_game.loser_name
    assert game_updated.loser_score == new_game.loser_score
    assert game_updated.is_playoff == new_game.is_playoff
    assert game_updated is new_game


@patch('app.data.repositories.game_repository.try_commit')
@patch('app.data.repositories.game_repository.sqla')
@patch('app.data.repositories.game_repository.GameRepository.game_exists')
def test_update_game_when_integrity_error_caught_should_rollback_transaction_and_reraise_error(
        fake_game_exists, fake_sqla, fake_try_commit, test_app,
        test_repo
):
    with test_app.app_context():
        # Arrange
        fake_game_exists.return_value = True

        db_init.init_db()

        games = (
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
        )
        for game in games:
            sqla.session.add(game)
        sqla.session.commit()

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

        fake_try_commit.side_effect = IntegrityError('statement', 'params', Exception())

        # Act
        with pytest.raises(IntegrityError):
            game_updated = test_repo.update_game(new_game)

    # Assert
    old_game = games[1]
    fake_sqla.session.add.assert_called_once_with(old_game)
    fake_try_commit.assert_called_once()


@patch('app.data.repositories.game_repository.try_commit')
@patch('app.data.repositories.game_repository.sqla')
def test_delete_game_when_game_does_not_exist_should_return_none_and_not_delete_game_from_database(
        fake_sqla, fake_try_commit, test_app, test_repo
):
    with test_app.app_context():
        # Arrange
        db_init.init_db()

        games = (
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
        )
        for game in games:
            sqla.session.add(game)
        sqla.session.commit()

        # Act
        game_deleted = test_repo.delete_game(id=-1)

    # Assert
    assert game_deleted is None
    fake_sqla.session.delete.assert_not_called()
    fake_try_commit.assert_not_called()


@patch('app.data.repositories.game_repository.try_commit')
@patch('app.data.repositories.game_repository.sqla')
def test_delete_game_when_game_exists_and_integrity_error_not_caught_should_return_game_and_delete_game_from_database(
        fake_sqla, fake_try_commit, test_app, test_repo
):
    with test_app.app_context():
        # Arrange
        db_init.init_db()

        games = (
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
        )
        for game in games:
            sqla.session.add(game)
        sqla.session.commit()

        # Act
        try:
            game_deleted = test_repo.delete_game(id=2)
        except IntegrityError:
            assert False

    # Assert
    fake_sqla.session.delete.assert_called_once_with(game_deleted)
    fake_try_commit.assert_called_once()
    assert game_deleted is games[1]


@patch('app.data.repositories.game_repository.try_commit')
@patch('app.data.repositories.game_repository.sqla')
def test_delete_game_when_integrity_error_caught_should_rollback_commit(
        fake_sqla, fake_try_commit, test_app, test_repo
):
    with test_app.app_context():
        # Arrange
        db_init.init_db()

        games = (
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
        )
        for game in games:
            sqla.session.add(game)
        sqla.session.commit()

        fake_try_commit.side_effect = IntegrityError('statement', 'params', Exception())

        # Act
        with pytest.raises(IntegrityError):
            game_deleted = test_repo.delete_game(id=2)

    # Assert
    fake_try_commit.assert_called_once()


def test_get_max_week_by_season_when_weeks_is_true_should_return_max_week(test_app, test_repo):
    with test_app.app_context():
        # Arrange
        db_init.init_db()

        games_in = (
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
        )
        for game in games_in:
            sqla.session.add(game)
        sqla.session.commit()

        # Act
        result = test_repo.get_max_week_by_season(season_year=1920)

    # Assert
    assert result == 3


def test_get_max_week_by_season_when_weeks_is_false_should_return_max_week(test_app, test_repo):
    with test_app.app_context():
        # Arrange
        db_init.init_db()

        # Act
        result = test_repo.get_max_week_by_season(season_year=1920)

    # Assert
    assert result is None
