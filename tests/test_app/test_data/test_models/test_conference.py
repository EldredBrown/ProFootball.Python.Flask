import pytest

from app.data.models.conference import Conference


def test_validate_not_empty_when_short_name_is_none_should_raise_value_error():
    # Arrange
    # Act
    with pytest.raises(ValueError) as err:
        test_conference = Conference(short_name=None)

    # Assert
    assert isinstance(err.value, ValueError)
    assert err.value.args[0] == "short_name is required."


def test_validate_not_empty_when_short_name_is_empty_should_raise_value_error():
    # Arrange
    # Act
    with pytest.raises(ValueError) as err:
        test_conference = Conference(short_name="")

    # Assert
    assert isinstance(err.value, ValueError)
    assert err.value.args[0] == "short_name is required."


def test_validate_not_empty_when_short_name_is_not_empty_should_not_raise_value_error():
    # Arrange
    err = None

    # Act
    try:
        test_conference = Conference(short_name="C")
    except ValueError as err:
        pass

    # Assert
    assert err is None


def test_validate_not_empty_when_long_name_is_none_should_raise_value_error():
    # Arrange
    # Act
    with pytest.raises(ValueError) as err:
        test_conference = Conference(short_name="C", long_name=None)

    # Assert
    assert isinstance(err.value, ValueError)
    assert err.value.args[0] == "long_name is required."


def test_validate_not_empty_when_long_name_is_empty_should_raise_value_error():
    # Arrange
    # Act
    with pytest.raises(ValueError) as err:
        test_conference = Conference(short_name="C", long_name="")

    # Assert
    assert isinstance(err.value, ValueError)
    assert err.value.args[0] == "long_name is required."


def test_validate_not_empty_when_long_name_is_not_empty_should_not_raise_value_error():
    # Arrange
    err = None

    # Act
    try:
        test_conference = Conference(short_name="C", long_name="Conference")
    except ValueError as err:
        pass

    # Assert
    assert err is None


def test_validate_not_empty_when_league_id_is_none_should_raise_value_error():
    # Arrange
    # Act
    with pytest.raises(ValueError) as err:
        test_conference = Conference(
            short_name="C",
            long_name="Conference",
            league_id=None
        )

    # Assert
    assert isinstance(err.value, ValueError)
    assert err.value.args[0] == "league_id is required."


def test_validate_not_empty_when_league_id_is_zero_should_not_raise_value_error():
    # Arrange
    err = None

    # Act
    try:
        test_conference = Conference(
            short_name="C",
            long_name="Conference",
            league_id=0
        )
    except ValueError as err:
        pass

    # Assert
    assert err is None


def test_validate_not_empty_when_league_id_is_greater_than_zero_should_not_raise_value_error():
    # Arrange
    err = None

    # Act
    try:
        test_conference = Conference(
            short_name="C",
            long_name="Conference",
            league_id=1
        )
    except ValueError as err:
        pass

    # Assert
    assert err is None


def test_validate_not_empty_when_first_season_id_is_none_should_raise_value_error():
    # Arrange
    # Act
    with pytest.raises(ValueError) as err:
        test_conference = Conference(
            short_name="C",
            long_name="Conference",
            league_id=1,
            first_season_id=None
        )

    # Assert
    assert isinstance(err.value, ValueError)
    assert err.value.args[0] == "first_season_id is required."


def test_validate_not_empty_when_first_season_id_is_zero_should_not_raise_value_error():
    # Arrange
    err = None

    # Act
    try:
        test_conference = Conference(
            short_name="C",
            long_name="Conference",
            league_id=1,
            first_season_id=0
        )
    except ValueError as err:
        pass

    # Assert
    assert err is None


def test_validate_not_empty_when_first_season_id_is_greater_than_zero_should_not_raise_value_error():
    # Arrange
    err = None

    # Act
    try:
        test_conference = Conference(
            short_name="C",
            long_name="Conference",
            league_id=1,
            first_season_id=1
        )
    except ValueError as err:
        pass

    # Assert
    assert err is None
