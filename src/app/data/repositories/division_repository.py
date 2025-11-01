from typing import List, Optional

from sqlalchemy.exc import IntegrityError

from app.data.models.division import Division
from app.data.sqla import sqla


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

    def get_division(self, id: int) -> Optional[Division]:
        """
        Gets the division in the data store with the specified id.

        :param id: The id of the division to fetch.

        :return: The fetched division.
        """
        divisions = self.get_divisions()
        if len(divisions) == 0:
            return None
        return Division.query.get(id)

    def get_division_by_name(self, short_name: str) -> Optional[Division]:
        """
        Gets the division in the data store with the specified id.

        :param short_name: The short_name of the division to fetch.

        :return: The fetched division.
        """
        divisions = self.get_divisions()
        if len(divisions) == 0:
            return None
        return Division.query.filter_by(short_name=short_name).first()

    def add_division(self, division: Division) -> Division:
        """
        Adds a division to the data store.

        :param **kwargs: A keyword args dictionary containing values for the division to add.

        :return: The added division.
        """
        sqla.session.add(division)
        try:
            sqla.session.commit()
        except IntegrityError:
            sqla.session.rollback()
            raise
        return division

    def add_divisions(self, divisions: tuple) -> tuple:
        """
        Adds a collection of division_args dictionaries to the data store.

        :param division_args: The tuple of division keyword args dictionaries to add.

        :return: The added divisions.
        """
        for division in divisions:
            sqla.session.add(division)
        try:
            sqla.session.commit()
        except IntegrityError:
            sqla.session.rollback()
            raise
        return divisions

    def update_division(self, division: Division) -> Optional[Division]:
        """
        Updates a division in the data store.

        :param division: The division to update.

        :return: The updated division.
        """
        if not self.division_exists(division.id):
            return division

        old_division = self.get_division(division.id)
        old_division.name = division.name
        old_division.league_name = division.league_name
        old_division.conference_name = division.conference_name
        old_division.first_season_year = division.first_season_year
        old_division.last_season_year = division.last_season_year

        sqla.session.add(old_division)
        try:
            sqla.session.commit()
        except IntegrityError:
            sqla.session.rollback()
            raise

        return division

    def delete_division(self, id: int) -> Optional[Division]:
        """
        Deletes a division from the data store.

        :param id: The id of the division to delete.

        :return: The deleted division.
        """
        if not self.division_exists(id):
            return None

        division = self.get_division(id)
        sqla.session.delete(division)
        try:
            sqla.session.commit()
        except IntegrityError:
            sqla.session.rollback()
            raise
        return division

    def division_exists(self, id: int) -> bool:
        """
        Checks to verify whether a specific division exists in the data store.

        :param id: The id of the division to verify.

        :return: True if the division with the specified id exists in the data store; otherwise false.
        """
        return self.get_division(id) is not None
