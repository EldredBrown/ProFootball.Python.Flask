from decimal import Decimal
from unittest.mock import patch

import pytest

import app.data.repositories.season_rankings_repository as mod
from app.data.models.rankings_team_season \
    import OffensiveRankingsTeamSeason, DefensiveRankingsTeamSeason, TotalRankingsTeamSeason


@pytest.mark.parametrize("season_year", [None, 1920])
def test_get_offensive_rankings_when_league_id_is_none_should_return_empty_list(season_year):
    # Arrange
    league_id = None

    # Act
    team_seasons_out = mod.get_offensive_rankings(season_year=season_year, league_id=league_id)

    # Assert
    assert team_seasons_out == []


@patch('app.data.repositories.season_rankings_repository.sqla')
def test_get_offensive_rankings_when_season_year_is_not_none_and_league_id_is_not_none_should_get_offensive_rankings(
        fake_sqla
):
    # Arrange
    team_seasons_in = (
        ("Team 1", 0, 0, 0, Decimal('0.00'), Decimal('0.000'), Decimal('0.00')),
        ("Team 2", 0, 0, 0, Decimal('0.00'), Decimal('0.000'), Decimal('0.00')),
        ("Team 3", 0, 0, 0, Decimal('0.00'), Decimal('0.000'), Decimal('0.00')),
    )
    fake_sqla.callproc.return_value = team_seasons_in

    season_year = 1920
    league_id = 1

    # Act
    team_seasons_out = mod.get_offensive_rankings(season_year, league_id)

    # Assert
    fake_sqla.callproc.assert_called_once_with(
        f"EXEC dbo.sp_GetRankingsOffensive @season_year = {season_year}, @league_id = {league_id};")

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


@pytest.mark.parametrize(
    "season_year",
    [
        (None),
        (1920),
    ]
)
def test_get_defensive_rankings_when_league_id_is_none_should_return_empty_list(season_year):
    # Arrange
    league_id = None

    # Act
    team_seasons_out = mod.get_defensive_rankings(season_year=season_year, league_id=league_id)

    # Assert
    assert team_seasons_out == []


@patch('app.data.repositories.season_rankings_repository.sqla')
def test_get_defensive_rankings_when_season_year_is_not_none_and_league_id_is_not_none_should_get_defensive_rankings(
        fake_sqla
):
    # Arrange
    team_seasons_in = (
        ("Team 1", 0, 0, 0, Decimal('0.00'), Decimal('0.000'), Decimal('0.00')),
        ("Team 2", 0, 0, 0, Decimal('0.00'), Decimal('0.000'), Decimal('0.00')),
        ("Team 3", 0, 0, 0, Decimal('0.00'), Decimal('0.000'), Decimal('0.00')),
    )
    fake_sqla.callproc.return_value = team_seasons_in

    season_year = 1920
    league_id = 1

    # Act
    team_seasons_out = mod.get_defensive_rankings(season_year, league_id)

    # Assert
    fake_sqla.callproc.assert_called_once_with(
        f"EXEC dbo.sp_GetRankingsDefensive @season_year = {season_year}, @league_id = {league_id};")

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


@pytest.mark.parametrize(
    "season_year",
    [
        (None),
        (1920),
    ]
)
def test_get_total_rankings_when_league_id_is_none_should_return_empty_list(season_year):
    # Arrange
    league_id = None

    # Act
    team_seasons_out = mod.get_total_rankings(season_year=season_year, league_id=league_id)

    # Assert
    assert team_seasons_out == []


@patch('app.data.repositories.season_rankings_repository.sqla')
def test_get_total_rankings_when_season_year_is_not_none_and_league_id_is_not_none_should_get_total_rankings(
        fake_sqla
):
    # Arrange
    team_seasons_in = (
        ("Team 1", 0, 0, 0, Decimal('0.00'), Decimal('0.000'), Decimal('0.00'), Decimal('0.00'), Decimal('0.000'), Decimal('0.00'), Decimal('0.000')),
        ("Team 2", 0, 0, 0, Decimal('0.00'), Decimal('0.000'), Decimal('0.00'), Decimal('0.00'), Decimal('0.000'), Decimal('0.00'), Decimal('0.000')),
        ("Team 3", 0, 0, 0, Decimal('0.00'), Decimal('0.000'), Decimal('0.00'), Decimal('0.00'), Decimal('0.000'), Decimal('0.00'), Decimal('0.000')),
    )
    fake_sqla.callproc.return_value = team_seasons_in

    season_year = 1920
    league_id = 1

    # Act
    team_seasons_out = mod.get_total_rankings(season_year, league_id)

    # Assert
    fake_sqla.callproc.assert_called_once_with(
        f"EXEC dbo.sp_GetRankingsTotal @season_year = {season_year}, @league_id = {league_id};")

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
