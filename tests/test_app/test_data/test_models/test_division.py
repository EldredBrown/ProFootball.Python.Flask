import sqlite3
from unittest.mock import patch

import pytest

from app.data.models.division import Division
from app.data.models.game import Game
from app.data.models.league_season import LeagueSeason
from app.data.models.team_season import TeamSeason
from instance.test_db.db_init import init_db
from test_app import create_app


def test_validate_not_empty_when_name_is_none_should_raise_value_error():
    # Arrange
    test_app = create_app()
    with test_app.app_context():
        # Act
        with pytest.raises(ValueError) as err:
            test_division = Division(name=None)

    # Assert
    assert isinstance(err.value, ValueError)
    assert err.value.args[0] == "name is required."


def test_validate_not_empty_when_name_is_empty_string_should_raise_value_error():
    # Arrange
    test_app = create_app()
    with test_app.app_context():
        # Act
        with pytest.raises(ValueError) as err:
            test_division = Division(name="")

    # Assert
    assert isinstance(err.value, ValueError)
    assert err.value.args[0] == "name is required."


@patch('app.data.models.division.Division._validate_is_unique')
def test_validate_not_empty_when_name_is_not_empty_string_should_validate_name_is_unique(
        fake_validate_is_unique
):
    # Arrange
    test_app = create_app()
    with test_app.app_context():
        # Act
        test_division = Division(name="NFC East")

    # Assert
    fake_validate_is_unique.assert_called_once_with(
        'name', 'NFC East', error_message=f"Row with name=NFC East already exists in the Division table."
    )


def test_validate_is_unique_when_name_is_not_unique_should_raise_value_error():
    # Arrange
    _init_and_populate_test_db()

    test_app = create_app()
    with test_app.app_context():
        # Act
        with pytest.raises(ValueError) as err:
            test_division = Division(name="NFC East")

    # Assert
    assert err.value.args[0] == f"Row with name=NFC East already exists in the Division table."


def test_validate_is_unique_when_name_is_unique_should_not_raise_value_error():
    # Arrange
    _init_and_populate_test_db()

    test_err = None

    test_app = create_app()
    with test_app.app_context():
        # Act
        try:
            test_division = Division(name="NFC Central")
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
            test_division = Division(league_name=None)

    # Assert
    assert isinstance(err.value, ValueError)
    assert err.value.args[0] == "league_name is required."


def test_validate_not_empty_when_league_name_is_empty_should_raise_value_error():
    # Arrange
    test_app = create_app()
    with test_app.app_context():
        # Act
        with pytest.raises(ValueError) as err:
            test_division = Division(league_name="")

    # Assert
    assert isinstance(err.value, ValueError)
    assert err.value.args[0] == "league_name is required."


@patch('app.data.models.conference.Conference._validate_is_unique')
def test_validate_not_empty_when_league_name_is_not_empty_should_not_raise_value_error(fake_validate_is_unique):
    # Arrange
    test_err = None

    test_app = create_app()
    with test_app.app_context():
        # Act
        try:
            test_division = Division(league_name="NFL")
        except ValueError as err:
            test_err = err

    # Assert
    assert test_err is None
    fake_validate_is_unique.assert_not_called()


def test_validate_not_empty_when_first_season_year_is_none_should_raise_value_error():
    # Arrange
    test_app = create_app()
    with test_app.app_context():
        # Act
        with pytest.raises(ValueError) as err:
            test_division = Division(first_season_year=None)

    # Assert
    assert isinstance(err.value, ValueError)
    assert err.value.args[0] == "first_season_year is required."


@patch('app.data.models.division.Division._validate_is_unique')
def test_validate_not_empty_when_first_season_year_is_zero_should_not_raise_value_error(fake_validate_is_unique):
    # Arrange
    test_err = None

    test_app = create_app()
    with test_app.app_context():
        # Act
        try:
            test_division = Division(first_season_year=0)
        except ValueError as err:
            test_err = err

    # Assert
    assert test_err is None
    fake_validate_is_unique.assert_not_called()


@patch('app.data.models.division.Division._validate_is_unique')
def test_validate_not_empty_when_first_season_year_is_greater_than_zero_should_not_raise_value_error(fake_validate_is_unique):
    # Arrange
    test_err = None

    test_app = create_app()
    with test_app.app_context():
        # Act
        try:
            test_division = Division(first_season_year=1)
        except ValueError as err:
            test_err = err

    # Assert
    assert test_err is None
    fake_validate_is_unique.assert_not_called()


def _init_and_populate_test_db():
    init_db()
    conn = sqlite3.connect(
        'D:\\Source\\Repos\\ProFootball\\Python\\Flask\\pro_football_app\\tests\\instance\\test_db\\test_db.sqlite3'
    )
    c = conn.cursor()
    c.execute('''
        INSERT INTO Division (name, league_name, conference_name, first_season_year)
            VALUES ("NFC East", "NFL", "NFC", 1)
    ''')
    conn.commit()
