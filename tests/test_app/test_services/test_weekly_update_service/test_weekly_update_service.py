from decimal import Decimal

from unittest.mock import Mock, call, patch

import pytest

from app.data.models.game import Game
from app.data.models.league_season import LeagueSeason
from app.data.models.league_season_totals import LeagueSeasonTotals
from app.data.models.season import Season
from app.data.models.team_season import TeamSeason
from app.data.models.team_season_schedule_averages import TeamSeasonScheduleAverages
from app.data.models.team_season_schedule_totals import TeamSeasonScheduleTotals

from app.services.weekly_update_service.weekly_update_service import WeeklyUpdateService


@pytest.fixture()
@patch('app.services.weekly_update_service.weekly_update_service.TeamSeasonScheduleRepository')
@patch('app.services.weekly_update_service.weekly_update_service.LeagueSeasonTotalsRepository')
@patch('app.services.weekly_update_service.weekly_update_service.TeamSeasonRepository')
@patch('app.services.weekly_update_service.weekly_update_service.LeagueSeasonRepository')
@patch('app.services.weekly_update_service.weekly_update_service.GameRepository')
@patch('app.services.weekly_update_service.weekly_update_service.SeasonRepository')
def test_service(
        fake_season_repository, fake_game_repository, fake_league_season_repository, fake_team_season_repository,
        fake_league_season_totals_repository, fake_team_season_schedule_repository
):
    test_service = WeeklyUpdateService(
        fake_season_repository,
        fake_game_repository,
        fake_league_season_repository,
        fake_team_season_repository,
        fake_league_season_totals_repository,
        fake_team_season_schedule_repository
    )
    return test_service


def test_run_weekly_update_when_league_season_totals_is_none_and_games_is_none_should_not_update_anything(
        test_service
):
    # Arrange
    test_service._league_season_totals_repository.get_league_season_totals.return_value = None

    fake_league_season = Mock(LeagueSeason)
    test_service._league_season_repository.get_league_season_by_league_name_and_season_year.return_value = None
    test_service._game_repository.get_games.return_value = None
    fake_team_season = Mock(TeamSeason)

    league_name = "APFA"
    season_year = 1

    # Act
    test_service.run_weekly_update(league_name, season_year)

    # Assert
    test_service._league_season_totals_repository.get_league_season_totals.assert_any_call(league_name, season_year)
    test_service._league_season_repository.get_league_season_by_league_name_and_season_year.assert_not_called()
    fake_league_season.update_games_and_points.assert_not_called()
    test_service._league_season_repository.update_league_season.assert_not_called()
    test_service._game_repository.get_games.assert_called()
    test_service._season_repository.get_season.assert_not_called()
    test_service._season_repository.update_season.assert_not_called()
    test_service._team_season_repository.get_team_seasons_by_season.assert_not_called()
    test_service._team_season_schedule_repository.get_team_season_schedule_totals.assert_not_called()
    test_service._team_season_schedule_repository.get_team_season_schedule_averages.assert_not_called()
    fake_team_season.update_rankings.assert_not_called()
    test_service._team_season_repository.update_team_season.assert_not_called()


def test_run_weekly_update_when_league_season_totals_total_games_is_none_and_games_is_none_should_not_update_anything(
        test_service
):
    # Arrange
    test_service._league_season_totals_repository.get_league_season_totals.return_value \
        = LeagueSeasonTotals(total_games=None, total_points=None, average_points=None, week_count=None)

    fake_league_season = Mock(LeagueSeason)
    test_service._league_season_repository.get_league_season_by_league_name_and_season_year.return_value = None
    test_service._game_repository.get_games.return_value = None
    fake_team_season = Mock(TeamSeason)

    league_name = "APFA"
    season_year = 1

    # Act
    test_service.run_weekly_update(league_name, season_year)

    # Assert
    test_service._league_season_totals_repository.get_league_season_totals.assert_any_call(league_name, season_year)
    test_service._league_season_repository.get_league_season_by_league_name_and_season_year.assert_not_called()
    fake_league_season.update_games_and_points.assert_not_called()
    test_service._league_season_repository.update_league_season.assert_not_called()
    test_service._game_repository.get_games.assert_called()
    test_service._season_repository.get_season.assert_not_called()
    test_service._season_repository.update_season.assert_not_called()
    test_service._team_season_repository.get_team_seasons_by_season.assert_not_called()
    test_service._team_season_schedule_repository.get_team_season_schedule_totals.assert_not_called()
    test_service._team_season_schedule_repository.get_team_season_schedule_averages.assert_not_called()
    fake_team_season.update_rankings.assert_not_called()
    test_service._team_season_repository.update_team_season.assert_not_called()


def test_run_weekly_update_when_league_season_totals_total_points_is_none_and_games_is_none_should_not_update_anything(
        test_service
):
    # Arrange
    test_service._league_season_totals_repository.get_league_season_totals.return_value \
        = LeagueSeasonTotals(total_games=0, total_points=None, average_points=None, week_count=None)

    fake_league_season = Mock(LeagueSeason)
    test_service._league_season_repository.get_league_season_by_league_name_and_season_year.return_value = None
    test_service._game_repository.get_games.return_value = None
    fake_team_season = Mock(TeamSeason)

    league_name = "APFA"
    season_year = 1

    # Act
    test_service.run_weekly_update(league_name, season_year)

    # Assert
    test_service._league_season_totals_repository.get_league_season_totals.assert_any_call(league_name, season_year)
    test_service._league_season_repository.get_league_season_by_league_name_and_season_year.assert_not_called()
    fake_league_season.update_games_and_points.assert_not_called()
    test_service._league_season_repository.update_league_season.assert_not_called()
    test_service._game_repository.get_games.assert_called()
    test_service._season_repository.get_season.assert_not_called()
    test_service._season_repository.update_season.assert_not_called()
    test_service._team_season_repository.get_team_seasons_by_season.assert_not_called()
    test_service._team_season_schedule_repository.get_team_season_schedule_totals.assert_not_called()
    test_service._team_season_schedule_repository.get_team_season_schedule_averages.assert_not_called()
    fake_team_season.update_rankings.assert_not_called()
    test_service._team_season_repository.update_team_season.assert_not_called()


