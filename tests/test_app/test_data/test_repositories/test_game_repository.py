import pytest

from unittest.mock import patch, call

from app import create_app
from app.data.models.game import Game
from app.data.models.league_season import LeagueSeason
from app.data.models.team_season import TeamSeason
from app.data.repositories.game_repository import GameRepository


@patch('app.data.repositories.game_repository.Game')
def test_get_games_should_get_games(fake_game):
    # Act
    test_app = create_app()
    with test_app.app_context():
        test_repo = GameRepository()
        games = test_repo.get_games()

    # Assert
    fake_game.query.all.assert_called_once()
    assert games == fake_game.query.all.return_value


@patch('app.data.repositories.game_repository.GameRepository.get_games')
def test_get_game_when_games_is_empty_should_return_none(fake_get_games):
    test_app = create_app()
    with test_app.app_context():
        # Arrange
        games = []
        fake_get_games.return_value = games

        # Act
        test_repo = GameRepository()
        game = test_repo.get_game(id=1)

    # Assert
    assert game is None


@patch('app.data.repositories.game_repository.Game')
@patch('app.data.repositories.game_repository.GameRepository.get_games')
def test_get_game_when_games_is_not_empty_and_game_is_not_found_should_return_none(
        fake_get_games, fake_game
):
    test_app = create_app()
    with test_app.app_context():
        # Arrange
        games = [
            Game(season_year=1, week=1, guest_name="Guest1", guest_score=1, host_name="Host1", host_score=2),
            Game(season_year=1, week=1, guest_name="Guest2", guest_score=2, host_name="Host2", host_score=1),
            Game(season_year=1, week=1, guest_name="Guest3", guest_score=2, host_name="Host3", host_score=2),
        ]
        fake_get_games.return_value = games

        id = len(games) + 1

        # Act
        test_repo = GameRepository()
        game = test_repo.get_game(id=id)

    # Assert
    fake_game.query.get.assert_called_once_with(id)
    assert game == fake_game.query.get.return_value


@patch('app.data.repositories.game_repository.Game')
@patch('app.data.repositories.game_repository.GameRepository.get_games')
def test_get_game_when_games_is_not_empty_and_game_is_found_should_return_game(fake_get_games, fake_game):
    test_app = create_app()
    with test_app.app_context():
        # Arrange
        games = [
            Game(season_year=1, week=1, guest_name="Guest1", guest_score=1, host_name="Host1", host_score=2),
            Game(season_year=1, week=1, guest_name="Guest2", guest_score=2, host_name="Host2", host_score=1),
            Game(season_year=1, week=1, guest_name="Guest3", guest_score=2, host_name="Host3", host_score=2),
        ]
        fake_get_games.return_value = games

        id = len(games) - 1

        # Act
        test_repo = GameRepository()
        game = test_repo.get_game(id=id)

    # Assert
    fake_game.query.get.assert_called_once_with(id)
    assert game == fake_game.query.get.return_value


@patch('app.data.repositories.game_repository.sqla')
def test_add_game_should_add_game(fake_sqla):
    # Arrange
    test_app = create_app()
    with test_app.app_context():
        # Act
        test_repo = GameRepository()
        game_in = Game(season_year=1, week=2, guest_name="Guest4", guest_score=3, host_name="Host4", host_score=3)
        game_out = test_repo.add_game(game_in)

    # Assert
    fake_sqla.session.add.assert_called_once_with(game_in)
    fake_sqla.session.commit.assert_called_once()
    assert game_out is game_in


@patch('app.data.repositories.game_repository.sqla')
def test_add_games_when_games_arg_is_empty_should_add_no_games(fake_sqla):
    # Arrange
    test_app = create_app()
    with test_app.app_context():
        # Act
        test_repo = GameRepository()
        games_in = ()
        games_out = test_repo.add_games(games_in)

    # Assert
    fake_sqla.session.add.assert_not_called()
    fake_sqla.session.commit.assert_called_once()
    assert games_out is games_in


@patch('app.data.repositories.game_repository.sqla')
def test_add_games_when_games_arg_is_not_empty_should_add_games(fake_sqla):
    # Arrange
    test_app = create_app()
    with test_app.app_context():
        # Act
        test_repo = GameRepository()
        games_in = (
            Game(season_year=1, week=2, guest_name="Guest4", guest_score=1, host_name="Host4", host_score=2),
            Game(season_year=1, week=2, guest_name="Guest5", guest_score=2, host_name="Host5", host_score=1),
            Game(season_year=1, week=2, guest_name="Guest6", guest_score=2, host_name="Host6", host_score=2),
        )
        games_out = test_repo.add_games(games_in)

    # Assert
    fake_sqla.session.add.assert_has_calls([
        call(games_in[0]),
        call(games_in[1]),
        call(games_in[2]),
    ])
    fake_sqla.session.commit.assert_called_once()
    assert games_out is games_in


