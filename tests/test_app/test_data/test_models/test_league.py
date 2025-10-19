import sqlite3
from unittest.mock import patch

import pytest

from app.data.models.season import Season
from app.data.models.league import League
from app.data.models.game import Game
from app.data.models.league_season import LeagueSeason
from app.data.models.team_season import TeamSeason
from instance.test_db.db_init import init_db
from test_app import create_app


def test_validate_not_empty_when_short_name_is_none_should_raise_value_error():
    # Arrange
    test_app = create_app()
    with test_app.app_context():
        # Act
        with pytest.raises(ValueError) as err:
            test_league = League(short_name=None)

    # Assert
    assert isinstance(err.value, ValueError)
    assert err.value.args[0] == "short_name is required."


def test_validate_not_empty_when_short_name_is_empty_string_should_raise_value_error():
    # Arrange
    test_app = create_app()
    with test_app.app_context():
        # Act
        with pytest.raises(ValueError) as err:
            test_league = League(short_name="")

    # Assert
    assert isinstance(err.value, ValueError)
    assert err.value.args[0] == "short_name is required."


@patch('app.data.models.league.League._validate_is_unique')
def test_validate_not_empty_when_short_name_is_not_empty_string_should_validate_short_name_is_unique(
        fake_validate_is_unique
):
    # Arrange
    test_app = create_app()
    with test_app.app_context():
        # Act
        test_league = League(short_name="APFA")

    # Assert
    fake_validate_is_unique.assert_called_once_with(
        'short_name', 'APFA', error_message=f"Row with short_name=APFA already exists in the League table."
    )


def test_validate_is_unique_when_short_name_is_not_unique_should_raise_value_error():
    # Arrange
    _init_and_populate_test_db()

    test_app = create_app()
    with test_app.app_context():
        # Act
        with pytest.raises(ValueError) as err:
            test_league = League(short_name="NFL")

    # Assert
    assert err.value.args[0] == f"Row with short_name=NFL already exists in the League table."


def test_validate_is_unique_when_short_name_is_unique_should_not_raise_value_error():
    # Arrange
    _init_and_populate_test_db()

    test_err = None

    test_app = create_app()
    with test_app.app_context():
        # Act
        try:
            test_league = League(short_name="AFL")
        except ValueError as err:
            test_err = err

    # Assert
    assert test_err is None


def test_validate_not_empty_when_long_name_is_none_should_raise_value_error():
    # Arrange
    test_app = create_app()
    with test_app.app_context():
        # Act
        with pytest.raises(ValueError) as err:
            test_league = League(long_name=None)

    # Assert
    assert isinstance(err.value, ValueError)
    assert err.value.args[0] == "long_name is required."


def test_validate_not_empty_when_long_name_is_empty_string_should_raise_value_error():
    # Arrange
    test_app = create_app()
    with test_app.app_context():
        # Act
        with pytest.raises(ValueError) as err:
            test_league = League(long_name="")

    # Assert
    assert isinstance(err.value, ValueError)
    assert err.value.args[0] == "long_name is required."


@patch('app.data.models.league.League._validate_is_unique')
def test_validate_not_empty_when_long_name_is_not_empty_string_should_validate_long_name_is_unique(
        fake_validate_is_unique
):
    # Arrange
    test_app = create_app()
    with test_app.app_context():
        # Act
        test_league = League(long_name="American Professional Football Association")

    # Assert
    fake_validate_is_unique.assert_called_once_with(
        'long_name', 'American Professional Football Association',
        error_message=f"Row with long_name=American Professional Football Association already exists in the League table."
    )


def test_validate_is_unique_when_long_name_is_not_unique_should_raise_value_error():
    # Arrange
    _init_and_populate_test_db()

    test_app = create_app()
    with test_app.app_context():
        # Act
        with pytest.raises(ValueError) as err:
            test_league = League(long_name="National Football League")

    # Assert
    assert err.value.args[0] == f"Row with long_name=National Football League already exists in the League table."


def test_validate_is_unique_when_long_name_is_unique_should_not_raise_value_error():
    # Arrange
    _init_and_populate_test_db()

    test_err = None

    test_app = create_app()
    with test_app.app_context():
        # Act
        try:
            test_league = League(long_name="American Football League")
        except ValueError as err:
            test_err = err

    # Assert
    assert test_err is None


def test_validate_not_empty_when_first_season_year_is_none_should_raise_value_error():
    # Arrange
    test_app = create_app()
    with test_app.app_context():
        # Act
        with pytest.raises(ValueError) as err:
            test_league = League(first_season_year=None)

    # Assert
    assert isinstance(err.value, ValueError)
    assert err.value.args[0] == "first_season_year is required."


@patch('app.data.models.league.League._validate_is_unique')
def test_validate_not_empty_when_first_season_year_is_zero_should_not_raise_value_error(fake_validate_is_unique):
    # Arrange
    test_err = None

    test_app = create_app()
    with test_app.app_context():
        # Act
        try:
            test_league = League(first_season_year=0)
        except ValueError as err:
            test_err = err

    # Assert
    assert test_err is None
    fake_validate_is_unique.assert_not_called()


@patch('app.data.models.league.League._validate_is_unique')
def test_validate_not_empty_when_first_season_year_is_greater_than_zero_should_not_raise_value_error(fake_validate_is_unique):
    # Arrange
    test_err = None

    test_app = create_app()
    with test_app.app_context():
        # Act
        try:
            test_league = League(first_season_year=1)
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
        INSERT INTO League (short_name, long_name, first_season_year)
            VALUES ("NFL", "National Football League", 1922)
    ''')
    conn.commit()
