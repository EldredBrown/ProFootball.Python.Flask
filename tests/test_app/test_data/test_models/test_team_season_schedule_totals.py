from decimal import Decimal

import pytest

from app.data.models.team_season_schedule_totals import TeamSeasonScheduleTotals


@pytest.fixture
def test_team_season_schedule_totals() -> TeamSeasonScheduleTotals:
    return TeamSeasonScheduleTotals()


def test_string(test_team_season_schedule_totals):
    # Assert
    assert str(test_team_season_schedule_totals) == \
           f"G: {test_team_season_schedule_totals.games}, " \
           f"PF: {test_team_season_schedule_totals.points_for}, " \
           f"PA: {test_team_season_schedule_totals.points_against}, " \
           f"SW: {test_team_season_schedule_totals.schedule_wins}, " \
           f"SL: {test_team_season_schedule_totals.schedule_losses}, " \
           f"ST: {test_team_season_schedule_totals.schedule_ties}, " \
           f"SWP: {test_team_season_schedule_totals.schedule_winning_percentage}, " \
           f"SG: {test_team_season_schedule_totals.schedule_games}, " \
           f"SPF: {test_team_season_schedule_totals.schedule_points_for}, " \
           f"SPA: {test_team_season_schedule_totals.schedule_points_against}"


def test_games_getter_can_return_none(test_team_season_schedule_totals):
    # Arrange
    test_team_season_schedule_totals._games = None

    # Assert
    assert test_team_season_schedule_totals.games is None


def test_games_getter_can_return_int(test_team_season_schedule_totals):
    # Arrange
    test_team_season_schedule_totals._games = 1

    # Assert
    assert test_team_season_schedule_totals.games == 1


def test_games_setter_when_value_is_none_should_set_games(test_team_season_schedule_totals):
    # Act
    test_team_season_schedule_totals.games = None

    # Assert
    assert test_team_season_schedule_totals._games is None


def test_games_setter_when_value_is_negative_should_raise_value_error(test_team_season_schedule_totals):
    # Act & Assert
    with pytest.raises(ValueError, match="Please enter a non-negative value for games."):
        test_team_season_schedule_totals.games = -1


def test_games_setter_when_value_is_positive_should_set_games(test_team_season_schedule_totals):
    # Act
    test_team_season_schedule_totals.games = 1

    # Assert
    assert test_team_season_schedule_totals._games == 1


def test_games_setter_when_value_is_zero_should_set_games(test_team_season_schedule_totals):
    # Act
    test_team_season_schedule_totals.games = 0

    # Assert
    assert test_team_season_schedule_totals._games == 0


def test_points_for_getter_can_return_none(test_team_season_schedule_totals):
    # Arrange
    test_team_season_schedule_totals._points_for = None

    # Assert
    assert test_team_season_schedule_totals.points_for is None


def test_points_for_getter_can_return_int(test_team_season_schedule_totals):
    # Arrange
    test_team_season_schedule_totals._points_for = 1

    # Assert
    assert test_team_season_schedule_totals.points_for == 1


def test_points_for_setter_when_value_is_none_should_set_points_for(test_team_season_schedule_totals):
    # Act
    test_team_season_schedule_totals.points_for = None

    # Assert
    assert test_team_season_schedule_totals._points_for is None


def test_points_for_setter_when_value_is_negative_should_raise_value_error(test_team_season_schedule_totals):
    # Act & Assert
    with pytest.raises(ValueError, match="Please enter a non-negative value for points for."):
        test_team_season_schedule_totals.points_for = -1


def test_points_for_setter_when_value_is_positive_should_set_points_for(test_team_season_schedule_totals):
    # Act
    test_team_season_schedule_totals.points_for = 1

    # Assert
    assert test_team_season_schedule_totals._points_for == 1


def test_points_for_setter_when_value_is_zero_should_set_points_for(test_team_season_schedule_totals):
    # Act
    test_team_season_schedule_totals.points_for = 0

    # Assert
    assert test_team_season_schedule_totals._points_for == 0


def test_points_against_getter_can_return_none(test_team_season_schedule_totals):
    # Arrange
    test_team_season_schedule_totals._points_against = None

    # Assert
    assert test_team_season_schedule_totals.points_against is None


