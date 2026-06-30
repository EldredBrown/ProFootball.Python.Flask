from unittest.mock import patch, call

import pytest

from app.data.factories import conference_factory
from app.data.models.conference import Conference
from app.data.models.league import League


def test_create_conference_when_key_is_not_in_view_model_map_should_raise_value_error():
    # Arrange
    kwargs = {
        'invalid_key': "Value"
    }

    # Act
    with pytest.raises(KeyError) as err:
        test_conference = conference_factory.create_conference(**kwargs)

    # Assert
    assert err.value.args[0] == f"invalid_key is invalid."


@patch('app.data.factories.conference_factory._validate_is_unique')
@patch('app.data.factories.conference_factory.LeagueRepository')
@patch('app.data.factories.conference_factory.injector')
def test_create_conference_when_unique_keys_are_in_kwargs_and_old_conference_id_is_not_provided_and_kwargs_short_name_and_long_name_are_unique_should_return_conference(
        fake_injector, fake_league_repository,
        fake_validate_is_unique
):
    # Arrange
    fake_validate_is_unique.return_value = None

    league = League(
        id=1,
        short_name="L",
        long_name="League",
        first_season_id=1920
    )
    fake_league_repository.get_league_by_short_name.return_value = league

    fake_injector.get.return_value = fake_league_repository

    kwargs = {
        'short_name': "C",
        'long_name': "Conference",
        'league_name': league.short_name,
        'first_season_year': 1920,
        'last_season_year': None,
    }

    # Act
    try:
        test_conference = conference_factory.create_conference(**kwargs)
    except ValueError:
        assert False

    # Assert
    error_messages = (
        f"Conference already exists with short_name={kwargs.get('short_name')}.",
        f"Conference already exists with long_name={kwargs.get('long_name')}.",
    )
    fake_validate_is_unique.assert_has_calls([
        call('short_name', kwargs.get('short_name'), error_message=error_messages[0]),
        call('long_name', kwargs.get('long_name'), error_message=error_messages[1])
    ])
    fake_injector.get.assert_called_once_with(fake_league_repository)
    fake_league_repository.get_league_by_short_name.assert_called_once_with("L")

    assert isinstance(test_conference, Conference)
    assert test_conference.short_name == kwargs.get('short_name')
    assert test_conference.long_name == kwargs.get('long_name')
    assert test_conference.league_id == league.id
    assert test_conference.first_season_id == kwargs.get('first_season_year')
    assert test_conference.last_season_id == kwargs.get('last_season_year')


@patch('app.data.factories.conference_factory._validate_is_unique')
@patch('app.data.factories.conference_factory.LeagueRepository')
@patch('app.data.factories.conference_factory.injector')
def test_create_conference_when_unique_keys_are_in_kwargs_and_old_conference_id_is_not_provided_and_kwargs_short_name_is_not_unique_should_raise_value_error(
        fake_injector, fake_league_repository,
        fake_validate_is_unique
):
    # Arrange
    fake_validate_is_unique.return_value = None

    league = League(
        id=1,
        short_name="L",
        long_name="League",
        first_season_id=1920
    )
    fake_league_repository.get_league_by_short_name.return_value = league

    fake_injector.get.return_value = fake_league_repository

    kwargs = {
        'short_name': "C",
        'long_name': "Conference",
        'league_name': league.short_name,
        'first_season_year': 1920,
        'last_season_year': None,
    }

    error_message = f"Conference already exists with short_name={kwargs.get('short_name')}."
    fake_validate_is_unique.side_effect = ValueError(error_message)

    # Act
    with pytest.raises(ValueError) as err:
        test_conference = conference_factory.create_conference(**kwargs)

    # Assert
    fake_validate_is_unique.assert_called_once_with('short_name', kwargs.get('short_name'), error_message=error_message)
    assert err.value.args[0] == error_message
    fake_injector.get.assert_not_called()
    fake_league_repository.get_league_by_short_name.assert_not_called()


@patch('app.data.factories.conference_factory._validate_is_unique')
@patch('app.data.factories.conference_factory.LeagueRepository')
@patch('app.data.factories.conference_factory.injector')
def test_create_conference_when_unique_keys_are_in_kwargs_and_old_conference_id_is_not_provided_and_kwargs_long_name_is_not_unique_should_raise_value_error(
        fake_injector, fake_league_repository,
        fake_validate_is_unique
):
    # Arrange
    league = League(
        id=1,
        short_name="L",
        long_name="League",
        first_season_id=1920
    )
    fake_league_repository.get_league_by_short_name.return_value = league

    fake_injector.get.return_value = fake_league_repository

    kwargs = {
        'short_name': "C",
        'long_name': "Conference",
        'league_name': league.short_name,
        'first_season_year': 1920,
        'last_season_year': None,
    }

    error_messages = (
        f"Conference already exists with short_name={kwargs.get('short_name')}.",
        f"Conference already exists with long_name={kwargs.get('long_name')}.",
    )
    fake_validate_is_unique.side_effect = [None, ValueError(error_messages[1])]

    # Act
    with pytest.raises(ValueError) as err:
        test_conference = conference_factory.create_conference(**kwargs)

    # Assert
    fake_validate_is_unique.assert_has_calls([
        call('short_name', kwargs.get('short_name'), error_message=error_messages[0]),
        call('long_name', kwargs.get('long_name'), error_message=error_messages[1])
    ])
    assert err.value.args[0] == error_messages[1]
    fake_injector.get.assert_not_called()
    fake_league_repository.get_league_by_short_name.assert_not_called()


