from injector import inject

from app.data.models.game import Game
from app.data.models.team_season import TeamSeason
from app.data.repositories.team_season_repository import TeamSeasonRepository
from app.services.game_service.process_game_strategy.process_game_strategy import ProcessGameStrategy


class AddGameStrategy(ProcessGameStrategy):
    """
    A ProcessGameStrategy implementation for adding games to the data store.
    """

    @inject
    def __init__(self, team_season_repository: TeamSeasonRepository):
        """
        Initializes a new instance of the AddGameStrategy class.

        :param team_season_repository:
        The repository by which team_season data will be accessed.
        """
        super().__init__(team_season_repository)

    def __repr__(self):
        return f"{type(self).__name__}(team_season_repository={super()._team_season_repository})"

    def _edit_scoring_data_for_team_season(self, team_season: TeamSeason, team_score: int, opponent_score: int) -> None:
        if team_season is None:
            return

        team_season.points_for += team_score
        team_season.points_against += opponent_score
        team_season.calculate_expected_wins_and_losses()

    def _update_games_for_team_seasons(self, guest_season: TeamSeason, host_season: TeamSeason) -> None:
        if guest_season is not None:
            guest_season.games += 1

        if host_season is not None:
            host_season.games += 1

    def _update_wins_losses_and_ties_for_team_seasons(self,
                                                      guest_season: TeamSeason,
                                                      host_season: TeamSeason,
                                                      game: Game) -> None:
        if game.is_tie():
            if guest_season is not None:
                guest_season.ties += 1

            if host_season is not None:
                host_season.ties += 1

        else:
            season_year = game.season_year

            winner_season = self._team_season_repository.get_team_season_by_team_name_and_season_year(game.winner_name,
                                                                                                      season_year)
            if winner_season is not None:
                winner_season.wins += 1

            loser_season = self._team_season_repository.get_team_season_by_team_name_and_season_year(game.loser_name,
                                                                                                     season_year)
            if loser_season is not None:
                loser_season.losses += 1
