import pytest

from app.data.models.division import Division


def test_validate_not_empty_when_name_is_none_should_raise_value_error():
    # Arrange
    # Act
    with pytest.raises(ValueError) as err:
        test_division = Division(name=None)

    # Assert
    assert isinstance(err.value, ValueError)
    assert err.value.args[0] == "name is required."


def test_validate_not_empty_when_name_is_empty_should_raise_value_error():
    # Arrange
    # Act
    with pytest.raises(ValueError) as err:
        test_division = Division(name="")

    # Assert
    assert isinstance(err.value, ValueError)
    assert err.value.args[0] == "name is required."


def test_validate_not_empty_when_name_is_not_empty_should_not_raise_value_error():
    # Arrange
    err = None

    # Act
    try:
        test_division = Division(name="NFC East")
    except ValueError as err:
        pass

    # Assert
    assert err is None


def test_validate_not_empty_when_league_name_is_none_should_raise_value_error():
    # Arrange
    # Act
    with pytest.raises(ValueError) as err:
        test_division = Division(name="NFC East", league_name=None)

    # Assert
    assert isinstance(err.value, ValueError)
    assert err.value.args[0] == "league_name is required."


def test_validate_not_empty_when_league_name_is_empty_should_raise_value_error():
    # Arrange
    # Act
    with pytest.raises(ValueError) as err:
        test_division = Division(name="NFC East", league_name="")

    # Assert
    assert isinstance(err.value, ValueError)
    assert err.value.args[0] == "league_name is required."


def test_validate_not_empty_when_league_name_is_not_empty_should_not_raise_value_error():
    # Arrange
    err = None

    # Act
    try:
        test_division = Division(name="NFC East", league_name="NFL")
    except ValueError as err:
        pass

    # Assert
    assert err is None


def test_validate_not_empty_when_first_season_year_is_none_should_raise_value_error():
    # Arrange
    # Act
    with pytest.raises(ValueError) as err:
        test_division = Division(
            name="NFC East", league_name="NFL", first_season_year=None
        )

    # Assert
    assert isinstance(err.value, ValueError)
    assert err.value.args[0] == "first_season_year is required."


def test_validate_not_empty_when_first_season_year_is_zero_should_not_raise_value_error():
    # Arrange
    err = None

    # Act
    try:
        test_division = Division(
            name="NFC East", league_name="NFL", first_season_year=0
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
        test_division = Division(
            name="NFC East", league_name="NFL", first_season_year=1
        )
    except ValueError as err:
        pass

    # Assert
    assert err is None
