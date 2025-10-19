import sqlite3
from unittest.mock import patch

import pytest

from app.data.models.season import Season
from app.data.models.game import Game
from app.data.models.league_season import LeagueSeason
from app.data.models.team_season import TeamSeason
from instance.test_db.db_init import init_db
from test_app import create_app


def test_validate_not_empty_when_year_is_none_should_raise_value_error():
    # Arrange
    test_app = create_app()
    with test_app.app_context():
        # Act
        with pytest.raises(ValueError) as err:
            test_season = Season(year=None)

    # Assert
    assert isinstance(err.value, ValueError)
    assert err.value.args[0] == "Year is required."


@patch('app.data.models.season.Season._validate_is_unique')
def test_validate_not_empty_when_year_is_zero_should_validate_year_is_unique(fake_validate_is_unique):
    # Arrange
    test_app = create_app()
    with test_app.app_context():
        # Act
        test_season = Season(year=0)

    # Assert
    fake_validate_is_unique.assert_called_once_with(
        'year', 0, error_message=f"Row with year=0 already exists in the Season table."
    )


@patch('app.data.models.season.Season._validate_is_unique')
def test_validate_not_empty_when_year_is_greater_than_zero_should_validate_year_is_unique(fake_validate_is_unique):
    # Arrange
    test_app = create_app()
    with test_app.app_context():
        # Act
        test_season = Season(year=1)

    # Assert
    fake_validate_is_unique.assert_called_once_with(
        'year', 1, error_message=f"Row with year=1 already exists in the Season table."
    )


def test_validate_is_unique_when_year_is_not_unique_should_raise_value_error():
    # Arrange
    _init_and_populate_test_db()

    test_app = create_app()
    with test_app.app_context():
        # Act
        with pytest.raises(ValueError) as err:
            season = Season(year=1)

    # Assert
    assert err.value.args[0] == f"Row with year=1 already exists in the Season table."


def test_validate_is_unique_when_year_is_unique_should_not_raise_value_error():
    # Arrange
    _init_and_populate_test_db()

    test_err = None

    test_app = create_app()
    with test_app.app_context():
        # Act
        try:
            season = Season(year=2)
        except ValueError as err:
            test_err = err

    # Assert
    assert test_err is None


def _init_and_populate_test_db():
    init_db()
    conn = sqlite3.connect(
        'D:\\Source\\Repos\\ProFootball\\Python\\Flask\\pro_football_app\\tests\\instance\\test_db\\test_db.sqlite3'
    )
    c = conn.cursor()
    c.execute('''
        INSERT INTO Season (year) VALUES (1)
    ''')
    conn.commit()
