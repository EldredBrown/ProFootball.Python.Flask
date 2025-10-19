from unittest.mock import patch

import pytest

from app.data.models.game import Game
from app.data.models.league_season import LeagueSeason
from app.data.models.team_season import TeamSeason
from test_app import create_app


def test_validate_not_empty_when_season_year_is_none_should_raise_value_error():
    # Arrange
    test_app = create_app()
    with test_app.app_context():
        # Act
        with pytest.raises(ValueError) as err:
            test_game = Game(season_year=None)

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
            test_game = Game(season_year=0)
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
            test_game = Game(season_year=1)
        except ValueError as err:
            test_err = err

    # Assert
    assert test_err is None


def test_validate_not_empty_when_week_is_none_should_raise_value_error():
    # Arrange
    test_app = create_app()
    with test_app.app_context():
        # Act
        with pytest.raises(ValueError) as err:
            test_game = Game(week=None)

    # Assert
    assert isinstance(err.value, ValueError)
    assert err.value.args[0] == "week is required."


def test_validate_not_empty_when_week_is_zero_should_not_raise_value_error():
    # Arrange
    test_err = None

    test_app = create_app()
    with test_app.app_context():
        # Act
        try:
            test_game = Game(week=0)
        except ValueError as err:
            test_err = err

    # Assert
    assert test_err is None


def test_validate_not_empty_when_week_is_greater_than_zero_not_raise_value_error():
    # Arrange
    test_err = None

    test_app = create_app()
    with test_app.app_context():
        # Act
        try:
            test_game = Game(week=1)
        except ValueError as err:
            test_err = err

    # Assert
    assert test_err is None


def test_validate_not_empty_when_guest_name_is_none_should_raise_value_error():
    # Arrange
    test_app = create_app()
    with test_app.app_context():
        # Act
        with pytest.raises(ValueError) as err:
            test_game = Game(guest_name=None)

    # Assert
    assert isinstance(err.value, ValueError)
    assert err.value.args[0] == "guest_name is required."


def test_validate_not_empty_when_guest_name_is_empty_string_should_raise_value_error():
    # Arrange
    test_app = create_app()
    with test_app.app_context():
        # Act
        with pytest.raises(ValueError) as err:
            test_game = Game(guest_name="")

    # Assert
    assert isinstance(err.value, ValueError)
    assert err.value.args[0] == "guest_name is required."


def test_validate_not_empty_when_guest_name_is_not_empty_string_not_raise_value_error():
    # Arrange
    test_err = None

    test_app = create_app()
    with test_app.app_context():
        # Act
        try:
            test_game = Game(guest_name="Akron Pros")
        except ValueError as err:
            test_err = err

    # Assert
    assert test_err is None


def test_validate_not_empty_when_guest_score_is_none_should_raise_value_error():
    # Arrange
    test_app = create_app()
    with test_app.app_context():
        # Act
        with pytest.raises(ValueError) as err:
            test_game = Game(guest_score=None)

    # Assert
    assert isinstance(err.value, ValueError)
    assert err.value.args[0] == "guest_score is required."


def test_validate_not_empty_when_guest_score_is_zero_should_not_raise_value_error():
    # Arrange
    test_err = None

    test_app = create_app()
    with test_app.app_context():
        # Act
        try:
            test_game = Game(guest_score=0)
        except ValueError as err:
            test_err = err

    # Assert
    assert test_err is None


def test_validate_not_empty_when_guest_score_is_greater_than_zero_not_raise_value_error():
    # Arrange
    test_err = None

    test_app = create_app()
    with test_app.app_context():
        # Act
        try:
            test_game = Game(guest_score=1)
        except ValueError as err:
            test_err = err

    # Assert
    assert test_err is None


def test_validate_not_empty_when_host_name_is_none_should_raise_value_error():
    # Arrange
    test_app = create_app()
    with test_app.app_context():
        # Act
        with pytest.raises(ValueError) as err:
            test_game = Game(host_name=None)

    # Assert
    assert isinstance(err.value, ValueError)
    assert err.value.args[0] == "host_name is required."


