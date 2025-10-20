from typing import List

from app.data.models.season import Season
from app.data.models.game import Game
from app.data.models.team_season import TeamSeason
from app.data.models.league_season import LeagueSeason
from app.data.sqla import sqla
from app.services.data_factories import season_factory


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

    def add_season(self, **kwargs) -> Season:
        """
        Adds a season to the data store.

        :param **kwargs: A keyword args dictionary containing values for the season to add.

        :return: The added season.
        """
        season = season_factory.create_season(**kwargs)
        sqla.session.add(season)
        sqla.session.commit()
        return season

    def add_seasons(self, season_args: tuple) -> List[Season]:
        """
        Adds a collection of season_args dictionaries to the data store.

        :param season_args: The tuple of season keyword args dictionaries to add.

        :return: The added seasons.
        """
        seasons = []
        for kwargs in season_args:
            season = season_factory.create_season(kwargs)
            seasons.append(season)
            sqla.session.add(season)
        sqla.session.commit()
        return seasons

    def update_season(self, **kwargs) -> Season | None:
        """
        Updates a season in the data store.

        :param season: The season to update.

        :return: The updated season.
        """
        if 'id' not in kwargs:
            raise ValueError("ID must be provided for existing Season.")

        if not self.season_exists(kwargs['id']):
            return Season(**kwargs)

        old_season = self.get_season(kwargs['id'])
        new_season = season_factory.create_season(old_season, **kwargs)

        old_season.year = new_season.year
        old_season.num_of_weeks_scheduled = new_season.num_of_weeks_scheduled
        old_season.num_of_weeks_completed = new_season.num_of_weeks_completed

        sqla.session.add(old_season)
        sqla.session.commit()

        return new_season

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
        sqla.session.commit()
        return season

    def season_exists(self, id: int) -> bool:
        """
        Checks to verify whether a specific season exists in the data store.

        :param id: The id of the season to verify.

        :return: True if the season with the specified id exists in the data store; otherwise false.
        """
        return self.get_season(id) is not None
