from unittest.mock import patch, call

import pytest

from app.data.factories import league_factory
from app.data.models.league import League


def test_create_league_when_key_is_not_in_view_model_map_should_raise_value_error():
    # Arrange
    kwargs = {
        'invalid_key': "Value"
    }

    # Act
    with pytest.raises(KeyError) as err:
        test_league = league_factory.create_league(**kwargs)

    # Assert
    assert err.value.args[0] == f"invalid_key is invalid."


@patch('app.data.factories.league_factory._validate_is_unique')
def test_create_league_when_unique_keys_are_in_kwargs_and_old_league_id_is_not_provided_and_kwargs_short_name_and_long_name_are_unique_should_return_league(
        fake_validate_is_unique
):
    # Arrange
    kwargs = {
        'short_name': "L",
        'long_name': "League",
        'first_season_year': 1920,
        'last_season_year': None,
    }

    fake_validate_is_unique.return_value = None

    # Act
    try:
        test_league = league_factory.create_league(**kwargs)
    except ValueError:
        assert False

    # Assert
    error_messages = (
        f"League already exists with short_name={kwargs.get('short_name')}.",
        f"League already exists with long_name={kwargs.get('long_name')}.",
    )
    fake_validate_is_unique.assert_has_calls([
        call('short_name', kwargs.get('short_name'), error_message=error_messages[0]),
        call('long_name', kwargs.get('long_name'), error_message=error_messages[1])
    ])
    assert isinstance(test_league, League)
    assert test_league.short_name == kwargs.get('short_name')
    assert test_league.long_name == kwargs.get('long_name')
    assert test_league.first_season_id == kwargs.get('first_season_year')
    assert test_league.last_season_id == kwargs.get('last_season_year')


@patch('app.data.factories.league_factory._validate_is_unique')
def test_create_league_when_unique_keys_are_in_kwargs_and_old_league_id_is_not_provided_and_kwargs_short_name_is_not_unique_should_raise_value_error(
        fake_validate_is_unique
):
    # Arrange
    kwargs = {
        'short_name': "L",
        'long_name': "League",
        'first_season_year': 1920,
        'last_season_year': None,
    }

    error_message = f"League already exists with short_name={kwargs.get('short_name')}."
    fake_validate_is_unique.side_effect = ValueError(error_message)

    # Act
    with pytest.raises(ValueError) as err:
        test_league = league_factory.create_league(**kwargs)

    # Assert
    fake_validate_is_unique.assert_called_once_with('short_name', kwargs.get('short_name'), error_message=error_message)
    assert err.value.args[0] == error_message


@patch('app.data.factories.league_factory._validate_is_unique')
def test_create_league_when_unique_keys_are_in_kwargs_and_old_league_id_is_not_provided_and_kwargs_long_name_is_not_unique_should_raise_value_error(
        fake_validate_is_unique
):
    # Arrange
    kwargs = {
        'short_name': "L",
        'long_name': "League",
        'first_season_year': 1920,
        'last_season_year': None,
    }

    error_messages = (
        f"League already exists with short_name={kwargs.get('short_name')}.",
        f"League already exists with long_name={kwargs.get('long_name')}.",
    )
    fake_validate_is_unique.side_effect = [None, ValueError(error_messages[1])]

    # Act
    with pytest.raises(ValueError) as err:
        test_league = league_factory.create_league(**kwargs)

    # Assert
    fake_validate_is_unique.assert_has_calls([
        call('short_name', kwargs.get('short_name'), error_message=error_messages[0]),
        call('long_name', kwargs.get('long_name'), error_message=error_messages[1])
    ])
    assert err.value.args[0] == error_messages[1]


@patch('app.data.factories.league_factory._validate_is_unique')
@patch('app.data.factories.league_factory.LeagueRepository')
@patch('app.data.factories.league_factory.injector')
def test_create_league_when_unique_keys_are_in_kwargs_and_old_league_id_is_provided_and_short_name_and_long_name_have_not_changed_should_not_validate_unique_key_values_and_return_league(
        fake_injector, fake_league_repository, fake_validate_is_unique
):
    # Arrange
    kwargs = {
        'id': 1,
        'short_name': "L",
        'long_name': "League",
        'first_season_year': 1920,
        'last_season_year': None,
    }

    old_league = League(short_name="L", long_name="League", first_season_id=1920)
    fake_league_repository.get_league.return_value = old_league
    fake_injector.get.return_value = fake_league_repository

    # Act
    try:
        test_league = league_factory.create_league(**kwargs)
    except ValueError:
        assert False

    # Assert
    fake_injector.get.assert_has_calls([
        call(fake_league_repository),
        call(fake_league_repository),
    ])
    fake_league_repository.get_league.assert_has_calls([
        call(kwargs.get('id')),
        call(kwargs.get('id')),
    ])
    fake_validate_is_unique.assert_not_called()
    assert isinstance(test_league, League)
    assert test_league.id == kwargs.get('id')
    assert test_league.short_name == kwargs.get('short_name')
    assert test_league.long_name == kwargs.get('long_name')
    assert test_league.first_season_id == kwargs.get('first_season_year')
    assert test_league.last_season_id == kwargs.get('last_season_year')


