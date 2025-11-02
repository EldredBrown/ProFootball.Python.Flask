from injector import inject

from app.data.repositories.team_season_repository import TeamSeasonRepository
from app.services.constants import Direction
from app.services.game_service.process_game_strategy.add_game_strategy import AddGameStrategy
from app.services.game_service.process_game_strategy.process_game_strategy import ProcessGameStrategy
from app.services.game_service.process_game_strategy.subtract_game_strategy import SubtractGameStrategy
from app.services.game_service.process_game_strategy.null_game_strategy import NullGameStrategy


class ProcessGameStrategyFactory:
    """
    A factory class for the creation of subclass instance of the ProcessGameStrategyBase class.
    """

    @inject
    def __init__(self, team_season_repository: TeamSeasonRepository):
        """
        Initializes a new instance of the ProcessGameStrategyFactory class
        """
        self.team_season_repository = team_season_repository

    def __repr__(self):
        return f"{type(self).__name__}()"

    def create_strategy(self, direction: int) -> ProcessGameStrategy:
        strategies = {
            Direction.UP:   AddGameStrategy,
            Direction.DOWN: SubtractGameStrategy
        }

        try:
            strategy = strategies[direction]
            return strategy(self.team_season_repository)
        except KeyError:
            return NullGameStrategy.instance()
