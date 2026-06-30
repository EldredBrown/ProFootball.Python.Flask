from typing import List, Optional

from app.data.models.league import League
from app.data.sqla import sqla, try_commit


class LeagueRepository:
    """
    Provides CRUD access to an external data store.
    """

    def get_leagues(self) -> List[League]:
        """
        Gets all the leagues in the data store.

        :return: A list of all fetched leagues.
        """
        leagues = self._get_leagues_with_navigation_properties()
        return leagues.all()

    def get_league(self, id: int) -> Optional[League]:
        """
        Gets the league in the data store with the specified id.

        :param id: The id of the league to fetch.

        :return: The fetched league.
        """
        leagues = self._get_leagues_with_navigation_properties()
        if len(leagues.all()) == 0:
            return None
        return leagues.get(id)

    def get_league_by_short_name(self, short_name: str) -> Optional[League]:
        """
        Gets the league in the data store with the specified id.

        :param short_name: The short_name of the league to fetch.

        :return: The fetched league.
        """
        leagues = self._get_leagues_with_navigation_properties()
        if len(leagues.all()) == 0:
            return None
        return leagues.filter_by(short_name=short_name).first()

    def add_league(self, league: League) -> League:
        """
        Adds a league to the data store.

        :param **kwargs: A keyword args dictionary containing values for the league to add.

        :return: The added league.
        """
        sqla.session.add(league)
        try_commit()
        return league

    def add_leagues(self, leagues: tuple) -> tuple:
        """
        Adds a collection of league_args dictionaries to the data store.

        :param league_args: The tuple of league keyword args dictionaries to add.

        :return: The added leagues.
        """
        for league in leagues:
            sqla.session.add(league)
        try_commit()
        return leagues

    def update_league(self, league: League) -> Optional[League]:
        """
        Updates a league in the data store.

        :param league: The league to update.

        :return: The updated league.
        """
        if not self.league_exists(league.id):
            return league
        league_in_db = self._set_values_of_league_in_db(league)
        sqla.session.add(league_in_db)
        try_commit()
        return league

    def delete_league(self, id: int) -> Optional[League]:
        """
        Deletes a league from the data store.

        :param id: The id of the league to delete.

        :return: The deleted league.
        """
        if not self.league_exists(id):
            return None
        league = self.get_league(id)
        sqla.session.delete(league)
        try_commit()
        return league

    def league_exists(self, id: int) -> bool:
        """
        Checks to verify whether a specific league exists in the data store.

        :param id: The id of the league to verify.

        :return: True if the league with the specified id exists in the data store; otherwise false.
        """
        return self.get_league(id) is not None

    def _get_leagues_with_navigation_properties(self):
        return League.query.options()

    def _set_values_of_league_in_db(self, league: League) -> League | None:
        league_in_db = self.get_league(league.id)
        league_in_db.short_name = league.short_name
        league_in_db.long_name = league.long_name
        league_in_db.first_season_id = league.first_season_id
        league_in_db.last_season_id = league.last_season_id
        return league_in_db
