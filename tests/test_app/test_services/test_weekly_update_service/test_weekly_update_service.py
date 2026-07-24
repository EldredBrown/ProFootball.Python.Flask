from unittest.mock import MagicMock, call, patch

import pytest

from app.data.models.league_season import LeagueSeason
from app.data.models.league_season_totals import LeagueSeasonTotals
from app.data.models.season import Season
from app.data.models.team_season import TeamSeason

from app.services.weekly_update_service.weekly_update_service import WeeklyUpdateService


@pytest.fixture()
@patch('app.services.weekly_update_service.weekly_update_service.TeamSeasonRepository')
@patch('app.services.weekly_update_service.weekly_update_service.LeagueSeasonRepository')
@patch('app.services.weekly_update_service.weekly_update_service.GameRepository')
@patch('app.services.weekly_update_service.weekly_update_service.SeasonRepository')
def test_service(
        fake_season_repository, fake_game_repository, fake_league_season_repository, fake_team_season_repository
):
    test_service = WeeklyUpdateService(
        fake_season_repository,
        fake_game_repository,
        fake_league_season_repository,
        fake_team_season_repository
    )
    return test_service


def test_run_weekly_update_when_league_id_is_none_should_raise_value_error(test_service):
    # Arrange
    league_id = None

    # Act
    with pytest.raises(ValueError) as err:
        test_service.run_weekly_update(league_id, None)

    # Assert
    assert err.value.args[0] == "league_id"


@pytest.mark.parametrize("season_year", [-1, 0])
def test_run_weekly_update_when_league_id_is_not_none_and_season_year_less_than_zero_should_raise_value_error(
        season_year, test_service
):
    # Arrange
    league_id = 1

    # Act
    with pytest.raises(ValueError) as err:
        test_service.run_weekly_update(league_id, season_year)

    # Assert
    assert err.value.args[0] == f"season_year must be a positive integer; got {season_year}"


@pytest.mark.parametrize(
    "league_season_totals",
    [
        None,
        LeagueSeasonTotals(total_games=None),
        LeagueSeasonTotals(total_games=0, total_points=None),
    ]
)
@patch('app.services.weekly_update_service.weekly_update_service.season_rankings_repository')
@patch('app.services.weekly_update_service.weekly_update_service.league_season_totals_repository')
def test_run_weekly_update_when_season_year_greater_than_zero_and_src_week_count_is_none_should_not_update_anything(
        fake_league_season_totals_repository,
        fake_season_rankings_repository,
        league_season_totals,
        test_service
):
    # Arrange
    league_id = 1
    season_year = 1920

    fake_league_season_totals_repository.get_league_season_totals.return_value = league_season_totals

    fake_league_season = MagicMock(LeagueSeason)
    test_service.league_season_repository.get_league_season_by_league_and_season.return_value = None
    test_service.game_repository.get_max_week_by_season.return_value = None
    fake_team_season = MagicMock(TeamSeason)

    # Act
    test_service.run_weekly_update(league_id, season_year)

    # Assert
    fake_league_season_totals_repository.get_league_season_totals.assert_called_once_with(league_id, season_year)
    test_service.league_season_repository.get_league_season_by_league_and_season.assert_not_called()
    fake_league_season.update_games_and_points.assert_not_called()
    test_service.league_season_repository.update_league_season.assert_not_called()
    test_service.game_repository.get_max_week_by_season.assert_called_once_with(season_year)
    test_service.season_repository.get_season.assert_not_called()
    test_service.season_repository.update_season.assert_not_called()
    test_service.team_season_repository.get_team_seasons_by_season.assert_not_called()
    fake_season_rankings_repository.get_data_for_rankings_update.assert_not_called()
    fake_team_season.update_rankings.assert_not_called()
    test_service.team_season_repository.update_team_season.assert_not_called()


