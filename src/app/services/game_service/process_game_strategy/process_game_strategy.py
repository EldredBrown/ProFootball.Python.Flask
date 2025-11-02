from typing import Optional

from injector import inject

from app.data.models.game import Game
from app.data.models.team_season import TeamSeason
from app.data.repositories.game_repository import GameRepository
from app.data.repositories.team_season_repository import TeamSeasonRepository
from app.services.utilities import guard


class ProcessGameStrategy:
    """
    Base class for the ProcessGameStrategy class hierarchy
    """

    @inject
    def __init__(self, team_season_repository: TeamSeasonRepository):
        """
        Initializes a new instance of the ProcessGameStrategy class.
        """
        self.team_season_repository = team_season_repository

    def __repr__(self):
        return f"{type(self).__name__}(team_season_repository={self.team_season_repository})"

    def process_game(self, game: Optional[Game]) -> None:
        """
        Processes a Game object into the team data store.

        :param game: The Game object to be processed into the team data store.

        :return: None

        :raises ValueError: If the passed game argument is None.
        """
        guard.raise_if_none(game, f"{type(self).__name__}.process_game: game")

        season_year = game.season_year
        guest_season = self.team_season_repository.get_team_season_by_team_name_and_season_year(game.guest_name, season_year)
        host_season = self.team_season_repository.get_team_season_by_team_name_and_season_year(game.host_name, season_year)

        self._edit_win_loss_data(guest_season, host_season, game)
        self._edit_scoring_data(guest_season, host_season, game.guest_score, game.host_score)

        self.team_season_repository.update_team_season(guest_season)
        self.team_season_repository.update_team_season(host_season)

    def _edit_win_loss_data(self, guest_season: TeamSeason, host_season: TeamSeason, game: Game) -> None:
        self._update_games_for_team_seasons(guest_season, host_season)
        self._update_wins_losses_and_ties_for_team_seasons(guest_season, host_season, game)
        self._update_winning_percentage_for_team_seasons(guest_season, host_season)

    def _update_games_for_team_seasons(self, guest_season: TeamSeason, host_season: TeamSeason) -> None:
        raise NotImplementedError(f"{type(self).__name__}"
                                  f"._update_games_for_team_seasons must be implemented in a subclass.")

    def _update_wins_losses_and_ties_for_team_seasons(self,
                                                      guest_season: TeamSeason,
                                                      host_season: TeamSeason,
                                                      game: Game) -> None:
        raise NotImplementedError(f"{type(self).__name__}"
                                  f"._update_wins_losses_and_ties_for_team_seasons must be implemented in "
                                  f"a subclass.")

    @staticmethod
    def _update_winning_percentage_for_team_seasons(guest_season: TeamSeason, host_season: TeamSeason) -> None:
        if guest_season is not None:
            guest_season.calculate_winning_percentage()

        if host_season is not None:
            host_season.calculate_winning_percentage()

    def _edit_scoring_data(self,
                           guest_season: TeamSeason,
                           host_season: TeamSeason,
                           guest_score: int,
                           host_score: int) -> None:
        self._edit_scoring_data_for_team_season(guest_season, guest_score, host_score)
        self._edit_scoring_data_for_team_season(host_season, host_score, guest_score)

    def _edit_scoring_data_for_team_season(self, team_season: TeamSeason, team_score: int, opponent_score: int) -> None:
        raise NotImplementedError(f"{type(self).__name__}"
                                  f"._edit_scoring_data_for_team_season must be implemented in a subclass.")
