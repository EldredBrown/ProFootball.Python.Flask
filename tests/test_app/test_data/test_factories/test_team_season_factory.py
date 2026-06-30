from unittest.mock import patch, MagicMock, call

import pytest

from app.data.factories import team_season_factory
from app.data.models.conference import Conference
from app.data.models.division import Division
from app.data.models.league import League
from app.data.models.season import Season
from app.data.models.team import Team
from app.data.models.team_season import TeamSeason
from app.data.repositories.conference_repository import ConferenceRepository
from app.data.repositories.division_repository import DivisionRepository
from app.data.repositories.league_repository import LeagueRepository
from app.data.repositories.team_repository import TeamRepository
from app.data.repositories.team_season_repository import TeamSeasonRepository


def test_create_team_season_when_key_is_not_in_view_model_map_should_raise_value_error():
    # Arrange
    kwargs = {
        'invalid_key': "Value"
    }

    # Act
    with pytest.raises(KeyError) as err:
        test_team_season = team_season_factory.create_team_season(**kwargs)

    # Assert
    assert err.value.args[0] == f"invalid_key is invalid."


@patch('app.data.factories.team_season_factory._validate_is_unique')
@patch('app.data.factories.team_season_factory.injector')
def test_create_team_season_when_unique_keys_are_in_kwargs_and_old_team_season_id_is_not_provided_and_kwargs_team_name_and_season_year_are_unique_should_return_team_season(
        fake_injector, fake_validate_is_unique
):
    # Arrange
    fake_team_repository = MagicMock(TeamRepository)
    team = Team(id=1, name="Team")
    fake_team_repository.get_team_by_name.return_value = team

    fake_league_repository = MagicMock(LeagueRepository)
    league = League(id=1, short_name="L", long_name="League")
    fake_league_repository.get_league_by_short_name.return_value = league

    fake_conference_repository = MagicMock(ConferenceRepository)
    conference = Conference(id=1, short_name="C", long_name="Conference")
    fake_conference_repository.get_conference_by_short_name.return_value = conference

    fake_division_repository = MagicMock(DivisionRepository)
    division = Division(id=1, name="Division")
    fake_division_repository.get_division_by_name.return_value = division

    fake_injector.get.side_effect = [
        fake_team_repository, fake_league_repository, fake_conference_repository, fake_division_repository
    ]

    season = Season(id=1920)

    kwargs = {
        'team_name': team.name,
        'season_year': season.id,
        'league_name': league.short_name,
        'conference_name': conference.short_name,
        'division_name': division.name,
    }

    fake_validate_is_unique.return_value = None

    # Act
    try:
        test_team_season = team_season_factory.create_team_season(**kwargs)
    except ValueError:
        assert False

    # Assert
    fake_injector.get.assert_has_calls([
        call(TeamRepository),
        call(LeagueRepository),
        call(ConferenceRepository),
        call(DivisionRepository),
    ])
    fake_team_repository.get_team_by_name.assert_called_once_with(team.name)
    fake_league_repository.get_league_by_short_name.assert_called_once_with(league.short_name)
    fake_conference_repository.get_conference_by_short_name.assert_called_once_with(conference.short_name)
    fake_division_repository.get_division_by_name.assert_called_once_with(division.name)

    error_message = f"TeamSeason already exists with team_id={team.id} and season_id={season.id}."
    fake_validate_is_unique.assert_called_once_with(team.id, season.id, error_message=error_message)

    assert isinstance(test_team_season, TeamSeason)
    assert test_team_season.team_id == team.id
    assert test_team_season.season_id == season.id


