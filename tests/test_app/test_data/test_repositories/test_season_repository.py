from unittest.mock import patch, call

import pytest

from sqlalchemy.exc import IntegrityError

from app import sqla
from instance.test_db import db_init
from test_app import create_app

from app.data.models.season import Season
from app.data.repositories.season_repository import SeasonRepository


@pytest.fixture
def test_app():
    return create_app()


@pytest.fixture
def test_repo():
    return SeasonRepository()


def test_get_seasons_should_get_seasons(test_app, test_repo):
    with test_app.app_context():
        # Arrange
        db_init.init_db()

        seasons_in= [
            Season(year=1920),
            Season(year=1921),
            Season(year=1922),
        ]
        for season in seasons_in:
            sqla.session.add(season)
        sqla.session.commit()

        # Act
        seasons_out = test_repo.get_seasons()

    # Assert
    assert seasons_out == seasons_in


@patch('app.data.repositories.season_repository.Season')
def test_get_season_when_seasons_is_empty_should_return_none(fake_season, test_app, test_repo):
    with test_app.app_context():
        # Arrange
        seasons_in = ()
        fake_season.query.all.return_value = seasons_in

        # Act
        season_out = test_repo.get_season(1)

    # Assert
    assert season_out is None


@patch('app.data.repositories.season_repository.Season')
def test_get_season_when_seasons_is_not_empty_and_season_is_not_found_should_return_none(
        fake_season, test_app, test_repo
):
    with test_app.app_context():
        # Arrange
        seasons_in = (
            Season(year=1920),
            Season(year=1921),
            Season(year=1922),
        )
        fake_season.query.all.return_value = seasons_in

        selected_season = None
        fake_season.query.get.return_value = selected_season

        # Act
        year = -1
        season_out = test_repo.get_season(year)

    # Assert
    assert season_out is None


@patch('app.data.repositories.season_repository.Season')
def test_get_season_when_seasons_is_not_empty_and_season_is_found_should_return_season(
        fake_season, test_app, test_repo
):
    with test_app.app_context():
        # Arrange
        seasons_in = (
            Season(year=1920),
            Season(year=1921),
            Season(year=1922),
        )
        fake_season.query.all.return_value = seasons_in

        selected_season = [s for s in seasons_in if s.year == 1920][0]
        fake_season.query.get.return_value = selected_season

        # Act
        season_out = test_repo.get_season(selected_season.year)

    # Assert
    assert season_out is selected_season


@patch('app.data.repositories.season_repository.try_commit')
@patch('app.data.repositories.season_repository.sqla')
def test_add_season_when_no_integrity_error_caught_should_add_season(
        fake_sqla, fake_try_commit, test_app, test_repo
):
    with test_app.app_context():
        # Arrange
        season_in = Season(
            year=1920
        )

        # Act
        try:
            season_out = test_repo.add_season(season_in)
        except IntegrityError:
            assert False

    # Assert
    fake_sqla.session.add.assert_called_once_with(season_in)
    fake_try_commit.assert_called_once()
    assert season_out is season_in


@patch('app.data.repositories.season_repository.try_commit')
@patch('app.data.repositories.season_repository.sqla')
def test_add_season_when_integrity_error_caught_should_rollback_transaction_and_reraise_error(
        fake_sqla, fake_try_commit, test_app, test_repo
):
    with test_app.app_context():
        # Arrange
        season_in = Season(
            year=1920
        )
        fake_try_commit.side_effect = IntegrityError('statement', 'params', Exception())

        # Act
        with pytest.raises(IntegrityError):
            season_out = test_repo.add_season(season_in)

    # Assert
    fake_sqla.session.add.assert_called_once_with(season_in)
    fake_try_commit.assert_called_once()


@patch('app.data.repositories.season_repository.try_commit')
@patch('app.data.repositories.season_repository.sqla')
def test_add_seasons_when_seasons_arg_is_empty_should_add_no_seasons(
        fake_sqla, fake_try_commit, test_app, test_repo
):
    with test_app.app_context():
        # Arrange
        seasons_in = ()

        # Act
        seasons_out = test_repo.add_seasons(seasons_in)

    # Assert
    fake_sqla.session.add.assert_not_called()
    fake_try_commit.assert_called_once()
    assert seasons_out == tuple()


