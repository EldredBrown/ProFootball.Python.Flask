from typing import List

from sqlalchemy.exc import IntegrityError

from app.data.models.conference import Conference
from app.data.sqla import sqla
from app.data.factories import conference_factory


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

        :param short_name: The short_name of the conference to fetch.

        :return: The fetched conference.
        """
        conferences = self.get_conferences()
        if len(conferences) == 0:
            return None
        return Conference.query.filter_by(short_name=short_name).first()

    def add_conference(self, **kwargs) -> Conference:
        """
        Adds a conference to the data store.

        :param **kwargs: A keyword args dictionary containing values for the conference to add.

        :return: The added conference.
        """
        conference = conference_factory.create_conference(**kwargs)
        sqla.session.add(conference)
        try:
            sqla.session.commit()
        except IntegrityError:
            sqla.session.rollback()
            raise
        return conference

    def add_conferences(self, conference_args: tuple) -> List[Conference]:
        """
        Adds a collection of conference_args dictionaries to the data store.

        :param conference_args: The tuple of conference keyword args dictionaries to add.

        :return: The added conferences.
        """
        conferences = []
        try:
            for kwargs in conference_args:
                conference = conference_factory.create_conference(kwargs)
                conferences.append(conference)
                sqla.session.add(conference)
            sqla.session.commit()
        except IntegrityError:
            sqla.session.rollback()
            raise
        return conferences

    def update_conference(self, **kwargs) -> Conference | None:
        """
        Updates a conference in the data store.

        :param conference: The conference to update.

        :return: The updated conference.
        """
        if 'id' not in kwargs:
            raise ValueError("ID must be provided for existing Conference.")

        if not self.conference_exists(kwargs['id']):
            return Conference(**kwargs)

        old_conference = self.get_conference(kwargs['id'])
        new_conference = conference_factory.create_conference(old_conference, **kwargs)

        old_conference.short_name = new_conference.short_name
        old_conference.long_name = new_conference.long_name
        old_conference.league_name = new_conference.league_name
        old_conference.first_season_year = new_conference.first_season_year
        old_conference.last_season_year = new_conference.last_season_year

        sqla.session.add(old_conference)
        try:
            sqla.session.commit()
        except IntegrityError:
            sqla.session.rollback()
            raise

        return new_conference

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
        return self.get_conference(id) is not None