@patch('app.data.factories.team_season_factory._validate_is_unique')
@patch('app.data.factories.team_season_factory.injector')
def test_create_team_season_when_unique_keys_are_in_kwargs_and_old_team_season_id_is_not_provided_and_kwargs_team_name_and_season_year_are_not_unique_should_raise_value_error(
        fake_injector, fake_validate_is_unique
):
    # Arrange
    fake_team_repository = MagicMock(TeamRepository)
    team = Team(id=1, name="Team")
    fake_team_repository.get_team_by_name.return_value = team

    fake_league_repository = MagicMock(LeagueRepository)
    league = League(id=1, short_name="L", long_name="League")
    fake_league_repository.get_league_by_short_name.return_value = league

    fake_conference_repository = MagicMock(ConferenceRepository)
    conference = Conference(id=1, short_name="C", long_name="Conference")
    fake_conference_repository.get_conference_by_short_name.return_value = conference

    fake_division_repository = MagicMock(DivisionRepository)
    division = Division(id=1, name="Division")
    fake_division_repository.get_division_by_name.return_value = division

    fake_injector.get.side_effect = [
        fake_team_repository, fake_league_repository, fake_conference_repository, fake_division_repository
    ]

    season = Season(id=1920)
    kwargs = {
        'team_name': team.name,
        'season_year': season.id,
        'league_name': league.short_name,
        'conference_name': conference.short_name,
        'division_name': division.name,
    }

    error_message = f"TeamSeason already exists with team_id={team.id} and season_id={season.id}."
    fake_validate_is_unique.side_effect = ValueError(error_message)

    # Act
    with pytest.raises(ValueError) as err:
        _ = team_season_factory.create_team_season(**kwargs)

    # Assert
    fake_validate_is_unique.assert_called_once_with(team.id, season.id, error_message=error_message)
    assert err.value.args[0] == error_message


@patch('app.data.factories.team_season_factory._validate_is_unique')
@patch('app.data.factories.team_season_factory._values_have_changed')
@patch('app.data.factories.team_season_factory.TeamSeasonRepository')
@patch('app.data.factories.team_season_factory.injector')
def test_create_team_season_when_unique_keys_are_in_kwargs_and_old_team_season_id_is_provided_and_kwargs_team_id_and_season_id_have_not_changed_should_not_validate_unique_key_values_and_return_team_season(
        fake_injector, fake_team_season_repository,
        fake_values_have_changed, fake_validate_is_unique
):
    # Arrange
    fake_team_repository = MagicMock(TeamRepository)
    team = Team(id=1, name="Team")
    fake_team_repository.get_team_by_name.return_value = team

    fake_league_repository = MagicMock(LeagueRepository)
    league = League(id=1, short_name="L", long_name="League")
    fake_league_repository.get_league_by_short_name.return_value = league

    fake_conference_repository = MagicMock(ConferenceRepository)
    conference = Conference(id=1, short_name="C", long_name="Conference")
    fake_conference_repository.get_conference_by_short_name.return_value = conference

    fake_division_repository = MagicMock(DivisionRepository)
    division = Division(id=1, name="Division")
    fake_division_repository.get_division_by_name.return_value = division

    fake_injector.get.side_effect = [
        fake_team_repository, fake_league_repository, fake_conference_repository, fake_division_repository
    ]

    season = Season(id=1920)

    id = 1
    view_kwargs = {
        'id': id,
        'team_name': team.name,
        'season_year': season.id,
        'league_name': league.short_name,
        'conference_name': conference.short_name,
        'division_name': division.name,
    }

    fake_values_have_changed.return_value = False

    # Act
    try:
        test_team_season = team_season_factory.create_team_season(**view_kwargs)
    except ValueError:
        assert False

    # Assert
    fake_injector.get.assert_has_calls([
        call(TeamRepository),
        call(LeagueRepository),
        call(ConferenceRepository),
        call(DivisionRepository),
    ])
    fake_team_repository.get_team_by_name.assert_called_once_with(team.name)
    fake_league_repository.get_league_by_short_name.assert_called_once_with(league.short_name)
    fake_conference_repository.get_conference_by_short_name.assert_called_once_with(conference.short_name)
    fake_division_repository.get_division_by_name.assert_called_once_with(division.name)

    model_kwargs = {
        'id': id,
        'team_id': team.id,
        'season_id': season.id,
        'league_id': league.id,
        'conference_id': conference.id,
        'division_id': division.id,
    }
    fake_values_have_changed.assert_called_once_with(**model_kwargs)
    fake_validate_is_unique.assert_not_called()

    assert isinstance(test_team_season, TeamSeason)
    assert test_team_season.id == id
    assert test_team_season.team_id == team.id
    assert test_team_season.season_id == season.id
    assert test_team_season.league_id == league.id
    assert test_team_season.conference_id == conference.id
    assert test_team_season.division_id == division.id


