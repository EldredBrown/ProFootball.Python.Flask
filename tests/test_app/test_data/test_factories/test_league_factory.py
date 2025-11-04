from unittest.mock import patch, call

import pytest

from app.data.factories import league_factory
from app.data.models.league import League


def test_create_league_when_short_name_not_in_kwargs_should_raise_value_error():
    # Arrange
    kwargs = {
        'long_name': "National Football League",
        'first_season_year': 1922,
        'last_season_year': None,
    }

    # Act
    with pytest.raises(ValueError) as err:
        test_league = league_factory.create_league(**kwargs)

    # Assert
    assert err.value.args[0] == "short_name is required."


@patch('app.data.factories.league_factory._validate_is_unique')
def test_create_league_when_short_name_is_in_kwargs_and_old_league_not_provided_and_kwargs_short_name_is_not_unique_should_raise_value_error(
        fake_validate_is_unique
):
    # Arrange
    kwargs = {
        'short_name': "NFL",
        'long_name': "National Football League",
        'first_season_year': 1922,
        'last_season_year': None,
    }

    error_message = f"League already exists with short_name={kwargs['short_name']}."
    fake_validate_is_unique.side_effect = ValueError(error_message)

    # Act
    with pytest.raises(ValueError) as err:
        test_league = league_factory.create_league(**kwargs)

    # Assert
    fake_validate_is_unique.assert_called_once_with('short_name', kwargs['short_name'], error_message=error_message)
    assert err.value.args[0] == error_message


@patch('app.data.factories.league_factory._validate_is_unique')
def test_create_league_when_short_name_is_in_kwargs_and_old_league_not_provided_and_kwargs_short_name_is_unique_should_return_league(
        fake_validate_is_unique
):
    # Arrange
    kwargs = {
        'id': 1,
        'short_name': "NFL",
        'long_name': "National Football League",
        'first_season_year': 1922,
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
        f"League already exists with short_name={kwargs['short_name']}.",
        f"League already exists with long_name={kwargs['long_name']}.",
    )
    fake_validate_is_unique.assert_has_calls([
        call('short_name', kwargs['short_name'], error_message=error_messages[0]),
        call('long_name', kwargs['long_name'], error_message=error_messages[1])
    ])
    assert isinstance(test_league, League)
    assert test_league.id == kwargs['id']
    assert test_league.short_name == kwargs['short_name']
    assert test_league.long_name == kwargs['long_name']
    assert test_league.first_season_year == kwargs['first_season_year']
    assert test_league.last_season_year == kwargs['last_season_year']


@patch('app.data.factories.league_factory._validate_is_unique')
def test_create_league_when_short_name_is_in_kwargs_and_old_league_provided_and_kwargs_short_name_equals_old_league_short_name_should_not_validate_unique_key_values_and_return_league(
        fake_validate_is_unique
):
    # Arrange
    kwargs = {
        'id': 1,
        'short_name': "NFL",
        'long_name': "National Football League",
        'first_season_year': 1922,
        'last_season_year': None,
    }

    old_league = League(
        id=1, short_name="NFL", long_name="National Football League", first_season_year=1922, last_season_year=None
    )

    # Act
    try:
        test_league = league_factory.create_league(old_league, **kwargs)
    except ValueError:
        assert False

    # Assert
    fake_validate_is_unique.assert_not_called()
    assert isinstance(test_league, League)
    assert test_league.id == kwargs['id']
    assert test_league.short_name == kwargs['short_name']
    assert test_league.long_name == kwargs['long_name']
    assert test_league.first_season_year == kwargs['first_season_year']
    assert test_league.last_season_year == kwargs['last_season_year']


@patch('app.data.factories.league_factory._validate_is_unique')
def test_create_league_when_short_name_is_in_kwargs_and_old_league_provided_and_kwargs_short_name_does_not_equal_old_league_short_name_and_kwargs_short_name_is_unique_should_validate_unique_key_values_and_return_league(
        fake_validate_is_unique
):
    # Arrange
    kwargs = {
        'id': 1,
        'short_name': "AFL",
        'long_name': "National Football League",
        'first_season_year': 1922,
        'last_season_year': None,
    }

    fake_validate_is_unique.return_value = None

    old_league = League(
        id=1, short_name="NFL", long_name="National Football League", first_season_year=1922, last_season_year=None
    )

    # Act
    try:
        test_league = league_factory.create_league(old_league, **kwargs)
    except ValueError:
        assert False

    # Assert
    error_message = f"League already exists with short_name={kwargs['short_name']}."
    fake_validate_is_unique.assert_called_once_with('short_name', kwargs['short_name'], error_message=error_message)
    assert isinstance(test_league, League)
    assert test_league.id == kwargs['id']
    assert test_league.short_name == kwargs['short_name']
    assert test_league.long_name == kwargs['long_name']
    assert test_league.first_season_year == kwargs['first_season_year']
    assert test_league.last_season_year == kwargs['last_season_year']


