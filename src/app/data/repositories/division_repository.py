from typing import List

from sqlalchemy.exc import IntegrityError

from app.data.models.division import Division
from app.data.sqla import sqla
from app.data.factories import division_factory


class DivisionRepository:
    """
    Provides CRUD access to an external data store.
    """

    def __init__(self) -> None:
        """
        Initializes a new instance of the DivisionRepository class.
        """
        pass

    def get_divisions(self) -> List[Division]:
        """
        Gets all the divisions in the data store.

        :return: A list of all fetched divisions.
        """
        return Division.query.all()

    def get_division(self, id: int) -> Division | None:
        """
        Gets the division in the data store with the specified id.

        :param id: The id of the division to fetch.

        :return: The fetched division.
        """
        divisions = self.get_divisions()
        if len(divisions) == 0:
            return None
        return Division.query.get(id)

    def get_division_by_name(self, short_name: str) -> Division | None:
        """
        Gets the division in the data store with the specified id.

        :param short_name: The short_name of the division to fetch.

        :return: The fetched division.
        """
        divisions = self.get_divisions()
        if len(divisions) == 0:
            return None
        return Division.query.filter_by(short_name=short_name).first()

    def add_division(self, **kwargs) -> Division:
        """
        Adds a division to the data store.

        :param **kwargs: A keyword args dictionary containing values for the division to add.

        :return: The added division.
        """
        division = division_factory.create_division(**kwargs)
        sqla.session.add(division)
        try:
            sqla.session.commit()
        except IntegrityError:
            sqla.session.rollback()
            raise
        return division

    def add_divisions(self, division_args: tuple) -> List[Division]:
        """
        Adds a collection of division_args dictionaries to the data store.

        :param division_args: The tuple of division keyword args dictionaries to add.

        :return: The added divisions.
        """
        divisions = []
        try:
            for kwargs in division_args:
                division = division_factory.create_division(kwargs)
                divisions.append(division)
                sqla.session.add(division)
            sqla.session.commit()
        except IntegrityError:
            sqla.session.rollback()
            raise
        return divisions

    def update_division(self, **kwargs) -> Division | None:
        """
        Updates a division in the data store.

        :param division: The division to update.

        :return: The updated division.
        """
        if 'id' not in kwargs:
            raise ValueError("ID must be provided for existing Division.")

        if not self.division_exists(kwargs['id']):
            return Division(**kwargs)

        old_division = self.get_division(kwargs['id'])
        new_division = division_factory.create_division(old_division, **kwargs)

        old_division.name = new_division.name
        old_division.league_name = new_division.league_name
        old_division.conference_name = new_division.conference_name
        old_division.first_season_year = new_division.first_season_year
        old_division.last_season_year = new_division.last_season_year

        sqla.session.add(old_division)
        try:
            sqla.session.commit()
        except IntegrityError:
            sqla.session.rollback()
            raise

        return new_division

    def delete_division(self, id: int) -> Division | None:
        """
        Deletes a division from the data store.

        :param id: The id of the division to delete.

        :return: The deleted division.
        """
        if not self.division_exists(id):
            return None

        division = self.get_division(id)
        sqla.session.delete(division)
        sqla.session.commit()
        return division

    def division_exists(self, id: int) -> bool:
        """
        Checks to verify whether a specific division exists in the data store.

        :param id: The id of the division to verify.

        :return: True if the division with the specified id exists in the data store; otherwise false.
        """
        return self.get_division(id) is not None
