from unittest.mock import Mock, PropertyMock, patch, call

import pytest

from app.data.errors import EntityNotFoundError
from app.data.models.game import Game
from app.data.models.team_season import TeamSeason
from app.services.game_service.process_game_strategy.add_game_strategy import AddGameStrategy


@pytest.fixture()
@patch('app.services.game_service.process_game_strategy.process_game_strategy.TeamSeasonRepository')
def test_strategy(fake_team_season_repository):
    test_strategy = AddGameStrategy(team_season_repository=fake_team_season_repository)
    return test_strategy


def test_process_game_when_game_arg_is_none_should_raise_value_error(test_strategy):
    # Arrange
    game = None

    # Act
    with pytest.raises(ValueError) as err:
        test_strategy.process_game(game)

        # Assert
        assert err.value.args[0] == f"{type(AddGameStrategy).__name__}.process_game: game"


def test_process_game_when_game_arg_is_not_none_and_guest_season_is_not_found_should_raise_entity_not_found_error(
        test_strategy
):
    # Arrange
    game = Mock(Game)
    game.guest_name = "Guest"
    game.host_name = "Host"
    game.season_year = 1

    guest_season = None
    test_strategy.team_season_repository.get_team_season_by_team_name_and_season_year.return_value = guest_season

    # Act
    with pytest.raises(EntityNotFoundError) as err:
        test_strategy.process_game(game)
        assert err.value.args[0] == f"No team season found for guest '{game.guest_name}' in year {game.season_year}"

    # Assert
    test_strategy.team_season_repository.get_team_season_by_team_name_and_season_year.assert_called_once_with(
        game.guest_name, game.season_year
    )


def test_process_game_when_guest_season_is_found_and_host_season_is_not_found_should_raise_entity_not_found_error(
        test_strategy
):
    # Arrange
    game = Mock(Game)
    game.guest_name = "Guest"
    game.host_name = "Host"
    game.season_year = 1

    guest_season = Mock(TeamSeason)
    host_season = None
    test_strategy.team_season_repository.get_team_season_by_team_name_and_season_year.side_effect = \
        [guest_season, host_season]

    # Act
    with pytest.raises(EntityNotFoundError) as err:
        test_strategy.process_game(game)
        assert err.value.args[0] == f"No team season found for host '{game.host_name}' in year {game.season_year}"

    # Assert
    test_strategy.team_season_repository.get_team_season_by_team_name_and_season_year.assert_has_calls([
        call(game.guest_name, game.season_year),
        call(game.host_name, game.season_year),
    ])


def test_process_game_when_game_is_a_tie_should_update_ties_for_team_seasons(test_strategy):
    # Arrange
    game = Mock(Game)
    game.guest_name = "Guest"
    game.guest_score = 1
    game.host_name = "Host"
    game.host_score = 1
    game.season_year = 1
    game.is_tie.return_value = True

    guest_season = Mock(TeamSeason)
    guest_season.games = 0
    guest_season.wins = 0
    guest_season.losses = 0
    guest_season.ties = 0
    guest_season.points_for = 0
    guest_season.points_against = 0

    host_season = Mock(TeamSeason)
    host_season.games = 0
    host_season.wins = 0
    host_season.losses = 0
    host_season.ties = 0
    host_season.points_for = 0
    host_season.points_against = 0

    test_strategy.team_season_repository.get_team_season_by_team_name_and_season_year.side_effect = \
        (guest_season, host_season)

    # Act
    test_strategy.process_game(game)

    # Assert
    test_strategy.team_season_repository.get_team_season_by_team_name_and_season_year.assert_has_calls([
        call(game.guest_name, game.season_year),
        call(game.host_name, game.season_year),
    ])

    assert guest_season.games == 1
    assert guest_season.wins == 0
    assert guest_season.losses == 0
    assert guest_season.ties == 1
    assert guest_season.points_for == 1
    assert guest_season.points_against == 1

    assert host_season.games == 1
    assert host_season.wins == 0
    assert host_season.losses == 0
    assert host_season.ties == 1
    assert host_season.points_for == 1
    assert host_season.points_against == 1

    guest_season.calculate_winning_percentage.assert_called_once()
    host_season.calculate_winning_percentage.assert_called_once()

    guest_season.calculate_expected_wins_and_losses.assert_called_once()
    host_season.calculate_expected_wins_and_losses.assert_called_once()

    test_strategy.team_season_repository.update_team_season.assert_has_calls([
        call(guest_season),
        call(host_season),
    ])


