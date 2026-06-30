from unittest.mock import patch, call

import pytest

from app.data.factories import division_factory
from app.data.models.conference import Conference
from app.data.models.division import Division
from app.data.models.league import League


def test_create_division_when_key_is_not_in_view_model_map_should_raise_value_error():
    # Arrange
    kwargs = {
        'invalid_key': "Value"
    }

    # Act
    with pytest.raises(KeyError) as err:
        test_division = division_factory.create_division(**kwargs)

    # Assert
    assert err.value.args[0] == f"invalid_key is invalid."


@patch('app.data.factories.division_factory._validate_is_unique')
@patch('app.data.factories.division_factory.ConferenceRepository')
@patch('app.data.factories.division_factory.LeagueRepository')
@patch('app.data.factories.division_factory.injector')
def test_create_division_when_name_is_in_kwargs_and_old_division_id_is_not_provided_and_kwargs_name_is_unique_should_return_division(
        fake_injector, fake_league_repository,
        fake_conference_repository, fake_validate_is_unique
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

    conference = Conference(
        id=1,
        short_name="C",
        long_name="Conference",
        first_season_id=1920
    )
    fake_conference_repository.get_conference_by_short_name.return_value = conference

    fake_injector.get.side_effect = [fake_league_repository, fake_conference_repository]

    kwargs = {
        'name': "Division",
        'league_name': league.short_name,
        'conference_name': conference.short_name,
        'first_season_year': 1920,
        'last_season_year': None,
    }

    # Act
    try:
        test_division = division_factory.create_division(**kwargs)
    except ValueError:
        assert False

    # Assert
    error_message = f"Division already exists with name={kwargs.get('name')}."
    fake_validate_is_unique.assert_called_once_with('name', kwargs.get('name'), error_message=error_message)
    fake_injector.get.assert_has_calls([
        call(fake_league_repository),
        call(fake_conference_repository),
    ])
    fake_league_repository.get_league_by_short_name.assert_called_once_with("L")
    fake_conference_repository.get_conference_by_short_name.assert_called_once_with("C")

    assert isinstance(test_division, Division)
    assert test_division.name == kwargs.get('name')
    assert test_division.league_id == league.id
    assert test_division.conference_id == conference.id
    assert test_division.first_season_id == kwargs.get('first_season_year')
    assert test_division.last_season_id == kwargs.get('last_season_year')


@patch('app.data.factories.division_factory._validate_is_unique')
@patch('app.data.factories.division_factory.ConferenceRepository')
@patch('app.data.factories.division_factory.LeagueRepository')
@patch('app.data.factories.division_factory.injector')
def test_create_division_when_name_is_in_kwargs_and_old_division_id_is_not_provided_and_kwargs_name_is_not_unique_should_raise_value_error(
        fake_injector, fake_league_repository,
        fake_conference_repository, fake_validate_is_unique
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

    conference = Conference(
        id=1,
        short_name="C",
        long_name="Conference",
        first_season_id=1920
    )
    fake_conference_repository.get_conference_by_short_name.return_value = conference

    fake_injector.get.side_effect = [fake_league_repository, fake_conference_repository]

    kwargs = {
        'name': "Division",
        'league_name': league.short_name,
        'conference_name': conference.short_name,
        'first_season_year': 1920,
        'last_season_year': None,
    }

    error_message = f"Division already exists with name={kwargs.get('name')}."
    fake_validate_is_unique.side_effect = ValueError(error_message)

    # Act
    with pytest.raises(ValueError) as err:
        test_division = division_factory.create_division(**kwargs)

    # Assert
    fake_validate_is_unique.assert_called_once_with('name', kwargs.get('name'), error_message=error_message)
    assert err.value.args[0] == error_message
    fake_injector.get.assert_not_called()
    fake_league_repository.get_league_by_short_name.assert_not_called()


@patch('app.data.factories.division_factory._validate_is_unique')
@patch('app.data.factories.division_factory.ConferenceRepository')
@patch('app.data.factories.division_factory.LeagueRepository')
@patch('app.data.factories.division_factory.DivisionRepository')
@patch('app.data.factories.division_factory.injector')
def test_create_division_when_name_is_in_kwargs_and_old_division_id_is_provided_and_name_has_not_changed_should_not_validate_name_and_return_division(
        fake_injector, fake_division_repository,
        fake_league_repository, fake_conference_repository,
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

    conference = Conference(
        id=1,
        short_name="C",
        long_name="Conference",
        first_season_id=1920
    )

    kwargs = {
        'id': 1,
        'name': "Division",
        'league_name': league.short_name,
        'conference_name': conference.short_name,
        'first_season_year': 1920,
        'last_season_year': None,
    }

    old_division = Division(
        name=kwargs.get('name'),
        league_id=league.id,
        conference_id=conference.id,
        first_season_id=kwargs.get('first_season_year')
    )

    fake_division_repository.get_division.return_value = old_division
    fake_league_repository.get_league_by_short_name.return_value = league
    fake_conference_repository.get_conference_by_short_name.return_value = conference
    fake_injector.get.side_effect = [fake_division_repository, fake_league_repository, fake_conference_repository]

    # Act
    try:
        test_division = division_factory.create_division(**kwargs)
    except ValueError:
        assert False

    # Assert
    fake_injector.get.assert_has_calls([
        call(fake_division_repository),
        call(fake_league_repository),
        call(fake_conference_repository),
    ])
    fake_division_repository.get_division.assert_called_once_with(kwargs.get('id'))
    fake_validate_is_unique.assert_not_called()
    fake_league_repository.get_league_by_short_name.assert_called_once_with("L")
    fake_conference_repository.get_conference_by_short_name.assert_called_once_with("C")

    assert isinstance(test_division, Division)
    assert test_division.id == kwargs.get('id')
    assert test_division.name == kwargs.get('name')
    assert test_division.league_id == league.id
    assert test_division.conference_id == conference.id
    assert test_division.first_season_id == kwargs.get('first_season_year')
    assert test_division.last_season_id == kwargs.get('last_season_year')


@patch('app.data.factories.division_factory._validate_is_unique')
@patch('app.data.factories.division_factory.ConferenceRepository')
@patch('app.data.factories.division_factory.LeagueRepository')
@patch('app.data.factories.division_factory.DivisionRepository')
@patch('app.data.factories.division_factory.injector')
def test_create_division_when_name_is_in_kwargs_and_old_division_id_is_provided_and_name_has_changed_and_is_unique_should_validate_unique_key_values_and_return_division(
        fake_injector, fake_division_repository,
        fake_league_repository, fake_conference_repository,
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

    conference = Conference(
        id=1,
        short_name="C",
        long_name="Conference",
        first_season_id=1920
    )

    kwargs = {
        'id': 1,
        'name': "New Division",
        'league_name': league.short_name,
        'conference_name': conference.short_name,
        'first_season_year': 1920,
        'last_season_year': None,
    }

    old_division = Division(
        name="Old Division",
        league_id=league.id,
        conference_id=conference.id,
        first_season_id=kwargs.get('first_season_year')
    )

    fake_division_repository.get_division.return_value = old_division
    fake_league_repository.get_league_by_short_name.return_value = league
    fake_conference_repository.get_conference_by_short_name.return_value = conference
    fake_injector.get.side_effect = [fake_division_repository, fake_league_repository, fake_conference_repository]

    fake_validate_is_unique.return_value = True

    # Act
    try:
        test_division = division_factory.create_division(**kwargs)
    except ValueError:
        assert False

    # Assert
    fake_injector.get.assert_has_calls([
        call(fake_division_repository),
        call(fake_league_repository),
        call(fake_conference_repository),
    ])
    fake_division_repository.get_division.assert_called_once_with(kwargs.get('id'))
    fake_validate_is_unique.assert_called_once_with(
        'name', kwargs.get('name'), error_message=f"Division already exists with name={kwargs.get('name')}."
    )
    fake_league_repository.get_league_by_short_name.assert_called_once_with("L")
    fake_conference_repository.get_conference_by_short_name.assert_called_once_with("C")

    assert isinstance(test_division, Division)
    assert test_division.id == kwargs.get('id')
    assert test_division.name == kwargs.get('name')
    assert test_division.league_id == league.id
    assert test_division.conference_id == conference.id
    assert test_division.first_season_id == kwargs.get('first_season_year')
    assert test_division.last_season_id == kwargs.get('last_season_year')


@patch('app.data.factories.division_factory._validate_is_unique')
@patch('app.data.factories.division_factory.ConferenceRepository')
@patch('app.data.factories.division_factory.LeagueRepository')
@patch('app.data.factories.division_factory.DivisionRepository')
@patch('app.data.factories.division_factory.injector')
def test_create_division_when_name_is_in_kwargs_and_old_division_id_is_provided_and_name_has_changed_and_is_not_unique_should_validate_unique_key_values_and_raise_value_error(
        fake_injector, fake_division_repository,
        fake_league_repository, fake_conference_repository,
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

    conference = Conference(
        id=1,
        short_name="C",
        long_name="Conference",
        first_season_id=1920
    )

    kwargs = {
        'id': 1,
        'name': "New Division",
        'league_name': league.short_name,
        'conference_name': conference.short_name,
        'first_season_year': 1920,
        'last_season_year': None,
    }

    old_division = Division(
        name="Old Division",
        league_id=league.id,
        conference_id=conference.id,
        first_season_id=kwargs.get('first_season_year')
    )

    fake_division_repository.get_division.return_value = old_division
    fake_league_repository.get_league_by_short_name.return_value = league
    fake_conference_repository.get_conference_by_short_name.return_value = conference
    fake_injector.get.side_effect = [fake_division_repository, fake_league_repository, fake_conference_repository]

    fake_validate_is_unique.side_effect = ValueError("name must be unique.")

    # Act
    with pytest.raises(ValueError) as err:
        test_division = division_factory.create_division(**kwargs)

    # Assert
    fake_injector.get.assert_called_once_with(fake_division_repository)
    fake_division_repository.get_division.assert_called_once_with(kwargs.get('id'))
    fake_validate_is_unique.assert_called_once_with(
        'name', kwargs.get('name'),
        error_message=f"Division already exists with name={kwargs.get('name')}."
    ),


@patch('app.data.factories.division_factory.Division')
def test_validate_is_unique_when_value_is_not_unique_and_error_message_is_not_provided_should_raise_value_error_with_default_error_message(fake_division):
    # Arrange
    fake_division.query.filter_by.return_value.first.return_value = Division()

    # Act
    with pytest.raises(ValueError) as err:
        result = division_factory._validate_is_unique('name', "Division")

    # Assert
    assert err.value.args[0] == "name must be unique."


@patch('app.data.factories.division_factory.Division')
def test_validate_is_unique_when_value_is_not_unique_and_error_message_is_provided_should_raise_value_error_with_provided_error_message(fake_division):
    # Arrange
    fake_division.query.filter_by.return_value.first.return_value = Division()

    error_message = f"Division already exists with name=Division."

    # Act
    with pytest.raises(ValueError) as err:
        result = division_factory._validate_is_unique('name', "Division", error_message=error_message)

    # Assert
    assert err.value.args[0] == error_message


@patch('app.data.factories.division_factory.DivisionRepository')
@patch('app.data.factories.division_factory.injector')
def test_value_has_changed_when_new_value_equals_old_value_should_return_false(
        fake_injector, fake_division_repository
):
    # Arrange
    kwargs = {
        'id': 1,
        'name': "Division",
    }

    old_division = Division(
        name="Division",
        league_id=1,
        first_season_id=1920
    )
    fake_division_repository.get_division.return_value = old_division
    fake_injector.get.return_value = fake_division_repository

    # Act
    result = division_factory._value_has_changed('name', **kwargs)

    # Assert
    assert result is False
    fake_injector.get.assert_called_once_with(fake_division_repository)
    fake_division_repository.get_division.assert_called_once_with(kwargs.get('id'))


@patch('app.data.factories.division_factory.DivisionRepository')
@patch('app.data.factories.division_factory.injector')
def test_value_has_changed_when_new_value_does_not_equal_old_value_should_return_true(
        fake_injector, fake_division_repository
):
    # Arrange
    kwargs = {
        'id': 1,
        'name': "New Division",
    }

    old_division = Division(
        name="Old Division",
        league_id=1,
        first_season_id=1920
    )
    fake_division_repository.get_division.return_value = old_division
    fake_injector.get.return_value = fake_division_repository

    # Act
    result = division_factory._value_has_changed('name', **kwargs)

    # Assert
    assert result is True
    fake_injector.get.assert_called_once_with(fake_division_repository)
    fake_division_repository.get_division.assert_called_once_with(kwargs.get('id'))
