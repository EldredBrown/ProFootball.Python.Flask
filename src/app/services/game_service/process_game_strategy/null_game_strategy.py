from app.data.models.game import Game
from app.data.models.team_season import TeamSeason
from app.services.game_service.process_game_strategy.process_game_strategy import ProcessGameStrategy


class NullGameStrategy(ProcessGameStrategy):
    """
    A ProcessGameStrategy implementation for doing nothing. This is an implementation of the Singleton and Null Object
    design patterns.
    """

    def process_game(self, game: Game) -> None:
        """Does nothing. Satisfies the Null Object contract."""
        pass

    def _edit_scoring_data_for_team_season(self, team_season: TeamSeason, team_score: int, opponent_score: int) -> None:
        pass

    def _update_games_for_team_seasons(self, guest_season: TeamSeason, host_season: TeamSeason) -> None:
        pass

    def _update_wins_losses_and_ties_for_team_seasons(self,
                                                      guest_season: TeamSeason,
                                                      host_season: TeamSeason,
                                                      game: Game) -> None:
        pass


NULL_GAME_STRATEGY = NullGameStrategy()
