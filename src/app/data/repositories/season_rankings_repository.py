from typing import List, Optional, Any

from app import CONN_STR
from app.data import sqla
from app.data.models.rankings_team_season \
    import OffensiveRankingsTeamSeason, DefensiveRankingsTeamSeason, TotalRankingsTeamSeason
from app.data.models.team_season import TeamSeason


class SeasonRankingsRepository:
    """
    Provides CRUD access to an external data store.
    """

    def __init__(self) -> None:
        """
        Initializes a new instance of the SeasonRankingsRepository class.
        """
        pass

    def get_offensive_rankings_by_season_year(self, season_year: Optional[int]) -> List[OffensiveRankingsTeamSeason]:
        if season_year is None:
            return []

        result = sqla.callproc(f"EXEC dbo.sp_GetRankingsOffensive {season_year};")

        # Process results if the stored procedure returns data
        rankings_team_seasons = []
        for row in result:
            rts = OffensiveRankingsTeamSeason(
                team_name=row[0],
                wins=row[1],
                losses=row[2],
                ties=row[3],
                offensive_average=row[4],
                offensive_factor=row[5],
                offensive_index=row[6]
            )
            rankings_team_seasons.append(rts)
        return rankings_team_seasons

    def get_defensive_rankings_by_season_year(self, season_year: Optional[int]) -> List[DefensiveRankingsTeamSeason]:
        if season_year is None:
            return []

        result = sqla.callproc(f"EXEC dbo.sp_GetRankingsDefensive {season_year};")

        # Process results if the stored procedure returns data
        rankings_team_seasons = []
        for row in result:
            rts = DefensiveRankingsTeamSeason(
                team_name=row[0],
                wins=row[1],
                losses=row[2],
                ties=row[3],
                defensive_average=row[4],
                defensive_factor=row[5],
                defensive_index=row[6]
            )
            rankings_team_seasons.append(rts)
        return rankings_team_seasons

    def get_total_rankings_by_season_year(self, season_year: Optional[int]) -> List[TotalRankingsTeamSeason]:
        if season_year is None:
            return []
        result = sqla.callproc(f"EXEC dbo.sp_GetRankingsTotal {season_year};")

        # Process results if the stored procedure returns data
        rankings_team_seasons = []
        for row in result:
            rts = TotalRankingsTeamSeason(
                team_name=row[0],
                wins=row[1],
                losses=row[2],
                ties=row[3],
                offensive_average=row[4],
                offensive_factor=row[5],
                offensive_index=row[6],
                defensive_average=row[7],
                defensive_factor=row[8],
                defensive_index=row[9],
                final_expected_winning_percentage=row[10]
            )
            rankings_team_seasons.append(rts)
        return rankings_team_seasons

    def get_data_for_rankings_update(self, team_season: TeamSeason) -> dict:
        # This method calls a stored procedure that returns multiple datasets; therefore, it can access the database
        # only via lower-level methods than those provided for other data access methods in the repository layer.
        from sqlalchemy import create_engine

        engine = create_engine(f"mssql+pyodbc:///?odbc_connect={CONN_STR}", future=True)

        results = dict()
        result_keys = ('team_season_schedule_totals', 'team_season_schedule_averages', 'league_season')

        with engine.raw_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "EXEC dbo.sp_GetDataForRankingsUpdate ?, ?, ?",
                (team_season.team_name, team_season.league_name, team_season.season_year)
            )

            try:
                for i in range(3):
                    row = cursor.fetchone()
                    if row:
                        # Convert to list of dicts with column names
                        columns = [col[0] for col in cursor.description]
                        result = dict(zip(columns, row))
                        results[result_keys[i]] = result

                    cursor.nextset()

                cursor.close()
            except Exception as e:
                print(f"Error calling stored procedure: {e}")
                raise

        return results
