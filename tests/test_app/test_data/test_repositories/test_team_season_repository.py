from decimal import Decimal
from unittest.mock import patch, call, MagicMock

import pytest

from sqlalchemy.exc import IntegrityError

from app import sqla
from app.data.models.team_season import TeamSeason
from app.data.repositories.team_season_repository import TeamSeasonRepository
from instance.test_db import db_init
from test_app import create_app


@pytest.fixture
def test_app():
    return create_app()


@pytest.fixture
def test_repo():
    return TeamSeasonRepository()


def test_get_team_seasons_should_get_team_seasons(test_app, test_repo):
    with test_app.app_context():
        # Arrange
        db_init.init_db()

        team_seasons_in = [
            TeamSeason(
                team_id=1,
                season_id=1920,
                league_id=1
            ),
            TeamSeason(
                team_id=2,
                season_id=1920,
                league_id=1
            ),
            TeamSeason(
                team_id=3,
                season_id=1920,
                league_id=1
            ),
        ]
        for team_season in team_seasons_in:
            sqla.session.add(team_season)
        sqla.session.commit()

        # Act
        team_seasons_out = test_repo.get_team_seasons()

    # Assert
    assert team_seasons_out == team_seasons_in


def test_get_team_seasons_by_team_when_team_id_is_none_should_get_empty_list(test_app, test_repo):
    with test_app.app_context():
        # Arrange
        db_init.init_db()

        team_seasons_in = (
            TeamSeason(
                team_id=1,
                season_id=1920,
                league_id=1
            ),
            TeamSeason(
                team_id=2,
                season_id=1920,
                league_id=1
            ),
            TeamSeason(
                team_id=3,
                season_id=1920,
                league_id=1
            ),
            TeamSeason(
                team_id=1,
                season_id=1921,
                league_id=1
            ),
            TeamSeason(
                team_id=2,
                season_id=1921,
                league_id=1
            ),
            TeamSeason(
                team_id=3,
                season_id=1921,
                league_id=1
            ),
            TeamSeason(
                team_id=1,
                season_id=1922,
                league_id=1
            ),
            TeamSeason(
                team_id=2,
                season_id=1922,
                league_id=1
            ),
            TeamSeason(
                team_id=3,
                season_id=1922,
                league_id=1
            ),
        )
        for team_season in team_seasons_in:
            sqla.session.add(team_season)
        sqla.session.commit()

        # Act
        team_seasons_out = test_repo.get_team_seasons_by_team(team_id=None)

    # Assert
    assert team_seasons_out == []


def test_get_team_seasons_by_team_when_team_id_is_not_none_should_get_team_seasons_for_the_specified_team_id(
        test_app, test_repo
):
    with test_app.app_context():
        # Arrange
        db_init.init_db()

        team_seasons_in = (
            TeamSeason(
                team_id=1,
                season_id=1920,
                league_id=1
            ),
            TeamSeason(
                team_id=2,
                season_id=1920,
                league_id=1
            ),
            TeamSeason(
                team_id=3,
                season_id=1920,
                league_id=1
            ),
            TeamSeason(
                team_id=1,
                season_id=1921,
                league_id=1
            ),
            TeamSeason(
                team_id=2,
                season_id=1921,
                league_id=1
            ),
            TeamSeason(
                team_id=3,
                season_id=1921,
                league_id=1
            ),
            TeamSeason(
                team_id=1,
                season_id=1922,
                league_id=1
            ),
            TeamSeason(
                team_id=2,
                season_id=1922,
                league_id=1
            ),
            TeamSeason(
                team_id=3,
                season_id=1922,
                league_id=1
            ),
        )
        for team_season in team_seasons_in:
            sqla.session.add(team_season)
        sqla.session.commit()

        team_id = 2

        # Act
        team_seasons_out = test_repo.get_team_seasons_by_team(team_id=team_id)

        # Assert
        assert team_seasons_out == [ts for ts in team_seasons_in if ts.team_id == team_id]


