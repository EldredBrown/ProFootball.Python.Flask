from unittest.mock import patch, MagicMock

import pytest

from app.data.factories import league_season_factory
from app.data.models.league import League
from app.data.models.league_season import LeagueSeason
from app.data.models.season import Season
from app.data.repositories.league_repository import LeagueRepository
from app.data.repositories.league_season_repository import LeagueSeasonRepository


def test_create_league_season_when_key_is_not_in_view_model_map_should_raise_value_error():
    # Arrange
    kwargs = {
        'invalid_key': "Value"
    }

    # Act
    with pytest.raises(KeyError) as err:
        test_league_season = league_season_factory.create_league_season(**kwargs)

    # Assert
    assert err.value.args[0] == f"invalid_key is invalid."


@patch('app.data.factories.league_season_factory._validate_is_unique')
@patch('app.data.factories.league_season_factory.injector')
def test_create_league_season_when_unique_keys_are_in_kwargs_and_old_league_season_id_is_not_provided_and_kwargs_league_name_and_season_year_are_unique_should_return_league_season(
        fake_injector, fake_validate_is_unique
):
    # Arrange
    fake_league_repository = MagicMock(LeagueRepository)
    league = League(id=1)
    fake_league_repository.get_league_by_short_name.return_value = league
    fake_injector.get.return_value = fake_league_repository

    kwargs = {
        'league_name': "L",
        'season_year': 1920,
    }

    fake_validate_is_unique.return_value = None

    # Act
    try:
        test_league_season = league_season_factory.create_league_season(**kwargs)
    except ValueError:
        assert False

    # Assert
    fake_injector.get.assert_called_once_with(LeagueRepository)
    fake_league_repository.get_league_by_short_name.assert_called_once_with(kwargs.get('league_name'))

    league_id = 1
    season_id = 1920
    error_message = f"LeagueSeason already exists with league_id={league_id} and season_id={season_id}."
    fake_validate_is_unique.assert_called_once_with(league_id, season_id, error_message=error_message)

    assert isinstance(test_league_season, LeagueSeason)
    assert test_league_season.league_id == league_id
    assert test_league_season.season_id == season_id


@patch('app.data.factories.league_season_factory._validate_is_unique')
@patch('app.data.factories.league_season_factory.injector')
def test_create_league_season_when_unique_keys_are_in_kwargs_and_old_league_season_id_is_not_provided_and_kwargs_league_name_and_season_year_are_not_unique_should_raise_value_error(
        fake_injector, fake_validate_is_unique
):
    # Arrange
    fake_league_repository = MagicMock(LeagueRepository)
    league = League(id=1)
    fake_league_repository.get_league_by_short_name.return_value = league
    fake_injector.get.return_value = fake_league_repository

    kwargs = {
        'league_name': "L",
        'season_year': 1920,
    }

    league_id = 1
    season_id = 1920
    error_message = f"LeagueSeason already exists with league_id={league_id} and season_id={season_id}."
    fake_validate_is_unique.side_effect = ValueError(error_message)

    # Act
    with pytest.raises(ValueError) as err:
        _ = league_season_factory.create_league_season(**kwargs)

    # Assert
    fake_validate_is_unique.assert_called_once_with(league_id, season_id, error_message=error_message)
    assert err.value.args[0] == error_message


@patch('app.data.factories.league_season_factory._validate_is_unique')
@patch('app.data.factories.league_season_factory._values_have_changed')
@patch('app.data.factories.league_season_factory.LeagueSeasonRepository')
@patch('app.data.factories.league_season_factory.injector')
def test_create_league_season_when_unique_keys_are_in_kwargs_and_old_league_season_id_is_provided_and_kwargs_league_id_and_season_id_have_not_changed_should_not_validate_unique_key_values_and_return_league_season(
        fake_injector, fake_league_season_repository,
        fake_values_have_changed, fake_validate_is_unique
):
    # Arrange
    fake_league_repository = MagicMock(LeagueRepository)
    league = League(id=1, short_name="L")
    fake_league_repository.get_league_by_short_name.return_value = league
    fake_injector.get.return_value = fake_league_repository

    season = Season(id=1920)

    view_kwargs = {
        'id': 1,
        'league_name': league.short_name,
        'season_year': season.id,
    }

    fake_values_have_changed.return_value = False

    # Act
    try:
        test_league_season = league_season_factory.create_league_season(**view_kwargs)
    except ValueError:
        assert False

    # Assert
    fake_injector.get.assert_called_once_with(LeagueRepository)
    fake_league_repository.get_league_by_short_name.assert_called_once_with(view_kwargs.get('league_name'))

    model_kwargs = {
        'id': 1,
        'league_id': league.id,
        'season_id': season.id,
    }
    fake_values_have_changed.assert_called_once_with(**model_kwargs)
    fake_validate_is_unique.assert_not_called()

    assert isinstance(test_league_season, LeagueSeason)
    assert test_league_season.id == view_kwargs.get('id')
    assert test_league_season.league_id == league.id
    assert test_league_season.season_id == season.id


