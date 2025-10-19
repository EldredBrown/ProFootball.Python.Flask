from decimal import Decimal
from fractions import Fraction

import pytest

from app.data.models.game import Game
from app.data.models.league_season import LeagueSeason
from app.data.models.team_season import EXPONENT, TeamSeason
from test_app import create_app


@pytest.fixture
def test_team_season() -> TeamSeason:
    return TeamSeason(team_name="Chicago Bears", season_year=1985, league_name="NFL")


def test_validate_not_empty_when_team_name_is_none_should_raise_value_error():
    # Arrange
    test_app = create_app()
    with test_app.app_context():
        # Act
        with pytest.raises(ValueError) as err:
            test_team_season = TeamSeason(team_name=None)

    # Assert
    assert isinstance(err.value, ValueError)
    assert err.value.args[0] == "team_name is required."


def test_validate_not_empty_when_team_name_is_zero_should_not_raise_value_error():
    # Arrange
    test_err = None

    test_app = create_app()
    with test_app.app_context():
        # Act
        try:
            test_team_season = TeamSeason(team_name=0)
        except ValueError as err:
            test_err = err

    # Assert
    assert test_err is None


def test_validate_not_empty_when_team_name_is_greater_than_zero_should_validate_team_name_is_unique():
    # Arrange
    test_err = None

    test_app = create_app()
    with test_app.app_context():
        # Act
        try:
            test_team_season = TeamSeason(team_name=1)
        except ValueError as err:
            test_err = err

    # Assert
    assert test_err is None


def test_validate_not_empty_when_season_year_is_none_should_raise_value_error():
    # Arrange
    test_app = create_app()
    with test_app.app_context():
        # Act
        with pytest.raises(ValueError) as err:
            test_team_season = TeamSeason(season_year=None)

    # Assert
    assert isinstance(err.value, ValueError)
    assert err.value.args[0] == "season_year is required."


def test_validate_not_empty_when_season_year_is_zero_should_not_raise_value_error():
    # Arrange
    test_err = None

    test_app = create_app()
    with test_app.app_context():
        # Act
        try:
            test_team_season = TeamSeason(season_year=0)
        except ValueError as err:
            test_err = err

    # Assert
    assert test_err is None


def test_validate_not_empty_when_season_year_is_greater_than_zero_should_validate_season_year_is_unique():
    # Arrange
    test_err = None

    test_app = create_app()
    with test_app.app_context():
        # Act
        try:
            test_team_season = TeamSeason(season_year=1)
        except ValueError as err:
            test_err = err

    # Assert
    assert test_err is None


def test_validate_not_empty_when_league_name_is_none_should_raise_value_error():
    # Arrange
    test_app = create_app()
    with test_app.app_context():
        # Act
        with pytest.raises(ValueError) as err:
            test_team_season = TeamSeason(league_name=None)

    # Assert
    assert isinstance(err.value, ValueError)
    assert err.value.args[0] == "league_name is required."


def test_validate_not_empty_when_league_name_is_zero_should_not_raise_value_error():
    # Arrange
    test_err = None

    test_app = create_app()
    with test_app.app_context():
        # Act
        try:
            test_team_season = TeamSeason(league_name=0)
        except ValueError as err:
            test_err = err

    # Assert
    assert test_err is None


def test_validate_not_empty_when_league_name_is_greater_than_zero_should_validate_league_name_is_unique():
    # Arrange
    test_err = None

    test_app = create_app()
    with test_app.app_context():
        # Act
        try:
            test_team_season = TeamSeason(league_name=1)
        except ValueError as err:
            test_err = err

    # Assert
    assert test_err is None


def test_calculate_expected_wins_and_losses_when_team_season_points_for_and_against_are_zero_should_set_expected_wins_and_losses_to_zero(
        test_team_season):
    # Arrange
    test_team_season.points_for = 0
    test_team_season.points_against = 0

    # Act
    test_team_season.calculate_expected_wins_and_losses()

    # Assert
    assert test_team_season.expected_wins == 0
    assert test_team_season.expected_losses == 0


def test_calculate_expected_wins_and_losses_when_team_season_points_for_and_against_are_not_zero_should_set_expected_wins_and_losses_to_not_zero(
        test_team_season):
    # Arrange
    games = 2
    points_for = 40
    points_against = 40

    test_team_season.games = games
    test_team_season.points_for = points_for
    test_team_season.points_against = points_against

    # Act
    test_team_season.calculate_expected_wins_and_losses()

    # Assert
    a = points_for ** EXPONENT
    b = points_for ** EXPONENT + points_against ** EXPONENT
    exp_pct = a / b
    assert test_team_season.expected_wins == exp_pct * games
    assert test_team_season.expected_losses == (1 - exp_pct) * games


def test_calculate_winning_percentage_when_team_has_no_games_should_set_winning_percentage_to_none(test_team_season):
    # Arrange
    test_team_season.games = 0

    # Act
    test_team_season.calculate_winning_percentage()

    # Assert
    assert test_team_season.winning_percentage is None


def test_calculate_winning_percentage_when_team_has_winning_record(test_team_season):
    # Arrange
    games = 2
    wins = 1
    ties = 1

    test_team_season.games = games
    test_team_season.wins = wins
    test_team_season.ties = ties

    # Act
    test_team_season.calculate_winning_percentage()

    # Assert
    assert test_team_season.winning_percentage == Fraction((2 * wins) + ties, (2 * games))


