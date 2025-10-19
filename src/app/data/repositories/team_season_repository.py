from typing import List

from sqlalchemy import exists

from app.data.models.team_season import TeamSeason
from app.data.sqla import sqla


class TeamSeasonRepository:
    """
    Provides CRUD access to an external data store.
    """

    def __init__(self) -> None:
        """
        Initializes a new instance of the TeamSeasonRepository class.
        """
        pass

    def get_team_seasons(self) -> List[TeamSeason]:
        """
        Gets all the team_seasons in the data store.

        :return: A list of all fetched team_seasons.
        """
        return TeamSeason.query.all()

    def get_team_season(self, id: int) -> TeamSeason | None:
        """
        Gets the team_season in the data store with the specified id.

        :param id: The id of the team_season to fetch.

        :return: The fetched team_season.
        """
        team_seasons = self.get_team_seasons()
        if len(team_seasons) == 0:
            return None
        return TeamSeason.query.get(id)

    def get_team_seasons_by_season(self, season_year: int) -> List[TeamSeason] | None:
        """
        Gets the team_seasons in the data store with the specified season_year.

        :param season_year: The season_year of the team_season to fetch.

        :return: The fetched team_seasons.
        """
        team_seasons = self.get_team_seasons()
        if len(team_seasons) == 0:
            return None
        return TeamSeason.query.filter_by(season_year=season_year).fetchall()

    def get_team_season_by_team_and_season(self, team_name: str, season_year: int) -> TeamSeason | None:
        """
        Gets the team_season in the data store with the specified team_name and season_year.

        :param team_name: The team_name of the team_season to fetch.
        :param season_year: The season_year of the team_season to fetch.

        :return: The fetched team_season.
        """
        team_seasons = self.get_team_seasons()
        if len(team_seasons) == 0:
            return None
        return TeamSeason.query.filter_by(team_name=team_name, season_year=season_year).first()

    def add_team_season(self, team_season: TeamSeason) -> TeamSeason:
        """
        Adds a team_season to the data store.

        :param team_season: The team_season to add.

        :return: The added team_season.
        """
        sqla.session.add(team_season)
        sqla.session.commit()
        return team_season

    def add_team_seasons(self, team_seasons: tuple) -> tuple:
        """
        Adds a collection of team_seasons to the data store.

        :param team_seasons: The team_seasons to add.

        :return: The added team_seasons.
        """
        for team_season in team_seasons:
            sqla.session.add(team_season)
        sqla.session.commit()
        return team_seasons

    def update_team_season(self, team_season: TeamSeason) -> TeamSeason | None:
        """
        Updates a team_season in the data store.

        :param team_season: The team_season to update.

        :return: The updated team_season.
        """
        if not self.team_season_exists(team_season.id):
            return team_season

        team_season_to_update = self.get_team_season(team_season.id)
        team_season_to_update.team_name = team_season.team_name
        team_season_to_update.season_year = team_season.season_year
        team_season_to_update.league_name = team_season.league_name
        team_season_to_update.conference_name = team_season.conference_name
        team_season_to_update.division_name = team_season.division_name
        team_season_to_update.games = team_season.games
        team_season_to_update.wins = team_season.wins
        team_season_to_update.losses = team_season.losses
        team_season_to_update.ties = team_season.ties
        team_season_to_update.winning_percentage = team_season.winning_percentage
        team_season_to_update.points_for = team_season.points_for
        team_season_to_update.points_against = team_season.points_against
        team_season_to_update.expected_wins = team_season.expected_wins
        team_season_to_update.expected_losses = team_season.expected_losses
        team_season_to_update.offensive_average = team_season.offensive_average
        team_season_to_update.offensive_factor = team_season.offensive_factor
        team_season_to_update.offensive_index = team_season.offensive_index
        team_season_to_update.defensive_average = team_season.defensive_average
        team_season_to_update.defensive_factor = team_season.defensive_factor
        team_season_to_update.defensive_index = team_season.defensive_index
        team_season_to_update.final_expected_winning_percentage = team_season.final_expected_winning_percentage
        sqla.session.add(team_season_to_update)
        sqla.session.commit()
        return team_season

    def delete_team_season(self, id: int) -> TeamSeason | None:
        """
        Deletes a team_season from the data store.

        :param id: The id of the team_season to delete.

        :return: The deleted team_season.
        """
        if not self.team_season_exists(id):
            return None

        team_season = self.get_team_season(id)
        sqla.session.delete(team_season)
        sqla.session.commit()
        return team_season

    def team_season_exists(self, id: int) -> bool:
        """
        Checks to verify whether a specific team_season exists in the data store.

        :param id: The id of the team_season to verify.

        :return: True if the team_season with the specified id exists in the data store; otherwise false.
        """
        return sqla.session.query(exists().where(TeamSeason.id == id)).scalar()

    def team_season_exists_with_team_and_season(self, team_name: str, season_year: int) -> bool:
        """
        Checks to verify whether a specific team_season exists in the data store.

        :param id: The id of the team_season to verify.

        :return: True if the team_season with the specified id exists in the data store; otherwise false.
        """
        return sqla.session.query(
            exists().where(TeamSeason.team_name == team_name and TeamSeason.season_year == season_year)
        ).scalar()