def test_run_weekly_update_when_league_season_is_none_and_games_is_none_should_not_update_anything(test_service):
    # Arrange
    test_service._league_season_totals_repository.get_league_season_totals.return_value \
        = LeagueSeasonTotals(total_games=0, total_points=0, average_points=Decimal('0'), week_count=0)

    fake_league_season = Mock(LeagueSeason)
    test_service._league_season_repository.get_league_season_by_league_name_and_season_year.return_value = None
    test_service._game_repository.get_games.return_value = None
    fake_team_season = Mock(TeamSeason)

    league_name = "APFA"
    season_year = 1

    # Act
    test_service.run_weekly_update(league_name, season_year)

    # Assert
    test_service._league_season_totals_repository.get_league_season_totals.assert_any_call(league_name, season_year)
    test_service._league_season_repository.get_league_season_by_league_name_and_season_year.assert_called_once_with(
        league_name, season_year
    )
    fake_league_season.update_games_and_points.assert_not_called()
    test_service._league_season_repository.update_league_season.assert_not_called()
    test_service._game_repository.get_games.assert_called()
    test_service._season_repository.get_season.assert_not_called()
    test_service._season_repository.update_season.assert_not_called()
    test_service._team_season_repository.get_team_seasons_by_season.assert_not_called()
    test_service._team_season_schedule_repository.get_team_season_schedule_totals.assert_not_called()
    test_service._team_season_schedule_repository.get_team_season_schedule_averages.assert_not_called()
    fake_team_season.update_rankings.assert_not_called()
    test_service._team_season_repository.update_team_season.assert_not_called()


def test_run_weekly_update_when_league_season_totals_and_league_season_are_not_none_and_games_is_none_should_update_league_season_total_points_and_games(
        test_service
):
    # Arrange
    league_season_totals = LeagueSeasonTotals()
    league_season_totals.total_games = 1
    league_season_totals.total_points = 2
    test_service._league_season_totals_repository.get_league_season_totals.return_value = league_season_totals

    fake_league_season = Mock(LeagueSeason)
    test_service._league_season_repository.get_league_season_by_league_name_and_season_year.return_value = fake_league_season
    test_service._game_repository.get_games.return_value = None
    fake_team_season = Mock(TeamSeason)

    league_name = "APFA"
    season_year = 1

    # Act
    test_service.run_weekly_update(league_name, season_year)

    # Assert
    test_service._league_season_totals_repository.get_league_season_totals.assert_any_call(league_name, season_year)
    test_service._league_season_repository.get_league_season_by_league_name_and_season_year.assert_called_once_with(
        league_name, season_year
    )
    fake_league_season.update_games_and_points.assert_any_call(
        league_season_totals.total_games, league_season_totals.total_points
    )
    test_service._league_season_repository.update_league_season.assert_any_call(fake_league_season)
    test_service._game_repository.get_games.assert_called()
    test_service._season_repository.get_season.assert_not_called()
    test_service._season_repository.update_season.assert_not_called()
    test_service._team_season_repository.get_team_seasons_by_season.assert_not_called()
    test_service._team_season_schedule_repository.get_team_season_schedule_totals.assert_not_called()
    test_service._team_season_schedule_repository.get_team_season_schedule_averages.assert_not_called()
    fake_team_season.update_rankings.assert_not_called()
    test_service._team_season_repository.update_team_season.assert_not_called()


def test_run_weekly_update_when_games_is_none_should_not_update_week_count(test_service):
    # Arrange
    league_season_totals = LeagueSeasonTotals()
    league_season_totals.total_games = 1
    league_season_totals.total_points = 2
    test_service._league_season_totals_repository.get_league_season_totals.return_value = league_season_totals

    fake_league_season = Mock(LeagueSeason)
    test_service._league_season_repository.get_league_season_by_league_name_and_season_year.return_value = fake_league_season
    test_service._game_repository.get_games.return_value = None
    fake_team_season = Mock(TeamSeason)

    league_name = "APFA"
    season_year = 1

    # Act
    test_service.run_weekly_update(league_name, season_year)

    # Assert
    test_service._league_season_totals_repository.get_league_season_totals.assert_any_call(league_name, season_year)
    test_service._league_season_repository.get_league_season_by_league_name_and_season_year.assert_called_once_with(
        league_name, season_year
    )
    fake_league_season.update_games_and_points.assert_any_call(
        league_season_totals.total_games, league_season_totals.total_points
    )
    test_service._league_season_repository.update_league_season.assert_any_call(fake_league_season)
    test_service._game_repository.get_games.assert_called()
    test_service._season_repository.get_season.assert_not_called()
    test_service._season_repository.update_season.assert_not_called()
    test_service._team_season_repository.get_team_seasons_by_season.assert_not_called()
    test_service._team_season_schedule_repository.get_team_season_schedule_totals.assert_not_called()
    test_service._team_season_schedule_repository.get_team_season_schedule_averages.assert_not_called()
    fake_team_season.update_rankings.assert_not_called()
    test_service._team_season_repository.update_team_season.assert_not_called()


def test_run_weekly_update_when_games_is_empty_should_not_update_week_count(test_service):
    # Arrange
    league_season_totals = LeagueSeasonTotals()
    league_season_totals.total_games = 1
    league_season_totals.total_points = 2
    test_service._league_season_totals_repository.get_league_season_totals.return_value = league_season_totals

    fake_league_season = Mock(LeagueSeason)
    test_service._league_season_repository.get_league_season_by_league_name_and_season_year.return_value = fake_league_season
    test_service._game_repository.get_games.return_value = []
    fake_team_season = Mock(TeamSeason)

    league_name = "APFA"
    season_year = 1

    # Act
    test_service.run_weekly_update(league_name, season_year)

    # Assert
    test_service._league_season_totals_repository.get_league_season_totals.assert_any_call(league_name, season_year)
    test_service._league_season_repository.get_league_season_by_league_name_and_season_year.assert_called_once_with(
        league_name, season_year
    )
    fake_league_season.update_games_and_points.assert_any_call(
        league_season_totals.total_games, league_season_totals.total_points
    )
    test_service._league_season_repository.update_league_season.assert_any_call(fake_league_season)
    test_service._game_repository.get_games.assert_called()
    test_service._season_repository.get_season.assert_not_called()
    test_service._season_repository.update_season.assert_not_called()
    test_service._team_season_repository.get_team_seasons_by_season.assert_not_called()
    test_service._team_season_schedule_repository.get_team_season_schedule_totals.assert_not_called()
    test_service._team_season_schedule_repository.get_team_season_schedule_averages.assert_not_called()
    fake_team_season.update_rankings.assert_not_called()
    test_service._team_season_repository.update_team_season.assert_not_called()


