from decimal import Decimal

from app.services.utilities import team_season_utils as mod


def test_calculate_expected_winning_percentage_when_sum_of_points_for_and_points_against_equals_zero_should_return_none():
    # Arrange
    points_for = Decimal('0.00')
    points_against = Decimal('0.00')

    # Act
    exp_winning_percentage = mod.calculate_expected_winning_percentage(points_for, points_against)

    # Assert
    assert exp_winning_percentage is None


def test_calculate_expected_winning_percentage_when_sum_of_points_for_and_points_against_does_not_equal_zero_should_return_correct_result():
    # Arrange
    points_for = Decimal('2.00')
    points_against = Decimal('2.00')

    # Act
    exp_winning_percentage = mod.calculate_expected_winning_percentage(points_for, points_against)

    # Assert
    o = pow(points_for, mod.EXPONENT)
    d = pow(points_against, mod.EXPONENT)
    assert exp_winning_percentage == o / (o + d)


def test_divide_when_args_are_decimals_and_denominator_equals_zero_should_return_none():
    # Arrange
    numerator = Decimal('1.00')
    denominator = Decimal('0.00')

    # Act
    result = mod.divide(numerator, denominator)

    # Assert
    assert result is None


def test_divide_when_args_are_decimals_and_denominator_does_not_equal_zero_should_return_correct_result():
    # Arrange
    numerator = Decimal('7.50')
    denominator = Decimal('3.75')

    # Act
    result = mod.divide(numerator, denominator)

    # Assert
    assert result == Decimal('2')


def test_divide_when_args_are_integers_and_denominator_equals_zero_should_return_none():
    # Arrange
    numerator = 1
    denominator = 0

    # Act
    result = mod.divide(numerator, denominator)

    # Assert
    assert result is None


def test_divide_when_args_are_integers_and_denominator_does_not_equal_zero_should_return_correct_result():
    # Arrange
    numerator = 4
    denominator = 3

    # Act
    result = mod.divide(numerator, denominator)

    # Assert
    assert result == Decimal(numerator) / Decimal(denominator)


def test_divide_when_numerator_is_integer_and_denominator_is_decimal_not_equal_to_zero_should_return_correct_result():
    # Arrange
    numerator = 4
    denominator = Decimal('3.14159')

    # Act
    result = mod.divide(numerator, denominator)

    # Assert
    assert result == Decimal(numerator) / Decimal(denominator)


def test_divide_when_numerator_is_decimal_and_denominator_is_integer_not_equal_to_zero_should_return_correct_result():
    # Arrange
    numerator = Decimal('3.14159')
    denominator = 4

    # Act
    result = mod.divide(numerator, denominator)

    # Assert
    assert result == Decimal(numerator) / Decimal(denominator)


def test_update_rankings_when_games_equals_zero_should_return_correct_result():
    # Arrange
    points = 0
    games = 0
    team_season_schedule_average_points = Decimal('0')
    league_season_average_points = Decimal('0')

    # Act
    result = mod.update_rankings(points, games, team_season_schedule_average_points, league_season_average_points)

    # Assert
    average = None
    factor = None
    index = None
    assert result == (average, factor, index)


def test_update_rankings_when_games_not_equal_to_zero_and_factor_is_none_should_return_correct_result():
    # Arrange
    points = 20
    games = 1
    team_season_schedule_average_points = Decimal('0')
    league_season_average_points = Decimal('0')

    # Act
    result = mod.update_rankings(points, games, team_season_schedule_average_points, league_season_average_points)

    # Assert
    average = mod.divide(points, games)
    factor = None
    index = None
    assert result == (average, factor, index)


def test_update_rankings_when_games_not_equal_to_zero_and_factor_is_not_none_should_return_correct_result():
    # Arrange
    points = 20
    games = 1
    team_season_schedule_average_points = Decimal('20.00')
    league_season_average_points = Decimal('0')

    # Act
    result = mod.update_rankings(points, games, team_season_schedule_average_points, league_season_average_points)

    # Assert
    average = mod.divide(points, games)
    factor = mod.divide(average, team_season_schedule_average_points)
    index = mod.divide(average + factor * league_season_average_points, 2)
    assert result == (average, factor, index)
