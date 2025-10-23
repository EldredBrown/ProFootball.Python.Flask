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


@patch('app.data.repositories.team_repository.Team')
def test_get_teams_should_get_teams(fake_team, test_app):
    with test_app.app_context():
        # Arrange
        teams_in = [
            Team(name="Chicago Cardinals"),
            Team(name="Decatur Staleys"),
            Team(name="Akron Pros"),
        ]
        fake_team.query.all.return_value = teams_in

        # Act
        test_repo = TeamRepository()
        teams_out = test_repo.get_teams()

    # Assert
    assert teams_out == teams_in


@patch('app.data.repositories.team_repository.Team')
def test_get_team_when_teams_is_empty_should_return_none(fake_team, test_app):
    with test_app.app_context():
        # Arrange
        teams_in = []
        fake_team.query.all.return_value = teams_in

        # Act
        test_repo = TeamRepository()
        team_out = test_repo.get_team(1)

    # Assert
    assert team_out is None


@patch('app.data.repositories.team_repository.Team')
def test_get_team_when_teams_is_not_empty_and_team_is_not_found_should_return_none(fake_team, test_app):
    with test_app.app_context():
        # Arrange
        teams_in = [
            Team(name="Chicago Cardinals"),
            Team(name="Decatur Staleys"),
            Team(name="Akron Pros"),
        ]
        fake_team.query.all.return_value = teams_in
        fake_team.query.get.return_value = None

        # Act
        test_repo = TeamRepository()

        id = len(teams_in) + 1
        team_out = test_repo.get_team(id)

    # Assert
    assert team_out is None


@patch('app.data.repositories.team_repository.Team')
def test_get_team_when_teams_is_not_empty_and_team_is_found_should_return_team(fake_team, test_app):
    with test_app.app_context():
        # Arrange
        teams_in = [
            Team(name="Chicago Cardinals"),
            Team(name="Decatur Staleys"),
            Team(name="Akron Pros"),
        ]
        fake_team.query.all.return_value = teams_in

        id = len(teams_in) - 1
        fake_team.query.get.return_value = teams_in[id]

        # Act
        test_repo = TeamRepository()

        team_out = test_repo.get_team(id)

    # Assert
    assert team_out is teams_in[id]


@patch('app.data.repositories.team_repository.Team')
def test_get_team_by_name_when_teams_is_empty_should_return_none(fake_team, test_app):
    with test_app.app_context():
        # Arrange
        teams_in = []
        fake_team.query.all.return_value = teams_in

        # Act
        test_repo = TeamRepository()
        team_out = test_repo.get_team_by_name("Chicago Cardinals")

    # Assert
    assert team_out is None


@patch('app.data.repositories.team_repository.Team')
def test_get_team_by_name_when_teams_is_not_empty_and_team_with_name_is_not_found_should_return_none(
        fake_team, test_app
):
    with test_app.app_context():
        # Arrange
        teams_in = [
            Team(name="Chicago Cardinals"),
            Team(name="Decatur Staleys"),
            Team(name="Akron Pros"),
        ]
        fake_team.query.all.return_value = teams_in
        fake_team.query.filter_by.return_value.first.return_value = None

        # Act
        test_repo = TeamRepository()
        team_out = test_repo.get_team_by_name("Canton Bulldogs")

    # Assert
    assert team_out is None


@patch('app.data.repositories.team_repository.Team')
def test_get_team_by_year_when_teams_is_not_empty_and_team_with_year_is_found_should_return_team(
        fake_team, test_app
):
    with test_app.app_context():
        # Arrange
        teams_in = [
            Team(name="Chicago Cardinals"),
            Team(name="Decatur Staleys"),
            Team(name="Akron Pros"),
        ]
        fake_team.query.all.return_value = teams_in
        fake_team.query.filter_by.return_value.first.return_value = teams_in[-1]

        # Act
        test_repo = TeamRepository()
        team_out = test_repo.get_team_by_name("Chicago Cardinals")

    # Assert
    assert team_out is teams_in[-1]