def test_get_team_seasons_by_season_when_season_id_is_none_should_get_empty_list(test_app, test_repo):
    with test_app.app_context():
        # Arrange
        db_init.init_db()

        team_seasons_in = (
            TeamSeason(
                team_id=1,
                season_id=1920,
                league_id=1
            ),
            TeamSeason(
                team_id=2,
                season_id=1920,
                league_id=1
            ),
            TeamSeason(
                team_id=3,
                season_id=1920,
                league_id=1
            ),
            TeamSeason(
                team_id=1,
                season_id=1921,
                league_id=1
            ),
            TeamSeason(
                team_id=2,
                season_id=1921,
                league_id=1
            ),
            TeamSeason(
                team_id=3,
                season_id=1921,
                league_id=1
            ),
            TeamSeason(
                team_id=1,
                season_id=1922,
                league_id=1
            ),
            TeamSeason(
                team_id=2,
                season_id=1922,
                league_id=1
            ),
            TeamSeason(
                team_id=3,
                season_id=1922,
                league_id=1
            ),
        )
        for team_season in team_seasons_in:
            sqla.session.add(team_season)
        sqla.session.commit()

        # Act
        team_seasons_out = test_repo.get_team_seasons_by_season(season_id=None)

    # Assert
    assert team_seasons_out == []


def test_get_team_seasons_by_season_when_season_id_is_not_none_should_get_team_seasons_for_the_specified_season_id(
        test_app, test_repo
):
    with test_app.app_context():
        # Arrange
        db_init.init_db()

        team_seasons_in = (
            TeamSeason(
                team_id=1,
                season_id=1920,
                league_id=1
            ),
            TeamSeason(
                team_id=2,
                season_id=1920,
                league_id=1
            ),
            TeamSeason(
                team_id=3,
                season_id=1920,
                league_id=1
            ),
            TeamSeason(
                team_id=1,
                season_id=1921,
                league_id=1
            ),
            TeamSeason(
                team_id=2,
                season_id=1921,
                league_id=1
            ),
            TeamSeason(
                team_id=3,
                season_id=1921,
                league_id=1
            ),
            TeamSeason(
                team_id=1,
                season_id=1922,
                league_id=1
            ),
            TeamSeason(
                team_id=2,
                season_id=1922,
                league_id=1
            ),
            TeamSeason(
                team_id=3,
                season_id=1922,
                league_id=1
            ),
        )
        for team_season in team_seasons_in:
            sqla.session.add(team_season)
        sqla.session.commit()

        season_id = 1921

        # Act
        team_seasons_out = test_repo.get_team_seasons_by_season(season_id=season_id)

        # Assert
        assert team_seasons_out == [ts for ts in team_seasons_in if ts.season_id == season_id]


def test_get_team_season_when_team_seasons_is_empty_should_return_none(test_app, test_repo):
    with test_app.app_context():
        # Arrange
        db_init.init_db()

        # Act
        team_season_out = test_repo.get_team_season(id=1)

    # Assert
    assert team_season_out is None


def test_get_team_season_when_team_seasons_is_not_empty_and_team_season_is_not_found_should_return_none(
        test_app, test_repo
):
    with test_app.app_context():
        # Arrange
        db_init.init_db()

        team_seasons_in = (
            TeamSeason(
                id=1,
                team_id=1,
                season_id=1920,
                league_id=1
            ),
            TeamSeason(
                id=2,
                team_id=2,
                season_id=1920,
                league_id=1
            ),
            TeamSeason(
                id=3,
                team_id=3,
                season_id=1920,
                league_id=1
            ),
        )
        for team_season in team_seasons_in:
            sqla.session.add(team_season)
        sqla.session.commit()

        # Act
        team_season_out = test_repo.get_team_season(id=-1)

    # Assert
    assert team_season_out is None


