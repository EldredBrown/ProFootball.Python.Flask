from decimal import Decimal
from unittest.mock import patch

import pytest

from app.data.models.standings_team_season import StandingsTeamSeason
from app.data.repositories.season_standings_repository import SeasonStandingsRepository


@pytest.fixture
def test_repo():
    return SeasonStandingsRepository()


@patch('app.data.repositories.season_standings_repository.sqla')
@patch('app.data.repositories.season_standings_repository.SQLQuery')
def test_get_season_standings_by_season_year_should_get_season_standings_for_specified_season_year(
        fake_SQLQuery, fake_sqla, test_repo
):
    # Arrange
    team_seasons_in = [
        (
            "Team 1",
            1, 1, 1, Decimal('0.500'),
            60, 60,
            Decimal('20.00'), Decimal('20.00'),
            Decimal('1.50'), Decimal('1.50')
        ),
        (
            "Team 2",
            2, 2, 2, Decimal('0.500'),
            120, 120,
            Decimal('20.00'), Decimal('20.00'),
            Decimal('1.50'), Decimal('1.50')
        ),
        (
            "Team 3",
            3, 3, 3, Decimal('0.500'),
            180, 180,
            Decimal('20.00'), Decimal('20.00'),
            Decimal('1.50'), Decimal('1.50')
        ),
    ]
    fake_sqla.session.execute.return_value = team_seasons_in

    # Act
    team_seasons_out = test_repo.get_season_standings_by_season_year(season_year=1)

    # Assert
    querystring = f"EXEC sp_GetSeasonStandings 1, False"
    fake_SQLQuery.assert_called_once_with(querystring)
    fake_sqla.session.execute.assert_called_once_with(fake_SQLQuery.return_value)
    for i in range(len(team_seasons_in)):
        assert isinstance(team_seasons_out[i], StandingsTeamSeason)
        assert team_seasons_out[i].team_name == team_seasons_in[i][0]
        assert team_seasons_out[i].wins == team_seasons_in[i][1]
        assert team_seasons_out[i].losses == team_seasons_in[i][2]
        assert team_seasons_out[i].ties == team_seasons_in[i][3]
        assert team_seasons_out[i].winning_percentage == team_seasons_in[i][4]
        assert team_seasons_out[i].points_for == team_seasons_in[i][5]
        assert team_seasons_out[i].points_against == team_seasons_in[i][6]
        assert team_seasons_out[i].avg_points_for == team_seasons_in[i][7]
        assert team_seasons_out[i].avg_points_against == team_seasons_in[i][8]
        assert team_seasons_out[i].expected_wins == team_seasons_in[i][9]
        assert team_seasons_out[i].expected_losses == team_seasons_in[i][10]
