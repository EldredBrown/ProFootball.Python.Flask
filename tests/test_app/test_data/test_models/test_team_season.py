import sqlite3
from decimal import Decimal
from unittest.mock import patch

import pytest

from app.data.models import team_season as mut
from app.data.models.team_season import TeamSeason
from instance.test_db.db_init import init_db


@patch('app.data.models.team_season.team_season_utils')
def test_calculate_expected_wins_and_losses_when_expected_winning_percentage_is_none_should_set_expected_wins_and_losses_to_zero(
    fake_team_season_utils
):
    # Arrange
    exp_pct = None
    fake_team_season_utils.calculate_expected_winning_percentage.return_value = exp_pct

    test_team_season = TeamSeason(
        team_name="Team",
        season_year=1,
        league_name="League",
        points_for = 1,
        points_against = 1,
    )

    # Act
    test_team_season.calculate_expected_wins_and_losses()

    # Assert
    fake_team_season_utils.calculate_expected_winning_percentage.assert_called_once_with(
        test_team_season.points_for, test_team_season.points_against
    )
    assert test_team_season.expected_wins == 0
    assert test_team_season.expected_losses == 0


@pytest.mark.parametrize(
    "test_input,expected_wins,expected_losses",
    [
        (Decimal('0.750'), Decimal('1.5'), Decimal('0.5')),
        (Decimal('0.500'), Decimal('1.0'), Decimal('1.0')),
        (Decimal('0.250'), Decimal('0.5'), Decimal('1.5')),
    ]
)
@patch('app.data.models.team_season.team_season_utils')
def test_calculate_expected_wins_and_losses_when_expected_winning_percentage_is_not_none_should_set_expected_wins_and_losses_to_correct_values(
    fake_team_season_utils, test_input, expected_wins, expected_losses
):
    # Arrange
    exp_pct = test_input
    fake_team_season_utils.calculate_expected_winning_percentage.return_value = exp_pct

    test_team_season = TeamSeason(
        team_name="Team",
        season_year=1,
        league_name="League",
        games=2,
        points_for = 1,
        points_against = 1,
    )

    # Act
    test_team_season.calculate_expected_wins_and_losses()

    # Assert
    fake_team_season_utils.calculate_expected_winning_percentage.assert_called_once_with(
        test_team_season.points_for, test_team_season.points_against
    )
    assert test_team_season.expected_wins == expected_wins
    assert test_team_season.expected_losses == expected_losses


@pytest.mark.parametrize(
    "test_wins,test_losses,test_ties,expected_winning_percentage",
    [
        (2, 0, 0, Decimal('1.000')),
        (1, 1, 0, Decimal('0.500')),
        (0, 2, 0, Decimal('0.000')),
        (1, 0, 1, Decimal('0.750')),
        (0, 1, 1, Decimal('0.250')),
        (0, 0, 2, Decimal('0.500')),
    ]
)
def test_calculate_winning_percentage_should_calculate_correct_winning_percentage(
    test_wins, test_losses, test_ties, expected_winning_percentage
):
    # Arrange
    test_team_season = TeamSeason(
        team_name="Team",
        season_year=1,
        league_name="League",
        games=2,
        wins=test_wins,
        losses=test_losses,
        ties=test_ties
    )

    # Act
    test_team_season.calculate_winning_percentage()

    # Assert
    assert test_team_season.winning_percentage == expected_winning_percentage


@pytest.mark.parametrize(
    "test_games,test_points_for,test_points_against,"
    "team_season_schedule_average_points_for,team_season_schedule_average_points_against,league_season_average_points,"
    "expected_offensive_average,expected_offensive_factor,expected_offensive_index,"
    "expected_defensive_average,expected_defensive_factor,expected_defensive_index,"
    "expected_final_expected_winning_percentage",
    [
        (
                0, 0, 0,
                Decimal('0.00'), Decimal('0.00'), Decimal('0.00'),
                None, None, None,
                None, None, None,
                None,
        ),
        (
                3, 60, 60,
                Decimal('0.00'), Decimal('0.00'), Decimal('0.00'),
                Decimal('20.00'), None, None,
                Decimal('20.00'), None, None,
                None,
        ),
        (
                3, 60, 60,
                Decimal('20.00'), Decimal('20.00'), Decimal('20.00'),
                Decimal('20.00'), Decimal('1.000'), Decimal('20.00'),
                Decimal('20.00'), Decimal('1.000'), Decimal('20.00'),
                Decimal('0.500'),
        ),
        (
                3, 45, 75,
                Decimal('20.00'), Decimal('20.00'), Decimal('20.00'),
                Decimal('15.00'), Decimal('0.750'), Decimal('15.00'),
                Decimal('25.00'), Decimal('1.250'), Decimal('25.00'),
                (Decimal('15.00')**mut.EXPONENT / (Decimal('15.00')**mut.EXPONENT + Decimal('25.00')**mut.EXPONENT)),
        ),
        (
                3, 75, 45,
                Decimal('20.00'), Decimal('20.00'), Decimal('20.00'),
                Decimal('25.00'), Decimal('1.250'), Decimal('25.00'),
                Decimal('15.00'), Decimal('0.750'), Decimal('15.00'),
                (Decimal('25.00')**mut.EXPONENT / (Decimal('15.00')**mut.EXPONENT + Decimal('25.00')**mut.EXPONENT)),
        ),
    ]
)
def test_team_season_update_rankings_should_update_rankings_to_correct_values(
        test_games, test_points_for, test_points_against,
        team_season_schedule_average_points_for, team_season_schedule_average_points_against, league_season_average_points,
        expected_offensive_average, expected_offensive_factor, expected_offensive_index,
        expected_defensive_average, expected_defensive_factor, expected_defensive_index,
        expected_final_expected_winning_percentage
):
    # Arrange
    test_team_season = TeamSeason(
        team_name="Team",
        season_year=1,
        league_name="League",
        games=test_games,
        points_for=test_points_for,
        points_against=test_points_against
    )

    # Act
    test_team_season.update_rankings(
        team_season_schedule_average_points_for,
        team_season_schedule_average_points_against,
        league_season_average_points
    )

    # Assert
    assert test_team_season.offensive_average == expected_offensive_average
    assert test_team_season.offensive_factor == expected_offensive_factor
    assert test_team_season.offensive_index == expected_offensive_index
    assert test_team_season.defensive_average == expected_defensive_average
    assert test_team_season.defensive_average == expected_defensive_average
    assert test_team_season.defensive_average == expected_defensive_average
    assert test_team_season.final_expected_winning_percentage == expected_final_expected_winning_percentage


def _init_and_populate_test_db():
    init_db()
    conn = sqlite3.connect(
        'D:\\Source\\Repos\\ProFootball\\ProFootball.Python.Flask\\tests\\instance\\test_db\\test_db.sqlite3'
    )
    c = conn.cursor()
    c.execute('''
        INSERT INTO TeamSeason (team_name, season_year, league_name) VALUES ("Chicago Cardinals", 1920, "APFA")
    ''')
    conn.commit()
