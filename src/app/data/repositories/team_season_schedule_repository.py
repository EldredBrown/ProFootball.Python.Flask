from typing import List, Any

from sqlalchemy import Result
from sqlalchemy.sql import text as SQLQuery

from app.data.models.team_season_schedule_averages import TeamSeasonScheduleAverages
from app.data.models.team_season_schedule_profile import TeamSeasonScheduleProfileRecord
from app.data.models.team_season_schedule_totals import TeamSeasonScheduleTotals
from app.data.sqla import sqla


class TeamSeasonScheduleRepository:
    """
    Provides CRUD access to a data store.
    """

    def __init__(self) -> None:
        """
        Initializes a new instance of the TeamSeasonScheduleRepository class.

        :param db_context: In-memory representation of the database.
        """
        pass

    def get_team_season_schedule_profile(self, team_name: str, season_year: int) -> List[TeamSeasonScheduleProfileRecord]:
        """
        Gets the TeamSeasonScheduleTotals in the data store with the specified team_name and season_year.

        :param team_name: The name of the team for which this TeamSeasonScheduleTotals will be fetched.
        :param season_year: The id of the seasons for which this TeamSeasonScheduleTotals will be fetched.

        :return: The fetched TeamSeasonScheduleTotals.
        """
        result = self._call_procedure(f"EXEC sp_GetTeamSeasonScheduleProfile '{team_name}', {season_year};")
        profile = result.all()

        opponent_records = []
        for row in profile:
            opp = TeamSeasonScheduleProfileRecord(
                opponent=row[0],
                game_points_for=row[1],
                game_points_against=row[2],
                opponent_wins=row[3],
                opponent_losses=row[4],
                opponent_ties=row[5],
                opponent_winning_percentage=row[6],
                opponent_weighted_games=row[7],
                opponent_weighted_points_for=row[8],
                opponent_weighted_points_against=row[9]
            )
            opponent_records.append(opp)
        return opponent_records

    def get_team_season_schedule_totals(self, team_name: str, season_year: int) -> TeamSeasonScheduleTotals:
        """
        Gets the TeamSeasonScheduleTotals in the data store with the specified team_name and season_year.

        :param team_name: The name of the team for which this TeamSeasonScheduleTotals will be fetched.
        :param season_year: The id of the seasons for which this TeamSeasonScheduleTotals will be fetched.

        :return: The fetched TeamSeasonScheduleTotals.
        """
        result = self._call_procedure(f"EXEC sp_GetTeamSeasonScheduleTotals '{team_name}', {season_year};")
        totals = result.first()

        if totals is None:
            return TeamSeasonScheduleTotals()

        return TeamSeasonScheduleTotals(
            games=totals[0],
            points_for=totals[1],
            points_against=totals[2],
            schedule_wins=totals[3],
            schedule_losses=totals[4],
            schedule_ties=totals[5],
            schedule_winning_percentage=totals[6],
            schedule_games=totals[7],
            schedule_points_for=totals[8],
            schedule_points_against=totals[9]
        )

    def get_team_season_schedule_averages(self, team_name: str, season_year: int) -> TeamSeasonScheduleAverages:
        """
        Gets the TeamSeasonScheduleAverages in the data store with the specified team_name and season_year.

        :param team_name: The id of the team for which this TeamSeasonScheduleAverages will be fetched.
        :param season_year: The id of the seasons for which this TeamSeasonScheduleAverages will be fetched.

        :return: The fetched TeamSeasonScheduleAverages.
        """
        result = self._call_procedure(f"EXEC sp_GetTeamSeasonScheduleAverages '{team_name}', {season_year};")
        averages = result.first()

        if averages is None:
            return TeamSeasonScheduleAverages()

        return TeamSeasonScheduleAverages(
            points_for=averages[0],
            points_against=averages[1],
            schedule_points_for=averages[2],
            schedule_points_against=averages[3]
        )

    def _call_procedure(self, querystring: str) -> Result[Any]:
        sql = SQLQuery(querystring)
        result = sqla.session.execute(sql)
        return result