@patch('app.data.factories.league_factory._validate_is_unique')
def test_create_league_when_short_name_is_in_kwargs_and_old_league_provided_and_kwargs_short_name_does_not_equal_old_league_short_name_and_kwargs_short_name_is_not_unique_should_validate_unique_key_values_and_raise_value_error(
        fake_validate_is_unique
):
    # Arrange
    kwargs = {
        'id': 1,
        'short_name': "AFL",
        'long_name': "National Football League",
        'first_season_year': 1922,
        'last_season_year': None,
    }

    error_message = f"League already exists with short_name={kwargs['short_name']}."
    fake_validate_is_unique.side_effect = ValueError(error_message)

    old_league = League(
        id=1, short_name="NFL", long_name="National Football League", first_season_year=1922, last_season_year=None
    )

    # Act
    with pytest.raises(ValueError) as err:
        test_league = league_factory.create_league(old_league, **kwargs)

    # Assert
    fake_validate_is_unique.assert_called_once_with('short_name', kwargs['short_name'], error_message=error_message)
    assert err.value.args[0] == error_message


@patch('app.data.factories.league_factory._validate_is_unique')
def test_create_league_when_long_name_not_in_kwargs_should_raise_value_error(fake_validate_is_unique):
    # Arrange
    kwargs = {
        'short_name': "NFL",
        'first_season_year': 1922,
        'last_season_year': None,
    }

    fake_validate_is_unique.return_value = None

    # Act
    with pytest.raises(ValueError) as err:
        test_league = league_factory.create_league(**kwargs)

    # Assert
    assert err.value.args[0] == "long_name is required."


@patch('app.data.factories.league_factory._validate_is_unique')
def test_create_league_when_long_name_is_in_kwargs_and_old_league_not_provided_and_kwargs_long_name_is_not_unique_should_raise_value_error(
        fake_validate_is_unique
):
    # Arrange
    kwargs = {
        'short_name': "NFL",
        'long_name': "National Football League",
        'first_season_year': 1922,
        'last_season_year': None,
    }

    error_messages = (
        f"League already exists with short_name={kwargs['short_name']}.",
        f"League already exists with long_name={kwargs['long_name']}.",
    )
    fake_validate_is_unique.side_effect = [None, ValueError(error_messages[1])]

    # Act
    with pytest.raises(ValueError) as err:
        test_league = league_factory.create_league(**kwargs)

    # Assert
    fake_validate_is_unique.assert_has_calls([
        call('short_name', kwargs['short_name'], error_message=error_messages[0]),
        call('long_name', kwargs['long_name'], error_message=error_messages[1])
    ])
    assert err.value.args[0] == error_messages[1]


@patch('app.data.factories.league_factory._validate_is_unique')
def test_create_league_when_long_name_is_in_kwargs_and_old_league_not_provided_and_kwargs_long_name_is_unique_should_return_league(
        fake_validate_is_unique
):
    # Arrange
    kwargs = {
        'id': 1,
        'short_name': "NFL",
        'long_name': "National Football League",
        'first_season_year': 1922,
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
        f"League already exists with short_name={kwargs['short_name']}.",
        f"League already exists with long_name={kwargs['long_name']}.",
    )
    fake_validate_is_unique.assert_has_calls([
        call('short_name', kwargs['short_name'], error_message=error_messages[0]),
        call('long_name', kwargs['long_name'], error_message=error_messages[1])
    ])
    assert isinstance(test_league, League)
    assert test_league.id == kwargs['id']
    assert test_league.short_name == kwargs['short_name']
    assert test_league.long_name == kwargs['long_name']
    assert test_league.first_season_year == kwargs['first_season_year']
    assert test_league.last_season_year == kwargs['last_season_year']