@patch('app.data.factories.league_season_factory._validate_is_unique')
@patch('app.data.factories.league_season_factory._values_have_changed')
@patch('app.data.factories.league_season_factory.LeagueSeasonRepository')
@patch('app.data.factories.league_season_factory.injector')
def test_create_league_season_when_unique_keys_are_in_kwargs_and_old_league_season_id_is_provided_and_values_have_changed_and_kwargs_league_id_and_season_id_are_unique_should_validate_unique_key_values_and_return_league_season(
        fake_injector, fake_league_season_repository,
        fake_values_have_changed, fake_validate_is_unique
):
    # Arrange
    fake_league_repository = MagicMock(LeagueRepository)
    league = League(id=1, short_name="L")
    fake_league_repository.get_league_by_short_name.return_value = league
    fake_injector.get.return_value = fake_league_repository

    season = Season(id=1920)

    view_kwargs = {
        'id': 1,
        'league_name': league.short_name,
        'season_year': season.id,
    }

    fake_values_have_changed.return_value = True
    fake_validate_is_unique.return_value = None

    # Act
    try:
        test_league_season = league_season_factory.create_league_season(**view_kwargs)
    except ValueError:
        assert False

    # Assert
    fake_injector.get.assert_called_once_with(LeagueRepository)
    fake_league_repository.get_league_by_short_name.assert_called_once_with(view_kwargs.get('league_name'))

    model_kwargs = {
        'id': 1,
        'league_id': league.id,
        'season_id': season.id,
    }
    fake_values_have_changed.assert_called_once_with(**model_kwargs)
    error_message = f"LeagueSeason already exists with league_id={league.id} and season_id={season.id}."
    fake_validate_is_unique.assert_called_once_with(league.id, season.id, error_message=error_message)

    assert isinstance(test_league_season, LeagueSeason)
    assert test_league_season.id == view_kwargs.get('id')
    assert test_league_season.league_id == league.id
    assert test_league_season.season_id == season.id


@patch('app.data.factories.league_season_factory.injector')
def test_values_have_changed_when_values_have_not_changed_should_return_false(fake_injector):
    # Arrange
    kwargs = {
        'id': 1,
        'league_id': 1,
        'season_id': 1920,
    }

    fake_league_season_repository = MagicMock(LeagueSeasonRepository)
    old_league_season = LeagueSeason(id=1, league_id=1, season_id=1920)
    fake_league_season_repository.get_league_season.return_value = old_league_season
    fake_injector.get.return_value = fake_league_season_repository

    # Act
    result = league_season_factory._values_have_changed(**kwargs)

    # Assert
    fake_injector.get.assert_called_once_with(LeagueSeasonRepository)
    fake_league_season_repository.get_league_season.assert_called_once_with(kwargs.get('id'))
    assert result is False


@patch('app.data.factories.league_season_factory.injector')
def test_values_have_changed_when_season_id_has_changed_should_return_true(fake_injector):
    # Arrange
    kwargs = {
        'id': 1,
        'league_id': 1,
        'season_id': 1920,
    }

    fake_league_season_repository = MagicMock(LeagueSeasonRepository)
    old_league_season = LeagueSeason(id=1, league_id=1, season_id=1921)
    fake_league_season_repository.get_league_season.return_value = old_league_season
    fake_injector.get.return_value = fake_league_season_repository

    # Act
    result = league_season_factory._values_have_changed(**kwargs)

    # Assert
    fake_injector.get.assert_called_once_with(LeagueSeasonRepository)
    fake_league_season_repository.get_league_season.assert_called_once_with(kwargs.get('id'))
    assert result is True


