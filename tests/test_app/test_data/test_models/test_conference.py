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
        test_conference = Conference(short_name="NFC")
    except ValueError as err:
        pass

    # Assert
    assert err is None


def test_validate_not_empty_when_long_name_is_none_should_raise_value_error():
    # Arrange
    # Act
    with pytest.raises(ValueError) as err:
        test_conference = Conference(short_name="NFC", long_name=None)

    # Assert
    assert isinstance(err.value, ValueError)
    assert err.value.args[0] == "long_name is required."


def test_validate_not_empty_when_long_name_is_empty_should_raise_value_error():
    # Arrange
    # Act
    with pytest.raises(ValueError) as err:
        test_conference = Conference(short_name="NFC", long_name="")

    # Assert
    assert isinstance(err.value, ValueError)
    assert err.value.args[0] == "long_name is required."


def test_validate_not_empty_when_long_name_is_not_empty_should_not_raise_value_error():
    # Arrange
    err = None

    # Act
    try:
        test_conference = Conference(short_name="NFC", long_name="National Football Conference")
    except ValueError as err:
        pass

    # Assert
    assert err is None


def test_validate_not_empty_when_league_name_is_none_should_raise_value_error():
    # Arrange
    # Act
    with pytest.raises(ValueError) as err:
        test_conference = Conference(short_name="NFC", long_name="National Football Conference", league_name=None)

    # Assert
    assert isinstance(err.value, ValueError)
    assert err.value.args[0] == "league_name is required."


def test_validate_not_empty_when_league_name_is_empty_should_raise_value_error():
    # Arrange
    # Act
    with pytest.raises(ValueError) as err:
        test_conference = Conference(short_name="NFC", long_name="National Football Conference", league_name="")

    # Assert
    assert isinstance(err.value, ValueError)
    assert err.value.args[0] == "league_name is required."


def test_validate_not_empty_when_league_name_is_not_empty_should_not_raise_value_error():
    # Arrange
    err = None

    # Act
    try:
        test_conference = Conference(short_name="NFC", long_name="National Football Conference", league_name="NFL")
    except ValueError as err:
        pass

    # Assert
    assert err is None


def test_validate_not_empty_when_first_season_year_is_none_should_raise_value_error():
    # Arrange
    # Act
    with pytest.raises(ValueError) as err:
        test_conference = Conference(
            short_name="NFC", long_name="National Football Conference", league_name="NFL", first_season_year=None
        )

    # Assert
    assert isinstance(err.value, ValueError)
    assert err.value.args[0] == "first_season_year is required."


def test_validate_not_empty_when_first_season_year_is_zero_should_not_raise_value_error():
    # Arrange
    err = None

    # Act
    try:
        test_conference = Conference(
            short_name="NFC", long_name="National Football Conference", league_name="NFL", first_season_year=0
        )
    except ValueError as err:
        pass

    # Assert
    assert err is None


def test_validate_not_empty_when_first_season_year_is_greater_than_zero_should_not_raise_value_error():
    # Arrange
    err = None

    # Act
    try:
        test_conference = Conference(
            short_name="NFC", long_name="National Football Conference", league_name="NFL", first_season_year=1
        )
    except ValueError as err:
        pass

    # Assert
    assert err is None
