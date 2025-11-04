from typing import List, Optional

from sqlalchemy.exc import IntegrityError

from app.data.models.team_season import TeamSeason
from app.data.sqla import sqla, try_commit


class TeamSeasonRepository:
    """
    Provides CRUD access to an external data store.
    """

    def __init__(self) -> None:
        """
        Initializes a new instance of the TeamSeasonRepository class.
        """
        pass

    def get_team_seasons(self) -> List[TeamSeason]:
        """
        Gets all the team_seasons in the data store.

        :return: A list of all fetched team_seasons.
        """
        return TeamSeason.query.all()

    def get_team_seasons_by_season_year(self, season_year: Optional[int]) -> List[TeamSeason]:
        """
        Gets all the team_seasons in the data store filtered by season_year.

        :param season_year: The season_year to filter.

        :return: A list of all fetched team_seasons.
        """
        if season_year is None:
            return []
        return TeamSeason.query.filter_by(season_year=season_year).all()

    def get_team_season(self, id: int) -> Optional[TeamSeason]:
        """
        Gets the team_season in the data store with the specified id.

        :param id: The id of the team_season to fetch.

        :return: The fetched team_season.
        """
        if self._team_seasons_empty():
            return None
        return TeamSeason.query.get(id)

    def get_team_season_by_team_name_and_season_year(self, team_name: str, season_year: int) -> Optional[TeamSeason]:
        return TeamSeason.query.filter_by(team_name=team_name, season_year=season_year).first()

    def _team_seasons_empty(self) -> bool:
        team_seasons = self.get_team_seasons()
        return len(team_seasons) == 0

    def update_team_season(self, team_season: TeamSeason) -> None:
        if not self.team_season_exists(team_season.id):
            return team_season
        team_season_in_db = self._set_values_of_team_season_in_db(team_season)
        sqla.session.add(team_season_in_db)
        try_commit()
        return team_season

    def _set_values_of_team_season_in_db(self, team_season: TeamSeason) -> TeamSeason:
        team_season_in_db = self.get_team_season(team_season.id)
        team_season_in_db.team_name = team_season.team_name
        team_season_in_db.season_year = team_season.season_year
        team_season_in_db.league_name = team_season.league_name
        team_season_in_db.conference_name = team_season.conference_name
        team_season_in_db.division_name = team_season.division_name
        team_season_in_db.games = team_season.games
        team_season_in_db.wins = team_season.wins
        team_season_in_db.losses = team_season.losses
        team_season_in_db.ties = team_season.ties
        team_season_in_db.winning_percentage = team_season.winning_percentage
        team_season_in_db.points_for = team_season.points_for
        team_season_in_db.points_against = team_season.points_against
        team_season_in_db.expected_wins = team_season.expected_wins
        team_season_in_db.expected_losses = team_season.expected_losses
        team_season_in_db.offensive_average = team_season.offensive_average
        team_season_in_db.offensive_factor = team_season.offensive_factor
        team_season_in_db.offensive_index = team_season.offensive_index
        team_season_in_db.defensive_average = team_season.defensive_average
        team_season_in_db.defensive_factor = team_season.defensive_factor
        team_season_in_db.defensive_index = team_season.defensive_index
        team_season_in_db.final_expected_winning_percentage = team_season.final_expected_winning_percentage
        return team_season_in_db

    def team_season_exists(self, id: int) -> bool:
        """
        Checks to verify whether a specific game exists in the data store.

        :param id: The id of the game to verify.

        :return: True if the game with the specified id exists in the data store; otherwise false.
        """
        return self.get_team_season(id) is not None

    def team_season_exists_with_team_name_and_season_year(self, team_name: str, season_year: int) -> bool:
        return self.get_team_season_by_team_name_and_season_year(team_name, season_year) is not None
