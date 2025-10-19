from sqlalchemy import create_engine

from app.data.entities.league import League
from app.data.entities.conference import Conference
from app.data.entities.division import Division
from app.data.entities.team import Team
from app.data.entities.team_season import TeamSeason
from app.data.entities.game import Game

engine = create_engine('mysql+mysqlconnector://root:root@localhost:3306/test_app')

SEASON_YEAR = 2022
LEAGUE_NAME = 'NFL'
TEAM_SEASONS = (
    TeamSeason(
        team_name='Arizona Cardinals',
        season_year=SEASON_YEAR,
        league_name=LEAGUE_NAME,
        conference_name='NFC',
        division_name='NFC West'
    ),
    TeamSeason(
        team_name='Atlanta Falcons',
        season_year=SEASON_YEAR,
        league_name=LEAGUE_NAME,
        conference_name='NFC',
        division_name='NFC South'
    ),
    TeamSeason(
        team_name='Baltimore Ravens',
        season_year=SEASON_YEAR,
        league_name=LEAGUE_NAME,
        conference_name='AFC',
        division_name='AFC North'
    ),
    TeamSeason(
        team_name='Buffalo Bills',
        season_year=SEASON_YEAR,
        league_name=LEAGUE_NAME,
        conference_name='AFC',
        division_name='AFC East'
    ),
    TeamSeason(
        team_name='Carolina Panthers',
        season_year=SEASON_YEAR,
        league_name=LEAGUE_NAME,
        conference_name='NFC',
        division_name='NFC South'
    ),
    TeamSeason(
        team_name='Chicago Bears',
        season_year=SEASON_YEAR,
        league_name=LEAGUE_NAME,
        conference_name='NFC',
        division_name='NFC North'
    ),
    TeamSeason(
        team_name='Cincinnati Bengals',
        season_year=SEASON_YEAR,
        league_name=LEAGUE_NAME,
        conference_name='AFC',
        division_name='AFC North'
    ),
    TeamSeason(
        team_name='Cleveland Browns',
        season_year=SEASON_YEAR,
        league_name=LEAGUE_NAME,
        conference_name='AFC',
        division_name='AFC North'
    ),
    TeamSeason(
        team_name='Dallas Cowboys',
        season_year=SEASON_YEAR,
        league_name=LEAGUE_NAME,
        conference_name='NFC',
        division_name='NFC East'
    ),
    TeamSeason(
        team_name='Denver Broncos',
        season_year=SEASON_YEAR,
        league_name=LEAGUE_NAME,
        conference_name='AFC',
        division_name='AFC West'
    ),
    TeamSeason(
        team_name='Detroit Lions',
        season_year=SEASON_YEAR,
        league_name=LEAGUE_NAME,
        conference_name='NFC',
        division_name='NFC North'
    ),
    TeamSeason(
        team_name='Green Bay Packers',
        season_year=SEASON_YEAR,
        league_name=LEAGUE_NAME,
        conference_name='NFC',
        division_name='NFC North'
    ),
    TeamSeason(
        team_name='Houston Texans',
        season_year=SEASON_YEAR,
        league_name=LEAGUE_NAME,
        conference_name='AFC',
        division_name='AFC South'
    ),
    TeamSeason(
        team_name='Indianapolis Colts',
        season_year=SEASON_YEAR,
        league_name=LEAGUE_NAME,
        conference_name='AFC',
        division_name='AFC South'
    ),
    TeamSeason(
        team_name='Jacksonville Jaguars',
        season_year=SEASON_YEAR,
        league_name=LEAGUE_NAME,
        conference_name='AFC',
        division_name='AFC South'
    ),
    TeamSeason(
        team_name='Kansas City Chiefs',
        season_year=SEASON_YEAR,
        league_name=LEAGUE_NAME,
        conference_name='AFC',
        division_name='AFC West'
    ),
    TeamSeason(
        team_name='Las Vegas Raiders',
        season_year=SEASON_YEAR,
        league_name=LEAGUE_NAME,
        conference_name='AFC',
        division_name='AFC West'
    ),
    TeamSeason(
        team_name='Los Angeles Chargers',
        season_year=SEASON_YEAR,
        league_name=LEAGUE_NAME,
        conference_name='AFC',
        division_name='AFC West'
    ),
    TeamSeason(
        team_name='Los Angeles Rams',
        season_year=SEASON_YEAR,
        league_name=LEAGUE_NAME,
        conference_name='NFC',
        division_name='NFC West'
    ),
    TeamSeason(
        team_name='Miami Dolphins',
        season_year=SEASON_YEAR,
        league_name=LEAGUE_NAME,
        conference_name='AFC',
        division_name='AFC East'
    ),
    TeamSeason(
        team_name='Minnesota Vikings',
        season_year=SEASON_YEAR,
        league_name=LEAGUE_NAME,
        conference_name='NFC',
        division_name='NFC North'
    ),
    TeamSeason(
        team_name='New England Patriots',
        season_year=SEASON_YEAR,
        league_name=LEAGUE_NAME,
        conference_name='AFC',
        division_name='AFC East'
    ),
    TeamSeason(
        team_name='New Orleans Saints',
        season_year=SEASON_YEAR,
        league_name=LEAGUE_NAME,
        conference_name='NFC',
        division_name='NFC South'
    ),
    TeamSeason(
        team_name='New York Giants',
        season_year=SEASON_YEAR,
        league_name=LEAGUE_NAME,
        conference_name='NFC',
        division_name='NFC East'
    ),
    TeamSeason(
        team_name='New York Jets',
        season_year=SEASON_YEAR,
        league_name=LEAGUE_NAME,
        conference_name='AFC',
        division_name='AFC East'
    ),
    TeamSeason(
        team_name='Philadelphia Eagles',
        season_year=SEASON_YEAR,
        league_name=LEAGUE_NAME,
        conference_name='NFC',
        division_name='NFC East'
    ),
    TeamSeason(
        team_name='Pittsburgh Steelers',
        season_year=SEASON_YEAR,
        league_name=LEAGUE_NAME,
        conference_name='AFC',
        division_name='AFC North'
    ),
    TeamSeason(
        team_name='San Francisco 49ers',
        season_year=SEASON_YEAR,
        league_name=LEAGUE_NAME,
        conference_name='NFC',
        division_name='NFC West'
    ),
    TeamSeason(
        team_name='Seattle Seahawks',
        season_year=SEASON_YEAR,
        league_name=LEAGUE_NAME,
        conference_name='NFC',
        division_name='NFC West'
    ),
    TeamSeason(
        team_name='Tampa Bay Buccaneers',
        season_year=SEASON_YEAR,
        league_name=LEAGUE_NAME,
        conference_name='NFC',
        division_name='NFC South'
    ),
    TeamSeason(
        team_name='Tennessee Titans',
        season_year=SEASON_YEAR,
        league_name=LEAGUE_NAME,
        conference_name='AFC',
        division_name='AFC South'
    ),
    TeamSeason(
        team_name='Washington Commanders',
        season_year=SEASON_YEAR,
        league_name=LEAGUE_NAME,
        conference_name='NFC',
        division_name='NFC East'
    )
)


