import pytest

from unittest.mock import Mock, patch, call

from app.data.errors import EntityNotFoundError
from app.data.models.game import Game
from app.data.models.team_season import TeamSeason
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
    # Act
    with pytest.raises(ValueError) as err:
        test_service.add_game(None)

        # Assert
        assert err.value.args[0] == f"{type(GameService).__name__}.add_game: new_game"


@patch('app.services.game_service.game_service.Game')
def test_add_game_when_new_game_arg_is_not_none_and_no_team_season_found_for_guest_should_raise_entity_not_found_error(fake_game, test_service):
    # Arrange
    fake_game.guest_name = "Guest"
    fake_game.host_name = "Host"

    test_service.team_season_repository.get_team_season.return_value = None

    # Act
    with pytest.raises(EntityNotFoundError) as err:
        test_service.add_game(fake_game)
        assert err.value.args[0] == f"No team season found for '{fake_game.guest_name}' in year {fake_game.season_year}"

    # Assert
    test_service.team_season_repository.get_team_season.assert_called_once_with(fake_game.guest_name)


@patch('app.services.game_service.game_service.Game')
def test_add_game_when_team_season_found_for_guest_and_no_team_season_found_for_host_should_raise_entity_not_found_error(fake_game, test_service):
    # Arrange
    fake_game.guest_name = "Guest"
    fake_game.host_name = "Host"

    test_service.team_season_repository.get_team_season.side_effect = [Mock(TeamSeason), None]

    # Act
    with pytest.raises(EntityNotFoundError) as err:
        test_service.add_game(fake_game)
        assert err.value.args[0] == f"No team season found for '{fake_game.host_name}' in year {fake_game.season_year}"

    # Assert
    test_service.team_season_repository.get_team_season.assert_has_calls([
        call(fake_game.guest_name),
        call(fake_game.host_name),
    ])


@patch('app.services.game_service.game_service.Game')
def test_add_game_when_team_seasons_found_for_both_teams_should_add_game_to_repository(fake_game, test_service):
    # Arrange
    fake_game.guest_name = "Guest"
    fake_game.host_name = "Host"

    test_service.team_season_repository.get_team_season.side_effect = [Mock(TeamSeason), Mock(TeamSeason)]

    fake_process_game_strategy = Mock(ProcessGameStrategy)
    test_service.process_game_strategy_factory.create_strategy.return_value = fake_process_game_strategy

    # Act
    test_service.add_game(fake_game)

    # Assert
    test_service.team_season_repository.get_team_season.assert_has_calls([
        call(fake_game.guest_name),
        call(fake_game.host_name),
    ])
    fake_game.decide_winner_and_loser.assert_called_once()
    test_service.game_repository.add_game.assert_called_once_with(fake_game)
    test_service.process_game_strategy_factory.create_strategy.assert_called_once_with(Direction.UP)
    fake_process_game_strategy.process_game.assert_called_once_with(fake_game)


def test_update_game_when_new_game_arg_is_none_should_raise_value_error(test_service):
    # Arrange
    new_game = None
    old_game = None

    # Act and Assert
    with pytest.raises(ValueError) as err:
        test_service.update_game(new_game, old_game)

        assert err.value.args[0] == f"{type(GameService).__name__}.update_game: new_game"


def test_update_game_when_new_game_arg_is_not_none_and_old_game_arg_is_none_should_raise_value_error(test_service):
    # Arrange
    new_game = Mock(Game)
    old_game = None

    # Act and Assert
    with pytest.raises(ValueError) as err:
        test_service.update_game(new_game, old_game)

        assert err.value.args[0] == f"{type(GameService).__name__}.update_game: old_game"