def test_run_weekly_update_when_games_has_no_games_for_specified_year_should_not_update_week_count(test_service):
    # Arrange
    league_season_totals = LeagueSeasonTotals()
    league_season_totals.total_games = 1
    league_season_totals.total_points = 2
    test_service._league_season_totals_repository.get_league_season_totals.return_value = league_season_totals

    fake_league_season = Mock(LeagueSeason)
    test_service._league_season_repository.get_league_season_by_league_name_and_season_year.return_value = fake_league_season

    season_year = 1
    test_service._game_repository.get_games.return_value = [
        Game(season_year=season_year, week=0, guest_name="Guest", guest_score=0, host_name="Host", host_score=0),
    ]

    fake_team_season = Mock(TeamSeason)

    league_name = "APFA"

    # Act
    test_service.run_weekly_update(league_name, season_year)

    # Assert
    test_service._league_season_totals_repository.get_league_season_totals.assert_any_call(league_name, season_year)
    test_service._league_season_repository.get_league_season_by_league_name_and_season_year.assert_called_once_with(
        league_name, season_year
    )
    fake_league_season.update_games_and_points.assert_any_call(
        league_season_totals.total_games, league_season_totals.total_points
    )
    test_service._league_season_repository.update_league_season.assert_any_call(fake_league_season)
    test_service._game_repository.get_games.assert_called()
    test_service._season_repository.get_season_by_year.assert_called_once_with(season_year)
    test_service._season_repository.update_season.assert_called_once_with(
        test_service._season_repository.get_season_by_year.return_value
    )
    test_service._team_season_repository.get_team_seasons_by_season.assert_not_called()
    test_service._team_season_schedule_repository.get_team_season_schedule_totals.assert_not_called()
    test_service._team_season_schedule_repository.get_team_season_schedule_averages.assert_not_called()
    fake_team_season.update_rankings.assert_not_called()
    test_service._team_season_repository.update_team_season.assert_not_called()


def test_run_weekly_update_when_games_has_games_for_specified_year_and_season_for_specified_year_is_none_should_not_update_week_count(
        test_service
):
    # Arrange
    league_season_totals = LeagueSeasonTotals()
    league_season_totals.total_games = 1
    league_season_totals.total_points = 2
    test_service._league_season_totals_repository.get_league_season_totals.return_value = league_season_totals

    fake_league_season = Mock(LeagueSeason)
    test_service._league_season_repository.get_league_season_by_league_name_and_season_year.return_value = fake_league_season

    season_year = 1
    test_service._game_repository.get_games.return_value = [
        Game(season_year=season_year, week=1, guest_name="Guest", guest_score=0, host_name="Host", host_score=0),
    ]

    season = Season(id=season_year, num_of_weeks_completed=0)
    test_service._season_repository.get_season.return_value = None

    fake_team_season = Mock(TeamSeason)

    league_name = "APFA"

    # Act
    test_service.run_weekly_update(league_name, season_year)

    # Assert
    test_service._league_season_totals_repository.get_league_season_totals.assert_any_call(league_name, season_year)
    test_service._league_season_repository.get_league_season_by_league_name_and_season_year.assert_called_once_with(
        league_name, season_year
    )
    fake_league_season.update_games_and_points.assert_any_call(
        league_season_totals.total_games, league_season_totals.total_points
    )
    test_service._league_season_repository.update_league_season.assert_any_call(fake_league_season)
    test_service._game_repository.get_games.assert_called()
    test_service._season_repository.get_season_by_year.assert_any_call(season_year)
    assert season.num_of_weeks_completed == 0
    test_service._season_repository.update_season.assert_called_once_with(
        test_service._season_repository.get_season_by_year.return_value
    )
    test_service._team_season_repository.get_team_seasons_by_season.assert_not_called()
    test_service._team_season_schedule_repository.get_team_season_schedule_totals.assert_not_called()
    test_service._team_season_schedule_repository.get_team_season_schedule_averages.assert_not_called()
    fake_team_season.update_rankings.assert_not_called()
    test_service._team_season_repository.update_team_season.assert_not_called()


def test_run_weekly_update_when_games_has_games_for_specified_year_and_season_for_specified_year_is_not_none_should_update_week_count(
        test_service
):
    # Arrange
    league_season_totals = LeagueSeasonTotals()
    league_season_totals.total_games = 1
    league_season_totals.total_points = 2
    test_service._league_season_totals_repository.get_league_season_totals.return_value = league_season_totals

    fake_league_season = Mock(LeagueSeason)
    test_service._league_season_repository.get_league_season_by_league_name_and_season_year.return_value = fake_league_season

    season_year = 1
    week_count = 1
    test_service._game_repository.get_games.return_value = [
        Game(season_year=season_year, week=week_count, guest_name="Guest", guest_score=0, host_name="Host", host_score=0),
    ]

    season = Season(id=season_year, num_of_weeks_completed=0)
    test_service._season_repository.get_season_by_year.return_value = season

    fake_team_season = Mock(TeamSeason)

    league_name = "APFA"

    # Act
    test_service.run_weekly_update(league_name, season_year)

    # Assert
    test_service._league_season_totals_repository.get_league_season_totals.assert_any_call(league_name, season_year)
    test_service._league_season_repository.get_league_season_by_league_name_and_season_year.assert_called_once_with(
        league_name, season_year
    )
    fake_league_season.update_games_and_points.assert_any_call(
        league_season_totals.total_games, league_season_totals.total_points
    )
    test_service._league_season_repository.update_league_season.assert_any_call(fake_league_season)
    test_service._game_repository.get_games.assert_called()
    test_service._season_repository.get_season_by_year.assert_any_call(season_year)
    assert season.num_of_weeks_completed == week_count
    test_service._season_repository.update_season.assert_any_call(season)
    test_service._team_season_repository.get_team_seasons_by_season.assert_not_called()
    test_service._team_season_schedule_repository.get_team_season_schedule_totals.assert_not_called()
    test_service._team_season_schedule_repository.get_team_season_schedule_averages.assert_not_called()
    fake_team_season.update_rankings.assert_not_called()
    test_service._team_season_repository.update_team_season.assert_not_called()


def test_run_weekly_update_when_week_count_is_less_than_three_should_not_update_rankings(test_service):
    # Arrange
    league_season_totals = LeagueSeasonTotals()
    league_season_totals.total_games = 1
    league_season_totals.total_points = 2
    test_service._league_season_totals_repository.get_league_season_totals.return_value = league_season_totals

    fake_league_season = Mock(LeagueSeason)
    test_service._league_season_repository.get_league_season_by_league_name_and_season_year.return_value = fake_league_season

    season_year = 1
    week_count = 2
    test_service._game_repository.get_games.return_value = [
        Game(season_year=season_year, week=week_count, guest_name="Guest", guest_score=0, host_name="Host", host_score=0),
    ]

    season = Season(id=season_year, num_of_weeks_completed=0)
    test_service._season_repository.get_season_by_year.return_value = season

    fake_team_season = Mock(TeamSeason)

    league_name = "APFA"

    # Act
    test_service.run_weekly_update(league_name, season_year)

    # Assert
    test_service._league_season_totals_repository.get_league_season_totals.assert_any_call(league_name, season_year)
    test_service._league_season_repository.get_league_season_by_league_name_and_season_year.assert_called_once_with(
        league_name, season_year
    )
    fake_league_season.update_games_and_points.assert_any_call(
        league_season_totals.total_games, league_season_totals.total_points
    )
    test_service._league_season_repository.update_league_season.assert_any_call(fake_league_season)
    test_service._game_repository.get_games.assert_called()
    test_service._season_repository.get_season_by_year.assert_any_call(season_year)
    assert season.num_of_weeks_completed == week_count
    test_service._season_repository.update_season.assert_any_call(season)
    test_service._team_season_repository.get_team_seasons_by_season.assert_not_called()
    test_service._team_season_schedule_repository.get_team_season_schedule_totals.assert_not_called()
    test_service._team_season_schedule_repository.get_team_season_schedule_averages.assert_not_called()
    fake_team_season.update_rankings.assert_not_called()
    test_service._team_season_repository.update_team_season.assert_not_called()


