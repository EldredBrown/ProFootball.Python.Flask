import pytest

from app.data.models.game import Game


def test_validate_season_id_when_season_id_is_none_should_raise_value_error():
    # Arrange
    # Act
    with pytest.raises(ValueError) as err:
        test_game = Game(
            season_id=None,
            week=1,
            guest_name="Guest",
            guest_score=0,
            host_name="Host",
            host_score=0,
            is_playoff=False
        )

    # Assert
    assert isinstance(err.value, ValueError)
    assert err.value.args[0] == "season_id is required."


def test_validate_season_id_when_season_id_is_zero_should_raise_value_error():
    # Arrange
    # Act
    with pytest.raises(ValueError) as err:
        test_game = Game(
            season_id=0,
            week=1,
            guest_name="Guest",
            guest_score=0,
            host_name="Host",
            host_score=0,
            is_playoff=False
        )

    # Assert
    assert isinstance(err.value, ValueError)
    assert err.value.args[0] == "season_id cannot be earlier than 1920."


def test_validate_season_id_when_season_id_is_before_1920_should_raise_value_error():
    # Arrange
    # Act
    with pytest.raises(ValueError) as err:
        test_game = Game(
            season_id=1919,
            week=1,
            guest_name="Guest",
            guest_score=0,
            host_name="Host",
            host_score=0,
            is_playoff=False
        )

    # Assert
    assert isinstance(err.value, ValueError)
    assert err.value.args[0] == "season_id cannot be earlier than 1920."


def test_validate_season_id_when_season_id_is_1920_should_not_raise_value_error():
    # Arrange
    err = None

    # Act
    try:
        test_game = Game(
            season_id=1920,
            week=1,
            guest_name="Guest",
            guest_score=0,
            host_name="Host",
            host_score=0,
            is_playoff=False
        )
    except ValueError as err:
        pass

    # Assert
    assert err is None


def test_validate_season_id_when_season_id_is_after_1920_should_not_raise_value_error():
    # Arrange
    err = None

    # Act
    try:
        test_game = Game(
            season_id=1921,
            week=1,
            guest_name="Guest",
            guest_score=0,
            host_name="Host",
            host_score=0,
            is_playoff=False
        )
    except ValueError as err:
        pass

    # Assert
    assert err is None


def test_validate_week_when_week_is_none_should_raise_value_error():
    # Arrange
    # Act
    with pytest.raises(ValueError) as err:
        test_game = Game(
            season_id=1920,
            week=None,
            guest_name="Guest",
            guest_score=0,
            host_name="Host",
            host_score=0,
            is_playoff=False
        )

    # Assert
    assert isinstance(err.value, ValueError)
    assert err.value.args[0] == "week is required."


def test_validate_not_empty_when_week_is_zero_should_raise_value_error():
    # Arrange
    # Act
    with pytest.raises(ValueError) as err:
        test_game = Game(
            season_id=1920,
            week=0,
            guest_name="Guest",
            guest_score=0,
            host_name="Host",
            host_score=0,
            is_playoff=False
        )

    # Assert
    assert isinstance(err.value, ValueError)
    assert err.value.args[0] == "week cannot be less than 1."


def test_validate_week_when_week_is_greater_than_zero_should_not_raise_value_error():
    # Arrange
    err = None

    # Act
    try:
        test_game = Game(
            season_id=1920,
            week=1,
            guest_name="Guest",
            guest_score=0,
            host_name="Host",
            host_score=0,
            is_playoff=False
        )
    except ValueError as err:
        pass

    # Assert
    assert err is None


def test_validate_name_when_guest_name_is_none_should_raise_value_error():
    # Arrange
    # Act
    with pytest.raises(ValueError) as err:
        test_game = Game(
            season_id=1920,
            week=1,
            guest_name=None,
            guest_score=0,
            host_name="Host",
            host_score=0,
            is_playoff=False
        )

    # Assert
    assert isinstance(err.value, ValueError)
    assert err.value.args[0] == "guest_name is required."