@patch('app.data.repositories.team_repository.sqla')
@patch('app.data.repositories.team_repository.team_factory')
def test_add_team_when_no_integrity_error_caught_should_add_team(fake_team_factory, fake_sqla, test_app):
    with test_app.app_context():
        # Arrange
        team_in = Team(name="Chicago Cardinals")
        fake_team_factory.create_team.return_value = team_in

        # Act
        test_repo = TeamRepository()
        kwargs = {
            'name': "Chicago Cardinals",
        }
        team_out = test_repo.add_team(**kwargs)

    # Assert
    fake_sqla.session.add.assert_called_once_with(team_in)
    fake_sqla.session.commit.assert_called_once()
    assert team_out is team_in


@patch('app.data.repositories.team_repository.sqla')
@patch('app.data.repositories.team_repository.team_factory')
def test_add_team_when_integrity_error_caught_should_rollback_transaction_and_reraise_error(
        fake_team_factory, fake_sqla, test_app
):
    with test_app.app_context():
        # Arrange
        team_in = Team(name="Chicago Cardinals")
        fake_team_factory.create_team.return_value = team_in
        fake_sqla.session.commit.side_effect = IntegrityError('statement', 'params', Exception())

        # Act
        test_repo = TeamRepository()
        kwargs = {
            'name': "Chicago Cardinals",
        }
        with pytest.raises(IntegrityError):
            team_out = test_repo.add_team(**kwargs)

    # Assert
    fake_sqla.session.rollback.assert_called_once()


@patch('app.data.repositories.team_repository.sqla')
def test_add_teams_when_teams_arg_is_empty_should_add_no_teams(fake_sqla, test_app):
    # Arrange
    with test_app.app_context():
        # Act
        test_repo = TeamRepository()

        team_args = ()
        teams_out = test_repo.add_teams(team_args)

    # Assert
    fake_sqla.session.add.assert_not_called()
    fake_sqla.session.commit.assert_called_once()
    assert teams_out == []


@patch('app.data.repositories.team_repository.sqla')
@patch('app.data.repositories.team_repository.team_factory')
def test_add_teams_when_teams_arg_is_not_empty_should_add_teams(fake_team_factory, fake_sqla, test_app):
    with test_app.app_context():
        # Arrange
        teams_in = [
            Team(name="Chicago Cardinals"),
            Team(name="Decatur Staleys"),
            Team(name="Akron Pros"),
        ]
        fake_team_factory.create_team.side_effect = teams_in

        # Act
        test_repo = TeamRepository()

        team_args = (
            {'name': "Chicago Cardinals"},
            {'name': "Decatur Staleys"},
            {'name': "Akron Pros"},
        )
        teams_out = test_repo.add_teams(team_args)

    # Assert
    fake_sqla.session.add.assert_has_calls([
        call(teams_in[0]),
        call(teams_in[1]),
        call(teams_in[2]),
    ])
    fake_sqla.session.commit.assert_called_once()
    assert teams_out == teams_in


@patch('app.data.repositories.team_repository.sqla')
@patch('app.data.repositories.team_repository.team_factory')
def test_add_teams_when_teams_arg_is_not_empty_and_no_integrity_error_caught_should_add_teams(
        fake_team_factory, fake_sqla, test_app
):
    with test_app.app_context():
        # Arrange
        teams_in = [
            Team(name="Chicago Cardinals"),
            Team(name="Decatur Staleys"),
            Team(name="Akron Pros"),
        ]
        fake_team_factory.create_team.side_effect = teams_in

        # Act
        test_repo = TeamRepository()

        team_args = (
            {'name': "Chicago Cardinals"},
            {'name': "Decatur Staleys"},
            {'name': "Akron Pros"},
        )
        teams_out = test_repo.add_teams(team_args)

    # Assert
    fake_sqla.session.add.assert_has_calls([
        call(teams_in[0]),
        call(teams_in[1]),
        call(teams_in[2]),
    ])
    fake_sqla.session.commit.assert_called_once()
    assert teams_out == teams_in


