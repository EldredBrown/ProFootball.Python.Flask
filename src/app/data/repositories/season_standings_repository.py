from typing import List, Optional

from app.data.models.standings_team_season import StandingsTeamSeason
from app.data import sqla


def get_season_standings(season_year: Optional[int], league_id: Optional[int], group_by_division: bool=False) \
        -> List[StandingsTeamSeason]:
    if season_year is None or league_id is None:
        return []

    querystring = f"EXEC sp_GetSeasonStandings @season_year = {season_year}, @league_id = {league_id}"
    result = sqla.callproc(querystring)

    # Process results if the stored procedure returns data
    standings_team_seasons = []
    for row in result:
        sts = StandingsTeamSeason(
            team_name=row[0],
            wins=row[1],
            losses=row[2],
            ties=row[3],
            winning_percentage=row[4],
            points_for=row[5],
            points_against=row[6],
            avg_points_for=row[7],
            avg_points_against=row[8],
            expected_wins=row[9],
            expected_losses=row[10]
        )
        standings_team_seasons.append(sts)
    return standings_team_seasons
