from unittest.mock import patch, MagicMock

import pytest

import app.data.factories.game_factory as mod
from app.data.models.association import Association
from app.data.models.game import Game
from app.data.repositories.association_repository import AssociationRepository


def test_create_game_when_key_is_not_in_view_model_map_should_raise_value_error():
    # Arrange
    kwargs = {
        'invalid_key': "Value"
    }

    # Act
    with pytest.raises(KeyError) as err:
        _ = mod.create_game(**kwargs)

    # Assert
    assert err.value.args[0] == f"invalid_key is invalid."


@pytest.mark.parametrize(
    ("league", "league_name", "expected"),
    [
        (None, None, None),
        (None, '', None),
        (None, 'value', -1),
        (Association(id=1, long_name="League", short_name="L", parent_id=None), None, 1),
        (Association(id=1, long_name="League", short_name="L", parent_id=None), '', 1),
        (Association(id=1, long_name="League", short_name="L", parent_id=None), 'value', 1),
    ]
)
@patch('app.data.factories.game_factory.injector')
def test_create_game_should_return_game(fake_injector, league, league_name, expected):
    # Arrange
    kwargs = {
        'season_year': 1920,
        'league_name': league_name,
        'week': 1,
        'guest_name': "Guest",
        'guest_score': 3,
        'host_name': "Host",
        'host_score': 3,
        'is_playoff': False,
        'notes': "The quick sly fox jumped over the lazy brown dog.",
    }

    fake_association_repository = MagicMock(AssociationRepository)
    fake_association_repository.get_association_by_short_name.return_value = league
    fake_injector.get.return_value = fake_association_repository

    # Act
    test_game = mod.create_game(**kwargs)

    # Assert
    assert isinstance(test_game, Game)
    assert test_game.season_year == kwargs.get('season_year')

    fake_injector.get.assert_called_once_with(AssociationRepository)
    fake_association_repository.get_association_by_short_name.assert_called_once_with(kwargs.get('league_name'))
    assert test_game.league_id == expected

    assert test_game.week == kwargs.get('week')
    assert test_game.guest_name == kwargs.get('guest_name')
    assert test_game.guest_score == kwargs.get('guest_score')
    assert test_game.host_name == kwargs.get('host_name')
    assert test_game.host_score == kwargs.get('host_score')
    assert test_game.is_playoff == kwargs.get('is_playoff')
    assert test_game.notes == kwargs.get('notes')
