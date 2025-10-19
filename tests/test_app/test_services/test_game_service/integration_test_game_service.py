from decimal import Decimal

import pytest

import unittest

from app.data.errors import EntityNotFoundError
from app.data.models.game import Game
from app.data.models.team_season import TeamSeason
from app.services.game_service.game_service import GameService

from test_app.test_services.database_setup import \
    SEASON_YEAR, clear_database, engine, set_up_seasons_table, set_up_leagues_table, \
    set_up_conferences_table, set_up_divisions_table, set_up_teams_table, set_up_league_seasons_table

GAME_DATA = {
    'id': 1,
    'season_year': SEASON_YEAR,
    'week': 20,
    'guest_id': "Cincinnati Bengals",
    'guest_score': 20,
    'host_id': "Los Angeles Rams",
    'host_score': 23,
    'is_playoff': True,
    'notes': "Super Bowl LVI"
}


class IntegrationTestGameService(unittest.TestCase):
    
    def setUp(self) -> None:
        clear_database()
        set_up_database()

    def tearDown(self) -> None:
        clear_database()

    def test_add_game_should_raise_entity_not_found_error_when_neither_team_is_in_league(self):
        # Arrange
        game = Game(
            id=GAME_DATA['id'],
            season_year=GAME_DATA['season_year'],
            week=GAME_DATA['week'],
            guest_name=GAME_DATA['guest_id'],
            guest_score=GAME_DATA['guest_score'],
            host_name=GAME_DATA['host_id'],
            host_score=GAME_DATA['host_score'],
            is_playoff=GAME_DATA['is_playoff'],
            notes=GAME_DATA['notes']
        )

        # Act
        with pytest.raises(EntityNotFoundError):
            test_service = GameService()
            test_service.add_game(game)
    
        # Assert
        verify_game_record_is_none()
        verify_team_season_record_is_none(game.guest_id, game.season_year)
        verify_team_season_record_is_none(game.host_id, game.season_year)

    def test_add_game_should_add_game_and_edit_guest_season_record_when_host_is_not_in_league(self):
        # Arrange
        game = Game(
            id=GAME_DATA['id'],
            season_year=GAME_DATA['season_year'],
            week=GAME_DATA['week'],
            guest_name=GAME_DATA['guest_id'],
            guest_score=GAME_DATA['guest_score'],
            host_name=GAME_DATA['host_id'],
            host_score=GAME_DATA['host_score'],
            is_playoff=GAME_DATA['is_playoff'],
            notes=GAME_DATA['notes']
        )

        league_name = 'NFL'
        conference_name = 'AFC'
        division_name = 'AFC North'
        tsa = TeamSeason(
            team_name=game.guest_id,
            season_year=game.season_year,
            league_name=league_name,
            conference_name=conference_name,
            division_name=division_name
        )
        add_team_season(tsa)

        # Act
        test_service = GameService()
        test_service.add_game(game)

        # Assert
        verify_game_record(game)

        tsa = TeamSeason(
            team_name=game.guest_id,
            season_year=game.season_year,
            league_name=league_name,
            conference_name=conference_name,
            division_name=division_name,
            games=1,
            wins=0,
            losses=1,
            ties=0,
            winning_percentage=Decimal('0'),
            points_for=20,
            points_against=23
        )
        verify_team_season_record(game.guest_id, game.season_year, tsa)

        verify_team_season_record_is_none(game.host_id, game.season_year)

    def test_add_game_should_add_game_and_edit_host_season_record_when_guest_is_not_in_league(self):
        # Arrange
        game = Game(
            id=GAME_DATA['id'],
            season_year=GAME_DATA['season_year'],
            week=GAME_DATA['week'],
            guest_name=GAME_DATA['guest_id'],
            guest_score=GAME_DATA['guest_score'],
            host_name=GAME_DATA['host_id'],
            host_score=GAME_DATA['host_score'],
            is_playoff=GAME_DATA['is_playoff'],
            notes=GAME_DATA['notes']
        )

        league_name = 'NFL'
        conference_name = 'NFC'
        division_name = 'NFC West'
        tsa = TeamSeason(
            team_name=game.host_id,
            season_year=game.season_year,
            league_name=league_name,
            conference_name=conference_name,
            division_name=division_name
        )
        add_team_season(tsa)

        # Act
        test_service = GameService()
        test_service.add_game(game)
    
        # Assert
        verify_game_record(game)

        verify_team_season_record_is_none(game.guest_id, game.season_year)

        tsa = TeamSeason(
            team_name=game.host_id,
            season_year=game.season_year,
            league_name=league_name,
            conference_name=conference_name,
            division_name=division_name,
            games=1,
            wins=1,
            losses=0,
            ties=0,
            winning_percentage=Decimal('1'),
            points_for=23,
            points_against=20
        )
        verify_team_season_record(game.host_id, game.season_year, tsa)

    def test_add_game_should_add_game_and_edit_both_team_season_records_when_both_teams_are_in_league(self):
        # Arrange
        game = Game(
            id=GAME_DATA['id'],
            season_year=GAME_DATA['season_year'],
            week=GAME_DATA['week'],
            guest_name=GAME_DATA['guest_id'],
            guest_score=GAME_DATA['guest_score'],
            host_name=GAME_DATA['host_id'],
            host_score=GAME_DATA['host_score'],
            is_playoff=GAME_DATA['is_playoff'],
            notes=GAME_DATA['notes']
        )

        league_name = 'NFL'

        guest_conference_name = 'AFC'
        guest_division_name = 'AFC North'
        guest_tsa = TeamSeason(
            team_name=game.guest_id,
            season_year=game.season_year,
            league_name=league_name,
            conference_name=guest_conference_name,
            division_name=guest_division_name
        )
        add_team_season(guest_tsa)

        host_conference_name = 'NFC'
        host_division_name = 'NFC West'
        host_tsa = TeamSeason(
            team_name=game.host_id,
            season_year=game.season_year,
            league_name=league_name,
            conference_name=host_conference_name,
            division_name=host_division_name
        )
        add_team_season(host_tsa)

        # Act
        test_service = GameService()
        test_service.add_game(game)

        # Assert
        verify_game_record(game)

        guest_tsa = TeamSeason(
            team_name=game.guest_id,
            season_year=game.season_year,
            league_name=league_name,
            conference_name=guest_conference_name,
            division_name=guest_division_name,
            games=1,
            wins=0,
            losses=1,
            ties=0,
            winning_percentage=Decimal('0'),
            points_for=20,
            points_against=23
        )
        verify_team_season_record(game.guest_id, game.season_year, guest_tsa)

        host_tsa = TeamSeason(
            team_name=game.host_id,
            season_year=game.season_year,
            league_name=league_name,
            conference_name=host_conference_name,
            division_name=host_division_name,
            games=1,
            wins=1,
            losses=0,
            ties=0,
            winning_percentage=Decimal('1'),
            points_for=23,
            points_against=20
        )
        verify_team_season_record(game.host_id, game.season_year, host_tsa)

    def test_edit_game_should_edit_game_and_not_edit_team_season_records_when_neither_team_is_in_league(self):
        # Arrange
        old_game = Game(
            id=GAME_DATA['id'],
            season_year=GAME_DATA['season_year'],
            week=GAME_DATA['week'],
            guest_name=GAME_DATA['host_id'],
            guest_score=GAME_DATA['host_score'],
            host_name=GAME_DATA['guest_id'],
            host_score=GAME_DATA['guest_score'],
            is_playoff=GAME_DATA['is_playoff'],
            notes=GAME_DATA['notes']
        )
        old_game.decide_winner_and_loser()
        add_game(old_game)
        
        new_game = Game(
            id=GAME_DATA['id'],
            season_year=GAME_DATA['season_year'],
            week=GAME_DATA['week'],
            guest_name=GAME_DATA['guest_id'],
            guest_score=GAME_DATA['guest_score'],
            host_name=GAME_DATA['host_id'],
            host_score=GAME_DATA['host_score'],
            is_playoff=GAME_DATA['is_playoff'],
            notes=GAME_DATA['notes']
        )

        # Act
        test_service = GameService()
        test_service.edit_game(new_game, old_game)
    
        # Assert
        verify_game_record(new_game)
        verify_team_season_record_is_none(new_game.guest_id, new_game.season_year)
        verify_team_season_record_is_none(new_game.host_id, new_game.season_year)
        verify_team_season_record_is_none(old_game.guest_id, old_game.season_year)
        verify_team_season_record_is_none(old_game.host_id, old_game.season_year)

    def test_edit_game_should_edit_game_and_guest_season_record_when_host_is_not_in_league(self):
        # Arrange
        old_game = Game(
            id=GAME_DATA['id'],
            season_year=GAME_DATA['season_year'],
            week=GAME_DATA['week'],
            guest_name=GAME_DATA['host_id'],
            guest_score=GAME_DATA['host_score'],
            host_name=GAME_DATA['guest_id'],
            host_score=GAME_DATA['guest_score'],
            is_playoff=GAME_DATA['is_playoff'],
            notes=GAME_DATA['notes']
        )
        old_game.decide_winner_and_loser()

        new_game = Game(
            id=GAME_DATA['id'],
            season_year=GAME_DATA['season_year'],
            week=GAME_DATA['week'],
            guest_name=GAME_DATA['guest_id'],
            guest_score=GAME_DATA['guest_score'],
            host_name=GAME_DATA['host_id'],
            host_score=GAME_DATA['host_score'],
            is_playoff=GAME_DATA['is_playoff'],
            notes=GAME_DATA['notes']
        )

        league_name = 'NFL'
        conference_name = 'AFC'
        division_name = 'AFC North'
        tsa = TeamSeason(
            team_name=old_game.host_id,
            season_year=old_game.season_year,
            league_name=league_name,
            conference_name=conference_name,
            division_name=division_name
        )
        add_team_season(tsa)

        test_service = GameService()
        test_service.add_game(old_game)

        # Act
        test_service.edit_game(new_game, old_game)

        # Assert
        verify_game_record(new_game)

        tsa = TeamSeason(
            team_name=new_game.guest_id,
            season_year=new_game.season_year,
            league_name=league_name,
            conference_name=conference_name,
            division_name=division_name,
            games=1,
            wins=0,
            losses=1,
            ties=0,
            winning_percentage=Decimal('0'),
            points_for=20,
            points_against=23
        )
        verify_team_season_record(old_game.guest_id, old_game.season_year, tsa)

        verify_team_season_record_is_none(old_game.host_id, old_game.season_year)

    def test_edit_game_should_edit_game_and_host_season_record_when_guest_is_not_in_league(self):
        # Arrange
        old_game = Game(
            id=GAME_DATA['id'],
            season_year=GAME_DATA['season_year'],
            week=GAME_DATA['week'],
            guest_name=GAME_DATA['host_id'],
            guest_score=GAME_DATA['host_score'],
            host_name=GAME_DATA['guest_id'],
            host_score=GAME_DATA['guest_score'],
            is_playoff=GAME_DATA['is_playoff'],
            notes=GAME_DATA['notes']
        )
        old_game.decide_winner_and_loser()

        new_game = Game(
            id=GAME_DATA['id'],
            season_year=GAME_DATA['season_year'],
            week=GAME_DATA['week'],
            guest_name=GAME_DATA['guest_id'],
            guest_score=GAME_DATA['guest_score'],
            host_name=GAME_DATA['host_id'],
            host_score=GAME_DATA['host_score'],
            is_playoff=GAME_DATA['is_playoff'],
            notes=GAME_DATA['notes']
        )

        league_name = 'NFL'
        conference_name = 'NFC'
        division_name = 'NFC West'
        tsa = TeamSeason(
            team_name=old_game.guest_id,
            season_year=old_game.season_year,
            league_name=league_name,
            conference_name=conference_name,
            division_name=division_name
        )
        add_team_season(tsa)

        test_service = GameService()
        test_service.add_game(old_game)

        # Act
        test_service.edit_game(new_game, old_game)

        # Assert
        verify_game_record(new_game)

        verify_team_season_record_is_none(old_game.guest_id, old_game.season_year)

        tsa = TeamSeason(
            team_name=new_game.host_id,
            season_year=new_game.season_year,
            league_name=league_name,
            conference_name=conference_name,
            division_name=division_name,
            games=1,
            wins=1,
            losses=0,
            ties=0,
            winning_percentage=Decimal('1'),
            points_for=23,
            points_against=20
        )
        verify_team_season_record(old_game.host_id, old_game.season_year, tsa)

    def test_edit_game_should_edit_game_and_both_team_season_records_when_both_teams_are_in_league(self):
        # Arrange
        old_game = Game(
            id=GAME_DATA['id'],
            season_year=GAME_DATA['season_year'],
            week=GAME_DATA['week'],
            guest_name=GAME_DATA['host_id'],
            guest_score=GAME_DATA['host_score'],
            host_name=GAME_DATA['guest_id'],
            host_score=GAME_DATA['guest_score'],
            is_playoff=GAME_DATA['is_playoff'],
            notes=GAME_DATA['notes']
        )
        old_game.decide_winner_and_loser()

        new_game = Game(
            id=GAME_DATA['id'],
            season_year=GAME_DATA['season_year'],
            week=GAME_DATA['week'],
            guest_name=GAME_DATA['guest_id'],
            guest_score=GAME_DATA['guest_score'],
            host_name=GAME_DATA['host_id'],
            host_score=GAME_DATA['host_score'],
            is_playoff=GAME_DATA['is_playoff'],
            notes=GAME_DATA['notes']
        )

        league_name = 'NFL'

        guest_conference_name = 'AFC'
        guest_division_name = 'AFC North'
        guest_tsa = TeamSeason(
            team_name=old_game.host_id,
            season_year=old_game.season_year,
            league_name=league_name,
            conference_name=guest_conference_name,
            division_name=guest_division_name
        )
        add_team_season(guest_tsa)

        host_conference_name = 'NFC'
        host_division_name = 'NFC West'
        host_tsa = TeamSeason(
            team_name=old_game.guest_id,
            season_year=old_game.season_year,
            league_name=league_name,
            conference_name=host_conference_name,
            division_name=host_division_name
        )
        add_team_season(host_tsa)

        test_service = GameService()
        test_service.add_game(old_game)

        # Act
        test_service.edit_game(new_game, old_game)

        # Assert
        verify_game_record(new_game)

        guest_tsa = TeamSeason(
            team_name=new_game.guest_id,
            season_year=new_game.season_year,
            league_name=league_name,
            conference_name=guest_conference_name,
            division_name=guest_division_name,
            games=1,
            wins=0,
            losses=1,
            ties=0,
            winning_percentage=Decimal('0'),
            points_for=20,
            points_against=23
        )
        verify_team_season_record(old_game.guest_id, old_game.season_year, guest_tsa)

        host_tsa = TeamSeason(
            team_name=new_game.host_id,
            season_year=new_game.season_year,
            league_name=league_name,
            conference_name=host_conference_name,
            division_name=host_division_name,
            games=1,
            wins=1,
            losses=0,
            ties=0,
            winning_percentage=Decimal('1'),
            points_for=23,
            points_against=20
        )
        verify_team_season_record(old_game.host_id, old_game.season_year, host_tsa)

    def test_delete_game_should_delete_game_and_not_edit_team_season_records_when_neither_team_is_in_league(self):
        # Arrange
        game = Game(
            id=GAME_DATA['id'],
            season_year=GAME_DATA['season_year'],
            week=GAME_DATA['week'],
            guest_name=GAME_DATA['guest_id'],
            guest_score=GAME_DATA['guest_score'],
            host_name=GAME_DATA['host_id'],
            host_score=GAME_DATA['host_score'],
            is_playoff=GAME_DATA['is_playoff'],
            notes=GAME_DATA['notes']
        )
        game.decide_winner_and_loser()
        add_game(game)

        # Act
        test_service = GameService()
        test_service.delete_game(game.id)
    
        # Assert
        verify_game_record_is_none()
        verify_team_season_record_is_none(game.guest_id, game.season_year)
        verify_team_season_record_is_none(game.host_id, game.season_year)

    def test_delete_game_should_delete_game_and_edit_guest_season_record_when_host_not_in_league(self):
        # Arrange
        game = Game(
            id=GAME_DATA['id'],
            season_year=GAME_DATA['season_year'],
            week=GAME_DATA['week'],
            guest_name=GAME_DATA['guest_id'],
            guest_score=GAME_DATA['guest_score'],
            host_name=GAME_DATA['host_id'],
            host_score=GAME_DATA['host_score'],
            is_playoff=GAME_DATA['is_playoff'],
            notes=GAME_DATA['notes']
        )
        game.decide_winner_and_loser()
        add_game(game)
        
        league_name = 'NFL'
        conference_name = 'AFC'
        division_name = 'AFC North'
        tsa = TeamSeason(
            team_name=game.guest_id,
            season_year=game.season_year,
            league_name=league_name,
            conference_name=conference_name,
            division_name=division_name,
            games=1,
            wins=0,
            losses=1,
            ties=0,
            winning_percentage=Decimal('0'),
            points_for=20,
            points_against=23
        )
        add_team_season(tsa)

        # Act
        test_service = GameService()
        test_service.delete_game(game.id)

        # Assert
        verify_game_record_is_none()
        
        tsa = TeamSeason(
            team_name=game.guest_id,
            season_year=game.season_year,
            league_name=league_name,
            conference_name=conference_name,
            division_name=division_name,
            games=0,
            wins=0,
            losses=0,
            ties=0,
            winning_percentage=None,
            points_for=0,
            points_against=0
        )
        verify_team_season_record(game.guest_id, game.season_year, tsa)

        verify_team_season_record_is_none(game.host_id, game.season_year)

    def test_delete_game_should_delete_game_and_edit_host_season_records_when_guest_not_in_league(self):
        # Arrange
        game = Game(
            id=GAME_DATA['id'],
            season_year=GAME_DATA['season_year'],
            week=GAME_DATA['week'],
            guest_name=GAME_DATA['guest_id'],
            guest_score=GAME_DATA['guest_score'],
            host_name=GAME_DATA['host_id'],
            host_score=GAME_DATA['host_score'],
            is_playoff=GAME_DATA['is_playoff'],
            notes=GAME_DATA['notes']
        )
        game.decide_winner_and_loser()
        add_game(game)

        league_name = 'NFL'
        conference_name = 'NFC'
        division_name = 'NFC West'
        tsa = TeamSeason(
            team_name=game.host_id,
            season_year=game.season_year,
            league_name=league_name,
            conference_name=conference_name,
            division_name=division_name,
            games=1,
            wins=1,
            losses=0,
            ties=0,
            winning_percentage=Decimal('1'),
            points_for=23,
            points_against=20
        )
        add_team_season(tsa)

        # Act
        test_service = GameService()
        test_service.delete_game(game.id)

        # Assert
        verify_game_record_is_none()

        verify_team_season_record_is_none(game.guest_id, game.season_year)

        tsa = TeamSeason(
            team_name=game.host_id,
            season_year=game.season_year,
            league_name=league_name,
            conference_name=conference_name,
            division_name=division_name,
            games=0,
            wins=0,
            losses=0,
            ties=0,
            winning_percentage=None,
            points_for=0,
            points_against=0
        )
        verify_team_season_record(game.host_id, game.season_year, tsa)

    def test_delete_game_should_delete_game_and_edit_both_season_records_when_both_teams_in_league(self):
        # Arrange
        game = Game(
            id=GAME_DATA['id'],
            season_year=GAME_DATA['season_year'],
            week=GAME_DATA['week'],
            guest_name=GAME_DATA['guest_id'],
            guest_score=GAME_DATA['guest_score'],
            host_name=GAME_DATA['host_id'],
            host_score=GAME_DATA['host_score'],
            is_playoff=GAME_DATA['is_playoff'],
            notes=GAME_DATA['notes']
        )
        game.decide_winner_and_loser()
        add_game(game)

        league_name = 'NFL'
        guest_conference_name = 'AFC'
        guest_division_name = 'AFC North'
        guest_tsa = TeamSeason(
            team_name=game.guest_id,
            season_year=game.season_year,
            league_name=league_name,
            conference_name=guest_conference_name,
            division_name=guest_division_name,
            games=1,
            wins=0,
            losses=1,
            ties=0,
            winning_percentage=Decimal('0'),
            points_for=20,
            points_against=23
        )
        add_team_season(guest_tsa)

        host_conference_name = 'NFC'
        host_division_name = 'NFC West'
        host_tsa = TeamSeason(
            team_name=game.host_id,
            season_year=game.season_year,
            league_name=league_name,
            conference_name=host_conference_name,
            division_name=host_division_name,
            games=1,
            wins=1,
            losses=0,
            ties=0,
            winning_percentage=Decimal('1'),
            points_for=23,
            points_against=20
        )
        add_team_season(host_tsa)

        # Act
        test_service = GameService()
        test_service.delete_game(game.id)

        # Assert
        verify_game_record_is_none()

        guest_tsa = TeamSeason(
            team_name=game.guest_id,
            season_year=game.season_year,
            league_name=league_name,
            conference_name=guest_conference_name,
            division_name=guest_division_name,
            games=0,
            wins=0,
            losses=0,
            ties=0,
            winning_percentage=None,
            points_for=0,
            points_against=0
        )
        verify_team_season_record(game.guest_id, game.season_year, guest_tsa)

        host_tsa = TeamSeason(
            team_name=game.host_id,
            season_year=game.season_year,
            league_name=league_name,
            conference_name=host_conference_name,
            division_name=host_division_name,
            games=0,
            wins=0,
            losses=0,
            ties=0,
            winning_percentage=None,
            points_for=0,
            points_against=0
        )
        verify_team_season_record(game.host_id, game.season_year, host_tsa)


