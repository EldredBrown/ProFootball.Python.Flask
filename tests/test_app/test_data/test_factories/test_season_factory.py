from unittest.mock import patch

import pytest

from app.data.factories import season_factory
from app.data.models.season import Season


def test_create_season_when_year_not_in_kwargs_should_raise_value_error():
    # Arrange
    kwargs = {
        'num_of_weeks_scheduled': 13,
    }

    # Act
    with pytest.raises(ValueError) as err:
        test_season = season_factory.create_season(**kwargs)

    # Assert
    assert err.value.args[0] == "Year is required."


@patch('app.data.factories.season_factory._validate_is_unique')
def test_create_season_when_year_is_in_kwargs_and_old_season_not_provided_and_kwargs_year_is_not_unique_should_raise_value_error(
        fake_validate_is_unique
):
    # Arrange
    kwargs = {
        'year': 1920,
        'num_of_weeks_scheduled': 13,
    }

    error_message = f"Season already exists with year={kwargs['year']}."
    fake_validate_is_unique.side_effect = ValueError(error_message)

    # Act
    with pytest.raises(ValueError) as err:
        test_season = season_factory.create_season(**kwargs)

    # Assert
    fake_validate_is_unique.assert_called_once_with('year', kwargs['year'], error_message=error_message)
    assert err.value.args[0] == error_message


@patch('app.data.factories.season_factory._validate_is_unique')
def test_create_season_when_year_is_in_kwargs_and_old_season_not_provided_and_kwargs_year_is_unique_should_return_season(
        fake_validate_is_unique
):
    # Arrange
    kwargs = {
        'id': 1,
        'year': 1920,
        'num_of_weeks_scheduled': 13,
        'num_of_weeks_completed': 0,
    }

    fake_validate_is_unique.return_value = None

    # Act
    try:
        test_season = season_factory.create_season(**kwargs)
    except ValueError:
        assert False

    # Assert
    error_message = f"Season already exists with year={kwargs['year']}."
    fake_validate_is_unique.assert_called_once_with('year', kwargs['year'], error_message=error_message)
    assert isinstance(test_season, Season)
    assert test_season.id == kwargs['id']
    assert test_season.year == kwargs['year']
    assert test_season.num_of_weeks_scheduled == kwargs['num_of_weeks_scheduled']
    assert test_season.num_of_weeks_completed == kwargs['num_of_weeks_completed']


@patch('app.data.factories.season_factory._validate_is_unique')
def test_create_season_when_year_is_in_kwargs_and_old_season_provided_and_kwargs_year_equals_old_season_year_should_not_validate_unique_key_values_and_return_season(
        fake_validate_is_unique
):
    # Arrange
    kwargs = {
        'id': 1,
        'year': 1920,
        'num_of_weeks_scheduled': 13,
        'num_of_weeks_completed': 0,
    }

    old_season = Season(id=1, year=1920, num_of_weeks_scheduled=13, num_of_weeks_completed=0)

    # Act
    try:
        test_season = season_factory.create_season(old_season, **kwargs)
    except ValueError:
        assert False

    # Assert
    fake_validate_is_unique.assert_not_called()
    assert isinstance(test_season, Season)
    assert test_season.id == kwargs['id']
    assert test_season.year == kwargs['year']
    assert test_season.num_of_weeks_scheduled == kwargs['num_of_weeks_scheduled']
    assert test_season.num_of_weeks_completed == kwargs['num_of_weeks_completed']


@patch('app.data.factories.season_factory._validate_is_unique')
def test_create_season_when_year_is_in_kwargs_and_old_season_provided_and_kwargs_year_does_not_equal_old_season_year_and_kwargs_year_is_unique_should_validate_unique_key_values_and_return_season(
        fake_validate_is_unique
):
    # Arrange
    kwargs = {
        'id': 1,
        'year': 1920,
        'num_of_weeks_scheduled': 13,
        'num_of_weeks_completed': 0,
    }

    fake_validate_is_unique.return_value = None

    old_season = Season(id=2, year=1921, num_of_weeks_scheduled=13, num_of_weeks_completed=0)

    # Act
    try:
        test_season = season_factory.create_season(old_season, **kwargs)
    except ValueError:
        assert False

    # Assert
    error_message = f"Season already exists with year={kwargs['year']}."
    fake_validate_is_unique.assert_called_once_with('year', kwargs['year'], error_message=error_message)
    assert isinstance(test_season, Season)
    assert test_season.id == kwargs['id']
    assert test_season.year == kwargs['year']
    assert test_season.num_of_weeks_scheduled == kwargs['num_of_weeks_scheduled']
    assert test_season.num_of_weeks_completed == kwargs['num_of_weeks_completed']


@patch('app.data.factories.season_factory._validate_is_unique')
def test_create_season_when_year_is_in_kwargs_and_old_season_provided_and_kwargs_year_does_not_equal_old_season_year_and_kwargs_year_is_not_unique_should_validate_unique_key_values_and_raise_value_error(
        fake_validate_is_unique
):
    # Arrange
    kwargs = {
        'id': 1,
        'year': 1920,
        'num_of_weeks_scheduled': 13,
        'num_of_weeks_completed': 0,
    }

    error_message = f"Season already exists with year={kwargs['year']}."
    fake_validate_is_unique.side_effect = ValueError(error_message)

    old_season = Season(id=2, year=1921, num_of_weeks_scheduled=13, num_of_weeks_completed=0)

    # Act
    with pytest.raises(ValueError) as err:
        test_season = season_factory.create_season(old_season, **kwargs)

    # Assert
    fake_validate_is_unique.assert_called_once_with('year', kwargs['year'], error_message=error_message)
    assert err.value.args[0] == error_message


@patch('app.data.factories.season_factory.Season')
def test_validate_is_unique_when_year_is_unique_should_not_raise_value_error(fake_season):
    # Arrange
    fake_season.query.filter_by.return_value.first.return_value = None

    # Act
    result = season_factory._validate_is_unique('year', 1920)

    # Assert
    assert result is None


@patch('app.data.factories.season_factory.Season')
def test_validate_is_unique_when_year_is_not_unique_and_error_message_is_not_provided_should_raise_value_error_with_default_error_message(fake_season):
    # Arrange
    fake_season.query.filter_by.return_value.first.return_value = Season()

    # Act
    with pytest.raises(ValueError) as err:
        result = season_factory._validate_is_unique('year', 1920)

    # Assert
    assert err.value.args[0] == "year must be unique."


@patch('app.data.factories.season_factory.Season')
def test_validate_is_unique_when_year_is_not_unique_and_error_message_is_provided_should_raise_value_error_with_provided_error_message(fake_season):
    # Arrange
    fake_season.query.filter_by.return_value.first.return_value = Season()

    error_message = f"Season already exists with year=1920."

    # Act
    with pytest.raises(ValueError) as err:
        result = season_factory._validate_is_unique('year', 1920, error_message=error_message)

    # Assert
    assert err.value.args[0] == error_message