def test_run_weekly_update_when_week_count_is_three_should_update_rankings(test_service):
    # Arrange
    league_season_totals = LeagueSeasonTotals()
    league_season_totals.total_games = 1
    league_season_totals.total_points = 2
    test_service._league_season_totals_repository.get_league_season_totals.return_value = league_season_totals

    fake_league_season = Mock(LeagueSeason)
    test_service._league_season_repository.get_league_season_by_league_name_and_season_year.return_value = fake_league_season

    season_year = 1
    week_count = 3
    test_service._game_repository.get_games.return_value = [
        Game(season_year=season_year, week=week_count, guest_name="Guest", guest_score=0, host_name="Host", host_score=0),
    ]

    season = Season(id=season_year, num_of_weeks_completed=0)
    test_service._season_repository.get_season_by_year.return_value = season

    fake_team_season = Mock(TeamSeason)
    test_service._team_season_repository.get_team_seasons_by_season.return_value = None

    league_name = "APFA"

    # Act
    test_service.run_weekly_update(league_name, season_year)

    # Assert
    test_service._league_season_totals_repository.get_league_season_totals.assert_any_call(league_name, season_year)
    test_service._league_season_repository.get_league_season_by_league_name_and_season_year.assert_called_once_with(
        league_name, season_year
    )
    fake_league_season.update_games_and_points.assert_any_call(
        league_season_totals.total_games, league_season_totals.total_points
    )
    test_service._league_season_repository.update_league_season.assert_any_call(fake_league_season)
    test_service._game_repository.get_games.assert_called()
    test_service._season_repository.get_season_by_year.assert_any_call(season_year)
    assert season.num_of_weeks_completed == week_count
    test_service._season_repository.update_season.assert_any_call(season)
    test_service._team_season_repository.get_team_seasons_by_season_year.assert_any_call(season_year)
    test_service._team_season_schedule_repository.get_team_season_schedule_totals.assert_not_called()
    test_service._team_season_schedule_repository.get_team_season_schedule_averages.assert_not_called()
    fake_team_season.update_rankings.assert_not_called()
    test_service._team_season_repository.update_team_season.assert_not_called()


def test_run_weekly_update_when_week_count_is_greater_than_three_should_update_rankings(test_service):
    # Arrange
    league_season_totals = LeagueSeasonTotals()
    league_season_totals.total_games = 1
    league_season_totals.total_points = 2
    test_service._league_season_totals_repository.get_league_season_totals.return_value = league_season_totals

    fake_league_season = Mock(LeagueSeason)
    test_service._league_season_repository.get_league_season_by_league_name_and_season_year.return_value = fake_league_season

    season_year = 1
    week_count = 4
    test_service._game_repository.get_games.return_value = [
        Game(season_year=season_year, week=week_count, guest_name="Guest", guest_score=0, host_name="Host", host_score=0),
    ]

    season = Season(id=season_year, num_of_weeks_completed=0)
    test_service._season_repository.get_season_by_year.return_value = season

    fake_team_season = Mock(TeamSeason)
    test_service._team_season_repository.get_team_seasons_by_season_year.return_value = None

    league_name = "APFA"

    # Act
    test_service.run_weekly_update(league_name, season_year)

    # Assert
    test_service._league_season_totals_repository.get_league_season_totals.assert_any_call(league_name, season_year)
    test_service._league_season_repository.get_league_season_by_league_name_and_season_year.assert_called_once_with(
        league_name, season_year
    )
    fake_league_season.update_games_and_points.assert_any_call(
        league_season_totals.total_games, league_season_totals.total_points
    )
    test_service._league_season_repository.update_league_season.assert_any_call(fake_league_season)
    test_service._game_repository.get_games.assert_called()
    test_service._season_repository.get_season_by_year.assert_any_call(season_year)
    assert season.num_of_weeks_completed == week_count
    test_service._season_repository.update_season.assert_any_call(season)
    test_service._team_season_repository.get_team_seasons_by_season_year.assert_any_call(season_year)
    test_service._team_season_schedule_repository.get_team_season_schedule_totals.assert_not_called()
    test_service._team_season_schedule_repository.get_team_season_schedule_averages.assert_not_called()
    fake_team_season.update_rankings.assert_not_called()
    test_service._team_season_repository.update_team_season.assert_not_called()


def test_run_weekly_update_when_week_count_is_greater_than_three_and_team_seasons_for_specified_year_is_none_should_not_update_rankings_for_any_team_season(
        test_service
):
    # Arrange
    league_season_totals = LeagueSeasonTotals()
    league_season_totals.total_games = 1
    league_season_totals.total_points = 2
    test_service._league_season_totals_repository.get_league_season_totals.return_value = league_season_totals

    fake_league_season = Mock(LeagueSeason)
    test_service._league_season_repository.get_league_season_by_league_name_and_season_year.return_value = fake_league_season

    season_year = 1
    week_count = 4
    test_service._game_repository.get_games.return_value = [
        Game(season_year=season_year, week=week_count, guest_name="Guest", guest_score=0, host_name="Host", host_score=0),
    ]

    season = Season(id=season_year, num_of_weeks_completed=0)
    test_service._season_repository.get_season_by_year.return_value = season

    fake_team_season = Mock(TeamSeason)
    test_service._team_season_repository.get_team_seasons_by_season_year.return_value = None

    league_name = "APFA"

    # Act
    test_service.run_weekly_update(league_name, season_year)

    # Assert
    test_service._league_season_totals_repository.get_league_season_totals.assert_any_call(league_name, season_year)
    test_service._league_season_repository.get_league_season_by_league_name_and_season_year.assert_called_once_with(
        league_name, season_year
    )
    fake_league_season.update_games_and_points.assert_any_call(league_season_totals.total_games,
                                                               league_season_totals.total_points)
    test_service._league_season_repository.update_league_season.assert_any_call(fake_league_season)
    test_service._game_repository.get_games.assert_called()
    test_service._season_repository.get_season_by_year.assert_any_call(season_year)
    assert season.num_of_weeks_completed == week_count
    test_service._season_repository.update_season.assert_any_call(season)
    test_service._team_season_repository.get_team_seasons_by_season_year.assert_any_call(season_year)
    test_service._team_season_schedule_repository.get_team_season_schedule_totals.assert_not_called()
    test_service._team_season_schedule_repository.get_team_season_schedule_averages.assert_not_called()
    fake_team_season.update_rankings.assert_not_called()
    test_service._team_season_repository.update_team_season.assert_not_called()


