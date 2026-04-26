from typing import NamedTuple

from injector import inject

from app.data.repositories.team_season_repository import TeamSeasonRepository


class GamePrediction(NamedTuple):
    guest_score: float
    host_score: float


class GamePredictorService:
    """
    A service for predicting the scores of future games.
    """

    @inject
    def __init__(self, team_season_repository: TeamSeasonRepository) -> None:
        """
        Initializes a new instance of the GamePredictorService class.

        :param team_season_repository: The repository from which team_season data will be fetched
        for both teams.
        """
        self.team_season_repository = team_season_repository

    def __repr__(self):
        return f"{type(self).__name__}(team_season_repository={self.team_season_repository})"

    def predict_game_score(
            self,
            guest_name: str, guest_season_year: int,
            host_name: str, host_season_year: int
    ) -> GamePrediction:
        """
        Predicts the score of a future/hypothetical game between two teams.

        :param guest_name: The name of the guest.
        :param guest_season_year: The season year of the guest.
        :param host_name: The name of the host.
        :param host_season_year: The season year of the host.
        :return: A NamedTuple containing the predicted guest score and host score respectively.
        """
        guest_season = (
            self.team_season_repository.get_team_season_by_team_name_and_season_year(guest_name, guest_season_year)
        )
        if guest_season is None:
            raise ValueError(f"No season data found for '{guest_name}' in year {guest_season_year}")

        host_season = (
            self.team_season_repository.get_team_season_by_team_name_and_season_year(host_name, host_season_year)
        )
        if host_season is None:
            raise ValueError(f"No season data found for '{host_name}' in year {host_season_year}")

        guest_score = _predict_score(guest_season, host_season)
        host_score = _predict_score(host_season, guest_season)
        return GamePrediction(guest_score, host_score)


def _predict_score(offensive_team, defensive_team) -> float:
    return round(
        ((offensive_team.offensive_factor * defensive_team.defensive_average
            + defensive_team.defensive_factor * offensive_team.offensive_average) / 2),
        1
    )
