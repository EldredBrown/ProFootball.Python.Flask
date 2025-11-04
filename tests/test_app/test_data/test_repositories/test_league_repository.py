from unittest.mock import patch, call

import pytest

from sqlalchemy.exc import IntegrityError

from test_app import create_app

from app.data.models.league import League
from app.data.repositories.league_repository import LeagueRepository


@pytest.fixture
def test_repo():
    return LeagueRepository()


@patch('app.data.repositories.league_repository.League')
def test_get_leagues_should_get_leagues(fake_league, test_repo):
    # Arrange
    leagues_in = [
        League(
            short_name="C1",
            long_name="League 1",
            first_season_year=1
        ),
        League(
            short_name="C2",
            long_name="League 2",
            first_season_year=2
        ),
        League(
            short_name="C3",
            long_name="League 3",
            first_season_year=3
        ),
    ]
    fake_league.query.all.return_value = leagues_in

    # Act
    leagues_out = test_repo.get_leagues()

    # Assert
    assert leagues_out == leagues_in


@patch('app.data.repositories.league_repository.League')
def test_get_league_when_leagues_is_empty_should_return_none(fake_league, test_repo):
    # Arrange
    leagues_in = []
    fake_league.query.all.return_value = leagues_in

    # Act
    league_out = test_repo.get_league(1)

    # Assert
    assert league_out is None


@patch('app.data.repositories.league_repository.League')
def test_get_league_when_leagues_is_not_empty_and_league_is_not_found_should_return_none(fake_league, test_repo):
    # Arrange
    leagues_in = [
        League(
            short_name="C1",
            long_name="League 1",
            first_season_year=1
        ),
        League(
            short_name="C2",
            long_name="League 2",
            first_season_year=2
        ),
        League(
            short_name="C3",
            long_name="League 3",
            first_season_year=3
        ),
    ]
    fake_league.query.all.return_value = leagues_in
    fake_league.query.get.return_value = None

    # Act
    id = len(leagues_in) + 1
    league_out = test_repo.get_league(id)

    # Assert
    assert league_out is None


@patch('app.data.repositories.league_repository.League')
def test_get_league_when_leagues_is_not_empty_and_league_is_found_should_return_league(fake_league, test_repo):
    # Arrange
    leagues_in = [
        League(
            short_name="C1",
            long_name="League 1",
            first_season_year=1
        ),
        League(
            short_name="C2",
            long_name="League 2",
            first_season_year=2
        ),
        League(
            short_name="C3",
            long_name="League 3",
            first_season_year=3
        ),
    ]
    fake_league.query.all.return_value = leagues_in

    id = len(leagues_in) - 1
    fake_league.query.get.return_value = leagues_in[id]

    # Act
    league_out = test_repo.get_league(id)

    # Assert
    assert league_out is leagues_in[id]


@patch('app.data.repositories.league_repository.League')
def test_get_league_by_name_when_leagues_is_empty_should_return_none(fake_league, test_repo):
    # Arrange
    leagues_in = []
    fake_league.query.all.return_value = leagues_in

    # Act
    league_out = test_repo.get_league_by_name("NFC")

    # Assert
    assert league_out is None


@patch('app.data.repositories.league_repository.League')
def test_get_league_by_name_when_leagues_is_not_empty_and_league_with_short_name_is_not_found_should_return_none(
        fake_league, test_repo
):
    # Arrange
    leagues_in = [
        League(
            short_name="C1",
            long_name="League 1",
            first_season_year=1
        ),
        League(
            short_name="C2",
            long_name="League 2",
            first_season_year=2
        ),
        League(
            short_name="C3",
            long_name="League 3",
            first_season_year=3
        ),
    ]
    fake_league.query.all.return_value = leagues_in
    fake_league.query.filter_by.return_value.first.return_value = None

    # Act
    league_out = test_repo.get_league_by_name("C4")

    # Assert
    assert league_out is None


@patch('app.data.repositories.league_repository.League')
def test_get_league_by_name_when_leagues_is_not_empty_and_league_with_name_is_found_should_return_league(
        fake_league, test_repo
):
    # Arrange
    leagues_in = [
        League(
            short_name="C1",
            long_name="League 1",
            first_season_year=1
        ),
        League(
            short_name="C2",
            long_name="League 2",
            first_season_year=2
        ),
        League(
            short_name="C3",
            long_name="League 3",
            first_season_year=3
        ),
    ]
    fake_league.query.all.return_value = leagues_in
    fake_league.query.filter_by.return_value.first.return_value = leagues_in[-1]

    # Act
    league_out = test_repo.get_league_by_name("AAFC")

    # Assert
    assert league_out is leagues_in[-1]


