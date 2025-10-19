from typing import List

from sqlalchemy import exists

from app.data.models.league_season import LeagueSeason
from app.data.sqla import sqla


class LeagueSeasonRepository:
    """
    Provides CRUD access to an external data store.
    """

    def __init__(self) -> None:
        """
        Initializes a new instance of the LeagueSeasonRepository class.
        """
        pass

    def get_league_seasons(self) -> List[LeagueSeason]:
        """
        Gets all the league_seasons in the data store.

        :return: A list of all fetched league_seasons.
        """
        return LeagueSeason.query.all()

    def get_league_season(self, id: int) -> LeagueSeason | None:
        """
        Gets the league_season in the data store with the specified id.

        :param id: The id of the league_season to fetch.

        :return: The fetched league_season.
        """
        league_seasons = self.get_league_seasons()
        if len(league_seasons) == 0:
            return None
        return LeagueSeason.query.get(id)

    def get_league_season_by_league_and_season(self, league_name: int, season_year: int) -> LeagueSeason | None:
        """
        Gets the league_season in the data store with the specified league_name and season_year.

        :param league_name: The league_name of the league_season to fetch.
        :param season_year: The season_year of the league_season to fetch.

        :return: The fetched league_season.
        """
        league_seasons = self.get_league_seasons()
        if len(league_seasons) == 0:
            return None
        return LeagueSeason.query.filter_by(league_id=league_name, season_id=season_year).first()

    def add_league_season(self, league_season: LeagueSeason) -> LeagueSeason:
        """
        Adds a league_season to the data store.

        :param league_season: The league_season to add.

        :return: The added league_season.
        """
        sqla.session.add(league_season)
        sqla.session.commit()
        return league_season

    def add_league_seasons(self, league_seasons: tuple) -> tuple:
        """
        Adds a collection of league_seasons to the data store.

        :param league_seasons: The league_seasons to add.

        :return: The added league_seasons.
        """
        for league_season in league_seasons:
            sqla.session.add(league_season)
        sqla.session.commit()
        return league_seasons

    def update_league_season(self, league_season: LeagueSeason) -> LeagueSeason | None:
        """
        Updates a league_season in the data store.

        :param league_season: The league_season to update.

        :return: The updated league_season.
        """
        if not self.league_season_exists(league_season.id):
            return league_season

        league_season_to_update = self.get_league_season(league_season.id)
        league_season_to_update.league_name = league_season.league_name
        league_season_to_update.season_year = league_season.season_year
        league_season_to_update.total_games = league_season.total_games
        league_season_to_update.total_points = league_season.total_points
        league_season_to_update.average_points = league_season.average_points
        sqla.session.add(league_season_to_update)
        sqla.session.commit()
        return league_season

    def delete_league_season(self, id: int) -> LeagueSeason | None:
        """
        Deletes a league_season from the data store.

        :param id: The id of the league_season to delete.

        :return: The deleted league_season.
        """
        if not self.league_season_exists(id):
            return None

        league_season = self.get_league_season(id)
        sqla.session.delete(league_season)
        sqla.session.commit()
        return league_season

    def league_season_exists(self, id: int) -> bool:
        """
        Checks to verify whether a specific league_season exists in the data store.

        :param id: The id of the league_season to verify.

        :return: True if the league_season with the specified id exists in the data store; otherwise false.
        """
        return sqla.session.query(exists().where(LeagueSeason.id == id)).scalar()
