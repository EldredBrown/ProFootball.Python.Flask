import pytest

from app.data.models.season import Season


def test_validate_not_empty_when_year_is_none_should_raise_value_error():
    # Arrange
    # Act
    with pytest.raises(ValueError) as err:
        _ = Season(year=None)

    # Assert
    assert isinstance(err.value, ValueError)
    assert err.value.args[0] == "Year is required."


def test_validate_not_empty_when_year_is_less_than_1920_should_not_raise_value_error():
    # Arrange
    # Act
    try:
        _ = Season(year=1919)
    except ValueError:
        # Assert
        assert False

    assert True


def test_validate_not_empty_when_year_is_greater_than_or_equal_to_1920_should_not_raise_value_error():
    # Arrange
    # Act
    try:
        _ = Season(year=1920)
    except ValueError:
        # Assert
        assert False

    assert True
