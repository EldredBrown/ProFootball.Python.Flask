import pytest

from unittest.mock import patch, call

from app.data.models.season import Season
from app.data.models.league import League
from app.data.models.game import Game
from app.data.models.league_season import LeagueSeason
from app.data.models.team_season import TeamSeason
from app.data.repositories.league_repository import LeagueRepository
from test_app import create_app


@patch('app.data.repositories.league_repository.League')
def test_get_leagues_should_get_leagues(fake_league):
    # Act
    test_app = create_app()
    with test_app.app_context():
        test_repo = LeagueRepository()
        leagues = test_repo.get_leagues()

    # Assert
    fake_league.query.all.assert_called_once()
    assert leagues == fake_league.query.all.return_value


@patch('app.data.repositories.league_repository.LeagueRepository.get_leagues')
def test_get_league_when_leagues_is_empty_should_return_none(fake_get_leagues):
    test_app = create_app()
    with test_app.app_context():
        # Arrange
        leagues = []
        fake_get_leagues.return_value = leagues

        # Act
        test_repo = LeagueRepository()
        league = test_repo.get_league(id=1)

    # Assert
    assert league is None


@patch('app.data.repositories.league_repository.League')
@patch('app.data.repositories.league_repository.LeagueRepository.get_leagues')
def test_get_league_when_leagues_is_not_empty_and_league_is_not_found_should_return_none(fake_get_leagues, fake_league):
    test_app = create_app()
    with test_app.app_context():
        # Arrange
        leagues = [
            League(short_name='A', long_name='A', first_season_year=1, last_season_year=2),
            League(short_name='B', long_name='B', first_season_year=3, last_season_year=4),
            League(short_name='C', long_name='C', first_season_year=5, last_season_year=None),
        ]
        fake_get_leagues.return_value = leagues

        id = len(leagues) + 1

        # Act
        test_repo = LeagueRepository()
        league = test_repo.get_league(id=id)

    # Assert
    fake_league.query.get.assert_called_once_with(id)
    assert league == fake_league.query.get.return_value


@patch('app.data.repositories.league_repository.League')
@patch('app.data.repositories.league_repository.LeagueRepository.get_leagues')
def test_get_league_when_leagues_is_not_empty_and_league_is_found_should_return_league(fake_get_leagues, fake_league):
    test_app = create_app()
    with test_app.app_context():
        # Arrange
        leagues = [
            League(short_name='A', long_name='A', first_season_year=1, last_season_year=2),
            League(short_name='B', long_name='B', first_season_year=3, last_season_year=4),
            League(short_name='C', long_name='C', first_season_year=5, last_season_year=None),
        ]
        fake_get_leagues.return_value = leagues

        id = len(leagues) - 1

        # Act
        test_repo = LeagueRepository()
        league = test_repo.get_league(id=id)

    # Assert
    fake_league.query.get.assert_called_once_with(id)
    assert league == fake_league.query.get.return_value


@patch('app.data.repositories.league_repository.LeagueRepository.get_leagues')
def test_get_league_by_name_when_leagues_is_empty_should_return_none(fake_get_leagues):
    test_app = create_app()
    with test_app.app_context():
        # Arrange
        leagues = []
        fake_get_leagues.return_value = leagues

        # Act
        test_repo = LeagueRepository()
        league = test_repo.get_league_by_name(short_name="A")

    # Assert
    assert league is None


@patch('app.data.repositories.league_repository.League')
@patch('app.data.repositories.league_repository.LeagueRepository.get_leagues')
def test_get_league_by_name_when_leagues_is_not_empty_and_league_with_short_name_is_not_found_should_return_none(
        fake_get_leagues, fake_league
):
    test_app = create_app()
    with test_app.app_context():
        # Arrange
        leagues = [
            League(short_name='A', long_name='A', first_season_year=1, last_season_year=2),
            League(short_name='B', long_name='B', first_season_year=3, last_season_year=4),
            League(short_name='C', long_name='C', first_season_year=5, last_season_year=None),
        ]
        fake_get_leagues.return_value = leagues

        # Act
        test_repo = LeagueRepository()
        league = test_repo.get_league_by_name(short_name="D")

    # Assert
    fake_league.query.filter_by.assert_called_once_with(short_name="D")
    fake_league.query.filter_by.return_value.first.assert_called_once_with()
    assert league == fake_league.query.filter_by.return_value.first.return_value


@patch('app.data.repositories.league_repository.League')
@patch('app.data.repositories.league_repository.LeagueRepository.get_leagues')
def test_get_league_by_name_when_leagues_is_not_empty_and_league_with_short_name_is_found_should_return_league(
        fake_get_leagues, fake_league
):
    test_app = create_app()
    with test_app.app_context():
        # Arrange
        leagues = [
            League(short_name='A', long_name='A', first_season_year=1, last_season_year=2),
            League(short_name='B', long_name='B', first_season_year=3, last_season_year=4),
            League(short_name='C', long_name='C', first_season_year=5, last_season_year=None),
        ]
        fake_get_leagues.return_value = leagues

        # Act
        test_repo = LeagueRepository()
        league = test_repo.get_league_by_name(short_name="B")

    # Assert
    fake_league.query.filter_by.assert_called_once_with(short_name="B")
    fake_league.query.filter_by.return_value.first.assert_called_once_with()
    assert league == fake_league.query.filter_by.return_value.first.return_value


