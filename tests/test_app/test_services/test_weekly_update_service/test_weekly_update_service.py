from unittest.mock import MagicMock, call, patch

import pytest

from app.data.models.league_season import LeagueSeason
from app.data.models.league_season_totals import LeagueSeasonTotals
from app.data.models.season import Season
from app.data.models.team_season import TeamSeason

from app.services.weekly_update_service.weekly_update_service import WeeklyUpdateService


@pytest.fixture()
@patch('app.services.weekly_update_service.weekly_update_service.SeasonRankingsRepository')
@patch('app.services.weekly_update_service.weekly_update_service.LeagueSeasonTotalsRepository')
@patch('app.services.weekly_update_service.weekly_update_service.TeamSeasonRepository')
@patch('app.services.weekly_update_service.weekly_update_service.LeagueSeasonRepository')
@patch('app.services.weekly_update_service.weekly_update_service.GameRepository')
@patch('app.services.weekly_update_service.weekly_update_service.SeasonRepository')
def test_service(
        fake_season_repository, fake_game_repository, fake_league_season_repository, fake_team_season_repository,
        fake_league_season_totals_repository, fake_season_rankings_repository
):
    test_service = WeeklyUpdateService(
        fake_season_repository,
        fake_game_repository,
        fake_league_season_repository,
        fake_team_season_repository,
        fake_league_season_totals_repository,
        fake_season_rankings_repository
    )
    return test_service


def test_run_weekly_update_when_league_id_is_none_should_raise_value_error(test_service):
    # Arrange
    league_id = None

    # Act
    with pytest.raises(ValueError) as e:
        test_service.run_weekly_update(league_id, None)

    # Assert
    assert e.value.args[0] == "league_id"


def test_run_weekly_update_when_league_id_is_not_none_and_season_id_less_than_zero_should_raise_value_error(test_service):
    # Arrange
    league_id = "League"
    season_id = -1

    # Act
    with pytest.raises(ValueError) as e:
        test_service.run_weekly_update(league_id, season_id)

    # Assert
    assert e.value.args[0] == f"season_id must be a positive integer; got {season_id}"


def test_run_weekly_update_when_season_id_equals_zero_should_raise_value_error(test_service):
    # Arrange
    league_id = "League"
    season_id = 0

    # Act
    with pytest.raises(ValueError) as e:
        test_service.run_weekly_update(league_id, season_id)

    # Assert
    assert e.value.args[0] == f"season_id must be a positive integer; got {season_id}"


def test_run_weekly_update_when_season_id_greater_than_zero_and_league_season_totals_is_none_and_src_week_count_is_none_should_not_update_anything(
        test_service
):
    # Arrange
    league_id = "League"
    season_id = 1

    test_service.game_repository.get_max_week_by_season.return_value = None

    fake_league_season = MagicMock(LeagueSeason)
    test_service.league_season_repository.get_league_season_by_league_and_season.return_value = None

    test_service.league_season_totals_repository.get_league_season_totals.return_value = None

    fake_team_season = MagicMock(TeamSeason)

    # Act
    test_service.run_weekly_update(league_id, season_id)

    # Assert
    test_service.league_season_totals_repository.get_league_season_totals.assert_called_once_with(league_id, season_id)
    test_service.league_season_repository.get_league_season_by_league_and_season.assert_not_called()
    fake_league_season.update_games_and_points.assert_not_called()
    test_service.league_season_repository.update_league_season.assert_not_called()
    test_service.game_repository.get_max_week_by_season.assert_called_once_with(season_id)
    test_service.season_repository.get_season.assert_not_called()
    test_service.season_repository.update_season.assert_not_called()
    test_service.team_season_repository.get_team_seasons_by_season.assert_not_called()
    test_service.season_rankings_repository.get_data_for_rankings_update.assert_not_called()
    fake_team_season.update_rankings.assert_not_called()
    test_service.team_season_repository.update_team_season.assert_not_called()


def test_run_weekly_update_when_league_season_totals_is_not_none_and_league_season_totals_total_games_is_none_and_src_week_count_is_none_should_not_update_anything(
        test_service
):
    # Arrange
    league_id = "League"
    season_id = 1

    test_service.league_season_totals_repository.get_league_season_totals.return_value \
        = LeagueSeasonTotals(total_games=None)

    fake_league_season = MagicMock(LeagueSeason)
    test_service.league_season_repository.get_league_season_by_league_and_season.return_value = None
    test_service.game_repository.get_max_week_by_season.return_value = None
    fake_team_season = MagicMock(TeamSeason)

    # Act
    test_service.run_weekly_update(league_id, season_id)

    # Assert
    test_service.league_season_totals_repository.get_league_season_totals.assert_called_once_with(league_id, season_id)
    test_service.league_season_repository.get_league_season_by_league_and_season.assert_not_called()
    fake_league_season.update_games_and_points.assert_not_called()
    test_service.league_season_repository.update_league_season.assert_not_called()
    test_service.game_repository.get_max_week_by_season.assert_called_once_with(season_id)
    test_service.season_repository.get_season.assert_not_called()
    test_service.season_repository.update_season.assert_not_called()
    test_service.team_season_repository.get_team_seasons_by_season.assert_not_called()
    test_service.season_rankings_repository.get_data_for_rankings_update.assert_not_called()
    fake_team_season.update_rankings.assert_not_called()
    test_service.team_season_repository.update_team_season.assert_not_called()


def test_run_weekly_update_when_league_season_totals_total_games_is_not_none_and_league_season_totals_total_points_is_none_and_src_week_count_is_none_should_not_update_anything(
        test_service
):
    # Arrange
    league_id = "League"
    season_id = 1

    test_service.league_season_totals_repository.get_league_season_totals.return_value \
        = LeagueSeasonTotals(total_games=0, total_points=None)

    fake_league_season = MagicMock(LeagueSeason)
    test_service.league_season_repository.get_league_season_by_league_and_season.return_value = None
    test_service.game_repository.get_max_week_by_season.return_value = None
    fake_team_season = MagicMock(TeamSeason)

    # Act
    test_service.run_weekly_update(league_id, season_id)

    # Assert
    test_service.league_season_totals_repository.get_league_season_totals.assert_called_once_with(league_id, season_id)
    test_service.league_season_repository.get_league_season_by_league_and_season.assert_not_called()
    fake_league_season.update_games_and_points.assert_not_called()
    test_service.league_season_repository.update_league_season.assert_not_called()
    test_service.game_repository.get_max_week_by_season.assert_called_once_with(season_id)
    test_service.season_repository.get_season.assert_not_called()
    test_service.season_repository.update_season.assert_not_called()
    test_service.team_season_repository.get_team_seasons_by_season.assert_not_called()
    test_service.season_rankings_repository.get_data_for_rankings_update.assert_not_called()
    fake_team_season.update_rankings.assert_not_called()
    test_service.team_season_repository.update_team_season.assert_not_called()


