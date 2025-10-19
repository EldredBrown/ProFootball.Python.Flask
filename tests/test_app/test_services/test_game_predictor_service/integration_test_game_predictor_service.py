import unittest

from decimal import Decimal

from app.data.entities.team_season import TeamSeason
from app.services.game_predictor_service.game_predictor_service import GamePredictorService
from test_app.test_services.database_setup import clear_database, set_up_seasons_table, set_up_leagues_table, \
    set_up_conferences_table, set_up_divisions_table, set_up_teams_table, set_up_league_seasons_table, \
    set_up_team_seasons_table, engine

SEASON_YEAR = 2022
LEAGUE_NAME = "NFL"
GUEST_NAME = "Cincinnati Bengals"
GUEST_CONFERENCE_NAME = "AFC"
GUEST_DIVISION_NAME = "AFC North"
HOST_NAME = "Los Angeles Rams"
HOST_CONFERENCE_NAME = "NFC"
HOST_DIVISION_NAME = "NFC West"


class IntegrationTestGamePredictorService(unittest.TestCase):

    def setUp(self) -> None:
        clear_database()

        set_up_seasons_table()
        set_up_leagues_table()
        set_up_conferences_table()
        set_up_divisions_table()
        set_up_teams_table()
        set_up_league_seasons_table()

    def test_predict_game_score_should_return_none_when_guest_season_is_none(self):
        # Arrange
        test_service = GamePredictorService()

        # Act
        predicted_guest_score, predicted_host_score \
            = test_service.predict_game_score(GUEST_NAME, SEASON_YEAR, HOST_NAME, SEASON_YEAR)

        # Assert
        assert predicted_guest_score is None
        assert predicted_host_score is None

    def test_predict_game_score_should_return_none_when_host_season_is_none(self):
        # Arrange
        test_service = GamePredictorService()

        guest_season = TeamSeason(
            GUEST_NAME,
            SEASON_YEAR,
            LEAGUE_NAME,
            conference_name=GUEST_CONFERENCE_NAME,
            division_name=GUEST_DIVISION_NAME
        )
        set_up_team_seasons_table((guest_season,))

        # Act
        predicted_guest_score, predicted_host_score \
            = test_service.predict_game_score(GUEST_NAME, SEASON_YEAR, HOST_NAME, SEASON_YEAR)

        # Assert
        assert predicted_guest_score is None
        assert predicted_host_score is None

    def test_predict_game_score_should_return_correctly_calculated_prediction_when_guest_season_and_host_season_are_not_none(self):
        # Arrange
        test_service = GamePredictorService()

        guest_season = TeamSeason(
            GUEST_NAME,
            SEASON_YEAR,
            LEAGUE_NAME,
            conference_name=GUEST_CONFERENCE_NAME,
            division_name=GUEST_DIVISION_NAME,
        )
        guest_season.offensive_average = Decimal('1')
        guest_season.offensive_factor = Decimal('2')
        guest_season.defensive_average = Decimal('3')
        guest_season.defensive_factor = Decimal('4')

        host_season = TeamSeason(
            HOST_NAME,
            SEASON_YEAR,
            LEAGUE_NAME,
            conference_name=HOST_CONFERENCE_NAME,
            division_name=HOST_DIVISION_NAME
        )
        host_season.offensive_average = Decimal('5')
        host_season.offensive_factor = Decimal('6')
        host_season.defensive_average = Decimal('7')
        host_season.defensive_factor = Decimal('8')

        with engine.connect() as connection:
            transaction = connection.begin()
            try:
                for team_season in (guest_season, host_season):
                    statement = f"""
                    INSERT INTO pro_football.team_seasons(
                        team_name,
                        season_year,
                        league_name,
                        conference_name,
                        division_name,
                        offensive_average,
                        offensive_factor,
                        defensive_average,
                        defensive_factor
                    )
                    VALUES(
                        '{team_season.team_name}',
                        {team_season.season_year},
                        '{team_season.league_name}',
                        '{team_season.conference_name}',
                        '{team_season.division_name}',
                        {team_season.offensive_average},
                        {team_season.offensive_factor},
                        {team_season.defensive_average},
                        {team_season.defensive_factor}
                    );
                    """
                    connection.execute(statement)
    
                transaction.commit()
            except:
                transaction.rollback()
                raise

        # Act
        predicted_guest_score, predicted_host_score \
            = test_service.predict_game_score(GUEST_NAME, SEASON_YEAR, HOST_NAME, SEASON_YEAR)

        # Assert
        assert predicted_guest_score == round(
            ((guest_season.offensive_factor * host_season.defensive_average
              + host_season.defensive_factor * guest_season.offensive_average) / 2), 1
        )
        assert predicted_host_score == round(
            ((host_season.offensive_factor * guest_season.defensive_average
              + guest_season.defensive_factor * host_season.offensive_average) / 2), 1
        )
