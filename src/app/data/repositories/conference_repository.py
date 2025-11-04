from typing import List, Optional

from app.data.models.conference import Conference
from app.data.sqla import sqla, try_commit


class ConferenceRepository:
    """
    Provides CRUD access to an external data store.
    """

    def __init__(self) -> None:
        """
        Initializes a new instance of the ConferenceRepository class.
        """
        pass

    def get_conferences(self) -> List[Conference]:
        """
        Gets all the conferences in the data store.

        :return: A list of all fetched conferences.
        """
        return Conference.query.all()

    def get_conference(self, id: int) -> Optional[Conference]:
        """
        Gets the conference in the data store with the specified id.

        :param id: The id of the conference to fetch.

        :return: The fetched conference.
        """
        if self._conferences_empty():
            return None
        return Conference.query.get(id)

    def get_conference_by_name(self, short_name: str) -> Optional[Conference]:
        """
        Gets the conference in the data store with the specified id.

        :param short_name: The short_name of the conference to fetch.

        :return: The fetched conference.
        """
        if self._conferences_empty():
            return None
        return Conference.query.filter_by(short_name=short_name).first()

    def _conferences_empty(self) -> bool:
        conferences = self.get_conferences()
        return len(conferences) == 0

    def add_conference(self, conference: Conference) -> Conference:
        """
        Adds a conference to the data store.

        :param **kwargs: A keyword args dictionary containing values for the conference to add.

        :return: The added conference.
        """
        sqla.session.add(conference)
        try_commit()
        return conference

    def add_conferences(self, conferences: tuple) -> tuple:
        """
        Adds a collection of conference_args dictionaries to the data store.

        :param conference_args: The tuple of conference keyword args dictionaries to add.

        :return: The added conferences.
        """
        for conference in conferences:
            sqla.session.add(conference)
        try_commit()
        return conferences

    def update_conference(self, conference: Conference) -> Optional[Conference]:
        """
        Updates a conference in the data store.

        :param conference: The conference to update.

        :return: The updated conference.
        """
        if not self.conference_exists(conference.id):
            return conference
        conference_in_db = self._set_values_of_conference_in_db(conference)
        sqla.session.add(conference_in_db)
        try_commit()
        return conference

    def _set_values_of_conference_in_db(self, conference: Conference) -> Conference:
        conference_in_db = self.get_conference(conference.id)
        conference_in_db.short_name = conference.short_name
        conference_in_db.long_name = conference.long_name
        conference_in_db.league_name = conference.league_name
        conference_in_db.first_season_year = conference.first_season_year
        conference_in_db.last_season_year = conference.last_season_year
        return conference_in_db

    def delete_conference(self, id: int) -> Optional[Conference]:
        """
        Deletes a conference from the data store.

        :param id: The id of the conference to delete.

        :return: The deleted conference.
        """
        if not self.conference_exists(id):
            return None
        conference = self.get_conference(id)
        sqla.session.delete(conference)
        try_commit()
        return conference

    def conference_exists(self, id: int) -> bool:
        """
        Checks to verify whether a specific conference exists in the data store.

        :param id: The id of the conference to verify.

        :return: True if the conference with the specified id exists in the data store; otherwise false.
        """
        return self.get_conference(id) is not None
