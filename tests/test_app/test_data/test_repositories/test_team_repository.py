from unittest.mock import patch, call

import pytest

from sqlalchemy.exc import IntegrityError

from test_app import create_app

from app.data.models.season import Season
from app.data.models.team import Team
from app.data.models.game import Game
from app.data.models.league_season import LeagueSeason
from app.data.models.team_season import TeamSeason
from app.data.repositories.team_repository import TeamRepository


@pytest.fixture
def test_app():
    return create_app()


@pytest.fixture
def test_repo():
    return TeamRepository()


@patch('app.data.repositories.team_repository.Team')
def test_get_teams_should_get_teams(fake_team, test_app, test_repo):
    with test_app.app_context():
        # Arrange
        teams_in = [
            Team(name="Team 1"),
            Team(name="Team 2"),
            Team(name="Team 3"),
        ]
        fake_team.query.all.return_value = teams_in

        # Act
        teams_out = test_repo.get_teams()

    # Assert
    assert teams_out == teams_in


@patch('app.data.repositories.team_repository.Team')
def test_get_team_when_teams_is_empty_should_return_none(fake_team, test_app, test_repo):
    with test_app.app_context():
        # Arrange
        teams_in = []
        fake_team.query.all.return_value = teams_in

        # Act
        team_out = test_repo.get_team(1)

    # Assert
    assert team_out is None


@patch('app.data.repositories.team_repository.Team')
def test_get_team_when_teams_is_not_empty_and_team_is_not_found_should_return_none(fake_team, test_app, test_repo):
    with test_app.app_context():
        # Arrange
        teams_in = [
            Team(name="Team 1"),
            Team(name="Team 2"),
            Team(name="Team 3"),
        ]
        fake_team.query.all.return_value = teams_in
        fake_team.query.get.return_value = None

        # Act
        id = len(teams_in) + 1
        team_out = test_repo.get_team(id)

    # Assert
    assert team_out is None


@patch('app.data.repositories.team_repository.Team')
def test_get_team_when_teams_is_not_empty_and_team_is_found_should_return_team(fake_team, test_app, test_repo):
    with test_app.app_context():
        # Arrange
        teams_in = [
            Team(name="Team 1"),
            Team(name="Team 2"),
            Team(name="Team 3"),
        ]
        fake_team.query.all.return_value = teams_in

        id = len(teams_in) - 1
        fake_team.query.get.return_value = teams_in[id]

        # Act
        team_out = test_repo.get_team(id)

    # Assert
    assert team_out is teams_in[id]


@patch('app.data.repositories.team_repository.Team')
def test_get_team_by_name_when_teams_is_empty_should_return_none(fake_team, test_app, test_repo):
    with test_app.app_context():
        # Arrange
        teams_in = []
        fake_team.query.all.return_value = teams_in

        # Act
        team_out = test_repo.get_team_by_name("Chicago Cardinals")

    # Assert
    assert team_out is None


@patch('app.data.repositories.team_repository.Team')
def test_get_team_by_name_when_teams_is_not_empty_and_team_with_name_is_not_found_should_return_none(
        fake_team, test_app, test_repo
):
    with test_app.app_context():
        # Arrange
        teams_in = [
            Team(name="Team 1"),
            Team(name="Team 2"),
            Team(name="Team 3"),
        ]
        fake_team.query.all.return_value = teams_in
        fake_team.query.filter_by.return_value.first.return_value = None

        # Act
        team_out = test_repo.get_team_by_name("Canton Bulldogs")

    # Assert
    assert team_out is None


@patch('app.data.repositories.team_repository.Team')
def test_get_team_by_year_when_teams_is_not_empty_and_team_with_year_is_found_should_return_team(
        fake_team, test_app, test_repo
):
    with test_app.app_context():
        # Arrange
        teams_in = [
            Team(name="Team 1"),
            Team(name="Team 2"),
            Team(name="Team 3"),
        ]
        fake_team.query.all.return_value = teams_in
        fake_team.query.filter_by.return_value.first.return_value = teams_in[-1]

        # Act
        team_out = test_repo.get_team_by_name("Chicago Cardinals")

    # Assert
    assert team_out is teams_in[-1]


@patch('app.data.repositories.team_repository.sqla')
def test_add_team_when_no_integrity_error_caught_should_add_team(fake_sqla, test_app, test_repo):
    with test_app.app_context():
        # Arrange
        team_in = Team(name="Team")

        # Act
        team_out = test_repo.add_team(team_in)

    # Assert
    fake_sqla.session.add.assert_called_once_with(team_in)
    fake_sqla.session.commit.assert_called_once()
    assert team_out is team_in


