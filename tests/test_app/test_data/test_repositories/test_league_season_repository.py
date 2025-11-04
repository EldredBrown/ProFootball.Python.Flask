from unittest.mock import patch, call

import pytest

from sqlalchemy.exc import IntegrityError

from test_app import create_app

from app.data.models.league_season import LeagueSeason
from app.data.repositories.league_season_repository import LeagueSeasonRepository


@pytest.fixture
def test_repo():
    return LeagueSeasonRepository()


@patch('app.data.repositories.league_season_repository.LeagueSeason')
def test_get_league_seasons_should_get_league_seasons(fake_league_season, test_repo):
    # Act
    league_seasons = test_repo.get_league_seasons()

    # Assert
    fake_league_season.query.all.assert_called_once()
    assert league_seasons == fake_league_season.query.all.return_value


@patch('app.data.repositories.league_season_repository.LeagueSeasonRepository.get_league_seasons')
def test_get_league_season_when_league_seasons_is_empty_should_return_none(fake_get_league_seasons, test_repo):
    # Arrange
    league_seasons = []
    fake_get_league_seasons.return_value = league_seasons

    # Act
    league_season = test_repo.get_league_season(1)

    # Assert
    assert league_season is None


@patch('app.data.repositories.league_season_repository.LeagueSeason')
@patch('app.data.repositories.league_season_repository.LeagueSeasonRepository.get_league_seasons')
def test_get_league_season_when_league_seasons_is_not_empty_and_league_season_is_not_found_should_return_none(
        fake_get_league_seasons, fake_league_season, test_repo
):
    # Arrange
    league_seasons = [
        LeagueSeason(league_name="League 1", season_year=1),
        LeagueSeason(league_name="League 2", season_year=1),
        LeagueSeason(league_name="League 1", season_year=2),
    ]
    fake_get_league_seasons.return_value = league_seasons

    id = len(league_seasons) + 1

    # Act
    league_season = test_repo.get_league_season(id)

    # Assert
    fake_league_season.query.get.assert_called_once_with(id)
    assert league_season == fake_league_season.query.get.return_value


@patch('app.data.repositories.league_season_repository.LeagueSeason')
@patch('app.data.repositories.league_season_repository.LeagueSeasonRepository.get_league_seasons')
def test_get_league_season_when_league_seasons_is_not_empty_and_league_season_is_found_should_return_league_season(
        fake_get_league_seasons, fake_league_season, test_repo
):
    # Arrange
    league_seasons = [
        LeagueSeason(league_name="League 1", season_year=1),
        LeagueSeason(league_name="League 2", season_year=1),
        LeagueSeason(league_name="League 1", season_year=2),
    ]
    fake_get_league_seasons.return_value = league_seasons

    id = len(league_seasons) - 1

    # Act
    league_season = test_repo.get_league_season(id)

    # Assert
    fake_league_season.query.get.assert_called_once_with(id)
    assert league_season == fake_league_season.query.get.return_value


@patch('app.data.repositories.league_season_repository.LeagueSeasonRepository.get_league_seasons')
def test_get_league_season_by_league_name_and_season_year_when_league_seasons_is_empty_should_return_none(
        fake_get_league_seasons, test_repo
):
    # Arrange
    league_seasons = []
    fake_get_league_seasons.return_value = league_seasons

    # Act
    league_season = test_repo.get_league_season_by_league_name_and_season_year(league_name="A", season_year=1)

    # Assert
    assert league_season is None


@patch('app.data.repositories.league_season_repository.LeagueSeason')
@patch('app.data.repositories.league_season_repository.LeagueSeasonRepository.get_league_seasons')
def test_get_league_season_by_league_name_and_season_year_when_league_seasons_is_not_empty_and_league_season_is_not_found_should_return_none(
        fake_get_league_seasons, fake_league_season, test_repo
):
    # Arrange
    league_seasons = [
        LeagueSeason(league_name="League 1", season_year=1),
        LeagueSeason(league_name="League 2", season_year=1),
        LeagueSeason(league_name="League 1", season_year=2),
    ]
    fake_get_league_seasons.return_value = league_seasons

    # Act
    league_season = test_repo.get_league_season_by_league_name_and_season_year(
        league_name="League 1", season_year=3
    )

    # Assert
    fake_league_season.query.filter_by.assert_called_once_with(league_name="League 1", season_year=3)
    fake_league_season.query.filter_by.return_value.first.assert_called_once()
    assert league_season == fake_league_season.query.filter_by.return_value.first.return_value