@patch('app.data.repositories.league_repository.try_commit')
@patch('app.data.repositories.league_repository.sqla')
def test_add_league_when_no_integrity_error_caught_should_add_league(fake_sqla, fake_try_commit, test_repo):
    # Arrange
    league_in = League(
        short_name="C",
        long_name="League",
        first_season_year=1
    )

    # Act
    league_out = test_repo.add_league(league_in)

    # Assert
    fake_sqla.session.add.assert_called_once_with(league_in)
    fake_try_commit.assert_called_once()
    assert league_out is league_in


@patch('app.data.repositories.league_repository.try_commit')
@patch('app.data.repositories.league_repository.sqla')
def test_add_league_when_integrity_error_caught_should_rollback_transaction_and_reraise_error(
        fake_sqla, fake_try_commit, test_repo
):
    # Arrange
    league_in = League(
        short_name="C",
        long_name="League",
        first_season_year=1
    )
    fake_try_commit.side_effect = IntegrityError('statement', 'params', Exception())

    # Act
    with pytest.raises(IntegrityError):
        league_out = test_repo.add_league(league_in)

    # Assert
    fake_sqla.session.add.assert_called_once_with(league_in)
    fake_try_commit.assert_called_once()


@patch('app.data.repositories.league_repository.try_commit')
@patch('app.data.repositories.league_repository.sqla')
def test_add_leagues_when_leagues_arg_is_empty_should_add_no_leagues(fake_sqla, fake_try_commit, test_repo):
    # Arrange
    leagues_in = ()

    # Act
    leagues_out = test_repo.add_leagues(leagues_in)

    # Assert
    fake_sqla.session.add.assert_not_called()
    fake_try_commit.assert_called_once()
    assert leagues_out == tuple()


@patch('app.data.repositories.league_repository.try_commit')
@patch('app.data.repositories.league_repository.sqla')
def test_add_leagues_when_leagues_arg_is_not_empty_and_no_integrity_error_caught_should_add_leagues(
        fake_sqla, fake_try_commit, test_repo
):
    # Arrange
    leagues_in = (
        League(
            short_name="C1",
            long_name="League 1",
            first_season_year=1
        ),
        League(
            short_name="C2",
            long_name="League 2",
            first_season_year=2
        ),
        League(
            short_name="C3",
            long_name="League 3",
            first_season_year=3
        ),
    )

    # Act
    leagues_out = test_repo.add_leagues(leagues_in)

    # Assert
    fake_sqla.session.add.assert_has_calls([
        call(leagues_in[0]),
        call(leagues_in[1]),
        call(leagues_in[2]),
    ])
    fake_try_commit.assert_called_once()
    assert leagues_out == leagues_in


@patch('app.data.repositories.league_repository.try_commit')
@patch('app.data.repositories.league_repository.sqla')
def test_add_leagues_when_leagues_arg_is_not_empty_and_integrity_error_caught_should_rollback_transaction_and_reraise_error(
        fake_sqla, fake_try_commit, test_repo
):
    # Arrange
    leagues_in = (
        League(
            short_name="C1",
            long_name="League 1",
            first_season_year=1
        ),
        League(
            short_name="C2",
            long_name="League 2",
            first_season_year=2
        ),
        League(
            short_name="C3",
            long_name="League 3",
            first_season_year=3
        ),
    )
    fake_try_commit.side_effect = IntegrityError('statement', 'params', Exception())

    # Act
    with pytest.raises(IntegrityError):
        leagues_out = test_repo.add_leagues(leagues_in)

    # Assert
    fake_sqla.session.add.assert_has_calls([
        call(leagues_in[0]),
        call(leagues_in[1]),
        call(leagues_in[2]),
    ])
    fake_try_commit.assert_called_once()


