from unittest.mock import patch, call

import pytest

from app.data.factories import conference_factory
from app.data.models.conference import Conference


def test_create_conference_when_short_name_not_in_kwargs_should_raise_value_error():
    # Arrange
    kwargs = {
        'long_name': "National Football Conference",
        'league_name': "NFL",
        'first_season_year': 1970,
        'last_season_year': None,
    }

    # Act
    with pytest.raises(ValueError) as err:
        test_conference = conference_factory.create_conference(**kwargs)

    # Assert
    assert err.value.args[0] == "short_name is required."


@patch('app.data.factories.conference_factory._validate_is_unique')
def test_create_conference_when_short_name_is_in_kwargs_and_old_conference_not_provided_and_kwargs_short_name_is_not_unique_should_raise_value_error(
        fake_validate_is_unique
):
    # Arrange
    kwargs = {
        'short_name': "NFC",
        'long_name': "National Football Conference",
        'league_name': "NFL",
        'first_season_year': 1970,
        'last_season_year': None,
    }

    error_message = f"Conference already exists with short_name={kwargs['short_name']}."
    fake_validate_is_unique.side_effect = ValueError(error_message)

    # Act
    with pytest.raises(ValueError) as err:
        test_conference = conference_factory.create_conference(**kwargs)

    # Assert
    fake_validate_is_unique.assert_called_once_with('short_name', kwargs['short_name'], error_message=error_message)
    assert err.value.args[0] == error_message


@patch('app.data.factories.conference_factory._validate_is_unique')
def test_create_conference_when_short_name_is_in_kwargs_and_old_conference_not_provided_and_kwargs_short_name_is_unique_should_return_conference(
        fake_validate_is_unique
):
    # Arrange
    kwargs = {
        'id': 1,
        'short_name': "NFC",
        'long_name': "National Football Conference",
        'league_name': "NFL",
        'first_season_year': 1970,
        'last_season_year': None,
    }

    fake_validate_is_unique.return_value = None

    # Act
    try:
        test_conference = conference_factory.create_conference(**kwargs)
    except ValueError:
        assert False

    # Assert
    error_messages = (
        f"Conference already exists with short_name={kwargs['short_name']}.",
        f"Conference already exists with long_name={kwargs['long_name']}.",
    )
    fake_validate_is_unique.assert_has_calls([
        call('short_name', kwargs['short_name'], error_message=error_messages[0]),
        call('long_name', kwargs['long_name'], error_message=error_messages[1])
    ])
    assert isinstance(test_conference, Conference)
    assert test_conference.id == kwargs['id']
    assert test_conference.short_name == kwargs['short_name']
    assert test_conference.long_name == kwargs['long_name']
    assert test_conference.league_name == kwargs['league_name']
    assert test_conference.first_season_year == kwargs['first_season_year']
    assert test_conference.last_season_year == kwargs['last_season_year']


@patch('app.data.factories.conference_factory._validate_is_unique')
def test_create_conference_when_short_name_is_in_kwargs_and_old_conference_provided_and_kwargs_short_name_equals_old_conference_short_name_should_not_validate_unique_key_values_and_return_conference(
        fake_validate_is_unique
):
    # Arrange
    kwargs = {
        'id': 1,
        'short_name': "NFC",
        'long_name': "National Football Conference",
        'league_name': "NFL",
        'first_season_year': 1970,
        'last_season_year': None,
    }

    old_conference = Conference(
        id=1, short_name="NFC", long_name="National Football Conference", league_name="NFL",
        first_season_year=1970, last_season_year=None
    )

    # Act
    try:
        test_conference = conference_factory.create_conference(old_conference, **kwargs)
    except ValueError:
        assert False

    # Assert
    fake_validate_is_unique.assert_not_called()
    assert isinstance(test_conference, Conference)
    assert test_conference.id == kwargs['id']
    assert test_conference.short_name == kwargs['short_name']
    assert test_conference.long_name == kwargs['long_name']
    assert test_conference.league_name == kwargs['league_name']
    assert test_conference.first_season_year == kwargs['first_season_year']
    assert test_conference.last_season_year == kwargs['last_season_year']


@patch('app.data.factories.conference_factory._validate_is_unique')
def test_create_conference_when_short_name_is_in_kwargs_and_old_conference_provided_and_kwargs_short_name_does_not_equal_old_conference_short_name_and_kwargs_short_name_is_unique_should_validate_unique_key_values_and_return_conference(
        fake_validate_is_unique
):
    # Arrange
    kwargs = {
        'id': 1,
        'short_name': "AFC",
        'long_name': "National Football Conference",
        'league_name': "NFL",
        'first_season_year': 1970,
        'last_season_year': None,
    }

    fake_validate_is_unique.return_value = None

    old_conference = Conference(
        id=1, short_name="NFC", long_name="National Football Conference", league_name="NFL",
        first_season_year=1970, last_season_year=None
    )

    # Act
    try:
        test_conference = conference_factory.create_conference(old_conference, **kwargs)
    except ValueError:
        assert False

    # Assert
    error_message = f"Conference already exists with short_name={kwargs['short_name']}."
    fake_validate_is_unique.assert_called_once_with('short_name', kwargs['short_name'], error_message=error_message)
    assert isinstance(test_conference, Conference)
    assert test_conference.id == kwargs['id']
    assert test_conference.short_name == kwargs['short_name']
    assert test_conference.long_name == kwargs['long_name']
    assert test_conference.league_name == kwargs['league_name']
    assert test_conference.first_season_year == kwargs['first_season_year']
    assert test_conference.last_season_year == kwargs['last_season_year']


