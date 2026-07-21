from unittest.mock import patch, call

import pytest

from app.data.factories import team_factory
from app.data.models.team import Team


def test_create_team_when_key_is_not_in_view_model_map_should_raise_value_error():
    # Arrange
    kwargs = {
        'invalid_key': "Value"
    }

    # Act
    with pytest.raises(KeyError) as err:
        _ = team_factory.create_team(**kwargs)

    # Assert
    assert err.value.args[0] == f"invalid_key is invalid."


@patch('app.data.factories.team_factory._validate_is_unique')
def test_create_team_when_name_is_in_kwargs_and_old_team_id_is_not_provided_and_kwargs_name_is_unique_should_return_team(
        fake_validate_is_unique
):
    # Arrange
    fake_validate_is_unique.return_value = None

    kwargs = {
        'name': "Team",
    }

    # Act
    try:
        test_team = team_factory.create_team(**kwargs)
    except ValueError:
        assert False

    # Assert
    error_message = f"Team already exists with name={kwargs.get('name')}."
    fake_validate_is_unique.assert_called_once_with('name', kwargs.get('name'), error_message=error_message)

    assert isinstance(test_team, Team)
    assert test_team.name == kwargs.get('name')


@patch('app.data.factories.team_factory._validate_is_unique')
def test_create_team_when_name_is_in_kwargs_and_old_team_id_is_not_provided_and_kwargs_name_is_not_unique_should_raise_value_error(
        fake_validate_is_unique
):
    # Arrange
    fake_validate_is_unique.return_value = None

    kwargs = {
        'name': "Team",
    }

    error_message = f"Team already exists with name={kwargs.get('name')}."
    fake_validate_is_unique.side_effect = ValueError(error_message)

    # Act
    with pytest.raises(ValueError) as err:
        _ = team_factory.create_team(**kwargs)

    # Assert
    fake_validate_is_unique.assert_called_once_with('name', kwargs.get('name'), error_message=error_message)
    assert err.value.args[0] == error_message


@patch('app.data.factories.team_factory._validate_is_unique')
@patch('app.data.factories.team_factory.TeamRepository')
@patch('app.data.factories.team_factory.injector')
def test_create_team_when_name_is_in_kwargs_and_old_team_id_is_provided_and_name_has_not_changed_should_not_validate_name_and_return_team(
        fake_injector, fake_team_repository, fake_validate_is_unique
):
    # Arrange
    fake_validate_is_unique.return_value = None

    kwargs = {
        'id': 1,
        'name': "Team",
    }

    old_team = Team(name=kwargs.get('name'))

    fake_team_repository.get_team.return_value = old_team
    fake_injector.get.return_value = fake_team_repository

    # Act
    try:
        test_team = team_factory.create_team(**kwargs)
    except ValueError:
        assert False

    # Assert
    fake_injector.get.assert_called_once_with(fake_team_repository)
    fake_team_repository.get_team.assert_called_once_with(kwargs.get('id'))
    fake_validate_is_unique.assert_not_called()

    assert isinstance(test_team, Team)
    assert test_team.id == kwargs.get('id')
    assert test_team.name == kwargs.get('name')


@patch('app.data.factories.team_factory._validate_is_unique')
@patch('app.data.factories.team_factory.TeamRepository')
@patch('app.data.factories.team_factory.injector')
def test_create_team_when_name_is_in_kwargs_and_old_team_id_is_provided_and_name_has_changed_and_is_unique_should_validate_unique_key_values_and_return_team(
        fake_injector, fake_team_repository, fake_validate_is_unique
):
    # Arrange
    fake_validate_is_unique.return_value = None

    kwargs = {
        'id': 1,
        'name': "New Team",
    }

    old_team = Team(name="Old Team")

    fake_team_repository.get_team.return_value = old_team
    fake_injector.get.return_value = fake_team_repository

    fake_validate_is_unique.return_value = True

    # Act
    try:
        test_team = team_factory.create_team(**kwargs)
    except ValueError:
        assert False

    # Assert
    fake_injector.get.assert_called_once_with(fake_team_repository)
    fake_team_repository.get_team.assert_called_once_with(kwargs.get('id'))
    fake_validate_is_unique.assert_called_once_with(
        'name', kwargs.get('name'), error_message=f"Team already exists with name={kwargs.get('name')}."
    )

    assert isinstance(test_team, Team)
    assert test_team.id == kwargs.get('id')
    assert test_team.name == kwargs.get('name')