@patch('app.data.factories.conference_factory._validate_is_unique')
@patch('app.data.factories.conference_factory.LeagueRepository')
@patch('app.data.factories.conference_factory.ConferenceRepository')
@patch('app.data.factories.conference_factory.injector')
def test_create_conference_when_unique_keys_are_in_kwargs_and_old_conference_id_is_provided_and_short_name_and_long_name_have_not_changed_should_not_validate_unique_key_values_and_return_conference(
        fake_injector, fake_conference_repository, fake_league_repository,
        fake_validate_is_unique
):
    # Arrange
    league = League(
        id=1,
        short_name="L",
        long_name="League",
        first_season_id=1920
    )

    kwargs = {
        'id': 1,
        'short_name': "C",
        'long_name': "Conference",
        'league_name': league.short_name,
        'first_season_year': 1920,
        'last_season_year': None,
    }

    old_conference = Conference(
        short_name=kwargs.get('short_name'),
        long_name=kwargs.get('long_name'),
        league_id=league.id,
        first_season_id=kwargs.get('first_season_year')
    )

    fake_conference_repository.get_conference.return_value = old_conference
    fake_league_repository.get_league_by_short_name.return_value = league
    fake_injector.get.side_effect = [fake_conference_repository, fake_conference_repository, fake_league_repository]

    # Act
    try:
        test_conference = conference_factory.create_conference(**kwargs)
    except ValueError:
        assert False

    # Assert
    fake_injector.get.assert_has_calls([
        call(fake_conference_repository),
        call(fake_conference_repository),
        call(fake_league_repository),
    ])
    fake_conference_repository.get_conference.assert_has_calls([
        call(kwargs.get('id')),
        call(kwargs.get('id')),
    ])
    fake_validate_is_unique.assert_not_called()
    fake_league_repository.get_league_by_short_name.assert_called_once_with("L")

    assert isinstance(test_conference, Conference)
    assert test_conference.id == kwargs.get('id')
    assert test_conference.short_name == kwargs.get('short_name')
    assert test_conference.long_name == kwargs.get('long_name')
    assert test_conference.league_id == league.id
    assert test_conference.first_season_id == kwargs.get('first_season_year')
    assert test_conference.last_season_id == kwargs.get('last_season_year')


@patch('app.data.factories.conference_factory._validate_is_unique')
@patch('app.data.factories.conference_factory.LeagueRepository')
@patch('app.data.factories.conference_factory.ConferenceRepository')
@patch('app.data.factories.conference_factory.injector')
def test_create_conference_when_unique_keys_are_in_kwargs_and_old_conference_id_is_provided_and_short_name_has_changed_and_is_unique_should_validate_unique_key_values_and_return_conference(
        fake_injector, fake_conference_repository, fake_league_repository,
        fake_validate_is_unique
):
    # Arrange
    league = League(
        id=1,
        short_name="L",
        long_name="League",
        first_season_id=1920
    )

    kwargs = {
        'id': 1,
        'short_name': "NC",
        'long_name': "Conference",
        'league_name': league.short_name,
        'first_season_year': 1922,
        'last_season_year': None,
    }

    old_conference = Conference(
        short_name="OC",
        long_name="Conference",
        league_id=league.id,
        first_season_id=1920,
        last_season_id=1921
    )

    fake_conference_repository.get_conference.return_value = old_conference
    fake_league_repository.get_league_by_short_name.return_value = league
    fake_injector.get.side_effect = [fake_conference_repository, fake_conference_repository, fake_league_repository]

    fake_validate_is_unique.return_value = True

    # Act
    try:
        test_conference = conference_factory.create_conference(**kwargs)
    except ValueError:
        assert False

    # Assert
    fake_injector.get.assert_has_calls([
        call(fake_conference_repository),
        call(fake_conference_repository),
        call(fake_league_repository),
    ])
    fake_conference_repository.get_conference.assert_has_calls([
        call(kwargs.get('id')),
        call(kwargs.get('id')),
    ])
    fake_validate_is_unique.assert_called_once_with(
        'short_name', kwargs.get('short_name'),
        error_message=f"Conference already exists with short_name={kwargs.get('short_name')}."
    )
    fake_league_repository.get_league_by_short_name.assert_called_once_with("L")

    assert isinstance(test_conference, Conference)
    assert test_conference.id == kwargs.get('id')
    assert test_conference.short_name == kwargs.get('short_name')
    assert test_conference.long_name == kwargs.get('long_name')
    assert test_conference.league_id == league.id
    assert test_conference.first_season_id == kwargs.get('first_season_year')
    assert test_conference.last_season_id == kwargs.get('last_season_year')