@patch('app.services.weekly_update_service.weekly_update_service.season_rankings_repository')
@patch('app.services.weekly_update_service.weekly_update_service.league_season_totals_repository')
def test_run_weekly_update_when_league_season_totals_total_points_is_not_none_and_league_season_is_none_and_src_week_count_is_none_should_not_update_anything(
        fake_league_season_totals_repository,
        fake_season_rankings_repository,
        test_service
):
    # Arrange
    league_id = 1
    season_year = 1920

    league_season_totals = LeagueSeasonTotals(total_games=0, total_points=0)
    fake_league_season_totals_repository.get_league_season_totals.return_value = league_season_totals

    fake_league_season = MagicMock(LeagueSeason)
    test_service.league_season_repository.get_league_season_by_league_and_season.return_value = None
    test_service.game_repository.get_max_week_by_season.return_value = None
    fake_team_season = MagicMock(TeamSeason)

    # Act
    test_service.run_weekly_update(league_id, season_year)

    # Assert
    fake_league_season_totals_repository.get_league_season_totals.assert_called_once_with(league_id, season_year)
    test_service.league_season_repository.get_league_season_by_league_and_season.assert_called_once_with(league_id, season_year)
    fake_league_season.update_games_and_points.assert_not_called()
    test_service.league_season_repository.update_league_season.assert_not_called()
    test_service.game_repository.get_max_week_by_season.assert_called_once_with(season_year)
    test_service.season_repository.get_season.assert_not_called()
    test_service.season_repository.update_season.assert_not_called()
    test_service.team_season_repository.get_team_seasons_by_season.assert_not_called()
    fake_season_rankings_repository.get_data_for_rankings_update.assert_not_called()
    fake_team_season.update_rankings.assert_not_called()
    test_service.team_season_repository.update_team_season.assert_not_called()


@patch('app.services.weekly_update_service.weekly_update_service.season_rankings_repository')
@patch('app.services.weekly_update_service.weekly_update_service.league_season_totals_repository')
def test_run_weekly_update_when_league_season_is_not_none_and_src_week_count_is_none_should_update_league_season_total_points_and_games(
        fake_league_season_totals_repository,
        fake_season_rankings_repository,
        test_service
):
    # Arrange
    league_id = 1
    season_year = 1920

    league_season_totals = LeagueSeasonTotals(total_games=0, total_points=0)
    fake_league_season_totals_repository.get_league_season_totals.return_value = league_season_totals

    fake_league_season = MagicMock(LeagueSeason)
    test_service.league_season_repository.get_league_season_by_league_and_season.return_value = fake_league_season
    test_service.game_repository.get_max_week_by_season.return_value = None
    fake_team_season = MagicMock(TeamSeason)

    # Act
    test_service.run_weekly_update(league_id, season_year)

    # Assert
    fake_league_season_totals_repository.get_league_season_totals.assert_called_once_with(league_id, season_year)
    test_service.league_season_repository.get_league_season_by_league_and_season.assert_called_once_with(league_id, season_year)
    fake_league_season.update_games_and_points.assert_called_once_with(league_season_totals.total_games, league_season_totals.total_points)
    test_service.league_season_repository.update_league_season.assert_called_once_with(fake_league_season)
    test_service.game_repository.get_max_week_by_season.assert_called_once_with(season_year)
    test_service.season_repository.get_season.assert_not_called()
    test_service.season_repository.update_season.assert_not_called()
    test_service.team_season_repository.get_team_seasons_by_season.assert_not_called()
    fake_season_rankings_repository.get_data_for_rankings_update.assert_not_called()
    fake_team_season.update_rankings.assert_not_called()
    test_service.team_season_repository.update_team_season.assert_not_called()


@patch('app.services.weekly_update_service.weekly_update_service.season_rankings_repository')
@patch('app.services.weekly_update_service.weekly_update_service.league_season_totals_repository')
def test_run_weekly_update_when_src_week_count_is_none_should_not_update_week_count(
        fake_league_season_totals_repository,
        fake_season_rankings_repository,
        test_service
):
    # Arrange
    league_id = 1
    season_year = 1920

    league_season_totals = LeagueSeasonTotals(total_games=0, total_points=0)
    fake_league_season_totals_repository.get_league_season_totals.return_value = league_season_totals

    fake_league_season = MagicMock(LeagueSeason)
    test_service.league_season_repository.get_league_season_by_league_and_season.return_value = fake_league_season
    test_service.game_repository.get_max_week_by_season.return_value = None
    fake_team_season = MagicMock(TeamSeason)

    # Act
    test_service.run_weekly_update(league_id, season_year)

    # Assert
    fake_league_season_totals_repository.get_league_season_totals.assert_called_once_with(league_id, season_year)
    test_service.league_season_repository.get_league_season_by_league_and_season.assert_called_once_with(league_id, season_year)
    fake_league_season.update_games_and_points.assert_called_once_with(league_season_totals.total_games, league_season_totals.total_points)
    test_service.league_season_repository.update_league_season.assert_called_once_with(fake_league_season)
    test_service.game_repository.get_max_week_by_season.assert_called_once_with(season_year)
    test_service.season_repository.get_season.assert_not_called()
    test_service.season_repository.update_season.assert_not_called()
    test_service.team_season_repository.get_team_seasons_by_season.assert_not_called()
    fake_season_rankings_repository.get_data_for_rankings_update.assert_not_called()
    fake_team_season.update_rankings.assert_not_called()
    test_service.team_season_repository.update_team_season.assert_not_called()