def test_update_game_when_both_args_are_not_none_and_no_team_season_found_for_guest_should_raise_entity_not_found_error(test_service):
    # Arrange
    new_game = Mock(Game)
    old_game = Mock(Game)

    test_service.team_season_repository.get_team_season.return_value = None

    # Act
    with pytest.raises(EntityNotFoundError) as err:
        test_service.update_game(new_game, old_game)
        assert err.value.args[0] == f"No team season found for '{new_game.guest_name}' in year {new_game.season_year}"

    # Assert
    test_service.team_season_repository.get_team_season.assert_called_once_with(new_game.guest_name)


def test_update_game_when_team_season_found_for_guest_and_no_team_season_found_for_host_should_raise_entity_not_found_error(test_service):
    # Arrange
    new_game = Mock(Game)
    old_game = Mock(Game)

    test_service.team_season_repository.get_team_season.side_effect = [Mock(TeamSeason), None]

    # Act
    with pytest.raises(EntityNotFoundError) as err:
        test_service.update_game(new_game, old_game)
        assert err.value.args[0] == f"No team season found for '{new_game.host_name}' in year {new_game.season_year}"

    # Assert
    test_service.team_season_repository.get_team_season.assert_has_calls([
        call(new_game.guest_name),
        call(new_game.host_name),
    ])


def test_update_game_when_team_seasons_found_for_both_teams_and_selected_game_does_not_exist_should_raise_entity_not_found_error(test_service):
    # Arrange
    new_game = Mock(Game)
    old_game = Mock(Game)

    test_service.team_season_repository.get_team_season.side_effect = [Mock(TeamSeason), Mock(TeamSeason)]

    selected_game = None
    test_service.game_repository.get_game.return_value = selected_game

    # Act
    with pytest.raises(EntityNotFoundError) as err:
        test_service.update_game(new_game, old_game)
        assert err.value.args[0] == f"{type(GameService).__name__}.update_game: A game with id={old_game.id} could not be found."

    # Assert
    test_service.team_season_repository.get_team_season.assert_has_calls([
        call(new_game.guest_name),
        call(new_game.host_name),
    ])
    test_service.game_repository.get_game.assert_called_once_with(old_game.id)


def test_update_game_when_selected_game_exists_and_should_update_game_in_repository(test_service):
    # Arrange
    new_game = Mock(Game)
    old_game = Mock(Game)

    test_service.team_season_repository.get_team_season.side_effect = [Mock(TeamSeason), Mock(TeamSeason)]

    selected_game = Mock(Game)
    test_service.game_repository.get_game.return_value = selected_game

    subtract_strategy = Mock(SubtractGameStrategy)
    add_strategy = Mock(AddGameStrategy)
    test_service.process_game_strategy_factory.create_strategy.side_effect = (subtract_strategy, add_strategy)

    # Act
    test_service.update_game(new_game, old_game)

    # Assert
    test_service.team_season_repository.get_team_season.assert_has_calls([
        call(new_game.guest_name),
        call(new_game.host_name),
    ])
    test_service.game_repository.get_game.assert_called_once_with(old_game.id)
    new_game.decide_winner_and_loser.assert_called_once()
    test_service.game_repository.update_game.assert_called_once_with(new_game)

    test_service.process_game_strategy_factory.create_strategy.assert_any_call(Direction.DOWN)
    subtract_strategy.process_game.assert_called_once_with(old_game)

    test_service.process_game_strategy_factory.create_strategy.assert_any_call(Direction.UP)
    add_strategy.process_game.assert_called_once_with(new_game)


def test_delete_game_when_game_with_passed_id_is_not_found_should_raise_entity_not_found_error(test_service):
    # Arrange
    test_service.game_repository.get_game.return_value = None

    # Act
    id = 1
    with pytest.raises(EntityNotFoundError) as err:
        test_service.delete_game(id)
        assert err.value.args[0] == f"{type(GameService).__name__}.delete_game: A game with id={id} could not be found."

    # Assert
    test_service.game_repository.get_game.assert_any_call(id)


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
    test_service.process_game_strategy_factory.create_strategy.assert_any_call(Direction.DOWN)
    strategy.process_game.assert_called_once_with(old_game)
    test_service.game_repository.delete_game.assert_any_call(id)