def test_points_against_getter_can_return_int(test_team_season_schedule_totals):
    # Arrange
    test_team_season_schedule_totals._points_against = 1

    # Assert
    assert test_team_season_schedule_totals.points_against == 1


def test_points_against_setter_when_value_is_none_should_set_points_against(test_team_season_schedule_totals):
    # Act
    test_team_season_schedule_totals.points_against = None

    # Assert
    assert test_team_season_schedule_totals._points_against is None


def test_points_against_setter_when_value_is_negative_should_raise_value_error(test_team_season_schedule_totals):
    # Act & Assert
    with pytest.raises(ValueError, match="Please enter a non-negative value for points against."):
        test_team_season_schedule_totals.points_against = -1


def test_points_against_setter_when_value_is_positive_should_set_points_against(test_team_season_schedule_totals):
    # Act
    test_team_season_schedule_totals.points_against = 1

    # Assert
    assert test_team_season_schedule_totals._points_against == 1


def test_points_against_setter_when_value_is_zero_should_set_points_against(test_team_season_schedule_totals):
    # Act
    test_team_season_schedule_totals.points_against = 0

    # Assert
    assert test_team_season_schedule_totals._points_against == 0


def test_schedule_wins_getter_can_return_none(test_team_season_schedule_totals):
    # Arrange
    test_team_season_schedule_totals._schedule_wins = None

    # Assert
    assert test_team_season_schedule_totals.schedule_wins is None


def test_schedule_wins_getter_can_return_int(test_team_season_schedule_totals):
    # Arrange
    test_team_season_schedule_totals._schedule_wins = 1

    # Assert
    assert test_team_season_schedule_totals.schedule_wins == 1


def test_schedule_wins_setter_when_value_is_none_should_set_schedule_wins(test_team_season_schedule_totals):
    # Act
    test_team_season_schedule_totals.schedule_wins = None

    # Assert
    assert test_team_season_schedule_totals._schedule_wins is None


def test_schedule_wins_setter_when_value_is_negative_should_raise_value_error(test_team_season_schedule_totals):
    # Act & Assert
    with pytest.raises(ValueError, match="Please enter a non-negative value for schedule wins."):
        test_team_season_schedule_totals.schedule_wins = -1


def test_schedule_wins_setter_when_value_is_positive_should_set_schedule_wins(test_team_season_schedule_totals):
    # Act
    test_team_season_schedule_totals.schedule_wins = 1

    # Assert
    assert test_team_season_schedule_totals._schedule_wins == 1


def test_schedule_wins_setter_when_value_is_zero_should_set_schedule_wins(test_team_season_schedule_totals):
    # Act
    test_team_season_schedule_totals.schedule_wins = 0

    # Assert
    assert test_team_season_schedule_totals._schedule_wins == 0


def test_schedule_losses_getter_can_return_none(test_team_season_schedule_totals):
    # Arrange
    test_team_season_schedule_totals._schedule_losses = None

    # Assert
    assert test_team_season_schedule_totals.schedule_losses is None


def test_schedule_losses_getter_can_return_int(test_team_season_schedule_totals):
    # Arrange
    test_team_season_schedule_totals._schedule_losses = 1

    # Assert
    assert test_team_season_schedule_totals.schedule_losses == 1


def test_schedule_losses_setter_when_value_is_none_should_set_schedule_losses(test_team_season_schedule_totals):
    # Act
    test_team_season_schedule_totals.schedule_losses = None

    # Assert
    assert test_team_season_schedule_totals._schedule_losses is None


def test_schedule_losses_setter_when_value_is_negative_should_raise_value_error(test_team_season_schedule_totals):
    # Act & Assert
    with pytest.raises(ValueError, match="Please enter a non-negative value for schedule losses."):
        test_team_season_schedule_totals.schedule_losses = -1


def test_schedule_losses_setter_when_value_is_positive_should_set_schedule_losses(test_team_season_schedule_totals):
    # Act
    test_team_season_schedule_totals.schedule_losses = 1

    # Assert
    assert test_team_season_schedule_totals._schedule_losses == 1