@patch('app.data.repositories.league_repository.sqla')
def test_add_league_should_add_league(fake_sqla):
    # Arrange
    test_app = create_app()
    with test_app.app_context():
        # Act
        test_repo = LeagueRepository()
        league_in = League(
            short_name="AAFC", long_name="All-American Football League", first_season_year=1946, last_season_year=1949
        )
        league_out = test_repo.add_league(league_in)

    # Assert
    fake_sqla.session.add.assert_called_once_with(league_in)
    fake_sqla.session.commit.assert_called_once()
    assert league_out is league_in


@patch('app.data.repositories.league_repository.sqla')
def test_add_leagues_when_leagues_arg_is_empty_should_add_no_leagues(fake_sqla):
    # Arrange
    test_app = create_app()
    with test_app.app_context():
        # Act
        test_repo = LeagueRepository()
        leagues_in = ()
        leagues_out = test_repo.add_leagues(leagues_in)

    # Assert
    fake_sqla.session.add.assert_not_called()
    fake_sqla.session.commit.assert_called_once()
    assert leagues_out is leagues_in


@patch('app.data.repositories.league_repository.sqla')
def test_add_leagues_when_leagues_arg_is_not_empty_should_add_leagues(fake_sqla):
    # Arrange
    test_app = create_app()
    with test_app.app_context():
        # Act
        test_repo = LeagueRepository()
        leagues_in = (
            League(short_name="D", long_name="D", first_season_year=7, last_season_year=8),
            League(short_name="E", long_name="E", first_season_year=9, last_season_year=10),
            League(short_name="F", long_name="F", first_season_year=11, last_season_year=12),
        )
        leagues_out = test_repo.add_leagues(leagues_in)

    # Assert
    fake_sqla.session.add.assert_has_calls([
        call(leagues_in[0]),
        call(leagues_in[1]),
        call(leagues_in[2]),
    ])
    fake_sqla.session.commit.assert_called_once()
    assert leagues_out is leagues_in


@patch('app.data.repositories.league_repository.sqla')
@patch('app.data.repositories.league_repository.exists')
def test_league_exists_should_query_database(fake_exists, fake_sqla):
    # Arrange
    test_app = create_app()
    with test_app.app_context():
        # Act
        test_repo = LeagueRepository()
        league_exists = test_repo.league_exists(id=1)

    # Assert
    fake_exists.assert_called_once()
    fake_exists.return_value.where.assert_called_once()
    fake_sqla.session.query.assert_called_once_with(fake_exists.return_value.where.return_value)
    fake_sqla.session.query.return_value.scalar.assert_called_once()
    assert league_exists == fake_sqla.session.query.return_value.scalar.return_value


@patch('app.data.repositories.league_repository.LeagueRepository.league_exists')
def test_update_league_when_league_does_not_exist_should_return_league(fake_league_exists):
    # Arrange
    fake_league_exists.return_value = False

    test_app = create_app()
    with test_app.app_context():
        # Act
        test_repo = LeagueRepository()
        league_to_update = League(
            id=1, short_name="B", long_name="B", first_season_year=98, last_season_year=99
        )
        league_updated = test_repo.update_league(league_to_update)

    # Assert
    fake_league_exists.assert_called_once_with(league_to_update.id)
    assert league_updated is league_to_update


@patch('app.data.repositories.league_repository.sqla')
@patch('app.data.repositories.league_repository.LeagueRepository.get_league')
@patch('app.data.repositories.league_repository.LeagueRepository.league_exists')
def test_update_league_when_league_exists_should_update_and_return_league(
        fake_league_exists, fake_get_league, fake_sqla
):
    # Arrange
    test_app = create_app()
    with test_app.app_context():
        fake_league_exists.return_value = True
        old_league = League(
            id=1, short_name="A", long_name="A", first_season_year=1, last_season_year=2
        )
        fake_get_league.return_value = old_league

        new_league = League(
            id=1, short_name="Z", long_name="Z", first_season_year=98, last_season_year=99
        )

        # Act
        test_repo = LeagueRepository()
        league_updated = test_repo.update_league(new_league)

    # Assert
    fake_league_exists.assert_called_once_with(old_league.id)
    fake_get_league.assert_called_once_with(old_league.id)
    assert league_updated.short_name == new_league.short_name
    assert league_updated.long_name == new_league.long_name
    assert league_updated.first_season_year == new_league.first_season_year
    assert league_updated.last_season_year == new_league.last_season_year
    fake_sqla.session.add.assert_called_once_with(old_league)
    fake_sqla.session.commit.assert_called_once()
    assert league_updated is new_league


@patch('app.data.repositories.league_repository.LeagueRepository.league_exists')
def test_delete_league_when_league_does_not_exist_should_return_none(fake_league_exists):
    # Arrange
    fake_league_exists.return_value = False
    id = 1

    test_app = create_app()
    with test_app.app_context():
        # Act
        test_repo = LeagueRepository()
        league_deleted = test_repo.delete_league(id=id)

    # Assert
    fake_league_exists.assert_called_once_with(id)
    assert league_deleted is None


@patch('app.data.repositories.league_repository.sqla')
@patch('app.data.repositories.league_repository.LeagueRepository.get_league')
@patch('app.data.repositories.league_repository.LeagueRepository.league_exists')
def test_delete_league_when_league_exists_should_return_league(fake_league_exists, fake_get_league, fake_sqla):
    # Arrange
    fake_league_exists.return_value = True
    id = 1

    test_app = create_app()
    with test_app.app_context():
        # Act
        test_repo = LeagueRepository()
        league_deleted = test_repo.delete_league(id=id)

    # Assert
    fake_league_exists.assert_called_once_with(id)
    fake_get_league.assert_called_once_with(id)
    fake_sqla.session.delete.assert_called_once_with(fake_get_league.return_value)
    fake_sqla.session.commit.assert_called_once()
    return league_deleted is fake_get_league.return_value
