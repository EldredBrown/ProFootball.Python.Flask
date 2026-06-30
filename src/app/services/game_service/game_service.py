from injector import inject

from app.data.errors import EntityNotFoundError
from app.data.models.game import Game
from app.data.repositories.game_repository import GameRepository
from app.data.repositories.team_season_repository import TeamSeasonRepository
from app.services.constants import Direction
from app.services.game_service.process_game_strategy.process_game_strategy_factory import ProcessGameStrategyFactory
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
        """
        self.game_repository = game_repository
        self.team_season_repository = team_season_repository
        self.process_game_strategy_factory = process_game_strategy_factory

    def __repr__(self):
        return (
            f"{type(self).__name__}("
            f"game_repository={self.game_repository}, "
            f"team_season_repository={self.team_season_repository}, "
            f"process_game_strategy_factory={self.process_game_strategy_factory}"
            f")"
        )

    def add_game(self, new_game: Game) -> None:
        """
        Adds a game to the data store

        :param new_game: The game to be added to the data store.

        :return: None

        :raises ValueError: When the new_game argument is None.
        """
        guard.raise_if_none(new_game, f"{type(self).__name__}.add_game: new_game")

        # self._validate_existence_of_teams_in_new_game(new_game)

        self.game_repository.add_game(new_game)
        self._edit_team_seasons(Direction.UP, new_game)

    def update_game(self, new_game: Game, old_game: Game) -> None:
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

        # self._validate_existence_of_teams_in_new_game(new_game)

        selected_game = self.game_repository.get_game(old_game.id)
        if selected_game is None:
            raise EntityNotFoundError(
                f"{type(self).__name__}.update_game: A game with id={old_game.id} could not be found."
            )

        self.game_repository.update_game(new_game)
        self._edit_team_seasons(Direction.DOWN, old_game)
        self._edit_team_seasons(Direction.UP, new_game)

    # def _validate_existence_of_teams_in_new_game(self, new_game: Game):
    #     for name in (new_game.guest_name, new_game.host_name):
    #         if not self.team_season_repository.get_team_season_by_team_and_season(name, new_game.season_year):
    #             raise EntityNotFoundError(f"No team season found for '{name}' in year {new_game.season_year}")

    def delete_game(self, id: int) -> None:
        """
        Deletes a game from the data store.

        :param id: The ID of the game to be deleted.

        :return: None

        :raises EntityNotFoundError: If the selected game cannot be found in the data store.
        :raises ValueError: If the id argument is None.
        """
        old_game = self.game_repository.get_game(id)
        if old_game is None:
            raise EntityNotFoundError(
                f"{type(self).__name__}.delete_game: A game with id={id} could not be found."
            )

        self._edit_team_seasons(Direction.DOWN, old_game)
        self.game_repository.delete_game(id)

    def _edit_team_seasons(self, direction: Direction, game: Game) -> None:
        process_game_strategy = self.process_game_strategy_factory.create_strategy(direction)
        process_game_strategy.process_game(game)