@patch('app.data.factories.conference_factory._validate_is_unique')
@patch('app.data.factories.conference_factory.LeagueRepository')
@patch('app.data.factories.conference_factory.ConferenceRepository')
@patch('app.data.factories.conference_factory.injector')
def test_create_conference_when_unique_keys_are_in_kwargs_and_old_conference_id_is_provided_and_short_name_has_changed_and_is_not_unique_should_validate_unique_key_values_and_raise_value_error(
        fake_injector, fake_conference_repository, fake_league_repository,
        fake_validate_is_unique
):
    # Arrange
    league = League(
        id=1,
        short_name="L",
        long_name="League",
        first_season_id=1920
    )

    kwargs = {
        'id': 1,
        'short_name': "NC",
        'long_name': "Conference",
        'league_name': league.short_name,
        'first_season_year': 1922,
        'last_season_year': None,
    }

    old_conference = Conference(
        short_name="OC",
        long_name="Conference",
        league_id=league.id,
        first_season_id=1920,
        last_season_id=1921
    )

    fake_conference_repository.get_conference.return_value = old_conference
    fake_league_repository.get_league_by_short_name.return_value = league
    fake_injector.get.side_effect = [fake_conference_repository, fake_conference_repository, fake_league_repository]

    fake_validate_is_unique.side_effect = ValueError("short_name must be unique.")

    # Act
    with pytest.raises(ValueError) as err:
        test_conference = conference_factory.create_conference(**kwargs)

    # Assert
    fake_injector.get.assert_called_once_with(fake_conference_repository)
    fake_conference_repository.get_conference.assert_called_once_with(kwargs.get('id'))
    fake_validate_is_unique.assert_called_once_with(
        'short_name', kwargs.get('short_name'),
        error_message=f"Conference already exists with short_name={kwargs.get('short_name')}."
    ),


@patch('app.data.factories.conference_factory._validate_is_unique')
@patch('app.data.factories.conference_factory.LeagueRepository')
@patch('app.data.factories.conference_factory.ConferenceRepository')
@patch('app.data.factories.conference_factory.injector')
def test_create_conference_when_unique_keys_are_in_kwargs_and_old_conference_id_is_provided_and_long_name_has_changed_and_is_unique_should_validate_unique_key_values_and_return_conference(
        fake_injector, fake_conference_repository, fake_league_repository,
        fake_validate_is_unique
):
    # Arrange
    league = League(
        id=1,
        short_name="L",
        long_name="League",
        first_season_id=1920
    )

    kwargs = {
        'id': 1,
        'short_name': "C",
        'long_name': "New Conference",
        'league_name': league.short_name,
        'first_season_year': 1922,
        'last_season_year': None,
    }

    old_conference = Conference(
        short_name="C",
        long_name="Old Conference",
        league_id=league.id,
        first_season_id=1920,
        last_season_id=1921
    )

    fake_conference_repository.get_conference.return_value = old_conference
    fake_league_repository.get_league_by_short_name.return_value = league
    fake_injector.get.side_effect = [fake_conference_repository, fake_conference_repository, fake_league_repository]

    fake_validate_is_unique.side_effect = [False, True]

    # Act
    try:
        test_conference = conference_factory.create_conference(**kwargs)
    except ValueError:
        assert False

    # Assert
    fake_injector.get.assert_has_calls([
        call(fake_conference_repository),
        call(fake_conference_repository),
        call(fake_league_repository),
    ])
    fake_conference_repository.get_conference.assert_has_calls([
        call(kwargs.get('id')),
        call(kwargs.get('id')),
    ])
    fake_validate_is_unique.assert_has_calls([
        call('long_name', kwargs.get('long_name'), error_message=f"Conference already exists with long_name={kwargs.get('long_name')}."),
    ])
    fake_league_repository.get_league_by_short_name.assert_called_once_with("L")

    assert isinstance(test_conference, Conference)
    assert test_conference.id == kwargs.get('id')
    assert test_conference.short_name == kwargs.get('short_name')
    assert test_conference.long_name == kwargs.get('long_name')
    assert test_conference.league_id == league.id
    assert test_conference.first_season_id == kwargs.get('first_season_year')
    assert test_conference.last_season_id == kwargs.get('last_season_year')


