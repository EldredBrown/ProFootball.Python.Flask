from unittest.mock import patch, MagicMock, call

import pytest

from app.data.models.team_season import TeamSeason
from app.services.game_predictor_service.game_predictor_service import GamePredictorService


@pytest.fixture
@patch('app.services.game_predictor_service.game_predictor_service.TeamSeasonRepository')
def test_service(fake_team_season_repository):
    test_service = GamePredictorService(fake_team_season_repository)
    return test_service


def test_predict_game_score_when_guest_season_is_none_should_raise_value_error(test_service):
    # Arrange
    guest_name = "Guest"
    guest_season_year = 1920
    guest_season = None

    host_name = "Host"
    host_season_year = 1920
    host_season = None

    test_service.team_season_repository.get_team_season_by_team_and_season.side_effect = \
        (guest_season, host_season)

    # Act
    with pytest.raises(ValueError) as err:
        test_service.predict_game_score(guest_name, guest_season_year, host_name, host_season_year)

    # Assert
    test_service.team_season_repository.get_team_season_by_team_and_season.assert_called_once_with(guest_name, guest_season_year)
    assert err.value.args[0] == f"No season data found for '{guest_name}' in year {guest_season_year}"


def test_predict_game_score_when_host_season_is_none_should_raise_value_error(test_service):
    # Arrange
    guest_name = "Guest"
    guest_season_year = 1920
    guest_season = MagicMock(TeamSeason)

    host_name = "Host"
    host_season_year = 1920
    host_season = None

    test_service.team_season_repository.get_team_season_by_team_and_season.side_effect = \
        (guest_season, host_season)

    # Act
    with pytest.raises(ValueError) as err:
        test_service.predict_game_score(guest_name, guest_season_year, host_name, host_season_year)

    # Assert
    test_service.team_season_repository.get_team_season_by_team_and_season.assert_has_calls([
        call(guest_name, guest_season_year),
        call(host_name, host_season_year),
    ])
    assert err.value.args[0] == f"No season data found for '{host_name}' in year {host_season_year}"


def test_predict_game_score_when_guest_season_and_host_season_are_not_none_should_return_correctly_calculated_prediction(
    test_service
):
    # Arrange
    league_id = 1

    guest_name = "Guest"
    guest_season_year = 1920
    guest_season = TeamSeason(team_id=1, season_year=guest_season_year, league_id=league_id)
    guest_season.offensive_average = 1.000
    guest_season.offensive_factor = 2.000
    guest_season.defensive_average = 3.000
    guest_season.defensive_factor = 4.000

    host_name = "Host"
    host_season_year = 1920
    host_season = TeamSeason(team_id=2, season_year=host_season_year, league_id=league_id)
    host_season.offensive_average = 5.000
    host_season.offensive_factor = 6.000
    host_season.defensive_average = 7.000
    host_season.defensive_factor = 8.000

    test_service.team_season_repository.get_team_season_by_team_and_season.side_effect = \
        (guest_season, host_season)

    # Act
    game_prediction = test_service.predict_game_score(guest_name, guest_season_year, host_name, host_season_year)

    # Assert
    test_service.team_season_repository.get_team_season_by_team_and_season.assert_has_calls([
        call(guest_name, guest_season_year),
        call(host_name, host_season_year),
    ])

    assert game_prediction.guest_score == round(
        ((guest_season.offensive_factor * host_season.defensive_average +
          host_season.defensive_factor * guest_season.offensive_average) / 2),
        1
    )
    assert game_prediction.host_score == round(
        ((host_season.offensive_factor * guest_season.defensive_average +
          guest_season.defensive_factor * host_season.offensive_average) / 2),
        1
    )