def test_schedule_losses_setter_when_value_is_zero_should_set_schedule_losses(test_team_season_schedule_totals):
    # Act
    test_team_season_schedule_totals.schedule_losses = 0

    # Assert
    assert test_team_season_schedule_totals._schedule_losses == 0


def test_schedule_ties_getter_can_return_none(test_team_season_schedule_totals):
    # Arrange
    test_team_season_schedule_totals._schedule_ties = None

    # Assert
    assert test_team_season_schedule_totals.schedule_ties is None


def test_schedule_ties_getter_can_return_int(test_team_season_schedule_totals):
    # Arrange
    test_team_season_schedule_totals._schedule_ties = 1

    # Assert
    assert test_team_season_schedule_totals.schedule_ties == 1


def test_schedule_ties_setter_when_value_is_none_should_set_schedule_ties(test_team_season_schedule_totals):
    # Act
    test_team_season_schedule_totals.schedule_ties = None

    # Assert
    assert test_team_season_schedule_totals._schedule_ties is None


def test_schedule_ties_setter_when_value_is_negative_should_raise_value_error(test_team_season_schedule_totals):
    # Act & Assert
    with pytest.raises(ValueError, match="Please enter a non-negative value for schedule ties."):
        test_team_season_schedule_totals.schedule_ties = -1


def test_schedule_ties_setter_when_value_is_positive_should_set_schedule_ties(test_team_season_schedule_totals):
    # Act
    test_team_season_schedule_totals.schedule_ties = 1

    # Assert
    assert test_team_season_schedule_totals._schedule_ties == 1


def test_schedule_ties_setter_when_value_is_zero_should_set_schedule_ties(test_team_season_schedule_totals):
    # Act
    test_team_season_schedule_totals.schedule_ties = 0

    # Assert
    assert test_team_season_schedule_totals._schedule_ties == 0


def test_schedule_winning_percentage_getter_can_return_none(test_team_season_schedule_totals):
    # Arrange
    test_team_season_schedule_totals._schedule_winning_percentage = None

    # Assert
    assert test_team_season_schedule_totals.schedule_winning_percentage is None


def test_schedule_winning_percentage_getter_can_return_float(test_team_season_schedule_totals):
    # Arrange
    test_team_season_schedule_totals._schedule_winning_percentage = 1.000

    # Assert
    assert test_team_season_schedule_totals.schedule_winning_percentage == 1.000


def test_schedule_winning_percentage_setter_when_value_is_none_should_set_schedule_winning_percentage(
        test_team_season_schedule_totals
):
    # Act
    test_team_season_schedule_totals.schedule_winning_percentage = None

    # Assert
    assert test_team_season_schedule_totals._schedule_winning_percentage is None


def test_schedule_winning_percentage_setter_when_value_is_negative_should_raise_value_error(
        test_team_season_schedule_totals
):
    # Act & Assert
    with pytest.raises(ValueError, match="Please enter a non-negative value for schedule winning percentage."):
        test_team_season_schedule_totals.schedule_winning_percentage = -1.000


def test_schedule_winning_percentage_setter_when_value_is_positive_should_set_schedule_winning_percentage(
        test_team_season_schedule_totals
):
    # Act
    test_team_season_schedule_totals.schedule_winning_percentage = 1.000

    # Assert
    assert test_team_season_schedule_totals._schedule_winning_percentage == 1.000


def test_schedule_winning_percentage_setter_when_value_is_zero_should_set_schedule_winning_percentage(
        test_team_season_schedule_totals):
    # Act
    test_team_season_schedule_totals.schedule_winning_percentage = 0.000

    # Assert
    assert test_team_season_schedule_totals._schedule_winning_percentage == 0.000


def test_schedule_games_getter_can_return_none(test_team_season_schedule_totals):
    # Arrange
    test_team_season_schedule_totals._schedule_games = None

    # Assert
    assert test_team_season_schedule_totals.schedule_games is None


def test_schedule_games_getter_can_return_decimal(test_team_season_schedule_totals):
    # Arrange
    test_team_season_schedule_totals._schedule_games = Decimal('1')

    # Assert
    assert test_team_season_schedule_totals.schedule_games == Decimal('1')


def test_schedule_games_setter_when_value_is_none_should_set_schedule_games(test_team_season_schedule_totals):
    # Act
    test_team_season_schedule_totals.schedule_games = None

    # Assert
    assert test_team_season_schedule_totals._schedule_games is None


