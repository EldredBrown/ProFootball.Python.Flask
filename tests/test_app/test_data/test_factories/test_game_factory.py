from app.data.factories import game_factory
from app.data.models.game import Game


def test_create_game_should_return_game():
    # Arrange
    kwargs = {
        'season_id': 1920,
        'week': 1,
        'guest_name': "Guest",
        'guest_score': 3,
        'host_name': "Host",
        'host_score': 3,
        'is_playoff': False,
    }

    # Act
    test_game = game_factory.create_game(**kwargs)

    # Assert
    assert isinstance(test_game, Game)
    assert test_game.season_id == kwargs['season_id']
    assert test_game.week == kwargs['week']
    assert test_game.guest_name == kwargs['guest_name']
    assert test_game.guest_score == kwargs['guest_score']
    assert test_game.host_name == kwargs['host_name']
    assert test_game.host_score == kwargs['host_score']
    assert test_game.is_playoff == kwargs['is_playoff']
