import pytest

from unittest.mock import MagicMock, patch, call

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


@pytest.mark.skip('WIP')
def test_add_game_when_new_game_arg_is_not_none_and_no_team_season_found_for_guest_should_raise_entity_not_found_error(
        test_service
):
    # Arrange
    game = Game(season_year=1920, guest_name="Guest", host_name="Host")

    test_service.team_season_repository.get_team_season_by_team_and_season.return_value = None

    # Act
    with pytest.raises(EntityNotFoundError) as err:
        test_service.add_game(game)

    # Assert
    assert err.value.args[0] == f"No team season found for '{game.guest_name}' in year {game.season_year}"
    test_service.team_season_repository.get_team_season_by_team_and_season.assert_called_once_with(
        game.guest_name, game.season_year
    )


@pytest.mark.skip('WIP')
def test_add_game_when_team_season_found_for_guest_and_no_team_season_found_for_host_should_raise_entity_not_found_error(
        test_service
):
    # Arrange
    game = Game(season_year=1920, guest_name="Guest", host_name="Host")

    test_service.team_season_repository.get_team_season_by_team_and_season.side_effect = [TeamSeason(), None]

    # Act
    with pytest.raises(EntityNotFoundError) as err:
        test_service.add_game(game)

    # Assert
    assert err.value.args[0] == f"No team season found for '{game.host_name}' in year {game.season_year}"
    test_service.team_season_repository.get_team_season_by_team_and_season.assert_has_calls([
        call(game.guest_name, game.season_year),
        call(game.host_name, game.season_year),
    ])


def test_add_game_when_team_seasons_found_for_both_teams_should_add_game_to_repository(
        test_service
):
    # Arrange
    game = Game(season_year=1920, guest_name="Guest", host_name="Host")

    test_service.team_season_repository.get_team_season_by_team_and_season.side_effect = [TeamSeason(), TeamSeason()]

    fake_process_game_strategy = MagicMock(ProcessGameStrategy)
    test_service.process_game_strategy_factory.create_strategy.return_value = fake_process_game_strategy

    # Act
    test_service.add_game(game)

    # Assert
    test_service.game_repository.add_game.assert_called_once_with(game)
    test_service.process_game_strategy_factory.create_strategy.assert_called_once_with(Direction.UP)
    fake_process_game_strategy.process_game.assert_called_once_with(game)


def test_update_game_when_new_game_arg_is_none_should_raise_value_error(test_service):
    # Arrange
    new_game = None
    old_game = None

    # Act
    with pytest.raises(ValueError) as err:
        test_service.update_game(new_game, old_game)

    # Assert
    assert err.value.args[0] == "GameService.update_game: new_game"


def test_update_game_when_new_game_arg_is_not_none_and_old_game_arg_is_none_should_raise_value_error(
        test_service
):
    # Arrange
    new_game = Game()
    old_game = None

    # Act
    with pytest.raises(ValueError) as err:
        test_service.update_game(new_game, old_game)

    # Assert
    assert err.value.args[0] == "GameService.update_game: old_game"


@pytest.mark.skip('WIP')
def test_update_game_when_both_args_are_not_none_and_no_team_season_found_for_guest_should_raise_entity_not_found_error(
        test_service
):
    # Arrange
    new_game = Game()
    old_game = Game()

    test_service.team_season_repository.get_team_season_by_team_and_season.return_value = None

    # Act
    with pytest.raises(EntityNotFoundError) as err:
        test_service.update_game(new_game, old_game)

    # Assert
    assert err.value.args[0] == f"No team season found for '{new_game.guest_name}' in year {new_game.season_year}"
    test_service.team_season_repository.get_team_season_by_team_and_season.assert_called_once_with(
        new_game.guest_name, new_game.season_year
    )


