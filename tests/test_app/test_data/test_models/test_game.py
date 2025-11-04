import pytest

from app.data.models.game import Game


def test_validate_not_empty_when_season_year_is_none_should_raise_value_error():
    # Arrange
    # Act
    with pytest.raises(ValueError) as err:
        test_game = Game(
            season_year=None,
            week=1,
            guest_name="St. Paul Ideals",
            guest_score=0,
            host_name="Rock Island Independents",
            host_score=48,
            is_playoff=False
        )

    # Assert
    assert isinstance(err.value, ValueError)
    assert err.value.args[0] == "season_year is required."


def test_validate_not_empty_when_season_year_is_zero_should_not_raise_value_error():
    # Arrange
    err = None

    # Act
    try:
        test_game = Game(
            season_year=0,
            week=1,
            guest_name="St. Paul Ideals",
            guest_score=0,
            host_name="Rock Island Independents",
            host_score=48,
            is_playoff=False
        )
    except ValueError as err:
        pass

    # Assert
    assert err is None


def test_validate_not_empty_when_season_year_is_greater_than_zero_should_not_raise_value_error():
    # Arrange
    err = None

    # Act
    try:
        test_game = Game(
            season_year=1,
            week=1,
            guest_name="St. Paul Ideals",
            guest_score=0,
            host_name="Rock Island Independents",
            host_score=48,
            is_playoff=False
        )
    except ValueError as err:
        pass

    # Assert
    assert err is None


def test_validate_not_empty_when_week_is_none_should_raise_value_error():
    # Arrange
    # Act
    with pytest.raises(ValueError) as err:
        test_game = Game(
            season_year=1920,
            week=None,
            guest_name="St. Paul Ideals",
            guest_score=0,
            host_name="Rock Island Independents",
            host_score=48,
            is_playoff=False
        )

    # Assert
    assert isinstance(err.value, ValueError)
    assert err.value.args[0] == "week is required."


def test_validate_not_empty_when_week_is_zero_should_not_raise_value_error():
    # Arrange
    err = None

    # Act
    try:
        test_game = Game(
            season_year=1920,
            week=0,
            guest_name="St. Paul Ideals",
            guest_score=0,
            host_name="Rock Island Independents",
            host_score=48,
            is_playoff=False
        )
    except ValueError as err:
        pass

    # Assert
    assert err is None


def test_validate_not_empty_when_week_is_greater_than_zero_should_not_raise_value_error():
    # Arrange
    err = None

    # Act
    try:
        test_game = Game(
            season_year=1920,
            week=1,
            guest_name="St. Paul Ideals",
            guest_score=0,
            host_name="Rock Island Independents",
            host_score=48,
            is_playoff=False
        )
    except ValueError as err:
        pass

    # Assert
    assert err is None


def test_validate_not_empty_when_guest_name_is_none_should_raise_value_error():
    # Arrange
    # Act
    with pytest.raises(ValueError) as err:
        test_game = Game(
            season_year=1920,
            week=1,
            guest_name=None,
            guest_score=0,
            host_name="Rock Island Independents",
            host_score=48,
            is_playoff=False
        )

    # Assert
    assert isinstance(err.value, ValueError)
    assert err.value.args[0] == "guest_name is required."


def test_validate_not_empty_when_guest_name_is_empty_should_raise_value_error():
    # Arrange
    # Act
    with pytest.raises(ValueError) as err:
        test_game = Game(
            season_year=1920,
            week=1,
            guest_name="",
            guest_score=0,
            host_name="Rock Island Independents",
            host_score=48,
            is_playoff=False
        )

    # Assert
    assert isinstance(err.value, ValueError)
    assert err.value.args[0] == "guest_name is required."


def test_validate_not_empty_when_guest_name_is_not_empty_should_not_raise_value_error():
    # Arrange
    err = None

    # Act
    try:
        test_game = Game(
            season_year=1920,
            week=1,
            guest_name="Guest",
            guest_score=0,
            host_name="Rock Island Independents",
            host_score=48,
            is_playoff=False
        )
    except ValueError as err:
        pass

    # Assert
    assert err is None