@patch('app.data.factories.conference_factory._validate_is_unique')
def test_create_conference_when_short_name_is_in_kwargs_and_old_conference_provided_and_kwargs_short_name_does_not_equal_old_conference_short_name_and_kwargs_short_name_is_not_unique_should_validate_unique_key_values_and_raise_value_error(
        fake_validate_is_unique
):
    # Arrange
    kwargs = {
        'id': 1,
        'short_name': "AFC",
        'long_name': "National Football Conference",
        'league_name': "NFL",
        'first_season_year': 1970,
        'last_season_year': None,
    }

    error_message = f"Conference already exists with short_name={kwargs['short_name']}."
    fake_validate_is_unique.side_effect = ValueError(error_message)

    old_conference = Conference(
        id=1, short_name="NFC", long_name="National Football Conference", league_name="NFL",
        first_season_year=1970, last_season_year=None
    )

    # Act
    with pytest.raises(ValueError) as err:
        test_conference = conference_factory.create_conference(old_conference, **kwargs)

    # Assert
    fake_validate_is_unique.assert_called_once_with('short_name', kwargs['short_name'], error_message=error_message)
    assert err.value.args[0] == error_message


@patch('app.data.factories.conference_factory._validate_is_unique')
def test_create_conference_when_long_name_not_in_kwargs_should_raise_value_error(fake_validate_is_unique):
    # Arrange
    kwargs = {
        'short_name': "NFC",
        'league_name': "NFL",
        'first_season_year': 1970,
        'last_season_year': None,
    }

    fake_validate_is_unique.return_value = None

    # Act
    with pytest.raises(ValueError) as err:
        test_conference = conference_factory.create_conference(**kwargs)

    # Assert
    assert err.value.args[0] == "long_name is required."


@patch('app.data.factories.conference_factory._validate_is_unique')
def test_create_conference_when_long_name_is_in_kwargs_and_old_conference_not_provided_and_kwargs_long_name_is_not_unique_should_raise_value_error(
        fake_validate_is_unique
):
    # Arrange
    kwargs = {
        'short_name': "NFC",
        'long_name': "National Football Conference",
        'league_name': "NFL",
        'first_season_year': 1970,
        'last_season_year': None,
    }

    error_messages = (
        f"Conference already exists with short_name={kwargs['short_name']}.",
        f"Conference already exists with long_name={kwargs['long_name']}.",
    )
    fake_validate_is_unique.side_effect = [None, ValueError(error_messages[1])]

    # Act
    with pytest.raises(ValueError) as err:
        test_conference = conference_factory.create_conference(**kwargs)

    # Assert
    fake_validate_is_unique.assert_has_calls([
        call('short_name', kwargs['short_name'], error_message=error_messages[0]),
        call('long_name', kwargs['long_name'], error_message=error_messages[1])
    ])
    assert err.value.args[0] == error_messages[1]


@patch('app.data.factories.conference_factory._validate_is_unique')
def test_create_conference_when_long_name_is_in_kwargs_and_old_conference_not_provided_and_kwargs_long_name_is_unique_should_return_conference(
        fake_validate_is_unique
):
    # Arrange
    kwargs = {
        'id': 1,
        'short_name': "NFC",
        'long_name': "National Football Conference",
        'league_name': "NFL",
        'first_season_year': 1970,
        'last_season_year': None,
    }

    fake_validate_is_unique.return_value = None

    # Act
    try:
        test_conference = conference_factory.create_conference(**kwargs)
    except ValueError:
        assert False

    # Assert
    error_messages = (
        f"Conference already exists with short_name={kwargs['short_name']}.",
        f"Conference already exists with long_name={kwargs['long_name']}.",
    )
    fake_validate_is_unique.assert_has_calls([
        call('short_name', kwargs['short_name'], error_message=error_messages[0]),
        call('long_name', kwargs['long_name'], error_message=error_messages[1])
    ])
    assert isinstance(test_conference, Conference)
    assert test_conference.id == kwargs['id']
    assert test_conference.short_name == kwargs['short_name']
    assert test_conference.long_name == kwargs['long_name']
    assert test_conference.league_name == kwargs['league_name']
    assert test_conference.first_season_year == kwargs['first_season_year']
    assert test_conference.last_season_year == kwargs['last_season_year']


