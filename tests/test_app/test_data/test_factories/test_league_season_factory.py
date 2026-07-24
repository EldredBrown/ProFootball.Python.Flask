from unittest.mock import patch, MagicMock

import pytest

import app.data.factories.league_season_factory as mod
from app.data.models.association import Association
from app.data.models.league_season import LeagueSeason
from app.data.repositories.association_repository import AssociationRepository


def test_create_league_season_when_key_is_not_in_view_model_map_should_raise_value_error():
    # Arrange
    kwargs = {
        'invalid_key': "Value"
    }

    # Act
    with pytest.raises(KeyError) as err:
        _ = mod.create_league_season(**kwargs)

    # Assert
    assert err.value.args[0] == f"invalid_key is invalid."


@pytest.mark.parametrize(
    ('league', 'exp_league_id'),
    [
        (None, -1),
        (Association(id=1, long_name="League", short_name="L", parent_id=None), 1),
    ]
)
@patch('app.data.factories.league_season_factory.injector')
def test_create_league_season_should_set_league_id_to_correct_value(
        fake_injector, league, exp_league_id
):
    # Arrange
    league_name = "L"
    view_kwargs = {'league_name': league_name}

    fake_association_repository = MagicMock(AssociationRepository)
    fake_association_repository.get_association_by_short_name.return_value = league
    fake_injector.get.return_value = fake_association_repository

    # Act
    result = mod.create_league_season(**view_kwargs)

    # Assert
    fake_injector.get.assert_called_once_with(AssociationRepository)
    fake_association_repository.get_association_by_short_name.assert_called_once_with(league_name)
    assert result is not None
    assert isinstance(result, LeagueSeason)
    assert result.league_id == exp_league_id
