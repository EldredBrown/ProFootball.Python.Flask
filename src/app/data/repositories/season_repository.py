from typing import List

from sqlalchemy.exc import IntegrityError

from app.data.models.season import Season
from app.data.sqla import sqla


class SeasonRepository:
    """
    Provides CRUD access to an external data store.
    """

    def __init__(self) -> None:
        """
        Initializes a new instance of the SeasonRepository class.
        """
        pass

    def get_seasons(self) -> List[Season]:
        """
        Gets all the seasons in the data store.

        :return: A list of all fetched seasons.
        """
        return Season.query.all()

    def get_season(self, id: int) -> Season | None:
        """
        Gets the season in the data store with the specified id.

        :param id: The id of the season to fetch.

        :return: The fetched season.
        """
        seasons = self.get_seasons()
        if len(seasons) == 0:
            return None
        return Season.query.get(id)

    def get_season_by_year(self, year: int) -> Season | None:
        """
        Gets the season in the data store with the specified id.

        :param year: The year of the season to fetch.

        :return: The fetched season.
        """
        seasons = self.get_seasons()
        if len(seasons) == 0:
            return None
        return Season.query.filter_by(year=year).first()

    def add_season(self, season: Season) -> Season:
        """
        Adds a season to the data store.

        :param season: The season to add.

        :return: The added season.
        """
        sqla.session.add(season)
        try:
            sqla.session.commit()
        except IntegrityError:
            sqla.session.rollback()
            raise
        return season

    def add_seasons(self, seasons: tuple) -> tuple:
        """
        Adds a collection of season_args dictionaries to the data store.

        :param seasons: The seasons to add.

        :return: The added seasons.
        """
        for season in seasons:
            sqla.session.add(season)
        try:
            sqla.session.commit()
        except IntegrityError:
            sqla.session.rollback()
            raise
        return seasons

    def update_season(self, season: Season) -> Season | None:
        """
        Updates a season in the data store.

        :param season: The season to update.

        :return: The updated season.
        """
        if not self.season_exists(season.id):
            return season

        old_season = self.get_season(season.id)
        old_season.year = season.year
        old_season.num_of_weeks_scheduled = season.num_of_weeks_scheduled
        old_season.num_of_weeks_completed = season.num_of_weeks_completed

        sqla.session.add(old_season)
        try:
            sqla.session.commit()
        except IntegrityError:
            sqla.session.rollback()
            raise

        return season

    def delete_season(self, id: int) -> Season | None:
        """
        Deletes a season from the data store.

        :param id: The id of the season to delete.

        :return: The deleted season.
        """
        if not self.season_exists(id):
            return None

        season = self.get_season(id)
        sqla.session.delete(season)
        try:
            sqla.session.commit()
        except IntegrityError:
            sqla.session.rollback()
            raise
        return season

    def season_exists(self, id: int) -> bool:
        """
        Checks to verify whether a specific season exists in the data store.

        :param id: The id of the season to verify.

        :return: True if the season with the specified id exists in the data store; otherwise false.
        """
        return self.get_season(id) is not None
