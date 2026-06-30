import pytest

from app.data.models.team import Team


def test_validate_not_empty_when_name_is_none_should_raise_value_error():
    # Arrange
    # Act
    with pytest.raises(ValueError) as err:
        test_team = Team(name=None)

    # Assert
    assert isinstance(err.value, ValueError)
    assert err.value.args[0] == "name is required."


def test_validate_not_empty_when_name_is_empty_should_raise_value_error():
    # Arrange
    # Act
    with pytest.raises(ValueError) as err:
        test_team = Team(name="")

    # Assert
    assert isinstance(err.value, ValueError)
    assert err.value.args[0] == "name is required."


def test_validate_not_empty_when_name_is_not_empty_should_not_raise_value_error():
    # Arrange
    err = None

    # Act
    try:
        test_team = Team(name="Team")
    except ValueError as err:
        pass

    # Assert
    assert err is None
