from unittest.mock import patch, call

import pytest
from sqlalchemy.exc import IntegrityError

from test_app import create_app

from app.data.models.season import Season
from app.data.models.league import League
from app.data.models.game import Game
from app.data.models.league_season import LeagueSeason
from app.data.models.team_season import TeamSeason
from app.data.repositories.league_repository import LeagueRepository


@pytest.fixture
def test_app():
    return create_app()


@patch('app.data.repositories.league_repository.League')
def test_get_leagues_should_get_leagues(fake_league, test_app):
    with test_app.app_context():
        # Arrange
        leagues_in = [
            League(short_name="NFL"),
            League(short_name="AFL"),
            League(short_name="AAFC"),
        ]
        fake_league.query.all.return_value = leagues_in

        # Act
        test_repo = LeagueRepository()
        leagues_out = test_repo.get_leagues()

    # Assert
    assert leagues_out == leagues_in


@patch('app.data.repositories.league_repository.League')
def test_get_league_when_leagues_is_empty_should_return_none(fake_league, test_app):
    with test_app.app_context():
        # Arrange
        leagues_in = []
        fake_league.query.all.return_value = leagues_in

        # Act
        test_repo = LeagueRepository()
        league_out = test_repo.get_league(1)

    # Assert
    assert league_out is None


@patch('app.data.repositories.league_repository.League')
def test_get_league_when_leagues_is_not_empty_and_league_is_not_found_should_return_none(fake_league, test_app):
    with test_app.app_context():
        # Arrange
        leagues_in = [
            League(short_name="NFL"),
            League(short_name="AFL"),
            League(short_name="AAFC"),
        ]
        fake_league.query.all.return_value = leagues_in
        fake_league.query.get.return_value = None

        # Act
        test_repo = LeagueRepository()

        id = len(leagues_in) + 1
        league_out = test_repo.get_league(id)

    # Assert
    assert league_out is None


@patch('app.data.repositories.league_repository.League')
def test_get_league_when_leagues_is_not_empty_and_league_is_found_should_return_league(fake_league, test_app):
    with test_app.app_context():
        # Arrange
        leagues_in = [
            League(short_name="NFL"),
            League(short_name="AFL"),
            League(short_name="AAFC"),
        ]
        fake_league.query.all.return_value = leagues_in

        id = len(leagues_in) - 1
        fake_league.query.get.return_value = leagues_in[id]

        # Act
        test_repo = LeagueRepository()

        league_out = test_repo.get_league(id)

    # Assert
    assert league_out is leagues_in[id]


@patch('app.data.repositories.league_repository.League')
def test_get_league_by_name_when_leagues_is_empty_should_return_none(fake_league, test_app):
    with test_app.app_context():
        # Arrange
        leagues_in = []
        fake_league.query.all.return_value = leagues_in

        # Act
        test_repo = LeagueRepository()
        league_out = test_repo.get_league_by_name("NFL")

    # Assert
    assert league_out is None


@patch('app.data.repositories.league_repository.League')
def test_get_league_by_name_when_leagues_is_not_empty_and_league_with_short_name_is_not_found_should_return_none(
        fake_league, test_app
):
    with test_app.app_context():
        # Arrange
        leagues_in = [
            League(short_name="NFL"),
            League(short_name="AFL"),
            League(short_name="AAFC"),
        ]
        fake_league.query.all.return_value = leagues_in
        fake_league.query.filter_by.return_value.first.return_value = None

        # Act
        test_repo = LeagueRepository()
        league_out = test_repo.get_league_by_name("USFL")

    # Assert
    assert league_out is None


@patch('app.data.repositories.league_repository.League')
def test_get_league_by_year_when_leagues_is_not_empty_and_league_with_year_is_found_should_return_league(
        fake_league, test_app
):
    with test_app.app_context():
        # Arrange
        leagues_in = [
            League(short_name="NFL"),
            League(short_name="AFL"),
            League(short_name="AAFC"),
        ]
        fake_league.query.all.return_value = leagues_in
        fake_league.query.filter_by.return_value.first.return_value = leagues_in[-1]

        # Act
        test_repo = LeagueRepository()
        league_out = test_repo.get_league_by_name("AAFC")

    # Assert
    assert league_out is leagues_in[-1]


