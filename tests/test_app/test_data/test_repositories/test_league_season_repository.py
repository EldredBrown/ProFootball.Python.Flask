from unittest.mock import patch, call

import pytest

from sqlalchemy.exc import IntegrityError

from app import sqla
from app.data.models.league_season import LeagueSeason
from app.data.repositories.league_season_repository import LeagueSeasonRepository
from instance.test_db import db_init
from test_app import create_app


@pytest.fixture
def test_app():
    return create_app()


@pytest.fixture
def test_repo():
    return LeagueSeasonRepository()


def test_get_league_seasons_should_get_league_seasons(test_app, test_repo):
    with test_app.app_context():
        # Arrange
        db_init.init_db()

        league_seasons_in = [
            LeagueSeason(
                id=1,
                league_id=1,
                season_year=1920,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
            LeagueSeason(
                id=2,
                league_id=2,
                season_year=1921,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
            LeagueSeason(
                id=3,
                league_id=3,
                season_year=1922,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
        ]
        for league_season in league_seasons_in:
            sqla.session.add(league_season)
        sqla.session.commit()

        # Act
        league_seasons_out = test_repo.get_league_seasons()

    # Assert
    assert league_seasons_out == league_seasons_in


def test_get_league_seasons_by_league_when_league_id_arg_is_none_should_return_empty_list(
        test_app, test_repo
):
    with test_app.app_context():
        # Arrange
        db_init.init_db()

        league_seasons_in = (
            LeagueSeason(
                id=1,
                league_id=1,
                season_year=1920,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
            LeagueSeason(
                id=2,
                league_id=1,
                season_year=1921,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
            LeagueSeason(
                id=3,
                league_id=1,
                season_year=1922,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
            LeagueSeason(
                id=4,
                league_id=2,
                season_year=1920,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
            LeagueSeason(
                id=5,
                league_id=2,
                season_year=1921,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
            LeagueSeason(
                id=6,
                league_id=2,
                season_year=1922,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
            LeagueSeason(
                id=7,
                league_id=3,
                season_year=1920,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
            LeagueSeason(
                id=8,
                league_id=3,
                season_year=1921,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
            LeagueSeason(
                id=9,
                league_id=3,
                season_year=1922,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
        )
        for league_season in league_seasons_in:
            sqla.session.add(league_season)
        sqla.session.commit()

        # Act
        league_seasons_out = test_repo.get_league_seasons_by_league(league_id=None)

    # Assert
    assert league_seasons_out == []


def test_get_league_seasons_by_league_when_league_id_arg_is_not_none_and_no_matching_league_seasons_found_should_return_empty_list(
        test_app, test_repo
):
    with test_app.app_context():
        # Arrange
        db_init.init_db()

        league_seasons_in = (
            LeagueSeason(
                id=1,
                league_id=1,
                season_year=1920,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
            LeagueSeason(
                id=2,
                league_id=1,
                season_year=1921,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
            LeagueSeason(
                id=3,
                league_id=1,
                season_year=1922,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
            LeagueSeason(
                id=4,
                league_id=2,
                season_year=1920,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
            LeagueSeason(
                id=5,
                league_id=2,
                season_year=1921,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
            LeagueSeason(
                id=6,
                league_id=2,
                season_year=1922,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
            LeagueSeason(
                id=7,
                league_id=3,
                season_year=1920,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
            LeagueSeason(
                id=8,
                league_id=3,
                season_year=1921,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
            LeagueSeason(
                id=9,
                league_id=3,
                season_year=1922,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
        )
        for league_season in league_seasons_in:
            sqla.session.add(league_season)
        sqla.session.commit()

        # Act
        league_seasons_out = test_repo.get_league_seasons_by_league(league_id=-1)

    # Assert
    assert league_seasons_out == []


def test_get_league_seasons_by_league_when_league_id_arg_is_not_none_and_matching_league_seasons_found_should_return_list_of_league_seasons_with_matching_league_id(
        test_app, test_repo
):
    with test_app.app_context():
        # Arrange
        db_init.init_db()

        league_seasons_in = (
            LeagueSeason(
                id=1,
                league_id=1,
                season_year=1920,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
            LeagueSeason(
                id=2,
                league_id=1,
                season_year=1921,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
            LeagueSeason(
                id=3,
                league_id=1,
                season_year=1922,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
            LeagueSeason(
                id=4,
                league_id=2,
                season_year=1920,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
            LeagueSeason(
                id=5,
                league_id=2,
                season_year=1921,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
            LeagueSeason(
                id=6,
                league_id=2,
                season_year=1922,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
            LeagueSeason(
                id=7,
                league_id=3,
                season_year=1920,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
            LeagueSeason(
                id=8,
                league_id=3,
                season_year=1921,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
            LeagueSeason(
                id=9,
                league_id=3,
                season_year=1922,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
        )
        for league_season in league_seasons_in:
            sqla.session.add(league_season)
        sqla.session.commit()

        # Act
        league_seasons_out = test_repo.get_league_seasons_by_league(league_id=2)

        # Assert
        assert league_seasons_out == [ls for ls in league_seasons_in if ls.league_id == 2]


def test_get_league_seasons_by_season_when_season_year_arg_is_none_should_return_empty_list(
        test_app, test_repo
):
    with test_app.app_context():
        # Arrange
        db_init.init_db()

        league_seasons_in = (
            LeagueSeason(
                id=1,
                league_id=1,
                season_year=1920,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
            LeagueSeason(
                id=2,
                league_id=1,
                season_year=1921,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
            LeagueSeason(
                id=3,
                league_id=1,
                season_year=1922,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
            LeagueSeason(
                id=4,
                league_id=2,
                season_year=1920,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
            LeagueSeason(
                id=5,
                league_id=2,
                season_year=1921,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
            LeagueSeason(
                id=6,
                league_id=2,
                season_year=1922,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
            LeagueSeason(
                id=7,
                league_id=3,
                season_year=1920,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
            LeagueSeason(
                id=8,
                league_id=3,
                season_year=1921,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
            LeagueSeason(
                id=9,
                league_id=3,
                season_year=1922,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
        )
        for league_season in league_seasons_in:
            sqla.session.add(league_season)
        sqla.session.commit()

        # Act
        league_seasons_out = test_repo.get_league_seasons_by_league(league_id=None)

        # Assert
        assert league_seasons_out == []


def test_get_league_seasons_by_season_when_season_year_arg_is_not_none_and_no_matching_league_seasons_found_should_return_empty_list(
        test_app, test_repo
):
    with test_app.app_context():
        # Arrange
        db_init.init_db()

        league_seasons_in = (
            LeagueSeason(
                id=1,
                league_id=1,
                season_year=1920,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
            LeagueSeason(
                id=2,
                league_id=1,
                season_year=1921,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
            LeagueSeason(
                id=3,
                league_id=1,
                season_year=1922,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
            LeagueSeason(
                id=4,
                league_id=2,
                season_year=1920,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
            LeagueSeason(
                id=5,
                league_id=2,
                season_year=1921,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
            LeagueSeason(
                id=6,
                league_id=2,
                season_year=1922,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
            LeagueSeason(
                id=7,
                league_id=3,
                season_year=1920,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
            LeagueSeason(
                id=8,
                league_id=3,
                season_year=1921,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
            LeagueSeason(
                id=9,
                league_id=3,
                season_year=1922,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
        )
        for league_season in league_seasons_in:
            sqla.session.add(league_season)
        sqla.session.commit()

        # Act
        league_seasons_out = test_repo.get_league_seasons_by_league(league_id=1919)

        # Assert
        assert league_seasons_out == []


def test_get_league_seasons_by_season_when_season_year_arg_is_not_none_and_matching_league_seasons_found_should_return_list_of_league_seasons_with_matching_season_year(
        test_app, test_repo
):
    with test_app.app_context():
        # Arrange
        db_init.init_db()

        league_seasons_in = (
            LeagueSeason(
                id=1,
                league_id=1,
                season_year=1920,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
            LeagueSeason(
                id=2,
                league_id=1,
                season_year=1921,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
            LeagueSeason(
                id=3,
                league_id=1,
                season_year=1922,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
            LeagueSeason(
                id=4,
                league_id=2,
                season_year=1920,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
            LeagueSeason(
                id=5,
                league_id=2,
                season_year=1921,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
            LeagueSeason(
                id=6,
                league_id=2,
                season_year=1922,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
            LeagueSeason(
                id=7,
                league_id=3,
                season_year=1920,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
            LeagueSeason(
                id=8,
                league_id=3,
                season_year=1921,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
            LeagueSeason(
                id=9,
                league_id=3,
                season_year=1922,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
        )
        for league_season in league_seasons_in:
            sqla.session.add(league_season)
        sqla.session.commit()

        # Act
        league_seasons_out = test_repo.get_league_seasons_by_season(season_year=1921)

        # Assert
        assert league_seasons_out == [ls for ls in league_seasons_in if ls.season_year == 1921]


def test_get_league_season_when_league_seasons_is_empty_should_return_none(
        test_app, test_repo
):
    with test_app.app_context():
        # Arrange
        db_init.init_db()

        # Act
        league_season_out = test_repo.get_league_season(id=3)

    # Assert
    assert league_season_out is None


def test_get_league_season_when_league_seasons_is_not_empty_and_league_season_is_not_found_should_return_none(
        test_app, test_repo
):
    with test_app.app_context():
        # Arrange
        db_init.init_db()

        league_seasons_in = (
            LeagueSeason(
                id=1,
                league_id=1,
                season_year=1920,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
            LeagueSeason(
                id=2,
                league_id=1,
                season_year=1921,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
            LeagueSeason(
                id=3,
                league_id=1,
                season_year=1922,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
        )
        for league_season in league_seasons_in:
            sqla.session.add(league_season)
        sqla.session.commit()

        # Act
        league_season_out = test_repo.get_league_season(id=-1)

    # Assert
    assert league_season_out is None


def test_get_league_season_when_league_seasons_is_not_empty_and_league_season_is_found_should_return_league_season(
        test_app, test_repo
):
    with test_app.app_context():
        # Arrange
        db_init.init_db()

        league_seasons_in = (
            LeagueSeason(
                id=1,
                league_id=1,
                season_year=1920,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
            LeagueSeason(
                id=2,
                league_id=1,
                season_year=1921,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
            LeagueSeason(
                id=3,
                league_id=1,
                season_year=1922,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
        )
        for league_season in league_seasons_in:
            sqla.session.add(league_season)
        sqla.session.commit()

        # Act
        league_season_out = test_repo.get_league_season(id=2)

    # Assert
    assert league_season_out is league_seasons_in[1]


def test_get_league_season_by_league_and_season_when_league_seasons_is_empty_should_return_none(
        test_app, test_repo
):
    with test_app.app_context():
        # Arrange
        db_init.init_db()

        # Act
        league_season_out = test_repo.get_league_season_by_league_and_season(league_id=1, season_year=1920)

    # Assert
    assert league_season_out is None


def test_get_league_season_by_league_and_season_when_league_seasons_is_not_empty_and_league_season_is_not_found_should_return_none(
        test_app, test_repo
):
    with test_app.app_context():
        # Arrange
        db_init.init_db()

        league_seasons_in = (
            LeagueSeason(
                id=1,
                league_id=1,
                season_year=1920,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
            LeagueSeason(
                id=2,
                league_id=2,
                season_year=1921,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
            LeagueSeason(
                id=3,
                league_id=3,
                season_year=1922,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
        )
        for league_season in league_seasons_in:
            sqla.session.add(league_season)
        sqla.session.commit()

        # Act
        league_season_out = test_repo.get_league_season_by_league_and_season(league_id=-1, season_year=1919)

    # Assert
    assert league_season_out is None


def test_get_league_season_by_league_and_season_when_league_seasons_is_not_empty_and_league_season_is_found_should_return_league_season(
        test_app, test_repo
):
    with test_app.app_context():
        # Arrange
        db_init.init_db()

        league_seasons_in = (
            LeagueSeason(
                id=1,
                league_id=1,
                season_year=1920,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
            LeagueSeason(
                id=2,
                league_id=2,
                season_year=1921,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
            LeagueSeason(
                id=3,
                league_id=3,
                season_year=1922,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
        )
        for league_season in league_seasons_in:
            sqla.session.add(league_season)
        sqla.session.commit()

        # Act
        league_season_out = test_repo.get_league_season_by_league_and_season(league_id=2, season_year=1921)

    # Assert
    assert league_season_out is league_seasons_in[1]


@patch('app.data.repositories.league_season_repository.try_commit')
@patch('app.data.repositories.league_season_repository.sqla')
def test_add_league_season_when_no_integrity_error_caught_should_add_league_season(
        fake_sqla, fake_try_commit, test_repo
):
    # Arrange
    league_season_in = LeagueSeason(
        league_id=1,
        season_year=1920,
        num_of_weeks_scheduled=0,
        num_of_weeks_completed=0
    )

    # Act
    league_season_out = test_repo.add_league_season(league_season_in)

    # Assert
    fake_sqla.session.add.assert_called_once_with(league_season_in)
    fake_try_commit.assert_called_once()
    assert league_season_out is league_season_in


@patch('app.data.repositories.league_season_repository.try_commit')
@patch('app.data.repositories.league_season_repository.sqla')
def test_add_league_season_when_integrity_error_caught_should_rollback_transaction_and_reraise_error(
        fake_sqla, fake_try_commit, test_repo
):
    # Arrange
    league_season_in = LeagueSeason(
        league_id=1,
        season_year=1920,
        num_of_weeks_scheduled=0,
        num_of_weeks_completed=0
    )
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
def test_add_league_seasons_when_league_seasons_arg_is_not_empty_and_no_integrity_error_caught_should_add_league_seasons(
        fake_sqla, fake_try_commit, test_repo
):
    # Arrange
    league_seasons_in = (
        LeagueSeason(
            id=1,
            league_id=1,
            season_year=1920,
            num_of_weeks_scheduled=0,
            num_of_weeks_completed=0
        ),
        LeagueSeason(
            id=2,
            league_id=2,
            season_year=1921,
            num_of_weeks_scheduled=0,
            num_of_weeks_completed=0
        ),
        LeagueSeason(
            id=3,
            league_id=3,
            season_year=1922,
            num_of_weeks_scheduled=0,
            num_of_weeks_completed=0
        ),
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
def test_add_league_seasons_when_league_seasons_arg_is_not_empty_and_integrity_error_caught_should_rollback_transaction_and_reraise_error(
        fake_sqla, fake_try_commit, test_repo
):
    # Arrange
    league_seasons_in = (
        LeagueSeason(
            league_id=1,
            season_year=1920,
            num_of_weeks_scheduled=0,
            num_of_weeks_completed=0
        ),
        LeagueSeason(
            league_id=2,
            season_year=1921,
            num_of_weeks_scheduled=0,
            num_of_weeks_completed=0
        ),
        LeagueSeason(
            league_id=3,
            season_year=1922,
            num_of_weeks_scheduled=0,
            num_of_weeks_completed=0
        ),
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


def test_league_season_exists_when_league_season_does_not_exist_should_return_false(
        test_app, test_repo
):
    with test_app.app_context():
        # Arrange
        db_init.init_db()

        league_seasons = (
            LeagueSeason(
                id=1,
                league_id=1,
                season_year=1920,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
            LeagueSeason(
                id=2,
                league_id=2,
                season_year=1921,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
            LeagueSeason(
                id=3,
                league_id=3,
                season_year=1922,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
        )
        for league_season in league_seasons:
            sqla.session.add(league_season)
        sqla.session.commit()

        # Act
        league_season_exists = test_repo.league_season_exists(id=-1)

    # Assert
    assert not league_season_exists


def test_league_season_exists_when_league_season_exists_should_return_true(
        test_app, test_repo
):
    with test_app.app_context():
        # Arrange
        db_init.init_db()

        league_seasons = (
            LeagueSeason(
                id=1,
                league_id=1,
                season_year=1920,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
            LeagueSeason(
                id=2,
                league_id=2,
                season_year=1921,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
            LeagueSeason(
                id=3,
                league_id=3,
                season_year=1922,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
        )
        for league_season in league_seasons:
            sqla.session.add(league_season)
        sqla.session.commit()

        # Act
        league_season_exists = test_repo.league_season_exists(id=2)

    # Assert
    assert league_season_exists


@patch('app.data.repositories.league_season_repository.try_commit')
@patch('app.data.repositories.league_season_repository.sqla')
@patch('app.data.repositories.league_season_repository.LeagueSeasonRepository.league_season_exists')
def test_update_league_season_when_no_league_season_exists_with_id_should_return_league_season_and_not_update_database(
        fake_league_season_exists, fake_sqla, fake_try_commit,
        test_repo
):
    # Arrange
    fake_league_season_exists.return_value = False

    # Act
    league_season = LeagueSeason(
        id=1,
        league_id=1,
        season_year=1920,
        num_of_weeks_scheduled=0,
        num_of_weeks_completed=0
    )

    try:
        league_season_updated = test_repo.update_league_season(league_season)
    except ValueError:
        assert False

    # Assert
    fake_sqla.session.add.assert_not_called()
    fake_try_commit.assert_not_called()
    assert isinstance(league_season_updated, LeagueSeason)
    assert league_season_updated.id == league_season.id
    assert league_season_updated.league_id == league_season.league_id
    assert league_season_updated.season_year == league_season.season_year
    assert league_season_updated.num_of_weeks_scheduled == league_season.num_of_weeks_scheduled
    assert league_season_updated.num_of_weeks_completed == league_season.num_of_weeks_completed


@patch('app.data.repositories.league_season_repository.try_commit')
@patch('app.data.repositories.league_season_repository.sqla')
@patch('app.data.repositories.league_season_repository.LeagueSeasonRepository.league_season_exists')
def test_update_league_season_when_league_season_exists_with_id_and_no_integrity_error_caught_should_return_league_season_and_update_database(
        fake_league_season_exists, fake_sqla, fake_try_commit,
        test_app, test_repo
):
    # Arrange
    with test_app.app_context():
        fake_league_season_exists.return_value = True

        db_init.init_db()

        league_seasons = (
            LeagueSeason(
                id=1,
                league_id=1,
                season_year=1920,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
            LeagueSeason(
                id=2,
                league_id=2,
                season_year=1921,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
            LeagueSeason(
                id=3,
                league_id=3,
                season_year=1922,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
        )
        for league_season in league_seasons:
            sqla.session.add(league_season)
        sqla.session.commit()

        new_league_season = LeagueSeason(
            id=2,
            league_id="L2",
            season_year=1923,
            num_of_weeks_scheduled=0,
            num_of_weeks_completed=0
        )

        # Act
        try:
            league_season_updated = test_repo.update_league_season(new_league_season)
        except IntegrityError:
            assert False

    # Assert
    old_league_season = league_seasons[1]
    fake_sqla.session.add.assert_called_once_with(old_league_season)
    fake_try_commit.assert_called_once()
    assert isinstance(league_season_updated, LeagueSeason)
    assert league_season_updated.id == new_league_season.id
    assert league_season_updated.league_id == new_league_season.league_id
    assert league_season_updated.season_year == new_league_season.season_year
    assert league_season_updated is new_league_season
    assert league_season_updated.num_of_weeks_scheduled == new_league_season.num_of_weeks_scheduled
    assert league_season_updated.num_of_weeks_completed == new_league_season.num_of_weeks_completed


@patch('app.data.repositories.league_season_repository.try_commit')
@patch('app.data.repositories.league_season_repository.sqla')
@patch('app.data.repositories.league_season_repository.LeagueSeasonRepository.league_season_exists')
def test_update_league_season_when_league_season_exists_with_id_and_integrity_error_caught_should_rollback_transaction_and_reraise_error(
        fake_league_season_exists, fake_sqla, fake_try_commit,
        test_app, test_repo
):
    # Arrange
    with test_app.app_context():
        fake_league_season_exists.return_value = True

        db_init.init_db()

        league_seasons = (
            LeagueSeason(
                id=1,
                league_id=1,
                season_year=1920,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
            LeagueSeason(
                id=2,
                league_id=2,
                season_year=1921,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
            LeagueSeason(
                id=3,
                league_id=3,
                season_year=1922,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
        )
        for league_season in league_seasons:
            sqla.session.add(league_season)
        sqla.session.commit()

        new_league_season = LeagueSeason(
            id=2,
            league_id="L2",
            season_year=1923,
            num_of_weeks_scheduled=0,
            num_of_weeks_completed=0
        )

        fake_try_commit.side_effect = IntegrityError('statement', 'params', Exception())

        # Act
        with pytest.raises(IntegrityError):
            league_season_updated = test_repo.update_league_season(new_league_season)

    # Assert
    old_league_season = league_seasons[1]
    fake_sqla.session.add.assert_called_once_with(old_league_season)
    fake_try_commit.assert_called_once()


@patch('app.data.repositories.league_season_repository.try_commit')
@patch('app.data.repositories.league_season_repository.sqla')
def test_delete_league_season_when_league_season_does_not_exist_should_return_none_and_not_delete_league_season_from_database(
        fake_sqla, fake_try_commit, test_app, test_repo
):
    with test_app.app_context():
        # Arrange
        db_init.init_db()

        league_seasons = (
            LeagueSeason(
                id=1,
                league_id=1,
                season_year=1920,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
            LeagueSeason(
                id=2,
                league_id=2,
                season_year=1921,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
            LeagueSeason(
                id=3,
                league_id=3,
                season_year=1922,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
        )
        for league_season in league_seasons:
            sqla.session.add(league_season)
        sqla.session.commit()

        # Act
        game_deleted = test_repo.delete_league_season(id=-1)

    # Assert
    assert game_deleted is None
    fake_sqla.session.delete.assert_not_called()
    fake_try_commit.assert_not_called()


@patch('app.data.repositories.league_season_repository.try_commit')
@patch('app.data.repositories.league_season_repository.sqla')
def test_delete_league_season_when_league_season_exists_and_integrity_error_not_caught_should_return_league_season_and_delete_league_season_from_database(
        fake_sqla, fake_try_commit, test_app, test_repo
):
    with test_app.app_context():
        # Arrange
        db_init.init_db()

        league_seasons = (
            LeagueSeason(
                id=1,
                league_id=1,
                season_year=1920,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
            LeagueSeason(
                id=2,
                league_id=2,
                season_year=1921,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
            LeagueSeason(
                id=3,
                league_id=3,
                season_year=1922,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
        )
        for league_season in league_seasons:
            sqla.session.add(league_season)
        sqla.session.commit()

        # Act
        try:
            league_season_deleted = test_repo.delete_league_season(id=2)
        except IntegrityError:
            assert False

    # Assert
    fake_sqla.session.delete.assert_called_once_with(league_season_deleted)
    fake_try_commit.assert_called_once()
    assert league_season_deleted is league_seasons[1]


@patch('app.data.repositories.league_season_repository.try_commit')
@patch('app.data.repositories.league_season_repository.sqla')
def test_delete_league_season_when_league_season_exists_and_integrity_error_caught_should_rollback_commit(
        fake_sqla, fake_try_commit, test_app, test_repo
):
    with test_app.app_context():
        # Arrange
        db_init.init_db()

        league_seasons = (
            LeagueSeason(
                id=1,
                league_id=1,
                season_year=1920,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
            LeagueSeason(
                id=2,
                league_id=2,
                season_year=1921,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
            LeagueSeason(
                id=3,
                league_id=3,
                season_year=1922,
                num_of_weeks_scheduled=0,
                num_of_weeks_completed=0
            ),
        )
        for league_season in league_seasons:
            sqla.session.add(league_season)
        sqla.session.commit()

        fake_try_commit.side_effect = IntegrityError('statement', 'params', Exception())

        # Act
        with pytest.raises(IntegrityError):
            league_season_deleted = test_repo.delete_league_season(id=2)

    # Assert
    fake_try_commit.assert_called_once()
