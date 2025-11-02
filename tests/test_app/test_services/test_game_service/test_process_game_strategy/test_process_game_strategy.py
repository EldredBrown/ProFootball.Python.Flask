import pytest

from unittest.mock import Mock, patch

from app.data.models.game import Game
from app.data.models.team_season import TeamSeason
from app.services.game_service.process_game_strategy.process_game_strategy import ProcessGameStrategy


@pytest.fixture()
@patch('app.services.game_service.process_game_strategy.process_game_strategy.TeamSeasonRepository')
def test_strategy(fake_team_season_repository):
    test_strategy = ProcessGameStrategy(team_season_repository=fake_team_season_repository)
    return test_strategy


def test_process_game_when_game_arg_is_none_should_raise_value_error(test_strategy):
    # Arrange
    game = None

    # Act & Assert
    with pytest.raises(ValueError):
        test_strategy.process_game(game)


def test_process_game_when_game_arg_is_not_none_should_process_game_and_raise_not_implemented_error(test_strategy):
    # Arrange
    game = Game(season_year=1, week=1, guest_name="Guest", guest_score=0, host_name="Host", host_score=0)
    guest_season = Mock(TeamSeason)
    host_season = Mock(TeamSeason)
    test_strategy.team_season_repository.get_team_season_by_team_name_and_season_year.side_effect = (guest_season, host_season)

    # Act
    with pytest.raises(NotImplementedError):
        test_strategy.process_game(game)

    # Assert
    assert test_strategy.team_season_repository.get_team_season_by_team_name_and_season_year.call_count == 2
    test_strategy.team_season_repository.get_team_season_by_team_name_and_season_year.assert_any_call(game.guest_name,
                                                                                                      game.season_year)
    test_strategy.team_season_repository.get_team_season_by_team_name_and_season_year.assert_any_call(game.host_name,
                                                                                                      game.season_year)
