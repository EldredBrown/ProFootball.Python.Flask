from unittest.mock import patch, call

import pytest

from app.data.factories import division_factory
from app.data.models.division import Division
from test_app import create_app


@pytest.fixture
def test_app():
    return create_app()


def test_create_division_when_name_not_in_kwargs_should_raise_value_error():
    # Arrange
    kwargs = {
        'league_name': "NFL",
        'conference_name': "NFC",
        'first_season_year': 1970,
        'last_season_year': None,
    }

    # Act
    with pytest.raises(ValueError) as err:
        test_division = division_factory.create_division(**kwargs)

    # Assert
    assert err.value.args[0] == "name is required."


@patch('app.data.factories.division_factory._validate_is_unique')
def test_create_division_when_name_is_in_kwargs_and_old_division_not_provided_and_kwargs_name_is_not_unique_should_raise_value_error(
        fake_validate_is_unique
):
    # Arrange
    kwargs = {
        'name': "NFC East",
        'league_name': "NFL",
        'conference_name': "NFC",
        'first_season_year': 1970,
        'last_season_year': None,
    }

    error_message = f"Division already exists with name={kwargs['name']}."
    fake_validate_is_unique.side_effect = ValueError(error_message)

    # Act
    with pytest.raises(ValueError) as err:
        test_division = division_factory.create_division(**kwargs)

    # Assert
    fake_validate_is_unique.assert_called_once_with('name', kwargs['name'], error_message=error_message)
    assert err.value.args[0] == error_message


@patch('app.data.factories.division_factory._validate_is_unique')
def test_create_division_when_name_is_in_kwargs_and_old_division_not_provided_and_kwargs_name_is_unique_should_return_division(
        fake_validate_is_unique, test_app
):
    with test_app.app_context():
        # Arrange
        kwargs = {
            'id': 1,
            'name': "NFC East",
            'league_name': "NFL",
            'conference_name': "NFC",
            'first_season_year': 1970,
            'last_season_year': None,
        }

        fake_validate_is_unique.return_value = None

        # Act
        try:
            test_division = division_factory.create_division(**kwargs)
        except ValueError:
            assert False

    # Assert
    error_message = f"Division already exists with name={kwargs['name']}."
    fake_validate_is_unique.assert_called_once_with('name', kwargs['name'], error_message=error_message)
    assert isinstance(test_division, Division)
    assert test_division.id == kwargs['id']
    assert test_division.name == kwargs['name']
    assert test_division.league_name == kwargs['league_name']
    assert test_division.conference_name == kwargs['conference_name']
    assert test_division.first_season_year == kwargs['first_season_year']
    assert test_division.last_season_year == kwargs['last_season_year']


@patch('app.data.factories.division_factory._validate_is_unique')
def test_create_division_when_name_is_in_kwargs_and_old_division_provided_and_kwargs_name_equals_old_division_name_should_not_validate_unique_key_values_and_return_division(
        fake_validate_is_unique, test_app
):
    with test_app.app_context():
        # Arrange
        kwargs = {
            'id': 1,
            'name': "NFC East",
            'league_name': "NFL",
            'conference_name': "NFC",
            'first_season_year': 1970,
            'last_season_year': None,
        }

        old_division = Division(
            id=1, name="NFC East", league_name="NFL", conference_name="NFC",
            first_season_year=1970, last_season_year=None
        )

        # Act
        try:
            test_division = division_factory.create_division(old_division, **kwargs)
        except ValueError:
            assert False

    # Assert
    fake_validate_is_unique.assert_not_called()
    assert isinstance(test_division, Division)
    assert test_division.id == kwargs['id']
    assert test_division.name == kwargs['name']
    assert test_division.league_name == kwargs['league_name']
    assert test_division.conference_name == kwargs['conference_name']
    assert test_division.first_season_year == kwargs['first_season_year']
    assert test_division.last_season_year == kwargs['last_season_year']


