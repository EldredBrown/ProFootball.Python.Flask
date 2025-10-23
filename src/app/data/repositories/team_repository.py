from typing import List

from sqlalchemy.exc import IntegrityError

from app.data.models.team import Team
from app.data.sqla import sqla
from app.data.factories import team_factory


class TeamRepository:
    """
    Provides CRUD access to an external data store.
    """

    def __init__(self) -> None:
        """
        Initializes a new instance of the TeamRepository class.
        """
        pass

    def get_teams(self) -> List[Team]:
        """
        Gets all the teams in the data store.

        :return: A list of all fetched teams.
        """
        return Team.query.all()

    def get_team(self, id: int) -> Team | None:
        """
        Gets the team in the data store with the specified id.

        :param id: The id of the team to fetch.

        :return: The fetched team.
        """
        teams = self.get_teams()
        if len(teams) == 0:
            return None
        return Team.query.get(id)

    def get_team_by_name(self, short_name: str) -> Team | None:
        """
        Gets the team in the data store with the specified id.

        :param short_name: The short_name of the team to fetch.

        :return: The fetched team.
        """
        teams = self.get_teams()
        if len(teams) == 0:
            return None
        return Team.query.filter_by(short_name=short_name).first()

    def add_team(self, **kwargs) -> Team:
        """
        Adds a team to the data store.

        :param **kwargs: A keyword args dictionary containing values for the team to add.

        :return: The added team.
        """
        team = team_factory.create_team(**kwargs)
        sqla.session.add(team)
        try:
            sqla.session.commit()
        except IntegrityError:
            sqla.session.rollback()
            raise
        return team

    def add_teams(self, team_args: tuple) -> List[Team]:
        """
        Adds a collection of team_args dictionaries to the data store.

        :param team_args: The tuple of team keyword args dictionaries to add.

        :return: The added teams.
        """
        teams = []
        try:
            for kwargs in team_args:
                team = team_factory.create_team(kwargs)
                teams.append(team)
                sqla.session.add(team)
            sqla.session.commit()
        except IntegrityError:
            sqla.session.rollback()
            raise
        return teams

    def update_team(self, **kwargs) -> Team | None:
        """
        Updates a team in the data store.

        :param team: The team to update.

        :return: The updated team.
        """
        if 'id' not in kwargs:
            raise ValueError("ID must be provided for existing Team.")

        if not self.team_exists(kwargs['id']):
            return Team(**kwargs)

        old_team = self.get_team(kwargs['id'])
        new_team = team_factory.create_team(old_team, **kwargs)

        old_team.name = new_team.name

        sqla.session.add(old_team)
        try:
            sqla.session.commit()
        except IntegrityError:
            sqla.session.rollback()
            raise

        return new_team

    def delete_team(self, id: int) -> Team | None:
        """
        Deletes a team from the data store.

        :param id: The id of the team to delete.

        :return: The deleted team.
        """
        if not self.team_exists(id):
            return None

        team = self.get_team(id)
        sqla.session.delete(team)
        sqla.session.commit()
        return team

    def team_exists(self, id: int) -> bool:
        """
        Checks to verify whether a specific team exists in the data store.

        :param id: The id of the team to verify.

        :return: True if the team with the specified id exists in the data store; otherwise false.
        """
        return self.get_team(id) is not None
