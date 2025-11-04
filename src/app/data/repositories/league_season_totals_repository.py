from typing import Any

from sqlalchemy import Result
from sqlalchemy.sql import text as SQLQuery

from app.data.models.league_season_totals import LeagueSeasonTotals
from app.data.sqla import sqla


class LeagueSeasonTotalsRepository:
    """
    Provides CRUD access to an external data store.
    """

    def __init__(self) -> None:
        """
        Initializes a new instance of the LeagueSeasonTotalsRepository class.

        :param db_context: In-memory representation of the database.
        """
        pass

    def get_league_season_totals(self, league_name: str, season_year: int) -> LeagueSeasonTotals:
        """
        Gets the league_season_totals in the data store with the specified team_name and season_year.

        :return: The fetched league_season_totals.
        """
        querystring = f"EXEC sp_GetLeagueSeasonTotals '{league_name}', {season_year};"
        result = self._call_procedure(querystring)
        totals = result.first()
        return LeagueSeasonTotals(
            total_games=totals[0], total_points=totals[1], average_points=totals[2], week_count=totals[3]
        )

    def _call_procedure(self, querystring: str) -> Result[Any]:
        sql = SQLQuery(querystring)
        totals = sqla.session.execute(sql)
        return totals