def test_validate_not_empty_when_host_name_is_empty_string_should_raise_value_error():
    # Arrange
    test_app = create_app()
    with test_app.app_context():
        # Act
        with pytest.raises(ValueError) as err:
            test_game = Game(host_name="")

    # Assert
    assert isinstance(err.value, ValueError)
    assert err.value.args[0] == "host_name is required."


def test_validate_not_empty_when_host_name_is_not_empty_string_not_raise_value_error():
    # Arrange
    test_err = None

    test_app = create_app()
    with test_app.app_context():
        # Act
        try:
            test_game = Game(host_name="Akron Pros")
        except ValueError as err:
            test_err = err

    # Assert
    assert test_err is None


def test_validate_not_empty_when_host_score_is_none_should_raise_value_error():
    # Arrange
    test_app = create_app()
    with test_app.app_context():
        # Act
        with pytest.raises(ValueError) as err:
            test_game = Game(host_score=None)

    # Assert
    assert isinstance(err.value, ValueError)
    assert err.value.args[0] == "host_score is required."


def test_validate_not_empty_when_host_score_is_zero_should_not_raise_value_error():
    # Arrange
    test_err = None

    test_app = create_app()
    with test_app.app_context():
        # Act
        try:
            test_game = Game(host_score=0)
        except ValueError as err:
            test_err = err

    # Assert
    assert test_err is None


def test_validate_not_empty_when_host_score_is_greater_than_zero_not_raise_value_error():
    # Arrange
    test_err = None

    test_app = create_app()
    with test_app.app_context():
        # Act
        try:
            test_game = Game(host_score=1)
        except ValueError as err:
            test_err = err

    # Assert
    assert test_err is None


def test_decide_winner_and_loser_when_guest_score_greater_than_host_score_should_declare_guest_winner_():
    # Arrange
    test_game = Game(season_year=1, week=1, guest_name='Guest', guest_score=1, host_name='Host', host_score=0)

    # Act
    test_game.decide_winner_and_loser()

    # Assert
    assert test_game.winner_name == test_game.guest_name
    assert test_game.winner_score == test_game.guest_score
    assert test_game.loser_name == test_game.host_name
    assert test_game.loser_score == test_game.host_score


def test_decide_winner_and_loser_when_host_score_greater_than_guest_score_should_declare_host_winner():
    # Arrange
    test_game = Game(season_year=1, week=1, guest_name='Guest', guest_score=0, host_name='Host', host_score=1)

    # Act
    test_game.decide_winner_and_loser()

    # Assert
    assert test_game.winner_name == test_game.host_name
    assert test_game.winner_score == test_game.host_score
    assert test_game.loser_name == test_game.guest_name
    assert test_game.loser_score == test_game.guest_score


def test_decide_winner_and_loser_when_guest_score_equals_host_score_should_declare_neither_guest_nor_host_winner():
    # Arrange
    test_game = Game(season_year=1, week=1, guest_name='Guest', guest_score=0, host_name='Host', host_score=0)

    # Act
    test_game.decide_winner_and_loser()

    # Assert
    assert test_game.winner_name is None
    assert test_game.loser_name is None


def test_is_tie_when_guest_score_greater_than_host_score_should_return_false():
    # Arrange
    test_game = Game(season_year=1, week=1, guest_name='Guest', guest_score=1, host_name='Host', host_score=0)

    # Act
    result = test_game.is_tie()

    # Assert
    assert not result


def test_is_tie_when_host_score_greater_than_guest_score_should_return_false():
    # Arrange
    test_game = Game(season_year=1, week=1, guest_name="Guest", guest_score=0, host_name="Host", host_score=1)

    test_game.guest_score = 0
    test_game.host_score = 1

    # Act
    result = test_game.is_tie()

    # Assert
    assert not result


def test_is_tie_when_guest_score_equals_host_score_should_return_true():
    # Arrange
    test_game = Game(season_year=1, week=1, guest_name="Guest", guest_score=0, host_name="Host", host_score=0)

    # Act
    result = test_game.is_tie()

    # Assert
    assert result