def test_run_weekly_update_when_week_count_is_greater_than_three_and_team_seasons_for_specified_year_is_empty_should_not_update_rankings_for_any_team_season(
        test_service
):
    # Arrange
    league_season_totals = LeagueSeasonTotals()
    league_season_totals.total_games = 1
    league_season_totals.total_points = 2
    test_service._league_season_totals_repository.get_league_season_totals.return_value = league_season_totals

    fake_league_season = Mock(LeagueSeason)
    test_service._league_season_repository.get_league_season_by_league_name_and_season_year.return_value = fake_league_season

    season_year = 1
    week_count = 4
    test_service._game_repository.get_games.return_value = [
        Game(season_year=season_year, week=week_count, guest_name="Guest", guest_score=0, host_name="Host", host_score=0),
    ]

    season = Season(id=season_year, num_of_weeks_completed=0)
    test_service._season_repository.get_season_by_year.return_value = season

    fake_team_season = Mock(TeamSeason)
    test_service._team_season_repository.get_team_seasons_by_season_year.return_value = []

    league_name = "APFA"

    # Act
    test_service.run_weekly_update(league_name, season_year)

    # Assert
    test_service._league_season_totals_repository.get_league_season_totals.assert_any_call(league_name, season_year)
    test_service._league_season_repository.get_league_season_by_league_name_and_season_year.assert_called_once_with(
        league_name, season_year
    )
    fake_league_season.update_games_and_points.assert_any_call(
        league_season_totals.total_games, league_season_totals.total_points
    )
    test_service._league_season_repository.update_league_season.assert_any_call(fake_league_season)
    test_service._game_repository.get_games.assert_called()
    test_service._season_repository.get_season_by_year.assert_any_call(season_year)
    assert season.num_of_weeks_completed == week_count
    test_service._season_repository.update_season.assert_any_call(season)
    test_service._team_season_repository.get_team_seasons_by_season_year.assert_any_call(season_year)
    test_service._team_season_schedule_repository.get_team_season_schedule_totals.assert_not_called()
    test_service._team_season_schedule_repository.get_team_season_schedule_averages.assert_not_called()
    fake_team_season.update_rankings.assert_not_called()
    test_service._team_season_repository.update_team_season.assert_not_called()


def test_run_weekly_update_when_week_count_is_greater_than_three_and_team_seasons_for_specified_year_is_not_empty_and_team_season_schedule_totals_is_none_should_not_update_rankings_for_any_team_season(
        test_service
):
    # Arrange
    league_season_totals = LeagueSeasonTotals()
    league_season_totals.total_games = 1
    league_season_totals.total_points = 2
    test_service._league_season_totals_repository.get_league_season_totals.return_value = league_season_totals

    fake_league_season = Mock(LeagueSeason)
    test_service._league_season_repository.get_league_season_by_league_name_and_season_year.return_value = fake_league_season

    season_year = 1
    week_count = 4
    test_service._game_repository.get_games.return_value = [
        Game(season_year=season_year, week=week_count, guest_name="Guest", guest_score=0, host_name="Host", host_score=0),
    ]

    season = Season(id=season_year, num_of_weeks_completed=0)
    test_service._season_repository.get_season_by_year.return_value = season

    fake_team_season = Mock(TeamSeason)
    fake_team_season.team_name = "Team"
    fake_team_season.season_year = season_year
    test_service._team_season_repository.get_team_seasons_by_season_year.return_value = [fake_team_season]

    test_service._team_season_schedule_repository.get_team_season_schedule_totals.return_value = None

    league_name = "APFA"

    # Act
    test_service.run_weekly_update(league_name, season_year)

    # Assert
    test_service._league_season_totals_repository.get_league_season_totals.assert_any_call(league_name, season_year)
    test_service._league_season_repository.get_league_season_by_league_name_and_season_year.assert_called_once_with(
        league_name, season_year
    )
    fake_league_season.update_games_and_points.assert_any_call(
        league_season_totals.total_games, league_season_totals.total_points
    )
    test_service._league_season_repository.update_league_season.assert_any_call(fake_league_season)
    test_service._game_repository.get_games.assert_called()
    test_service._season_repository.get_season_by_year.assert_any_call(season_year)
    assert season.num_of_weeks_completed == week_count
    test_service._season_repository.update_season.assert_any_call(season)
    test_service._team_season_repository.get_team_seasons_by_season_year.assert_any_call(season_year)
    test_service._team_season_schedule_repository.get_team_season_schedule_totals.assert_any_call(
        fake_team_season.team_name, fake_team_season.season_year
    )
    test_service._team_season_schedule_repository.get_team_season_schedule_averages.assert_not_called()
    fake_team_season.update_rankings.assert_not_called()
    test_service._team_season_repository.update_team_season.assert_not_called()


def test_run_weekly_update_when_week_count_is_greater_than_three_and_team_seasons_for_specified_year_is_not_empty_and_team_season_schedule_totals_schedule_games_is_none_should_not_update_rankings_for_any_team_season(
        test_service
):
    # Arrange
    league_season_totals = LeagueSeasonTotals()
    league_season_totals.total_games = 1
    league_season_totals.total_points = 2
    test_service._league_season_totals_repository.get_league_season_totals.return_value = league_season_totals

    fake_league_season = Mock(LeagueSeason)
    test_service._league_season_repository.get_league_season_by_league_name_and_season_year.return_value = fake_league_season

    season_year = 1
    week_count = 4
    test_service._game_repository.get_games.return_value = [
        Game(season_year=season_year, week=week_count, guest_name="Guest", guest_score=0, host_name="Host", host_score=0),
    ]

    season = Season(id=season_year, num_of_weeks_completed=0)
    test_service._season_repository.get_season_by_year.return_value = season

    fake_team_season = Mock(TeamSeason)
    fake_team_season.team_name = "Team"
    fake_team_season.season_year = season_year
    test_service._team_season_repository.get_team_seasons_by_season_year.return_value = [fake_team_season]

    team_season_schedule_totals = TeamSeasonScheduleTotals(schedule_games=None)
    test_service._team_season_schedule_repository.get_team_season_schedule_totals.return_value \
        = team_season_schedule_totals

    league_name = "APFA"

    # Act
    test_service.run_weekly_update(league_name, season_year)

    # Assert
    test_service._league_season_totals_repository.get_league_season_totals.assert_any_call(league_name, season_year)
    test_service._league_season_repository.get_league_season_by_league_name_and_season_year.assert_called_once_with(
        league_name, season_year
    )
    fake_league_season.update_games_and_points.assert_any_call(
        league_season_totals.total_games, league_season_totals.total_points
    )
    test_service._league_season_repository.update_league_season.assert_any_call(fake_league_season)
    test_service._game_repository.get_games.assert_called()
    test_service._season_repository.get_season_by_year.assert_any_call(season_year)
    assert season.num_of_weeks_completed == week_count
    test_service._season_repository.update_season.assert_any_call(season)
    test_service._team_season_repository.get_team_seasons_by_season_year.assert_any_call(season_year)
    test_service._team_season_schedule_repository.get_team_season_schedule_totals.assert_any_call(
        fake_team_season.team_name, fake_team_season.season_year
    )
    test_service._team_season_schedule_repository.get_team_season_schedule_averages.assert_not_called()
    fake_team_season.update_rankings.assert_not_called()
    test_service._team_season_repository.update_team_season.assert_not_called()