def test_get_team_season_when_team_seasons_is_not_empty_and_team_season_is_found_should_return_team_season(
        test_app, test_repo
):
    with test_app.app_context():
        # Arrange
        db_init.init_db()

        team_seasons_in = (
            TeamSeason(
                id=1,
                team_id=1,
                season_id=1920,
                league_id=1
            ),
            TeamSeason(
                id=2,
                team_id=2,
                season_id=1920,
                league_id=1
            ),
            TeamSeason(
                id=3,
                team_id=3,
                season_id=1920,
                league_id=1
            ),
        )
        for team_season in team_seasons_in:
            sqla.session.add(team_season)
        sqla.session.commit()

        # Act
        team_season_out = test_repo.get_team_season(id=2)

    # Assert
    assert team_season_out is team_seasons_in[1]


def test_get_team_season_by_team_and_season_when_team_seasons_is_empty_should_return_none(
        test_app, test_repo
):
    with test_app.app_context():
        # Arrange
        db_init.init_db()

        # Act
        team_season_out = test_repo.get_team_season_by_team_and_season(team_id=1, season_id=1920)

    # Assert
    assert team_season_out is None


def test_get_team_season_by_league_and_season_when_team_seasons_is_not_empty_and_team_season_is_not_found_should_return_none(
        test_app, test_repo
):
    with test_app.app_context():
        # Arrange
        db_init.init_db()

        team_seasons_in = (
            TeamSeason(
                id=1,
                team_id=1,
                season_id=1920,
                league_id=1
            ),
            TeamSeason(
                id=2,
                team_id=2,
                season_id=1921,
                league_id=1
            ),
            TeamSeason(
                id=3,
                team_id=3,
                season_id=1922,
                league_id=1
            ),
        )
        for team_season in team_seasons_in:
            sqla.session.add(team_season)
        sqla.session.commit()

        # Act
        team_season_out = test_repo.get_team_season_by_team_and_season(team_id=-1, season_id=1919)

    # Assert
    assert team_season_out is None


def test_get_team_season_by_team_and_season_when_team_seasons_is_not_empty_and_team_season_is_found_should_return_team_season(
        test_app, test_repo
):
    with test_app.app_context():
        # Arrange
        db_init.init_db()

        team_seasons_in = (
            TeamSeason(
                id=1,
                team_id=1,
                season_id=1920,
                league_id=1
            ),
            TeamSeason(
                id=2,
                team_id=2,
                season_id=1921,
                league_id=1
            ),
            TeamSeason(
                id=3,
                team_id=3,
                season_id=1922,
                league_id=1
            ),
        )
        for team_season in team_seasons_in:
            sqla.session.add(team_season)
        sqla.session.commit()

        # Act
        team_season_out = test_repo.get_team_season_by_team_and_season(team_id=2, season_id=1921)

    # Assert
    assert team_season_out is team_seasons_in[1]


@patch('app.data.repositories.team_season_repository.try_commit')
@patch('app.data.repositories.team_season_repository.sqla')
def test_add_team_season_when_no_integrity_error_caught_should_add_team_season(
        fake_sqla, fake_try_commit, test_repo
):
    # Arrange
    team_season_in = TeamSeason(
        team_id=1,
        season_id=1920
    )

    # Act
    team_season_out = test_repo.add_team_season(team_season_in)

    # Assert
    fake_sqla.session.add.assert_called_once_with(team_season_in)
    fake_try_commit.assert_called_once()
    assert team_season_out is team_season_in


@patch('app.data.repositories.team_season_repository.try_commit')
@patch('app.data.repositories.team_season_repository.sqla')
def test_add_team_season_when_integrity_error_caught_should_rollback_transaction_and_reraise_error(
        fake_sqla, fake_try_commit, test_repo
):
    # Arrange
    team_season_in = TeamSeason(
        team_id=1,
        season_id=1920
    )
    fake_try_commit.side_effect = IntegrityError('statement', 'params', Exception())

    # Act
    with pytest.raises(IntegrityError):
        team_season_out = test_repo.add_team_season(team_season_in)

    # Assert
    fake_sqla.session.add.assert_called_once_with(team_season_in)
    fake_try_commit.assert_called_once()


