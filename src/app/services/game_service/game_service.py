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

    def __init__(self,
                 game_repository: GameRepository = None,
                 team_season_repository: TeamSeasonRepository = None,
                 process_game_strategy_factory: ProcessGameStrategyFactory = None):
        """
        Initializes a new instance of the GameService class.

        :param game_repository: The repository by which game data will be accessed.

        :param team_season_repository:
        The repository by which team_season data will be accessed.

        :param process_game_strategy_factory: The factory that will initialize the needed ProcessGameStrategy subclass.
        """
        self._game_repository = game_repository or GameRepository()
        self._team_season_repository = team_season_repository or TeamSeasonRepository()
        self._process_game_strategy_factory = process_game_strategy_factory or ProcessGameStrategyFactory()

    def __repr__(self):
        return f"{type(self).__name__}(game_repository={self._game_repository}, " \
               f"process_game_strategy_factory={self._process_game_strategy_factory})"

    def add_game(self, new_game: Game | None) -> None:
        """
        Adds a game to the data store

        :param new_game: The game to be added to the data store.

        :return: None

        :raises ValueError: When the new_game argument is None.
        """
        guard.raise_if_none(new_game, f"{type(self).__name__}.add_game: new_game")

        if not (
            self._team_season_repository.team_season_exists_with_team_and_season(new_game.guest_name,
                                                                                 new_game.season_year)
            or self._team_season_repository.team_season_exists_with_team_and_season(new_game.host_name,
                                                                                    new_game.season_year)
        ):
            raise EntityNotFoundError()

        new_game.decide_winner_and_loser()
        self._game_repository.add_game(new_game)
        self._edit_teams(Direction.UP, new_game)

    def edit_game(self, new_game: Game | None, old_game: Game | None) -> None:
        """
        Edits a game in the data store.

        :param new_game: The game containing data to be added to the data store.
        :param old_game: The game containing data to be removed from the data store.

        :return: None

        :raises EntityNotFoundError: If the selected game cannot be found in the data store.
        :raises ValueError: If the new_game or old_game argument is None.
        """
        guard.raise_if_none(new_game, f"{type(self).__name__}.edit_game: new_game")
        guard.raise_if_none(old_game, f"{type(self).__name__}.edit_game: old_game")

        selected_game = self._game_repository.get_game(old_game.id)
        if selected_game is None:
            raise EntityNotFoundError(
                f"{type(self).__name__}.edit_game: A game with id={id} could not be found.")

        new_game.decide_winner_and_loser()
        self._game_repository.update_game(new_game)
        self._edit_teams(Direction.DOWN, old_game)
        self._edit_teams(Direction.UP, new_game)

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

        self._edit_teams(Direction.DOWN, old_game)
        self._game_repository.delete_game(id)

    def _edit_teams(self, direction: int, game: Game) -> None:
        process_game_strategy = self._process_game_strategy_factory.create_strategy(direction)
        process_game_strategy.process_game(game)


if __name__ == '__main__':
    from app.data.models.league_season import LeagueSeason

    app = create_app()
    with app.app_context():
        game_repository = GameRepository()
        team_season_repository = TeamSeasonRepository()
        process_game_strategy_factory = ProcessGameStrategyFactory()
        service = GameService(game_repository, team_season_repository, process_game_strategy_factory)

        service.add_game(
            Game(season_id=103, week=1,
                 guest_name="Dallas Cowboys", guest_score=29,
                 host_name="Tampa Bay Buccaneers", host_score=31)
        )
        service.add_game(
            Game(season_id=103, week=1,
                 guest_name="Philadelphia Eagles", guest_score=32,
                 host_name="Atlanta Falcons", host_score=6)
        )
        service.add_game(
            Game(season_id=103, week=1,
                 guest_name="Pittsburgh Steelers", guest_score=23,
                 host_name="Buffalo Bills", host_score=16)
        )
        service.add_game(
            Game(season_id=103, week=1,
                 guest_name="New York Jets", guest_score=14,
                 host_name="Carolina Panthers", host_score=19)
        )
        service.add_game(
            Game(season_id=103, week=1,
                 guest_name="Minnesota Vikings", guest_score=24,
                 host_name="Cincinnati Bengals", host_score=27, notes="OT")
        )
        service.add_game(
            Game(season_id=103, week=1,
                 guest_name="Seattle Seahawks", guest_score=28,
                 host_name="Indianapolis Colts", host_score=16)
        )
        service.add_game(
            Game(season_id=103, week=1,
                 guest_name="San Francisco 49ers", guest_score=41,
                 host_name="Detroit Lions", host_score=33)
        )
        service.add_game(
            Game(season_id=103, week=1,
                 guest_name="Jacksonville Jaguars", guest_score=21,
                 host_name="Houston Texans", host_score=37)
        )
        service.add_game(
            Game(season_id=103, week=1,
                 guest_name="Arizona Cardinals", guest_score=38,
                 host_name="Tennessee Titans", host_score=13)
        )
        service.add_game(
            Game(season_id=103, week=1,
                 guest_name="Los Angeles Chargers", guest_score=20,
                 host_name="Washington Football Team", host_score=16)
        )
        service.add_game(
            Game(season_id=103, week=1,
                 guest_name="Cleveland Browns", guest_score=29,
                 host_name="Kansas City Chiefs", host_score=33)
        )
        service.add_game(
            Game(season_id=103, week=1,
                 guest_name="Green Bay Packers", guest_score=3,
                 host_name="New Orleans Saints", host_score=38)
        )
        service.add_game(
            Game(season_id=103, week=1,
                 guest_name="Miami Dolphins", guest_score=17,
                 host_name="New England Patriots", host_score=16)
        )
        service.add_game(
            Game(season_id=103, week=1,
                 guest_name="Denver Broncos", guest_score=27,
                 host_name="New York Giants", host_score=13)
        )
        service.add_game(
            Game(season_id=103, week=1,
                 guest_name="Chicago Bears", guest_score=14,
                 host_name="Los Angeles Rams", host_score=34)
        )
        service.add_game(
            Game(season_id=103, week=1,
                 guest_name="Baltimore Ravens", guest_score=27,
                 host_name="Las Vegas Raiders", host_score=33, notes="OT")
        )