@patch('app.data.repositories.team_repository.sqla')
@patch('app.data.repositories.team_repository.team_factory')
def test_add_teams_when_teams_arg_is_not_empty_and_integrity_error_caught_should_rollback_transaction_and_reraise_error(
        fake_team_factory, fake_sqla, test_app
):
    with test_app.app_context():
        # Arrange
        teams_in = [
            Team(name="Chicago Cardinals"),
            Team(name="Decatur Staleys"),
            Team(name="Akron Pros"),
        ]
        fake_team_factory.create_team.side_effect = teams_in
        fake_sqla.session.commit.side_effect = IntegrityError('statement', 'params', Exception())

        # Act
        test_repo = TeamRepository()

        team_args = (
            {'name': "Chicago Cardinals"},
            {'name': "Decatur Staleys"},
            {'name': "Akron Pros"},
        )
        with pytest.raises(IntegrityError):
            teams_out = test_repo.add_teams(team_args)

    # Assert
    fake_sqla.session.rollback.assert_called_once()


@patch('app.data.repositories.team_repository.Team')
def test_team_exists_when_team_does_not_exist_should_return_false(fake_team, test_app):
    with test_app.app_context():
        # Arrange
        teams_in = [
            Team(name="Chicago Cardinals"),
            Team(name="Decatur Staleys"),
            Team(name="Akron Pros"),
        ]
        fake_team.query.all.return_value = teams_in
        fake_team.query.get.return_value = None

        # Act
        test_repo = TeamRepository()
        team_exists = test_repo.team_exists(id=1)

    # Assert
    assert not team_exists


@patch('app.data.repositories.team_repository.Team')
def test_team_exists_when_team_exists_should_return_true(fake_team, test_app):
    with test_app.app_context():
        # Arrange
        teams_in = [
            Team(name="Chicago Cardinals"),
            Team(name="Decatur Staleys"),
            Team(name="Akron Pros"),
        ]
        fake_team.query.all.return_value = teams_in
        fake_team.query.get.return_value = teams_in[1]

        # Act
        test_repo = TeamRepository()
        team_exists = test_repo.team_exists(id=1)

    # Assert
    assert team_exists


def test_update_team_when_id_not_in_kwargs_should_raise_value_error(test_app):
    # Arrange
    with test_app.app_context():
        # Act
        test_repo = TeamRepository()
        kwargs = {
            'name': "Chicago Cardinals",
        }
        with pytest.raises(ValueError) as err:
            team_updated = test_repo.update_team(**kwargs)

    # Assert
    assert err.value.args[0] == "ID must be provided for existing Team."


@patch('app.data.repositories.team_repository.sqla')
@patch('app.data.repositories.team_repository.TeamRepository.team_exists')
def test_update_team_when_id_is_in_kwargs_and_no_team_exists_with_id_should_return_team_and_not_update_database(
        fake_team_exists, fake_sqla, test_app
):
    with test_app.app_context():
        # Arrange
        fake_team_exists.return_value = False

        # Act
        test_repo = TeamRepository()
        kwargs = {
            'id': 1,
            'name': "Chicago Cardinals",
        }
        try:
            team_updated = test_repo.update_team(**kwargs)
        except ValueError as err:
            assert False

    # Assert
    fake_sqla.session.add.assert_not_called()
    fake_sqla.session.commit.assert_not_called()
    assert isinstance(team_updated, Team)
    assert team_updated.id == 1
    assert team_updated.name == "Chicago Cardinals"


