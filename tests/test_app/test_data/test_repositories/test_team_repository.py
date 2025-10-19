import pytest

from unittest.mock import patch, call

from app import create_app
from app.data.models.team import Team
from app.data.models.game import Game
from app.data.models.league_season import LeagueSeason
from app.data.models.team_season import TeamSeason
from app.data.repositories.team_repository import TeamRepository


@patch('app.data.repositories.team_repository.Team')
def test_get_teams_should_get_teams(fake_team):
    # Act
    test_app = create_app()
    with test_app.app_context():
        test_repo = TeamRepository()
        teams = test_repo.get_teams()

    # Assert
    fake_team.query.all.assert_called_once()
    assert teams == fake_team.query.all.return_value


@patch('app.data.repositories.team_repository.TeamRepository.get_teams')
def test_get_team_when_teams_is_empty_should_return_none(fake_get_teams):
    test_app = create_app()
    with test_app.app_context():
        # Arrange
        teams = []
        fake_get_teams.return_value = teams

        # Act
        test_repo = TeamRepository()
        team = test_repo.get_team(id=1)

    # Assert
    assert team is None


@patch('app.data.repositories.team_repository.Team')
@patch('app.data.repositories.team_repository.TeamRepository.get_teams')
def test_get_team_when_teams_is_not_empty_and_team_is_not_found_should_return_none(
        fake_get_teams, fake_team
):
    test_app = create_app()
    with test_app.app_context():
        # Arrange
        teams = [
            Team(name="A"),
            Team(name="B"),
            Team(name="C"),
        ]
        fake_get_teams.return_value = teams

        id = len(teams) + 1

        # Act
        test_repo = TeamRepository()
        team = test_repo.get_team(id=id)

    # Assert
    fake_team.query.get.assert_called_once_with(id)
    assert team == fake_team.query.get.return_value


@patch('app.data.repositories.team_repository.Team')
@patch('app.data.repositories.team_repository.TeamRepository.get_teams')
def test_get_team_when_teams_is_not_empty_and_team_is_found_should_return_team(fake_get_teams, fake_team):
    test_app = create_app()
    with test_app.app_context():
        # Arrange
        teams = [
            Team(name="A"),
            Team(name="B"),
            Team(name="C"),
        ]
        fake_get_teams.return_value = teams

        id = len(teams) - 1

        # Act
        test_repo = TeamRepository()
        team = test_repo.get_team(id=id)

    # Assert
    fake_team.query.get.assert_called_once_with(id)
    assert team == fake_team.query.get.return_value


@patch('app.data.repositories.team_repository.TeamRepository.get_teams')
def test_get_team_by_name_when_teams_is_empty_should_return_none(fake_get_teams):
    test_app = create_app()
    with test_app.app_context():
        # Arrange
        teams = []
        fake_get_teams.return_value = teams

        # Act
        test_repo = TeamRepository()
        team = test_repo.get_team_by_name(name="A")

    # Assert
    assert team is None


@patch('app.data.repositories.team_repository.Team')
@patch('app.data.repositories.team_repository.TeamRepository.get_teams')
def test_get_team_by_name_when_teams_is_not_empty_and_team_with_short_name_is_not_found_should_return_none(
        fake_get_teams, fake_team
):
    test_app = create_app()
    with test_app.app_context():
        # Arrange
        teams = [
            Team(name="A"),
            Team(name="B"),
            Team(name="C"),
        ]
        fake_get_teams.return_value = teams

        # Act
        test_repo = TeamRepository()
        team = test_repo.get_team_by_name(name="D")

    # Assert
    fake_team.query.filter_by.assert_called_once_with(name="D")
    fake_team.query.filter_by.return_value.first.assert_called_once_with()
    assert team == fake_team.query.filter_by.return_value.first.return_value


@patch('app.data.repositories.team_repository.Team')
@patch('app.data.repositories.team_repository.TeamRepository.get_teams')
def test_get_team_by_name_when_teams_is_not_empty_and_team_with_short_name_is_found_should_return_team(
        fake_get_teams, fake_team
):
    test_app = create_app()
    with test_app.app_context():
        # Arrange
        teams = [
            Team(name="A"),
            Team(name="B"),
            Team(name="C"),
        ]
        fake_get_teams.return_value = teams

        # Act
        test_repo = TeamRepository()
        team = test_repo.get_team_by_name(name="B")

    # Assert
    fake_team.query.filter_by.assert_called_once_with(name="B")
    fake_team.query.filter_by.return_value.first.assert_called_once_with()
    assert team == fake_team.query.filter_by.return_value.first.return_value


@patch('app.data.repositories.team_repository.sqla')
def test_add_team_should_add_team(fake_sqla):
    # Arrange
    test_app = create_app()
    with test_app.app_context():
        # Act
        test_repo = TeamRepository()
        team_in = Team(name="D")
        team_out = test_repo.add_team(team_in)

    # Assert
    fake_sqla.session.add.assert_called_once_with(team_in)
    fake_sqla.session.commit.assert_called_once()
    assert team_out is team_in