def set_up_database():
    set_up_seasons_table()
    set_up_leagues_table()
    set_up_conferences_table()
    set_up_divisions_table()
    set_up_teams_table()
    set_up_league_seasons_table()


def add_game(game: Game) -> None:
    connection = engine.connect()
    transaction = connection.begin()
    try:
        statement = f"""
            INSERT INTO pro_football.games(
                id, season_year, week,
                guest_id, guest_score, host_id, host_score,
                winner_name, winner_score, loser_name, loser_score,
                is_playoff, notes
            )
            VALUES(
                {game.id}, {game.season_year}, {game.week},
                '{game.guest_id}', {game.guest_score}, '{game.host_id}', {game.host_score},
                '{game.winner_id}', {game.winner_score}, '{game.loser_id}', {game.loser_score},
                {game.is_playoff}, '{game.notes}'
            );
        """
        connection.execute(statement)
        transaction.commit()
    except:
        transaction.rollback()
        raise


def add_team_season(team_season: TeamSeason) -> None:
    connection = engine.connect()
    transaction = connection.begin()
    try:
        statement = f"""
            INSERT INTO pro_football.team_seasons(
                team_name, season_year, league_name, conference_name, division_name,
                games, wins, losses, ties, winning_percentage, points_for, points_against
            )
        """
        if team_season.winning_percentage is None:
            statement += f"""
                VALUES(
                    '{team_season.team_name}',
                    {team_season.season_year},
                    '{team_season.league_name}',
                    '{team_season.conference_name}',
                    '{team_season.division_name}',
                    {team_season.games},
                    {team_season.wins},
                    {team_season.losses},
                    {team_season.ties},
                    NULL,
                    {team_season.points_for},
                    {team_season.points_against}
                );
            """
        else:
            statement += f"""
                VALUES(
                    '{team_season.team_name}',
                    {team_season.season_year},
                    '{team_season.league_name}',
                    '{team_season.conference_name}',
                    '{team_season.division_name}',
                    {team_season.games},
                    {team_season.wins},
                    {team_season.losses},
                    {team_season.ties},
                    {team_season.winning_percentage},
                    {team_season.points_for},
                    {team_season.points_against}
                );
            """
        connection.execute(statement)
        transaction.commit()
    except:
        transaction.rollback()
        raise