def test_run_weekly_update_when_league_season_totals_total_points_is_not_none_and_league_season_is_none_and_src_week_count_is_none_should_not_update_anything(test_service):
    # Arrange
    league_id = "League"
    season_id = 1

    test_service.league_season_totals_repository.get_league_season_totals.return_value \
        = LeagueSeasonTotals(total_games=0, total_points=0)

    fake_league_season = MagicMock(LeagueSeason)
    test_service.league_season_repository.get_league_season_by_league_and_season.return_value = None
    test_service.game_repository.get_max_week_by_season.return_value = None
    fake_team_season = MagicMock(TeamSeason)

    # Act
    test_service.run_weekly_update(league_id, season_id)

    # Assert
    test_service.league_season_totals_repository.get_league_season_totals.assert_called_once_with(league_id, season_id)
    test_service.league_season_repository.get_league_season_by_league_and_season.assert_called_once_with(league_id, season_id)
    fake_league_season.update_games_and_points.assert_not_called()
    test_service.league_season_repository.update_league_season.assert_not_called()
    test_service.game_repository.get_max_week_by_season.assert_called_once_with(season_id)
    test_service.season_repository.get_season.assert_not_called()
    test_service.season_repository.update_season.assert_not_called()
    test_service.team_season_repository.get_team_seasons_by_season.assert_not_called()
    test_service.season_rankings_repository.get_data_for_rankings_update.assert_not_called()
    fake_team_season.update_rankings.assert_not_called()
    test_service.team_season_repository.update_team_season.assert_not_called()


def test_run_weekly_update_when_league_season_is_not_none_and_src_week_count_is_none_should_update_league_season_total_points_and_games(
        test_service
):
    # Arrange
    league_id = "League"
    season_id = 1

    league_season_totals = LeagueSeasonTotals(total_games=0, total_points=0)
    test_service.league_season_totals_repository.get_league_season_totals.return_value = league_season_totals

    fake_league_season = MagicMock(LeagueSeason)
    test_service.league_season_repository.get_league_season_by_league_and_season.return_value = fake_league_season
    test_service.game_repository.get_max_week_by_season.return_value = None
    fake_team_season = MagicMock(TeamSeason)

    # Act
    test_service.run_weekly_update(league_id, season_id)

    # Assert
    test_service.league_season_totals_repository.get_league_season_totals.assert_called_once_with(league_id, season_id)
    test_service.league_season_repository.get_league_season_by_league_and_season.assert_called_once_with(league_id, season_id)
    fake_league_season.update_games_and_points.assert_called_once_with(league_season_totals.total_games, league_season_totals.total_points)
    test_service.league_season_repository.update_league_season.assert_called_once_with(fake_league_season)
    test_service.game_repository.get_max_week_by_season.assert_called_once_with(season_id)
    test_service.season_repository.get_season.assert_not_called()
    test_service.season_repository.update_season.assert_not_called()
    test_service.team_season_repository.get_team_seasons_by_season.assert_not_called()
    test_service.season_rankings_repository.get_data_for_rankings_update.assert_not_called()
    fake_team_season.update_rankings.assert_not_called()
    test_service.team_season_repository.update_team_season.assert_not_called()


def test_run_weekly_update_when_src_week_count_is_none_should_not_update_week_count(test_service):
    # Arrange
    league_id = "League"
    season_id = 1

    league_season_totals = LeagueSeasonTotals(total_games=0, total_points=0)
    test_service.league_season_totals_repository.get_league_season_totals.return_value = league_season_totals

    fake_league_season = MagicMock(LeagueSeason)
    test_service.league_season_repository.get_league_season_by_league_and_season.return_value = fake_league_season
    test_service.game_repository.get_max_week_by_season.return_value = None
    fake_team_season = MagicMock(TeamSeason)

    # Act
    test_service.run_weekly_update(league_id, season_id)

    # Assert
    test_service.league_season_totals_repository.get_league_season_totals.assert_called_once_with(league_id, season_id)
    test_service.league_season_repository.get_league_season_by_league_and_season.assert_called_once_with(league_id, season_id)
    fake_league_season.update_games_and_points.assert_called_once_with(league_season_totals.total_games, league_season_totals.total_points)
    test_service.league_season_repository.update_league_season.assert_called_once_with(fake_league_season)
    test_service.game_repository.get_max_week_by_season.assert_called_once_with(season_id)
    test_service.season_repository.get_season.assert_not_called()
    test_service.season_repository.update_season.assert_not_called()
    test_service.team_season_repository.get_team_seasons_by_season.assert_not_called()
    test_service.season_rankings_repository.get_data_for_rankings_update.assert_not_called()
    fake_team_season.update_rankings.assert_not_called()
    test_service.team_season_repository.update_team_season.assert_not_called()


