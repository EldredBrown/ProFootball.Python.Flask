from flask import Flask
from flask_migrate import Migrate

from app.data.sqla import sqla


def create_app():
    app = Flask(__name__)

    conn_str = (
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=(localdb)\\MSSQLLocalDB;'
        'DATABASE=ProFootballDb;'
    )

    app.config.from_mapping(
        SECRET_KEY='secretkey',
        # SQLALCHEMY_DATABASE_URI='mysql+mysqlconnector://root:root@localhost:3306/app',
        # SQLALCHEMY_DATABASE_URI='mssql+pyodbc://<username>:<password>@<server>:<port>/<database>?driver=ODBC+Driver+17+for+SQL+Server',
        # SQLALCHEMY_DATABASE_URI='mssql+pyodbc://<server>:<port>/<database>?driver=ODBC+Driver+17+for+SQL+Server?trusted_connection=yes',
        SQLALCHEMY_DATABASE_URI=f"mssql+pyodbc:///?odbc_connect={conn_str}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        DEBUG=True
    )

    sqla.init_app(app)

    # Flask-Migrate
    Migrate(app, sqla, render_as_batch=True)

    from app.flask import (home_controller, season_controller, league_controller, conference_controller,
                           division_controller, team_controller, game_controller, team_season_controller,
                           season_standings_controller, season_rankings_controller, game_predictor_controller)

    app.register_blueprint(home_controller.blueprint, url_prefix='/')
    app.register_blueprint(season_controller.blueprint, url_prefix='/seasons')
    app.register_blueprint(league_controller.blueprint, url_prefix='/leagues')
    app.register_blueprint(conference_controller.blueprint, url_prefix='/conferences')
    app.register_blueprint(division_controller.blueprint, url_prefix='/divisions')
    app.register_blueprint(team_controller.blueprint, url_prefix='/teams')
    app.register_blueprint(game_controller.blueprint, url_prefix='/games')
    app.register_blueprint(team_season_controller.blueprint, url_prefix='/team_seasons')
    app.register_blueprint(season_standings_controller.blueprint, url_prefix='/season_standings')
    app.register_blueprint(season_rankings_controller.blueprint, url_prefix='/season_rankings')
    app.register_blueprint(game_predictor_controller.blueprint, url_prefix='/game_predictor')

    app.add_url_rule('/', endpoint='index')

    return app