def clear_database() -> None:
    connection = engine.connect()
    transaction = connection.begin()
    try:
        tables = (
            'test_app.seasons',
            'test_app.teams'
        )

        for table in tables:
            statement = f"""
                DELETE FROM {table};
            """
            connection.execute(statement)

        transaction.commit()
    except:
        transaction.rollback()
        raise


def set_up_seasons_table(statement: str = None) -> None:
    connection = engine.connect()
    transaction = connection.begin()
    try:
        sql = statement or f"""
            INSERT INTO test_app.seasons(year)
            VALUES({SEASON_YEAR});
        """
        connection.execute(sql)
        transaction.commit()
    except:
        transaction.rollback()
        raise


def set_up_leagues_table() -> None:
    connection = engine.connect()
    transaction = connection.begin()
    try:
        leagues = (
            League(long_name='National Football League', short_name=LEAGUE_NAME, first_season_year=SEASON_YEAR),
        )

        for league in leagues:
            statement = f"""
                INSERT INTO test_app.leagues(long_name, short_name, first_season_year)
                VALUES('{league.long_name}', '{league.short_name}', {league.first_season_year});
            """
            connection.execute(statement)

        transaction.commit()
    except:
        transaction.rollback()
        raise


def set_up_conferences_table() -> None:
    connection = engine.connect()
    transaction = connection.begin()
    try:
        conferences = (
            Conference(
                league_name=LEAGUE_NAME,
                long_name='American Football Conference',
                short_name='AFC',
                first_season_year=SEASON_YEAR
            ),
            Conference(
                league_name=LEAGUE_NAME,
                long_name='National Football Conference',
                short_name='NFC',
                first_season_year=SEASON_YEAR
            )
        )

        for conference in conferences:
            statement = f"""
                INSERT INTO test_app.conferences(league_name, long_name, short_name, first_season_year)
                VALUES(
                    '{conference.league_name}',
                    '{conference.long_name}',
                    '{conference.short_name}',
                    {conference.first_season_year}
                );
            """
            connection.execute(statement)

        transaction.commit()
    except:
        transaction.rollback()
        raise