def test_run_weekly_update_when_src_week_count_is_zero_and_dest_season_is_none_should_not_update_week_count(test_service):
    # Arrange
    league_id = "League"
    season_id = 1

    league_season_totals = LeagueSeasonTotals(total_games=0, total_points=0)
    test_service.league_season_totals_repository.get_league_season_totals.return_value = league_season_totals

    fake_league_season = MagicMock(LeagueSeason)
    test_service.league_season_repository.get_league_season_by_league_and_season.return_value = fake_league_season
    test_service.game_repository.get_max_week_by_season.return_value = 0

    test_service.season_repository.get_season.return_value = None

    fake_team_season = MagicMock(TeamSeason)

    # Act
    test_service.run_weekly_update(league_id, season_id)

    # Assert
    test_service.league_season_totals_repository.get_league_season_totals.assert_called_once_with(league_id, season_id)
    test_service.league_season_repository.get_league_season_by_league_and_season.assert_called_once_with(league_id, season_id)
    fake_league_season.update_games_and_points.assert_called_once_with(league_season_totals.total_games, league_season_totals.total_points)
    test_service.league_season_repository.update_league_season.assert_called_once_with(fake_league_season)
    test_service.game_repository.get_max_week_by_season.assert_called_once_with(season_id)
    test_service.season_repository.get_season.assert_called_once_with(season_id)
    test_service.season_repository.update_season.assert_not_called()
    test_service.team_season_repository.get_team_seasons_by_season.assert_not_called()
    test_service.season_rankings_repository.get_data_for_rankings_update.assert_not_called()
    fake_team_season.update_rankings.assert_not_called()
    test_service.team_season_repository.update_team_season.assert_not_called()


def test_run_weekly_update_when_dest_season_is_not_none_should_update_week_count(test_service):
    # Arrange
    league_id = "League"
    season_id = 1

    league_season_totals = LeagueSeasonTotals(total_games=0, total_points=0)
    test_service.league_season_totals_repository.get_league_season_totals.return_value = league_season_totals

    fake_league_season = MagicMock(LeagueSeason)
    test_service.league_season_repository.get_league_season_by_league_and_season.return_value = fake_league_season
    test_service.game_repository.get_max_week_by_season.return_value = 0

    dest_season = MagicMock(Season)
    test_service.season_repository.get_season.return_value = dest_season

    fake_team_season = MagicMock(TeamSeason)

    # Act
    test_service.run_weekly_update(league_id, season_id)

    # Assert
    test_service.league_season_totals_repository.get_league_season_totals.assert_called_once_with(league_id, season_id)
    test_service.league_season_repository.get_league_season_by_league_and_season.assert_called_once_with(league_id, season_id)
    fake_league_season.update_games_and_points.assert_called_once_with(league_season_totals.total_games, league_season_totals.total_points)
    test_service.league_season_repository.update_league_season.assert_called_once_with(fake_league_season)
    test_service.game_repository.get_max_week_by_season.assert_called_once_with(season_id)
    test_service.season_repository.get_season.assert_called_once_with(season_id)
    test_service.season_repository.update_season.assert_called_once_with(dest_season)
    test_service.team_season_repository.get_team_seasons_by_season.assert_not_called()
    test_service.season_rankings_repository.get_data_for_rankings_update.assert_not_called()
    fake_team_season.update_rankings.assert_not_called()
    test_service.team_season_repository.update_team_season.assert_not_called()


def test_run_weekly_update_when_week_count_is_less_than_three_should_not_update_rankings(test_service):
    # Arrange
    league_id = "League"
    season_id = 1

    league_season_totals = LeagueSeasonTotals(total_games=0, total_points=0)
    test_service.league_season_totals_repository.get_league_season_totals.return_value = league_season_totals

    fake_league_season = MagicMock(LeagueSeason)
    test_service.league_season_repository.get_league_season_by_league_and_season.return_value = fake_league_season
    test_service.game_repository.get_max_week_by_season.return_value = 2

    dest_season = MagicMock(Season)
    test_service.season_repository.get_season.return_value = dest_season

    fake_team_season = MagicMock(TeamSeason)

    # Act
    test_service.run_weekly_update(league_id, season_id)

    # Assert
    test_service.league_season_totals_repository.get_league_season_totals.assert_called_once_with(league_id, season_id)
    test_service.league_season_repository.get_league_season_by_league_and_season.assert_called_once_with(league_id, season_id)
    fake_league_season.update_games_and_points.assert_called_once_with(league_season_totals.total_games, league_season_totals.total_points)
    test_service.league_season_repository.update_league_season.assert_called_once_with(fake_league_season)
    test_service.game_repository.get_max_week_by_season.assert_called_once_with(season_id)
    test_service.season_repository.get_season.assert_called_once_with(season_id)
    test_service.season_repository.update_season.assert_called_once_with(dest_season)
    test_service.team_season_repository.get_team_seasons_by_season.assert_not_called()
    test_service.season_rankings_repository.get_data_for_rankings_update.assert_not_called()
    fake_team_season.update_rankings.assert_not_called()
    test_service.team_season_repository.update_team_season.assert_not_called()


def test_run_weekly_update_when_week_count_is_three_and_team_seasons_for_specified_year_is_none_should_not_update_rankings_for_any_team_season(test_service):
    # Arrange
    league_id = "League"
    season_id = 1

    dest_season = MagicMock(Season)
    test_service.season_repository.get_season.return_value = dest_season

    fake_league_season = MagicMock(LeagueSeason)
    test_service.league_season_repository.get_league_season_by_league_and_season.return_value = fake_league_season
    test_service.game_repository.get_max_week_by_season.return_value = 3

    league_season_totals = LeagueSeasonTotals(total_games=0, total_points=0)
    test_service.league_season_totals_repository.get_league_season_totals.return_value = league_season_totals

    fake_team_season = MagicMock(TeamSeason)
    test_service.team_season_repository.get_team_seasons_by_season.return_value = None

    # Act
    test_service.run_weekly_update(league_id, season_id)

    # Assert
    test_service.league_season_totals_repository.get_league_season_totals.assert_called_once_with(league_id, season_id)
    test_service.league_season_repository.get_league_season_by_league_and_season.assert_called_once_with(league_id, season_id)
    fake_league_season.update_games_and_points.assert_called_once_with(league_season_totals.total_games, league_season_totals.total_points)
    test_service.league_season_repository.update_league_season.assert_called_once_with(fake_league_season)
    test_service.game_repository.get_max_week_by_season.assert_called_once_with(season_id)
    test_service.season_repository.get_season.assert_called_once_with(season_id)
    test_service.season_repository.update_season.assert_called_once_with(dest_season)
    test_service.team_season_repository.get_team_seasons_by_season.assert_called_once_with(season_id)
    test_service.season_rankings_repository.get_data_for_rankings_update.assert_not_called()
    fake_team_season.update_rankings.assert_not_called()
    test_service.team_season_repository.update_team_season.assert_not_called()