@patch('app.data.repositories.league_repository.League')
def test_league_exists_when_league_does_not_exist_should_return_false(fake_league, test_repo):
    # Arrange
    leagues = [
        League(
            short_name="C1",
            long_name="League 1",
            first_season_year=1
        ),
        League(
            short_name="C2",
            long_name="League 2",
            first_season_year=2
        ),
        League(
            short_name="C3",
            long_name="League 3",
            first_season_year=3
        ),
    ]
    fake_league.query.all.return_value = leagues
    fake_league.query.get.return_value = None

    # Act
    league_exists = test_repo.league_exists(id=1)

    # Assert
    assert not league_exists


@patch('app.data.repositories.league_repository.League')
def test_league_exists_when_league_exists_should_return_true(fake_league, test_repo):
    # Arrange
    leagues = [
        League(
            short_name="C1",
            long_name="League 1",
            first_season_year=1
        ),
        League(
            short_name="C2",
            long_name="League 2",
            first_season_year=2
        ),
        League(
            short_name="C3",
            long_name="League 3",
            first_season_year=3
        ),
    ]
    fake_league.query.all.return_value = leagues
    fake_league.query.get.return_value = leagues[1]

    # Act
    league_exists = test_repo.league_exists(id=1)

    # Assert
    assert league_exists


@patch('app.data.repositories.league_repository.try_commit')
@patch('app.data.repositories.league_repository.sqla')
@patch('app.data.repositories.league_repository.LeagueRepository.league_exists')
def test_update_league_when_no_league_exists_with_id_should_return_league_and_not_update_database(
        fake_league_exists, fake_sqla, fake_try_commit, test_repo
):
    # Arrange
    fake_league_exists.return_value = False

    # Act
    league = League(
        id=1,
        short_name="C",
        long_name="League",
        first_season_year=1,
        last_season_year=2
    )

    try:
        league_updated = test_repo.update_league(league)
    except ValueError:
        assert False

    # Assert
    fake_sqla.session.add.assert_not_called()
    fake_try_commit.assert_not_called()
    assert isinstance(league_updated, League)
    assert isinstance(league_updated, League)
    assert league_updated.id == league.id
    assert league_updated.short_name == league.short_name
    assert league_updated.long_name == league.long_name
    assert league_updated.first_season_year == league.first_season_year
    assert league_updated.last_season_year == league.last_season_year


@patch('app.data.repositories.league_repository.try_commit')
@patch('app.data.repositories.league_repository.sqla')
@patch('app.data.repositories.league_repository.League')
@patch('app.data.repositories.league_repository.LeagueRepository.league_exists')
def test_update_league_when_league_exists_with_id_and_no_integrity_error_caught_should_return_league_and_update_database(
        fake_league_exists, fake_league, fake_sqla, fake_try_commit, test_repo
):
    # Arrange
    fake_league_exists.return_value = True

    leagues = [
        League(
            id=1,
            short_name="C1",
            long_name="League 1",
            first_season_year=1,
            last_season_year=2
        ),
        League(
            id=2,
            short_name="C2",
            long_name="League 2",
            first_season_year=3,
            last_season_year=4
        ),
        League(
            id=3,
            short_name="C3",
            long_name="League 3",
            first_season_year=5,
            last_season_year=6
        ),
    ]
    fake_league.query.all.return_value = leagues

    old_league = leagues[1]
    fake_league.query.get.return_value = old_league

    new_league = League(
        id=2,
        short_name="C4",
        long_name="League 4",
        first_season_year=7,
        last_season_year=8
    )

    # Act
    try:
        league_updated = test_repo.update_league(new_league)
    except IntegrityError:
        assert False

    # Assert
    fake_sqla.session.add.assert_called_once_with(old_league)
    fake_try_commit.assert_called_once()
    assert isinstance(league_updated, League)
    assert isinstance(league_updated, League)
    assert league_updated.id == new_league.id
    assert league_updated.short_name == new_league.short_name
    assert league_updated.long_name == new_league.long_name
    assert league_updated.first_season_year == new_league.first_season_year
    assert league_updated.last_season_year == new_league.last_season_year
    assert league_updated is new_league