def test_validate_not_empty_when_guest_score_is_none_should_raise_value_error():
    # Arrange
    # Act
    with pytest.raises(ValueError) as err:
        test_game = Game(
            season_year=1920,
            week=1,
            guest_name="St. Paul Ideals",
            guest_score=None,
            host_name="Rock Island Independents",
            host_score=48,
            is_playoff=False
        )

    # Assert
    assert isinstance(err.value, ValueError)
    assert err.value.args[0] == "guest_score is required."


def test_validate_not_empty_when_guest_score_is_zero_should_not_raise_value_error():
    # Arrange
    err = None

    # Act
    try:
        test_game = Game(
            season_year=1920,
            week=1,
            guest_name="St. Paul Ideals",
            guest_score=0,
            host_name="Rock Island Independents",
            host_score=48,
            is_playoff=False
        )
    except ValueError as err:
        pass

    # Assert
    assert err is None


def test_validate_not_empty_when_guest_score_is_greater_than_zero_should_not_raise_value_error():
    # Arrange
    err = None

    # Act
    try:
        test_game = Game(
            season_year=1920,
            week=1,
            guest_name="St. Paul Ideals",
            guest_score=1,
            host_name="Rock Island Independents",
            host_score=48,
            is_playoff=False
        )
    except ValueError as err:
        pass

    # Assert
    assert err is None


def test_validate_not_empty_when_host_name_is_none_should_raise_value_error():
    # Arrange
    # Act
    with pytest.raises(ValueError) as err:
        test_game = Game(
            season_year=1920,
            week=1,
            guest_name="St. Paul Ideals",
            guest_score=0,
            host_name=None,
            host_score=48,
            is_playoff=False
        )

    # Assert
    assert isinstance(err.value, ValueError)
    assert err.value.args[0] == "host_name is required."


def test_validate_not_empty_when_host_name_is_empty_should_raise_value_error():
    # Arrange
    # Act
    with pytest.raises(ValueError) as err:
        test_game = Game(
            season_year=1920,
            week=1,
            guest_name="St. Paul Ideals",
            guest_score=0,
            host_name="",
            host_score=48,
            is_playoff=False
        )

    # Assert
    assert isinstance(err.value, ValueError)
    assert err.value.args[0] == "host_name is required."


def test_validate_not_empty_when_host_name_is_not_empty_should_not_raise_value_error():
    # Arrange
    err = None

    # Act
    try:
        test_game = Game(
            season_year=1920,
            week=1,
            guest_name="St. Paul Ideals",
            guest_score=0,
            host_name="Host",
            host_score=48,
            is_playoff=False
        )
    except ValueError as err:
        pass

    # Assert
    assert err is None


def test_validate_not_empty_when_host_score_is_none_should_raise_value_error():
    # Arrange
    # Act
    with pytest.raises(ValueError) as err:
        test_game = Game(
            season_year=1920,
            week=1,
            guest_name="St. Paul Ideals",
            guest_score=0,
            host_name="Rock Island Independents",
            host_score=None,
            is_playoff=False
        )

    # Assert
    assert isinstance(err.value, ValueError)
    assert err.value.args[0] == "host_score is required."


def test_validate_not_empty_when_host_score_is_zero_should_not_raise_value_error():
    # Arrange
    err = None

    # Act
    try:
        test_game = Game(
            season_year=1920,
            week=1,
            guest_name="St. Paul Ideals",
            guest_score=0,
            host_name="Rock Island Independents",
            host_score=0,
            is_playoff=False
        )
    except ValueError as err:
        pass

    # Assert
    assert err is None


def test_validate_not_empty_when_host_score_is_greater_than_zero_should_not_raise_value_error():
    # Arrange
    err = None

    # Act
    try:
        test_game = Game(
            season_year=1920,
            week=1,
            guest_name="St. Paul Ideals",
            guest_score=0,
            host_name="Rock Island Independents",
            host_score=1,
            is_playoff=False
        )
    except ValueError as err:
        pass

    # Assert
    assert err is None