@patch('app.data.repositories.league_repository.sqla')
@patch('app.data.repositories.league_repository.league_factory')
def test_add_league_when_no_integrity_error_caught_should_add_league(fake_league_factory, fake_sqla, test_app):
    with test_app.app_context():
        # Arrange
        league_in = League(short_name="NFL")
        fake_league_factory.create_league.return_value = league_in

        # Act
        test_repo = LeagueRepository()
        kwargs = {
            'short_name': "NFL",
        }
        league_out = test_repo.add_league(**kwargs)

    # Assert
    fake_sqla.session.add.assert_called_once_with(league_in)
    fake_sqla.session.commit.assert_called_once()
    assert league_out is league_in


@patch('app.data.repositories.league_repository.sqla')
@patch('app.data.repositories.league_repository.league_factory')
def test_add_league_when_integrity_error_caught_should_rollback_transaction_and_reraise_error(
        fake_league_factory, fake_sqla, test_app
):
    with test_app.app_context():
        # Arrange
        league_in = League(short_name="NFL")
        fake_league_factory.create_league.return_value = league_in
        fake_sqla.session.commit.side_effect = IntegrityError('statement', 'params', Exception())

        # Act
        test_repo = LeagueRepository()
        kwargs = {
            'short_name': "NFL",
        }
        with pytest.raises(IntegrityError):
            league_out = test_repo.add_league(**kwargs)

    # Assert
    fake_sqla.session.rollback.assert_called_once()


@patch('app.data.repositories.league_repository.sqla')
def test_add_leagues_when_leagues_arg_is_empty_should_add_no_leagues(fake_sqla, test_app):
    # Arrange
    with test_app.app_context():
        # Act
        test_repo = LeagueRepository()

        league_args = ()
        leagues_out = test_repo.add_leagues(league_args)

    # Assert
    fake_sqla.session.add.assert_not_called()
    fake_sqla.session.commit.assert_called_once()
    assert leagues_out == []


@patch('app.data.repositories.league_repository.sqla')
@patch('app.data.repositories.league_repository.league_factory')
def test_add_leagues_when_leagues_arg_is_not_empty_should_add_leagues(fake_league_factory, fake_sqla, test_app):
    with test_app.app_context():
        # Arrange
        leagues_in = [
            League(short_name="NFL"),
            League(short_name="AFL"),
            League(short_name="AAFC"),
        ]
        fake_league_factory.create_league.side_effect = leagues_in

        # Act
        test_repo = LeagueRepository()

        league_args = (
            {'short_name': "NFL"},
            {'short_name': "AFL"},
            {'short_name': "AAFC"},
        )
        leagues_out = test_repo.add_leagues(league_args)

    # Assert
    fake_sqla.session.add.assert_has_calls([
        call(leagues_in[0]),
        call(leagues_in[1]),
        call(leagues_in[2]),
    ])
    fake_sqla.session.commit.assert_called_once()
    assert leagues_out == leagues_in


@patch('app.data.repositories.league_repository.sqla')
@patch('app.data.repositories.league_repository.league_factory')
def test_add_leagues_when_leagues_arg_is_not_empty_and_no_integrity_error_caught_should_add_leagues(
        fake_league_factory, fake_sqla, test_app
):
    with test_app.app_context():
        # Arrange
        leagues_in = [
            League(short_name="NFL"),
            League(short_name="AFL"),
            League(short_name="AAFC"),
        ]
        fake_league_factory.create_league.side_effect = leagues_in

        # Act
        test_repo = LeagueRepository()

        league_args = (
            {'short_name': "NFL"},
            {'short_name': "AFL"},
            {'short_name': "AAFC"},
        )
        leagues_out = test_repo.add_leagues(league_args)

    # Assert
    fake_sqla.session.add.assert_has_calls([
        call(leagues_in[0]),
        call(leagues_in[1]),
        call(leagues_in[2]),
    ])
    fake_sqla.session.commit.assert_called_once()
    assert leagues_out == leagues_in


