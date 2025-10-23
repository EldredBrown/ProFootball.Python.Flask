from unittest.mock import patch

import pytest

from app.data.factories import team_factory
from app.data.models.team import Team
from test_app import create_app


@pytest.fixture
def test_app():
    return create_app()


def test_create_team_when_name_not_in_kwargs_should_raise_value_error():
    # Arrange
    kwargs = {}

    # Act
    with pytest.raises(ValueError) as err:
        test_team = team_factory.create_team(**kwargs)

    # Assert
    assert err.value.args[0] == "name is required."


@patch('app.data.factories.team_factory._validate_is_unique')
def test_create_team_when_name_is_in_kwargs_and_old_team_not_provided_and_kwargs_name_is_not_unique_should_raise_value_error(
        fake_validate_is_unique
):
    # Arrange
    kwargs = {
        'name': "Chicago Cardinals",
    }

    error_message = f"Team already exists with name={kwargs['name']}."
    fake_validate_is_unique.side_effect = ValueError(error_message)

    # Act
    with pytest.raises(ValueError) as err:
        test_team = team_factory.create_team(**kwargs)

    # Assert
    fake_validate_is_unique.assert_called_once_with('name', kwargs['name'], error_message=error_message)
    assert err.value.args[0] == error_message


@patch('app.data.factories.team_factory._validate_is_unique')
def test_create_team_when_name_is_in_kwargs_and_old_team_not_provided_and_kwargs_name_is_unique_should_return_team(
        fake_validate_is_unique, test_app
):
    with test_app.app_context():
        # Arrange
        kwargs = {
            'id': 1,
            'name': "Chicago Cardinals",
        }

        fake_validate_is_unique.return_value = None

        # Act
        try:
            test_team = team_factory.create_team(**kwargs)
        except ValueError:
            assert False

    # Assert
    error_message = f"Team already exists with name={kwargs['name']}."
    fake_validate_is_unique.assert_called_once_with('name', kwargs['name'], error_message=error_message)
    assert isinstance(test_team, Team)
    assert test_team.id == kwargs['id']
    assert test_team.name == kwargs['name']


@patch('app.data.factories.team_factory._validate_is_unique')
def test_create_team_when_name_is_in_kwargs_and_old_team_provided_and_kwargs_name_equals_old_team_name_should_not_validate_unique_key_values_and_return_team(
        fake_validate_is_unique, test_app
):
    with test_app.app_context():
        # Arrange
        kwargs = {
            'id': 1,
            'name': "Chicago Cardinals",
        }

        old_team = Team(id=1, name="Chicago Cardinals")

        # Act
        try:
            test_team = team_factory.create_team(old_team, **kwargs)
        except ValueError:
            assert False

    # Assert
    fake_validate_is_unique.assert_not_called()
    assert isinstance(test_team, Team)
    assert test_team.id == kwargs['id']
    assert test_team.name == kwargs['name']


@patch('app.data.factories.team_factory._validate_is_unique')
def test_create_team_when_name_is_in_kwargs_and_old_team_provided_and_kwargs_name_does_not_equal_old_team_name_and_kwargs_name_is_unique_should_validate_unique_key_values_and_return_team(
        fake_validate_is_unique, test_app
):
    with test_app.app_context():
        # Arrange
        kwargs = {
            'id': 1,
            'name': "Decatur Staleys",
        }

        fake_validate_is_unique.return_value = None

        old_team = Team(id=1, name="Chicago Cardinals")

        # Act
        try:
            test_team = team_factory.create_team(old_team, **kwargs)
        except ValueError:
            assert False

    # Assert
    error_message = f"Team already exists with name={kwargs['name']}."
    fake_validate_is_unique.assert_called_once_with('name', kwargs['name'], error_message=error_message)
    assert isinstance(test_team, Team)
    assert test_team.id == kwargs['id']
    assert test_team.name == kwargs['name']


@patch('app.data.factories.team_factory._validate_is_unique')
def test_create_team_when_name_is_in_kwargs_and_old_team_provided_and_kwargs_name_does_not_equal_old_team_name_and_kwargs_name_is_not_unique_should_validate_unique_key_values_and_raise_value_error(
        fake_validate_is_unique, test_app
):
    with test_app.app_context():
        # Arrange
        kwargs = {
            'id': 1,
            'name': "Decatur Staleys",
        }

        error_message = f"Team already exists with name={kwargs['name']}."
        fake_validate_is_unique.side_effect = ValueError(error_message)

        old_team = Team(id=1, name="Chicago Cardinals")

        # Act
        with pytest.raises(ValueError) as err:
            test_team = team_factory.create_team(old_team, **kwargs)

    # Assert
    fake_validate_is_unique.assert_called_once_with('name', kwargs['name'], error_message=error_message)
    assert err.value.args[0] == error_message


@patch('app.data.factories.team_factory.Team')
def test_validate_is_unique_when_name_is_unique_should_not_raise_value_error(fake_team):
    # Arrange
    fake_team.query.filter_by.return_value.first.return_value = None

    # Act
    result = team_factory._validate_is_unique('name', "Chicago Cardinals")

    # Assert
    assert result is None


@patch('app.data.factories.team_factory.Team')
def test_validate_is_unique_when_name_is_not_unique_and_error_message_is_not_provided_should_raise_value_error_with_default_error_message(fake_team):
    # Arrange
    fake_team.query.filter_by.return_value.first.return_value = Team()

    # Act
    with pytest.raises(ValueError) as err:
        result = team_factory._validate_is_unique('name', "Chicago Cardinals")

    # Assert
    assert err.value.args[0] == "name must be unique."


@patch('app.data.factories.team_factory.Team')
def test_validate_is_unique_when_name_is_not_unique_and_error_message_is_provided_should_raise_value_error_with_provided_error_message(fake_team):
    # Arrange
    fake_team.query.filter_by.return_value.first.return_value = Team()

    error_message = f"Team already exists with name=Chicago Cardinals."

    # Act
    with pytest.raises(ValueError) as err:
        result = team_factory._validate_is_unique('name', "Chicago Cardinals", error_message=error_message)

    # Assert
    assert err.value.args[0] == error_message
