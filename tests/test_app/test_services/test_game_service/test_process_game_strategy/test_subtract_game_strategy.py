import unittest
from unittest.mock import Mock, PropertyMock, patch

import pytest

from app.data.models.game import Game
from app.data.models.team_season import TeamSeason
from app.services.game_service.process_game_strategy.subtract_game_strategy import SubtractGameStrategy


@pytest.fixture()
@patch('app.services.game_service.process_game_strategy.add_game_strategy.TeamSeasonRepository')
def test_strategy(fake_team_season_repository):
    test_strategy = SubtractGameStrategy(team_season_repository=fake_team_season_repository)
    return test_strategy


def test_process_game_when_game_is_a_tie_should_update_ties_for_team_seasons(test_strategy):
    # Arrange
    game = Mock(Game)
    game.guest_name = "Guest"
    game.guest_score = 1
    game.host_name = "Host"
    game.host_score = 1
    game.season_year = 0
    game.is_tie.return_value = True

    guest_season = Mock(TeamSeason)
    guest_season.games = 3
    guest_season.wins = 1
    guest_season.losses = 1
    guest_season.ties = 1
    guest_season.points_for = 1
    guest_season.points_against = 1

    host_season = Mock(TeamSeason)
    host_season.games = 3
    host_season.wins = 1
    host_season.losses = 1
    host_season.ties = 1
    host_season.points_for = 1
    host_season.points_against = 1

    test_strategy._team_season_repository.get_team_season_by_team_and_season.side_effect = (guest_season, host_season)

    # Act
    test_strategy.process_game(game)

    # Assert
    test_strategy._team_season_repository.get_team_season_by_team_and_season.assert_any_call(game.guest_name,
                                                                                             game.season_year)
    test_strategy._team_season_repository.get_team_season_by_team_and_season.assert_any_call(game.host_name,
                                                                                             game.season_year)
    assert guest_season.games == 2
    assert guest_season.wins == 1
    assert guest_season.losses == 1
    assert guest_season.ties == 0
    assert guest_season.points_for == 0
    assert guest_season.points_against == 0

    assert host_season.games == 2
    assert host_season.wins == 1
    assert host_season.losses == 1
    assert host_season.ties == 0
    assert host_season.points_for == 0
    assert host_season.points_against == 0

    guest_season.calculate_winning_percentage.assert_called_once()
    host_season.calculate_winning_percentage.assert_called_once()

    guest_season.calculate_expected_wins_and_losses.assert_called_once()
    host_season.calculate_expected_wins_and_losses.assert_called_once()


def test_process_game_when_game_is_not_a_tie_should_update_wins_and_losses_for_team_seasons(test_strategy):
    # Arrange
    game = Mock(Game)
    game.guest_name = "Guest"
    game.guest_score = 1
    game.host_name = "Host"
    game.host_score = 2
    game.winner_name = "Winner"
    game.loser_name = "Loser"
    game.season_year = 0
    game.is_tie.return_value = False

    guest_season = Mock(TeamSeason)
    guest_season.games = 3
    guest_season.wins = 1
    guest_season.losses = 1
    guest_season.ties = 1
    guest_season.points_for = 2
    guest_season.points_against = 2

    host_season = Mock(TeamSeason)
    host_season.games = 3
    host_season.wins = 1
    host_season.losses = 1
    host_season.ties = 1
    host_season.points_for = 2
    host_season.points_against = 2

    test_strategy._team_season_repository.get_team_season_by_team_and_season.side_effect = (guest_season, host_season,
                                                                                   host_season, guest_season)

    # Act
    test_strategy.process_game(game)

    # Assert
    test_strategy._team_season_repository.get_team_season_by_team_and_season.assert_any_call(game.guest_name,
                                                                                             game.season_year)
    test_strategy._team_season_repository.get_team_season_by_team_and_season.assert_any_call(game.host_name,
                                                                                             game.season_year)
    test_strategy._team_season_repository.get_team_season_by_team_and_season.assert_any_call(game.winner_name,
                                                                                             game.season_year)
    test_strategy._team_season_repository.get_team_season_by_team_and_season.assert_any_call(game.loser_name,
                                                                                             game.season_year)
    assert guest_season.games == 2
    assert guest_season.wins == 1
    assert guest_season.losses == 0
    assert guest_season.ties == 1
    assert guest_season.points_for == 1
    assert guest_season.points_against == 0

    assert host_season.games == 2
    assert host_season.wins == 0
    assert host_season.losses == 1
    assert host_season.ties == 1
    assert host_season.points_for == 0
    assert host_season.points_against == 1

    guest_season.calculate_winning_percentage.assert_called_once()
    host_season.calculate_winning_percentage.assert_called_once()

    guest_season.calculate_expected_wins_and_losses.assert_called_once()
    host_season.calculate_expected_wins_and_losses.assert_called_once()
