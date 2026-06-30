from decimal import Decimal
from unittest.mock import patch

import pytest

from app.data.models.team_season_schedule_averages import TeamSeasonScheduleAverages
from app.data.models.team_season_schedule_profile import TeamSeasonOpponentProfile
from app.data.models.team_season_schedule_totals import TeamSeasonScheduleTotals
from app.data.repositories.team_season_schedule_repository import TeamSeasonScheduleRepository


@pytest.fixture()
def test_repo() -> TeamSeasonScheduleRepository:
    return TeamSeasonScheduleRepository()


@patch('app.data.repositories.team_season_schedule_repository.sqla')
def test_get_team_season_schedule_profile_when_query_returns_empty_list_should_get_empty_team_season_schedule_profile(
        fake_sqla, test_repo
):
    # Arrange
    profile = []
    fake_sqla.callproc.return_value.all.return_value = profile

    team_id = 1
    season_id = 1920

    # Act
    result = test_repo.get_team_season_schedule_profile(team_id, season_id)

    # Assert
    fake_sqla.callproc.assert_called_once_with(f"EXEC sp_GetTeamSeasonScheduleProfile '{team_id}', {season_id};")
    assert result == []


@patch('app.data.repositories.team_season_schedule_repository.sqla')
def test_get_team_season_schedule_profile_when_query_returns_non_empty_list_should_get_team_season_schedule_profile(
        fake_sqla, test_repo
):
    # Arrange
    profile = [
        ("Opponent 1", 3, 2, 1, 1, 1, Decimal('0.5'), 10, 10, 10),
        ("Opponent 2", 2, 3, 1, 1, 1, Decimal('0.5'), 10, 10, 10),
        ("Opponent 3", 3, 3, 1, 1, 1, Decimal('0.5'), 10, 10, 10),
    ]
    fake_sqla.callproc.return_value.all.return_value = profile

    team_id = 1
    season_id = 1920

    # Act
    result = test_repo.get_team_season_schedule_profile(team_id, season_id)

    # Assert
    fake_sqla.callproc.assert_called_once_with(f"EXEC sp_GetTeamSeasonScheduleProfile '{team_id}', {season_id};")
    fake_sqla.callproc.return_value.all.assert_called_once()

    assert isinstance(result, list)
    assert len(result) == 3
    for i in range(len(result)):
        profile_item = profile[i]
        result_item = result[i]

        assert isinstance(result_item, TeamSeasonOpponentProfile)
        assert result_item.opponent == profile_item[0]
        assert result_item.game_points_for == profile_item[1]
        assert result_item.game_points_against == profile_item[2]
        assert result_item.opponent_wins == profile_item[3]
        assert result_item.opponent_losses == profile_item[4]
        assert result_item.opponent_ties == profile_item[5]
        assert result_item.opponent_winning_percentage == profile_item[6]
        assert result_item.opponent_weighted_games == profile_item[7]
        assert result_item.opponent_weighted_points_for == profile_item[8]
        assert result_item.opponent_weighted_points_against == profile_item[9]
        

@patch('app.data.repositories.team_season_schedule_repository.sqla')
def test_get_team_season_schedule_totals_when_query_returns_none_should_get_empty_team_season_schedule_totals(
        fake_sqla, test_repo
):
    # Arrange
    totals = None
    fake_sqla.callproc.return_value.first.return_value = totals

    team_id = 1
    season_id = 1920

    # Act
    result = test_repo.get_team_season_schedule_totals(team_id, season_id)

    # Assert
    fake_sqla.callproc.assert_called_once_with(f"EXEC sp_GetTeamSeasonScheduleTotals '{team_id}', {season_id};")

    assert isinstance(result, TeamSeasonScheduleTotals)
    assert result.games is None
    assert result.points_for is None
    assert result.points_against is None
    assert result.schedule_wins is None
    assert result.schedule_losses is None
    assert result.schedule_ties is None
    assert result.schedule_winning_percentage is None
    assert result.schedule_games is None
    assert result.schedule_points_for is None
    assert result.schedule_points_against is None


@patch('app.data.repositories.team_season_schedule_repository.sqla')
def test_get_team_season_schedule_totals_when_query_does_not_return_none_should_get_not_empty_team_season_schedule_totals(
        fake_sqla, test_repo
):
    # Arrange
    games = 0
    points_for = 1
    points_against = 2
    schedule_wins = 3
    schedule_losses = 4
    schedule_ties = 5
    schedule_winning_percentage = 6
    schedule_games = 7
    schedule_points_for = 8
    schedule_points_against = 9
    fake_sqla.callproc.return_value.first.return_value = (
        games, points_for, points_against, schedule_wins, schedule_losses, schedule_ties, schedule_winning_percentage,
        schedule_games, schedule_points_for, schedule_points_against
    )

    team_id = 1
    season_id = 1920

    # Act
    result = test_repo.get_team_season_schedule_totals(team_id, season_id)

    # Assert
    fake_sqla.callproc.assert_called_once_with(f"EXEC sp_GetTeamSeasonScheduleTotals '{team_id}', {season_id};")
    fake_sqla.callproc.return_value.first.assert_called_once()

    assert isinstance(result, TeamSeasonScheduleTotals)
    assert result.games == games
    assert result.points_for == points_for
    assert result.points_against == points_against
    assert result.schedule_wins == schedule_wins
    assert result.schedule_losses == schedule_losses
    assert result.schedule_ties == schedule_ties
    assert result.schedule_winning_percentage == schedule_winning_percentage
    assert result.schedule_games == schedule_games
    assert result.schedule_points_for == schedule_points_for
    assert result.schedule_points_against == schedule_points_against


@patch('app.data.repositories.team_season_schedule_repository.sqla')
def test_get_team_season_schedule_averages_when_query_returns_none_should_get_empty_team_season_schedule_averages(
        fake_sqla, test_repo
):
    # Arrange
    averages = None
    fake_sqla.callproc.return_value.first.return_value = averages

    team_id = 1
    season_id = 1920

    # Act
    result = test_repo.get_team_season_schedule_averages(team_id, season_id)

    # Assert
    fake_sqla.callproc.assert_called_once_with(f"EXEC sp_GetTeamSeasonScheduleAverages '{team_id}', {season_id};")
    fake_sqla.callproc.return_value.first.assert_called_once()

    assert isinstance(result, TeamSeasonScheduleAverages)
    assert result.avg_points_for is None
    assert result.avg_points_against is None
    assert result.avg_schedule_points_for is None
    assert result.avg_schedule_points_against is None


@patch('app.data.repositories.team_season_schedule_repository.sqla')
def test_get_team_season_schedule_averages_when_query_does_not_return_none_should_get_not_empty_team_season_schedule_averages(
        fake_sqla, test_repo
):
    # Arrange
    points_for = 1
    points_against = 2
    schedule_points_for = 3
    schedule_points_against = 4
    fake_sqla.callproc.return_value.first.return_value = (
        points_for, points_against, schedule_points_for, schedule_points_against
    )

    team_id = 1
    season_id = 1920

    # Act
    result = test_repo.get_team_season_schedule_averages(team_id, season_id)

    # Assert
    fake_sqla.callproc.assert_called_once_with(f"EXEC sp_GetTeamSeasonScheduleAverages '{team_id}', {season_id};")
    fake_sqla.callproc.return_value.first.assert_called_once()

    assert isinstance(result, TeamSeasonScheduleAverages)
    assert result.avg_points_for == points_for
    assert result.avg_points_against == points_against
    assert result.avg_schedule_points_for == schedule_points_for
    assert result.avg_schedule_points_against == schedule_points_against
