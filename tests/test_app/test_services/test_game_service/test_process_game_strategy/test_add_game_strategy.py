from unittest.mock import MagicMock, patch, call

import pytest

from app.data.errors import EntityNotFoundError
from app.data.models.game import Game
from app.data.models.team import Team
from app.data.models.team_season import TeamSeason
from app.services.game_service.process_game_strategy.add_game_strategy import AddGameStrategy


@pytest.fixture()
@patch('app.services.game_service.process_game_strategy.process_game_strategy.TeamSeasonRepository')
@patch('app.services.game_service.process_game_strategy.process_game_strategy.TeamRepository')
def test_strategy(fake_team_repository, fake_team_season_repository):
    test_strategy = AddGameStrategy(
        team_repository=fake_team_repository, team_season_repository=fake_team_season_repository
    )
    return test_strategy


def test_process_game_when_game_arg_is_none_should_raise_value_error(test_strategy):
    # Arrange
    game = None

    # Act
    with pytest.raises(ValueError) as err:
        test_strategy.process_game(game)

        # Assert
        assert err.value.args[0] == "AddGameStrategy.process_game: game"


def test_process_game_when_game_arg_is_not_none_and_guest_season_is_not_found_should_raise_entity_not_found_error(
        test_strategy
):
    # Arrange
    game = Game(season_year=1920, guest_name="Guest", host_name="Host")

    guest = Team(id=1, name="Guest")
    host = Team(id=2, name="Host")
    test_strategy.team_repository.get_team_by_name.side_effect = [guest, host]

    guest_season = None
    host_season = None
    test_strategy.team_season_repository.get_team_season_by_team_and_season.side_effect = [guest_season, host_season]

    # Act
    with pytest.raises(EntityNotFoundError) as err:
        test_strategy.process_game(game)
        assert err.value.args[0] == f"No team season found for guest '{game.guest_name}' in year {game.season_year}"

    # Assert
    test_strategy.team_repository.get_team_by_name.assert_has_calls([
        call(game.guest_name),
        call(game.host_name),
    ])
    test_strategy.team_season_repository.get_team_season_by_team_and_season.assert_has_calls([
        call(guest.id, game.season_year),
        call(host.id, game.season_year),
    ])


@pytest.mark.skip(reason="Not implemented")
def test_process_game_when_guest_season_is_found_and_host_season_is_not_found_should_raise_entity_not_found_error(
        test_strategy
):
    # Arrange
    game = Game(season_year=1920, guest_name="Guest", host_name="Host")

    guest = Team(id=1, name="Guest")
    host = Team(id=2, name="Host")
    test_strategy.team_repository.get_team_by_name.side_effect = [guest, host]

    guest_season = TeamSeason(team_id=1, season_year=1920)
    host_season = None
    test_strategy.team_season_repository.get_team_season_by_team_and_season.side_effect = [guest_season, host_season]

    # Act
    with pytest.raises(EntityNotFoundError) as err:
        test_strategy.process_game(game)
        assert err.value.args[0] == f"No team season found for host '{game.host_name}' in year {game.season_year}"

    # Assert
    test_strategy.team_repository.get_team_by_name.assert_has_calls([
        call(game.guest_name),
        call(game.host_name),
    ])
    test_strategy.team_season_repository.get_team_season_by_team_and_season.assert_has_calls([
        call(guest.id, game.season_year),
        call(host.id, game.season_year),
    ])


@pytest.mark.parametrize(
    "guest_score,host_score,expected_guest_wins,expected_guest_losses,expected_host_wins,expected_host_losses,expected_ties",
    [
        (1,1,0,0,0,0,1),
        (2,1,1,0,0,1,0),
        (1,2,0,1,1,0,0),
    ]
)
def test_process_game_when_guest_and_host_seasons_found_should_update_team_seasons_with_correct_data(
        test_strategy, guest_score, host_score,
        expected_guest_wins, expected_guest_losses,
        expected_host_wins, expected_host_losses, expected_ties
):
    # Arrange
    game = Game(season_year=1920, guest_name="Guest", guest_score=guest_score, host_name="Host", host_score=host_score)

    guest = Team(id=1, name="Guest")
    host = Team(id=2, name="Host")
    test_strategy.team_repository.get_team_by_name.side_effect = [guest, host]

    fake_guest_season = MagicMock(TeamSeason)
    fake_guest_season.games = 0
    fake_guest_season.wins = 0
    fake_guest_season.losses = 0
    fake_guest_season.ties = 0
    fake_guest_season.points_for = 0
    fake_guest_season.points_against = 0

    fake_host_season = MagicMock(TeamSeason)
    fake_host_season.games = 0
    fake_host_season.wins = 0
    fake_host_season.losses = 0
    fake_host_season.ties = 0
    fake_host_season.points_for = 0
    fake_host_season.points_against = 0

    test_strategy.team_season_repository.get_team_season_by_team_and_season.side_effect = \
        (fake_guest_season, fake_host_season)

    # Act
    test_strategy.process_game(game)

    # Assert
    test_strategy.team_repository.get_team_by_name.assert_has_calls([
        call(game.guest_name),
        call(game.host_name),
    ])
    test_strategy.team_season_repository.get_team_season_by_team_and_season.assert_has_calls([
        call(guest.id, game.season_year),
        call(host.id, game.season_year),
    ])

    assert fake_guest_season.games == 1
    assert fake_guest_season.wins == expected_guest_wins
    assert fake_guest_season.losses == expected_guest_losses
    assert fake_guest_season.ties == expected_ties
    assert fake_guest_season.points_for == guest_score
    assert fake_guest_season.points_against == host_score

    assert fake_host_season.games == 1
    assert fake_host_season.wins == expected_host_wins
    assert fake_host_season.losses == expected_host_losses
    assert fake_host_season.ties == expected_ties
    assert fake_host_season.points_for == host_score
    assert fake_host_season.points_against == guest_score

    fake_guest_season.calculate_expected_wins_and_losses.assert_called_once()
    fake_host_season.calculate_expected_wins_and_losses.assert_called_once()

    test_strategy.team_season_repository.update_team_season.assert_has_calls([
        call(fake_guest_season),
        call(fake_host_season),
    ])
