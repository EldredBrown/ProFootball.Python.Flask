import pytest

from app.data.models.season import Season


def test_validate_not_empty_when_year_is_none_should_raise_value_error():
    # Arrange
    # Act
    with pytest.raises(ValueError) as err:
        test_season = Season(year=None)

    # Assert
    assert isinstance(err.value, ValueError)
    assert err.value.args[0] == "Year is required."


def test_validate_not_empty_when_year_is_zero_should_not_raise_value_error():
    # Arrange
    err = None

    # Act
    try:
        test_season = Season(year=0)
    except ValueError as err:
        pass

    # Assert
    assert err is None


def test_validate_not_empty_when_year_is_greater_than_zero_should_not_raise_value_error():
    # Arrange
    err = None

    # Act
    try:
        test_season = Season(year=1)
    except ValueError as err:
        pass

    # Assert
    assert err is None
