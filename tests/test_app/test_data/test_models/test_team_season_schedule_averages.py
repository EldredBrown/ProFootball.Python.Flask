from decimal import Decimal

import pytest

from app.data.models.team_season_schedule_averages import TeamSeasonScheduleAverages


@pytest.fixture
def test_team_season_schedule_averages() -> TeamSeasonScheduleAverages:
    return TeamSeasonScheduleAverages()


def test_string(test_team_season_schedule_averages):
    # Assert
    assert str(test_team_season_schedule_averages) == \
           f"PF: {test_team_season_schedule_averages.points_for}, " \
           f"PA: {test_team_season_schedule_averages.points_against}, " \
           f"SPF: {test_team_season_schedule_averages.schedule_points_for}, " \
           f"SPA: {test_team_season_schedule_averages.schedule_points_against}"


def test_points_for_getter_can_return_none(test_team_season_schedule_averages):
    # Arrange
    test_team_season_schedule_averages._points_for = None

    # Assert
    assert test_team_season_schedule_averages.points_for is None


def test_points_for_getter_can_return_float(test_team_season_schedule_averages):
    # Arrange
    test_team_season_schedule_averages._points_for = 1.00

    # Assert
    assert test_team_season_schedule_averages.points_for == 1.00


def test_points_for_setter_when_value_is_none_should_set_points_for(test_team_season_schedule_averages):
    # Act
    test_team_season_schedule_averages.points_for = None

    # Assert
    assert test_team_season_schedule_averages._points_for is None


def test_points_for_setter_when_value_is_negative_should_raise_value_error(test_team_season_schedule_averages):
    # Act & Assert
    with pytest.raises(ValueError, match="Please enter a non-negative value for points for."):
        test_team_season_schedule_averages.points_for = -1.00


def test_points_for_setter_when_value_is_positive_should_set_points_for(test_team_season_schedule_averages):
    # Act
    test_team_season_schedule_averages.points_for = 1.00

    # Assert
    assert test_team_season_schedule_averages._points_for == 1.00


def test_points_for_setter_when_value_is_zero_should_set_points_for(test_team_season_schedule_averages):
    # Act
    test_team_season_schedule_averages.points_for = 1.00
    test_team_season_schedule_averages.points_for = 0

    # Assert
    assert test_team_season_schedule_averages._points_for == 0


def test_points_against_getter_can_return_none(test_team_season_schedule_averages):
    # Arrange
    test_team_season_schedule_averages._points_against = None

    # Assert
    assert test_team_season_schedule_averages.points_against is None


def test_points_against_getter_can_return_float(test_team_season_schedule_averages):
    # Arrange
    test_team_season_schedule_averages._points_against = 1.00

    # Assert
    assert test_team_season_schedule_averages.points_against == 1.00


def test_points_against_setter_when_value_is_none_should_set_points_against(test_team_season_schedule_averages):
    # Act
    test_team_season_schedule_averages.points_against = None

    # Assert
    assert test_team_season_schedule_averages._points_against is None


def test_points_against_setter_when_value_is_negative_should_raise_value_error(test_team_season_schedule_averages):
    # Act & Assert
    with pytest.raises(ValueError, match="Please enter a non-negative value for points against."):
        test_team_season_schedule_averages.points_against = -1.00


def test_points_against_setter_when_value_is_positive_should_set_points_against(test_team_season_schedule_averages):
    # Act
    test_team_season_schedule_averages.points_against = 1.00

    # Assert
    assert test_team_season_schedule_averages._points_against == Decimal('1.00')


def test_points_against_setter_when_value_is_zero_should_set_points_against(test_team_season_schedule_averages):
    # Act
    test_team_season_schedule_averages.points_against = 1.00
    test_team_season_schedule_averages.points_against = 0

    # Assert
    assert test_team_season_schedule_averages._points_against == 0


def test_schedule_points_for_getter_can_return_none(test_team_season_schedule_averages):
    # Arrange
    test_team_season_schedule_averages._schedule_points_for = None

    # Assert
    assert test_team_season_schedule_averages.schedule_points_for is None


def test_schedule_points_for_getter_can_return_float(test_team_season_schedule_averages):
    # Arrange
    test_team_season_schedule_averages._schedule_points_for = 1.00

    # Assert
    assert test_team_season_schedule_averages.schedule_points_for == 1.00


def test_schedule_points_for_setter_when_value_is_none_should_set_schedule_points_for(
        test_team_season_schedule_averages):
    # Act
    test_team_season_schedule_averages.schedule_points_for = None

    # Assert
    assert test_team_season_schedule_averages._schedule_points_for is None


def test_schedule_points_for_setter_when_value_is_negative_should_raise_value_error(test_team_season_schedule_averages):
    # Act & Assert
    with pytest.raises(ValueError, match="Please enter a non-negative value for schedule points for."):
        test_team_season_schedule_averages.schedule_points_for = -1.00


def test_schedule_points_for_setter_when_value_is_positive_should_set_schedule_points_for(
        test_team_season_schedule_averages):
    # Act
    test_team_season_schedule_averages.schedule_points_for = 1.00

    # Assert
    assert test_team_season_schedule_averages._schedule_points_for == 1.00


def test_schedule_points_for_setter_when_value_is_zero_should_set_schedule_points_for(
        test_team_season_schedule_averages):
    # Act
    test_team_season_schedule_averages.schedule_points_for = 1.00
    test_team_season_schedule_averages.schedule_points_for = 0

    # Assert
    assert test_team_season_schedule_averages._schedule_points_for == 0


def test_schedule_points_against_getter_can_return_none(test_team_season_schedule_averages):
    # Arrange
    test_team_season_schedule_averages._schedule_points_against = None

    # Assert
    assert test_team_season_schedule_averages.schedule_points_against is None


def test_schedule_points_against_getter_can_return_float(test_team_season_schedule_averages):
    # Arrange
    test_team_season_schedule_averages._schedule_points_against = 1.00

    # Assert
    assert test_team_season_schedule_averages.schedule_points_against == 1.00


def test_schedule_points_against_setter_when_value_is_none_should_set_schedule_points_against(
        test_team_season_schedule_averages):
    # Act
    test_team_season_schedule_averages.schedule_points_against = None

    # Assert
    assert test_team_season_schedule_averages._schedule_points_against is None


def test_schedule_points_against_setter_when_value_is_negative_should_raise_value_error(
        test_team_season_schedule_averages):
    # Act & Assert
    with pytest.raises(ValueError, match="Please enter a non-negative value for schedule points against."):
        test_team_season_schedule_averages.schedule_points_against = -1.00


def test_schedule_points_against_setter_when_value_is_positive_should_set_schedule_points_against(
        test_team_season_schedule_averages):
    # Act
    test_team_season_schedule_averages.schedule_points_against = 1.00

    # Assert
    assert test_team_season_schedule_averages._schedule_points_against == 1.00


def test_schedule_points_against_setter_when_value_is_zero_should_set_schedule_points_against(
        test_team_season_schedule_averages):
    # Act
    test_team_season_schedule_averages.schedule_points_against = 1.00
    test_team_season_schedule_averages.schedule_points_against = 0

    # Assert
    assert test_team_season_schedule_averages._schedule_points_against == 0