@patch('app.data.repositories.season_repository.try_commit')
@patch('app.data.repositories.season_repository.sqla')
def test_add_seasons_when_seasons_arg_is_not_empty_and_no_integrity_error_caught_should_add_seasons(
        fake_sqla, fake_try_commit, test_app, test_repo
):
    with test_app.app_context():
        # Arrange
        seasons_in = (
            Season(year=1920),
            Season(year=1921),
            Season(year=1922),
        )

        # Act
        seasons_out = test_repo.add_seasons(seasons_in)

    # Assert
    fake_sqla.session.add.assert_has_calls([
        call(seasons_in[0]),
        call(seasons_in[1]),
        call(seasons_in[2]),
    ])
    fake_try_commit.assert_called_once()
    assert seasons_out == seasons_in


@patch('app.data.repositories.season_repository.try_commit')
@patch('app.data.repositories.season_repository.sqla')
def test_add_seasons_when_seasons_arg_is_not_empty_and_integrity_error_caught_should_rollback_transaction_and_reraise_error(
        fake_sqla, fake_try_commit, test_app, test_repo
):
    with test_app.app_context():
        # Arrange
        seasons_in = (
            Season(year=1920),
            Season(year=1921),
            Season(year=1922),
        )
        fake_try_commit.side_effect = IntegrityError('statement', 'params', Exception())

        # Act
        with pytest.raises(IntegrityError):
            seasons_out = test_repo.add_seasons(seasons_in)

    # Assert
    fake_sqla.session.add.assert_has_calls([
        call(seasons_in[0]),
        call(seasons_in[1]),
        call(seasons_in[2]),
    ])
    fake_try_commit.assert_called_once()


@patch('app.data.repositories.season_repository.Season')
def test_season_exists_when_season_does_not_exist_should_return_false(
        fake_season, test_app, test_repo
):
    with test_app.app_context():
        # Arrange
        seasons= (
            Season(year=1920),
            Season(year=1921),
            Season(year=1922),
        )
        fake_season.query.all.return_value = seasons
        fake_season.query.get.return_value = None

        # Act
        season_exists = test_repo.season_exists(year=-1)

    # Assert
    assert not season_exists


@patch('app.data.repositories.season_repository.Season')
def test_season_exists_when_season_exists_should_return_true(fake_season, test_app, test_repo):
    with test_app.app_context():
        # Arrange
        seasons= (
            Season(year=1920),
            Season(year=1921),
            Season(year=1922),
        )
        fake_season.query.all.return_value = seasons
        fake_season.query.get.return_value = seasons[1]

        # Act
        season_exists = test_repo.season_exists(year=1920)

    # Assert
    assert season_exists


@patch('app.data.repositories.season_repository.try_commit')
@patch('app.data.repositories.season_repository.sqla')
@patch('app.data.repositories.season_repository.SeasonRepository.season_exists')
def test_update_season_when_no_season_exists_with_year_should_return_season_and_not_update_database(
        fake_season_exists, fake_sqla, fake_try_commit, test_app,
        test_repo
):
    with test_app.app_context():
        # Arrange
        fake_season_exists.return_value = False

        # Act
        season = Season(
            year=1920
        )
        try:
            season_updated = test_repo.update_season(season)
        except ValueError:
            assert False

    # Assert
    fake_sqla.session.add.assert_not_called()
    fake_try_commit.assert_not_called()
    assert isinstance(season_updated, Season)
    assert season_updated.year == season.year


@patch('app.data.repositories.season_repository.try_commit')
@patch('app.data.repositories.season_repository.sqla')
@patch('app.data.repositories.season_repository.Season')
@patch('app.data.repositories.season_repository.SeasonRepository.season_exists')
def test_update_season_when_season_exists_with_year_and_no_integrity_error_caught_should_return_season_and_update_database(
        fake_season_exists, fake_season, fake_sqla, fake_try_commit,
        test_app, test_repo
):
    with test_app.app_context():
        # Arrange
        fake_season_exists.return_value = True

        seasons= (
            Season(year=1920),
            Season(year=1921),
            Season(year=1922),
        )
        fake_season.query.all.return_value = seasons

        old_season = seasons[1]
        fake_season.query.get.return_value = old_season

        new_season = Season(
            year=1921
        )

        # Act
        try:
            season_updated = test_repo.update_season(new_season)
        except IntegrityError:
            assert False

    # Assert
    fake_sqla.session.add.assert_called_once_with(old_season)
    fake_try_commit.assert_called_once()
    assert isinstance(season_updated, Season)
    assert season_updated.year == new_season.year