@patch('app.data.factories.conference_factory._validate_is_unique')
@patch('app.data.factories.conference_factory.LeagueRepository')
@patch('app.data.factories.conference_factory.ConferenceRepository')
@patch('app.data.factories.conference_factory.injector')
def test_create_conference_when_unique_keys_are_in_kwargs_and_old_conference_id_is_provided_and_long_name_has_changed_and_is_not_unique_should_validate_unique_key_values_and_raise_value_error(
        fake_injector, fake_conference_repository, fake_league_repository,
        fake_validate_is_unique
):
    # Arrange
    league = League(
        id=1,
        short_name="L",
        long_name="League",
        first_season_id=1920
    )

    kwargs = {
        'id': 1,
        'short_name': "C",
        'long_name': "New Conference",
        'league_name': league.short_name,
        'first_season_year': 1922,
        'last_season_year': None,
    }

    old_conference = Conference(
        short_name="C",
        long_name="Old Conference",
        league_id=league.id,
        first_season_id=1920,
        last_season_id=1921
    )

    fake_conference_repository.get_conference.return_value = old_conference
    fake_league_repository.get_league_by_short_name.return_value = league
    fake_injector.get.side_effect = [fake_conference_repository, fake_conference_repository, fake_league_repository]

    fake_validate_is_unique.side_effect = ValueError("long_name must be unique.")

    # Act
    with pytest.raises(ValueError) as err:
        test_conference = conference_factory.create_conference(**kwargs)

    # Assert
    fake_injector.get.assert_has_calls([
        call(fake_conference_repository),
        call(fake_conference_repository),
    ])
    fake_conference_repository.get_conference.assert_has_calls([
        call(kwargs.get('id')),
        call(kwargs.get('id')),
    ])
    fake_validate_is_unique.assert_called_once_with(
        'long_name', kwargs.get('long_name'),
        error_message=f"Conference already exists with long_name={kwargs.get('long_name')}."
    )


@patch('app.data.factories.conference_factory.Conference')
def test_validate_is_unique_when_value_is_not_unique_and_error_message_is_not_provided_should_raise_value_error_with_default_error_message(fake_conference):
    # Arrange
    fake_conference.query.filter_by.return_value.first.return_value = Conference()

    # Act
    with pytest.raises(ValueError) as err:
        result = conference_factory._validate_is_unique('short_name', "C")

    # Assert
    assert err.value.args[0] == "short_name must be unique."


@patch('app.data.factories.conference_factory.Conference')
def test_validate_is_unique_when_value_is_not_unique_and_error_message_is_provided_should_raise_value_error_with_provided_error_message(fake_conference):
    # Arrange
    fake_conference.query.filter_by.return_value.first.return_value = Conference()

    error_message = f"Conference already exists with short_name=C."

    # Act
    with pytest.raises(ValueError) as err:
        result = conference_factory._validate_is_unique('short_name', "C", error_message=error_message)

    # Assert
    assert err.value.args[0] == error_message


@patch('app.data.factories.conference_factory.ConferenceRepository')
@patch('app.data.factories.conference_factory.injector')
def test_value_has_changed_when_new_value_equals_old_value_should_return_false(
        fake_injector, fake_conference_repository
):
    # Arrange
    kwargs = {
        'id': 1,
        'short_name': "C",
    }

    old_conference = Conference(
        short_name="C",
        long_name="Conference",
        league_id=1,
        first_season_id=1920
    )
    fake_conference_repository.get_conference.return_value = old_conference
    fake_injector.get.return_value = fake_conference_repository

    # Act
    result = conference_factory._value_has_changed('short_name', **kwargs)

    # Assert
    assert result is False
    fake_injector.get.assert_called_once_with(fake_conference_repository)
    fake_conference_repository.get_conference.assert_called_once_with(kwargs.get('id'))


@patch('app.data.factories.conference_factory.ConferenceRepository')
@patch('app.data.factories.conference_factory.injector')
def test_value_has_changed_when_new_value_does_not_equal_old_value_should_return_true(
        fake_injector, fake_conference_repository
):
    # Arrange
    kwargs = {
        'id': 1,
        'short_name': "NC",
    }

    old_conference = Conference(
        short_name="OC",
        long_name="Conference",
        league_id=1,
        first_season_id=1920
    )
    fake_conference_repository.get_conference.return_value = old_conference
    fake_injector.get.return_value = fake_conference_repository

    # Act
    result = conference_factory._value_has_changed('short_name', **kwargs)

    # Assert
    assert result is True
    fake_injector.get.assert_called_once_with(fake_conference_repository)
    fake_conference_repository.get_conference.assert_called_once_with(kwargs.get('id'))