def test_run_weekly_update_when_week_count_is_greater_than_three_and_team_seasons_for_specified_year_is_none_should_not_update_rankings_for_any_team_season(
        test_service
):
    # Arrange
    league_id = "League"
    season_id = 1

    league_season_totals = LeagueSeasonTotals(total_games=0, total_points=0)
    test_service.league_season_totals_repository.get_league_season_totals.return_value = league_season_totals

    fake_league_season = MagicMock(LeagueSeason)
    test_service.league_season_repository.get_league_season_by_league_and_season.return_value = fake_league_season
    test_service.game_repository.get_max_week_by_season.return_value = 4

    dest_season = MagicMock(Season)
    test_service.season_repository.get_season.return_value = dest_season

    test_service.team_season_repository.get_team_seasons_by_season.return_value = None

    fake_team_season = MagicMock(TeamSeason)

    # Act
    test_service.run_weekly_update(league_id, season_id)

    # Assert
    test_service.league_season_totals_repository.get_league_season_totals.assert_called_once_with(league_id, season_id)
    test_service.league_season_repository.get_league_season_by_league_and_season.assert_called_once_with(league_id, season_id)
    fake_league_season.update_games_and_points.assert_called_once_with(league_season_totals.total_games, league_season_totals.total_points)
    test_service.league_season_repository.update_league_season.assert_called_once_with(fake_league_season)
    test_service.game_repository.get_max_week_by_season.assert_called_once_with(season_id)
    test_service.season_repository.get_season.assert_called_once_with(season_id)
    test_service.season_repository.update_season.assert_called_once_with(dest_season)
    test_service.team_season_repository.get_team_seasons_by_season.assert_called_once_with(season_id)
    test_service.season_rankings_repository.get_data_for_rankings_update.assert_not_called()
    fake_team_season.update_rankings.assert_not_called()
    test_service.team_season_repository.update_team_season.assert_not_called()


def test_run_weekly_update_when_team_seasons_for_specified_year_is_empty_should_not_update_rankings_for_any_team_season(
        test_service
):
    # Arrange
    league_id = "League"
    season_id = 1

    league_season_totals = LeagueSeasonTotals(total_games=0, total_points=0)
    test_service.league_season_totals_repository.get_league_season_totals.return_value = league_season_totals

    fake_league_season = MagicMock(LeagueSeason)
    test_service.league_season_repository.get_league_season_by_league_and_season.return_value = fake_league_season
    test_service.game_repository.get_max_week_by_season.return_value = 4

    dest_season = MagicMock(Season)
    test_service.season_repository.get_season.return_value = dest_season

    team_seasons = []
    test_service.team_season_repository.get_team_seasons_by_season.return_value = team_seasons

    fake_team_season = MagicMock(TeamSeason)

    # Act
    test_service.run_weekly_update(league_id, season_id)

    # Assert
    test_service.league_season_totals_repository.get_league_season_totals.assert_called_once_with(league_id, season_id)
    test_service.league_season_repository.get_league_season_by_league_and_season.assert_called_once_with(league_id, season_id)
    fake_league_season.update_games_and_points.assert_called_once_with(league_season_totals.total_games, league_season_totals.total_points)
    test_service.league_season_repository.update_league_season.assert_called_once_with(fake_league_season)
    test_service.game_repository.get_max_week_by_season.assert_called_once_with(season_id)
    test_service.season_repository.get_season.assert_called_once_with(season_id)
    test_service.season_repository.update_season.assert_called_once_with(dest_season)
    test_service.team_season_repository.get_team_seasons_by_season.assert_called_once_with(season_id)
    test_service.season_rankings_repository.get_data_for_rankings_update.assert_not_called()
    fake_team_season.update_rankings.assert_not_called()
    test_service.team_season_repository.update_team_season.assert_not_called()


def test_run_weekly_update_when_team_seasons_for_specified_year_is_not_empty_and_team_season_schedule_totals_is_none_should_not_update_rankings_for_any_team_season(
        test_service
):
    # Arrange
    league_id = "League"
    season_id = 1

    league_season_totals = LeagueSeasonTotals(total_games=0, total_points=0)
    test_service.league_season_totals_repository.get_league_season_totals.return_value = league_season_totals

    fake_league_season = MagicMock(LeagueSeason)
    test_service.league_season_repository.get_league_season_by_league_and_season.return_value = fake_league_season
    test_service.game_repository.get_max_week_by_season.return_value = 4

    dest_season = MagicMock(Season)
    test_service.season_repository.get_season.return_value = dest_season

    fake_team_season = MagicMock(TeamSeason)
    team_seasons = [
        fake_team_season,
    ]
    test_service.team_season_repository.get_team_seasons_by_season.return_value = team_seasons

    test_service.season_rankings_repository.get_data_for_rankings_update.return_value = \
        {
            'team_season_schedule_totals': None,
        }

    # Act
    test_service.run_weekly_update(league_id, season_id)

    # Assert
    test_service.league_season_totals_repository.get_league_season_totals.assert_called_once_with(league_id, season_id)
    test_service.league_season_repository.get_league_season_by_league_and_season.assert_called_once_with(league_id, season_id)
    fake_league_season.update_games_and_points.assert_called_once_with(league_season_totals.total_games, league_season_totals.total_points)
    test_service.league_season_repository.update_league_season.assert_called_once_with(fake_league_season)
    test_service.game_repository.get_max_week_by_season.assert_called_once_with(season_id)
    test_service.season_repository.get_season.assert_called_once_with(season_id)
    test_service.season_repository.update_season.assert_called_once_with(dest_season)
    test_service.team_season_repository.get_team_seasons_by_season.assert_called_once_with(season_id)
    test_service.season_rankings_repository.get_data_for_rankings_update.assert_called_once_with(fake_team_season)
    fake_team_season.update_rankings.assert_not_called()
    test_service.team_season_repository.update_team_season.assert_not_called()