@patch('app.data.repositories.season_repository.try_commit')
@patch('app.data.repositories.season_repository.sqla')
@patch('app.data.repositories.season_repository.Season')
@patch('app.data.repositories.season_repository.SeasonRepository.season_exists')
def test_update_season_when_season_exists_with_year_and_integrity_error_caught_should_rollback_transaction_and_reraise_error(
        fake_season_exists, fake_season, fake_sqla,
        fake_try_commit, test_app, test_repo
):
    with test_app.app_context():
        # Arrange
        fake_season_exists.return_value = True

        seasons= (
            Season(year=1920),
            Season(year=1921),
            Season(year=1922),
        )
        fake_season.query.all.return_value = seasons

        old_season = seasons[1]
        fake_season.query.get.return_value = old_season

        new_season = Season(
            year=1921
        )

        fake_try_commit.side_effect = IntegrityError('statement', 'params', Exception())

        # Act
        with pytest.raises(IntegrityError):
            season_updated = test_repo.update_season(new_season)

    # Assert
    fake_sqla.session.add.assert_called_once_with(old_season)
    fake_try_commit.assert_called_once()


@patch('app.data.repositories.season_repository.try_commit')
@patch('app.data.repositories.season_repository.sqla')
@patch('app.data.repositories.season_repository.Season')
def test_delete_season_when_season_does_not_exist_should_return_none_and_not_delete_season_from_database(
        fake_season, fake_sqla, fake_try_commit, test_app, test_repo
):
    with test_app.app_context():
        # Arrange
        seasons= (
            Season(year=1920),
            Season(year=1921),
            Season(year=1922),
        )
        fake_season.query.all.return_value = seasons
        fake_season.query.get.return_value = None

        year = -1

        # Act
        season_deleted = test_repo.delete_season(year)

    # Assert
    assert season_deleted is None
    fake_sqla.session.delete.assert_not_called()
    fake_try_commit.assert_not_called()


@patch('app.data.repositories.season_repository.try_commit')
@patch('app.data.repositories.season_repository.sqla')
@patch('app.data.repositories.season_repository.Season')
def test_delete_season_when_season_exists_and_integrity_error_not_caught_should_return_season_and_delete_season_from_database(
        fake_season, fake_sqla, fake_try_commit, test_app, test_repo
):
    with test_app.app_context():
        # Arrange
        seasons= (
            Season(year=1920),
            Season(year=1921),
            Season(year=1922),
        )
        fake_season.query.all.return_value = seasons

        selected_season = [s for s in seasons if s.year == 1920][0]
        fake_season.query.get.return_value = selected_season

        # Act
        try:
            season_deleted = test_repo.delete_season(selected_season.year)
        except IntegrityError:
            assert False

    # Assert
    fake_sqla.session.delete.assert_called_once_with(season_deleted)
    fake_try_commit.assert_called_once()
    assert season_deleted is selected_season


@patch('app.data.repositories.season_repository.try_commit')
@patch('app.data.repositories.season_repository.sqla')
@patch('app.data.repositories.season_repository.Season')
def test_delete_season_when_season_exists_and_integrity_error_caught_should_rollback_commit(
        fake_season, fake_sqla, fake_try_commit, test_app,
        test_repo
):
    with test_app.app_context():
        # Arrange
        seasons= (
            Season(year=1920),
            Season(year=1921),
            Season(year=1922),
        )
        fake_season.query.all.return_value = seasons

        selected_season = [s for s in seasons if s.year == 1920][0]
        fake_season.query.get.return_value = selected_season

        fake_try_commit.side_effect = IntegrityError('statement', 'params', Exception())

        # Act
        with pytest.raises(IntegrityError):
            season_deleted = test_repo.delete_season(selected_season.year)

    # Assert
    fake_sqla.session.delete.assert_called_once_with(fake_season.query.get.return_value)
    fake_try_commit.assert_called_once()