@patch('app.data.repositories.league_season_repository.LeagueSeason')
@patch('app.data.repositories.league_season_repository.LeagueSeasonRepository.get_league_seasons')
def test_get_league_season_by_league_name_and_season_year_when_league_seasons_is_not_empty_and_league_season_is_found_should_return_league_season(
        fake_get_league_seasons, fake_league_season, test_repo
):
    # Arrange
    league_seasons = [
        LeagueSeason(league_name="League 1", season_year=1),
        LeagueSeason(league_name="League 2", season_year=1),
        LeagueSeason(league_name="League 1", season_year=2),
    ]
    fake_get_league_seasons.return_value = league_seasons

    # Act
    league_season = test_repo.get_league_season_by_league_name_and_season_year(
        league_name="League 1", season_year=1
    )

    # Assert
    fake_league_season.query.filter_by.assert_called_once_with(league_name="League 1", season_year=1)
    fake_league_season.query.filter_by.return_value.first.assert_called_once()
    assert league_season == fake_league_season.query.filter_by.return_value.first.return_value


@patch('app.data.repositories.league_season_repository.try_commit')
@patch('app.data.repositories.league_season_repository.sqla')
def test_add_league_season_when_no_integrity_error_caught_should_add_league_season(
        fake_sqla, fake_try_commit, test_repo
):
    # Arrange
    league_season_in = LeagueSeason(league_name="League 1", season_year=1)

    # Act
    league_season_out = test_repo.add_league_season(league_season_in)

    # Assert
    fake_sqla.session.add.assert_called_once_with(league_season_in)
    fake_try_commit.assert_called_once()
    assert league_season_in is league_season_in


@patch('app.data.repositories.league_season_repository.try_commit')
@patch('app.data.repositories.league_season_repository.sqla')
def test_add_league_season_when_integrity_error_caught_should_rollback_transaction_and_reraise_error(
        fake_sqla, fake_try_commit, test_repo
):
    # Arrange
    league_season_in = LeagueSeason(league_name="League 1", season_year=1)
    fake_try_commit.side_effect = IntegrityError('statement', 'params', Exception())

    # Act
    with pytest.raises(IntegrityError):
        league_season_out = test_repo.add_league_season(league_season_in)

    # Assert
    fake_sqla.session.add.assert_called_once_with(league_season_in)
    fake_try_commit.assert_called_once()


@patch('app.data.repositories.league_season_repository.try_commit')
@patch('app.data.repositories.league_season_repository.sqla')
def test_add_league_seasons_when_league_seasons_arg_is_empty_should_add_no_league_seasons(
        fake_sqla, fake_try_commit, test_repo
):
    # Arrange
    league_seasons_in = ()

    # Act
    league_seasons_out = test_repo.add_league_seasons(league_seasons_in)

    # Assert
    fake_sqla.session.add.assert_not_called()
    fake_try_commit.assert_called_once()
    assert league_seasons_out == tuple()


@patch('app.data.repositories.league_season_repository.try_commit')
@patch('app.data.repositories.league_season_repository.sqla')
def test_add_league_seasons_when_games_arg_is_not_empty_and_no_integrity_error_caught_should_add_league_seasons(
        fake_sqla, fake_try_commit, test_repo
):
    # Arrange
    league_seasons_in = (
        LeagueSeason(league_name="League 1", season_year=1),
        LeagueSeason(league_name="League 2", season_year=2),
        LeagueSeason(league_name="League 3", season_year=3),
    )

    # Act
    league_seasons_out = test_repo.add_league_seasons(league_seasons_in)

    # Assert
    fake_sqla.session.add.assert_has_calls([
        call(league_seasons_in[0]),
        call(league_seasons_in[1]),
        call(league_seasons_in[2]),
    ])
    fake_try_commit.assert_called_once()
    assert league_seasons_out == league_seasons_in


@patch('app.data.repositories.league_season_repository.try_commit')
@patch('app.data.repositories.league_season_repository.sqla')
def test_add_league_seasons_when_games_arg_is_not_empty_and_integrity_error_caught_should_rollback_transaction_and_reraise_error(
        fake_sqla, fake_try_commit, test_repo
):
    # Arrange
    league_seasons_in = (
        LeagueSeason(league_name="League 1", season_year=1),
        LeagueSeason(league_name="League 2", season_year=2),
        LeagueSeason(league_name="League 3", season_year=3),
    )
    fake_try_commit.side_effect = IntegrityError('statement', 'params', Exception())

    # Act
    with pytest.raises(IntegrityError):
        league_seasons_out = test_repo.add_league_seasons(league_seasons_in)

    # Assert
    fake_sqla.session.add.assert_has_calls([
        call(league_seasons_in[0]),
        call(league_seasons_in[1]),
        call(league_seasons_in[2]),
    ])
    fake_try_commit.assert_called_once()