@patch('app.data.factories.league_factory._validate_is_unique')
@patch('app.data.factories.league_factory.LeagueRepository')
@patch('app.data.factories.league_factory.injector')
def test_create_league_when_unique_keys_are_in_kwargs_and_old_league_id_is_provided_and_short_name_has_changed_and_is_unique_should_not_validate_unique_key_values_and_return_league(
        fake_injector, fake_league_repository, fake_validate_is_unique
):
    # Arrange
    kwargs = {
        'id': 1,
        'short_name': "NL",
        'long_name': "New League",
        'first_season_year': 1922,
        'last_season_year': None,
    }

    old_league = League(short_name="L", long_name="League", first_season_id=1920, last_season_id=1921)
    fake_league_repository.get_league.return_value = old_league
    fake_injector.get.return_value = fake_league_repository

    fake_validate_is_unique.return_value = True

    # Act
    try:
        test_league = league_factory.create_league(**kwargs)
    except ValueError:
        assert False

    # Assert
    fake_injector.get.assert_has_calls([
        call(fake_league_repository),
        call(fake_league_repository),
    ])
    fake_league_repository.get_league.assert_has_calls([
        call(kwargs.get('id')),
        call(kwargs.get('id')),
    ])
    fake_validate_is_unique.assert_has_calls([
        call('short_name', kwargs.get('short_name'), error_message=f"League already exists with short_name={kwargs.get('short_name')}."),
        call('long_name', kwargs.get('long_name'), error_message=f"League already exists with long_name={kwargs.get('long_name')}."),
    ])
    assert isinstance(test_league, League)
    assert test_league.id == kwargs.get('id')
    assert test_league.short_name == kwargs.get('short_name')
    assert test_league.long_name == kwargs.get('long_name')
    assert test_league.first_season_id == kwargs.get('first_season_year')
    assert test_league.last_season_id == kwargs.get('last_season_year')


@patch('app.data.factories.league_factory._validate_is_unique')
@patch('app.data.factories.league_factory.LeagueRepository')
@patch('app.data.factories.league_factory.injector')
def test_create_league_when_unique_keys_are_in_kwargs_and_old_league_id_is_provided_and_short_name_has_changed_and_is_not_unique_should_validate_unique_key_values_and_raise_value_error(
        fake_injector, fake_league_repository, fake_validate_is_unique
):
    # Arrange
    kwargs = {
        'id': 1,
        'short_name': "NL",
        'long_name': "New League",
        'first_season_year': 1922,
        'last_season_year': None,
    }

    old_league = League(short_name="L", long_name="League", first_season_id=1920, last_season_id=1921)
    fake_league_repository.get_league.return_value = old_league
    fake_injector.get.return_value = fake_league_repository

    fake_validate_is_unique.side_effect = ValueError("short_name must be unique.")

    # Act
    with pytest.raises(ValueError) as err:
        test_league = league_factory.create_league(**kwargs)

    # Assert
    fake_injector.get.assert_called_once_with(fake_league_repository)
    fake_league_repository.get_league.assert_called_once_with(kwargs.get('id'))
    fake_validate_is_unique.assert_called_once_with(
        'short_name', kwargs.get('short_name'),
        error_message=f"League already exists with short_name={kwargs.get('short_name')}."
    ),


@patch('app.data.factories.league_factory._validate_is_unique')
@patch('app.data.factories.league_factory.LeagueRepository')
@patch('app.data.factories.league_factory.injector')
def test_create_league_when_unique_keys_are_in_kwargs_and_old_league_id_is_provided_and_long_name_has_changed_and_is_unique_should_not_validate_unique_key_values_and_return_league(
        fake_injector, fake_league_repository, fake_validate_is_unique
):
    # Arrange
    kwargs = {
        'id': 1,
        'short_name': "L",
        'long_name': "New League",
        'first_season_year': 1922,
        'last_season_year': None,
    }

    old_league = League(short_name="L", long_name="League", first_season_id=1920, last_season_id=1921)
    fake_league_repository.get_league.return_value = old_league
    fake_injector.get.return_value = fake_league_repository

    fake_validate_is_unique.side_effect = [False, True]

    # Act
    try:
        test_league = league_factory.create_league(**kwargs)
    except ValueError:
        assert False

    # Assert
    fake_injector.get.assert_has_calls([
        call(fake_league_repository),
        call(fake_league_repository),
    ])
    fake_league_repository.get_league.assert_has_calls([
        call(kwargs.get('id')),
        call(kwargs.get('id')),
    ])
    fake_validate_is_unique.assert_has_calls([
        call('long_name', kwargs.get('long_name'), error_message=f"League already exists with long_name={kwargs.get('long_name')}."),
    ])
    assert isinstance(test_league, League)
    assert test_league.id == kwargs.get('id')
    assert test_league.short_name == kwargs.get('short_name')
    assert test_league.long_name == kwargs.get('long_name')
    assert test_league.first_season_id == kwargs.get('first_season_year')
    assert test_league.last_season_id == kwargs.get('last_season_year')


