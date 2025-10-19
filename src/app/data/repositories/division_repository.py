from typing import List

from sqlalchemy import exists

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

    def get_division_by_name(self, name: str) -> Division | None:
        """
        Gets the division in the data store with the specified id.

        :param name: The year of the division to fetch.

        :return: The fetched division.
        """
        divisions = self.get_divisions()
        if len(divisions) == 0:
            return None
        return Division.query.filter_by(name=name).first()

    def add_division(self, division: Division) -> Division:
        """
        Adds a division to the data store.

        :param division: The division to add.

        :return: The added division.
        """
        sqla.session.add(division)
        sqla.session.commit()
        return division

    def add_divisions(self, divisions: tuple) -> tuple:
        """
        Adds a collection of divisions to the data store.

        :param divisions: The divisions to add.

        :return: The added divisions.
        """
        for division in divisions:
            sqla.session.add(division)
        sqla.session.commit()
        return divisions

    def update_division(self, division: Division) -> Division | None:
        """
        Updates a division in the data store.

        :param division: The division to update.

        :return: The updated division.
        """
        if not self.division_exists(division.id):
            return division

        division_to_update = self.get_division(division.id)
        division_to_update.name = division.name
        division_to_update.league_name = division.league_name
        division_to_update.conference_name = division.conference_name
        division_to_update.first_season_year = division.first_season_year
        division_to_update.last_season_year = division.last_season_year
        sqla.session.add(division_to_update)
        sqla.session.commit()
        return division

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
        return sqla.session.query(exists().where(Division.id == id)).scalar()
