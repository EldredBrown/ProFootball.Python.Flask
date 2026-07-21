import pytest

from app.data.factories import season_factory


def test_create_season_when_year_not_in_kwargs_should_raise_value_error():
    # Arrange
    kwargs = {}

    # Act
    with pytest.raises(ValueError) as err:
        _ = season_factory.create_season(**kwargs)

    # Assert
    assert err.value.args[0] == "Year is required."


def test_create_season_when_year_is_in_kwargs_should_not_raise_value_error():
    # Arrange
    kwargs = {'year': 1920}

    # Act
    try:
        _ = season_factory.create_season(**kwargs)
    except ValueError:
        # Assert
        assert False