@patch('app.data.factories.league_factory._validate_is_unique')
@patch('app.data.factories.league_factory.LeagueRepository')
@patch('app.data.factories.league_factory.injector')
def test_create_league_when_unique_keys_are_in_kwargs_and_old_league_id_is_provided_and_long_name_has_changed_and_is_not_unique_should_validate_unique_key_values_and_raise_value_error(
        fake_injector, fake_league_repository, fake_validate_is_unique
):
    # Arrange
    kwargs = {
        'id': 1,
        'short_name': "L",
        'long_name': "New League",
        'first_season_year': 1922,
        'last_season_year': None,
    }

    old_league = League(short_name="L", long_name="League", first_season_id=1920, last_season_id=1921)
    fake_league_repository.get_league.return_value = old_league
    fake_injector.get.return_value = fake_league_repository

    fake_validate_is_unique.side_effect = ValueError("long_name must be unique.")

    # Act
    with pytest.raises(ValueError) as err:
        test_league = league_factory.create_league(**kwargs)

    # Assert
    fake_injector.get.assert_has_calls([
        call(fake_league_repository),
        call(fake_league_repository),
    ])
    fake_league_repository.get_league.assert_has_calls([
        call(kwargs.get('id')),
        call(kwargs.get('id')),
    ])
    fake_validate_is_unique.assert_called_once_with(
        'long_name', kwargs.get('long_name'),
        error_message=f"League already exists with long_name={kwargs.get('long_name')}."
    ),


@patch('app.data.factories.league_factory.League')
def test_validate_is_unique_when_value_is_not_unique_and_error_message_is_not_provided_should_raise_value_error_with_default_error_message(fake_league):
    # Arrange
    fake_league.query.filter_by.return_value.first.return_value = League()

    # Act
    with pytest.raises(ValueError) as err:
        result = league_factory._validate_is_unique('short_name', "L")

    # Assert
    assert err.value.args[0] == "short_name must be unique."


@patch('app.data.factories.league_factory.League')
def test_validate_is_unique_when_value_is_not_unique_and_error_message_is_provided_should_raise_value_error_with_provided_error_message(fake_league):
    # Arrange
    fake_league.query.filter_by.return_value.first.return_value = League()

    error_message = f"League already exists with short_name=L."

    # Act
    with pytest.raises(ValueError) as err:
        result = league_factory._validate_is_unique('short_name', "L", error_message=error_message)

    # Assert
    assert err.value.args[0] == error_message


@patch('app.data.factories.league_factory.LeagueRepository')
@patch('app.data.factories.league_factory.injector')
def test_value_has_changed_when_new_value_equals_old_value_should_return_false(
        fake_injector, fake_league_repository
):
    # Arrange
    kwargs = {
        'id': 1,
        'short_name': "L",
    }

    old_league = League(short_name="L", long_name="League", first_season_id=1920)
    fake_league_repository.get_league.return_value = old_league
    fake_injector.get.return_value = fake_league_repository

    # Act
    result = league_factory._value_has_changed('short_name', **kwargs)

    # Assert
    assert result is False
    fake_injector.get.assert_called_once_with(fake_league_repository)
    fake_league_repository.get_league.assert_called_once_with(kwargs.get('id'))


@patch('app.data.factories.league_factory.LeagueRepository')
@patch('app.data.factories.league_factory.injector')
def test_value_has_changed_when_new_value_does_not_equal_old_value_should_return_true(
        fake_injector, fake_league_repository
):
    # Arrange
    kwargs = {
        'id': 1,
        'short_name': "NL",
    }

    old_league = League(short_name="OL", long_name="League", first_season_id=1920)
    fake_league_repository.get_league.return_value = old_league
    fake_injector.get.return_value = fake_league_repository

    # Act
    result = league_factory._value_has_changed('short_name', **kwargs)

    # Assert
    assert result is True
    fake_injector.get.assert_called_once_with(fake_league_repository)
    fake_league_repository.get_league.assert_called_once_with(kwargs.get('id'))
