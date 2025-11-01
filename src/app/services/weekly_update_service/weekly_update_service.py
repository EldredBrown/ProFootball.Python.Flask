from injector import inject

from app.data.models.team_season import TeamSeason
from app.data.repositories.game_repository import GameRepository
from app.data.repositories.league_season_repository import LeagueSeasonRepository
from app.data.repositories.league_season_totals_repository import LeagueSeasonTotalsRepository
from app.data.repositories.season_repository import SeasonRepository
from app.data.repositories.team_season_repository import TeamSeasonRepository
from app.data.repositories.team_season_schedule_repository import TeamSeasonScheduleRepository
from app.services.utilities.utils import typename
from app.services.utilities import guard


class WeeklyUpdateService:
    """
    A service to run a weekly update of the pro football data store.
    """

    @inject
    def __init__(
            self,
            season_repository: SeasonRepository,
            game_repository: GameRepository,
            league_season_repository: LeagueSeasonRepository,
            team_season_repository: TeamSeasonRepository,
            league_season_totals_repository: LeagueSeasonTotalsRepository,
            team_season_schedule_repository: TeamSeasonScheduleRepository
    ):
        """
        Initializes a new instance of the WeeklyUpdateService class.

        :param season_repository: The repository by which Season data will be accessed.
        :param game_repository: The repository by which Game data will be accessed.
        :param league_season_repository: The repository by which LeagueSeason data will be accessed.

        :param league_season_totals_repository:
        The repository by which LeagueSeasonTotals data will be accessed.

        :param team_season_repository: The repository by which TeamSeason data will be accessed.
        :param team_season_schedule_repository: The repository by which TeamSeasonSchedule data will be accessed.
        """
        self._season_repository = season_repository
        self._game_repository = game_repository
        self._league_season_repository = league_season_repository
        self._team_season_repository = team_season_repository
        self._league_season_totals_repository = league_season_totals_repository
        self._team_season_schedule_repository = team_season_schedule_repository

    def __repr__(self):
        return f"{typename(self)}(" \
               f"season_repository={self._season_repository}," \
               f"game_repository={self._game_repository}," \
               f"league_season_repository={self._league_season_repository}," \
               f"league_season_totals_repository={self._league_season_totals_repository}," \
               f"team_season_repository={self._team_season_repository}," \
               f"team_season_schedule_repository={self._team_season_schedule_repository})"

    def __str__(self):
        return format(self)

    def __format__(self, format_spec):
        return f"Season Repository: {self._season_repository}," \
               f"Game Repository: {self._game_repository}," \
               f"League Season Repository: {self._league_season_repository}," \
               f"Team Season Repository: {self._team_season_repository}," \
               f"League Season Totals Repository: {self._league_season_totals_repository}," \
               f"Team Season Schedule Repository: {self._team_season_schedule_repository})"

    def run_weekly_update(self, league_name: str, season_year: int) -> None:
        """
        Runs a weekly update of the data store.

        :param league_name: The league_name of the league_season within which a weekly update will be run.
        :param season_year: The season_year of the league_season within which a weekly update will be run.

        :return: None
        """
        guard.raise_if_none(league_name, 'league_name')
        guard.raise_if_none(season_year, 'season_year')

        self._update_league_season(league_name, season_year)
        src_week_count = self._update_week_count(season_year)

        if src_week_count >= 3:
            self._update_rankings(season_year)

    def _update_league_season(self, league_name: str, season_year: int) -> None:
        league_season_totals = self._league_season_totals_repository.get_league_season_totals(league_name, season_year)
        if (
                league_season_totals is None
                or league_season_totals.total_games is None
                or league_season_totals.total_points is None
        ):
            return

        league_season = (
            self._league_season_repository.get_league_season_by_league_name_and_season_year(league_name, season_year)
        )
        if league_season is None:
            return

        league_season.update_games_and_points(league_season_totals.total_games, league_season_totals.total_points)
        self._league_season_repository.update_league_season(league_season)

    def _update_week_count(self, season_year: int) -> int:
        try:
            src_week_count = max(
                [game.week for game in self._game_repository.get_games() if game.season_year == season_year]
            )
        except TypeError:
            return 0
        except ValueError:
            return 0

        dest_season = self._season_repository.get_season_by_year(season_year)
        if dest_season is not None:
            dest_season.num_of_weeks_completed = src_week_count

        self._season_repository.update_season(dest_season)
        return src_week_count

    def _update_rankings(self, season_year: int) -> None:
        team_seasons = self._team_season_repository.get_team_seasons_by_season_year(season_year)
        if team_seasons is None:
            return

        for team_season in team_seasons:
            self._update_rankings_for_team_season(team_season)

    def _update_rankings_for_team_season(self, team_season: TeamSeason) -> None:
        team_season_schedule_totals = self._team_season_schedule_repository.get_team_season_schedule_totals(
            team_season.team_name, team_season.season_year
        )
        if (team_season_schedule_totals is None) or (team_season_schedule_totals.schedule_games is None):
            return

        team_season_schedule_averages = \
            self._team_season_schedule_repository.get_team_season_schedule_averages(
                team_season.team_name, team_season.season_year
            )
        if (
                team_season_schedule_averages is None
                or team_season_schedule_averages.points_for is None
                or team_season_schedule_averages.points_against is None
        ):
            return

        league_season = self._league_season_repository.get_league_season_by_league_name_and_season_year(
            team_season.league_name, team_season.season_year
        )
        if (league_season is None) or (league_season.average_points is None):
            return

        team_season.update_rankings(team_season_schedule_averages.points_for,
                                    team_season_schedule_averages.points_against,
                                    league_season.average_points)
        self._team_season_repository.update_team_season(team_season)
