from unittest.mock import patch, MagicMock

from app.data.factories import game_factory
from app.data.models.association import Association
from app.data.models.game import Game
from app.data.repositories.association_repository import AssociationRepository


@patch('app.data.factories.game_factory.injector')
def test_create_game_should_return_game(fake_injector):
    # Arrange
    kwargs = {
        'season_year': 1920,
        'league_name': "L",
        'week': 1,
        'guest_name': "Guest",
        'guest_score': 3,
        'host_name': "Host",
        'host_score': 3,
        'is_playoff': False,
    }

    fake_association_repository = MagicMock(AssociationRepository)
    league = Association(id=1, long_name="League", short_name="L", parent_id=None)
    fake_association_repository.get_association_by_short_name.return_value = league
    fake_injector.get.return_value = fake_association_repository

    # Act
    test_game = game_factory.create_game(**kwargs)

    # Assert
    assert isinstance(test_game, Game)
    assert test_game.season_year == kwargs['season_year']

    fake_injector.get.assert_called_once_with(AssociationRepository)
    fake_association_repository.get_association_by_short_name.assert_called_once_with(kwargs.get('league_name'))
    assert test_game.league_id == league.id

    assert test_game.week == kwargs['week']
    assert test_game.guest_name == kwargs['guest_name']
    assert test_game.guest_score == kwargs['guest_score']
    assert test_game.host_name == kwargs['host_name']
    assert test_game.host_score == kwargs['host_score']
    assert test_game.is_playoff == kwargs['is_playoff']
