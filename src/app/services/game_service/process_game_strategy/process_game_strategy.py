from abc import ABC, abstractmethod

from injector import inject

from app.data.errors import EntityNotFoundError
from app.data.models.game import Game
from app.data.models.team_season import TeamSeason
from app.data.repositories.team_repository import TeamRepository
from app.data.repositories.team_season_repository import TeamSeasonRepository
from app.services.utilities import guard


class ProcessGameStrategy(ABC):
    """
    Base class for the ProcessGameStrategy class hierarchy
    """

    @inject
    def __init__(self, team_repository: TeamRepository=None, team_season_repository: TeamSeasonRepository=None):
        """
        Initializes a new instance of the ProcessGameStrategy class.
        """
        self.team_repository = team_repository
        self.team_season_repository = team_season_repository

    def __repr__(self):
        return f"{type(self).__name__}(team_season_repository={self.team_season_repository})"

    def process_game(self, game: Game) -> None:
        """
        Processes a Game object into the team data store.

        :param game: The Game object to be processed into the team data store.

        :return: None

        :raises ValueError: If the passed game argument is None.
        """
        guard.raise_if_none(game, f"{type(self).__name__}.process_game: game")

        season_id = game.season_id

        guest = self.team_repository.get_team_by_name(game.guest_name)
        guest_season = self.team_season_repository.get_team_season_by_team_and_season(guest.id, season_id)
        if guest_season is None:
            # raise EntityNotFoundError(f"No team season found for guest '{game.guest_name}' in year {season_id}")
            pass

        host = self.team_repository.get_team_by_name(game.host_name)
        host_season = self.team_season_repository.get_team_season_by_team_and_season(host.id, season_id)
        if host_season is None:
            # raise EntityNotFoundError(f"No team season found for host '{game.host_name}' in year {season_id}")
            pass

        # The following if block is only a temporary patch to allow this app to work through the two seasons of the APFA,
        # when member teams were permitted to play counting games against non-member opponents. This patch will be removed
        # as soon as I progress to that season where this practice was no longer permitted.
        if guest_season is None and host_season is None:
            raise EntityNotFoundError(f"No team season found for either guest '{game.guest_name}' or host '{game.host_name}' in year {season_id}")

        self._edit_win_loss_data(guest_season, host_season, game)
        self._edit_scoring_data(guest_season, host_season, game.guest_score, game.host_score)

        self.team_season_repository.update_team_season(guest_season)
        self.team_season_repository.update_team_season(host_season)

    def _edit_win_loss_data(self, guest_season: TeamSeason, host_season: TeamSeason, game: Game) -> None:
        self._update_games_for_team_seasons(guest_season, host_season)
        self._update_wins_losses_and_ties_for_team_seasons(guest_season, host_season, game)

    @abstractmethod
    def _update_games_for_team_seasons(self, guest_season: TeamSeason, host_season: TeamSeason) -> None:
        raise NotImplementedError(f"{type(self).__name__}"
                                  f"._update_games_for_team_seasons must be implemented in a subclass.")

    @abstractmethod
    def _update_wins_losses_and_ties_for_team_seasons(
            self, guest_season: TeamSeason, host_season: TeamSeason, game: Game
    ) -> None:
        raise NotImplementedError(f"{type(self).__name__}"
                                  f"._update_wins_losses_and_ties_for_team_seasons must be implemented in "
                                  f"a subclass.")

    def _edit_scoring_data(
            self, guest_season: TeamSeason, host_season: TeamSeason, guest_score: int, host_score: int
    ) -> None:
        # Each team's score is passed as "team_score" and the opponent's as "opponent_score".
        self._edit_scoring_data_for_team_season(guest_season, guest_score, host_score)
        self._edit_scoring_data_for_team_season(host_season, host_score, guest_score)

    @abstractmethod
    def _edit_scoring_data_for_team_season(self, team_season: TeamSeason, team_score: int, opponent_score: int) -> None:
        raise NotImplementedError(f"{type(self).__name__}"
                                  f"._edit_scoring_data_for_team_season must be implemented in a subclass.")
