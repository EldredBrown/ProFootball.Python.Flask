from typing import List, Optional

from sqlalchemy.orm import joinedload

from app.data.models.league_season import LeagueSeason
from app.data.sqla import sqla, try_commit


class LeagueSeasonRepository:
    """
    Provides CRUD access to an external data store.
    """

    def get_league_seasons(self) -> List[LeagueSeason]:
        """
        Gets all the league_seasons in the data store.

        :return: A list of all fetched league_seasons.
        """
        league_seasons = self._get_league_seasons_with_navigation_properties()
        return league_seasons.all()

    def get_league_seasons_by_league(self, league_id: int) -> List[LeagueSeason]:
        """
        Gets all the league_seasons in the data store.

        :return: A list of all fetched league_seasons.
        """
        league_seasons = self._get_league_seasons_with_navigation_properties()
        return league_seasons.filter_by(league_id=league_id).all()

    def get_league_seasons_by_season(self, season_id: int) -> List[LeagueSeason]:
        """
        Gets all the league_seasons in the data store.

        :return: A list of all fetched league_seasons.
        """
        league_seasons = self._get_league_seasons_with_navigation_properties()
        return league_seasons.filter_by(season_id=season_id).all()

    def get_league_season(self, id: int) -> Optional[LeagueSeason]:
        """
        Gets the league_season in the data store with the specified id.

        :param id: The id of the league_season to fetch.

        :return: The fetched league_season.
        """
        league_seasons = self._get_league_seasons_with_navigation_properties()
        if len(league_seasons.all()) == 0:
            return None
        return league_seasons.get(id)

    def get_league_season_by_league_and_season(self, league_id: int, season_id: int) -> Optional[LeagueSeason]:
        """
        Gets the league_season in the data store with the specified league_name and season_year.

        :param league_id: The league_name of the league_season to fetch.
        :param season_id: The season_year of the league_season to fetch.

        :return: The fetched league_season.
        """
        league_seasons = self._get_league_seasons_with_navigation_properties()
        if len(league_seasons.all()) == 0:
            return None
        return league_seasons.filter_by(league_id=league_id, season_id=season_id).first()

    def add_league_season(self, league_season: LeagueSeason) -> LeagueSeason:
        """
        Adds a league_season to the data store.

        :param league_season: The league_season to add.

        :return: The added league_season.
        """
        sqla.session.add(league_season)
        try_commit()
        return league_season

    def add_league_seasons(self, league_seasons: tuple) -> tuple:
        """
        Adds a collection of league_seasons to the data store.

        :param league_seasons: The league_seasons to add.

        :return: The added league_seasons.
        """
        for league_season in league_seasons:
            sqla.session.add(league_season)
        try_commit()
        return league_seasons

    def update_league_season(self, league_season: LeagueSeason) -> Optional[LeagueSeason]:
        """
        Updates a league_season in the data store.

        :param league_season: The league_season to update.

        :return: The updated league_season.
        """
        if not self.league_season_exists(league_season.id):
            return league_season
        league_season_in_db = self._set_values_of_league_season_in_db(league_season)
        sqla.session.add(league_season_in_db)
        try_commit()
        return league_season

    def delete_league_season(self, id: int) -> Optional[LeagueSeason]:
        """
        Deletes a league_season from the data store.

        :param id: The id of the league_season to delete.

        :return: The deleted league_season.
        """
        if not self.league_season_exists(id):
            return None
        league_season = self.get_league_season(id)
        sqla.session.delete(league_season)
        try_commit()
        return league_season

    def league_season_exists(self, id: int) -> bool:
        """
        Checks to verify whether a specific league_season exists in the data store.

        :param id: The id of the league_season to verify.

        :return: True if the league_season with the specified id exists in the data store; otherwise false.
        """
        return self.get_league_season(id) is not None

    def _get_league_seasons_with_navigation_properties(self):
        return LeagueSeason.query.options(
            joinedload(LeagueSeason.league),
            joinedload(LeagueSeason.season)
        )

    def _set_values_of_league_season_in_db(self, league_season: LeagueSeason) -> LeagueSeason | None:
        league_season_in_db = self.get_league_season(league_season.id)
        league_season_in_db.league_id = league_season.league_id
        league_season_in_db.season_id = league_season.season_id
        return league_season_in_db