def test_validate_name_when_guest_name_is_empty_should_raise_value_error():
    # Arrange
    # Act
    with pytest.raises(ValueError) as err:
        test_game = Game(
            season_id=1920,
            week=1,
            guest_name="",
            guest_score=0,
            host_name="Host",
            host_score=0,
            is_playoff=False
        )

    # Assert
    assert isinstance(err.value, ValueError)
    assert err.value.args[0] == "guest_name is required."


def test_validate_name_when_guest_name_is_not_empty_should_not_raise_value_error():
    # Arrange
    err = None

    # Act
    try:
        test_game = Game(
            season_id=1920,
            week=1,
            guest_name="Guest",
            guest_score=0,
            host_name="Host",
            host_score=0,
            is_playoff=False
        )
    except ValueError as err:
        pass

    # Assert
    assert err is None


def test_validate_name_when_host_name_is_none_should_raise_value_error():
    # Arrange
    # Act
    with pytest.raises(ValueError) as err:
        test_game = Game(
            season_id=1920,
            week=1,
            guest_name="Guest",
            guest_score=0,
            host_name=None,
            host_score=0,
            is_playoff=False
        )

    # Assert
    assert isinstance(err.value, ValueError)
    assert err.value.args[0] == "host_name is required."


def test_validate_name_when_host_name_is_empty_should_raise_value_error():
    # Arrange
    # Act
    with pytest.raises(ValueError) as err:
        test_game = Game(
            season_id=1920,
            week=1,
            guest_name="Guest",
            guest_score=0,
            host_name="",
            host_score=0,
            is_playoff=False
        )

    # Assert
    assert isinstance(err.value, ValueError)
    assert err.value.args[0] == "host_name is required."


def test_validate_name_when_host_name_is_not_empty_should_not_raise_value_error():
    # Arrange
    err = None

    # Act
    try:
        test_game = Game(
            season_id=1920,
            week=1,
            guest_name="Guest",
            guest_score=0,
            host_name="Host",
            host_score=0,
            is_playoff=False
        )
    except ValueError as err:
        pass

    # Assert
    assert err is None


def test_validate_score_when_guest_score_is_none_should_raise_value_error():
    # Arrange
    # Act
    with pytest.raises(ValueError) as err:
        test_game = Game(
            season_id=1920,
            week=1,
            guest_name="Guest",
            guest_score=None,
            host_name="Host",
            host_score=0,
            is_playoff=False
        )

    # Assert
    assert isinstance(err.value, ValueError)
    assert err.value.args[0] == "guest_score is required."


def test_validate_score_when_guest_score_is_negative_should_raise_value_error():
    # Arrange
    # Act
    with pytest.raises(ValueError) as err:
        test_game = Game(
            season_id=1920,
            week=1,
            guest_name="Guest",
            guest_score=-1,
            host_name="Host",
            host_score=0,
            is_playoff=False
        )

    # Assert
    assert isinstance(err.value, ValueError)
    assert err.value.args[0] == "guest_score cannot be negative."


def test_validate_score_when_guest_score_is_zero_should_not_raise_value_error():
    # Arrange
    err = None

    # Act
    try:
        test_game = Game(
            season_id=1920,
            week=1,
            guest_name="Guest",
            guest_score=0,
            host_name="Host",
            host_score=0,
            is_playoff=False
        )
    except ValueError as err:
        pass

    # Assert
    assert err is None


def test_validate_score_when_guest_score_is_positive_should_not_raise_value_error():
    # Arrange
    err = None

    # Act
    try:
        test_game = Game(
            season_id=1920,
            week=1,
            guest_name="Guest",
            guest_score=1,
            host_name="Host",
            host_score=0,
            is_playoff=False
        )
    except ValueError as err:
        pass

    # Assert
    assert err is None