def test_run_weekly_update_when_team_season_schedule_totals_is_empty_should_not_update_rankings_for_any_team_season(
        test_service
):
    # Arrange
    league_id = "League"
    season_id = 1

    league_season_totals = LeagueSeasonTotals(total_games=0, total_points=0)
    test_service.league_season_totals_repository.get_league_season_totals.return_value = league_season_totals

    fake_league_season = MagicMock(LeagueSeason)
    test_service.league_season_repository.get_league_season_by_league_and_season.return_value = fake_league_season
    test_service.game_repository.get_max_week_by_season.return_value = 4

    dest_season = MagicMock(Season)
    test_service.season_repository.get_season.return_value = dest_season

    fake_team_season = MagicMock(TeamSeason)
    team_seasons = [
        fake_team_season,
    ]
    test_service.team_season_repository.get_team_seasons_by_season.return_value = team_seasons

    test_service.season_rankings_repository.get_data_for_rankings_update.return_value = \
        {
            'team_season_schedule_totals': dict(),
        }

    # Act
    test_service.run_weekly_update(league_id, season_id)

    # Assert
    test_service.league_season_totals_repository.get_league_season_totals.assert_called_once_with(league_id, season_id)
    test_service.league_season_repository.get_league_season_by_league_and_season.assert_called_once_with(league_id, season_id)
    fake_league_season.update_games_and_points.assert_called_once_with(league_season_totals.total_games, league_season_totals.total_points)
    test_service.league_season_repository.update_league_season.assert_called_once_with(fake_league_season)
    test_service.game_repository.get_max_week_by_season.assert_called_once_with(season_id)
    test_service.season_repository.get_season.assert_called_once_with(season_id)
    test_service.season_repository.update_season.assert_called_once_with(dest_season)
    test_service.team_season_repository.get_team_seasons_by_season.assert_called_once_with(season_id)
    test_service.season_rankings_repository.get_data_for_rankings_update.assert_called_once_with(fake_team_season)
    fake_team_season.update_rankings.assert_not_called()
    test_service.team_season_repository.update_team_season.assert_not_called()


def test_run_weekly_update_when_team_season_schedule_totals_is_not_empty_and_team_season_schedule_totals_schedule_games_is_none_should_not_update_rankings_for_any_team_season(
        test_service
):
    # Arrange
    league_id = "League"
    season_id = 1

    league_season_totals = LeagueSeasonTotals(total_games=0, total_points=0)
    test_service.league_season_totals_repository.get_league_season_totals.return_value = league_season_totals

    fake_league_season = MagicMock(LeagueSeason)
    test_service.league_season_repository.get_league_season_by_league_and_season.return_value = fake_league_season
    test_service.game_repository.get_max_week_by_season.return_value = 4

    dest_season = MagicMock(Season)
    test_service.season_repository.get_season.return_value = dest_season

    fake_team_season = MagicMock(TeamSeason)
    team_seasons = [
        fake_team_season,
    ]
    test_service.team_season_repository.get_team_seasons_by_season.return_value = team_seasons

    test_service.season_rankings_repository.get_data_for_rankings_update.return_value = \
        {
            'team_season_schedule_totals': {'schedule_games': None},
        }

    # Act
    test_service.run_weekly_update(league_id, season_id)

    # Assert
    test_service.league_season_totals_repository.get_league_season_totals.assert_called_once_with(league_id, season_id)
    test_service.league_season_repository.get_league_season_by_league_and_season.assert_called_once_with(league_id, season_id)
    fake_league_season.update_games_and_points.assert_called_once_with(league_season_totals.total_games, league_season_totals.total_points)
    test_service.league_season_repository.update_league_season.assert_called_once_with(fake_league_season)
    test_service.game_repository.get_max_week_by_season.assert_called_once_with(season_id)
    test_service.season_repository.get_season.assert_called_once_with(season_id)
    test_service.season_repository.update_season.assert_called_once_with(dest_season)
    test_service.team_season_repository.get_team_seasons_by_season.assert_called_once_with(season_id)
    test_service.season_rankings_repository.get_data_for_rankings_update.assert_called_once_with(fake_team_season)
    fake_team_season.update_rankings.assert_not_called()
    test_service.team_season_repository.update_team_season.assert_not_called()


def test_run_weekly_update_when_team_season_schedule_totals_schedule_games_is_not_none_and_team_season_schedule_averages_is_none_should_not_update_rankings_for_any_team_season(
        test_service
):
    # Arrange
    league_id = "League"
    season_id = 1

    league_season_totals = LeagueSeasonTotals(total_games=0, total_points=0)
    test_service.league_season_totals_repository.get_league_season_totals.return_value = league_season_totals

    fake_league_season = MagicMock(LeagueSeason)
    test_service.league_season_repository.get_league_season_by_league_and_season.return_value = fake_league_season
    test_service.game_repository.get_max_week_by_season.return_value = 4

    dest_season = MagicMock(Season)
    test_service.season_repository.get_season.return_value = dest_season

    fake_team_season = MagicMock(TeamSeason)
    team_seasons = [
        fake_team_season,
    ]
    test_service.team_season_repository.get_team_seasons_by_season.return_value = team_seasons

    test_service.season_rankings_repository.get_data_for_rankings_update.return_value = \
        {
            'team_season_schedule_totals': {'schedule_games': 0},
            'team_season_schedule_averages': None,
        }

    # Act
    test_service.run_weekly_update(league_id, season_id)

    # Assert
    test_service.league_season_totals_repository.get_league_season_totals.assert_called_once_with(league_id, season_id)
    test_service.league_season_repository.get_league_season_by_league_and_season.assert_called_once_with(league_id, season_id)
    fake_league_season.update_games_and_points.assert_called_once_with(league_season_totals.total_games, league_season_totals.total_points)
    test_service.league_season_repository.update_league_season.assert_called_once_with(fake_league_season)
    test_service.game_repository.get_max_week_by_season.assert_called_once_with(season_id)
    test_service.season_repository.get_season.assert_called_once_with(season_id)
    test_service.season_repository.update_season.assert_called_once_with(dest_season)
    test_service.team_season_repository.get_team_seasons_by_season.assert_called_once_with(season_id)
    test_service.season_rankings_repository.get_data_for_rankings_update.assert_called_once_with(fake_team_season)
    fake_team_season.update_rankings.assert_not_called()
    test_service.team_season_repository.update_team_season.assert_not_called()