@patch('app.data.repositories.team_repository.sqla')
def test_add_team_when_integrity_error_caught_should_rollback_transaction_and_reraise_error(
        fake_sqla, test_app, test_repo
):
    with test_app.app_context():
        # Arrange
        team_in = Team(name="Team")
        fake_sqla.session.commit.side_effect = IntegrityError('statement', 'params', Exception())

        # Act
        with pytest.raises(IntegrityError):
            team_out = test_repo.add_team(team_in)

    # Assert
    fake_sqla.session.rollback.assert_called_once()


@patch('app.data.repositories.team_repository.sqla')
def test_add_teams_when_teams_arg_is_empty_should_add_no_teams(fake_sqla, test_app, test_repo):
    with test_app.app_context():
        # Arrange
        teams_in = ()

        # Act
        teams_out = test_repo.add_teams(teams_in)

    # Assert
    fake_sqla.session.add.assert_not_called()
    fake_sqla.session.commit.assert_called_once()
    assert teams_out == tuple()


@patch('app.data.repositories.team_repository.sqla')
def test_add_teams_when_teams_arg_is_not_empty_should_add_teams(fake_sqla, test_app, test_repo):
    with test_app.app_context():
        # Arrange
        teams_in = (
            Team(name="Team 1"),
            Team(name="Team 2"),
            Team(name="Team 3"),
        )

        # Act
        teams_out = test_repo.add_teams(teams_in)

    # Assert
    fake_sqla.session.add.assert_has_calls([
        call(teams_in[0]),
        call(teams_in[1]),
        call(teams_in[2]),
    ])
    fake_sqla.session.commit.assert_called_once()
    assert teams_out == teams_in


@patch('app.data.repositories.team_repository.sqla')
def test_add_teams_when_teams_arg_is_not_empty_and_no_integrity_error_caught_should_add_teams(
        fake_sqla, test_app, test_repo
):
    with test_app.app_context():
        # Arrange
        teams_in = (
            Team(name="Team 1"),
            Team(name="Team 2"),
            Team(name="Team 3"),
        )

        # Act
        teams_out = test_repo.add_teams(teams_in)

    # Assert
    fake_sqla.session.add.assert_has_calls([
        call(teams_in[0]),
        call(teams_in[1]),
        call(teams_in[2]),
    ])
    fake_sqla.session.commit.assert_called_once()
    assert teams_out == teams_in


@patch('app.data.repositories.team_repository.sqla')
def test_add_teams_when_teams_arg_is_not_empty_and_integrity_error_caught_should_rollback_transaction_and_reraise_error(
        fake_sqla, test_app, test_repo
):
    with test_app.app_context():
        # Arrange
        teams_in = (
            Team(name="Team 1"),
            Team(name="Team 2"),
            Team(name="Team 3"),
        )
        fake_sqla.session.commit.side_effect = IntegrityError('statement', 'params', Exception())

        # Act
        with pytest.raises(IntegrityError):
            teams_out = test_repo.add_teams(teams_in)

    # Assert
    fake_sqla.session.rollback.assert_called_once()


@patch('app.data.repositories.team_repository.Team')
def test_team_exists_when_team_does_not_exist_should_return_false(fake_team, test_app, test_repo):
    with test_app.app_context():
        # Arrange
        teams = [
            Team(name="Team 1"),
            Team(name="Team 2"),
            Team(name="Team 3"),
        ]
        fake_team.query.all.return_value = teams
        fake_team.query.get.return_value = None

        # Act
        team_exists = test_repo.team_exists(id=1)

    # Assert
    assert not team_exists


@patch('app.data.repositories.team_repository.Team')
def test_team_exists_when_team_exists_should_return_true(fake_team, test_app, test_repo):
    with test_app.app_context():
        # Arrange
        teams = [
            Team(name="Team 1"),
            Team(name="Team 2"),
            Team(name="Team 3"),
        ]
        fake_team.query.all.return_value = teams
        fake_team.query.get.return_value = teams[1]

        # Act
        team_exists = test_repo.team_exists(id=1)

    # Assert
    assert team_exists


@patch('app.data.repositories.team_repository.sqla')
@patch('app.data.repositories.team_repository.TeamRepository.team_exists')
def test_update_team_when_no_team_exists_with_id_should_return_team_and_not_update_database(
        fake_team_exists, fake_sqla, test_app, test_repo
):
    with test_app.app_context():
        # Arrange
        fake_team_exists.return_value = False

        # Act
        team = Team(id=1, name="Team")
        try:
            team_updated = test_repo.update_team(team)
        except ValueError:
            assert False

    # Assert
    fake_sqla.session.add.assert_not_called()
    fake_sqla.session.commit.assert_not_called()
    assert isinstance(team_updated, Team)
    assert team_updated.id == team.id
    assert team_updated.name == team.name