def test_run_weekly_update_when_week_count_is_greater_than_three_and_team_seasons_for_specified_year_is_not_empty_and_team_season_schedule_totals_schedule_games_is_not_none_and_team_season_schedule_averages_is_none_should_not_update_rankings_for_any_team_season(
        test_service
):
    # Arrange
    league_season_totals = LeagueSeasonTotals()
    league_season_totals.total_games = 1
    league_season_totals.total_points = 2
    test_service._league_season_totals_repository.get_league_season_totals.return_value = league_season_totals

    fake_league_season = Mock(LeagueSeason)
    test_service._league_season_repository.get_league_season_by_league_name_and_season_year.return_value = fake_league_season

    season_year = 1
    week_count = 4
    test_service._game_repository.get_games.return_value = [
        Game(season_year=season_year, week=week_count, guest_name="Guest", guest_score=0, host_name="Host", host_score=0),
    ]

    season = Season(id=season_year, num_of_weeks_completed=0)
    test_service._season_repository.get_season_by_year.return_value = season

    fake_team_season = Mock(TeamSeason)
    fake_team_season.team_name = "Team"
    fake_team_season.season_year = season_year
    test_service._team_season_repository.get_team_seasons_by_season_year.return_value = [fake_team_season]

    team_season_schedule_totals = TeamSeasonScheduleTotals(schedule_games=3)
    test_service._team_season_schedule_repository.get_team_season_schedule_totals.return_value \
        = team_season_schedule_totals

    test_service._team_season_schedule_repository.get_team_season_schedule_averages.return_value = None

    league_name = "APFA"

    # Act
    test_service.run_weekly_update(league_name, season_year)

    # Assert
    test_service._league_season_totals_repository.get_league_season_totals.assert_any_call(league_name, season_year)
    test_service._league_season_repository.get_league_season_by_league_name_and_season_year.assert_called_once_with(
        league_name, season_year
    )
    fake_league_season.update_games_and_points.assert_any_call(
        league_season_totals.total_games, league_season_totals.total_points
    )
    test_service._league_season_repository.update_league_season.assert_any_call(fake_league_season)
    test_service._game_repository.get_games.assert_called()
    test_service._season_repository.get_season_by_year.assert_any_call(season_year)
    assert season.num_of_weeks_completed == week_count
    test_service._season_repository.update_season.assert_any_call(season)
    test_service._team_season_repository.get_team_seasons_by_season_year.assert_any_call(season_year)
    test_service._team_season_schedule_repository.get_team_season_schedule_totals.assert_any_call(
        fake_team_season.team_name, fake_team_season.season_year
    )
    test_service._team_season_schedule_repository.get_team_season_schedule_averages.assert_any_call(
        fake_team_season.team_name, fake_team_season.season_year
    )
    fake_team_season.update_rankings.assert_not_called()
    test_service._team_season_repository.update_team_season.assert_not_called()


def test_run_weekly_update_when_week_count_is_greater_than_three_and_team_seasons_for_specified_year_is_not_empty_and_team_season_schedule_totals_schedule_games_is_not_none_and_team_season_schedule_average_points_for_is_none_should_not_update_rankings_for_any_team_season(
        test_service
):
    # Arrange
    league_season_totals = LeagueSeasonTotals()
    league_season_totals.total_games = 1
    league_season_totals.total_points = 2
    test_service._league_season_totals_repository.get_league_season_totals.return_value = league_season_totals

    fake_league_season = Mock(LeagueSeason)
    test_service._league_season_repository.get_league_season_by_league_name_and_season_year.return_value = fake_league_season

    season_year = 1
    week_count = 4
    test_service._game_repository.get_games.return_value = [
        Game(season_year=season_year, week=week_count, guest_name="Guest", guest_score=0, host_name="Host", host_score=0),
    ]

    season = Season(id=season_year, num_of_weeks_completed=0)
    test_service._season_repository.get_season_by_year.return_value = season

    fake_team_season = Mock(TeamSeason)
    fake_team_season.team_name = "Team"
    fake_team_season.season_year = season_year
    test_service._team_season_repository.get_team_seasons_by_season_year.return_value = [fake_team_season]

    team_season_schedule_totals = TeamSeasonScheduleTotals(schedule_games=3)
    test_service._team_season_schedule_repository.get_team_season_schedule_totals.return_value \
        = team_season_schedule_totals

    team_season_schedule_averages = TeamSeasonScheduleAverages(points_for=None, points_against=None)
    test_service._team_season_schedule_repository.get_team_season_schedule_averages.return_value \
        = team_season_schedule_averages

    league_name = "APFA"

    # Act
    test_service.run_weekly_update(league_name, season_year)

    # Assert
    test_service._league_season_totals_repository.get_league_season_totals.assert_any_call(league_name, season_year)
    test_service._league_season_repository.get_league_season_by_league_name_and_season_year.assert_called_once_with(
        league_name, season_year
    )
    fake_league_season.update_games_and_points.assert_any_call(
        league_season_totals.total_games, league_season_totals.total_points
    )
    test_service._league_season_repository.update_league_season.assert_any_call(fake_league_season)
    test_service._game_repository.get_games.assert_called()
    test_service._season_repository.get_season_by_year.assert_any_call(season_year)
    assert season.num_of_weeks_completed == week_count
    test_service._season_repository.update_season.assert_any_call(season)
    test_service._team_season_repository.get_team_seasons_by_season_year.assert_any_call(season_year)
    test_service._team_season_schedule_repository.get_team_season_schedule_totals.assert_any_call(
        fake_team_season.team_name, fake_team_season.season_year
    )
    test_service._team_season_schedule_repository.get_team_season_schedule_averages.assert_any_call(
        fake_team_season.team_name, fake_team_season.season_year
    )
    fake_team_season.update_rankings.assert_not_called()
    test_service._team_season_repository.update_team_season.assert_not_called()


