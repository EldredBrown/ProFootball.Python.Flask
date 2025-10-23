import sqlite3

from unittest.mock import patch

import pytest

from app.data.models.season import Season
from app.data.models.game import Game
from app.data.models.league_season import LeagueSeason
from app.data.models.team_season import TeamSeason
from instance.test_db.db_init import init_db
from test_app import create_app


@pytest.fixture
def test_app():
    return create_app()


def test_validate_not_empty_when_year_is_none_should_raise_value_error(test_app):
    # Arrange
    with test_app.app_context():
        # Act
        with pytest.raises(ValueError) as err:
            test_season = Season(year=None)

    # Assert
    assert isinstance(err.value, ValueError)
    assert err.value.args[0] == "Year is required."


def test_validate_not_empty_when_year_is_zero_should_not_raise_value_error(test_app):
    # Arrange
    err = None

    with test_app.app_context():
        # Act
        try:
            test_season = Season(year=0)
        except ValueError as err:
            pass

    # Assert
    assert err is None


def test_validate_not_empty_when_year_is_greater_than_zero_should_not_raise_value_error(test_app):
    # Arrange
    err = None

    with test_app.app_context():
        # Act
        try:
            test_season = Season(year=1)
        except ValueError as err:
            pass

    # Assert
    assert err is None


def _init_and_populate_test_db():
    init_db()
    conn = sqlite3.connect(
        'D:\\Source\\Repos\\ProFootball\\ProFootball.Python.Flask\\tests\\instance\\test_db\\test_db.sqlite3'
    )
    c = conn.cursor()
    c.execute('''
        INSERT INTO Season (year) VALUES (1)
    ''')
    conn.commit()