def test_run_weekly_update_when_team_season_schedule_averages_is_empty_should_not_update_rankings_for_any_team_season(
        test_service
):
    # Arrange
    league_id = "League"
    season_id = 1

    league_season_totals = LeagueSeasonTotals(total_games=0, total_points=0)
    test_service.league_season_totals_repository.get_league_season_totals.return_value = league_season_totals

    fake_league_season = MagicMock(LeagueSeason)
    test_service.league_season_repository.get_league_season_by_league_and_season.return_value = fake_league_season
    test_service.game_repository.get_max_week_by_season.return_value = 4

    dest_season = MagicMock(Season)
    test_service.season_repository.get_season.return_value = dest_season

    fake_team_season = MagicMock(TeamSeason)
    team_seasons = [
        fake_team_season,
    ]
    test_service.team_season_repository.get_team_seasons_by_season.return_value = team_seasons

    test_service.season_rankings_repository.get_data_for_rankings_update.return_value = \
        {
            'team_season_schedule_totals': {'schedule_games': 0},
            'team_season_schedule_averages': dict(),
        }

    # Act
    test_service.run_weekly_update(league_id, season_id)

    # Assert
    test_service.league_season_totals_repository.get_league_season_totals.assert_called_once_with(league_id, season_id)
    test_service.league_season_repository.get_league_season_by_league_and_season.assert_called_once_with(league_id, season_id)
    fake_league_season.update_games_and_points.assert_called_once_with(league_season_totals.total_games, league_season_totals.total_points)
    test_service.league_season_repository.update_league_season.assert_called_once_with(fake_league_season)
    test_service.game_repository.get_max_week_by_season.assert_called_once_with(season_id)
    test_service.season_repository.get_season.assert_called_once_with(season_id)
    test_service.season_repository.update_season.assert_called_once_with(dest_season)
    test_service.team_season_repository.get_team_seasons_by_season.assert_called_once_with(season_id)
    test_service.season_rankings_repository.get_data_for_rankings_update.assert_called_once_with(fake_team_season)
    fake_team_season.update_rankings.assert_not_called()
    test_service.team_season_repository.update_team_season.assert_not_called()


def test_run_weekly_update_when_team_season_schedule_averages_is_not_empty_and_team_season_schedule_averages_avg_points_for_is_none_should_not_update_rankings_for_any_team_season(
        test_service
):
    # Arrange
    league_id = "League"
    season_id = 1

    league_season_totals = LeagueSeasonTotals(total_games=0, total_points=0)
    test_service.league_season_totals_repository.get_league_season_totals.return_value = league_season_totals

    fake_league_season = MagicMock(LeagueSeason)
    test_service.league_season_repository.get_league_season_by_league_and_season.return_value = fake_league_season
    test_service.game_repository.get_max_week_by_season.return_value = 4

    dest_season = MagicMock(Season)
    test_service.season_repository.get_season.return_value = dest_season

    fake_team_season = MagicMock(TeamSeason)
    team_seasons = [
        fake_team_season,
    ]
    test_service.team_season_repository.get_team_seasons_by_season.return_value = team_seasons

    test_service.season_rankings_repository.get_data_for_rankings_update.return_value = \
        {
            'team_season_schedule_totals': {'schedule_games': 0},
            'team_season_schedule_averages': {'avg_points_for': None, 'avg_points_against': None},
        }

    # Act
    test_service.run_weekly_update(league_id, season_id)

    # Assert
    test_service.league_season_totals_repository.get_league_season_totals.assert_called_once_with(league_id, season_id)
    test_service.league_season_repository.get_league_season_by_league_and_season.assert_called_once_with(league_id, season_id)
    fake_league_season.update_games_and_points.assert_called_once_with(league_season_totals.total_games, league_season_totals.total_points)
    test_service.league_season_repository.update_league_season.assert_called_once_with(fake_league_season)
    test_service.game_repository.get_max_week_by_season.assert_called_once_with(season_id)
    test_service.season_repository.get_season.assert_called_once_with(season_id)
    test_service.season_repository.update_season.assert_called_once_with(dest_season)
    test_service.team_season_repository.get_team_seasons_by_season.assert_called_once_with(season_id)
    test_service.season_rankings_repository.get_data_for_rankings_update.assert_called_once_with(fake_team_season)
    fake_team_season.update_rankings.assert_not_called()
    test_service.team_season_repository.update_team_season.assert_not_called()


def test_run_weekly_update_when_team_season_schedule_averages_avg_points_for_is_not_none_and_team_season_schedule_averages_avg_points_against_is_none_should_not_update_rankings_for_any_team_season(
        test_service
):
    # Arrange
    league_id = "League"
    season_id = 1

    league_season_totals = LeagueSeasonTotals(total_games=0, total_points=0)
    test_service.league_season_totals_repository.get_league_season_totals.return_value = league_season_totals

    fake_league_season = MagicMock(LeagueSeason)
    test_service.league_season_repository.get_league_season_by_league_and_season.return_value = fake_league_season
    test_service.game_repository.get_max_week_by_season.return_value = 4

    dest_season = MagicMock(Season)
    test_service.season_repository.get_season.return_value = dest_season

    fake_team_season = MagicMock(TeamSeason)
    team_seasons = [
        fake_team_season,
    ]
    test_service.team_season_repository.get_team_seasons_by_season.return_value = team_seasons

    test_service.season_rankings_repository.get_data_for_rankings_update.return_value = \
        {
            'team_season_schedule_totals': {'schedule_games': 0},
            'team_season_schedule_averages': {'avg_points_for': 0, 'avg_points_against': None},
        }

    # Act
    test_service.run_weekly_update(league_id, season_id)

    # Assert
    test_service.league_season_totals_repository.get_league_season_totals.assert_called_once_with(league_id, season_id)
    test_service.league_season_repository.get_league_season_by_league_and_season.assert_called_once_with(league_id, season_id)
    fake_league_season.update_games_and_points.assert_called_once_with(league_season_totals.total_games, league_season_totals.total_points)
    test_service.league_season_repository.update_league_season.assert_called_once_with(fake_league_season)
    test_service.game_repository.get_max_week_by_season.assert_called_once_with(season_id)
    test_service.season_repository.get_season.assert_called_once_with(season_id)
    test_service.season_repository.update_season.assert_called_once_with(dest_season)
    test_service.team_season_repository.get_team_seasons_by_season.assert_called_once_with(season_id)
    test_service.season_rankings_repository.get_data_for_rankings_update.assert_called_once_with(fake_team_season)
    fake_team_season.update_rankings.assert_not_called()
    test_service.team_season_repository.update_team_season.assert_not_called()