def set_up_divisions_table() -> None:
    connection = engine.connect()
    transaction = connection.begin()
    try:
        divisions = (
            Division(league_name=LEAGUE_NAME, conference_name='AFC', name='AFC East', first_season_year=SEASON_YEAR),
            Division(league_name=LEAGUE_NAME, conference_name='AFC', name='AFC North', first_season_year=SEASON_YEAR),
            Division(league_name=LEAGUE_NAME, conference_name='AFC', name='AFC South', first_season_year=SEASON_YEAR),
            Division(league_name=LEAGUE_NAME, conference_name='AFC', name='AFC West', first_season_year=SEASON_YEAR),
            Division(league_name=LEAGUE_NAME, conference_name='NFC', name='NFC East', first_season_year=SEASON_YEAR),
            Division(league_name=LEAGUE_NAME, conference_name='NFC', name='NFC North', first_season_year=SEASON_YEAR),
            Division(league_name=LEAGUE_NAME, conference_name='NFC', name='NFC South', first_season_year=SEASON_YEAR),
            Division(league_name=LEAGUE_NAME, conference_name='NFC', name='NFC West', first_season_year=SEASON_YEAR)
        )

        for division in divisions:
            statement = f"""
                INSERT INTO test_app.divisions(league_name, conference_name, name, first_season_year)
                VALUES(
                    '{division.league_name}',
                    '{division.conference_name}',
                    '{division.name}',
                    {division.first_season_year}
                );
            """
            connection.execute(statement)

        transaction.commit()
    except:
        transaction.rollback()
        raise


def set_up_teams_table() -> None:
    connection = engine.connect()
    transaction = connection.begin()
    try:
        teams = (
            Team(name='Arizona Cardinals'),
            Team(name='Atlanta Falcons'),
            Team(name='Baltimore Ravens'),
            Team(name='Buffalo Bills'),
            Team(name='Carolina Panthers'),
            Team(name='Chicago Bears'),
            Team(name='Cincinnati Bengals'),
            Team(name='Cleveland Browns'),
            Team(name='Dallas Cowboys'),
            Team(name='Denver Broncos'),
            Team(name='Detroit Lions'),
            Team(name='Green Bay Packers'),
            Team(name='Houston Texans'),
            Team(name='Indianapolis Colts'),
            Team(name='Jacksonville Jaguars'),
            Team(name='Kansas City Chiefs'),
            Team(name='Las Vegas Raiders'),
            Team(name='Los Angeles Chargers'),
            Team(name='Los Angeles Rams'),
            Team(name='Miami Dolphins'),
            Team(name='Minnesota Vikings'),
            Team(name='New England Patriots'),
            Team(name='New Orleans Saints'),
            Team(name='New York Giants'),
            Team(name='New York Jets'),
            Team(name='Philadelphia Eagles'),
            Team(name='Pittsburgh Steelers'),
            Team(name='San Francisco 49ers'),
            Team(name='Seattle Seahawks'),
            Team(name='Tampa Bay Buccaneers'),
            Team(name='Tennessee Titans'),
            Team(name='Washington Commanders')
        )

        for team in teams:
            statement = f"""
                INSERT INTO test_app.teams(name)
                VALUES('{team.name}');
            """
            connection.execute(statement)

        transaction.commit()
    except:
        transaction.rollback()
        raise


def set_up_league_seasons_table(statement: str = None) -> None:
    connection = engine.connect()
    transaction = connection.begin()
    try:
        sql = statement or f"""
            INSERT INTO test_app.league_seasons(league_name, season_year)
            VALUES('{LEAGUE_NAME}', {SEASON_YEAR});
        """
        connection.execute(sql)
        transaction.commit()
    except:
        transaction.rollback()
        raise