def test_validate_not_empty_when_is_playoff_is_none_should_raise_value_error():
    # Arrange
    # Act
    with pytest.raises(ValueError) as err:
        test_game = Game(
            season_year=1920,
            week=1,
            guest_name="St. Paul Ideals",
            guest_score=0,
            host_name="Rock Island Independents",
            host_score=48,
            is_playoff=None
        )

    # Assert
    assert isinstance(err.value, ValueError)
    assert err.value.args[0] == "is_playoff is required."


def test_validate_not_empty_when_is_playoff_is_not_none_should_not_raise_value_error():
    # Arrange
    err = None

    # Act
    try:
        test_game = Game(
            season_year=1920,
            week=1,
            guest_name="St. Paul Ideals",
            guest_score=0,
            host_name="Rock Island Independents",
            host_score=48,
            is_playoff=False
        )
    except ValueError as err:
        pass

    # Assert
    assert err is None


def test_decide_winner_and_loser_when_host_score_greater_than_guest_score_should_declare_host_the_winner_and_guest_the_loser():
    # Arrange
    test_game = Game(
        season_year=1920,
        week=1,
        guest_name="Guest",
        guest_score=1,
        host_name="Host",
        host_score=2,
        is_playoff=False
    )

    # Act
    test_game.decide_winner_and_loser()

    # Assert
    assert test_game.winner_name == test_game.host_name
    assert test_game.winner_score == test_game.host_score
    assert test_game.loser_name == test_game.guest_name
    assert test_game.loser_score == test_game.guest_score


def test_decide_winner_and_loser_when_guest_score_greater_than_host_score_should_declare_guest_the_winner_and_host_the_loser():
    # Arrange
    test_game = Game(
        season_year=1920,
        week=1,
        guest_name="Guest",
        guest_score=2,
        host_name="Host",
        host_score=1,
        is_playoff=False
    )

    # Act
    test_game.decide_winner_and_loser()

    # Assert
    assert test_game.winner_name == test_game.guest_name
    assert test_game.winner_score == test_game.guest_score
    assert test_game.loser_name == test_game.host_name
    assert test_game.loser_score == test_game.host_score


def test_decide_winner_and_loser_when_guest_score_equals_host_score_should_declare_none_the_winner_and_none_the_loser():
    # Arrange
    test_game = Game(
        season_year=1920,
        week=1,
        guest_name="Guest",
        guest_score=2,
        host_name="Host",
        host_score=2,
        is_playoff=False
    )

    # Act
    test_game.decide_winner_and_loser()

    # Assert
    assert test_game.winner_name is None
    assert test_game.winner_score is None
    assert test_game.loser_name is None
    assert test_game.loser_score is None


def test_is_tie_when_host_score_greater_than_guest_score_should_return_false():
    # Arrange
    test_game = Game(
        season_year=1920,
        week=1,
        guest_name="Guest",
        guest_score=1,
        host_name="Host",
        host_score=2,
        is_playoff=False
    )

    # Act
    is_tie = test_game.is_tie()

    # Assert
    assert not is_tie


def test_is_tie_when_guest_score_greater_than_host_score_should_return_false():
    # Arrange
    test_game = Game(
        season_year=1920,
        week=1,
        guest_name="Guest",
        guest_score=2,
        host_name="Host",
        host_score=1,
        is_playoff=False
    )

    # Act
    is_tie = test_game.is_tie()

    # Assert
    assert not is_tie


def test_is_tie_when_guest_equals_host_score_should_return_true():
    # Arrange
    test_game = Game(
        season_year=1920,
        week=1,
        guest_name="Guest",
        guest_score=2,
        host_name="Host",
        host_score=2,
        is_playoff=False
    )

    # Act
    is_tie = test_game.is_tie()

    # Assert
    assert is_tie
