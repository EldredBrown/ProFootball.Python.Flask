from typing import List, Optional

from sqlalchemy.orm import joinedload

from app.data.models.team_season import TeamSeason
from app.data.sqla import sqla, try_commit


class TeamSeasonRepository:
    """
    Provides CRUD access to an external data store.
    """

    def get_team_seasons(self) -> List[TeamSeason]:
        """
        Gets all the team_seasons in the data store.

        :return: A list of all fetched team_seasons.
        """
        team_seasons = self._get_team_seasons_with_navigation_properties()
        return team_seasons.all()

    def get_team_seasons_by_team(self, team_id: Optional[int]) -> List[TeamSeason]:
        """
        Gets all the team_seasons in the data store filtered by season_year.

        :param season_id: The season_year to filter.

        :return: A list of all fetched team_seasons.
        """
        team_seasons = self._get_team_seasons_with_navigation_properties()
        if team_id is None:
            return []
        return team_seasons.filter_by(team_id=team_id).all()

    def get_team_seasons_by_season(self, season_id: Optional[int]) -> List[TeamSeason]:
        """
        Gets all the team_seasons in the data store filtered by season_year.

        :param season_id: The season_year to filter.

        :return: A list of all fetched team_seasons.
        """
        team_seasons = self._get_team_seasons_with_navigation_properties()
        if season_id is None:
            return []
        return team_seasons.filter_by(season_id=season_id).all()

    def get_team_season(self, id: int) -> Optional[TeamSeason]:
        """
        Gets the team_season in the data store with the specified id.

        :param id: The id of the team_season to fetch.

        :return: The fetched team_season.
        """
        team_seasons = self._get_team_seasons_with_navigation_properties()
        if len(team_seasons.all()) == 0:
            return None
        return team_seasons.get(id)

    def get_team_season_by_team_and_season(self, team_id: int, season_id: int) -> Optional[TeamSeason]:
        team_seasons = self._get_team_seasons_with_navigation_properties()
        if len(team_seasons.all()) == 0:
            return None
        return team_seasons.filter_by(team_id=team_id, season_id=season_id).first()

    def add_team_season(self, team_season: TeamSeason) -> TeamSeason:
        """
        Adds a TeamSeason to the data store.

        :param **kwargs: A keyword args dictionary containing values for the TeamSeason to add.

        :return: The added TeamSeason.
        """
        sqla.session.add(team_season)
        try_commit()
        return team_season

    def add_team_seasons(self, team_seasons: tuple) -> tuple:
        """
        Adds a collection of TeamSeason dictionaries to the data store.

        :param division_args: The tuple of division keyword args dictionaries to add.

        :return: The added divisions.
        """
        for team_season in team_seasons:
            sqla.session.add(team_season)
        try_commit()
        return team_seasons

    def update_team_season(self, team_season: TeamSeason) -> Optional[TeamSeason]:
        if team_season is None:
            return team_season

        if not self.team_season_exists(team_season.id):
            return team_season
        team_season_in_db = self._set_values_of_team_season_in_db(team_season)
        sqla.session.add(team_season_in_db)
        try_commit()
        return team_season

    def delete_team_season(self, id: int) -> Optional[TeamSeason]:
        """
        Deletes a division from the data store.

        :param id: The id of the division to delete.

        :return: The deleted division.
        """
        if not self.team_season_exists(id):
            return None
        team_season = self.get_team_season(id)
        sqla.session.delete(team_season)
        try_commit()
        return team_season

    def team_season_exists(self, id: int) -> bool:
        """
        Checks to verify whether a specific game exists in the data store.

        :param id: The id of the game to verify.

        :return: True if the game with the specified id exists in the data store; otherwise false.
        """
        return self.get_team_season(id) is not None

    def team_season_exists_with_team_id_and_season_id(self, team_id: int, season_id: int) -> bool:
        return self.get_team_season_by_team_and_season(team_id, season_id) is not None

    def _get_team_seasons_with_navigation_properties(self):
        return TeamSeason.query.options(
            joinedload(TeamSeason.team),
            joinedload(TeamSeason.season),
            joinedload(TeamSeason.league),
            joinedload(TeamSeason.conference),
            joinedload(TeamSeason.division),
        )

    def _set_values_of_team_season_in_db(self, team_season: TeamSeason) -> TeamSeason | None:
        team_season_in_db = self.get_team_season(team_season.id)
        team_season_in_db.team_id = team_season.team_id
        team_season_in_db.season_id = team_season.season_id
        team_season_in_db.league_id = team_season.league_id
        team_season_in_db.conference_id = team_season.conference_id
        team_season_in_db.division_id = team_season.division_id
        team_season_in_db.games = team_season.games
        team_season_in_db.wins = team_season.wins
        team_season_in_db.losses = team_season.losses
        team_season_in_db.ties = team_season.ties
        team_season_in_db.points_for = team_season.points_for
        team_season_in_db.points_against = team_season.points_against
        team_season_in_db.expected_wins = team_season.expected_wins
        team_season_in_db.expected_losses = team_season.expected_losses
        team_season_in_db.offensive_average = team_season.offensive_average
        team_season_in_db.offensive_factor = team_season.offensive_factor
        team_season_in_db.offensive_index = team_season.offensive_index
        team_season_in_db.defensive_average = team_season.defensive_average
        team_season_in_db.defensive_factor = team_season.defensive_factor
        team_season_in_db.defensive_index = team_season.defensive_index
        team_season_in_db.final_expected_winning_percentage = team_season.final_expected_winning_percentage
        return team_season_in_db
