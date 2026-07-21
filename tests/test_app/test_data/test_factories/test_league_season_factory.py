from unittest.mock import patch, MagicMock

import pytest

from app.data.factories import league_season_factory as mod
from app.data.models.association import Association
from app.data.models.league_season import LeagueSeason
from app.data.models.season import Season
from app.data.repositories.association_repository import AssociationRepository
from app.data.repositories.league_season_repository import LeagueSeasonRepository
from app.data.repositories.season_repository import SeasonRepository


def test_create_league_season_when_key_is_not_in_view_model_map_should_raise_value_error():
    # Arrange
    kwargs = {
        'invalid_key': "Value"
    }

    # Act
    with pytest.raises(KeyError) as err:
        test_league_season = mod.create_league_season(**kwargs)

    # Assert
    assert err.value.args[0] == f"invalid_key is invalid."


@patch('app.data.factories.league_season_factory.injector')
def test_create_league_season_when_league_is_none_should_set_league_id_to_minus_one(
        fake_injector
):
    # Arrange
    league_name = "A"
    view_kwargs = {'league_name': league_name}

    fake_association_repository = MagicMock(AssociationRepository)
    league = None
    fake_association_repository.get_association_by_short_name.return_value = league
    fake_injector.get.return_value = fake_association_repository

    # Act
    result = mod.create_league_season(**view_kwargs)

    # Assert
    fake_injector.get.assert_called_once_with(AssociationRepository)
    fake_association_repository.get_association_by_short_name.assert_called_once_with(league_name)
    assert result is not None
    assert isinstance(result, LeagueSeason)
    assert result.league_id == -1


@patch('app.data.factories.league_season_factory.injector')
def test_create_league_season_when_league_is_not_none_should_set_league_id_to_league_id(
        fake_injector
):
    # Arrange
    league_name = "A"
    view_kwargs = {'league_name': league_name}

    fake_association_repository = MagicMock(AssociationRepository)
    league = Association(id=1, long_name="Association", short_name="A", parent_id=None)
    fake_association_repository.get_association_by_short_name.return_value = league
    fake_injector.get.return_value = fake_association_repository

    # Act
    result = mod.create_league_season(**view_kwargs)

    # Assert
    fake_injector.get.assert_called_once_with(AssociationRepository)
    fake_association_repository.get_association_by_short_name.assert_called_once_with(league_name)
    assert result is not None
    assert isinstance(result, LeagueSeason)
    assert result.league_id == league.id
