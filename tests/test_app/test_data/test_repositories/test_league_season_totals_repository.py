from unittest.mock import patch

from app.data.models.league_season_totals import LeagueSeasonTotals
from app.data.repositories.league_season_totals_repository import LeagueSeasonTotalsRepository


@patch('app.data.repositories.league_season_totals_repository.sqla')
def test_get_league_season_totals_should_get_league_season_totals(fake_sqla):
    # Arrange
    total_games = 1
    total_points = 2
    totals = [total_games, total_points]
    fake_sqla.session.execute.return_value.first.return_value = totals

    league_name = "A"
    season_year = 1

    # Act
    test_repository = LeagueSeasonTotalsRepository()
    result = test_repository.get_league_season_totals(league_name, season_year)

    # Assert
    statement = f"CALL sp_GetLeagueSeasonTotals('{league_name}', {season_year});"
    fake_sqla.session.execute.assert_called_once_with(statement)
    fake_sqla.session.execute.return_value.first.assert_called_once()
    assert isinstance(result, LeagueSeasonTotals)
    assert result.total_games == total_games
    assert result.total_points == total_points