def test_run_weekly_update_when_week_count_is_greater_than_three_and_team_seasons_for_specified_year_is_not_empty_and_team_season_schedule_totals_schedule_games_is_not_none_and_team_season_schedule_average_points_against_is_none_should_not_update_rankings_for_any_team_season(
        test_service
):
    # Arrange
    league_season_totals = LeagueSeasonTotals()
    league_season_totals.total_games = 1
    league_season_totals.total_points = 2
    test_service._league_season_totals_repository.get_league_season_totals.return_value = league_season_totals

    fake_league_season = Mock(LeagueSeason)
    test_service._league_season_repository.get_league_season_by_league_name_and_season_year.return_value = fake_league_season

    season_year = 1
    week_count = 4
    test_service._game_repository.get_games.return_value = [
        Game(season_year=season_year, week=week_count, guest_name="Guest", guest_score=0, host_name="Host", host_score=0),
    ]

    season = Season(id=season_year, num_of_weeks_completed=0)
    test_service._season_repository.get_season_by_year.return_value = season

    fake_team_season = Mock(TeamSeason)
    fake_team_season.team_name = "Team"
    fake_team_season.season_year = season_year
    test_service._team_season_repository.get_team_seasons_by_season_year.return_value = [fake_team_season]

    team_season_schedule_totals = TeamSeasonScheduleTotals(schedule_games=3)
    test_service._team_season_schedule_repository.get_team_season_schedule_totals.return_value \
        = team_season_schedule_totals

    team_season_schedule_averages = TeamSeasonScheduleAverages(points_for=Decimal('0'), points_against=None)
    test_service._team_season_schedule_repository.get_team_season_schedule_averages.return_value \
        = team_season_schedule_averages

    league_name = "APFA"

    # Act
    test_service.run_weekly_update(league_name, season_year)

    # Assert
    test_service._league_season_totals_repository.get_league_season_totals.assert_any_call(league_name, season_year)
    test_service._league_season_repository.get_league_season_by_league_name_and_season_year.assert_called_once_with(
        league_name, season_year
    )
    fake_league_season.update_games_and_points.assert_any_call(
        league_season_totals.total_games, league_season_totals.total_points
    )
    test_service._league_season_repository.update_league_season.assert_any_call(fake_league_season)
    test_service._game_repository.get_games.assert_called()
    test_service._season_repository.get_season_by_year.assert_any_call(season_year)
    assert season.num_of_weeks_completed == week_count
    test_service._season_repository.update_season.assert_any_call(season)
    test_service._team_season_repository.get_team_seasons_by_season_year.assert_any_call(season_year)
    test_service._team_season_schedule_repository.get_team_season_schedule_totals.assert_any_call(
        fake_team_season.team_name, fake_team_season.season_year
    )
    test_service._team_season_schedule_repository.get_team_season_schedule_averages.assert_any_call(
        fake_team_season.team_name, fake_team_season.season_year
    )
    fake_team_season.update_rankings.assert_not_called()
    test_service._team_season_repository.update_team_season.assert_not_called()


def test_run_weekly_update_when_week_count_is_greater_than_three_and_team_seasons_for_specified_year_is_not_empty_and_team_season_schedule_totals_schedule_games_is_not_none_and_team_season_schedule_average_points_for_and_points_against_are_not_none_and_league_season_is_none_should_not_update_rankings_for_any_team_season(
        test_service
):
    # Arrange
    league_season_totals = LeagueSeasonTotals()
    league_season_totals.total_games = 1
    league_season_totals.total_points = 2
    test_service._league_season_totals_repository.get_league_season_totals.return_value = league_season_totals

    fake_league_season = Mock(LeagueSeason)
    league_season = None
    test_service._league_season_repository.get_league_season_by_league_name_and_season_year.side_effect = (fake_league_season,
                                                                                                           league_season)

    season_year = 1
    week_count = 4
    test_service._game_repository.get_games.return_value = [
        Game(season_year=season_year, week=week_count, guest_name="Guest", guest_score=0, host_name="Host", host_score=0),
    ]

    season = Season(id=season_year, num_of_weeks_completed=0)
    test_service._season_repository.get_season_by_year.return_value = season

    fake_team_season = Mock(TeamSeason)
    fake_team_season.team_name = "Team"
    fake_team_season.season_year = season_year

    league_name = "APFA"
    fake_team_season.league_name = league_name
    test_service._team_season_repository.get_team_seasons_by_season_year.return_value = [fake_team_season]

    team_season_schedule_totals = TeamSeasonScheduleTotals(schedule_games=3)
    test_service._team_season_schedule_repository.get_team_season_schedule_totals.return_value \
        = team_season_schedule_totals

    team_season_schedule_averages = TeamSeasonScheduleAverages(points_for=Decimal('0'), points_against=Decimal('0'))
    test_service._team_season_schedule_repository.get_team_season_schedule_averages.return_value \
        = team_season_schedule_averages

    # Act
    test_service.run_weekly_update(league_name, season_year)

    # Assert
    test_service._league_season_totals_repository.get_league_season_totals.assert_any_call(league_name, season_year)
    test_service._league_season_repository.get_league_season_by_league_name_and_season_year.assert_has_calls([
        call(league_name, season_year),
        call(fake_team_season.league_name, fake_team_season.season_year)
    ])
    fake_league_season.update_games_and_points.assert_any_call(
        league_season_totals.total_games, league_season_totals.total_points
    )
    test_service._league_season_repository.update_league_season.assert_any_call(fake_league_season)
    test_service._game_repository.get_games.assert_called()
    test_service._season_repository.get_season_by_year.assert_any_call(season_year)
    assert season.num_of_weeks_completed == week_count
    test_service._season_repository.update_season.assert_any_call(season)
    test_service._team_season_repository.get_team_seasons_by_season_year.assert_any_call(season_year)
    test_service._team_season_schedule_repository.get_team_season_schedule_totals.assert_any_call(
        fake_team_season.team_name, fake_team_season.season_year
    )
    test_service._team_season_schedule_repository.get_team_season_schedule_averages.assert_any_call(
        fake_team_season.team_name, fake_team_season.season_year
    )
    fake_team_season.update_rankings.assert_not_called()
    test_service._team_season_repository.update_team_season.assert_not_called()