def test_process_game_when_game_is_not_a_tie_and_guest_wins_should_update_wins_and_losses_for_team_seasons(test_strategy):
    # Arrange
    game = Mock(Game)
    game.guest_name = "Guest"
    game.guest_score = 2
    game.host_name = "Host"
    game.host_score = 1
    game.winner_name = "Guest"
    game.loser_name = "Host"
    game.season_year = 1
    game.is_tie.return_value = False

    guest_season = Mock(TeamSeason)
    guest_season.games = 0
    guest_season.wins = 0
    guest_season.losses = 0
    guest_season.ties = 0
    guest_season.points_for = 0
    guest_season.points_against = 0

    host_season = Mock(TeamSeason)
    host_season.games = 0
    host_season.wins = 0
    host_season.losses = 0
    host_season.ties = 0
    host_season.points_for = 0
    host_season.points_against = 0

    test_strategy.team_season_repository.get_team_season_by_team_name_and_season_year.side_effect = \
        (guest_season, host_season)

    # Act
    test_strategy.process_game(game)

    # Assert
    test_strategy.team_season_repository.get_team_season_by_team_name_and_season_year.assert_has_calls([
        call(game.guest_name, game.season_year),
        call(game.host_name, game.season_year),
    ])

    assert guest_season.games == 1
    assert guest_season.wins == 1
    assert guest_season.losses == 0
    assert guest_season.ties == 0
    assert guest_season.points_for == 2
    assert guest_season.points_against == 1

    assert host_season.games == 1
    assert host_season.wins == 0
    assert host_season.losses == 1
    assert host_season.ties == 0
    assert host_season.points_for == 1
    assert host_season.points_against == 2

    guest_season.calculate_winning_percentage.assert_called_once()
    host_season.calculate_winning_percentage.assert_called_once()

    guest_season.calculate_expected_wins_and_losses.assert_called_once()
    host_season.calculate_expected_wins_and_losses.assert_called_once()

    test_strategy.team_season_repository.update_team_season.assert_has_calls([
        call(guest_season),
        call(host_season),
    ])


def test_process_game_when_game_is_not_a_tie_and_host_wins_should_update_wins_and_losses_for_team_seasons(test_strategy):
    # Arrange
    game = Mock(Game)
    game.guest_name = "Guest"
    game.guest_score = 1
    game.host_name = "Host"
    game.host_score = 2
    game.winner_name = "Host"
    game.loser_name = "Guest"
    game.season_year = 1
    game.is_tie.return_value = False

    guest_season = Mock(TeamSeason)
    guest_season.games = 0
    guest_season.wins = 0
    guest_season.losses = 0
    guest_season.ties = 0
    guest_season.points_for = 0
    guest_season.points_against = 0

    host_season = Mock(TeamSeason)
    host_season.games = 0
    host_season.wins = 0
    host_season.losses = 0
    host_season.ties = 0
    host_season.points_for = 0
    host_season.points_against = 0

    test_strategy.team_season_repository.get_team_season_by_team_name_and_season_year.side_effect = \
        (guest_season, host_season)

    # Act
    test_strategy.process_game(game)

    # Assert
    test_strategy.team_season_repository.get_team_season_by_team_name_and_season_year.assert_has_calls([
        call(game.guest_name, game.season_year),
        call(game.host_name, game.season_year),
    ])

    assert guest_season.games == 1
    assert guest_season.wins == 0
    assert guest_season.losses == 1
    assert guest_season.ties == 0
    assert guest_season.points_for == 1
    assert guest_season.points_against == 2

    assert host_season.games == 1
    assert host_season.wins == 1
    assert host_season.losses == 0
    assert host_season.ties == 0
    assert host_season.points_for == 2
    assert host_season.points_against == 1

    guest_season.calculate_winning_percentage.assert_called_once()
    host_season.calculate_winning_percentage.assert_called_once()

    guest_season.calculate_expected_wins_and_losses.assert_called_once()
    host_season.calculate_expected_wins_and_losses.assert_called_once()

    test_strategy.team_season_repository.update_team_season.assert_has_calls([
        call(guest_season),
        call(host_season),
    ])