def test_validate_score_when_host_score_is_none_should_raise_value_error():
    # Arrange
    # Act
    with pytest.raises(ValueError) as err:
        test_game = Game(
            season_id=1920,
            week=1,
            guest_name="Guest",
            guest_score=0,
            host_name="Host",
            host_score=None,
            is_playoff=False
        )

    # Assert
    assert isinstance(err.value, ValueError)
    assert err.value.args[0] == "host_score is required."


def test_validate_score_when_host_score_is_negative_should_raise_value_error():
    # Arrange
    # Act
    with pytest.raises(ValueError) as err:
        test_game = Game(
            season_id=1920,
            week=1,
            guest_name="Guest",
            guest_score=0,
            host_name="Host",
            host_score=-1,
            is_playoff=False
        )

    # Assert
    assert isinstance(err.value, ValueError)
    assert err.value.args[0] == "host_score cannot be negative."


def test_validate_score_when_host_score_is_zero_should_not_raise_value_error():
    # Arrange
    err = None

    # Act
    try:
        test_game = Game(
            season_id=1920,
            week=1,
            guest_name="Guest",
            guest_score=0,
            host_name="Host",
            host_score=0,
            is_playoff=False
        )
    except ValueError as err:
        pass

    # Assert
    assert err is None


def test_validate_score_when_host_score_is_positive_should_not_raise_value_error():
    # Arrange
    err = None

    # Act
    try:
        test_game = Game(
            season_id=1920,
            week=1,
            guest_name="Guest",
            guest_score=0,
            host_name="Host",
            host_score=1,
            is_playoff=False
        )
    except ValueError as err:
        pass

    # Assert
    assert err is None


def test_is_tie_when_guest_score_greater_than_host_score_should_return_false():
    # Arrange
    test_game = Game(
        season_id=1920,
        week=1,
        guest_name="Guest",
        guest_score=3,
        host_name="Host",
        host_score=2,
        is_playoff=False
    )

    # Act
    assert not test_game.is_tie


def test_is_tie_when_host_score_greater_than_guest_score_should_return_false():
    # Arrange
    test_game = Game(
        season_id=1920,
        week=1,
        guest_name="Guest",
        guest_score=2,
        host_name="Host",
        host_score=3,
        is_playoff=False
    )

    # Act & Assert
    assert not test_game.is_tie


def test_is_tie_when_guest_equals_host_score_should_return_true():
    # Arrange
    test_game = Game(
        season_id=1920,
        week=1,
        guest_name="Guest",
        guest_score=3,
        host_name="Host",
        host_score=3,
        is_playoff=False
    )

    # Act
    assert test_game.is_tie


def test_winner_loser_properties_when_game_is_tie_should_all_return_none():
    # Arrange
    test_game = Game(
        season_id=1920,
        week=1,
        guest_name="Guest",
        guest_score=3,
        host_name="Host",
        host_score=3,
        is_playoff=False
    )

    # Act & Assert
    assert test_game.winner_name is None
    assert test_game.winner_score is None
    assert test_game.loser_name is None
    assert test_game.loser_score is None


def test_winner_loser_properties_when_guest_score_is_greater_than_host_score_should_all_return_correct_values():
    # Arrange
    test_game = Game(
        season_id=1920,
        week=1,
        guest_name="Guest",
        guest_score=3,
        host_name="Host",
        host_score=2,
        is_playoff=False
    )

    # Act & Assert
    assert test_game.winner_name == "Guest"
    assert test_game.winner_score == 3
    assert test_game.loser_name == "Host"
    assert test_game.loser_score == 2


def test_winner_loser_properties_when_host_score_is_greater_than_guest_score_should_all_return_correct_values():
    # Arrange
    test_game = Game(
        season_id=1920,
        week=1,
        guest_name="Guest",
        guest_score=2,
        host_name="Host",
        host_score=3,
        is_playoff=False
    )

    # Act & Assert
    assert test_game.winner_name == "Host"
    assert test_game.winner_score == 3
    assert test_game.loser_name == "Guest"
    assert test_game.loser_score == 2
