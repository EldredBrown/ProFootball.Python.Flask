from unittest.mock import patch

import pytest

from app.data.factories import game_factory
from app.data.models.game import Game
from test_app import create_app


@pytest.fixture
def test_app():
    return create_app()


def test_create_game_should_return_game(test_app):
    with test_app.app_context():
        # Arrange
        kwargs = {
            'season_year': 1920,
            'week': 1,
            'guest_name': "St. Paul Ideals",
            'guest_score': 0,
            'host_name': "Rock Island Independents",
            'host_score': 48,
            'is_playoff': False,
        }

        # Act
        test_game = game_factory.create_game(**kwargs)

    # Assert
    assert isinstance(test_game, Game)
    assert test_game.season_year == kwargs['season_year']
    assert test_game.week == kwargs['week']
    assert test_game.guest_name == kwargs['guest_name']
    assert test_game.guest_score == kwargs['guest_score']
    assert test_game.host_name == kwargs['host_name']
    assert test_game.host_score == kwargs['host_score']
    assert test_game.is_playoff == kwargs['is_playoff']