@patch('app.data.repositories.team_repository.sqla')
def test_add_teams_when_teams_arg_is_empty_should_add_no_teams(fake_sqla):
    # Arrange
    test_app = create_app()
    with test_app.app_context():
        # Act
        test_repo = TeamRepository()
        teams_in = ()
        teams_out = test_repo.add_teams(teams_in)

    # Assert
    fake_sqla.session.add.assert_not_called()
    fake_sqla.session.commit.assert_called_once()
    assert teams_out is teams_in


@patch('app.data.repositories.team_repository.sqla')
def test_add_teams_when_teams_arg_is_not_empty_should_add_teams(fake_sqla):
    # Arrange
    test_app = create_app()
    with test_app.app_context():
        # Act
        test_repo = TeamRepository()
        teams_in = (
            Team(name="D"),
            Team(name="E"),
            Team(name="F"),
        )
        teams_out = test_repo.add_teams(teams_in)

    # Assert
    fake_sqla.session.add.assert_has_calls([
        call(teams_in[0]),
        call(teams_in[1]),
        call(teams_in[2]),
    ])
    fake_sqla.session.commit.assert_called_once()
    assert teams_out is teams_in


@patch('app.data.repositories.team_repository.sqla')
@patch('app.data.repositories.team_repository.exists')
def test_team_exists_should_query_database(fake_exists, fake_sqla):
    # Arrange
    test_app = create_app()
    with test_app.app_context():
        # Act
        test_repo = TeamRepository()
        team_exists = test_repo.team_exists(id=1)

    # Assert
    fake_exists.assert_called_once()
    fake_exists.return_value.where.assert_called_once()
    fake_sqla.session.query.assert_called_once_with(fake_exists.return_value.where.return_value)
    fake_sqla.session.query.return_value.scalar.assert_called_once()
    assert team_exists == fake_sqla.session.query.return_value.scalar.return_value


@patch('app.data.repositories.team_repository.TeamRepository.team_exists')
def test_update_team_when_team_does_not_exist_should_return_team(fake_team_exists):
    # Arrange
    fake_team_exists.return_value = False

    test_app = create_app()
    with test_app.app_context():
        # Act
        test_repo = TeamRepository()
        team_to_update = Team(id=1, name="A")
        team_updated = test_repo.update_team(team_to_update)

    # Assert
    fake_team_exists.assert_called_once_with(team_to_update.id)
    assert team_updated is team_to_update


@patch('app.data.repositories.team_repository.sqla')
@patch('app.data.repositories.team_repository.TeamRepository.get_team')
@patch('app.data.repositories.team_repository.TeamRepository.team_exists')
def test_update_team_when_team_exists_should_update_and_return_team(
        fake_team_exists, fake_get_team, fake_sqla
):
    # Arrange
    test_app = create_app()
    with test_app.app_context():
        fake_team_exists.return_value = True
        old_team = Team(id=1, name="A")
        fake_get_team.return_value = old_team

        new_team = Team(id=1, name="Z")

        # Act
        test_repo = TeamRepository()
        team_updated = test_repo.update_team(new_team)

    # Assert
    fake_team_exists.assert_called_once_with(old_team.id)
    fake_get_team.assert_called_once_with(old_team.id)
    assert team_updated.name == new_team.name
    fake_sqla.session.add.assert_called_once_with(old_team)
    fake_sqla.session.commit.assert_called_once()
    assert team_updated is new_team


@patch('app.data.repositories.team_repository.TeamRepository.team_exists')
def test_delete_team_when_team_does_not_exist_should_return_none(fake_team_exists):
    # Arrange
    fake_team_exists.return_value = False
    id = 1

    test_app = create_app()
    with test_app.app_context():
        # Act
        test_repo = TeamRepository()
        team_deleted = test_repo.delete_team(id=id)

    # Assert
    fake_team_exists.assert_called_once_with(id)
    assert team_deleted is None


@patch('app.data.repositories.team_repository.sqla')
@patch('app.data.repositories.team_repository.TeamRepository.get_team')
@patch('app.data.repositories.team_repository.TeamRepository.team_exists')
def test_delete_team_when_team_exists_should_return_team(fake_team_exists, fake_get_team, fake_sqla):
    # Arrange
    fake_team_exists.return_value = True
    id = 1

    test_app = create_app()
    with test_app.app_context():
        # Act
        test_repo = TeamRepository()
        team_deleted = test_repo.delete_team(id=id)

    # Assert
    fake_team_exists.assert_called_once_with(id)
    fake_get_team.assert_called_once_with(id)
    fake_sqla.session.delete.assert_called_once_with(fake_get_team.return_value)
    fake_sqla.session.commit.assert_called_once()
    return team_deleted is fake_get_team.return_value
