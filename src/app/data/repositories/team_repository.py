from typing import List

from sqlalchemy import exists

from app.data.models.team import Team
from app.data.sqla import sqla


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

    def get_team_by_name(self, name: str) -> Team | None:
        """
        Gets the team in the data store with the specified id.

        :param name: The year of the team to fetch.

        :return: The fetched team.
        """
        teams = self.get_teams()
        if len(teams) == 0:
            return None
        return Team.query.filter_by(name=name).first()

    def add_team(self, team: Team) -> Team:
        """
        Adds a team to the data store.

        :param team: The team to add.

        :return: The added team.
        """
        sqla.session.add(team)
        sqla.session.commit()
        return team

    def add_teams(self, teams: tuple) -> tuple:
        """
        Adds a collection of teams to the data store.

        :param teams: The teams to add.

        :return: The added teams.
        """
        for team in teams:
            sqla.session.add(team)
        sqla.session.commit()
        return teams

    def update_team(self, team: Team) -> Team | None:
        """
        Updates a team in the data store.

        :param team: The team to update.

        :return: The updated team.
        """
        if not self.team_exists(team.id):
            return team

        team_to_update = self.get_team(team.id)
        team_to_update.name = team.name
        sqla.session.add(team_to_update)
        sqla.session.commit()
        return team

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
        return sqla.session.query(exists().where(Team.id == id)).scalar()
