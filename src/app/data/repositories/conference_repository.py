from typing import List

from sqlalchemy import exists

from app.data.models.conference import Conference
from app.data.sqla import sqla


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

    def get_conference(self, id: int) -> Conference | None:
        """
        Gets the conference in the data store with the specified id.

        :param id: The id of the conference to fetch.

        :return: The fetched conference.
        """
        conferences = self.get_conferences()
        if len(conferences) == 0:
            return None
        return Conference.query.get(id)

    def get_conference_by_name(self, short_name: str) -> Conference | None:
        """
        Gets the conference in the data store with the specified id.

        :param short_name: The year of the conference to fetch.

        :return: The fetched conference.
        """
        conferences = self.get_conferences()
        if len(conferences) == 0:
            return None
        return Conference.query.filter_by(short_name=short_name).first()

    def add_conference(self, conference: Conference) -> Conference:
        """
        Adds a conference to the data store.

        :param conference: The conference to add.

        :return: The added conference.
        """
        sqla.session.add(conference)
        sqla.session.commit()
        return conference

    def add_conferences(self, conferences: tuple) -> tuple:
        """
        Adds a collection of conferences to the data store.

        :param conferences: The conferences to add.

        :return: The added conferences.
        """
        for conference in conferences:
            sqla.session.add(conference)
        sqla.session.commit()
        return conferences

    def update_conference(self, conference: Conference) -> Conference | None:
        """
        Updates a conference in the data store.

        :param conference: The conference to update.

        :return: The updated conference.
        """
        if not self.conference_exists(conference.id):
            return conference

        conference_to_update = self.get_conference(conference.id)
        conference_to_update.short_name = conference.short_name
        conference_to_update.long_name = conference.long_name
        conference_to_update.league_name = conference.league_name
        conference_to_update.first_season_year = conference.first_season_year
        conference_to_update.last_season_year = conference.last_season_year
        sqla.session.add(conference_to_update)
        sqla.session.commit()
        return conference

    def delete_conference(self, id: int) -> Conference | None:
        """
        Deletes a conference from the data store.

        :param id: The id of the conference to delete.

        :return: The deleted conference.
        """
        if not self.conference_exists(id):
            return None

        conference = self.get_conference(id)
        sqla.session.delete(conference)
        sqla.session.commit()
        return conference

    def conference_exists(self, id: int) -> bool:
        """
        Checks to verify whether a specific conference exists in the data store.

        :param id: The id of the conference to verify.

        :return: True if the conference with the specified id exists in the data store; otherwise false.
        """
        return sqla.session.query(exists().where(Conference.id == id)).scalar()