@patch('app.data.repositories.team_repository.sqla')
@patch('app.data.repositories.team_repository.Team')
@patch('app.data.repositories.team_repository.TeamRepository.team_exists')
def test_update_team_when_team_exists_with_id_and_no_integrity_error_caught_should_return_team_and_update_database(
        fake_team_exists, fake_team, fake_sqla, test_app, test_repo
):
    with test_app.app_context():
        # Arrange
        fake_team_exists.return_value = True

        teams = [
            Team(id=1, name="Team 1"),
            Team(id=2, name="Team 2"),
            Team(id=3, name="Team 3"),
        ]
        fake_team.query.all.return_value = teams

        old_team = teams[1]
        fake_team.query.get.return_value = old_team

        new_team = Team(id=2, name="Team 4")

        # Act
        try:
            team_updated = test_repo.update_team(new_team)
        except IntegrityError:
            assert False

    # Assert
    fake_sqla.session.add.assert_called_once_with(old_team)
    fake_sqla.session.commit.assert_called_once()
    assert isinstance(team_updated, Team)
    assert team_updated.id == new_team.id
    assert team_updated.name == new_team.name
    assert team_updated is new_team


@patch('app.data.repositories.team_repository.sqla')
@patch('app.data.repositories.team_repository.Team')
@patch('app.data.repositories.team_repository.TeamRepository.team_exists')
def test_update_team_when_team_exists_with_id_and_integrity_error_caught_should_rollback_transaction_and_reraise_error(
        fake_team_exists, fake_team, fake_sqla, test_app, test_repo
):
    with test_app.app_context():
        # Arrange
        fake_team_exists.return_value = True

        teams = [
            Team(id=1, name="Team 1"),
            Team(id=2, name="Team 2"),
            Team(id=3, name="Team 3"),
        ]
        fake_team.query.all.return_value = teams

        old_team = teams[1]
        fake_team.query.get.return_value = old_team

        new_team = Team(id=2, name="Team 4")

        fake_sqla.session.commit.side_effect = IntegrityError('statement', 'params', Exception())

        # Act
        with pytest.raises(IntegrityError):
            team_updated = test_repo.update_team(new_team)

    # Assert
    fake_sqla.session.rollback.assert_called_once()


@patch('app.data.repositories.team_repository.sqla')
@patch('app.data.repositories.team_repository.Team')
def test_delete_team_when_team_does_not_exist_should_return_none_and_not_delete_team_from_database(
        fake_team, fake_sqla, test_app, test_repo
):
    with test_app.app_context():
        # Arrange
        teams = [
            Team(name="Team 1"),
            Team(name="Team 2"),
            Team(name="Team 3"),
        ]
        fake_team.query.all.return_value = teams
        fake_team.query.get.return_value = None

        id = 1

        # Act
        team_deleted = test_repo.delete_team(id)

    # Assert
    assert team_deleted is None
    fake_sqla.session.delete.assert_not_called()
    fake_sqla.session.commit.assert_not_called()


@patch('app.data.repositories.team_repository.sqla')
@patch('app.data.repositories.team_repository.Team')
def test_delete_team_when_team_exists_and_integrity_error_not_caught_should_return_team_and_delete_team_from_database(
        fake_team, fake_sqla, test_app, test_repo
):
    with test_app.app_context():
        # Arrange
        teams = [
            Team(name="Team 1"),
            Team(name="Team 2"),
            Team(name="Team 3"),
        ]
        fake_team.query.all.return_value = teams

        id = 1
        fake_team.query.get.return_value = teams[id]

        # Act
        try:
            team_deleted = test_repo.delete_team(id)
        except IntegrityError:
            assert False

    # Assert
    fake_sqla.session.delete.assert_called_once_with(team_deleted)
    fake_sqla.session.commit.assert_called_once()
    assert team_deleted is teams[id]


@patch('app.data.repositories.team_repository.sqla')
@patch('app.data.repositories.team_repository.Team')
def test_delete_team_when_team_exists_and_integrity_error_caught_should_rollback_commit(
        fake_team, fake_sqla, test_app, test_repo
):
    with test_app.app_context():
        # Arrange
        teams = [
            Team(name="Team 1"),
            Team(name="Team 2"),
            Team(name="Team 3"),
        ]
        fake_team.query.all.return_value = teams

        id = 1
        fake_team.query.get.return_value = teams[id]

        fake_sqla.session.commit.side_effect = IntegrityError('statement', 'params', Exception())

        # Act
        with pytest.raises(IntegrityError):
            team_deleted = test_repo.delete_team(id)

    # Assert
    fake_sqla.session.rollback.assert_called_once()
