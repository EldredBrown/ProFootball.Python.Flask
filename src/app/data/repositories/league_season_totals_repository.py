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
        statement = f"CALL sp_GetLeagueSeasonTotals('{league_name}', {season_year});"
        totals = sqla.session.execute(statement).first()
        return LeagueSeasonTotals(total_games=totals[0], total_points=totals[1])


if __name__ == '__main__':
    repo = LeagueSeasonTotalsRepository()
    league_season_totals = repo.get_league_season_totals("A", 1)
    print(league_season_totals)