@patch('app.data.factories.division_factory._validate_is_unique')
def test_create_division_when_name_is_in_kwargs_and_old_division_provided_and_kwargs_name_does_not_equal_old_division_name_and_kwargs_name_is_unique_should_validate_unique_key_values_and_return_division(
        fake_validate_is_unique, test_app
):
    with test_app.app_context():
        # Arrange
        kwargs = {
            'id': 1,
            'name': "NFC Central",
            'league_name': "NFL",
            'conference_name': "NFC",
            'first_season_year': 1970,
            'last_season_year': None,
        }

        fake_validate_is_unique.return_value = None

        old_division = Division(
            id=1, name="NFC East", league_name="NFL", conference_name="NFC",
            first_season_year=1970, last_season_year=None
        )

        # Act
        try:
            test_division = division_factory.create_division(old_division, **kwargs)
        except ValueError:
            assert False

    # Assert
    error_message = f"Division already exists with name={kwargs['name']}."
    fake_validate_is_unique.assert_called_once_with('name', kwargs['name'], error_message=error_message)
    assert isinstance(test_division, Division)
    assert test_division.id == kwargs['id']
    assert test_division.name == kwargs['name']
    assert test_division.league_name == kwargs['league_name']
    assert test_division.conference_name == kwargs['conference_name']
    assert test_division.first_season_year == kwargs['first_season_year']
    assert test_division.last_season_year == kwargs['last_season_year']


@patch('app.data.factories.division_factory._validate_is_unique')
def test_create_division_when_name_is_in_kwargs_and_old_division_provided_and_kwargs_name_does_not_equal_old_division_name_and_kwargs_name_is_not_unique_should_validate_unique_key_values_and_raise_value_error(
        fake_validate_is_unique, test_app
):
    with test_app.app_context():
        # Arrange
        kwargs = {
            'id': 1,
            'name': "NFC Central",
            'league_name': "NFL",
            'conference_name': "NFC",
            'first_season_year': 1970,
            'last_season_year': None,
        }

        error_message = f"Division already exists with name={kwargs['name']}."
        fake_validate_is_unique.side_effect = ValueError(error_message)

        old_division = Division(
            id=1, name="NFC East", league_name="NFL", conference_name="NFC",
            first_season_year=1970, last_season_year=None
        )

        # Act
        with pytest.raises(ValueError) as err:
            test_division = division_factory.create_division(old_division, **kwargs)

    # Assert
    fake_validate_is_unique.assert_called_once_with('name', kwargs['name'], error_message=error_message)
    assert err.value.args[0] == error_message


@patch('app.data.factories.division_factory.Division')
def test_validate_is_unique_when_name_is_unique_should_not_raise_value_error(fake_division):
    # Arrange
    fake_division.query.filter_by.return_value.first.return_value = None

    # Act
    result = division_factory._validate_is_unique('name', "NFC East")

    # Assert
    assert result is None


@patch('app.data.factories.division_factory.Division')
def test_validate_is_unique_when_name_is_not_unique_and_error_message_is_not_provided_should_raise_value_error_with_default_error_message(fake_division):
    # Arrange
    fake_division.query.filter_by.return_value.first.return_value = Division()

    # Act
    with pytest.raises(ValueError) as err:
        result = division_factory._validate_is_unique('name', "NFC East")

    # Assert
    assert err.value.args[0] == "name must be unique."


@patch('app.data.factories.division_factory.Division')
def test_validate_is_unique_when_name_is_not_unique_and_error_message_is_provided_should_raise_value_error_with_provided_error_message(fake_division):
    # Arrange
    fake_division.query.filter_by.return_value.first.return_value = Division()

    error_message = f"Division already exists with name=NFC East."

    # Act
    with pytest.raises(ValueError) as err:
        result = division_factory._validate_is_unique('name', "NFC East", error_message=error_message)

    # Assert
    assert err.value.args[0] == error_message
