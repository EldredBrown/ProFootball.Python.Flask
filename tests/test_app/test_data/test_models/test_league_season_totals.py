import pytest

from app.data.models.league_season_totals import LeagueSeasonTotals


@pytest.fixture
def test_league_season_totals() -> LeagueSeasonTotals:
    return LeagueSeasonTotals()


def test_string(test_league_season_totals):
    # Assert
    assert str(test_league_season_totals) == f"Total Games: {test_league_season_totals.total_games}, " \
                                             f"Total Points: {test_league_season_totals.total_points}"


def test_total_games_getter_can_return_none(test_league_season_totals):
    # Arrange
    test_league_season_totals._total_games = None

    # Assert
    assert test_league_season_totals.total_games is None


def test_total_games_getter_can_return_int(test_league_season_totals):
    # Arrange
    test_league_season_totals._total_games = 1

    # Assert
    assert test_league_season_totals.total_games == 1


def test_total_games_setter_should_set_total_games_when_value_is_none(test_league_season_totals):
    # Act
    test_league_season_totals.total_games = None

    # Assert
    assert test_league_season_totals._total_games is None


def test_total_games_setter_should_raise_value_error_when_value_is_negative(test_league_season_totals):
    # Act & Assert
    with pytest.raises(ValueError, match="Please enter a non-negative value for total games."):
        test_league_season_totals.total_games = -1


def test_total_games_setter_should_set_total_games_when_value_is_positive(test_league_season_totals):
    # Act
    test_league_season_totals.total_games = 1

    # Assert
    assert test_league_season_totals._total_games == 1


def test_total_games_setter_should_set_total_games_when_value_is_zero(test_league_season_totals):
    # Act
    test_league_season_totals.total_games = 1
    test_league_season_totals.total_games = 0

    # Assert
    assert test_league_season_totals._total_games == 0


def test_total_points_getter_can_return_none(test_league_season_totals):
    # Arrange
    test_league_season_totals._total_points = None

    # Assert
    assert test_league_season_totals.total_points is None


def test_total_points_getter_can_return_int(test_league_season_totals):
    # Arrange
    test_league_season_totals._total_points = 1

    # Assert
    assert test_league_season_totals.total_points == 1


def test_total_points_setter_should_set_total_points_when_value_is_none(test_league_season_totals):
    # Act
    test_league_season_totals.total_points = None

    # Assert
    assert test_league_season_totals._total_points is None


def test_total_points_setter_should_raise_value_error_when_value_is_negative(test_league_season_totals):
    # Act & Assert
    with pytest.raises(ValueError, match="Please enter a non-negative value for total points."):
        test_league_season_totals.total_points = -1


def test_total_points_setter_should_set_total_points_when_value_is_positive(test_league_season_totals):
    # Act
    test_league_season_totals.total_points = 1

    # Assert
    assert test_league_season_totals._total_points == 1


def test_total_points_setter_should_set_total_points_when_value_is_zero(test_league_season_totals):
    # Act
    test_league_season_totals.total_points = 1
    test_league_season_totals.total_points = 0

    # Assert
    assert test_league_season_totals._total_points == 0
