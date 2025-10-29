from decimal import Decimal
from unittest.mock import patch

from app.data.models.league_season_totals import LeagueSeasonTotals
from app.data.repositories.league_season_totals_repository import LeagueSeasonTotalsRepository


@patch('app.data.repositories.league_season_totals_repository.SQLQuery')
@patch('app.data.repositories.league_season_totals_repository.sqla')
def test_get_league_season_totals_should_get_league_season_totals(fake_sqla, fake_SQLQuery):
    # Arrange
    total_games = 1
    total_points = 2
    average_points = Decimal('3')
    week_count = 4
    totals = [total_games, total_points, average_points, week_count]
    fake_sqla.session.execute.return_value.first.return_value = totals

    league_name = "APFA"
    season_year = 1

    # Act
    test_repository = LeagueSeasonTotalsRepository()
    result = test_repository.get_league_season_totals(league_name, season_year)

    # Assert
    querystring = f"EXEC sp_GetLeagueSeasonTotals '{league_name}', {season_year};"
    fake_SQLQuery.assert_called_once_with(querystring)
    fake_sqla.session.execute.assert_called_once_with(fake_SQLQuery.return_value)
    fake_sqla.session.execute.return_value.first.assert_called_once()
    assert isinstance(result, LeagueSeasonTotals)
    assert result.total_games == total_games
    assert result.total_points == total_points
    assert result.average_points == average_points
    assert result.week_count == week_count