@pytest.mark.skip('WIP')
def test_update_game_when_team_season_found_for_guest_and_no_team_season_found_for_host_should_raise_entity_not_found_error(
        test_service
):
    # Arrange
    new_game = Game()
    old_game = Game()

    test_service.team_season_repository.get_team_season_by_team_and_season.side_effect = [TeamSeason(), None]

    # Act
    with pytest.raises(EntityNotFoundError) as err:
        test_service.update_game(new_game, old_game)
        assert err.value.args[0] == f"No team season found for '{new_game.host_name}' in year {new_game.season_year}"

    # Assert
    test_service.team_season_repository.get_team_season_by_team_and_season.assert_has_calls([
        call(new_game.guest_name, new_game.season_year),
        call(new_game.host_name, new_game.season_year),
    ])


def test_update_game_when_team_seasons_found_for_both_teams_and_selected_game_does_not_exist_should_raise_entity_not_found_error(
        test_service
):
    # Arrange
    new_game = Game()
    old_game = Game()

    test_service.team_season_repository.get_team_season_by_team_and_season.side_effect = [TeamSeason(), TeamSeason()]

    selected_game = None
    test_service.game_repository.get_game.return_value = selected_game

    # Act
    with pytest.raises(EntityNotFoundError) as err:
        test_service.update_game(new_game, old_game)

    # Assert
    assert err.value.args[0] == f"GameService.update_game: A game with id={old_game.id} could not be found."
    test_service.game_repository.get_game.assert_called_once_with(old_game.id)


def test_update_game_when_selected_game_exists_should_update_game_in_repository(test_service):
    # Arrange
    new_game = Game(id=1, season_year=1920, guest_name="New Guest", host_name="New Host")
    old_game = Game(id=1, season_year=1920, guest_name="Old Guest", host_name="Old Host")

    test_service.team_season_repository.get_team_season_by_team_and_season.side_effect = [TeamSeason(), TeamSeason()]

    selected_game = Game()
    test_service.game_repository.get_game.return_value = selected_game

    subtract_strategy = MagicMock(SubtractGameStrategy)
    add_strategy = MagicMock(AddGameStrategy)
    test_service.process_game_strategy_factory.create_strategy.side_effect = (subtract_strategy, add_strategy)

    # Act
    test_service.update_game(new_game, old_game)

    # Assert
    # test_service.team_season_repository.get_team_season_by_team_and_season.assert_has_calls([
    #     call(new_game.guest_name, new_game.season_year),
    #     call(new_game.host_name, new_game.season_year),
    # ])
    test_service.game_repository.get_game.assert_called_once_with(old_game.id)
    test_service.game_repository.update_game.assert_called_once_with(new_game)

    test_service.process_game_strategy_factory.create_strategy.assert_has_calls([
        call(Direction.DOWN),
        call(Direction.UP),
    ])

    subtract_strategy.process_game.assert_called_once_with(old_game)
    add_strategy.process_game.assert_called_once_with(new_game)


def test_delete_game_when_game_with_passed_id_is_not_found_should_raise_entity_not_found_error(test_service):
    # Arrange
    test_service.game_repository.get_game.return_value = None

    # Act
    id = 1
    with pytest.raises(EntityNotFoundError) as err:
        test_service.delete_game(id)
        assert err.value.args[0] == f"GameService.delete_game: A game with id={id} could not be found."

    # Assert
    test_service.game_repository.get_game.assert_called_once_with(id)


def test_delete_game_when_game_with_passed_id_is_found_should_delete_game_from_repository(test_service):
    # Arrange
    old_game = MagicMock(Game)
    test_service.game_repository.get_game.return_value = old_game

    strategy = MagicMock(SubtractGameStrategy)
    test_service.process_game_strategy_factory.create_strategy.return_value = strategy

    # Act
    id = 1
    test_service.delete_game(id)

    # Assert
    test_service.game_repository.get_game.assert_called_once_with(id)
    test_service.process_game_strategy_factory.create_strategy.assert_called_once_with(Direction.DOWN)
    strategy.process_game.assert_called_once_with(old_game)
    test_service.game_repository.delete_game.assert_called_once_with(id)