@patch('app.data.repositories.league_season_repository.LeagueSeason')
def test_league_season_exists_when_league_season_does_not_exist_should_return_false(
        fake_league_season, test_repo
):
    # Arrange
    league_seasons = (
        LeagueSeason(league_name="League 1", season_year=1),
        LeagueSeason(league_name="League 2", season_year=2),
        LeagueSeason(league_name="League 3", season_year=3),
    )
    fake_league_season.query.all.return_value = league_seasons
    fake_league_season.query.get.return_value = None

    # Act
    league_season_exists = test_repo.league_season_exists(id=1)

    # Assert
    assert not league_season_exists


@patch('app.data.repositories.league_season_repository.LeagueSeason')
def test_league_season_exists_when_league_season_exists_should_return_true(fake_league_season, test_repo):
    # Arrange
    league_seasons = (
        LeagueSeason(league_name="League 1", season_year=1),
        LeagueSeason(league_name="League 2", season_year=2),
        LeagueSeason(league_name="League 3", season_year=3),
    )
    fake_league_season.query.all.return_value = league_seasons
    fake_league_season.query.get.return_value = league_seasons[1]

    # Act
    league_season_exists = test_repo.league_season_exists(id=1)

    # Assert
    assert league_season_exists


@patch('app.data.repositories.league_season_repository.try_commit')
@patch('app.data.repositories.league_season_repository.sqla')
@patch('app.data.repositories.league_season_repository.LeagueSeasonRepository.league_season_exists')
def test_update_league_season_when_no_league_season_exists_with_id_should_return_league_season_and_not_update_database(
        fake_league_season_exists, fake_sqla, fake_try_commit, test_repo
):
    # Arrange
    fake_league_season_exists.return_value = False

    # Act
    league_season = LeagueSeason(
        league_name="League 1",
        season_year=1
    )
    try:
        league_season_updated = test_repo.update_league_season(league_season)
    except ValueError:
        assert False

    # Assert
    fake_sqla.session.add.assert_not_called()
    fake_try_commit.assert_not_called()
    assert isinstance(league_season_updated, LeagueSeason)
    assert league_season_updated.league_name == league_season.league_name
    assert league_season_updated.season_year == league_season.season_year
    assert league_season_updated.total_games == league_season.total_games
    assert league_season_updated.total_points == league_season.total_points
    assert league_season_updated.average_points == league_season.average_points


@patch('app.data.repositories.league_season_repository.try_commit')
@patch('app.data.repositories.league_season_repository.sqla')
@patch('app.data.repositories.league_season_repository.LeagueSeason')
@patch('app.data.repositories.league_season_repository.LeagueSeasonRepository.league_season_exists')
def test_update_league_season_when_league_season_exists_with_id_and_no_integrity_error_caught_should_return_league_season_and_update_database(
        fake_league_season_exists, fake_league_season, fake_sqla, fake_try_commit, test_repo
):
    # Arrange
    fake_league_season_exists.return_value = True

    league_seasons = [
        LeagueSeason(league_name="League 1", season_year=1),
        LeagueSeason(league_name="League 2", season_year=2),
        LeagueSeason(league_name="League 3", season_year=3),
    ]
    fake_league_season.query.all.return_value = league_seasons

    old_league_season = league_seasons[1]
    fake_league_season.query.get.return_value = old_league_season

    new_league_season = LeagueSeason(id=2, league_name="League 4", season_year=4)

    # Act
    try:
        league_season_updated = test_repo.update_league_season(new_league_season)
    except IntegrityError:
        assert False

    # Assert
    fake_sqla.session.add.assert_called_once_with(old_league_season)
    fake_try_commit.assert_called_once()
    assert isinstance(league_season_updated, LeagueSeason)
    assert league_season_updated.league_name == new_league_season.league_name
    assert league_season_updated.season_year == new_league_season.season_year
    assert league_season_updated.total_games == new_league_season.total_games
    assert league_season_updated.total_points == new_league_season.total_points
    assert league_season_updated.average_points == new_league_season.average_points


