from typing import List

from sqlalchemy.exc import IntegrityError

from app.data.models.league import League
from app.data.sqla import sqla
from app.data.factories import league_factory


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

        :param short_name: The short_name of the league to fetch.

        :return: The fetched league.
        """
        leagues = self.get_leagues()
        if len(leagues) == 0:
            return None
        return League.query.filter_by(short_name=short_name).first()

    def add_league(self, **kwargs) -> League:
        """
        Adds a league to the data store.

        :param **kwargs: A keyword args dictionary containing values for the league to add.

        :return: The added league.
        """
        league = league_factory.create_league(**kwargs)
        sqla.session.add(league)
        try:
            sqla.session.commit()
        except IntegrityError:
            sqla.session.rollback()
            raise
        return league

    def add_leagues(self, league_args: tuple) -> List[League]:
        """
        Adds a collection of league_args dictionaries to the data store.

        :param league_args: The tuple of league keyword args dictionaries to add.

        :return: The added leagues.
        """
        leagues = []
        try:
            for kwargs in league_args:
                league = league_factory.create_league(kwargs)
                leagues.append(league)
                sqla.session.add(league)
            sqla.session.commit()
        except IntegrityError:
            sqla.session.rollback()
            raise
        return leagues

    def update_league(self, **kwargs) -> League | None:
        """
        Updates a league in the data store.

        :param league: The league to update.

        :return: The updated league.
        """
        if 'id' not in kwargs:
            raise ValueError("ID must be provided for existing League.")

        if not self.league_exists(kwargs['id']):
            return League(**kwargs)

        old_league = self.get_league(kwargs['id'])
        new_league = league_factory.create_league(old_league, **kwargs)

        old_league.short_name = new_league.short_name
        old_league.long_name = new_league.long_name
        old_league.first_season_year = new_league.first_season_year
        old_league.last_season_year = new_league.last_season_year

        sqla.session.add(old_league)
        try:
            sqla.session.commit()
        except IntegrityError:
            sqla.session.rollback()
            raise

        return new_league

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
        return self.get_league(id) is not None
