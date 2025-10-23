import sqlite3

import pytest

from app.data.models.season import Season
from app.data.models.team import Team
from app.data.models.game import Game
from app.data.models.league_season import LeagueSeason
from app.data.models.team_season import TeamSeason
from instance.test_db.db_init import init_db
from test_app import create_app


@pytest.fixture
def test_app():
    return create_app()


def test_validate_not_empty_when_name_is_none_should_raise_value_error(test_app):
    # Arrange
    with test_app.app_context():
        # Act
        with pytest.raises(ValueError) as err:
            test_team = Team(name=None)

    # Assert
    assert isinstance(err.value, ValueError)
    assert err.value.args[0] == "name is required."


def test_validate_not_empty_when_name_is_empty_should_raise_value_error(test_app):
    # Arrange
    with test_app.app_context():
        # Act
        with pytest.raises(ValueError) as err:
            test_team = Team(name="")

    # Assert
    assert isinstance(err.value, ValueError)
    assert err.value.args[0] == "name is required."


def test_validate_not_empty_when_name_is_not_empty_should_not_raise_value_error(test_app):
    # Arrange
    err = None

    with test_app.app_context():
        # Act
        try:
            test_team = Team(name="Chicago Cardinals")
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
        INSERT INTO Team (name) VALUES ("Chicago Cardinals")
    ''')
    conn.commit()
