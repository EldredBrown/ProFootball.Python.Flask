import pytest

from unittest.mock import Mock, patch

from app.data.errors import EntityNotFoundError
from app.data.models.game import Game
from app.services.constants import Direction
from app.services.game_service.game_service import GameService
from app.services.game_service.process_game_strategy.add_game_strategy import AddGameStrategy
from app.services.game_service.process_game_strategy.process_game_strategy import ProcessGameStrategy
from app.services.game_service.process_game_strategy.subtract_game_strategy import SubtractGameStrategy


@pytest.fixture()
@patch('app.services.game_service.game_service.ProcessGameStrategyFactory')
@patch('app.services.game_service.game_service.TeamSeasonRepository')
@patch('app.services.game_service.game_service.GameRepository')
def test_service(fake_game_repository, fake_team_season_repository, fake_process_game_strategy_factory):
    test_service = GameService(fake_game_repository, fake_team_season_repository, fake_process_game_strategy_factory)
    return test_service


def test_add_game_when_new_game_arg_is_none_should_raise_value_error(test_service):
    # Act and Assert
    with pytest.raises(ValueError):
        test_service.add_game(None)


@patch('app.services.game_service.game_service.Game')
def test_add_game_when_new_team_season_with_new_game_guest_and_season_is_in_datastore_should_add_game_to_repository(
        fake_game, test_service
):
    # Arrange
    test_service.team_season_repository.team_season_exists_with_team_name_and_season_year.side_effect = (True, False)
    strategy = Mock(ProcessGameStrategy)
    test_service.process_game_strategy_factory.create_strategy.return_value = strategy

    # Act
    try:
        test_service.add_game(fake_game)
    except EntityNotFoundError:
        assert False

    # Assert
    test_service.team_season_repository.team_season_exists_with_team_name_and_season_year.assert_called_once_with(
        fake_game.guest_name, fake_game.season_year
    )
    fake_game.decide_winner_and_loser.assert_called_once()
    test_service.game_repository.add_game.assert_any_call(fake_game)
    test_service.process_game_strategy_factory.create_strategy.assert_any_call(Direction.UP)
    strategy.process_game.assert_called_once_with(fake_game)


@patch('app.services.game_service.game_service.Game')
def test_add_game_when_new_team_seasons_with_new_game_guest_and_season_and_with_new_game_host_and_season_are_in_datastore_should_add_game_to_repository(
        fake_game, test_service
):
    # Arrange
    test_service.team_season_repository.team_season_exists_with_team_name_and_season_year.side_effect = (False, True)
    strategy = Mock(ProcessGameStrategy)
    test_service.process_game_strategy_factory.create_strategy.return_value = strategy

    # Act
    try:
        test_service.add_game(fake_game)
    except EntityNotFoundError:
        assert False

    # Assert
    test_service.team_season_repository.team_season_exists_with_team_name_and_season_year.assert_any_call(
        fake_game.guest_name, fake_game.season_year
    )
    test_service.team_season_repository.team_season_exists_with_team_name_and_season_year.assert_any_call(
        fake_game.host_name, fake_game.season_year
    )
    fake_game.decide_winner_and_loser.assert_called_once()
    test_service.game_repository.add_game.assert_any_call(fake_game)
    test_service.process_game_strategy_factory.create_strategy.assert_any_call(Direction.UP)
    strategy.process_game.assert_called_once_with(fake_game)


def test_add_game_when_team_season_with_new_game_guest_and_season_and_team_season_with_new_game_host_and_season_not_in_datastore_should_raise_entity_not_found_error(
        test_service
):
    # Arrange
    test_service.team_season_repository.team_season_exists_with_team_name_and_season_year.side_effect = (False, False)

    new_game = Game(season_year=1, week=1, guest_name="Guest", guest_score=0, host_name="Host", host_score=0)

    # Act and Assert
    with pytest.raises(EntityNotFoundError):
        test_service.add_game(new_game)

    test_service.team_season_repository.team_season_exists_with_team_name_and_season_year.assert_any_call(
        new_game.guest_name, new_game.season_year
    )


def test_edit_game_when_new_game_arg_is_none_should_raise_value_error(test_service):
    # Act and Assert
    with pytest.raises(ValueError):
        test_service.update_game(None, None)


def test_edit_game_when_old_game_arg_is_none_should_raise_value_error(test_service):
    # Arrange
    new_game = Game(season_year=1, week=1, guest_name="Guest", guest_score=0, host_name="Host", host_score=0)

    # Act and Assert
    with pytest.raises(ValueError):
        test_service.update_game(new_game, None)


def test_edit_game_when_selected_game_not_found_should_raise_entity_not_found_error(test_service):
    # Arrange
    test_service.game_repository.get_game.return_value = None

    new_game = Game(season_year=1, week=1, guest_name="Guest", guest_score=0, host_name="Host", host_score=0)
    old_game = Game(season_year=1, week=1, guest_name="Guest", guest_score=0, host_name="Host", host_score=0)

    # Act and Assert
    with pytest.raises(EntityNotFoundError):
        test_service.update_game(new_game, old_game)

    test_service.game_repository.get_game.assert_called_once_with(old_game.id)


def test_edit_game_when_args_are_not_none_and_selected_game_is_found_should_edit_game_in_repository(test_service):
    # Arrange
    selected_game = Mock(Game)
    test_service.game_repository.get_game.return_value = selected_game

    subtract_strategy = Mock(SubtractGameStrategy)
    add_strategy = Mock(AddGameStrategy)
    test_service.process_game_strategy_factory.create_strategy.side_effect = (subtract_strategy, add_strategy)

    new_game = Mock(Game)
    old_game = Mock(Game)

    # Act
    test_service.update_game(new_game, old_game)

    # Assert
    new_game.decide_winner_and_loser.assert_called()
    test_service.game_repository.update_game.assert_called_once_with(new_game)

    test_service.process_game_strategy_factory.create_strategy.assert_any_call(Direction.DOWN)
    subtract_strategy.process_game.assert_called_once_with(old_game)

    test_service.process_game_strategy_factory.create_strategy.assert_any_call(Direction.UP)
    add_strategy.process_game.assert_called_once_with(new_game)


def test_delete_game_when_game_with_passed_id_is_not_found_should_raise_entity_not_found_error(test_service):
    # Arrange
    test_service.game_repository.get_game.return_value = None

    # Act and Assert
    id = 1
    with pytest.raises(EntityNotFoundError):
        test_service.delete_game(id)


def test_delete_game_when_game_with_passed_id_is_found_should_delete_game_from_repository(test_service):
    # Arrange
    old_game = Mock(Game)
    test_service.game_repository.get_game.return_value = old_game

    strategy = Mock(SubtractGameStrategy)
    test_service.process_game_strategy_factory.create_strategy.return_value = strategy

    # Act
    id = 1
    test_service.delete_game(id)

    # Assert
    test_service.game_repository.get_game.assert_any_call(id)
    test_service.game_repository.delete_game.assert_any_call(id)
    test_service.process_game_strategy_factory.create_strategy.assert_any_call(Direction.DOWN)
    strategy.process_game.assert_called_once_with(old_game)
