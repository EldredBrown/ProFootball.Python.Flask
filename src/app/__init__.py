from flask import Flask
from flask_migrate import Migrate
from injector import Injector, singleton

from app.data.sqla import sqla

CONN_STR = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=(localdb)\\MSSQLLocalDB;'
    'DATABASE=ProFootballDb;'
)


def create_app():
    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY='secretkey',
        # SQLALCHEMY_DATABASE_URI='mysql+mysqlconnector://root:root@localhost:3306/app',
        # SQLALCHEMY_DATABASE_URI='mssql+pyodbc://<username>:<password>@<server>:<port>/<database>?driver=ODBC+Driver+17+for+SQL+Server',
        # SQLALCHEMY_DATABASE_URI='mssql+pyodbc://<server>:<port>/<database>?driver=ODBC+Driver+17+for+SQL+Server?trusted_connection=yes',
        SQLALCHEMY_DATABASE_URI=f"mssql+pyodbc:///?odbc_connect={CONN_STR}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        DEBUG=True
    )

    sqla.init_app(app)

    # Flask-Migrate
    Migrate(app, sqla, render_as_batch=True)

    from app.flask import (home_controller, season_controller, association_controller, team_controller, game_controller,
                           league_season_controller, team_season_admin_controller, team_season_controller,
                           season_standings_controller, season_rankings_controller, game_predictor_controller)

    app.register_blueprint(home_controller.blueprint, url_prefix='/')
    app.register_blueprint(season_controller.blueprint, url_prefix='/seasons')
    app.register_blueprint(association_controller.blueprint, url_prefix='/associations')
    app.register_blueprint(team_controller.blueprint, url_prefix='/teams')
    app.register_blueprint(game_controller.blueprint, url_prefix='/games')
    app.register_blueprint(league_season_controller.blueprint, url_prefix='/league_seasons')
    app.register_blueprint(team_season_admin_controller.blueprint, url_prefix='/team_seasons_admin')
    app.register_blueprint(team_season_controller.blueprint, url_prefix='/team_seasons')
    app.register_blueprint(season_standings_controller.blueprint, url_prefix='/season_standings')
    app.register_blueprint(season_rankings_controller.blueprint, url_prefix='/season_rankings')
    app.register_blueprint(game_predictor_controller.blueprint, url_prefix='/game_predictor')

    app.add_url_rule('/', endpoint='index')

    return app


def configure(binder):
    from app.data.repositories.association_repository import AssociationRepository
    from app.data.repositories.game_repository import GameRepository
    from app.data.repositories.league_season_repository import LeagueSeasonRepository
    from app.data.repositories.season_repository import SeasonRepository
    from app.data.repositories.team_repository import TeamRepository
    from app.data.repositories.team_season_repository import TeamSeasonRepository

    from app.services.game_predictor_service.game_predictor_service import GamePredictorService
    from app.services.game_service.game_service import GameService
    from app.services.game_service.process_game_strategy.process_game_strategy_factory import ProcessGameStrategyFactory
    from app.services.weekly_update_service.weekly_update_service import WeeklyUpdateService

    binder.bind(AssociationRepository, to=AssociationRepository, scope=singleton)
    binder.bind(GameRepository, to=GameRepository, scope=singleton)
    binder.bind(LeagueSeasonRepository, to=LeagueSeasonRepository, scope=singleton)
    binder.bind(SeasonRepository, to=SeasonRepository, scope=singleton)
    binder.bind(TeamRepository, to=TeamRepository, scope=singleton)
    binder.bind(TeamSeasonRepository, to=TeamSeasonRepository, scope=singleton)

    binder.bind(GameService, to=GameService, scope=singleton)
    binder.bind(GamePredictorService, to=GamePredictorService, scope=singleton)
    binder.bind(WeeklyUpdateService, to=WeeklyUpdateService, scope=singleton)

    binder.bind(ProcessGameStrategyFactory, to=ProcessGameStrategyFactory, scope=singleton)


injector = Injector([configure])
