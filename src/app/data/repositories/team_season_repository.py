from typing import List, Optional

from sqlalchemy.exc import IntegrityError

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

    def get_team_seasons_by_season_year(self, season_year: Optional[int]) -> List[TeamSeason]:
        """
        Gets all the team_seasons in the data store filtered by season_year.

        :param season_year: The season_year to filter.

        :return: A list of all fetched team_seasons.
        """
        if season_year is None:
            return []
        return TeamSeason.query.filter_by(season_year=season_year).all()

    def get_team_season(self, id: int) -> Optional[TeamSeason]:
        """
        Gets the team_season in the data store with the specified id.

        :param id: The id of the team_season to fetch.

        :return: The fetched team_season.
        """
        team_seasons = self.get_team_seasons()
        if len(team_seasons) == 0:
            return None
        return TeamSeason.query.get(id)

    def get_team_season_by_team_name_and_season_year(self, team_name: str, season_year: int) -> TeamSeason:
        return TeamSeason.query.filter_by(team_name=team_name, season_year=season_year).first()

    def update_team_season(self, team_season: TeamSeason) -> None:
        if not self.team_season_exists(team_season.id):
            return team_season

        old_team_season = self.get_team_season(team_season.id)
        old_team_season.team_name = team_season.team_name
        old_team_season.season_year = team_season.season_year
        old_team_season.league_name = team_season.league_name
        old_team_season.conference_name = team_season.conference_name
        old_team_season.division_name = team_season.division_name
        old_team_season.games = team_season.games
        old_team_season.wins = team_season.wins
        old_team_season.losses = team_season.losses
        old_team_season.ties = team_season.ties
        old_team_season.winning_percentage = team_season.winning_percentage
        old_team_season.points_for = team_season.points_for
        old_team_season.points_against = team_season.points_against
        old_team_season.expected_wins = team_season.expected_wins
        old_team_season.expected_losses = team_season.expected_losses
        old_team_season.offensive_average = team_season.offensive_average
        old_team_season.offensive_factor = team_season.offensive_factor
        old_team_season.offensive_index = team_season.offensive_index
        old_team_season.defensive_average = team_season.defensive_average
        old_team_season.defensive_factor = team_season.defensive_factor
        old_team_season.defensive_index = team_season.defensive_index
        old_team_season.final_expected_winning_percentage = team_season.final_expected_winning_percentage

        sqla.session.add(old_team_season)
        try:
            sqla.session.commit()
        except IntegrityError:
            sqla.session.rollback()
            raise

        return team_season

    def team_season_exists(self, id: int) -> bool:
        """
        Checks to verify whether a specific game exists in the data store.

        :param id: The id of the game to verify.

        :return: True if the game with the specified id exists in the data store; otherwise false.
        """
        return self.get_team_season(id) is not None

    def team_season_exists_with_team_name_and_season_year(self, team_name: str, season_year: int) -> bool:
        return self.get_team_season_by_team_name_and_season_year(team_name, season_year) is not None