@patch('app.data.repositories.league_repository.sqla')
@patch('app.data.repositories.league_repository.league_factory')
def test_add_leagues_when_leagues_arg_is_not_empty_and_integrity_error_caught_should_rollback_transaction_and_reraise_error(
        fake_league_factory, fake_sqla, test_app
):
    with test_app.app_context():
        # Arrange
        leagues_in = [
            League(short_name="NFL"),
            League(short_name="AFL"),
            League(short_name="AAFC"),
        ]
        fake_league_factory.create_league.side_effect = leagues_in
        fake_sqla.session.commit.side_effect = IntegrityError('statement', 'params', Exception())

        # Act
        test_repo = LeagueRepository()

        league_args = (
            {'short_name': "NFL"},
            {'short_name': "AFL"},
            {'short_name': "AAFC"},
        )
        with pytest.raises(IntegrityError):
            leagues_out = test_repo.add_leagues(league_args)

    # Assert
    fake_sqla.session.rollback.assert_called_once()


@patch('app.data.repositories.league_repository.League')
def test_league_exists_when_league_does_not_exist_should_return_false(fake_league, test_app):
    with test_app.app_context():
        # Arrange
        leagues_in = [
            League(short_name="NFL"),
            League(short_name="AFL"),
            League(short_name="AAFC"),
        ]
        fake_league.query.all.return_value = leagues_in
        fake_league.query.get.return_value = None

        # Act
        test_repo = LeagueRepository()
        league_exists = test_repo.league_exists(id=1)

    # Assert
    assert not league_exists


@patch('app.data.repositories.league_repository.League')
def test_league_exists_when_league_exists_should_return_true(fake_league, test_app):
    with test_app.app_context():
        # Arrange
        leagues_in = [
            League(short_name="NFL"),
            League(short_name="AFL"),
            League(short_name="AAFC"),
        ]
        fake_league.query.all.return_value = leagues_in
        fake_league.query.get.return_value = leagues_in[1]

        # Act
        test_repo = LeagueRepository()
        league_exists = test_repo.league_exists(id=1)

    # Assert
    assert league_exists


def test_update_league_when_id_not_in_kwargs_should_raise_value_error(test_app):
    # Arrange
    with test_app.app_context():
        # Act
        test_repo = LeagueRepository()
        kwargs = {
            'short_name': "NFL",
            'long_name': "National Football League",
            'first_season_year': 1922,
            'last_season_year': None,
        }
        with pytest.raises(ValueError) as err:
            league_updated = test_repo.update_league(**kwargs)

    # Assert
    assert err.value.args[0] == "ID must be provided for existing League."


@patch('app.data.repositories.league_repository.sqla')
@patch('app.data.repositories.league_repository.LeagueRepository.league_exists')
def test_update_league_when_id_is_in_kwargs_and_no_league_exists_with_id_should_return_league_and_not_update_database(
        fake_league_exists, fake_sqla, test_app
):
    with test_app.app_context():
        # Arrange
        fake_league_exists.return_value = False

        # Act
        test_repo = LeagueRepository()
        kwargs = {
            'id': 1,
            'short_name': "NFL",
            'long_name': "National Football League",
            'first_season_year': 1922,
            'last_season_year': None,
        }
        try:
            league_updated = test_repo.update_league(**kwargs)
        except ValueError as err:
            assert False

    # Assert
    fake_sqla.session.add.assert_not_called()
    fake_sqla.session.commit.assert_not_called()
    assert isinstance(league_updated, League)
    assert league_updated.id == 1
    assert league_updated.short_name == "NFL"
    assert league_updated.long_name == "National Football League"
    assert league_updated.first_season_year == 1922
    assert league_updated.last_season_year == None


@patch('app.data.repositories.league_repository.sqla')
@patch('app.data.repositories.league_repository.league_factory')
@patch('app.data.repositories.league_repository.League')
@patch('app.data.repositories.league_repository.LeagueRepository.league_exists')
def test_update_league_when_id_is_in_kwargs_and_league_exists_with_id_and_no_integrity_error_caught_should_return_league_and_update_database(
        fake_league_exists, fake_league, fake_league_factory, fake_sqla, test_app
):
    with test_app.app_context():
        # Arrange
        fake_league_exists.return_value = True

        leagues = [
            League(
                id=1, short_name="NFL", long_name="National Football League", first_season_year=1922, last_season_year=None
            ),
            League(
                id=2, short_name="AFL", long_name="American Football League", first_season_year=1960, last_season_year=1969
            ),
            League(
                id=3, short_name="AAFC", long_name="All-American Football Conference",
                first_season_year=1946, last_season_year=1949
            ),
        ]
        fake_league.query.all.return_value = leagues

        old_league = leagues[1]
        fake_league.query.get.return_value = old_league

        new_league = League(
            id=2, short_name="USFL", long_name="United States Football League",
            first_season_year=1983, last_season_year=1987
        )
        fake_league_factory.create_league.return_value = new_league

        # Act
        test_repo = LeagueRepository()
        kwargs = {
            'id': 2,
            'short_name': "USFL",
            'long_name': "United States Football League",
            'first_season_year': 1983,
            'last_season_year': 1987,
        }
        try:
            league_updated = test_repo.update_league(**kwargs)
        except ValueError as err:
            assert False

    # Assert
    fake_sqla.session.add.assert_called_once_with(old_league)
    fake_sqla.session.commit.assert_called_once()
    assert isinstance(league_updated, League)
    assert league_updated.id == 2
    assert league_updated.short_name == "USFL"
    assert league_updated.long_name == "United States Football League"
    assert league_updated.first_season_year == 1983
    assert league_updated.last_season_year == 1987
    assert league_updated is new_league