def test_calculate_winning_percentage_when_team_has_losing_record(test_team_season):
    # Arrange
    games = 2
    wins = 0
    ties = 1

    test_team_season.games = games
    test_team_season.wins = wins
    test_team_season.ties = ties

    # Act
    test_team_season.calculate_winning_percentage()

    # Assert
    assert test_team_season.winning_percentage == Fraction((2 * wins) + ties, (2 * games))


def test_calculate_winning_percentage_when_team_has_500_record_without_ties(test_team_season):
    # Arrange
    games = 2
    wins = 1
    ties = 0

    test_team_season.games = games
    test_team_season.wins = wins
    test_team_season.ties = ties

    # Act
    test_team_season.calculate_winning_percentage()

    # Assert
    assert test_team_season.winning_percentage == Fraction((2 * wins) + ties, (2 * games))


def test_calculate_winning_percentage_when_team_has_500_record_with_ties(test_team_season):
    # Arrange
    games = 2
    wins = 0
    ties = 2

    test_team_season.games = games
    test_team_season.wins = wins
    test_team_season.ties = ties

    # Act
    test_team_season.calculate_winning_percentage()

    # Assert
    assert test_team_season.winning_percentage == Fraction((2 * wins) + ties, (2 * games))


def test_update_rankings_when_team_games_is_zero_should_set_all_rankings_to_none(test_team_season):
    # Arrange
    test_team_season.games = 0

    # Act
    team_season_schedule_average_points_for = Decimal('0')
    team_season_schedule_average_points_against = Decimal('0')
    league_season_average_points = Decimal('0')
    test_team_season.update_rankings(team_season_schedule_average_points_for,
                                     team_season_schedule_average_points_against,
                                     league_season_average_points)

    # Assert
    assert test_team_season.offensive_average is None
    assert test_team_season.offensive_factor is None
    assert test_team_season.offensive_index is None
    assert test_team_season.defensive_average is None
    assert test_team_season.defensive_factor is None
    assert test_team_season.defensive_index is None
    assert test_team_season.final_expected_winning_percentage is None


def test_update_rankings_when_team_season_schedule_average_points_against_is_zero_should_set_offensive_factor_to_none(
        test_team_season):
    # Arrange
    games = 2
    points_for = 30
    points_against = 30

    test_team_season.games = games
    test_team_season.points_for = points_for
    test_team_season.points_against = points_against

    # Act
    team_season_schedule_average_points_for = 0.00
    team_season_schedule_average_points_against = 0.00
    league_season_average_points = 0.00
    test_team_season.update_rankings(team_season_schedule_average_points_for,
                                     team_season_schedule_average_points_against,
                                     league_season_average_points)

    # Assert
    assert test_team_season.offensive_average == Decimal(points_for) / Decimal(games)
    assert test_team_season.offensive_factor is None
    assert test_team_season.offensive_index is None

    assert test_team_season.defensive_average == Decimal(points_against) / Decimal(games)
    assert test_team_season.defensive_factor is None
    assert test_team_season.defensive_index is None

    assert test_team_season.final_expected_winning_percentage is None


def test_update_rankings_when_team_season_schedule_average_points_against_is_not_zero_should_set_offensive_factor_to_not_none(
        test_team_season):
    # Arrange
    games = 2
    points_for = 30
    points_against = 30

    test_team_season.games = games
    test_team_season.points_for = points_for
    test_team_season.points_against = points_against

    # Act
    team_season_schedule_average_points_for = 0.00
    team_season_schedule_average_points_against = 20.00
    league_season_average_points = 0.00
    test_team_season.update_rankings(team_season_schedule_average_points_for,
                                     team_season_schedule_average_points_against,
                                     league_season_average_points)

    # Assert
    assert test_team_season.offensive_average == Decimal(points_for) / Decimal(games)
    assert test_team_season.offensive_factor == \
           test_team_season.offensive_average / team_season_schedule_average_points_against
    assert test_team_season.offensive_index == \
           (test_team_season.offensive_average + test_team_season.offensive_factor * league_season_average_points) / 2

    assert test_team_season.defensive_average == Decimal(points_against) / Decimal(games)
    assert test_team_season.defensive_factor is None
    assert test_team_season.defensive_index is None

    assert test_team_season.final_expected_winning_percentage is None


def test_update_rankings_when_team_season_schedule_average_points_are_not_zero_should_set_all_rankings_to_not_none(
        test_team_season):
    # Arrange
    games = 2
    points_for = 30
    points_against = 30

    test_team_season.games = games
    test_team_season.points_for = points_for
    test_team_season.points_against = points_against

    # Act
    team_season_schedule_average_points_for = 20.00
    team_season_schedule_average_points_against = 20.00
    league_season_average_points = 0
    test_team_season.update_rankings(team_season_schedule_average_points_for,
                                     team_season_schedule_average_points_against,
                                     league_season_average_points)

    # Assert
    assert test_team_season.offensive_average == points_for / games
    assert test_team_season.offensive_factor == \
           test_team_season.offensive_average / team_season_schedule_average_points_against
    assert test_team_season.offensive_index == \
           (test_team_season.offensive_average + test_team_season.offensive_factor * league_season_average_points) / 2

    assert test_team_season.defensive_average == points_against / games
    assert test_team_season.defensive_factor == \
           test_team_season.defensive_average / team_season_schedule_average_points_for
    assert test_team_season.defensive_index == \
           (test_team_season.defensive_average + test_team_season.defensive_factor * league_season_average_points) / 2

    o = test_team_season.offensive_index ** EXPONENT
    d = test_team_season.defensive_index ** EXPONENT
    assert test_team_season.final_expected_winning_percentage == o / (o + d)
