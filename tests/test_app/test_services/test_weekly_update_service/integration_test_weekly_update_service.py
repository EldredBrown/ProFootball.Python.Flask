import unittest
from decimal import Decimal

from app.data.entities.game import Game
from app.services.game_service.game_service import GameService
from app.services.weekly_update_service.weekly_update_service import WeeklyUpdateService

from test_app.test_services.database_setup import \
    LEAGUE_NAME, SEASON_YEAR, TEAM_SEASONS, clear_database, engine, get_default_games, set_up_conferences_table, \
    set_up_divisions_table, set_up_games_table, set_up_league_seasons_table, set_up_leagues_table, \
    set_up_seasons_table, set_up_team_season_record, set_up_team_seasons_table, set_up_teams_table


class TestWeeklyUpdateService(unittest.TestCase):

    def setUp(self) -> None:
        clear_database()

        self._test_service = WeeklyUpdateService()

    def tearDown(self) -> None:
        clear_database()

    def test_run_weekly_update_should_not_update_anything_when_get_league_season_totals_returns_empty_object_and_game_table_is_empty(self):
        # Arrange
        statement = f"""
            INSERT INTO pro_football.seasons(year, num_of_weeks_completed)
            VALUES({SEASON_YEAR}, 0);
        """
        set_up_seasons_table(statement)
        set_up_leagues_table()
        set_up_conferences_table()
        set_up_divisions_table()
        set_up_teams_table()

        statement = f"""
            INSERT INTO pro_football.league_seasons(league_name, season_year, total_games, total_points)
            VALUES('{LEAGUE_NAME}', {SEASON_YEAR}, 0, 0);
        """
        set_up_league_seasons_table(statement)

        # Act
        self._test_service.run_weekly_update(LEAGUE_NAME, SEASON_YEAR)

        # Assert
        with engine.connect() as connection:
            statement = f"""
                SELECT *
                FROM pro_football.league_seasons
                WHERE
                    league_name = '{LEAGUE_NAME}'
                    AND season_year = {SEASON_YEAR}
            """
            lsa = connection.execute(statement).first()

            lsa_total_games = lsa[3]
            assert lsa_total_games == 0

            lsa_total_points = lsa[4]
            assert lsa_total_points == 0

            lsa_average_points = lsa[5]
            assert lsa_average_points is None

            statement = f"""
                SELECT *
                FROM pro_football.seasons
                WHERE
                    year = {SEASON_YEAR}
            """
            season = connection.execute(statement).first()
            season_num_of_weeks_completed = season[3]
            assert season_num_of_weeks_completed == 0

            statement = f"""
                SELECT *
                FROM pro_football.team_seasons
            """
            tsa_list = connection.execute(statement).all()
            assert len(tsa_list) == 0

    def test_run_weekly_update_should_not_update_anything_when_league_season_table_has_no_record_for_specified_league_and_season_and_game_table_is_empty(self):
        # Arrange
        statement = f"""
            INSERT INTO pro_football.seasons(year, num_of_weeks_completed)
            VALUES({SEASON_YEAR}, 0);
        """
        set_up_seasons_table(statement)
        set_up_leagues_table()
        set_up_conferences_table()
        set_up_divisions_table()
        set_up_teams_table()
        set_up_team_seasons_table()

        # Act
        self._test_service.run_weekly_update(LEAGUE_NAME, SEASON_YEAR)

        # Assert
        with engine.connect() as connection:
            statement = f"""
                SELECT *
                FROM pro_football.league_seasons
                WHERE
                    league_name = '{LEAGUE_NAME}'
                    AND season_year = {SEASON_YEAR}
            """
            lsa = connection.execute(statement).first()
            assert lsa is None

            statement = f"""
                SELECT *
                FROM pro_football.seasons
                WHERE
                    year = {SEASON_YEAR}
            """
            season = connection.execute(statement).first()
            season_num_of_weeks_completed = season[3]
            assert season_num_of_weeks_completed == 0

            statement = f"""
                SELECT *
                FROM pro_football.team_seasons
            """
            tsa_list = connection.execute(statement).all()
            for tsa in tsa_list:
                tsa_offensive_average = tsa[15]
                assert tsa_offensive_average is None

                tsa_offensive_factor = tsa[16]
                assert tsa_offensive_factor is None

                tsa_offensive_index = tsa[17]
                assert tsa_offensive_index is None

                tsa_defensive_average = tsa[18]
                assert tsa_defensive_average is None

                tsa_defensive_factor = tsa[19]
                assert tsa_defensive_factor is None

                tsa_defensive_index = tsa[20]
                assert tsa_defensive_index is None

                tsa_final_expected_winning_percentage = tsa[21]
                assert tsa_final_expected_winning_percentage is None
        
    def test_run_weekly_update_should_update_league_season_when_get_league_season_totals_returns_records_and_league_season_table_has_record_for_specified_league_and_season_and_game_table_is_empty(self):
        # Arrange
        statement = f"""
            INSERT INTO pro_football.seasons(year, num_of_weeks_completed)
            VALUES({SEASON_YEAR}, 0);
        """
        set_up_seasons_table(statement)
        set_up_leagues_table()
        set_up_conferences_table()
        set_up_divisions_table()
        set_up_teams_table()
        set_up_league_seasons_table()

        for tsa in TEAM_SEASONS:
            statement = f"""
                INSERT INTO pro_football.team_seasons(
                    team_name, season_year, league_name, conference_name, division_name, games, points_for
                )
                VALUES(
                    '{tsa.team_name}',
                    {tsa.season_year},
                    '{tsa.league_name}',
                    '{tsa.conference_name}',
                    '{tsa.division_name}',
                    1, 2
                )
            """
            set_up_team_season_record(tsa, statement)

        # Act
        self._test_service.run_weekly_update(LEAGUE_NAME, SEASON_YEAR)

        # Assert
        with engine.connect() as connection:
            statement = f"""
                SELECT *
                FROM pro_football.league_seasons
                WHERE
                    league_name = '{LEAGUE_NAME}'
                    AND season_year = {SEASON_YEAR}
            """
            lsa = connection.execute(statement).first()

            lsa_total_games = lsa[3]
            assert lsa_total_games == 32

            lsa_total_points = lsa[4]
            assert lsa_total_points == 64

            lsa_average_points = lsa[5]
            assert lsa_average_points == Decimal('2')

            statement = f"""
                SELECT *
                FROM pro_football.seasons
                WHERE
                    year = {SEASON_YEAR}
            """
            season = connection.execute(statement).first()
            season_num_of_weeks_completed = season[3]
            assert season_num_of_weeks_completed == 0

            statement = f"""
                SELECT *
                FROM pro_football.team_seasons
            """
            tsa_list = connection.execute(statement).all()
            for tsa in tsa_list:
                tsa_offensive_average = tsa[15]
                assert tsa_offensive_average is None

                tsa_offensive_factor = tsa[16]
                assert tsa_offensive_factor is None

                tsa_offensive_index = tsa[17]
                assert tsa_offensive_index is None

                tsa_defensive_average = tsa[18]
                assert tsa_defensive_average is None

                tsa_defensive_factor = tsa[19]
                assert tsa_defensive_factor is None

                tsa_defensive_index = tsa[20]
                assert tsa_defensive_index is None

                tsa_final_expected_winning_percentage = tsa[21]
                assert tsa_final_expected_winning_percentage is None

    def test_run_weekly_update_should_not_update_season_table_when_game_table_is_empty(self):
        # Arrange
        statement = f"""
            INSERT INTO pro_football.seasons(year, num_of_weeks_completed)
            VALUES({SEASON_YEAR}, 0);
        """
        set_up_seasons_table(statement)
        set_up_leagues_table()
        set_up_conferences_table()
        set_up_divisions_table()
        set_up_teams_table()
        set_up_league_seasons_table()

        for tsa in TEAM_SEASONS:
            statement = f"""
                INSERT INTO pro_football.team_seasons(
                    team_name, season_year, league_name, conference_name, division_name, games, points_for
                )
                VALUES(
                    '{tsa.team_name}',
                    {tsa.season_year},
                    '{tsa.league_name}',
                    '{tsa.conference_name}',
                    '{tsa.division_name}',
                    1, 2
                )
            """
            set_up_team_season_record(tsa, statement)

        # Act
        self._test_service.run_weekly_update(LEAGUE_NAME, SEASON_YEAR)

        # Assert
        with engine.connect() as connection:
            statement = f"""
                SELECT *
                FROM pro_football.league_seasons
                WHERE
                    league_name = '{LEAGUE_NAME}'
                    AND season_year = {SEASON_YEAR}
            """
            lsa = connection.execute(statement).first()

            lsa_total_games = lsa[3]
            assert lsa_total_games == 32

            lsa_total_points = lsa[4]
            assert lsa_total_points == 64

            lsa_average_points = lsa[5]
            assert lsa_average_points == Decimal('2')

            statement = f"""
                SELECT *
                FROM pro_football.seasons
                WHERE
                    year = {SEASON_YEAR}
            """
            season = connection.execute(statement).first()
            season_num_of_weeks_completed = season[3]
            assert season_num_of_weeks_completed == 0

            statement = f"""
                SELECT *
                FROM pro_football.team_seasons
            """
            tsa_list = connection.execute(statement).all()
            for tsa in tsa_list:
                tsa_offensive_average = tsa[15]
                assert tsa_offensive_average is None

                tsa_offensive_factor = tsa[16]
                assert tsa_offensive_factor is None

                tsa_offensive_index = tsa[17]
                assert tsa_offensive_index is None

                tsa_defensive_average = tsa[18]
                assert tsa_defensive_average is None

                tsa_defensive_factor = tsa[19]
                assert tsa_defensive_factor is None

                tsa_defensive_index = tsa[20]
                assert tsa_defensive_index is None

                tsa_final_expected_winning_percentage = tsa[21]
                assert tsa_final_expected_winning_percentage is None

    def test_run_weekly_update_should_not_update_season_table_when_game_table_has_no_records_for_specified_year(self):
        # Arrange
        statement = f"""
            INSERT INTO pro_football.seasons(year, num_of_weeks_completed)
            VALUES({SEASON_YEAR}, 0);
        """
        set_up_seasons_table(statement)
        statement = f"""
            INSERT INTO pro_football.seasons(year, num_of_weeks_completed)
            VALUES({SEASON_YEAR - 1}, 0);
        """
        set_up_seasons_table(statement)

        set_up_leagues_table()
        set_up_conferences_table()
        set_up_divisions_table()
        set_up_teams_table()
        set_up_league_seasons_table()

        for tsa in TEAM_SEASONS:
            statement = f"""
                INSERT INTO pro_football.team_seasons(
                    team_name, season_year, league_name, conference_name, division_name, games, points_for
                )
                VALUES(
                    '{tsa.team_name}',
                    {tsa.season_year},
                    '{tsa.league_name}',
                    '{tsa.conference_name}',
                    '{tsa.division_name}',
                    1, 2
                )
            """
            set_up_team_season_record(tsa, statement)

        for tsa in TEAM_SEASONS:
            statement = f"""
                INSERT INTO pro_football.team_seasons(
                    team_name, season_year, league_name, conference_name, division_name, games, points_for
                )
                VALUES(
                    '{tsa.team_name}',
                    {tsa.season_year - 1},
                    '{tsa.league_name}',
                    '{tsa.conference_name}',
                    '{tsa.division_name}',
                    1, 2
                )
            """
            set_up_team_season_record(tsa, statement)

        games = get_default_games(season_year=(SEASON_YEAR - 1), week=1)
        set_up_games_table(games=games)

        # Act
        self._test_service.run_weekly_update(LEAGUE_NAME, SEASON_YEAR)

        # Assert
        with engine.connect() as connection:
            statement = f"""
                SELECT *
                FROM pro_football.league_seasons
                WHERE
                    league_name = '{LEAGUE_NAME}'
                    AND season_year = {SEASON_YEAR}
            """
            lsa = connection.execute(statement).first()

            lsa_total_games = lsa[3]
            assert lsa_total_games == 32

            lsa_total_points = lsa[4]
            assert lsa_total_points == 64

            lsa_average_points = lsa[5]
            assert lsa_average_points == Decimal('2')

            statement = f"""
                SELECT *
                FROM pro_football.seasons
                WHERE
                    year = {SEASON_YEAR}
            """
            season = connection.execute(statement).first()
            season_num_of_weeks_completed = season[3]
            assert season_num_of_weeks_completed == 0

            statement = f"""
                SELECT *
                FROM pro_football.team_seasons
            """
            tsa_list = connection.execute(statement).all()
            for tsa in tsa_list:
                tsa_offensive_average = tsa[15]
                assert tsa_offensive_average is None

                tsa_offensive_factor = tsa[16]
                assert tsa_offensive_factor is None

                tsa_offensive_index = tsa[17]
                assert tsa_offensive_index is None

                tsa_defensive_average = tsa[18]
                assert tsa_defensive_average is None

                tsa_defensive_factor = tsa[19]
                assert tsa_defensive_factor is None

                tsa_defensive_index = tsa[20]
                assert tsa_defensive_index is None

                tsa_final_expected_winning_percentage = tsa[21]
                assert tsa_final_expected_winning_percentage is None

    def test_run_weekly_update_should_update_season_table_when_game_table_and_season_table_have_records_for_specified_year(self):
        # Arrange
        statement = f"""
            INSERT INTO pro_football.seasons(year, num_of_weeks_completed)
            VALUES({SEASON_YEAR}, 0);
        """
        set_up_seasons_table(statement)
        set_up_leagues_table()
        set_up_conferences_table()
        set_up_divisions_table()
        set_up_teams_table()
        set_up_league_seasons_table()

        for tsa in TEAM_SEASONS:
            statement = f"""
                INSERT INTO pro_football.team_seasons(
                    team_name, season_year, league_name, conference_name, division_name, games, points_for
                )
                VALUES(
                    '{tsa.team_name}',
                    {tsa.season_year},
                    '{tsa.league_name}',
                    '{tsa.conference_name}',
                    '{tsa.division_name}',
                    1, 2
                )
            """
            set_up_team_season_record(tsa, statement)

        week = 1
        set_up_games_table(week=week)

        # Act
        self._test_service.run_weekly_update(LEAGUE_NAME, SEASON_YEAR)

        # Assert
        with engine.connect() as connection:
            statement = f"""
                SELECT *
                FROM pro_football.league_seasons
                WHERE
                    league_name = '{LEAGUE_NAME}'
                    AND season_year = {SEASON_YEAR}
            """
            lsa = connection.execute(statement).first()

            lsa_total_games = lsa[3]
            assert lsa_total_games == 32

            lsa_total_points = lsa[4]
            assert lsa_total_points == 64

            lsa_average_points = lsa[5]
            assert lsa_average_points == Decimal('2')

            statement = f"""
                SELECT *
                FROM pro_football.seasons
                WHERE
                    year = {SEASON_YEAR}
            """
            season = connection.execute(statement).first()
            season_num_of_weeks_completed = season[3]
            assert season_num_of_weeks_completed == week

            statement = f"""
                SELECT *
                FROM pro_football.team_seasons
            """
            tsa_list = connection.execute(statement).all()
            for tsa in tsa_list:
                tsa_offensive_average = tsa[15]
                assert tsa_offensive_average is None

                tsa_offensive_factor = tsa[16]
                assert tsa_offensive_factor is None

                tsa_offensive_index = tsa[17]
                assert tsa_offensive_index is None

                tsa_defensive_average = tsa[18]
                assert tsa_defensive_average is None

                tsa_defensive_factor = tsa[19]
                assert tsa_defensive_factor is None

                tsa_defensive_index = tsa[20]
                assert tsa_defensive_index is None

                tsa_final_expected_winning_percentage = tsa[21]
                assert tsa_final_expected_winning_percentage is None

    def test_run_weekly_update_should_not_update_team_season_table_when_week_count_is_less_than_three(self):
        # Arrange
        statement = f"""
            INSERT INTO pro_football.seasons(year, num_of_weeks_completed)
            VALUES({SEASON_YEAR}, 0);
        """
        set_up_seasons_table(statement)
        set_up_leagues_table()
        set_up_conferences_table()
        set_up_divisions_table()
        set_up_teams_table()
        set_up_league_seasons_table()

        for tsa in TEAM_SEASONS:
            statement = f"""
                INSERT INTO pro_football.team_seasons(
                    team_name, season_year, league_name, conference_name, division_name, games, points_for
                )
                VALUES(
                    '{tsa.team_name}',
                    {tsa.season_year},
                    '{tsa.league_name}',
                    '{tsa.conference_name}',
                    '{tsa.division_name}',
                    1, 2
                )
            """
            set_up_team_season_record(tsa, statement)

        week = 2
        set_up_games_table(week=week)

        # Act
        self._test_service.run_weekly_update(LEAGUE_NAME, SEASON_YEAR)

        # Assert
        with engine.connect() as connection:
            statement = f"""
                SELECT *
                FROM pro_football.league_seasons
                WHERE
                    league_name = '{LEAGUE_NAME}'
                    AND season_year = {SEASON_YEAR}
            """
            lsa = connection.execute(statement).first()

            lsa_total_games = lsa[3]
            assert lsa_total_games == 32

            lsa_total_points = lsa[4]
            assert lsa_total_points == 64

            lsa_average_points = lsa[5]
            assert lsa_average_points == Decimal('2')

            statement = f"""
                SELECT *
                FROM pro_football.seasons
                WHERE
                    year = {SEASON_YEAR}
            """
            season = connection.execute(statement).first()
            season_num_of_weeks_completed = season[3]
            assert season_num_of_weeks_completed == week

            statement = f"""
                SELECT *
                FROM pro_football.team_seasons
            """
            tsa_list = connection.execute(statement).all()
            for tsa in tsa_list:
                tsa_offensive_average = tsa[15]
                assert tsa_offensive_average is None

                tsa_offensive_factor = tsa[16]
                assert tsa_offensive_factor is None

                tsa_offensive_index = tsa[17]
                assert tsa_offensive_index is None

                tsa_defensive_average = tsa[18]
                assert tsa_defensive_average is None

                tsa_defensive_factor = tsa[19]
                assert tsa_defensive_factor is None

                tsa_defensive_index = tsa[20]
                assert tsa_defensive_index is None

                tsa_final_expected_winning_percentage = tsa[21]
                assert tsa_final_expected_winning_percentage is None

    def test_run_weekly_update_should_update_team_season_table_when_week_count_is_three_and_team_season_table_has_no_records_for_specified_year(self):
        # Arrange
        statement = f"""
            INSERT INTO pro_football.seasons(year, num_of_weeks_completed)
            VALUES({SEASON_YEAR}, 0);
        """
        set_up_seasons_table(statement)
        set_up_leagues_table()
        set_up_conferences_table()
        set_up_divisions_table()
        set_up_teams_table()
        set_up_league_seasons_table()

        week = 3
        set_up_games_table(week=week)

        # Act
        self._test_service.run_weekly_update(LEAGUE_NAME, SEASON_YEAR)

        # Assert
        with engine.connect() as connection:
            statement = f"""
                SELECT *
                FROM pro_football.league_seasons
                WHERE
                    league_name = '{LEAGUE_NAME}'
                    AND season_year = {SEASON_YEAR}
            """
            lsa = connection.execute(statement).first()

            lsa_total_games = lsa[3]
            assert lsa_total_games == 0

            lsa_total_points = lsa[4]
            assert lsa_total_points == 0

            lsa_average_points = lsa[5]
            assert lsa_average_points is None

            statement = f"""
                SELECT *
                FROM pro_football.seasons
                WHERE
                    year = {SEASON_YEAR}
            """
            season = connection.execute(statement).first()
            season_num_of_weeks_completed = season[3]
            assert season_num_of_weeks_completed == week

            statement = f"""
                SELECT *
                FROM pro_football.team_seasons
            """
            tsa_list = connection.execute(statement).all()
            for tsa in tsa_list:
                tsa_offensive_average = tsa[15]
                assert tsa_offensive_average is None

                tsa_offensive_factor = tsa[16]
                assert tsa_offensive_factor is None

                tsa_offensive_index = tsa[17]
                assert tsa_offensive_index is None

                tsa_defensive_average = tsa[18]
                assert tsa_defensive_average is None

                tsa_defensive_factor = tsa[19]
                assert tsa_defensive_factor is None

                tsa_defensive_index = tsa[20]
                assert tsa_defensive_index is None

                tsa_final_expected_winning_percentage = tsa[21]
                assert tsa_final_expected_winning_percentage is None

    def test_run_weekly_update_should_update_team_season_table_when_week_count_is_greater_than_three_and_team_season_table_has_no_records_for_specified_year(self):
        # Arrange
        statement = f"""
            INSERT INTO pro_football.seasons(year, num_of_weeks_completed)
            VALUES({SEASON_YEAR}, 0);
        """
        set_up_seasons_table(statement)
        set_up_leagues_table()
        set_up_conferences_table()
        set_up_divisions_table()
        set_up_teams_table()
        set_up_league_seasons_table()

        week = 4
        set_up_games_table(week=week)

        # Act
        self._test_service.run_weekly_update(LEAGUE_NAME, SEASON_YEAR)

        # Assert
        with engine.connect() as connection:
            statement = f"""
                SELECT *
                FROM pro_football.league_seasons
                WHERE
                    league_name = '{LEAGUE_NAME}'
                    AND season_year = {SEASON_YEAR}
            """
            lsa = connection.execute(statement).first()

            lsa_total_games = lsa[3]
            assert lsa_total_games == 0

            lsa_total_points = lsa[4]
            assert lsa_total_points == 0

            lsa_average_points = lsa[5]
            assert lsa_average_points is None

            statement = f"""
                SELECT *
                FROM pro_football.seasons
                WHERE
                    year = {SEASON_YEAR}
            """
            season = connection.execute(statement).first()
            season_num_of_weeks_completed = season[3]
            assert season_num_of_weeks_completed == week

            statement = f"""
                SELECT *
                FROM pro_football.team_seasons
            """
            tsa_list = connection.execute(statement).all()
            for tsa in tsa_list:
                tsa_offensive_average = tsa[15]
                assert tsa_offensive_average is None

                tsa_offensive_factor = tsa[16]
                assert tsa_offensive_factor is None

                tsa_offensive_index = tsa[17]
                assert tsa_offensive_index is None

                tsa_defensive_average = tsa[18]
                assert tsa_defensive_average is None

                tsa_defensive_factor = tsa[19]
                assert tsa_defensive_factor is None

                tsa_defensive_index = tsa[20]
                assert tsa_defensive_index is None

                tsa_final_expected_winning_percentage = tsa[21]
                assert tsa_final_expected_winning_percentage is None

    def test_run_weekly_update_should_update_team_season_table_when_week_count_is_greater_than_three_and_team_season_table_has_records_for_specified_year_and_get_team_season_schedule_totals_returns_schedule_games_equal_to_none(self):
        # Arrange
        statement = f"""
            INSERT INTO pro_football.seasons(year, num_of_weeks_completed)
            VALUES({SEASON_YEAR}, 0);
        """
        set_up_seasons_table(statement)
        set_up_leagues_table()
        set_up_conferences_table()
        set_up_divisions_table()
        set_up_teams_table()
        set_up_league_seasons_table()
        set_up_team_seasons_table()

        week = 4
        games = (
            Game(SEASON_YEAR, week, "Buffalo Bills", 31, "Los Angeles Rams", 10),
            Game(SEASON_YEAR, week, "New Orleans Saints", 27, "Atlanta Falcons", 26),
            Game(SEASON_YEAR, week, "Cleveland Browns", 26, "Carolina Panthers", 24),
            Game(SEASON_YEAR, week, "San Francisco 49ers", 10, "Chicago Bears", 19),
            Game(SEASON_YEAR, week, "Pittsburgh Steelers", 23, "Cincinnati Bengals", 20),
            Game(SEASON_YEAR, week, "Philadelphia Eagles", 38, "Detroit Lions", 35),
            Game(SEASON_YEAR, week, "Indianapolis Colts", 20, "Houston Texans", 20),
            Game(SEASON_YEAR, week, "New England Patriots", 7, "Miami Dolphins", 20),
            Game(SEASON_YEAR, week, "Baltimore Ravens", 24, "New York Jets", 9),
            Game(SEASON_YEAR, week, "Jacksonville Jaguars", 22, "Washington Commanders", 28),
            Game(SEASON_YEAR, week, "Kansas City Chiefs", 44, "Arizona Cardinals", 21),
            Game(SEASON_YEAR, week, "Green Bay Packers", 7, "Minnesota Vikings", 23),
            Game(SEASON_YEAR, week, "New York Giants", 21, "Tennessee Titans", 20),
            Game(SEASON_YEAR, week, "Las Vegas Raiders", 19, "Los Angeles Chargers", 24),
            Game(SEASON_YEAR, week, "Tampa Bay Buccaneers", 19, "Dallas Cowboys", 3),
            Game(SEASON_YEAR, week, "Denver Broncos", 16, "Seattle Seahawks", 17)
        )
        game_service = GameService()
        for game in games:
            game_service.add_game(game)

        # Act
        self._test_service.run_weekly_update(LEAGUE_NAME, SEASON_YEAR)

        # Assert
        with engine.connect() as connection:
            statement = f"""
                SELECT *
                FROM pro_football.league_seasons
                WHERE
                    league_name = '{LEAGUE_NAME}'
                    AND season_year = {SEASON_YEAR}
            """
            lsa = connection.execute(statement).first()

            lsa_total_games = lsa[3]
            assert lsa_total_games > 0

            lsa_total_points = lsa[4]
            assert lsa_total_points > 0

            lsa_average_points = lsa[5]
            assert lsa_average_points > 0

            statement = f"""
                SELECT *
                FROM pro_football.seasons
                WHERE
                    year = {SEASON_YEAR}
            """
            season = connection.execute(statement).first()
            season_num_of_weeks_completed = season[3]
            assert season_num_of_weeks_completed == week

            statement = f"""
                SELECT *
                FROM pro_football.team_seasons
            """
            tsa_list = connection.execute(statement).all()
            for tsa in tsa_list:
                tsa_offensive_average = tsa[15]
                assert tsa_offensive_average is None

                tsa_offensive_factor = tsa[16]
                assert tsa_offensive_factor is None

                tsa_offensive_index = tsa[17]
                assert tsa_offensive_index is None

                tsa_defensive_average = tsa[18]
                assert tsa_defensive_average is None

                tsa_defensive_factor = tsa[19]
                assert tsa_defensive_factor is None

                tsa_defensive_index = tsa[20]
                assert tsa_defensive_index is None

                tsa_final_expected_winning_percentage = tsa[21]
                assert tsa_final_expected_winning_percentage is None

    def test_run_weekly_update_should_update_team_season_table_when_week_count_is_greater_than_three_and_team_season_table_has_records_for_specified_year_and_get_team_season_schedule_totals_returns_schedule_games_not_equal_to_none(self):
        # Arrange
        statement = f"""
            INSERT INTO pro_football.seasons(year, num_of_weeks_completed)
            VALUES({SEASON_YEAR}, 0);
        """
        set_up_seasons_table(statement)
        set_up_leagues_table()
        set_up_conferences_table()
        set_up_divisions_table()
        set_up_teams_table()
        set_up_league_seasons_table()
        set_up_team_seasons_table()

        game_service = GameService()

        week = 1
        games = get_default_games(week=week)
        for game in games:
            game_service.add_game(game)

        week = 4
        games = (
            Game(SEASON_YEAR, week, "Miami Dolphins", 15, "Cincinnati Bengals", 27),
            Game(SEASON_YEAR, week, "Minnesota Vikings", 28, "New Orleans Saints", 25),
            Game(SEASON_YEAR, week, "Cleveland Browns", 20, "Atlanta Falcons", 23),
            Game(SEASON_YEAR, week, "Tennessee Titans", 24, "Indianapolis Colts", 17),
            Game(SEASON_YEAR, week, "Washington Commanders", 10, "Dallas Cowboys", 25),
            Game(SEASON_YEAR, week, "Seattle Seahawks", 48, "Detroit Lions", 45),
            Game(SEASON_YEAR, week, "Los Angeles Chargers", 34, "Houston Texans", 24),
            Game(SEASON_YEAR, week, "Chicago Bears", 12, "New York Giants", 20),
            Game(SEASON_YEAR, week, "Jacksonville Jaguars", 21, "Philadelphia Eagles", 29),
            Game(SEASON_YEAR, week, "New York Jets", 24, "Pittsburgh Steelers", 20),
            Game(SEASON_YEAR, week, "Buffalo Bills", 23, "Baltimore Ravens", 20),
            Game(SEASON_YEAR, week, "Arizona Cardinals", 26, "Carolina Panthers", 16),
            Game(SEASON_YEAR, week, "New England Patriots", 27, "Green Bay Packers", 24),
            Game(SEASON_YEAR, week, "Denver Broncos", 23, "Las Vegas Raiders", 32),
            Game(SEASON_YEAR, week, "Kansas City Chiefs", 41, "Tampa Bay Buccaneers", 31),
            Game(SEASON_YEAR, week, "Los Angeles Rams", 9, "San Francisco 49ers", 24)
        )
        for game in games:
            game_service.add_game(game)

        # Act
        self._test_service.run_weekly_update(LEAGUE_NAME, SEASON_YEAR)

        # Assert
        with engine.connect() as connection:
            statement = f"""
                SELECT *
                FROM pro_football.league_seasons
                WHERE
                    league_name = '{LEAGUE_NAME}'
                    AND season_year = {SEASON_YEAR}
            """
            lsa = connection.execute(statement).first()

            lsa_total_games = lsa[3]
            assert lsa_total_games > 0

            lsa_total_points = lsa[4]
            assert lsa_total_points > 0

            lsa_average_points = lsa[5]
            assert lsa_average_points > 0

            statement = f"""
                SELECT *
                FROM pro_football.seasons
                WHERE
                    year = {SEASON_YEAR}
            """
            season = connection.execute(statement).first()
            season_num_of_weeks_completed = season[3]
            assert season_num_of_weeks_completed == week

            statement = f"""
                SELECT *
                FROM pro_football.team_seasons
            """
            tsa_list = connection.execute(statement).all()
            for tsa in tsa_list:
                tsa_offensive_average = tsa[15]
                assert tsa_offensive_average is not None

                tsa_offensive_factor = tsa[16]
                assert tsa_offensive_factor is not None

                tsa_offensive_index = tsa[17]
                assert tsa_offensive_index is not None

                tsa_defensive_average = tsa[18]
                assert tsa_defensive_average is not None

                tsa_defensive_factor = tsa[19]
                assert tsa_defensive_factor is not None

                tsa_defensive_index = tsa[20]
                assert tsa_defensive_index is not None

                tsa_final_expected_winning_percentage = tsa[21]
                assert tsa_final_expected_winning_percentage is not None