@patch('app.data.factories.team_factory._validate_is_unique')
@patch('app.data.factories.team_factory.TeamRepository')
@patch('app.data.factories.team_factory.injector')
def test_create_team_when_name_is_in_kwargs_and_old_team_id_is_provided_and_name_has_changed_and_is_not_unique_should_validate_unique_key_values_and_raise_value_error(
        fake_injector, fake_team_repository, fake_validate_is_unique
):
    # Arrange
    fake_validate_is_unique.return_value = None

    kwargs = {
        'id': 1,
        'name': "New Team",
    }

    old_team = Team(name="Old Team")

    fake_team_repository.get_team.return_value = old_team
    fake_injector.get.return_value = fake_team_repository

    fake_validate_is_unique.side_effect = ValueError("name must be unique.")

    # Act
    with pytest.raises(ValueError) as err:
        _ = team_factory.create_team(**kwargs)

    # Assert
    fake_injector.get.assert_called_once_with(fake_team_repository)
    fake_team_repository.get_team.assert_called_once_with(kwargs.get('id'))
    fake_validate_is_unique.assert_called_once_with(
        'name', kwargs.get('name'),
        error_message=f"Team already exists with name={kwargs.get('name')}."
    ),


@patch('app.data.factories.team_factory.Team')
def test_validate_is_unique_when_value_is_not_unique_and_error_message_is_not_provided_should_raise_value_error_with_default_error_message(fake_team):
    # Arrange
    fake_team.query.filter_by.return_value.first.return_value = Team()

    # Act
    with pytest.raises(ValueError) as err:
        _ = team_factory._validate_is_unique('name', "Team")

    # Assert
    assert err.value.args[0] == "name must be unique."


@patch('app.data.factories.team_factory.Team')
def test_validate_is_unique_when_value_is_not_unique_and_error_message_is_provided_should_raise_value_error_with_provided_error_message(fake_team):
    # Arrange
    fake_team.query.filter_by.return_value.first.return_value = Team()

    error_message = f"Team already exists with name=Team."

    # Act
    with pytest.raises(ValueError) as err:
        _ = team_factory._validate_is_unique('name', "Team", error_message=error_message)

    # Assert
    assert err.value.args[0] == error_message


@patch('app.data.factories.team_factory.TeamRepository')
@patch('app.data.factories.team_factory.injector')
def test_value_has_changed_when_new_value_equals_old_value_should_return_false(fake_injector, fake_team_repository):
    # Arrange
    kwargs = {
        'id': 1,
        'name': "Team",
    }

    old_team = Team(name="Team")
    fake_team_repository.get_team.return_value = old_team
    fake_injector.get.return_value = fake_team_repository

    # Act
    result = team_factory._value_has_changed('name', **kwargs)

    # Assert
    assert result is False
    fake_injector.get.assert_called_once_with(fake_team_repository)
    fake_team_repository.get_team.assert_called_once_with(kwargs.get('id'))


@patch('app.data.factories.team_factory.TeamRepository')
@patch('app.data.factories.team_factory.injector')
def test_value_has_changed_when_new_value_does_not_equal_old_value_should_return_true(fake_injector, fake_team_repository):
    # Arrange
    kwargs = {
        'id': 1,
        'name': "New Team",
    }

    old_team = Team(name="Old Team")
    fake_team_repository.get_team.return_value = old_team
    fake_injector.get.return_value = fake_team_repository

    # Act
    result = team_factory._value_has_changed('name', **kwargs)

    # Assert
    assert result is True
    fake_injector.get.assert_called_once_with(fake_team_repository)
    fake_team_repository.get_team.assert_called_once_with(kwargs.get('id'))