def test_schedule_games_setter_when_value_is_negative_should_raise_value_error(test_team_season_schedule_totals):
    # Act & Assert
    with pytest.raises(ValueError, match="Please enter a non-negative value for schedule games."):
        test_team_season_schedule_totals.schedule_games = Decimal('-1')


def test_schedule_games_setter_when_value_is_positive_should_set_schedule_games(test_team_season_schedule_totals):
    # Act
    test_team_season_schedule_totals.schedule_games = 1

    # Assert
    assert test_team_season_schedule_totals._schedule_games == 1


def test_schedule_games_setter_when_value_is_zero_should_set_schedule_games(test_team_season_schedule_totals):
    # Act
    test_team_season_schedule_totals.schedule_games = 0

    # Assert
    assert test_team_season_schedule_totals._schedule_games == 0


def test_schedule_points_for_getter_can_return_none(test_team_season_schedule_totals):
    # Arrange
    test_team_season_schedule_totals._schedule_points_for = None

    # Assert
    assert test_team_season_schedule_totals.schedule_points_for is None


def test_schedule_points_for_getter_can_return_int(test_team_season_schedule_totals):
    # Arrange
    test_team_season_schedule_totals._schedule_points_for = 1

    # Assert
    assert test_team_season_schedule_totals.schedule_points_for == 1


def test_schedule_points_for_setter_when_value_is_none_should_set_schedule_points_for(test_team_season_schedule_totals):
    # Act
    test_team_season_schedule_totals.schedule_points_for = None

    # Assert
    assert test_team_season_schedule_totals._schedule_points_for is None


def test_schedule_points_for_setter_when_value_is_negative_should_raise_value_error(test_team_season_schedule_totals):
    # Act & Assert
    with pytest.raises(ValueError, match="Please enter a non-negative value for schedule points for."):
        test_team_season_schedule_totals.schedule_points_for = -1


def test_schedule_points_for_setter_when_value_is_positive_should_set_schedule_points_for(
        test_team_season_schedule_totals):
    # Act
    test_team_season_schedule_totals.schedule_points_for = 1

    # Assert
    assert test_team_season_schedule_totals._schedule_points_for == 1


def test_schedule_points_for_setter_when_value_is_zero_should_set_schedule_points_for(test_team_season_schedule_totals):
    # Act
    test_team_season_schedule_totals.schedule_points_for = 0

    # Assert
    assert test_team_season_schedule_totals._schedule_points_for == 0


def test_schedule_points_against_getter_can_return_none(test_team_season_schedule_totals):
    # Arrange
    test_team_season_schedule_totals._schedule_points_against = None

    # Assert
    assert test_team_season_schedule_totals.schedule_points_against is None


def test_schedule_points_against_getter_can_return_int(test_team_season_schedule_totals):
    # Arrange
    test_team_season_schedule_totals._schedule_points_against = 1

    # Assert
    assert test_team_season_schedule_totals.schedule_points_against == 1


def test_schedule_points_against_setter_when_value_is_none_should_set_schedule_points_against(
        test_team_season_schedule_totals
):
    # Act
    test_team_season_schedule_totals.schedule_points_against = None

    # Assert
    assert test_team_season_schedule_totals._schedule_points_against is None


def test_schedule_points_against_setter_when_value_is_negative_should_raise_value_error(
        test_team_season_schedule_totals):
    # Act & Assert
    with pytest.raises(ValueError, match="Please enter a non-negative value for schedule points against."):
        test_team_season_schedule_totals.schedule_points_against = -1


def test_schedule_points_against_setter_when_value_is_positive_should_set_schedule_points_against(
        test_team_season_schedule_totals):
    # Act
    test_team_season_schedule_totals.schedule_points_against = 1

    # Assert
    assert test_team_season_schedule_totals._schedule_points_against == 1


def test_schedule_points_against_setter_when_value_is_zero_should_set_schedule_points_against(
        test_team_season_schedule_totals):
    # Act
    test_team_season_schedule_totals.schedule_points_against = 0

    # Assert
    assert test_team_season_schedule_totals._schedule_points_against == 0