@patch('app.data.repositories.team_repository.sqla')
@patch('app.data.repositories.team_repository.team_factory')
@patch('app.data.repositories.team_repository.Team')
@patch('app.data.repositories.team_repository.TeamRepository.team_exists')
def test_update_team_when_id_is_in_kwargs_and_team_exists_with_id_and_no_integrity_error_caught_should_return_team_and_update_database(
        fake_team_exists, fake_team, fake_team_factory, fake_sqla, test_app
):
    with test_app.app_context():
        # Arrange
        fake_team_exists.return_value = True

        teams = [
            Team(id=1, name="Chicago Cardinals"),
            Team(id=2, name="Decatur Staleys"),
            Team(id=3, name="Akron Pros"),
        ]
        fake_team.query.all.return_value = teams

        old_team = teams[1]
        fake_team.query.get.return_value = old_team

        new_team = Team(id=2, name="Canton Bulldogs")
        fake_team_factory.create_team.return_value = new_team

        # Act
        test_repo = TeamRepository()
        kwargs = {
            'id': 2,
            'name': "Canton Bulldogs",
        }
        try:
            team_updated = test_repo.update_team(**kwargs)
        except ValueError:
            assert False

    # Assert
    fake_sqla.session.add.assert_called_once_with(old_team)
    fake_sqla.session.commit.assert_called_once()
    assert isinstance(team_updated, Team)
    assert team_updated.id == 2
    assert team_updated.name == "Canton Bulldogs"
    assert team_updated is new_team


@patch('app.data.repositories.team_repository.sqla')
@patch('app.data.repositories.team_repository.team_factory')
@patch('app.data.repositories.team_repository.Team')
@patch('app.data.repositories.team_repository.TeamRepository.team_exists')
def test_update_team_when_id_is_in_kwargs_and_team_exists_with_id_and_integrity_error_caught_should_rollback_transaction_and_reraise_error(
        fake_team_exists, fake_team, fake_team_factory, fake_sqla, test_app
):
    with test_app.app_context():
        # Arrange
        fake_team_exists.return_value = True

        teams = [
            Team(id=1, name="Chicago Cardinals"),
            Team(id=2, name="Decatur Staleys"),
            Team(id=3, name="Akron Pros"),
        ]
        fake_team.query.all.return_value = teams

        old_team = teams[1]
        fake_team.query.get.return_value = old_team

        new_team = Team(id=2, name="Canton Bulldogs")
        fake_team_factory.create_team.return_value = new_team

        fake_sqla.session.commit.side_effect = IntegrityError('statement', 'params', Exception())

        # Act
        test_repo = TeamRepository()
        kwargs = {
            'id': 2,
            'name': "Canton Bulldogs",
        }
        with pytest.raises(IntegrityError):
            team_updated = test_repo.update_team(**kwargs)

    # Assert
    fake_sqla.session.rollback.assert_called_once()


@patch('app.data.repositories.team_repository.sqla')
@patch('app.data.repositories.team_repository.Team')
def test_delete_team_when_team_does_not_exist_should_return_none_and_not_delete_team_from_database(
        fake_team, fake_sqla, test_app
):
    with test_app.app_context():
        # Arrange
        teams_in = [
            Team(name="Chicago Cardinals"),
            Team(name="Decatur Staleys"),
            Team(name="Akron Pros"),
        ]
        fake_team.query.all.return_value = teams_in
        fake_team.query.get.return_value = None

        id = 1

        # Act
        test_repo = TeamRepository()
        team_deleted = test_repo.delete_team(id)

    # Assert
    assert team_deleted is None
    fake_sqla.session.delete.assert_not_called()
    fake_sqla.session.commit.assert_not_called()


@patch('app.data.repositories.team_repository.sqla')
@patch('app.data.repositories.team_repository.Team')
def test_delete_team_when_team_exists_should_return_team_and_delete_team_from_database(
        fake_team, fake_sqla, test_app
):
    with test_app.app_context():
        # Arrange
        teams_in = [
            Team(name="Chicago Cardinals"),
            Team(name="Decatur Staleys"),
            Team(name="Akron Pros"),
        ]
        fake_team.query.all.return_value = teams_in

        id = 1
        fake_team.query.get.return_value = teams_in[id]

        # Act
        test_repo = TeamRepository()
        team_deleted = test_repo.delete_team(id)

    # Assert
    fake_sqla.session.delete.assert_called_once_with(team_deleted)
    fake_sqla.session.commit.assert_called_once()
    assert team_deleted is teams_in[id]
