from flask_injector import FlaskInjector, request
from injector import singleton

from app import create_app
from app.data.repositories.conference_repository import ConferenceRepository
from app.data.repositories.division_repository import DivisionRepository
from app.data.repositories.game_repository import GameRepository
from app.data.repositories.league_repository import LeagueRepository
from app.data.repositories.league_season_repository import LeagueSeasonRepository
from app.data.repositories.league_season_totals_repository import LeagueSeasonTotalsRepository
from app.data.repositories.season_rankings_repository import SeasonRankingsRepository
from app.data.repositories.season_repository import SeasonRepository
from app.data.repositories.season_standings_repository import SeasonStandingsRepository
from app.data.repositories.team_repository import TeamRepository
from app.data.repositories.team_season_repository import TeamSeasonRepository
from app.data.repositories.team_season_schedule_repository import TeamSeasonScheduleRepository
from app.services.game_predictor_service.game_predictor_service import GamePredictorService
from app.services.game_service.game_service import GameService
from app.services.game_service.process_game_strategy.process_game_strategy_factory import ProcessGameStrategyFactory
from app.services.weekly_update_service.weekly_update_service import WeeklyUpdateService

app = create_app()

def configure(binder):
    binder.bind(SeasonRepository, to=SeasonRepository, scope=singleton)
    binder.bind(LeagueRepository, to=LeagueRepository, scope=singleton)
    binder.bind(ConferenceRepository, to=ConferenceRepository, scope=singleton)
    binder.bind(DivisionRepository, to=DivisionRepository, scope=singleton)
    binder.bind(TeamRepository, to=TeamRepository, scope=singleton)
    binder.bind(GameRepository, to=GameRepository, scope=singleton)
    binder.bind(LeagueSeasonRepository, to=LeagueSeasonRepository, scope=singleton)
    binder.bind(TeamSeasonRepository, to=TeamSeasonRepository, scope=singleton)
    binder.bind(TeamSeasonScheduleRepository, to=TeamSeasonScheduleRepository, scope=singleton)
    binder.bind(SeasonStandingsRepository, to=SeasonStandingsRepository, scope=singleton)
    binder.bind(SeasonRankingsRepository, to=SeasonRankingsRepository, scope=singleton)
    binder.bind(LeagueSeasonTotalsRepository, to=LeagueSeasonTotalsRepository, scope=singleton)
    binder.bind(GameService, to=GameService, scope=request)
    binder.bind(WeeklyUpdateService, to=WeeklyUpdateService, scope=request)
    binder.bind(GamePredictorService, to=GamePredictorService, scope=request)
    binder.bind(ProcessGameStrategyFactory, to=ProcessGameStrategyFactory, scope=request)

FlaskInjector(app=app, modules=[configure])


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