def test_run_weekly_update_when_team_season_schedule_averages_avg_points_against_is_not_none_and_league_season_is_none_should_not_update_rankings_for_any_team_season(
        test_service
):
    # Arrange
    league_id = "League"
    season_id = 1

    league_season_totals = LeagueSeasonTotals(total_games=0, total_points=0)
    test_service.league_season_totals_repository.get_league_season_totals.return_value = league_season_totals

    fake_league_season = MagicMock(LeagueSeason)
    test_service.league_season_repository.get_league_season_by_league_and_season.return_value = fake_league_season
    test_service.game_repository.get_max_week_by_season.return_value = 4

    dest_season = MagicMock(Season)
    test_service.season_repository.get_season.return_value = dest_season

    fake_team_season = MagicMock(TeamSeason)
    team_seasons = [
        fake_team_season,
    ]
    test_service.team_season_repository.get_team_seasons_by_season.return_value = team_seasons

    test_service.season_rankings_repository.get_data_for_rankings_update.return_value = \
        {
            'team_season_schedule_totals': {'schedule_games': 0},
            'team_season_schedule_averages': {'avg_points_for': 0, 'avg_points_against': 0},
            'league_season': None
        }

    # Act
    test_service.run_weekly_update(league_id, season_id)

    # Assert
    test_service.league_season_totals_repository.get_league_season_totals.assert_called_once_with(league_id, season_id)
    test_service.league_season_repository.get_league_season_by_league_and_season.assert_called_once_with(league_id, season_id)
    fake_league_season.update_games_and_points.assert_called_once_with(league_season_totals.total_games, league_season_totals.total_points)
    test_service.league_season_repository.update_league_season.assert_called_once_with(fake_league_season)
    test_service.game_repository.get_max_week_by_season.assert_called_once_with(season_id)
    test_service.season_repository.get_season.assert_called_once_with(season_id)
    test_service.season_repository.update_season.assert_called_once_with(dest_season)
    test_service.team_season_repository.get_team_seasons_by_season.assert_called_once_with(season_id)
    test_service.season_rankings_repository.get_data_for_rankings_update.assert_called_once_with(fake_team_season)
    fake_team_season.update_rankings.assert_not_called()
    test_service.team_season_repository.update_team_season.assert_not_called()


def test_run_weekly_update_when_league_season_is_empty_should_not_update_rankings_for_any_team_season(
        test_service
):
    # Arrange
    league_id = "League"
    season_id = 1

    league_season_totals = LeagueSeasonTotals(total_games=0, total_points=0)
    test_service.league_season_totals_repository.get_league_season_totals.return_value = league_season_totals

    fake_league_season = MagicMock(LeagueSeason)
    test_service.league_season_repository.get_league_season_by_league_and_season.return_value = fake_league_season
    test_service.game_repository.get_max_week_by_season.return_value = 4

    dest_season = MagicMock(Season)
    test_service.season_repository.get_season.return_value = dest_season

    fake_team_season = MagicMock(TeamSeason)
    team_seasons = [
        fake_team_season,
    ]
    test_service.team_season_repository.get_team_seasons_by_season.return_value = team_seasons

    test_service.season_rankings_repository.get_data_for_rankings_update.return_value = \
        {
            'team_season_schedule_totals': {'schedule_games': 0},
            'team_season_schedule_averages': {'avg_points_for': 0, 'avg_points_against': 0},
            'league_season': dict()
        }

    # Act
    test_service.run_weekly_update(league_id, season_id)

    # Assert
    test_service.league_season_totals_repository.get_league_season_totals.assert_called_once_with(league_id, season_id)
    test_service.league_season_repository.get_league_season_by_league_and_season.assert_called_once_with(league_id, season_id)
    fake_league_season.update_games_and_points.assert_called_once_with(league_season_totals.total_games, league_season_totals.total_points)
    test_service.league_season_repository.update_league_season.assert_called_once_with(fake_league_season)
    test_service.game_repository.get_max_week_by_season.assert_called_once_with(season_id)
    test_service.season_repository.get_season.assert_called_once_with(season_id)
    test_service.season_repository.update_season.assert_called_once_with(dest_season)
    test_service.team_season_repository.get_team_seasons_by_season.assert_called_once_with(season_id)
    test_service.season_rankings_repository.get_data_for_rankings_update.assert_called_once_with(fake_team_season)
    fake_team_season.update_rankings.assert_not_called()
    test_service.team_season_repository.update_team_season.assert_not_called()


def test_run_weekly_update_when_league_season_is_not_empty_and_league_season_average_points_is_none_should_not_update_rankings_for_any_team_season(
        test_service
):
    # Arrange
    league_id = "League"
    season_id = 1

    league_season_totals = LeagueSeasonTotals(total_games=0, total_points=0)
    test_service.league_season_totals_repository.get_league_season_totals.return_value = league_season_totals

    fake_league_season = MagicMock(LeagueSeason)
    test_service.league_season_repository.get_league_season_by_league_and_season.return_value = fake_league_season
    test_service.game_repository.get_max_week_by_season.return_value = 4

    dest_season = MagicMock(Season)
    test_service.season_repository.get_season.return_value = dest_season

    fake_team_season = MagicMock(TeamSeason)
    team_seasons = [
        fake_team_season,
    ]
    test_service.team_season_repository.get_team_seasons_by_season.return_value = team_seasons

    test_service.season_rankings_repository.get_data_for_rankings_update.return_value = \
        {
            'team_season_schedule_totals': {'schedule_games': 0},
            'team_season_schedule_averages': {'avg_points_for': 0, 'avg_points_against': 0},
            'league_season': {'average_points': None}
        }

    # Act
    test_service.run_weekly_update(league_id, season_id)

    # Assert
    test_service.league_season_totals_repository.get_league_season_totals.assert_called_once_with(league_id, season_id)
    test_service.league_season_repository.get_league_season_by_league_and_season.assert_called_once_with(league_id, season_id)
    fake_league_season.update_games_and_points.assert_called_once_with(league_season_totals.total_games, league_season_totals.total_points)
    test_service.league_season_repository.update_league_season.assert_called_once_with(fake_league_season)
    test_service.game_repository.get_max_week_by_season.assert_called_once_with(season_id)
    test_service.season_repository.get_season.assert_called_once_with(season_id)
    test_service.season_repository.update_season.assert_called_once_with(dest_season)
    test_service.team_season_repository.get_team_seasons_by_season.assert_called_once_with(season_id)
    test_service.season_rankings_repository.get_data_for_rankings_update.assert_called_once_with(fake_team_season)
    fake_team_season.update_rankings.assert_not_called()
    test_service.team_season_repository.update_team_season.assert_not_called()