def test_run_weekly_update_when_week_count_is_greater_than_three_and_team_seasons_for_specified_year_is_not_empty_and_team_season_schedule_totals_schedule_games_is_not_none_and_team_season_schedule_average_points_for_and_points_against_are_not_none_and_league_season_average_points_is_none_should_not_update_rankings_for_any_team_season(
        test_service
):
    # Arrange
    league_season_totals = LeagueSeasonTotals()
    league_season_totals.total_games = 1
    league_season_totals.total_points = 2
    test_service._league_season_totals_repository.get_league_season_totals.return_value = league_season_totals

    fake_league_season = Mock(LeagueSeason)
    league_name = "APFA"
    season_year = 1
    league_season = LeagueSeason(league_name=league_name, season_year=season_year, average_points=None)
    test_service._league_season_repository.get_league_season_by_league_name_and_season_year.side_effect = (fake_league_season,
                                                                                                           league_season)

    week_count = 4
    test_service._game_repository.get_games.return_value = [
        Game(season_year=season_year, week=week_count, guest_name="Guest", guest_score=0, host_name="Host", host_score=0),
    ]

    season = Season(id=season_year, num_of_weeks_completed=0)
    test_service._season_repository.get_season_by_year.return_value = season

    fake_team_season = Mock(TeamSeason)
    fake_team_season.team_name = "Team"
    fake_team_season.season_year = season_year
    fake_team_season.league_name = league_name
    test_service._team_season_repository.get_team_seasons_by_season_year.return_value = [fake_team_season]

    team_season_schedule_totals = TeamSeasonScheduleTotals(schedule_games=3)
    test_service._team_season_schedule_repository.get_team_season_schedule_totals.return_value \
        = team_season_schedule_totals

    team_season_schedule_averages = TeamSeasonScheduleAverages(points_for=Decimal('0'), points_against=Decimal('0'))
    test_service._team_season_schedule_repository.get_team_season_schedule_averages.return_value \
        = team_season_schedule_averages

    # Act
    test_service.run_weekly_update(league_name, season_year)

    # Assert
    test_service._league_season_totals_repository.get_league_season_totals.assert_any_call(league_name, season_year)
    test_service._league_season_repository.get_league_season_by_league_name_and_season_year.assert_has_calls([
        call(league_name, season_year),
        call(fake_team_season.league_name, fake_team_season.season_year)
    ])
    fake_league_season.update_games_and_points.assert_any_call(
        league_season_totals.total_games, league_season_totals.total_points
    )
    test_service._league_season_repository.update_league_season.assert_any_call(fake_league_season)
    test_service._game_repository.get_games.assert_called()
    test_service._season_repository.get_season_by_year.assert_any_call(season_year)
    assert season.num_of_weeks_completed == week_count
    test_service._season_repository.update_season.assert_any_call(season)
    test_service._team_season_repository.get_team_seasons_by_season_year.assert_any_call(season_year)
    test_service._team_season_schedule_repository.get_team_season_schedule_totals.assert_any_call(
        fake_team_season.team_name, fake_team_season.season_year
    )
    test_service._team_season_schedule_repository.get_team_season_schedule_averages.assert_any_call(
        fake_team_season.team_name, fake_team_season.season_year
    )
    fake_team_season.update_rankings.assert_not_called()
    test_service._team_season_repository.update_team_season.assert_not_called()


def test_run_weekly_update_when_week_count_is_greater_than_three_and_team_seasons_for_specified_year_is_not_empty_and_team_season_schedule_totals_schedule_games_is_not_none_and_team_season_schedule_average_points_for_and_points_against_are_not_none_and_league_season_average_points_is_not_none_should_update_rankings_for_team_season(
        test_service
):
    # Arrange
    league_season_totals = LeagueSeasonTotals()
    league_season_totals.total_games = 1
    league_season_totals.total_points = 2
    test_service._league_season_totals_repository.get_league_season_totals.return_value = league_season_totals

    fake_league_season = Mock(LeagueSeason)
    league_name = "APFA"
    season_year = 1
    league_season = LeagueSeason(league_name=league_name, season_year=season_year, average_points=0.00)
    test_service._league_season_repository.get_league_season_by_league_name_and_season_year.side_effect = (fake_league_season,
                                                                                                           league_season)

    week_count = 4
    test_service._game_repository.get_games.return_value = [
        Game(season_year=season_year, week=week_count, guest_name="Guest", guest_score=0, host_name="Host", host_score=0),
    ]

    season = Season(id=season_year, num_of_weeks_completed=0)
    test_service._season_repository.get_season_by_year.return_value = season

    fake_team_season = Mock(TeamSeason)
    fake_team_season.team_name = "Team"
    fake_team_season.season_year = season_year
    fake_team_season.league_name = league_name
    test_service._team_season_repository.get_team_seasons_by_season_year.return_value = [fake_team_season]

    team_season_schedule_totals = TeamSeasonScheduleTotals(schedule_games=3)
    test_service._team_season_schedule_repository.get_team_season_schedule_totals.return_value \
        = team_season_schedule_totals

    team_season_schedule_averages = TeamSeasonScheduleAverages(points_for=Decimal('1'), points_against=Decimal('2'))
    test_service._team_season_schedule_repository.get_team_season_schedule_averages.return_value \
        = team_season_schedule_averages

    # Act
    test_service.run_weekly_update(league_name, season_year)

    # Assert
    test_service._league_season_totals_repository.get_league_season_totals.assert_any_call(league_name, season_year)
    test_service._league_season_repository.get_league_season_by_league_name_and_season_year.assert_has_calls([
        call(league_name, season_year),
        call(fake_team_season.league_name, fake_team_season.season_year)
    ])
    fake_league_season.update_games_and_points.assert_any_call(
        league_season_totals.total_games, league_season_totals.total_points
    )
    test_service._league_season_repository.update_league_season.assert_any_call(fake_league_season)
    test_service._game_repository.get_games.assert_called()
    test_service._season_repository.get_season_by_year.assert_any_call(season_year)
    assert season.num_of_weeks_completed == week_count
    test_service._season_repository.update_season.assert_any_call(season)
    test_service._team_season_repository.get_team_seasons_by_season_year.assert_any_call(season_year)
    test_service._team_season_schedule_repository.get_team_season_schedule_totals.assert_any_call(
        fake_team_season.team_name, fake_team_season.season_year
    )
    test_service._team_season_schedule_repository.get_team_season_schedule_averages.assert_any_call(
        fake_team_season.team_name, fake_team_season.season_year
    )
    fake_team_season.update_rankings.assert_any_call(
        team_season_schedule_averages.points_for,
        team_season_schedule_averages.points_against,
        league_season.average_points
    )
    test_service._team_season_repository.update_team_season.assert_any_call(fake_team_season)