@patch('app.data.factories.league_season_factory.injector')
def test_values_have_changed_when_league_id_has_changed_should_return_true(fake_injector):
    # Arrange
    kwargs = {
        'id': 1,
        'league_id': 1,
        'season_id': 1920,
    }

    fake_league_season_repository = MagicMock(LeagueSeasonRepository)
    old_league_season = LeagueSeason(id=1, league_id=2, season_id=1921)
    fake_league_season_repository.get_league_season.return_value = old_league_season
    fake_injector.get.return_value = fake_league_season_repository

    # Act
    result = league_season_factory._values_have_changed(**kwargs)

    # Assert
    fake_injector.get.assert_called_once_with(LeagueSeasonRepository)
    fake_league_season_repository.get_league_season.assert_called_once_with(kwargs.get('id'))
    assert result is True


@patch('app.data.factories.league_season_factory.LeagueSeason')
@patch('app.data.factories.league_season_factory.injector')
def test_validate_is_unique_when_values_are_not_unique_and_error_message_is_not_provided_should_raise_value_error_with_default_error_message(
        fake_injector, fake_league_season
):
    # Arrange
    fake_league_season_repository = MagicMock(LeagueSeasonRepository)
    league_id = 1
    season_id = 1920
    league_season = LeagueSeason(id=1, league_id=league_id, season_id=season_id)
    fake_league_season_repository.get_league_season_by_league_and_season.return_value = league_season
    fake_injector.get.return_value = fake_league_season_repository

    fake_league_season.query.filter_by.return_value.first.return_value = LeagueSeason()

    # Act
    with pytest.raises(ValueError) as err:
        league_season_factory._validate_is_unique(league_id, season_id)

    # Assert
    fake_injector.get.assert_called_once_with(LeagueSeasonRepository)
    fake_league_season_repository.get_league_season_by_league_and_season.assert_called_once_with(
        league_id=league_id, season_id=season_id
    )
    assert err.value.args[0] == "league_id and season_id together must be unique."


@patch('app.data.factories.league_season_factory.LeagueSeason')
@patch('app.data.factories.league_season_factory.injector')
def test_validate_is_unique_when_values_are_not_unique_and_error_message_is_provided_should_raise_value_error_with_provided_error_message(
        fake_injector, fake_league_season
):
    # Arrange
    fake_league_season_repository = MagicMock(LeagueSeasonRepository)
    league_id = 1
    season_id = 1920
    league_season = LeagueSeason(id=1, league_id=league_id, season_id=season_id)
    fake_league_season_repository.get_league_season_by_league_and_season.return_value = league_season
    fake_injector.get.return_value = fake_league_season_repository

    fake_league_season.query.filter_by.return_value.first.return_value = LeagueSeason()

    # Act
    with pytest.raises(ValueError) as err:
        league_season_factory._validate_is_unique(
            league_id, season_id, error_message="Test error message"
        )

    # Assert
    fake_injector.get.assert_called_once_with(LeagueSeasonRepository)
    fake_league_season_repository.get_league_season_by_league_and_season.assert_called_once_with(
        league_id=league_id, season_id=season_id
    )
    assert err.value.args[0] == "Test error message"


@patch('app.data.factories.league_season_factory.LeagueSeason')
@patch('app.data.factories.league_season_factory.injector')
def test_validate_is_unique_when_values_are_unique_should_not_raise_value_error(
        fake_injector, fake_league_season
):
    # Arrange
    fake_league_season_repository = MagicMock(LeagueSeasonRepository)
    fake_league_season_repository.get_league_season_by_league_and_season.return_value = None
    fake_injector.get.return_value = fake_league_season_repository

    fake_league_season.query.filter_by.return_value.first.return_value = LeagueSeason()

    league_id = 1
    season_id = 1920

    # Act
    try:
        league_season_factory._validate_is_unique(league_id, season_id, error_message="Test error message")
    except ValueError:
        assert False

    # Assert
    fake_injector.get.assert_called_once_with(LeagueSeasonRepository)
    fake_league_season_repository.get_league_season_by_league_and_season.assert_called_once_with(
        league_id=league_id, season_id=season_id
    )