@patch('app.data.repositories.team_season_repository.try_commit')
@patch('app.data.repositories.team_season_repository.sqla')
def test_add_team_seasons_when_team_seasons_arg_is_empty_should_add_no_team_seasons(
        fake_sqla, fake_try_commit, test_repo
):
    # Arrange
    team_seasons_in = ()

    # Act
    team_seasons_out = test_repo.add_team_seasons(team_seasons_in)

    # Assert
    fake_sqla.session.add.assert_not_called()
    fake_try_commit.assert_called_once()
    assert team_seasons_out == tuple()


@patch('app.data.repositories.team_season_repository.try_commit')
@patch('app.data.repositories.team_season_repository.sqla')
def test_add_team_seasons_when_team_seasons_arg_is_not_empty_and_no_integrity_error_caught_should_add_team_seasons(
        fake_sqla, fake_try_commit, test_repo
):
    # Arrange
    team_seasons_in = (
        TeamSeason(
            team_id=1,
            season_id=1920,
        ),
        TeamSeason(
            team_id=2,
            season_id=1921,
        ),
        TeamSeason(
            team_id=3,
            season_id=1922,
        ),
    )

    # Act
    team_seasons_out = test_repo.add_team_seasons(team_seasons_in)

    # Assert
    fake_sqla.session.add.assert_has_calls([
        call(team_seasons_in[0]),
        call(team_seasons_in[1]),
        call(team_seasons_in[2]),
    ])
    fake_try_commit.assert_called_once()
    assert team_seasons_out == team_seasons_in


@patch('app.data.repositories.team_season_repository.try_commit')
@patch('app.data.repositories.team_season_repository.sqla')
def test_add_team_seasons_when_team_seasons_arg_is_not_empty_and_integrity_error_caught_should_rollback_transaction_and_reraise_error(
        fake_sqla, fake_try_commit, test_repo
):
    # Arrange
    team_seasons_in = (
        TeamSeason(
            team_id=1,
            season_id=1920,
        ),
        TeamSeason(
            team_id=2,
            season_id=1921,
        ),
        TeamSeason(
            team_id=3,
            season_id=1922,
        ),
    )
    fake_try_commit.side_effect = IntegrityError('statement', 'params', Exception())

    # Act
    with pytest.raises(IntegrityError):
        team_seasons_out = test_repo.add_team_seasons(team_seasons_in)

    # Assert
    fake_sqla.session.add.assert_has_calls([
        call(team_seasons_in[0]),
        call(team_seasons_in[1]),
        call(team_seasons_in[2]),
    ])
    fake_try_commit.assert_called_once()


def test_team_season_exists_when_team_season_does_not_exist_should_return_false(test_app, test_repo):
    with test_app.app_context():
        # Arrange
        db_init.init_db()

        team_seasons = (
            TeamSeason(
                id=1,
                team_id=1,
                season_id=1920,
                league_id=1
            ),
            TeamSeason(
                id=2,
                team_id=2,
                season_id=1921,
                league_id=1
            ),
            TeamSeason(
                id=3,
                team_id=3,
                season_id=1922,
                league_id=1
            ),
        )
        for team_season in team_seasons:
            sqla.session.add(team_season)
        sqla.session.commit()

        # Act
        team_season_exists = test_repo.team_season_exists(id=-1)

    # Assert
    assert not team_season_exists


def test_team_season_exists_when_team_season_exists_should_return_true(test_app, test_repo):
    with test_app.app_context():
        # Arrange
        db_init.init_db()

        team_seasons = (
            TeamSeason(
                id=1,
                team_id=1,
                season_id=1920,
                league_id=1
            ),
            TeamSeason(
                id=2,
                team_id=2,
                season_id=1921,
                league_id=1
            ),
            TeamSeason(
                id=3,
                team_id=3,
                season_id=1922,
                league_id=1
            ),
        )
        for team_season in team_seasons:
            sqla.session.add(team_season)
        sqla.session.commit()

        # Act
        team_season_exists = test_repo.team_season_exists(id=2)

    # Assert
    assert team_season_exists