@patch('app.data.repositories.league_repository.sqla')
@patch('app.data.repositories.league_repository.league_factory')
@patch('app.data.repositories.league_repository.League')
@patch('app.data.repositories.league_repository.LeagueRepository.league_exists')
def test_update_league_when_id_is_in_kwargs_and_league_exists_with_id_and_integrity_error_caught_should_rollback_transaction_and_reraise_error(
        fake_league_exists, fake_league, fake_league_factory, fake_sqla, test_app
):
    with test_app.app_context():
        # Arrange
        fake_league_exists.return_value = True

        leagues = [
            League(
                id=1, short_name="NFL", long_name="National Football League", first_season_year=1922, last_season_year=None
            ),
            League(
                id=2, short_name="AFL", long_name="American Football League", first_season_year=1960, last_season_year=1969
            ),
            League(
                id=3, short_name="AAFC", long_name="All-American Football Conference",
                first_season_year=1946, last_season_year=1949
            ),
        ]
        fake_league.query.all.return_value = leagues

        old_league = leagues[1]
        fake_league.query.get.return_value = old_league

        new_league = League(
            id=2, short_name="USFL", long_name="United States Football League",
            first_season_year=1983, last_season_year=1987
        )
        fake_league_factory.create_league.return_value = new_league

        fake_sqla.session.commit.side_effect = IntegrityError('statement', 'params', Exception())

        # Act
        test_repo = LeagueRepository()
        kwargs = {
            'id': 2,
            'short_name': "USFL",
            'long_name': "United States Football League",
            'first_season_year': 1983,
            'last_season_year': 1987,
        }
        with pytest.raises(IntegrityError):
            league_updated = test_repo.update_league(**kwargs)

    # Assert
    fake_sqla.session.rollback.assert_called_once()


@patch('app.data.repositories.league_repository.sqla')
@patch('app.data.repositories.league_repository.League')
def test_delete_league_when_league_does_not_exist_should_return_none_and_not_delete_league_from_database(
        fake_league, fake_sqla, test_app
):
    with test_app.app_context():
        # Arrange
        leagues_in = [
            League(short_name="NFL"),
            League(short_name="AFL"),
            League(short_name="AAFC"),
        ]
        fake_league.query.all.return_value = leagues_in
        fake_league.query.get.return_value = None

        id = 1

        # Act
        test_repo = LeagueRepository()
        league_deleted = test_repo.delete_league(id)

    # Assert
    assert league_deleted is None
    fake_sqla.session.delete.assert_not_called()
    fake_sqla.session.commit.assert_not_called()


@patch('app.data.repositories.league_repository.sqla')
@patch('app.data.repositories.league_repository.League')
def test_delete_league_when_league_exists_should_return_league_and_delete_league_from_database(
        fake_league, fake_sqla, test_app
):
    with test_app.app_context():
        # Arrange
        leagues_in = [
            League(short_name="NFL"),
            League(short_name="AFL"),
            League(short_name="AAFC"),
        ]
        fake_league.query.all.return_value = leagues_in

        id = 1
        fake_league.query.get.return_value = leagues_in[id]

        # Act
        test_repo = LeagueRepository()
        league_deleted = test_repo.delete_league(id)

    # Assert
    fake_sqla.session.delete.assert_called_once_with(league_deleted)
    fake_sqla.session.commit.assert_called_once()
    assert league_deleted is leagues_in[id]