@patch('app.data.repositories.game_repository.sqla')
@patch('app.data.repositories.game_repository.exists')
def test_game_exists_should_query_database(fake_exists, fake_sqla):
    # Arrange
    test_app = create_app()
    with test_app.app_context():
        # Act
        test_repo = GameRepository()
        game_exists = test_repo.game_exists(id=1)

    # Assert
    fake_exists.assert_called_once()
    fake_exists.return_value.where.assert_called_once()
    fake_sqla.session.query.assert_called_once_with(fake_exists.return_value.where.return_value)
    fake_sqla.session.query.return_value.scalar.assert_called_once()
    assert game_exists == fake_sqla.session.query.return_value.scalar.return_value


@patch('app.data.repositories.game_repository.GameRepository.game_exists')
def test_update_game_when_game_does_not_exist_should_return_game(fake_game_exists):
    # Arrange
    fake_game_exists.return_value = False

    test_app = create_app()
    with test_app.app_context():
        # Act
        test_repo = GameRepository()
        game_to_update = Game(season_year=1, week=2, guest_name="Guest4", guest_score=1, host_name="Host4", host_score=2)
        game_updated = test_repo.update_game(game_to_update)

    # Assert
    fake_game_exists.assert_called_once_with(game_to_update.id)
    assert game_updated is game_to_update


@patch('app.data.repositories.game_repository.sqla')
@patch('app.data.repositories.game_repository.GameRepository.get_game')
@patch('app.data.repositories.game_repository.GameRepository.game_exists')
def test_update_game_when_game_exists_should_update_and_return_game(
        fake_game_exists, fake_get_game, fake_sqla
):
    # Arrange
    test_app = create_app()
    with test_app.app_context():
        fake_game_exists.return_value = True
        old_game = Game(season_year=1, week=1, guest_name="Guest1", guest_score=1, host_name="Host1", host_score=2)
        fake_get_game.return_value = old_game

        new_game = Game(season_year=99, week=99, guest_name="Guest99", guest_score=99, host_name="Host99", host_score=99)

        # Act
        test_repo = GameRepository()
        game_updated = test_repo.update_game(new_game)

    # Assert
    fake_game_exists.assert_called_once_with(old_game.id)
    fake_get_game.assert_called_once_with(old_game.id)
    assert game_updated.season_year == new_game.season_year
    assert game_updated.week == new_game.week
    assert game_updated.guest_name == new_game.guest_name
    assert game_updated.guest_score == new_game.guest_score
    assert game_updated.host_name == new_game.host_name
    assert game_updated.host_score == new_game.host_score
    fake_sqla.session.add.assert_called_once_with(old_game)
    fake_sqla.session.commit.assert_called_once()
    assert game_updated is new_game


@patch('app.data.repositories.game_repository.GameRepository.game_exists')
def test_delete_game_when_game_does_not_exist_should_return_none(fake_game_exists):
    # Arrange
    fake_game_exists.return_value = False
    id = 1

    test_app = create_app()
    with test_app.app_context():
        # Act
        test_repo = GameRepository()
        game_deleted = test_repo.delete_game(id=id)

    # Assert
    fake_game_exists.assert_called_once_with(id)
    assert game_deleted is None


@patch('app.data.repositories.game_repository.sqla')
@patch('app.data.repositories.game_repository.GameRepository.get_game')
@patch('app.data.repositories.game_repository.GameRepository.game_exists')
def test_delete_game_when_game_exists_should_return_game(fake_game_exists, fake_get_game, fake_sqla):
    # Arrange
    fake_game_exists.return_value = True
    id = 1

    test_app = create_app()
    with test_app.app_context():
        # Act
        test_repo = GameRepository()
        game_deleted = test_repo.delete_game(id=id)

    # Assert
    fake_game_exists.assert_called_once_with(id)
    fake_get_game.assert_called_once_with(id)
    fake_sqla.session.delete.assert_called_once_with(fake_get_game.return_value)
    fake_sqla.session.commit.assert_called_once()
    return game_deleted is fake_get_game.return_value
