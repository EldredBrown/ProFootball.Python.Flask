from typing import Optional

from injector import inject

from app import create_app
from app.data.errors import EntityNotFoundError
from app.data.models.game import Game
from app.data.repositories.game_repository import GameRepository
from app.data.repositories.team_season_repository import TeamSeasonRepository
from app.services.constants import Direction
from app.services.game_service.process_game_strategy.process_game_strategy_factory \
    import ProcessGameStrategyFactory
from app.services.utilities import guard


class GameService:
    """
    A service to handle the more complicated actions of adding, editing, or deleting games in the data store.
    """

    @inject
    def __init__(
            self,
            game_repository: GameRepository,
            team_season_repository: TeamSeasonRepository,
            process_game_strategy_factory: ProcessGameStrategyFactory
    ):
        """
        Initializes a new instance of the GameService class.

        :param game_repository: The repository by which game data will be accessed.

        :param team_season_repository:
        The repository by which team_season data will be accessed.

        :param process_game_strategy_factory: The factory that will initialize the needed ProcessGameStrategy subclass.
        """
        self._game_repository = game_repository
        self._team_season_repository = team_season_repository
        self._process_game_strategy_factory = process_game_strategy_factory

    def __repr__(self):
        return f"{type(self).__name__}(game_repository={self._game_repository}, " \
               f"process_game_strategy_factory={self._process_game_strategy_factory})"

    def add_game(self, new_game: Optional[Game]) -> None:
        """
        Adds a game to the data store

        :param new_game: The game to be added to the data store.

        :return: None

        :raises ValueError: When the new_game argument is None.
        """
        guard.raise_if_none(new_game, f"{type(self).__name__}.add_game: new_game")

        if not (
            self._team_season_repository.team_season_exists_with_team_name_and_season_year(new_game.guest_name,
                                                                                           new_game.season_year)
            or self._team_season_repository.team_season_exists_with_team_name_and_season_year(new_game.host_name,
                                                                                              new_game.season_year)
        ):
            raise EntityNotFoundError()

        new_game.decide_winner_and_loser()
        self._game_repository.add_game(new_game)
        self._edit_team_seasons(Direction.UP, new_game)

    def update_game(self, new_game: Optional[Game], old_game: Optional[Game]) -> None:
        """
        Edits a game in the data store.

        :param new_game: The game containing data to be added to the data store.
        :param old_game: The game containing data to be removed from the data store.

        :return: None

        :raises EntityNotFoundError: If the selected game cannot be found in the data store.
        :raises ValueError: If the new_game or old_game argument is None.
        """
        guard.raise_if_none(new_game, f"{type(self).__name__}.update_game: new_game")
        guard.raise_if_none(old_game, f"{type(self).__name__}.update_game: old_game")

        selected_game = self._game_repository.get_game(old_game.id)
        if selected_game is None:
            raise EntityNotFoundError(
                f"{type(self).__name__}.update_game: A game with id={id} could not be found.")

        new_game.decide_winner_and_loser()
        self._game_repository.update_game(new_game)
        self._edit_team_seasons(Direction.DOWN, old_game)
        self._edit_team_seasons(Direction.UP, new_game)

    def delete_game(self, id: int) -> None:
        """
        Deletes a game from the data store.

        :param id: The ID of the game to be deleted.

        :return: None

        :raises EntityNotFoundError: If the selected game cannot be found in the data store.
        :raises ValueError: If the id argument is None.
        """
        old_game = self._game_repository.get_game(id)
        if old_game is None:
            raise EntityNotFoundError(
                f"{type(self).__name__}.delete_game: A game with id={id} could not be found.")

        self._edit_team_seasons(Direction.DOWN, old_game)
        self._game_repository.delete_game(id)

    def _edit_team_seasons(self, direction: int, game: Game) -> None:
        process_game_strategy = self._process_game_strategy_factory.create_strategy(direction)
        process_game_strategy.process_game(game)