@patch('app.data.factories.team_season_factory._validate_is_unique')
@patch('app.data.factories.team_season_factory._values_have_changed')
@patch('app.data.factories.team_season_factory.TeamSeasonRepository')
@patch('app.data.factories.team_season_factory.injector')
def test_create_team_season_when_unique_keys_are_in_kwargs_and_old_team_season_id_is_provided_and_values_have_changed_and_kwargs_team_id_and_season_id_are_unique_should_validate_unique_key_values_and_return_team_season(
        fake_injector, fake_team_season_repository,
        fake_values_have_changed, fake_validate_is_unique
):
    # Arrange
    fake_team_repository = MagicMock(TeamRepository)
    team = Team(id=1, name="Team")
    fake_team_repository.get_team_by_name.return_value = team

    fake_league_repository = MagicMock(LeagueRepository)
    league = League(id=1, short_name="L", long_name="League")
    fake_league_repository.get_league_by_short_name.return_value = league

    fake_conference_repository = MagicMock(ConferenceRepository)
    conference = Conference(id=1, short_name="C", long_name="Conference")
    fake_conference_repository.get_conference_by_short_name.return_value = conference

    fake_division_repository = MagicMock(DivisionRepository)
    division = Division(id=1, name="Division")
    fake_division_repository.get_division_by_name.return_value = division

    fake_injector.get.side_effect = [
        fake_team_repository, fake_league_repository, fake_conference_repository, fake_division_repository
    ]

    season = Season(id=1920)

    id = 1

    view_kwargs = {
        'id': id,
        'team_name': team.name,
        'season_year': season.id,
        'league_name': league.short_name,
        'conference_name': conference.short_name,
        'division_name': division.name,
    }

    fake_values_have_changed.return_value = True
    fake_validate_is_unique.return_value = None

    # Act
    try:
        test_team_season = team_season_factory.create_team_season(**view_kwargs)
    except ValueError:
        assert False

    # Assert
    fake_injector.get.assert_has_calls([
        call(TeamRepository),
        call(LeagueRepository),
        call(ConferenceRepository),
        call(DivisionRepository),
    ])
    fake_team_repository.get_team_by_name.assert_called_once_with(team.name)
    fake_league_repository.get_league_by_short_name.assert_called_once_with(league.short_name)
    fake_conference_repository.get_conference_by_short_name.assert_called_once_with(conference.short_name)
    fake_division_repository.get_division_by_name.assert_called_once_with(division.name)

    model_kwargs = {
        'id': id,
        'team_id': team.id,
        'season_id': season.id,
        'league_id': league.id,
        'conference_id': conference.id,
        'division_id': division.id,
    }
    fake_values_have_changed.assert_called_once_with(**model_kwargs)

    error_message = f"TeamSeason already exists with team_id={team.id} and season_id={season.id}."
    fake_validate_is_unique.assert_called_once_with(team.id, season.id, error_message=error_message)

    assert isinstance(test_team_season, TeamSeason)
    assert test_team_season.id == id
    assert test_team_season.team_id == team.id
    assert test_team_season.season_id == season.id
    assert test_team_season.league_id == league.id
    assert test_team_season.conference_id == conference.id
    assert test_team_season.division_id == division.id


@patch('app.data.factories.team_season_factory.injector')
def test_values_have_changed_when_values_have_not_changed_should_return_false(fake_injector):
    # Arrange
    kwargs = {
        'id': 1,
        'team_id': 1,
        'season_id': 1920,
        'league_id': 1,
        'conference_id': 1,
        'division_id': 1,
    }

    fake_team_season_repository = MagicMock(TeamSeasonRepository)
    old_team_season = TeamSeason(id=1, team_id=1, season_id=1920, league_id=1, conference_id=1, division_id=1)
    fake_team_season_repository.get_team_season.return_value = old_team_season
    fake_injector.get.return_value = fake_team_season_repository

    # Act
    result = team_season_factory._values_have_changed(**kwargs)

    # Assert
    fake_injector.get.assert_called_once_with(TeamSeasonRepository)
    fake_team_season_repository.get_team_season.assert_called_once_with(kwargs.get('id'))
    assert result is False


@patch('app.data.factories.team_season_factory.injector')
def test_values_have_changed_when_season_id_has_changed_should_return_true(fake_injector):
    # Arrange
    kwargs = {
        'id': 1,
        'team_id': 1,
        'season_id': 1920,
        'league_id': 1,
        'conference_id': 1,
        'division_id': 1,
    }

    fake_team_season_repository = MagicMock(TeamSeasonRepository)
    old_team_season = TeamSeason(id=1, team_id=1, season_id=1921)
    fake_team_season_repository.get_team_season.return_value = old_team_season
    fake_injector.get.return_value = fake_team_season_repository

    # Act
    result = team_season_factory._values_have_changed(**kwargs)

    # Assert
    fake_injector.get.assert_called_once_with(TeamSeasonRepository)
    fake_team_season_repository.get_team_season.assert_called_once_with(kwargs.get('id'))
    assert result is True