def test_team_season_exists_with_team_id_and_season_id_when_team_season_does_not_exist_should_return_false(
        test_app, test_repo
):
    with test_app.app_context():
        # Arrange
        db_init.init_db()

        team_seasons = (
            TeamSeason(
                id=1,
                team_id=1,
                season_id=1920,
                league_id=1
            ),
            TeamSeason(
                id=2,
                team_id=2,
                season_id=1921,
                league_id=1
            ),
            TeamSeason(
                id=3,
                team_id=3,
                season_id=1922,
                league_id=1
            ),
        )
        for team_season in team_seasons:
            sqla.session.add(team_season)
        sqla.session.commit()

        # Act
        team_season_exists = test_repo.team_season_exists_with_team_id_and_season_id(team_id=-1, season_id=1919)

    # Assert
    assert not team_season_exists


def test_team_season_exists_with_team_name_and_season_id_when_team_season_exists_should_return_true(
        test_app, test_repo
):
    with test_app.app_context():
        # Arrange
        db_init.init_db()

        team_seasons = (
            TeamSeason(
                id=1,
                team_id=1,
                season_id=1920,
                league_id=1
            ),
            TeamSeason(
                id=2,
                team_id=2,
                season_id=1921,
                league_id=1
            ),
            TeamSeason(
                id=3,
                team_id=3,
                season_id=1922,
                league_id=1
            ),
        )
        for team_season in team_seasons:
            sqla.session.add(team_season)
        sqla.session.commit()

        # Act
        team_season_exists = test_repo.team_season_exists_with_team_id_and_season_id(team_id=2, season_id=1921)

    # Assert
    assert team_season_exists


@patch('app.data.repositories.team_season_repository.try_commit')
@patch('app.data.repositories.team_season_repository.sqla')
@patch('app.data.repositories.team_season_repository.TeamSeasonRepository.team_season_exists')
def test_update_team_season_when_no_team_season_exists_with_id_should_return_team_season_and_not_update_database(
        fake_team_season_exists, fake_sqla, fake_try_commit,
        test_repo
):
    # Arrange
    fake_team_season_exists.return_value = False

    # Act
    test_repo = TeamSeasonRepository()
    team_season = MagicMock(TeamSeason)
    team_season.team_id = 1
    team_season.season_id = 1920
    team_season.league_id = 1
    try:
        team_season_updated = test_repo.update_team_season(team_season)
    except ValueError:
        assert False

    # Assert
    fake_sqla.session.add.assert_not_called()
    fake_try_commit.assert_not_called()
    assert isinstance(team_season_updated, TeamSeason)
    assert team_season_updated.team_id == team_season.team_id
    assert team_season_updated.season_id == team_season.season_id
    assert team_season_updated.league_id == team_season.league_id
    assert team_season_updated.conference_id == team_season.conference_id
    assert team_season_updated.division_id == team_season.division_id
    assert team_season_updated.games == team_season.games
    assert team_season_updated.wins == team_season.wins
    assert team_season_updated.losses == team_season.losses
    assert team_season_updated.ties == team_season.ties
    assert team_season_updated.winning_percentage == team_season.winning_percentage
    assert team_season_updated.points_for == team_season.points_for
    assert team_season_updated.points_against == team_season.points_against
    assert team_season_updated.expected_wins == team_season.expected_wins
    assert team_season_updated.expected_losses == team_season.expected_losses
    assert team_season_updated.offensive_average == team_season.offensive_average
    assert team_season_updated.offensive_factor == team_season.offensive_factor
    assert team_season_updated.offensive_index == team_season.offensive_index
    assert team_season_updated.defensive_average == team_season.defensive_average
    assert team_season_updated.defensive_factor == team_season.defensive_factor
    assert team_season_updated.defensive_index == team_season.defensive_index
    assert team_season_updated.final_expected_winning_percentage == team_season.final_expected_winning_percentage