def test_run_weekly_update_when_team_season_schedule_totals_and_averages_and_league_season_are_good_should_update_rankings_for_team_season(
        test_service
):
    # Arrange
    league_id = "League"
    season_id = 1

    league_season_totals = LeagueSeasonTotals(total_games=0, total_points=0)
    test_service.league_season_totals_repository.get_league_season_totals.return_value = league_season_totals

    fake_league_season = MagicMock(LeagueSeason)
    test_service.league_season_repository.get_league_season_by_league_and_season.return_value = fake_league_season
    test_service.game_repository.get_max_week_by_season.return_value = 4

    dest_season = MagicMock(Season)
    test_service.season_repository.get_season.return_value = dest_season

    fake_team_season = MagicMock(TeamSeason)
    team_seasons = [
        fake_team_season,
    ]
    test_service.team_season_repository.get_team_seasons_by_season.return_value = team_seasons

    rankings_data =\
        {
            'team_season_schedule_totals': {'schedule_games': 0},
            'team_season_schedule_averages': {'avg_points_for': 0, 'avg_points_against': 0},
            'league_season': {'average_points': 0}
        }
    test_service.season_rankings_repository.get_data_for_rankings_update.return_value = rankings_data

    # Act
    test_service.run_weekly_update(league_id, season_id)

    # Assert
    test_service.league_season_totals_repository.get_league_season_totals.assert_called_once_with(league_id, season_id)
    test_service.league_season_repository.get_league_season_by_league_and_season.assert_called_once_with(league_id, season_id)
    fake_league_season.update_games_and_points.assert_called_once_with(league_season_totals.total_games, league_season_totals.total_points)
    test_service.league_season_repository.update_league_season.assert_called_once_with(fake_league_season)
    test_service.game_repository.get_max_week_by_season.assert_called_once_with(season_id)
    test_service.season_repository.get_season.assert_called_once_with(season_id)
    test_service.season_repository.update_season.assert_called_once_with(dest_season)
    test_service.team_season_repository.get_team_seasons_by_season.assert_called_once_with(season_id)
    test_service.season_rankings_repository.get_data_for_rankings_update.assert_called_once_with(fake_team_season)
    fake_team_season.update_rankings.assert_called_once_with(
        rankings_data['team_season_schedule_averages']['avg_points_for'],
        rankings_data['team_season_schedule_averages']['avg_points_against'],
        rankings_data['league_season']['average_points']
    )
    test_service.team_season_repository.update_team_season.assert_called_once_with(fake_team_season)


def test_run_weekly_update_when_more_than_one_good_team_season_should_update_rankings_for_all_team_seasons(
        test_service
):
    # Arrange
    league_id = "League"
    season_id = 1

    league_season_totals = LeagueSeasonTotals(total_games=0, total_points=0)
    test_service.league_season_totals_repository.get_league_season_totals.return_value = league_season_totals

    fake_league_season = MagicMock(LeagueSeason)
    test_service.league_season_repository.get_league_season_by_league_and_season.return_value = fake_league_season
    test_service.game_repository.get_max_week_by_season.return_value = 4

    dest_season = MagicMock(Season)
    test_service.season_repository.get_season.return_value = dest_season

    fake_team_seasons = [MagicMock(TeamSeason), MagicMock(TeamSeason), MagicMock(TeamSeason)]
    team_seasons = [
        fake_team_seasons[0],
        fake_team_seasons[1],
        fake_team_seasons[2],
    ]
    test_service.team_season_repository.get_team_seasons_by_season.return_value = team_seasons

    rankings_data =\
        {
            'team_season_schedule_totals': {'schedule_games': 0},
            'team_season_schedule_averages': {'avg_points_for': 0, 'avg_points_against': 0},
            'league_season': {'average_points': 0}
        }
    test_service.season_rankings_repository.get_data_for_rankings_update.return_value = rankings_data

    # Act
    test_service.run_weekly_update(league_id, season_id)

    # Assert
    test_service.league_season_totals_repository.get_league_season_totals.assert_called_once_with(league_id, season_id)
    test_service.league_season_repository.get_league_season_by_league_and_season.assert_called_once_with(league_id, season_id)
    fake_league_season.update_games_and_points.assert_called_once_with(league_season_totals.total_games, league_season_totals.total_points)
    test_service.league_season_repository.update_league_season.assert_called_once_with(fake_league_season)
    test_service.game_repository.get_max_week_by_season.assert_called_once_with(season_id)
    test_service.season_repository.get_season.assert_called_once_with(season_id)
    test_service.season_repository.update_season.assert_called_once_with(dest_season)
    test_service.team_season_repository.get_team_seasons_by_season.assert_called_once_with(season_id)
    test_service.season_rankings_repository.get_data_for_rankings_update.assert_has_calls([
        call(fake_team_seasons[0]),
        call(fake_team_seasons[1]),
        call(fake_team_seasons[2]),
    ])
    for ts in fake_team_seasons:
        ts.update_rankings.assert_called_once_with(
            rankings_data['team_season_schedule_averages']['avg_points_for'],
            rankings_data['team_season_schedule_averages']['avg_points_against'],
            rankings_data['league_season']['average_points']
        )
    test_service.team_season_repository.update_team_season.assert_has_calls([
        call(fake_team_seasons[0]),
        call(fake_team_seasons[1]),
        call(fake_team_seasons[2]),
    ])