def verify_game_record(game: Game) -> None:
    with engine.connect() as connection:
        statement = f"""
            SELECT *
            FROM pro_football.games;
        """
        game_record = connection.execute(statement).first()

    assert game_record is not None
    
    game_id = game_record[0]
    assert game_id == game.id

    game_season_year = game_record[1]
    assert game_season_year == game.season_year

    game_week = game_record[2]
    assert game_week == game.week

    game_guest_name = game_record[3]
    assert game_guest_name == game.guest_id

    game_guest_score = game_record[4]
    assert game_guest_score == game.guest_score

    game_host_name = game_record[5]
    assert game_host_name == game.host_id

    game_host_score = game_record[6]
    assert game_host_score == game.host_score

    game_winner_name = game_record[7]
    assert game_winner_name == game.winner_id

    game_winner_score = game_record[8]
    assert game_winner_score == game.winner_score

    game_loser_name = game_record[9]
    assert game_loser_name == game.loser_id

    game_loser_score = game_record[10]
    assert game_loser_score == game.loser_score

    game_is_playoff = game_record[11]
    assert game_is_playoff == game.is_playoff

    game_notes = game_record[12]
    assert game_notes == game.notes


def verify_game_record_is_none() -> None:
    with engine.connect() as connection:
        statement = f"""
            SELECT *
            FROM pro_football.games;
        """
        game_record = connection.execute(statement).first()

    assert game_record is None