@patch('app.data.repositories.team_season_repository.try_commit')
@patch('app.data.repositories.team_season_repository.sqla')
@patch('app.data.repositories.team_season_repository.TeamSeasonRepository.team_season_exists')
def test_update_team_season_when_team_season_exists_with_id_and_no_integrity_error_caught_should_return_team_season_and_update_database(
        fake_team_season_exists, fake_sqla,
        fake_try_commit, test_app, test_repo
):
    # Arrange
    with test_app.app_context():
        fake_team_season_exists.return_value = True

        db_init.init_db()

        team_seasons = (
            TeamSeason(
                id=1,
                team_id=1,
                season_id=1920,
                league_id=1,
                conference_id=1,
                division_id=1,
                games=1,
                wins=1,
                losses=1,
                ties=1,
                points_for=1,
                points_against=1,
                expected_wins=Decimal('1.0'),
                expected_losses=Decimal('1.0'),
                offensive_average=Decimal('1.00'),
                offensive_factor=Decimal('1.000'),
                offensive_index=Decimal('1.00'),
                defensive_average=Decimal('1.00'),
                defensive_factor=Decimal('1.000'),
                defensive_index=Decimal('1.00'),
                final_expected_winning_percentage=Decimal('1.000')
            ),
            TeamSeason(
                id=2,
                team_id=2,
                season_id=1921,
                league_id=2,
                conference_id=2,
                division_id=2,
                games=2,
                wins=2,
                losses=2,
                ties=2,
                points_for=2,
                points_against=2,
                expected_wins=Decimal('2.0'),
                expected_losses=Decimal('2.0'),
                offensive_average=Decimal('2.00'),
                offensive_factor=Decimal('2.000'),
                offensive_index=Decimal('2.00'),
                defensive_average=Decimal('2.00'),
                defensive_factor=Decimal('2.000'),
                defensive_index=Decimal('2.00'),
                final_expected_winning_percentage=Decimal('2.000')
            ),
            TeamSeason(
                id=3,
                team_id=3,
                season_id=1922,
                league_id=3,
                conference_id=3,
                division_id=3,
                games=3,
                wins=3,
                losses=3,
                ties=3,
                points_for=3,
                points_against=3,
                expected_wins=Decimal('3.0'),
                expected_losses=Decimal('3.0'),
                offensive_average=Decimal('3.00'),
                offensive_factor=Decimal('3.000'),
                offensive_index=Decimal('3.00'),
                defensive_average=Decimal('3.00'),
                defensive_factor=Decimal('3.000'),
                defensive_index=Decimal('3.00'),
                final_expected_winning_percentage=Decimal('3.000')
            ),
        )
        for team_season in team_seasons:
            sqla.session.add(team_season)
        sqla.session.commit()

        new_team_season = TeamSeason(
            id=2,
            team_id=4,
            season_id=4,
            league_id=4,
            conference_id=4,
            division_id=4,
            games=4,
            wins=4,
            losses=4,
            ties=4,
            points_for=4,
            points_against=4,
            expected_wins=Decimal('4.0'),
            expected_losses=Decimal('4.0'),
            offensive_average=Decimal('4.00'),
            offensive_factor=Decimal('4.000'),
            offensive_index=Decimal('4.00'),
            defensive_average=Decimal('4.00'),
            defensive_factor=Decimal('4.000'),
            defensive_index=Decimal('4.00'),
            final_expected_winning_percentage=Decimal('4.000')
        )

        # Act
        try:
            team_season_updated = test_repo.update_team_season(new_team_season)
        except IntegrityError:
            assert False

    # Assert
    old_team_season = team_seasons[1]
    fake_sqla.session.add.assert_called_once_with(old_team_season)
    fake_try_commit.assert_called_once()
    assert isinstance(team_season_updated, TeamSeason)
    assert team_season_updated.team_id == new_team_season.team_id
    assert team_season_updated.season_id == new_team_season.season_id
    assert team_season_updated.league_id == new_team_season.league_id
    assert team_season_updated.conference_id == new_team_season.conference_id
    assert team_season_updated.division_id == new_team_season.division_id
    assert team_season_updated.games == new_team_season.games
    assert team_season_updated.wins == new_team_season.wins
    assert team_season_updated.losses == new_team_season.losses
    assert team_season_updated.ties == new_team_season.ties
    assert team_season_updated.winning_percentage == new_team_season.winning_percentage
    assert team_season_updated.points_for == new_team_season.points_for
    assert team_season_updated.points_against == new_team_season.points_against
    assert team_season_updated.expected_wins == new_team_season.expected_wins
    assert team_season_updated.expected_losses == new_team_season.expected_losses
    assert team_season_updated.offensive_average == new_team_season.offensive_average
    assert team_season_updated.offensive_factor == new_team_season.offensive_factor
    assert team_season_updated.offensive_index == new_team_season.offensive_index
    assert team_season_updated.defensive_average == new_team_season.defensive_average
    assert team_season_updated.defensive_factor == new_team_season.defensive_factor
    assert team_season_updated.defensive_index == new_team_season.defensive_index
    assert team_season_updated.final_expected_winning_percentage == new_team_season.final_expected_winning_percentage
    assert team_season_updated is new_team_season