@patch('app.services.weekly_update_service.weekly_update_service.season_rankings_repository')
@patch('app.services.weekly_update_service.weekly_update_service.league_season_totals_repository')
def test_run_weekly_update_when_src_week_count_is_zero_and_dest_season_is_none_should_not_update_week_count(
        fake_league_season_totals_repository,
        fake_season_rankings_repository,
        test_service
):
    # Arrange
    league_id = 1
    season_year = 1920

    league_season_totals = LeagueSeasonTotals(total_games=0, total_points=0)
    fake_league_season_totals_repository.get_league_season_totals.return_value = league_season_totals

    fake_league_season = MagicMock(LeagueSeason)
    test_service.league_season_repository.get_league_season_by_league_and_season.return_value = fake_league_season
    test_service.game_repository.get_max_week_by_season.return_value = 0

    test_service.season_repository.get_season.return_value = None

    fake_team_season = MagicMock(TeamSeason)

    # Act
    test_service.run_weekly_update(league_id, season_year)

    # Assert
    fake_league_season_totals_repository.get_league_season_totals.assert_called_once_with(league_id, season_year)
    test_service.league_season_repository.get_league_season_by_league_and_season.assert_called_once_with(league_id, season_year)
    fake_league_season.update_games_and_points.assert_called_once_with(league_season_totals.total_games, league_season_totals.total_points)
    test_service.league_season_repository.update_league_season.assert_called_once_with(fake_league_season)
    test_service.game_repository.get_max_week_by_season.assert_called_once_with(season_year)
    test_service.season_repository.get_season.assert_called_once_with(season_year)
    test_service.season_repository.update_season.assert_not_called()
    test_service.team_season_repository.get_team_seasons_by_season.assert_not_called()
    fake_season_rankings_repository.get_data_for_rankings_update.assert_not_called()
    fake_team_season.update_rankings.assert_not_called()
    test_service.team_season_repository.update_team_season.assert_not_called()


@pytest.mark.parametrize("week_count", [0, 2])
@patch('app.services.weekly_update_service.weekly_update_service.season_rankings_repository')
@patch('app.services.weekly_update_service.weekly_update_service.league_season_totals_repository')
def test_run_weekly_update_when_dest_season_is_not_none_and_week_count_is_less_than_three_should_update_week_count(
        fake_league_season_totals_repository,
        fake_season_rankings_repository,
        week_count,
        test_service
):
    # Arrange
    league_id = 1
    season_year = 1920

    league_season_totals = LeagueSeasonTotals(total_games=0, total_points=0)
    fake_league_season_totals_repository.get_league_season_totals.return_value = league_season_totals

    fake_league_season = MagicMock(LeagueSeason)
    test_service.league_season_repository.get_league_season_by_league_and_season.return_value = fake_league_season
    test_service.game_repository.get_max_week_by_season.return_value = week_count

    dest_season = MagicMock(Season)
    test_service.season_repository.get_season.return_value = dest_season

    fake_team_season = MagicMock(TeamSeason)

    # Act
    test_service.run_weekly_update(league_id, season_year)

    # Assert
    fake_league_season_totals_repository.get_league_season_totals.assert_called_once_with(league_id, season_year)
    test_service.league_season_repository.get_league_season_by_league_and_season.assert_called_once_with(league_id, season_year)
    fake_league_season.update_games_and_points.assert_called_once_with(league_season_totals.total_games, league_season_totals.total_points)
    test_service.league_season_repository.update_league_season.assert_called_once_with(fake_league_season)
    test_service.game_repository.get_max_week_by_season.assert_called_once_with(season_year)
    test_service.season_repository.get_season.assert_called_once_with(season_year)
    test_service.season_repository.update_season.assert_called_once_with(dest_season)
    test_service.team_season_repository.get_team_seasons_by_season.assert_not_called()
    fake_season_rankings_repository.get_data_for_rankings_update.assert_not_called()
    fake_team_season.update_rankings.assert_not_called()
    test_service.team_season_repository.update_team_season.assert_not_called()


