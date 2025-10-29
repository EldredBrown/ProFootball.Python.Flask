from typing import List

from sqlalchemy.sql import text as SQLQuery

from app.data.models.rankings_team_season \
    import OffensiveRankingsTeamSeason, DefensiveRankingsTeamSeason, TotalRankingsTeamSeason
from app.data.sqla import sqla


class SeasonRankingsRepository:
    """
    Provides CRUD access to an external data store.
    """

    def __init__(self) -> None:
        """
        Initializes a new instance of the SeasonRankingsRepository class.
        """
        pass

    def get_offensive_rankings_by_season_year(self, season_year: int | None) -> List[OffensiveRankingsTeamSeason]:
        if season_year is None:
            return []

        querystring = f"EXEC dbo.sp_GetRankingsOffensive {season_year}"
        sql = SQLQuery(querystring)
        result = sqla.session.execute(sql)

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

    def get_defensive_rankings_by_season_year(self, season_year: int | None) -> List[DefensiveRankingsTeamSeason]:
        if season_year is None:
            return []

        querystring = f"EXEC dbo.sp_GetRankingsDefensive {season_year}"
        sql = SQLQuery(querystring)
        result = sqla.session.execute(sql)

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

    def get_total_rankings_by_season_year(self, season_year: int | None) -> List[TotalRankingsTeamSeason]:
        if season_year is None:
            return []

        querystring = f"EXEC dbo.sp_GetRankingsTotal {season_year}"
        sql = SQLQuery(querystring)
        result = sqla.session.execute(sql)

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