@patch('app.data.repositories.league_repository.try_commit')
@patch('app.data.repositories.league_repository.sqla')
@patch('app.data.repositories.league_repository.League')
@patch('app.data.repositories.league_repository.LeagueRepository.league_exists')
def test_update_league_when_and_league_exists_with_id_and_integrity_error_caught_should_rollback_transaction_and_reraise_error(
        fake_league_exists, fake_league, fake_sqla, fake_try_commit, test_repo
):
    # Arrange
    fake_league_exists.return_value = True

    leagues = [
        League(
            id=1,
            short_name="C1",
            long_name="League 1",
            first_season_year=1,
            last_season_year=2
        ),
        League(
            id=2,
            short_name="C2",
            long_name="League 2",
            first_season_year=3,
            last_season_year=4
        ),
        League(
            id=3,
            short_name="C3",
            long_name="League 3",
            first_season_year=5,
            last_season_year=6
        ),
    ]
    fake_league.query.all.return_value = leagues

    old_league = leagues[1]
    fake_league.query.get.return_value = old_league

    new_league = League(
        id=2,
        short_name="C4",
        long_name="League 4",
        first_season_year=7,
        last_season_year=8
    )

    fake_try_commit.side_effect = IntegrityError('statement', 'params', Exception())

    # Act
    with pytest.raises(IntegrityError):
        league_updated = test_repo.update_league(new_league)

    # Assert
    fake_sqla.session.add.assert_called_once_with(old_league)
    fake_try_commit.assert_called_once()


@patch('app.data.repositories.league_repository.try_commit')
@patch('app.data.repositories.league_repository.sqla')
@patch('app.data.repositories.league_repository.League')
def test_delete_league_when_league_does_not_exist_should_return_none_and_not_delete_league_from_database(
        fake_league, fake_sqla, fake_try_commit, test_repo
):
    # Arrange
    leagues = [
        League(
            short_name="C1",
            long_name="League 1",
            first_season_year=1,
            last_season_year=2
        ),
        League(
            short_name="C2",
            long_name="League 2",
            first_season_year=3,
            last_season_year=4
        ),
        League(
            short_name="C3",
            long_name="League 3",
            first_season_year=5,
            last_season_year=6
        ),
    ]
    fake_league.query.all.return_value = leagues
    fake_league.query.get.return_value = None

    id = 1

    # Act
    league_deleted = test_repo.delete_league(id)

    # Assert
    assert league_deleted is None
    fake_sqla.session.delete.assert_not_called()
    fake_try_commit.assert_not_called()


@patch('app.data.repositories.league_repository.try_commit')
@patch('app.data.repositories.league_repository.sqla')
@patch('app.data.repositories.league_repository.League')
def test_delete_league_when_league_exists_and_integrity_error_not_caught_should_return_league_and_delete_league_from_database(
        fake_league, fake_sqla, fake_try_commit, test_repo
):
    # Arrange
    leagues = [
        League(
            short_name="C1",
            long_name="League 1",
            first_season_year=1,
            last_season_year=2
        ),
        League(
            short_name="C2",
            long_name="League 2",
            first_season_year=3,
            last_season_year=4
        ),
        League(
            short_name="C3",
            long_name="League 3",
            first_season_year=5,
            last_season_year=6
        ),
    ]
    fake_league.query.all.return_value = leagues

    id = 1
    fake_league.query.get.return_value = leagues[id]

    # Act
    try:
        league_deleted = test_repo.delete_league(id)
    except IntegrityError:
        assert False

    # Assert
    fake_sqla.session.delete.assert_called_once_with(league_deleted)
    fake_try_commit.assert_called_once()
    assert league_deleted is leagues[id]


@patch('app.data.repositories.league_repository.try_commit')
@patch('app.data.repositories.league_repository.sqla')
@patch('app.data.repositories.league_repository.League')
def test_delete_league_when_league_exists_and_integrity_error_caught_should_rollback_commit(
        fake_league, fake_sqla, fake_try_commit, test_repo
):
    # Arrange
    leagues = [
        League(
            short_name="C1",
            long_name="League 1",
            first_season_year=1,
            last_season_year=2
        ),
        League(
            short_name="C2",
            long_name="League 2",
            first_season_year=3,
            last_season_year=4
        ),
        League(
            short_name="C3",
            long_name="League 3",
            first_season_year=5,
            last_season_year=6
        ),
    ]
    fake_league.query.all.return_value = leagues

    id = 1
    fake_league.query.get.return_value = leagues[id]

    fake_try_commit.side_effect = IntegrityError('statement', 'params', Exception())

    # Act
    with pytest.raises(IntegrityError):
        league_deleted = test_repo.delete_league(id)

    # Assert
    fake_sqla.session.delete.assert_called_once_with(fake_league.query.get.return_value)
    fake_try_commit.assert_called_once()