@patch('app.data.repositories.league_season_repository.try_commit')
@patch('app.data.repositories.league_season_repository.sqla')
@patch('app.data.repositories.league_season_repository.LeagueSeason')
@patch('app.data.repositories.league_season_repository.LeagueSeasonRepository.league_season_exists')
def test_update_league_season_when_and_league_season_exists_with_id_and_integrity_error_caught_should_rollback_transaction_and_reraise_error(
        fake_league_season_exists, fake_league_season, fake_sqla, fake_try_commit, test_repo
):
    # Arrange
    fake_league_season_exists.return_value = True

    league_seasons = [
        LeagueSeason(league_name="League 1", season_year=1),
        LeagueSeason(league_name="League 2", season_year=2),
        LeagueSeason(league_name="League 3", season_year=3),
    ]
    fake_league_season.query.all.return_value = league_seasons

    old_league_season = league_seasons[1]
    fake_league_season.query.get.return_value = old_league_season

    new_league_season = LeagueSeason(id=2, league_name="League 4", season_year=4)

    fake_try_commit.side_effect = IntegrityError('statement', 'params', Exception())

    # Act
    with pytest.raises(IntegrityError):
        league_season_updated = test_repo.update_league_season(new_league_season)

    # Assert
    fake_sqla.session.add.assert_called_once_with(old_league_season)
    fake_try_commit.assert_called_once()


@patch('app.data.repositories.league_season_repository.try_commit')
@patch('app.data.repositories.league_season_repository.sqla')
@patch('app.data.repositories.league_season_repository.LeagueSeason')
def test_delete_league_season_when_league_season_does_not_exist_should_return_none_and_not_delete_league_season_from_database(
        fake_league_season, fake_sqla, fake_try_commit, test_repo
):
    # Arrange
    league_seasons = [
        LeagueSeason(league_name="League 1", season_year=1),
        LeagueSeason(league_name="League 2", season_year=2),
        LeagueSeason(league_name="League 3", season_year=3),
    ]
    fake_league_season.query.all.return_value = league_seasons
    fake_league_season.query.get.return_value = None

    id = 1

    # Act
    league_season_deleted = test_repo.delete_league_season(id)

    # Assert
    assert league_season_deleted is None
    fake_sqla.session.delete.assert_not_called()
    fake_try_commit.assert_not_called()


@patch('app.data.repositories.league_season_repository.try_commit')
@patch('app.data.repositories.league_season_repository.sqla')
@patch('app.data.repositories.league_season_repository.LeagueSeason')
def test_delete_league_season_when_league_season_exists_and_integrity_error_not_caught_should_return_league_season_and_delete_league_season_from_database(
        fake_league_season, fake_sqla, fake_try_commit, test_repo
):
    # Arrange
    league_seasons = [
        LeagueSeason(league_name="League 1", season_year=1),
        LeagueSeason(league_name="League 2", season_year=2),
        LeagueSeason(league_name="League 3", season_year=3),
    ]
    fake_league_season.query.all.return_value = league_seasons

    id = 1
    fake_league_season.query.get.return_value = league_seasons[id]

    # Act
    try:
        league_season_deleted = test_repo.delete_league_season(id)
    except IntegrityError:
        assert False

    # Assert
    fake_sqla.session.delete.assert_called_once_with(league_season_deleted)
    fake_try_commit.assert_called_once()
    assert league_season_deleted is league_seasons[id]


@patch('app.data.repositories.league_season_repository.try_commit')
@patch('app.data.repositories.league_season_repository.sqla')
@patch('app.data.repositories.league_season_repository.LeagueSeason')
def test_delete_league_season_when_league_season_exists_and_integrity_error_caught_should_rollback_commit(
        fake_league_season, fake_sqla, fake_try_commit, test_repo
):
    # Arrange
    league_seasons = [
        LeagueSeason(league_name="League 1", season_year=1),
        LeagueSeason(league_name="League 2", season_year=2),
        LeagueSeason(league_name="League 3", season_year=3),
    ]
    fake_league_season.query.all.return_value = league_seasons

    id = 1
    fake_league_season.query.get.return_value = league_seasons[id]

    fake_try_commit.side_effect = IntegrityError('statement', 'params', Exception())

    # Act
    with pytest.raises(IntegrityError):
        league_season_deleted = test_repo.delete_league_season(id)

    # Assert
    fake_sqla.session.delete.assert_called_once_with(fake_league_season.query.get.return_value)
    fake_try_commit.assert_called_once()
