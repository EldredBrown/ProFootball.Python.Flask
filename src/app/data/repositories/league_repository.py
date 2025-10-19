from typing import List

from sqlalchemy import exists

from app.data.models.league import League
from app.data.sqla import sqla


class LeagueRepository:
    """
    Provides CRUD access to an external data store.
    """

    def __init__(self) -> None:
        """
        Initializes a new instance of the LeagueRepository class.
        """
        pass

    def get_leagues(self) -> List[League]:
        """
        Gets all the leagues in the data store.

        :return: A list of all fetched leagues.
        """
        return League.query.all()

    def get_league(self, id: int) -> League | None:
        """
        Gets the league in the data store with the specified id.

        :param id: The id of the league to fetch.

        :return: The fetched league.
        """
        leagues = self.get_leagues()
        if len(leagues) == 0:
            return None
        return League.query.get(id)

    def get_league_by_name(self, short_name: str) -> League | None:
        """
        Gets the league in the data store with the specified id.

        :param short_name: The year of the league to fetch.

        :return: The fetched league.
        """
        leagues = self.get_leagues()
        if len(leagues) == 0:
            return None
        return League.query.filter_by(short_name=short_name).first()

    def add_league(self, league: League) -> League:
        """
        Adds a league to the data store.

        :param league: The league to add.

        :return: The added league.
        """
        sqla.session.add(league)
        sqla.session.commit()
        return league

    def add_leagues(self, leagues: tuple) -> tuple:
        """
        Adds a collection of leagues to the data store.

        :param leagues: The leagues to add.

        :return: The added leagues.
        """
        for league in leagues:
            sqla.session.add(league)
        sqla.session.commit()
        return leagues

    def update_league(self, league: League) -> League | None:
        """
        Updates a league in the data store.

        :param league: The league to update.

        :return: The updated league.
        """
        if not self.league_exists(league.id):
            return league

        league_to_update = self.get_league(league.id)
        league_to_update.short_name = league.short_name
        league_to_update.long_name = league.long_name
        league_to_update.first_season_year = league.first_season_year
        league_to_update.last_season_year = league.last_season_year
        sqla.session.add(league_to_update)
        sqla.session.commit()
        return league

    def delete_league(self, id: int) -> League | None:
        """
        Deletes a league from the data store.

        :param id: The id of the league to delete.

        :return: The deleted league.
        """
        if not self.league_exists(id):
            return None

        league = self.get_league(id)
        sqla.session.delete(league)
        sqla.session.commit()
        return league

    def league_exists(self, id: int) -> bool:
        """
        Checks to verify whether a specific league exists in the data store.

        :param id: The id of the league to verify.

        :return: True if the league with the specified id exists in the data store; otherwise false.
        """
        return sqla.session.query(exists().where(League.id == id)).scalar()
