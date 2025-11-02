from injector import inject

from app.data.models.game import Game
from app.data.models.team_season import TeamSeason
from app.data.repositories.team_season_repository import TeamSeasonRepository
from app.services.game_service.process_game_strategy.process_game_strategy import ProcessGameStrategy


class NullGameStrategy(ProcessGameStrategy):
    """
    A ProcessGameStrategy implementation for doing nothing. This is an implementation of the Singleton and Null Object
    design patterns.
    """

    _instance = None

    @inject
    def __init__(self, team_season_repository: TeamSeasonRepository = None):
        super().__init__(team_season_repository)

    def __repr__(self):
        return f"{type(self).__name__}(team_season_repository={super().team_season_repository})"

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()

        return cls._instance

    def _edit_scoring_data_for_team_season(self, team_season: TeamSeason, team_score: int, opponent_score: int) -> None:
        pass

    def _update_games_for_team_seasons(self, guest_season: TeamSeason, host_season: TeamSeason) -> None:
        pass

    def _update_wins_losses_and_ties_for_team_seasons(self,
                                                      guest_season: TeamSeason,
                                                      host_season: TeamSeason,
                                                      game: Game) -> None:
        pass