@patch('app.data.factories.league_factory._validate_is_unique')
def test_create_league_when_long_name_is_in_kwargs_and_old_league_provided_and_kwargs_long_name_equals_old_league_long_name_should_not_validate_unique_key_values_and_return_league(
        fake_validate_is_unique
):
    # Arrange
    kwargs = {
        'id': 1,
        'short_name': "NFL",
        'long_name': "National Football League",
        'first_season_year': 1922,
        'last_season_year': None,
    }

    old_league = League(
        id=1, short_name="NFL", long_name="National Football League", first_season_year=1922, last_season_year=None
    )

    # Act
    try:
        test_league = league_factory.create_league(old_league, **kwargs)
    except ValueError:
        assert False

    # Assert
    fake_validate_is_unique.assert_not_called()
    assert isinstance(test_league, League)
    assert test_league.id == kwargs['id']
    assert test_league.short_name == kwargs['short_name']
    assert test_league.long_name == kwargs['long_name']
    assert test_league.first_season_year == kwargs['first_season_year']
    assert test_league.last_season_year == kwargs['last_season_year']


@patch('app.data.factories.league_factory._validate_is_unique')
def test_create_league_when_long_name_is_in_kwargs_and_old_league_provided_and_kwargs_long_name_does_not_equal_old_league_long_name_and_kwargs_long_name_is_unique_should_validate_unique_key_values_and_return_league(
        fake_validate_is_unique
):
    # Arrange
    kwargs = {
        'id': 1,
        'short_name': "NFL",
        'long_name': "National Football League",
        'first_season_year': 1922,
        'last_season_year': None,
    }

    fake_validate_is_unique.return_value = None

    old_league = League(
        id=1, short_name="NFL", long_name="American Football League", first_season_year=1922, last_season_year=None
    )

    # Act
    try:
        test_league = league_factory.create_league(old_league, **kwargs)
    except ValueError:
        assert False

    # Assert
    error_message = f"League already exists with long_name={kwargs['long_name']}."
    fake_validate_is_unique.assert_called_once_with('long_name', kwargs['long_name'], error_message=error_message)
    assert isinstance(test_league, League)
    assert test_league.id == kwargs['id']
    assert test_league.short_name == kwargs['short_name']
    assert test_league.long_name == kwargs['long_name']
    assert test_league.first_season_year == kwargs['first_season_year']
    assert test_league.last_season_year == kwargs['last_season_year']


@patch('app.data.factories.league_factory._validate_is_unique')
def test_create_league_when_long_name_is_in_kwargs_and_old_league_provided_and_kwargs_long_name_does_not_equal_old_league_long_name_and_kwargs_long_name_is_not_unique_should_validate_unique_key_values_and_raise_value_error(
        fake_validate_is_unique
):
    # Arrange
    kwargs = {
        'id': 1,
        'short_name': "NFL",
        'long_name': "National Football League",
        'first_season_year': 1922,
        'last_season_year': None,
    }

    error_message = f"League already exists with long_name={kwargs['long_name']}."
    fake_validate_is_unique.side_effect = ValueError(error_message)

    old_league = League(
        id=1, short_name="NFL", long_name="American Football League", first_season_year=1922, last_season_year=None
    )

    # Act
    with pytest.raises(ValueError) as err:
        test_league = league_factory.create_league(old_league, **kwargs)

    # Assert
    fake_validate_is_unique.assert_called_once_with('long_name', kwargs['long_name'], error_message=error_message)
    assert err.value.args[0] == error_message


@patch('app.data.factories.league_factory.League')
def test_validate_is_unique_when_short_name_is_unique_should_not_raise_value_error(fake_league):
    # Arrange
    fake_league.query.filter_by.return_value.first.return_value = None

    # Act
    result = league_factory._validate_is_unique('short_name', "NFL")

    # Assert
    assert result is None


@patch('app.data.factories.league_factory.League')
def test_validate_is_unique_when_short_name_is_not_unique_and_error_message_is_not_provided_should_raise_value_error_with_default_error_message(fake_league):
    # Arrange
    fake_league.query.filter_by.return_value.first.return_value = League()

    # Act
    with pytest.raises(ValueError) as err:
        result = league_factory._validate_is_unique('short_name', "NFL")

    # Assert
    assert err.value.args[0] == "short_name must be unique."


@patch('app.data.factories.league_factory.League')
def test_validate_is_unique_when_short_name_is_not_unique_and_error_message_is_provided_should_raise_value_error_with_provided_error_message(fake_league):
    # Arrange
    fake_league.query.filter_by.return_value.first.return_value = League()

    error_message = f"League already exists with short_name=NFL."

    # Act
    with pytest.raises(ValueError) as err:
        result = league_factory._validate_is_unique('short_name', "NFL", error_message=error_message)

    # Assert
    assert err.value.args[0] == error_message