def verify_team_season_record(team_name: str, season_year: int, tsa: TeamSeason) -> None:
    with engine.connect() as connection:
        statement = f"""
            SELECT *
            FROM pro_football.team_seasons
            WHERE
                team_name = '{team_name}'
                AND season_year = {season_year};
        """
        tsa_record = connection.execute(statement).first()

    assert tsa_record is not None

    tsa_name = tsa_record[1]
    assert tsa_name == tsa.team_name

    tsa_season_year = tsa_record[2]
    assert tsa_season_year == tsa.season_year

    tsa_league_name = tsa_record[3]
    assert tsa_league_name == tsa.league_name

    tsa_conference_name = tsa_record[4]
    assert tsa_conference_name == tsa.conference_name

    tsa_division_name = tsa_record[5]
    assert tsa_division_name == tsa.division_name

    tsa_games = tsa_record[6]
    assert tsa_games == tsa.games

    tsa_wins = tsa_record[7]
    assert tsa_wins == tsa.wins

    tsa_losses = tsa_record[8]
    assert tsa_losses == tsa.losses

    tsa_ties = tsa_record[9]
    assert tsa_ties == tsa.ties

    tsa_winning_percentage = tsa_record[10]
    assert tsa_winning_percentage == tsa.winning_percentage

    tsa_points_for = tsa_record[11]
    assert tsa_points_for == tsa.points_for

    tsa_points_against = tsa_record[12]
    assert tsa_points_against == tsa.points_against


def verify_team_season_record_is_none(team_name: str, season_year: int) -> None:
    with engine.connect() as connection:
        statement = f"""
            SELECT *
            FROM pro_football.team_seasons
            WHERE
                team_name = '{team_name}'
                AND season_year = {season_year};
        """
        tsa_record = connection.execute(statement).first()
        assert tsa_record is None
