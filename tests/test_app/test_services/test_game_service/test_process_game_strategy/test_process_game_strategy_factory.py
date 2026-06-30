import pytest

from unittest.mock import patch

from app.services.constants import Direction
from app.services.game_service.process_game_strategy.add_game_strategy import AddGameStrategy
from app.services.game_service.process_game_strategy.null_game_strategy import NULL_GAME_STRATEGY
from app.services.game_service.process_game_strategy.process_game_strategy_factory import ProcessGameStrategyFactory
from app.services.game_service.process_game_strategy.subtract_game_strategy import SubtractGameStrategy


@pytest.fixture
@patch('app.services.game_service.process_game_strategy.process_game_strategy_factory.TeamSeasonRepository')
@patch('app.services.game_service.process_game_strategy.process_game_strategy_factory.TeamRepository')
def test_factory(fake_team_repository, fake_team_season_repository) -> ProcessGameStrategyFactory:
    test_factory = ProcessGameStrategyFactory(fake_team_repository, fake_team_season_repository)
    return test_factory


def test_create_strategy_when_direction_is_up_should_create_add_game_strategy(test_factory):
    strategy = test_factory.create_strategy(Direction.UP)

    assert isinstance(strategy, AddGameStrategy)


def test_create_strategy_when_direction_is_down_should_create_subtract_game_strategy(
        test_factory
):
    strategy = test_factory.create_strategy(Direction.DOWN)

    assert isinstance(strategy, SubtractGameStrategy)


def test_create_strategy_when_direction_is_neither_up_nor_down_should_create_null_game_strategy(
        test_factory
):
    strategy = test_factory.create_strategy(-1)

    assert strategy is NULL_GAME_STRATEGY
