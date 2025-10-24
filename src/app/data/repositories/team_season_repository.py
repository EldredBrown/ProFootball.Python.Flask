from typing import List

from sqlalchemy.exc import IntegrityError

from app.data.models.team_season import TeamSeason
from app.data.sqla import sqla


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

    def get_team_season(self, id: int) -> TeamSeason | None:
        """
        Gets the team_season in the data store with the specified id.

        :param id: The id of the team_season to fetch.

        :return: The fetched team_season.
        """
        team_seasons = self.get_team_seasons()
        if len(team_seasons) == 0:
            return None
        return TeamSeason.query.get(id)