@patch('app.data.factories.conference_factory._validate_is_unique')
def test_create_conference_when_long_name_is_in_kwargs_and_old_conference_provided_and_kwargs_long_name_equals_old_conference_long_name_should_not_validate_unique_key_values_and_return_conference(
        fake_validate_is_unique
):
    # Arrange
    kwargs = {
        'id': 1,
        'short_name': "NFC",
        'long_name': "National Football Conference",
        'league_name': "NFL",
        'first_season_year': 1970,
        'last_season_year': None,
    }

    old_conference = Conference(
        id=1, short_name="NFC", long_name="National Football Conference", league_name="NFL",
        first_season_year=1970, last_season_year=None
    )

    # Act
    try:
        test_conference = conference_factory.create_conference(old_conference, **kwargs)
    except ValueError:
        assert False

    # Assert
    fake_validate_is_unique.assert_not_called()
    assert isinstance(test_conference, Conference)
    assert test_conference.id == kwargs['id']
    assert test_conference.short_name == kwargs['short_name']
    assert test_conference.long_name == kwargs['long_name']
    assert test_conference.league_name == kwargs['league_name']
    assert test_conference.first_season_year == kwargs['first_season_year']
    assert test_conference.last_season_year == kwargs['last_season_year']


@patch('app.data.factories.conference_factory._validate_is_unique')
def test_create_conference_when_long_name_is_in_kwargs_and_old_conference_provided_and_kwargs_long_name_does_not_equal_old_conference_long_name_and_kwargs_long_name_is_unique_should_validate_unique_key_values_and_return_conference(
        fake_validate_is_unique
):
    # Arrange
    kwargs = {
        'id': 1,
        'short_name': "NFC",
        'long_name': "American Football Conference",
        'league_name': "NFL",
        'first_season_year': 1970,
        'last_season_year': None,
    }

    fake_validate_is_unique.return_value = None

    old_conference = Conference(
        id=1, short_name="NFC", long_name="National Football Conference", league_name="NFL",
        first_season_year=1970, last_season_year=None
    )

    # Act
    try:
        test_conference = conference_factory.create_conference(old_conference, **kwargs)
    except ValueError:
        assert False

    # Assert
    error_message = f"Conference already exists with long_name={kwargs['long_name']}."
    fake_validate_is_unique.assert_called_once_with('long_name', kwargs['long_name'], error_message=error_message)
    assert isinstance(test_conference, Conference)
    assert test_conference.id == kwargs['id']
    assert test_conference.short_name == kwargs['short_name']
    assert test_conference.long_name == kwargs['long_name']
    assert test_conference.league_name == kwargs['league_name']
    assert test_conference.first_season_year == kwargs['first_season_year']
    assert test_conference.last_season_year == kwargs['last_season_year']


@patch('app.data.factories.conference_factory._validate_is_unique')
def test_create_conference_when_long_name_is_in_kwargs_and_old_conference_provided_and_kwargs_long_name_does_not_equal_old_conference_long_name_and_kwargs_long_name_is_not_unique_should_validate_unique_key_values_and_raise_value_error(
        fake_validate_is_unique
):
    # Arrange
    kwargs = {
        'id': 1,
        'short_name': "NFC",
        'long_name': "American Football Conference",
        'league_name': "NFL",
        'first_season_year': 1970,
        'last_season_year': None,
    }

    error_message = f"Conference already exists with long_name={kwargs['long_name']}."
    fake_validate_is_unique.side_effect = ValueError(error_message)

    old_conference = Conference(
        id=1, short_name="NFC", long_name="National Football Conference", league_name="NFL",
        first_season_year=1970, last_season_year=None
    )

    # Act
    with pytest.raises(ValueError) as err:
        test_conference = conference_factory.create_conference(old_conference, **kwargs)

    # Assert
    fake_validate_is_unique.assert_called_once_with('long_name', kwargs['long_name'], error_message=error_message)
    assert err.value.args[0] == error_message


@patch('app.data.factories.conference_factory.Conference')
def test_validate_is_unique_when_short_name_is_unique_should_not_raise_value_error(fake_conference):
    # Arrange
    fake_conference.query.filter_by.return_value.first.return_value = None

    # Act
    result = conference_factory._validate_is_unique('short_name', "NFC")

    # Assert
    assert result is None


@patch('app.data.factories.conference_factory.Conference')
def test_validate_is_unique_when_short_name_is_not_unique_and_error_message_is_not_provided_should_raise_value_error_with_default_error_message(fake_conference):
    # Arrange
    fake_conference.query.filter_by.return_value.first.return_value = Conference()

    # Act
    with pytest.raises(ValueError) as err:
        result = conference_factory._validate_is_unique('short_name', "NFC")

    # Assert
    assert err.value.args[0] == "short_name must be unique."


@patch('app.data.factories.conference_factory.Conference')
def test_validate_is_unique_when_short_name_is_not_unique_and_error_message_is_provided_should_raise_value_error_with_provided_error_message(fake_conference):
    # Arrange
    fake_conference.query.filter_by.return_value.first.return_value = Conference()

    error_message = f"Conference already exists with short_name=NFC."

    # Act
    with pytest.raises(ValueError) as err:
        result = conference_factory._validate_is_unique('short_name', "NFC", error_message=error_message)

    # Assert
    assert err.value.args[0] == error_message
