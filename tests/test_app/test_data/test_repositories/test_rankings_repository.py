from decimal import Decimal
from unittest.mock import patch

import pytest

from app.data.models.rankings_team_season \
    import OffensiveRankingsTeamSeason, DefensiveRankingsTeamSeason, TotalRankingsTeamSeason
from app.data.repositories.rankings_repository import RankingsRepository
from test_app import create_app


@pytest.fixture
def test_app():
    return create_app()


@patch('app.data.repositories.rankings_repository.sqla')
@patch('app.data.repositories.rankings_repository.SQLQuery')
def test_get_offensive_rankings_by_season_year_should_get_offensive_rankings_for_specified_season_year(
        fake_SQLQuery, fake_sqla, test_app
):
    with test_app.app_context():
        # Arrange
        team_seasons_in = [
        ]
        fake_sqla.session.execute.return_value = team_seasons_in

        # Act
        test_repo = RankingsRepository()
        team_seasons_out = test_repo.get_offensive_rankings_by_season_year(season_year=1)

    # Assert
    querystring = f"EXEC dbo.sp_GetRankingsOffensive 1"
    fake_SQLQuery.assert_called_once_with(querystring)
    fake_sqla.session.execute.assert_called_once_with(fake_SQLQuery.return_value)
    for i in range(len(team_seasons_in)):
        assert isinstance(team_seasons_out[i], OffensiveRankingsTeamSeason)
        assert team_seasons_out[i].team_name == team_seasons_in[i][0]
        assert team_seasons_out[i].wins == team_seasons_in[i][1]
        assert team_seasons_out[i].losses == team_seasons_in[i][2]
        assert team_seasons_out[i].ties == team_seasons_in[i][3]
        assert team_seasons_out[i].offensive_average == team_seasons_in[i][4]
        assert team_seasons_out[i].offensive_factor == team_seasons_in[i][5]
        assert team_seasons_out[i].offensive_index == team_seasons_in[i][6]


@patch('app.data.repositories.rankings_repository.sqla')
@patch('app.data.repositories.rankings_repository.SQLQuery')
def test_get_defensive_rankings_by_season_year_should_get_defensive_rankings_for_specified_season_year(
        fake_SQLQuery, fake_sqla, test_app
):
    with test_app.app_context():
        # Arrange
        team_seasons_in = [
        ]
        fake_sqla.session.execute.return_value = team_seasons_in

        # Act
        test_repo = RankingsRepository()
        team_seasons_out = test_repo.get_defensive_rankings_by_season_year(season_year=1)

    # Assert
    querystring = f"EXEC dbo.sp_GetRankingsDefensive 1"
    fake_SQLQuery.assert_called_once_with(querystring)
    fake_sqla.session.execute.assert_called_once_with(fake_SQLQuery.return_value)
    for i in range(len(team_seasons_in)):
        assert isinstance(team_seasons_out[i], DefensiveRankingsTeamSeason)
        assert team_seasons_out[i].team_name == team_seasons_in[i][0]
        assert team_seasons_out[i].wins == team_seasons_in[i][1]
        assert team_seasons_out[i].losses == team_seasons_in[i][2]
        assert team_seasons_out[i].ties == team_seasons_in[i][3]
        assert team_seasons_out[i].defensive_average == team_seasons_in[i][4]
        assert team_seasons_out[i].defensive_factor == team_seasons_in[i][5]
        assert team_seasons_out[i].defensive_index == team_seasons_in[i][6]


@patch('app.data.repositories.rankings_repository.sqla')
@patch('app.data.repositories.rankings_repository.SQLQuery')
def test_get_total_rankings_by_season_year_should_get_total_rankings_for_specified_season_year(
        fake_SQLQuery, fake_sqla, test_app
):
    with test_app.app_context():
        # Arrange
        team_seasons_in = [
        ]
        fake_sqla.session.execute.return_value = team_seasons_in

        # Act
        test_repo = RankingsRepository()
        team_seasons_out = test_repo.get_total_rankings_by_season_year(season_year=1)

    # Assert
    querystring = f"EXEC dbo.sp_GetRankingsTotal 1"
    fake_SQLQuery.assert_called_once_with(querystring)
    fake_sqla.session.execute.assert_called_once_with(fake_SQLQuery.return_value)
    for i in range(len(team_seasons_in)):
        assert isinstance(team_seasons_out[i], TotalRankingsTeamSeason)
        assert team_seasons_out[i].team_name == team_seasons_in[i][0]
        assert team_seasons_out[i].wins == team_seasons_in[i][1]
        assert team_seasons_out[i].losses == team_seasons_in[i][2]
        assert team_seasons_out[i].ties == team_seasons_in[i][3]
        assert team_seasons_out[i].offensive_average == team_seasons_in[i][4]
        assert team_seasons_out[i].offensive_factor == team_seasons_in[i][5]
        assert team_seasons_out[i].offensive_index == team_seasons_in[i][6]
        assert team_seasons_out[i].defensive_average == team_seasons_in[i][7]
        assert team_seasons_out[i].defensive_factor == team_seasons_in[i][8]
        assert team_seasons_out[i].defensive_index == team_seasons_in[i][9]
        assert team_seasons_out[i].final_expected_winning_percentage == team_seasons_in[i][10]
