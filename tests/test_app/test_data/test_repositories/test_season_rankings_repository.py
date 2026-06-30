from decimal import Decimal
from unittest.mock import patch

import pytest

from app.data.models.rankings_team_season \
    import OffensiveRankingsTeamSeason, DefensiveRankingsTeamSeason, TotalRankingsTeamSeason
from app.data.repositories.season_rankings_repository import SeasonRankingsRepository


@pytest.fixture()
def test_repo():
    return SeasonRankingsRepository()


def test_get_offensive_rankings_by_season_year_when_season_year_is_none_should_return_empty_list(test_repo):
    # Arrange
    season_id = None

    # Act
    team_seasons_out = test_repo.get_offensive_rankings_by_season(season_id)

    # Assert
    assert team_seasons_out == []


@patch('app.data.repositories.season_rankings_repository.sqla')
def test_get_offensive_rankings_by_season_year_when_season_year_is_not_none_should_get_offensive_rankings_for_specified_season_year(
        fake_sqla, test_repo
):
    # Arrange
    team_seasons_in = (
        ("Team 1", 0, 0, 0, Decimal('0.00'), Decimal('0.000'), Decimal('0.00')),
        ("Team 2", 0, 0, 0, Decimal('0.00'), Decimal('0.000'), Decimal('0.00')),
        ("Team 3", 0, 0, 0, Decimal('0.00'), Decimal('0.000'), Decimal('0.00')),
    )
    fake_sqla.callproc.return_value = team_seasons_in

    season_id = 1920

    # Act
    team_seasons_out = test_repo.get_offensive_rankings_by_season(season_id)

    # Assert
    fake_sqla.callproc.assert_called_once_with(f"EXEC dbo.sp_GetRankingsOffensive @season_id = {season_id};")

    for i in range(len(team_seasons_in)):
        team_season_out = team_seasons_out[i]
        team_season_in = team_seasons_in[i]

        assert isinstance(team_season_out, OffensiveRankingsTeamSeason)
        assert team_season_out.team_name == team_season_in[0]
        assert team_season_out.wins == team_season_in[1]
        assert team_season_out.losses == team_season_in[2]
        assert team_season_out.ties == team_season_in[3]
        assert team_season_out.offensive_average == team_season_in[4]
        assert team_season_out.offensive_factor == team_season_in[5]
        assert team_season_out.offensive_index == team_season_in[6]


def test_get_defensive_rankings_by_season_year_when_season_year_is_none_should_return_empty_list(test_repo):
    # Arrange
    season_id = None

    # Act
    team_seasons_out = test_repo.get_defensive_rankings_by_season(season_id)

    # Assert
    assert team_seasons_out == []


@patch('app.data.repositories.season_rankings_repository.sqla')
def test_get_defensive_rankings_by_season_year_when_season_year_is_not_none_should_get_defensive_rankings_for_specified_season_year(
        fake_sqla, test_repo
):
    # Arrange
    team_seasons_in = (
        ("Team 1", 0, 0, 0, Decimal('0.00'), Decimal('0.000'), Decimal('0.00')),
        ("Team 2", 0, 0, 0, Decimal('0.00'), Decimal('0.000'), Decimal('0.00')),
        ("Team 3", 0, 0, 0, Decimal('0.00'), Decimal('0.000'), Decimal('0.00')),
    )
    fake_sqla.callproc.return_value = team_seasons_in

    season_id = 1920

    # Act
    team_seasons_out = test_repo.get_defensive_rankings_by_season(season_id)

    # Assert
    fake_sqla.callproc.assert_called_once_with(f"EXEC dbo.sp_GetRankingsDefensive @season_id = {season_id};")

    for i in range(len(team_seasons_in)):
        team_season_out = team_seasons_out[i]
        team_season_in = team_seasons_in[i]

        assert isinstance(team_season_out, DefensiveRankingsTeamSeason)
        assert team_season_out.team_name == team_season_in[0]
        assert team_season_out.wins == team_season_in[1]
        assert team_season_out.losses == team_season_in[2]
        assert team_season_out.ties == team_season_in[3]
        assert team_season_out.defensive_average == team_season_in[4]
        assert team_season_out.defensive_factor == team_season_in[5]
        assert team_season_out.defensive_index == team_season_in[6]


def test_get_total_rankings_by_season_year_when_season_year_is_none_should_return_empty_list(test_repo):
    # Arrange
    season_id = None

    # Act
    team_seasons_out = test_repo.get_total_rankings_by_season(season_id)

    # Assert
    assert team_seasons_out == []


@patch('app.data.repositories.season_rankings_repository.sqla')
def test_get_total_rankings_by_season_year_when_season_year_is_not_none_should_get_total_rankings_for_specified_season_year(
        fake_sqla, test_repo
):
    # Arrange
    team_seasons_in = (
        ("Team 1", 0, 0, 0, Decimal('0.00'), Decimal('0.000'), Decimal('0.00'), Decimal('0.00'), Decimal('0.000'), Decimal('0.00'), Decimal('0.000')),
        ("Team 2", 0, 0, 0, Decimal('0.00'), Decimal('0.000'), Decimal('0.00'), Decimal('0.00'), Decimal('0.000'), Decimal('0.00'), Decimal('0.000')),
        ("Team 3", 0, 0, 0, Decimal('0.00'), Decimal('0.000'), Decimal('0.00'), Decimal('0.00'), Decimal('0.000'), Decimal('0.00'), Decimal('0.000')),
    )
    fake_sqla.callproc.return_value = team_seasons_in

    season_id = 1920

    # Act
    team_seasons_out = test_repo.get_total_rankings_by_season(season_id)

    # Assert
    fake_sqla.callproc.assert_called_once_with(f"EXEC dbo.sp_GetRankingsTotal @season_id = {season_id};")

    for i in range(len(team_seasons_in)):
        team_season_out = team_seasons_out[i]
        team_season_in = team_seasons_in[i]

        assert isinstance(team_season_out, TotalRankingsTeamSeason)
        assert team_season_out.team_name == team_season_in[0]
        assert team_season_out.wins == team_season_in[1]
        assert team_season_out.losses == team_season_in[2]
        assert team_season_out.ties == team_season_in[3]
        assert team_season_out.offensive_average == team_season_in[4]
        assert team_season_out.offensive_factor == team_season_in[5]
        assert team_season_out.offensive_index == team_season_in[6]
        assert team_season_out.defensive_average == team_season_in[7]
        assert team_season_out.defensive_factor == team_season_in[8]
        assert team_season_out.defensive_index == team_season_in[9]
        assert team_season_out.final_expected_winning_percentage == team_season_in[10]