@pytest.mark.parametrize(
    ("week_count", "team_seasons"),
    [
        (3, None),
        (4, None),
        (4, []),
    ]
)
@patch('app.services.weekly_update_service.weekly_update_service.season_rankings_repository')
@patch('app.services.weekly_update_service.weekly_update_service.league_season_totals_repository')
def test_run_weekly_update_when_week_count_is_three_and_team_seasons_for_specified_year_is_none_should_not_update_rankings_for_any_team_season(
        fake_league_season_totals_repository,
        fake_season_rankings_repository,
        week_count, team_seasons,
        test_service
):
    # Arrange
    league_id = 1
    season_year = 1920

    league_season_totals = LeagueSeasonTotals(total_games=0, total_points=0)
    fake_league_season_totals_repository.get_league_season_totals.return_value = league_season_totals

    fake_league_season = MagicMock(LeagueSeason)
    test_service.league_season_repository.get_league_season_by_league_and_season.return_value = fake_league_season
    test_service.game_repository.get_max_week_by_season.return_value = week_count

    dest_season = MagicMock(Season)
    test_service.season_repository.get_season.return_value = dest_season

    test_service.team_season_repository.get_team_seasons_by_season.return_value = team_seasons

    fake_team_season = MagicMock(TeamSeason)

    # Act
    test_service.run_weekly_update(league_id, season_year)

    # Assert
    fake_league_season_totals_repository.get_league_season_totals.assert_called_once_with(league_id, season_year)
    test_service.league_season_repository.get_league_season_by_league_and_season.assert_called_once_with(league_id, season_year)
    fake_league_season.update_games_and_points.assert_called_once_with(league_season_totals.total_games, league_season_totals.total_points)
    test_service.league_season_repository.update_league_season.assert_called_once_with(fake_league_season)
    test_service.game_repository.get_max_week_by_season.assert_called_once_with(season_year)
    test_service.season_repository.get_season.assert_called_once_with(season_year)
    test_service.season_repository.update_season.assert_called_once_with(dest_season)
    test_service.team_season_repository.get_team_seasons_by_season.assert_called_once_with(season_year)
    fake_season_rankings_repository.get_data_for_rankings_update.assert_not_called()
    fake_team_season.update_rankings.assert_not_called()
    test_service.team_season_repository.update_team_season.assert_not_called()


@pytest.mark.parametrize(
    ("team_season_schedule_totals", "team_season_schedule_averages", "league_season"),
    [
        (None, None, None),
        (dict(), None, None),
        ({'schedule_games': None}, None, None),
        ({'schedule_games': None}, dict(), None),
        ({'schedule_games': None}, {'avg_points_for': None, 'avg_points_against': None}, None),
        ({'schedule_games': None}, {'avg_points_for': 0, 'avg_points_against': None}, None),
        ({'schedule_games': None}, {'avg_points_for': 0, 'avg_points_against': 0}, None),
        ({'schedule_games': None}, {'avg_points_for': 0, 'avg_points_against': 0}, dict()),
        ({'schedule_games': None}, {'avg_points_for': 0, 'avg_points_against': 0}, {'average_points': None}),
    ]
)
@patch('app.services.weekly_update_service.weekly_update_service.season_rankings_repository')
@patch('app.services.weekly_update_service.weekly_update_service.league_season_totals_repository')
def test_run_weekly_update_when_team_seasons_for_specified_year_is_not_empty_and_team_season_schedule_totals_is_none_should_not_update_rankings_for_any_team_season(
        fake_league_season_totals_repository,
        fake_season_rankings_repository,
        team_season_schedule_totals, team_season_schedule_averages,
        league_season,
        test_service
):
    # Arrange
    league_id = 1
    season_year = 1920

    league_season_totals = LeagueSeasonTotals(total_games=0, total_points=0)
    fake_league_season_totals_repository.get_league_season_totals.return_value = league_season_totals

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

    fake_season_rankings_repository.get_data_for_rankings_update.return_value = \
        {
            'team_season_schedule_totals': team_season_schedule_totals,
            'team_season_schedule_averages': team_season_schedule_averages,
            'league_season': league_season
        }

    # Act
    test_service.run_weekly_update(league_id, season_year)

    # Assert
    fake_league_season_totals_repository.get_league_season_totals.assert_called_once_with(league_id, season_year)
    test_service.league_season_repository.get_league_season_by_league_and_season.assert_called_once_with(league_id, season_year)
    fake_league_season.update_games_and_points.assert_called_once_with(league_season_totals.total_games, league_season_totals.total_points)
    test_service.league_season_repository.update_league_season.assert_called_once_with(fake_league_season)
    test_service.game_repository.get_max_week_by_season.assert_called_once_with(season_year)
    test_service.season_repository.get_season.assert_called_once_with(season_year)
    test_service.season_repository.update_season.assert_called_once_with(dest_season)
    test_service.team_season_repository.get_team_seasons_by_season.assert_called_once_with(season_year)
    fake_season_rankings_repository.get_data_for_rankings_update.assert_called_once_with(fake_team_season)
    fake_team_season.update_rankings.assert_not_called()
    test_service.team_season_repository.update_team_season.assert_not_called()


