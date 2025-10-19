import sqlite3
from unittest.mock import patch

import pytest

from app.data.models.season import Season
from app.data.models.team import Team
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
            test_team = Team(name=None)

    # Assert
    assert isinstance(err.value, ValueError)
    assert err.value.args[0] == "name is required."


def test_validate_not_empty_when_name_is_empty_string_should_raise_value_error():
    # Arrange
    test_app = create_app()
    with test_app.app_context():
        # Act
        with pytest.raises(ValueError) as err:
            test_team = Team(name="")

    # Assert
    assert isinstance(err.value, ValueError)
    assert err.value.args[0] == "name is required."


@patch('app.data.models.team.Team._validate_is_unique')
def test_validate_not_empty_when_name_is_not_empty_string_should_validate_name_is_unique(
        fake_validate_is_unique
):
    # Arrange
    test_app = create_app()
    with test_app.app_context():
        # Act
        test_team = Team(name="Chicago Bears")

    # Assert
    fake_validate_is_unique.assert_called_once_with(
        'name', "Chicago Bears", error_message=f"Row with name='Chicago Bears' already exists in the Team table."
    )


def test_validate_is_unique_when_name_is_not_unique_should_raise_value_error():
    # Arrange
    _init_and_populate_test_db()

    test_app = create_app()
    with test_app.app_context():
        # Act
        with pytest.raises(ValueError) as err:
            test_team = Team(name="Chicago Bears")

    # Assert
    assert err.value.args[0] == f"Row with name='Chicago Bears' already exists in the Team table."


def test_validate_is_unique_when_name_is_unique_should_not_raise_value_error():
    # Arrange
    _init_and_populate_test_db()

    test_err = None

    test_app = create_app()
    with test_app.app_context():
        # Act
        try:
            test_team = Team(name="Green Bay Packers")
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
        INSERT INTO Team (name) VALUES ("Chicago Bears")
    ''')
    conn.commit()