@patch('app.data.factories.team_season_factory.injector')
def test_values_have_changed_when_team_id_has_changed_should_return_true(fake_injector):
    # Arrange
    kwargs = {
        'id': 1,
        'team_id': 1,
        'season_id': 1920,
        'league_id': 1,
        'conference_id': 1,
        'division_id': 1,
    }

    fake_team_season_repository = MagicMock(TeamSeasonRepository)
    old_team_season = TeamSeason(id=1, team_id=2, season_id=1921)
    fake_team_season_repository.get_team_season.return_value = old_team_season
    fake_injector.get.return_value = fake_team_season_repository

    # Act
    result = team_season_factory._values_have_changed(**kwargs)

    # Assert
    fake_injector.get.assert_called_once_with(TeamSeasonRepository)
    fake_team_season_repository.get_team_season.assert_called_once_with(kwargs.get('id'))
    assert result is True


@patch('app.data.factories.team_season_factory.TeamSeason')
@patch('app.data.factories.team_season_factory.injector')
def test_validate_is_unique_when_values_are_not_unique_and_error_message_is_not_provided_should_raise_value_error_with_default_error_message(
        fake_injector, fake_team_season
):
    # Arrange
    fake_team_season_repository = MagicMock(TeamSeasonRepository)
    team_id = 1
    season_id = 1920
    team_season = TeamSeason(id=1, team_id=team_id, season_id=season_id)
    fake_team_season_repository.get_team_season_by_team_and_season.return_value = team_season
    fake_injector.get.return_value = fake_team_season_repository

    fake_team_season.query.filter_by.return_value.first.return_value = TeamSeason()

    # Act
    with pytest.raises(ValueError) as err:
        team_season_factory._validate_is_unique(team_id, season_id)

    # Assert
    fake_injector.get.assert_called_once_with(TeamSeasonRepository)
    fake_team_season_repository.get_team_season_by_team_and_season.assert_called_once_with(
        team_id=team_id, season_id=season_id
    )
    assert err.value.args[0] == "team_id and season_id together must be unique."


@patch('app.data.factories.team_season_factory.TeamSeason')
@patch('app.data.factories.team_season_factory.injector')
def test_validate_is_unique_when_values_are_not_unique_and_error_message_is_provided_should_raise_value_error_with_provided_error_message(
        fake_injector, fake_team_season
):
    # Arrange
    fake_team_season_repository = MagicMock(TeamSeasonRepository)
    team_id = 1
    season_id = 1920
    team_season = TeamSeason(id=1, team_id=team_id, season_id=season_id)
    fake_team_season_repository.get_team_season_by_team_and_season.return_value = team_season
    fake_injector.get.return_value = fake_team_season_repository

    fake_team_season.query.filter_by.return_value.first.return_value = TeamSeason()

    # Act
    with pytest.raises(ValueError) as err:
        team_season_factory._validate_is_unique(
            team_id, season_id, error_message="Test error message"
        )

    # Assert
    fake_injector.get.assert_called_once_with(TeamSeasonRepository)
    fake_team_season_repository.get_team_season_by_team_and_season.assert_called_once_with(
        team_id=team_id, season_id=season_id
    )
    assert err.value.args[0] == "Test error message"


@patch('app.data.factories.team_season_factory.TeamSeason')
@patch('app.data.factories.team_season_factory.injector')
def test_validate_is_unique_when_values_are_unique_should_not_raise_value_error(
        fake_injector, fake_team_season
):
    # Arrange
    fake_team_season_repository = MagicMock(TeamSeasonRepository)
    fake_team_season_repository.get_team_season_by_team_and_season.return_value = None
    fake_injector.get.return_value = fake_team_season_repository

    fake_team_season.query.filter_by.return_value.first.return_value = TeamSeason()

    team_id = 1
    season_id = 1920

    # Act
    try:
        team_season_factory._validate_is_unique(team_id, season_id, error_message="Test error message")
    except ValueError:
        assert False

    # Assert
    fake_injector.get.assert_called_once_with(TeamSeasonRepository)
    fake_team_season_repository.get_team_season_by_team_and_season.assert_called_once_with(
        team_id=team_id, season_id=season_id
    )