@patch('app.data.repositories.team_season_repository.try_commit')
@patch('app.data.repositories.team_season_repository.sqla')
@patch('app.data.repositories.team_season_repository.TeamSeasonRepository.team_season_exists')
def test_update_team_season_when_and_team_season_exists_with_id_and_integrity_error_caught_should_rollback_transaction_and_reraise_error(
        fake_team_season_exists, fake_sqla,
        fake_try_commit, test_app, test_repo
):
    # Arrange
    with test_app.app_context():
        fake_team_season_exists.return_value = True

        db_init.init_db()

        team_seasons = (
            TeamSeason(
                id=1,
                team_id=1,
                season_id=1920,
                league_id=1,
                conference_id=1,
                division_id=1,
                games=1,
                wins=1,
                losses=1,
                ties=1,
                points_for=1,
                points_against=1,
                expected_wins=Decimal('1.0'),
                expected_losses=Decimal('1.0'),
                offensive_average=Decimal('1.00'),
                offensive_factor=Decimal('1.000'),
                offensive_index=Decimal('1.00'),
                defensive_average=Decimal('1.00'),
                defensive_factor=Decimal('1.000'),
                defensive_index=Decimal('1.00'),
                final_expected_winning_percentage=Decimal('1.000')
            ),
            TeamSeason(
                id=2,
                team_id=2,
                season_id=1921,
                league_id=2,
                conference_id=2,
                division_id=2,
                games=2,
                wins=2,
                losses=2,
                ties=2,
                points_for=2,
                points_against=2,
                expected_wins=Decimal('2.0'),
                expected_losses=Decimal('2.0'),
                offensive_average=Decimal('2.00'),
                offensive_factor=Decimal('2.000'),
                offensive_index=Decimal('2.00'),
                defensive_average=Decimal('2.00'),
                defensive_factor=Decimal('2.000'),
                defensive_index=Decimal('2.00'),
                final_expected_winning_percentage=Decimal('2.000')
            ),
            TeamSeason(
                id=3,
                team_id=3,
                season_id=1922,
                league_id=3,
                conference_id=3,
                division_id=3,
                games=3,
                wins=3,
                losses=3,
                ties=3,
                points_for=3,
                points_against=3,
                expected_wins=Decimal('3.0'),
                expected_losses=Decimal('3.0'),
                offensive_average=Decimal('3.00'),
                offensive_factor=Decimal('3.000'),
                offensive_index=Decimal('3.00'),
                defensive_average=Decimal('3.00'),
                defensive_factor=Decimal('3.000'),
                defensive_index=Decimal('3.00'),
                final_expected_winning_percentage=Decimal('3.000')
            ),
        )
        for team_season in team_seasons:
            sqla.session.add(team_season)
        sqla.session.commit()

        new_team_season = TeamSeason(
            id=2,
            team_id=4,
            season_id=4,
            league_id=4,
            conference_id=4,
            division_id=4,
            games=4,
            wins=4,
            losses=4,
            ties=4,
            points_for=4,
            points_against=4,
            expected_wins=Decimal('4.0'),
            expected_losses=Decimal('4.0'),
            offensive_average=Decimal('4.00'),
            offensive_factor=Decimal('4.000'),
            offensive_index=Decimal('4.00'),
            defensive_average=Decimal('4.00'),
            defensive_factor=Decimal('4.000'),
            defensive_index=Decimal('4.00'),
            final_expected_winning_percentage=Decimal('4.000')
        )

        fake_try_commit.side_effect = IntegrityError('statement', 'params', Exception())

        # Act
        with pytest.raises(IntegrityError):
            team_season_updated = test_repo.update_team_season(new_team_season)

    # Assert
    old_team_season = team_seasons[1]
    fake_sqla.session.add.assert_called_once_with(old_team_season)
    fake_try_commit.assert_called_once()