def set_up_team_seasons_table(team_season_associations: list | tuple = None) -> None:
    tsa_collection = team_season_associations or TEAM_SEASONS

    connection = engine.connect()
    transaction = connection.begin()
    try:
        for tsa in tsa_collection:
            statement = f"""
            INSERT INTO test_app.team_seasons(
                team_name,
                season_year,
                league_name,
                conference_name,
                division_name
            )
            VALUES(
                '{tsa.team_name}',
                {tsa.season_year},
                '{tsa.league_name}',
                '{tsa.conference_name}',
                '{tsa.division_name}'
            );
            """
            connection.execute(statement)

        transaction.commit()
    except:
        transaction.rollback()
        raise


def set_up_team_season_record(tsa: TeamSeason, statement: str = None) -> None:
    connection = engine.connect()
    transaction = connection.begin()
    try:
        sql = statement or f"""
            INSERT INTO test_app.team_seasons(
                team_name,
                season_year,
                league_name,
                conference_name,
                division_name
            )
            VALUES(
                '{tsa.team_name}',
                {tsa.season_year},
                '{tsa.league_name}',
                '{tsa.conference_name}',
                '{tsa.division_name}'
            )
        """
        connection.execute(sql)
        transaction.commit()
    except:
        transaction.rollback()
        raise


def set_up_games_table(season_year: int = SEASON_YEAR, week: int = 1, games: tuple = None) -> None:
    for game in games or get_default_games(season_year=season_year, week=week):
        connection = engine.connect()
        transaction = connection.begin()
        try:
            statement = f"""
                INSERT INTO test_app.games(
                    season_year,
                    week,
                    guest_name,
                    guest_score,
                    host_name,
                    host_score,
                    winner_name,
                    winner_score,
                    loser_name,
                    loser_score
                )
            """
            if game.winner_id is None or game.loser_id is None:
                statement += f"""
                    VALUES(
                        {game.season_year},
                        {game.week},
                        '{game.guest_id}',
                        {game.guest_score},
                        '{game.host_id}',
                        {game.host_score},
                        NULL,
                        NULL,
                        NULL,
                        NULL
                    )
                """
            else:
                statement += f"""
                    VALUES(
                        {game.season_year},
                        {game.week},
                        '{game.guest_id}',
                        {game.guest_score},
                        '{game.host_id}',
                        {game.host_score},
                        '{game.winner_id}',
                        {game.winner_score},
                        '{game.loser_id}',
                        {game.loser_score}
                    )
                """
            connection.execute(statement)
            transaction.commit()
        except:
            transaction.rollback()
            raise


def get_default_games(week: int, season_year: int = SEASON_YEAR) -> tuple:
    return (
        Game(season_year, week, "Buffalo Bills", 31, "Los Angeles Rams", 10),
        Game(season_year, week, "New Orleans Saints", 27, "Atlanta Falcons", 26),
        Game(season_year, week, "Cleveland Browns", 26, "Carolina Panthers", 24),
        Game(season_year, week, "San Francisco 49ers", 10, "Chicago Bears", 19),
        Game(season_year, week, "Pittsburgh Steelers", 23, "Cincinnati Bengals", 20),
        Game(season_year, week, "Philadelphia Eagles", 38, "Detroit Lions", 35),
        Game(season_year, week, "Indianapolis Colts", 20, "Houston Texans", 20),
        Game(season_year, week, "New England Patriots", 7, "Miami Dolphins", 20),
        Game(season_year, week, "Baltimore Ravens", 24, "New York Jets", 9),
        Game(season_year, week, "Jacksonville Jaguars", 22, "Washington Commanders", 28),
        Game(season_year, week, "Kansas City Chiefs", 44, "Arizona Cardinals", 21),
        Game(season_year, week, "Green Bay Packers", 7, "Minnesota Vikings", 23),
        Game(season_year, week, "New York Giants", 21, "Tennessee Titans", 20),
        Game(season_year, week, "Las Vegas Raiders", 19, "Los Angeles Chargers", 24),
        Game(season_year, week, "Tampa Bay Buccaneers", 19, "Dallas Cowboys", 3),
        Game(season_year, week, "Denver Broncos", 16, "Seattle Seahawks", 17)
    )
