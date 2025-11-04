from typing import List, Optional

from sqlalchemy.exc import IntegrityError

from app.data.models.team import Team
from app.data.sqla import sqla, try_commit


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

    def get_team(self, id: int) -> Optional[Team]:
        """
        Gets the team in the data store with the specified id.

        :param id: The id of the team to fetch.

        :return: The fetched team.
        """
        if self._teams_empty():
            return None
        return Team.query.get(id)

    def get_team_by_name(self, short_name: str) -> Optional[Team]:
        """
        Gets the team in the data store with the specified id.

        :param short_name: The short_name of the team to fetch.

        :return: The fetched team.
        """
        if self._teams_empty():
            return None
        return Team.query.filter_by(short_name=short_name).first()

    def _teams_empty(self) -> bool:
        teams = self.get_teams()
        return len(teams) == 0

    def add_team(self, team: Team) -> Team:
        """
        Adds a team to the data store.

        :param **kwargs: A keyword args dictionary containing values for the team to add.

        :return: The added team.
        """
        sqla.session.add(team)
        try_commit()
        return team

    def add_teams(self, teams: tuple) -> tuple:
        """
        Adds a collection of team_args dictionaries to the data store.

        :param team_args: The tuple of team keyword args dictionaries to add.

        :return: The added teams.
        """
        for team in teams:
            sqla.session.add(team)
        try_commit()
        return teams

    def update_team(self, team: Team) -> Optional[Team]:
        """
        Updates a team in the data store.

        :param team: The team to update.

        :return: The updated team.
        """
        if not self.team_exists(team.id):
            return team
        team_in_db = self._set_values_of_team_in_db(team)
        sqla.session.add(team_in_db)
        try_commit()
        return team

    def _set_values_of_team_in_db(self, team: Team) -> Team:
        team_in_db = self.get_team(team.id)
        team_in_db.name = team.name
        return team_in_db

    def delete_team(self, id: int) -> Optional[Team]:
        """
        Deletes a team from the data store.

        :param id: The id of the team to delete.

        :return: The deleted team.
        """
        if not self.team_exists(id):
            return None
        team = self.get_team(id)
        sqla.session.delete(team)
        try_commit()
        return team

    def team_exists(self, id: int) -> bool:
        """
        Checks to verify whether a specific team exists in the data store.

        :param id: The id of the team to verify.

        :return: True if the team with the specified id exists in the data store; otherwise false.
        """
        return self.get_team(id) is not None
