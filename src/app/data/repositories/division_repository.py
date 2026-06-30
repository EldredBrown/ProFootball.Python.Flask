from typing import List, Optional

from sqlalchemy.orm import joinedload

from app.data.models.division import Division
from app.data.sqla import sqla, try_commit


class DivisionRepository:
    """
    Provides CRUD access to an external data store.
    """

    def get_divisions(self) -> List[Division]:
        """
        Gets all the divisions in the data store.

        :return: A list of all fetched divisions.
        """
        divisions = self._get_divisions_with_navigation_properties()
        return divisions.all()

    def get_division(self, id: int) -> Optional[Division]:
        """
        Gets the division in the data store with the specified id.

        :param id: The id of the division to fetch.

        :return: The fetched division.
        """
        divisions = self._get_divisions_with_navigation_properties()
        if len(divisions.all()) == 0:
            return None
        return divisions.get(id)

    def get_division_by_name(self, name: str) -> Optional[Division]:
        """
        Gets the division in the data store with the specified id.

        :param short_name: The short_name of the division to fetch.

        :return: The fetched division.
        """
        divisions = self._get_divisions_with_navigation_properties()
        if len(divisions.all()) == 0:
            return None
        return divisions.filter_by(name=name).first()

    def add_division(self, division: Division) -> Division:
        """
        Adds a division to the data store.

        :param **kwargs: A keyword args dictionary containing values for the division to add.

        :return: The added division.
        """
        sqla.session.add(division)
        try_commit()
        return division

    def add_divisions(self, divisions: tuple) -> tuple:
        """
        Adds a collection of division_args dictionaries to the data store.

        :param division_args: The tuple of division keyword args dictionaries to add.

        :return: The added divisions.
        """
        for division in divisions:
            sqla.session.add(division)
        try_commit()
        return divisions

    def update_division(self, division: Division) -> Optional[Division]:
        """
        Updates a division in the data store.

        :param division: The division to update.

        :return: The updated division.
        """
        if not self.division_exists(division.id):
            return division
        division_in_db = self._set_values_of_division_in_db(division)
        sqla.session.add(division_in_db)
        try_commit()
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
        try_commit()
        return division

    def division_exists(self, id: int) -> bool:
        """
        Checks to verify whether a specific division exists in the data store.

        :param id: The id of the division to verify.

        :return: True if the division with the specified id exists in the data store; otherwise false.
        """
        return self.get_division(id) is not None

    def _get_divisions_with_navigation_properties(self):
        return Division.query.options(joinedload(Division.league), joinedload(Division.conference))

    def _set_values_of_division_in_db(self, division: Division) -> Division | None:
        division_in_db = self.get_division(division.id)
        division_in_db.name = division.name
        division_in_db.league_id = division.league_id
        division_in_db.conference_id = division.conference_id
        division_in_db.first_season_id = division.first_season_id
        division_in_db.last_season_id = division.last_season_id
        return division_in_db