@patch('app.services.weekly_update_service.weekly_update_service.season_rankings_repository')
@patch('app.services.weekly_update_service.weekly_update_service.league_season_totals_repository')
def test_run_weekly_update_when_team_season_schedule_totals_and_averages_and_league_season_are_good_should_update_rankings_for_team_season(
        fake_league_season_totals_repository,
        fake_season_rankings_repository,
        test_service
):
    # Arrange
    league_id = 1
    season_year = 1920

    league_season_totals = LeagueSeasonTotals(total_games=0, total_points=0)
    fake_league_season_totals_repository.get_league_season_totals.return_value = league_season_totals

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
    fake_season_rankings_repository.get_data_for_rankings_update.return_value = rankings_data

    # Act
    test_service.run_weekly_update(league_id, season_year)

    # Assert
    fake_league_season_totals_repository.get_league_season_totals.assert_called_once_with(league_id, season_year)
    test_service.league_season_repository.get_league_season_by_league_and_season.assert_called_once_with(league_id, season_year)
    fake_league_season.update_games_and_points.assert_called_once_with(league_season_totals.total_games, league_season_totals.total_points)
    test_service.league_season_repository.update_league_season.assert_called_once_with(fake_league_season)
    test_service.game_repository.get_max_week_by_season.assert_called_once_with(season_year)
    test_service.season_repository.get_season.assert_called_once_with(season_year)
    test_service.season_repository.update_season.assert_called_once_with(dest_season)
    test_service.team_season_repository.get_team_seasons_by_season.assert_called_once_with(season_year)
    fake_season_rankings_repository.get_data_for_rankings_update.assert_called_once_with(fake_team_season)
    fake_team_season.update_rankings.assert_called_once_with(
        rankings_data['team_season_schedule_averages']['avg_points_for'],
        rankings_data['team_season_schedule_averages']['avg_points_against'],
        rankings_data['league_season']['average_points']
    )
    test_service.team_season_repository.update_team_season.assert_called_once_with(fake_team_season)


@patch('app.services.weekly_update_service.weekly_update_service.season_rankings_repository')
@patch('app.services.weekly_update_service.weekly_update_service.league_season_totals_repository')
def test_run_weekly_update_when_more_than_one_good_team_season_should_update_rankings_for_all_team_seasons(
        fake_league_season_totals_repository,
        fake_season_rankings_repository,
        test_service
):
    # Arrange
    league_id = 1
    season_year = 1920

    league_season_totals = LeagueSeasonTotals(total_games=0, total_points=0)
    fake_league_season_totals_repository.get_league_season_totals.return_value = league_season_totals

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
    fake_season_rankings_repository.get_data_for_rankings_update.return_value = rankings_data

    # Act
    test_service.run_weekly_update(league_id, season_year)

    # Assert
    fake_league_season_totals_repository.get_league_season_totals.assert_called_once_with(league_id, season_year)
    test_service.league_season_repository.get_league_season_by_league_and_season.assert_called_once_with(league_id, season_year)
    fake_league_season.update_games_and_points.assert_called_once_with(league_season_totals.total_games, league_season_totals.total_points)
    test_service.league_season_repository.update_league_season.assert_called_once_with(fake_league_season)
    test_service.game_repository.get_max_week_by_season.assert_called_once_with(season_year)
    test_service.season_repository.get_season.assert_called_once_with(season_year)
    test_service.season_repository.update_season.assert_called_once_with(dest_season)
    test_service.team_season_repository.get_team_seasons_by_season.assert_called_once_with(season_year)
    fake_season_rankings_repository.get_data_for_rankings_update.assert_has_calls([
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