@patch('app.data.repositories.team_season_repository.try_commit')
@patch('app.data.repositories.team_season_repository.sqla')
def test_delete_team_season_when_team_season_does_not_exist_should_return_none_and_not_delete_team_season_from_database(
        fake_sqla, fake_try_commit, test_app, test_repo
):
    with test_app.app_context():
        # Arrange
        db_init.init_db()

        team_seasons = (
            TeamSeason(
                id=1,
                team_id=1,
                season_id=1920,
                league_id=1
            ),
            TeamSeason(
                id=2,
                team_id=2,
                season_id=1921,
                league_id=1
            ),
            TeamSeason(
                id=3,
                team_id=3,
                season_id=1922,
                league_id=1
            ),
        )
        for team_season in team_seasons:
            sqla.session.add(team_season)
        sqla.session.commit()

        # Act
        game_deleted = test_repo.delete_team_season(id=-1)

    # Assert
    assert game_deleted is None
    fake_sqla.session.delete.assert_not_called()
    fake_try_commit.assert_not_called()


@patch('app.data.repositories.team_season_repository.try_commit')
@patch('app.data.repositories.team_season_repository.sqla')
def test_delete_team_season_when_team_season_exists_and_integrity_error_not_caught_should_return_team_season_and_delete_team_season_from_database(
        fake_sqla, fake_try_commit, test_app, test_repo
):
    with test_app.app_context():
        # Arrange
        db_init.init_db()

        team_seasons = (
            TeamSeason(
                id=1,
                team_id=1,
                season_id=1920,
                league_id=1
            ),
            TeamSeason(
                id=2,
                team_id=2,
                season_id=1921,
                league_id=1
            ),
            TeamSeason(
                id=3,
                team_id=3,
                season_id=1922,
                league_id=1
            ),
        )
        for team_season in team_seasons:
            sqla.session.add(team_season)
        sqla.session.commit()

        # Act
        try:
            team_season_deleted = test_repo.delete_team_season(id=2)
        except IntegrityError:
            assert False

    # Assert
    fake_sqla.session.delete.assert_called_once_with(team_season_deleted)
    fake_try_commit.assert_called_once()
    assert team_season_deleted is team_seasons[1]


@patch('app.data.repositories.team_season_repository.try_commit')
@patch('app.data.repositories.team_season_repository.sqla')
def test_delete_team_season_when_team_season_exists_and_integrity_error_caught_should_rollback_commit(
        fake_sqla, fake_try_commit, test_app, test_repo
):
    with test_app.app_context():
        # Arrange
        db_init.init_db()

        team_seasons = (
            TeamSeason(
                id=1,
                team_id=1,
                season_id=1920,
                league_id=1
            ),
            TeamSeason(
                id=2,
                team_id=2,
                season_id=1921,
                league_id=1
            ),
            TeamSeason(
                id=3,
                team_id=3,
                season_id=1922,
                league_id=1
            ),
        )
        for team_season in team_seasons:
            sqla.session.add(team_season)
        sqla.session.commit()

        fake_try_commit.side_effect = IntegrityError('statement', 'params', Exception())

        # Act
        with pytest.raises(IntegrityError):
            team_season_deleted = test_repo.delete_team_season(id=2)

    # Assert
    fake_try_commit.assert_called_once()
