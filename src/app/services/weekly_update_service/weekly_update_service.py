from dataclasses import dataclass

from injector import inject

from app.data.models.league_season import LeagueSeason
from app.data.models.league_season_totals import LeagueSeasonTotals
from app.data.models.team_season import TeamSeason
from app.data.repositories.game_repository import GameRepository
from app.data.repositories.league_season_repository import LeagueSeasonRepository
from app.data.repositories.league_season_totals_repository import LeagueSeasonTotalsRepository
from app.data.repositories.season_rankings_repository import SeasonRankingsRepository
from app.data.repositories.season_repository import SeasonRepository
from app.data.repositories.team_season_repository import TeamSeasonRepository
from app.services.utilities.utils import typename
from app.services.utilities import guard


MIN_WEEKS_FOR_RANKINGS = 3


@dataclass
class LeagueSeasonData:
    league_season_totals: LeagueSeasonTotals
    league_season: LeagueSeason


@dataclass
class RankingsData:
    averages: dict
    league_season: dict


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
            season_rankings_repository: SeasonRankingsRepository
    ):
        """
        Initializes a new instance of the WeeklyUpdateService class.
        """
        self.season_repository = season_repository
        self.game_repository = game_repository
        self.league_season_repository = league_season_repository
        self.team_season_repository = team_season_repository
        self.league_season_totals_repository = league_season_totals_repository
        self.season_rankings_repository = season_rankings_repository

    def __repr__(self):
        return (
            f"{typename(self)}("
            f"season_repository={self.season_repository}, "
            f"game_repository={self.game_repository}, "
            f"league_season_repository={self.league_season_repository}, "
            f"team_season_repository={self.team_season_repository}, "
            f"league_season_totals_repository={self.league_season_totals_repository}, "
            f"season_rankings_repository={self.season_rankings_repository}"
            f")"
        )

    def __str__(self):
        return f"Season Repository: {self.season_repository}, " \
               f"Game Repository: {self.game_repository}, " \
               f"League Season Repository: {self.league_season_repository}, " \
               f"Team Season Repository: {self.team_season_repository}, " \
               f"League Season Totals Repository: {self.league_season_totals_repository}, " \
               f"Season Rankings Repository: {self.season_rankings_repository}"

    def run_weekly_update(self, league_id: int, season_id: int) -> None:
        """
        Runs a weekly update of the rankings in the data store.

        :param league_id: The league_id of the league_season within which a weekly update will be run.
        :param season_id: The season_id of the league_season within which a weekly update will be run.

        :return: None
        """
        guard.raise_if_none(league_id, 'league_id')
        if season_id <= 0:
            raise ValueError(f"season_id must be a positive integer; got {season_id}")

        self._update_league_season(league_id, season_id)
        src_week_count = self._update_week_count(season_id)

        if src_week_count >= MIN_WEEKS_FOR_RANKINGS:
            self._update_rankings(season_id)

    def _update_league_season(self, league_id: int, season_id: int) -> None:
        data = self._get_league_season_data(league_id, season_id)
        if not data:
            return

        league_season_totals = data.league_season_totals
        league_season = data.league_season
        league_season.update_games_and_points(league_season_totals.total_games, league_season_totals.total_points)
        self.league_season_repository.update_league_season(league_season)

    def _get_league_season_data(self, league_id: int, season_id: int) -> LeagueSeasonData | None:
        league_season_totals = self.league_season_totals_repository.get_league_season_totals(league_id, season_id)
        if (
                league_season_totals is None
                or league_season_totals.total_games is None
                or league_season_totals.total_points is None
        ):
            return None

        league_season = (
            self.league_season_repository.get_league_season_by_league_and_season(league_id, season_id)
        )
        if league_season is None:
            return None

        return LeagueSeasonData(league_season_totals=league_season_totals, league_season=league_season)

    def _update_week_count(self, season_id: int) -> int:
        src_week_count = self.game_repository.get_max_week_by_season(season_id)
        if src_week_count is None:
            return 0

        dest_season = self.season_repository.get_season(season_id)
        if dest_season is None:
            # TODO - 2026-04-21: Log a warning here — rankings will still run, but season won't be updated
            return src_week_count

        dest_season.num_of_weeks_completed = src_week_count
        self.season_repository.update_season(dest_season)
        return src_week_count

    def _update_rankings(self, season_id: int) -> None:
        team_seasons = self.team_season_repository.get_team_seasons_by_season(season_id)
        if not team_seasons:
            return

        for team_season in team_seasons:
            self._update_rankings_for_team_season(team_season)

    def _update_rankings_for_team_season(self, team_season: TeamSeason) -> None:
        data = self._get_rankings_data(team_season)
        if data is None:
            return

        team_season.update_rankings(data.averages['avg_points_for'],
                                    data.averages['avg_points_against'],
                                    data.league_season['average_points'])
        self.team_season_repository.update_team_season(team_season)

    def _get_rankings_data(self, team_season: TeamSeason) -> RankingsData | None:
        results = self.season_rankings_repository.get_data_for_rankings_update(team_season)

        totals = results['team_season_schedule_totals']
        if not totals or totals['schedule_games'] is None:
            return None

        averages = results['team_season_schedule_averages']
        if not averages or averages['avg_points_for'] is None or averages['avg_points_against'] is None:
            return None

        league_season = results['league_season']
        if not league_season or league_season['average_points'] is None:
            return None

        return RankingsData(averages=averages, league_season=league_season)
