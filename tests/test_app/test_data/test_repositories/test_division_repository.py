import pytest

from unittest.mock import patch, call

from app import create_app
from app.data.models.division import Division
from app.data.models.game import Game
from app.data.models.league_season import LeagueSeason
from app.data.models.team_season import TeamSeason
from app.data.repositories.division_repository import DivisionRepository


@patch('app.data.repositories.division_repository.Division')
def test_get_divisions_should_get_divisions(fake_division):
    # Act
    test_app = create_app()
    with test_app.app_context():
        test_repo = DivisionRepository()
        divisions = test_repo.get_divisions()

    # Assert
    fake_division.query.all.assert_called_once()
    assert divisions == fake_division.query.all.return_value


@patch('app.data.repositories.division_repository.DivisionRepository.get_divisions')
def test_get_division_when_divisions_is_empty_should_return_none(fake_get_divisions):
    test_app = create_app()
    with test_app.app_context():
        # Arrange
        divisions = []
        fake_get_divisions.return_value = divisions

        # Act
        test_repo = DivisionRepository()
        division = test_repo.get_division(id=1)

    # Assert
    assert division is None


@patch('app.data.repositories.division_repository.Division')
@patch('app.data.repositories.division_repository.DivisionRepository.get_divisions')
def test_get_division_when_divisions_is_not_empty_and_division_is_not_found_should_return_none(
        fake_get_divisions, fake_division
):
    test_app = create_app()
    with test_app.app_context():
        # Arrange
        divisions = [
            Division(name="A", league_name="A", conference_name="A", first_season_year=1, last_season_year=2),
            Division(name="B", league_name="A", conference_name="A", first_season_year=3, last_season_year=4),
            Division(name="C", league_name="A", conference_name="A", first_season_year=5, last_season_year=None),
        ]
        fake_get_divisions.return_value = divisions

        id = len(divisions) + 1

        # Act
        test_repo = DivisionRepository()
        division = test_repo.get_division(id=id)

    # Assert
    fake_division.query.get.assert_called_once_with(id)
    assert division == fake_division.query.get.return_value


@patch('app.data.repositories.division_repository.Division')
@patch('app.data.repositories.division_repository.DivisionRepository.get_divisions')
def test_get_division_when_divisions_is_not_empty_and_division_is_found_should_return_division(fake_get_divisions, fake_division):
    test_app = create_app()
    with test_app.app_context():
        # Arrange
        divisions = [
            Division(name="A", league_name="A", conference_name="A", first_season_year=1, last_season_year=2),
            Division(name="B", league_name="A", conference_name="A", first_season_year=3, last_season_year=4),
            Division(name="C", league_name="A", conference_name="A", first_season_year=5, last_season_year=None),
        ]
        fake_get_divisions.return_value = divisions

        id = len(divisions) - 1

        # Act
        test_repo = DivisionRepository()
        division = test_repo.get_division(id=id)

    # Assert
    fake_division.query.get.assert_called_once_with(id)
    assert division == fake_division.query.get.return_value


@patch('app.data.repositories.division_repository.DivisionRepository.get_divisions')
def test_get_division_by_name_when_divisions_is_empty_should_return_none(fake_get_divisions):
    test_app = create_app()
    with test_app.app_context():
        # Arrange
        divisions = []
        fake_get_divisions.return_value = divisions

        # Act
        test_repo = DivisionRepository()
        division = test_repo.get_division_by_name(name="A")

    # Assert
    assert division is None


@patch('app.data.repositories.division_repository.Division')
@patch('app.data.repositories.division_repository.DivisionRepository.get_divisions')
def test_get_division_by_name_when_divisions_is_not_empty_and_division_with_short_name_is_not_found_should_return_none(
        fake_get_divisions, fake_division
):
    test_app = create_app()
    with test_app.app_context():
        # Arrange
        divisions = [
            Division(name="A", league_name="A", conference_name="A", first_season_year=1, last_season_year=2),
            Division(name="B", league_name="A", conference_name="A", first_season_year=3, last_season_year=4),
            Division(name="C", league_name="A", conference_name="A", first_season_year=5, last_season_year=None),
        ]
        fake_get_divisions.return_value = divisions

        # Act
        test_repo = DivisionRepository()
        division = test_repo.get_division_by_name(name="D")

    # Assert
    fake_division.query.filter_by.assert_called_once_with(name="D")
    fake_division.query.filter_by.return_value.first.assert_called_once_with()
    assert division == fake_division.query.filter_by.return_value.first.return_value


@patch('app.data.repositories.division_repository.Division')
@patch('app.data.repositories.division_repository.DivisionRepository.get_divisions')
def test_get_division_by_name_when_divisions_is_not_empty_and_division_with_short_name_is_found_should_return_division(
        fake_get_divisions, fake_division
):
    test_app = create_app()
    with test_app.app_context():
        # Arrange
        divisions = [
            Division(name="A", league_name="A", conference_name="A", first_season_year=1, last_season_year=2),
            Division(name="B", league_name="A", conference_name="A", first_season_year=3, last_season_year=4),
            Division(name="C", league_name="A", conference_name="A", first_season_year=5, last_season_year=None),
        ]
        fake_get_divisions.return_value = divisions

        # Act
        test_repo = DivisionRepository()
        division = test_repo.get_division_by_name(name="B")

    # Assert
    fake_division.query.filter_by.assert_called_once_with(name="B")
    fake_division.query.filter_by.return_value.first.assert_called_once_with()
    assert division == fake_division.query.filter_by.return_value.first.return_value


@patch('app.data.repositories.division_repository.sqla')
def test_add_division_should_add_division(fake_sqla):
    # Arrange
    test_app = create_app()
    with test_app.app_context():
        # Act
        test_repo = DivisionRepository()
        division_in = Division(name="D", league_name=1, conference_name=1, first_season_year=7, last_season_year=8)
        division_out = test_repo.add_division(division_in)

    # Assert
    fake_sqla.session.add.assert_called_once_with(division_in)
    fake_sqla.session.commit.assert_called_once()
    assert division_out is division_in


@patch('app.data.repositories.division_repository.sqla')
def test_add_divisions_when_divisions_arg_is_empty_should_add_no_divisions(fake_sqla):
    # Arrange
    test_app = create_app()
    with test_app.app_context():
        # Act
        test_repo = DivisionRepository()
        divisions_in = ()
        divisions_out = test_repo.add_divisions(divisions_in)

    # Assert
    fake_sqla.session.add.assert_not_called()
    fake_sqla.session.commit.assert_called_once()
    assert divisions_out is divisions_in


@patch('app.data.repositories.division_repository.sqla')
def test_add_divisions_when_divisions_arg_is_not_empty_should_add_divisions(fake_sqla):
    # Arrange
    test_app = create_app()
    with test_app.app_context():
        # Act
        test_repo = DivisionRepository()
        divisions_in = (
            Division(name="D", league_name="A", conference_name="A", first_season_year=7, last_season_year=8),
            Division(name="E", league_name="A", conference_name="B", first_season_year=9, last_season_year=10),
            Division(name="F", league_name="A", conference_name="C", first_season_year=11, last_season_year=12),
        )
        divisions_out = test_repo.add_divisions(divisions_in)

    # Assert
    fake_sqla.session.add.assert_has_calls([
        call(divisions_in[0]),
        call(divisions_in[1]),
        call(divisions_in[2]),
    ])
    fake_sqla.session.commit.assert_called_once()
    assert divisions_out is divisions_in


@patch('app.data.repositories.division_repository.sqla')
@patch('app.data.repositories.division_repository.exists')
def test_division_exists_should_query_database(fake_exists, fake_sqla):
    # Arrange
    test_app = create_app()
    with test_app.app_context():
        # Act
        test_repo = DivisionRepository()
        division_exists = test_repo.division_exists(id=1)

    # Assert
    fake_exists.assert_called_once()
    fake_exists.return_value.where.assert_called_once()
    fake_sqla.session.query.assert_called_once_with(fake_exists.return_value.where.return_value)
    fake_sqla.session.query.return_value.scalar.assert_called_once()
    assert division_exists == fake_sqla.session.query.return_value.scalar.return_value


@patch('app.data.repositories.division_repository.DivisionRepository.division_exists')
def test_update_division_when_division_does_not_exist_should_return_division(fake_division_exists):
    # Arrange
    fake_division_exists.return_value = False

    test_app = create_app()
    with test_app.app_context():
        # Act
        test_repo = DivisionRepository()
        division_to_update = Division(
            id=1, name="A", league_name="A", conference_name="A", first_season_year=98, last_season_year=99
        )
        division_updated = test_repo.update_division(division_to_update)

    # Assert
    fake_division_exists.assert_called_once_with(division_to_update.id)
    assert division_updated is division_to_update


@patch('app.data.repositories.division_repository.sqla')
@patch('app.data.repositories.division_repository.DivisionRepository.get_division')
@patch('app.data.repositories.division_repository.DivisionRepository.division_exists')
def test_update_division_when_division_exists_should_update_and_return_division(
        fake_division_exists, fake_get_division, fake_sqla
):
    # Arrange
    test_app = create_app()
    with test_app.app_context():
        fake_division_exists.return_value = True
        old_division = Division(
            id=1, name="A", league_name="A", conference_name="A", first_season_year=1, last_season_year=2
        )
        fake_get_division.return_value = old_division

        new_division = Division(
            id=1, name="Z", league_name="Z", conference_name="Z", first_season_year=98, last_season_year=99
        )

        # Act
        test_repo = DivisionRepository()
        division_updated = test_repo.update_division(new_division)

    # Assert
    fake_division_exists.assert_called_once_with(old_division.id)
    fake_get_division.assert_called_once_with(old_division.id)
    assert division_updated.name == new_division.name
    assert division_updated.league_name == new_division.league_name
    assert division_updated.conference_name == new_division.conference_name
    assert division_updated.first_season_year == new_division.first_season_year
    assert division_updated.last_season_year == new_division.last_season_year
    fake_sqla.session.add.assert_called_once_with(old_division)
    fake_sqla.session.commit.assert_called_once()
    assert division_updated is new_division


@patch('app.data.repositories.division_repository.DivisionRepository.division_exists')
def test_delete_division_when_division_does_not_exist_should_return_none(fake_division_exists):
    # Arrange
    fake_division_exists.return_value = False
    id = 1

    test_app = create_app()
    with test_app.app_context():
        # Act
        test_repo = DivisionRepository()
        division_deleted = test_repo.delete_division(id=id)

    # Assert
    fake_division_exists.assert_called_once_with(id)
    assert division_deleted is None


@patch('app.data.repositories.division_repository.sqla')
@patch('app.data.repositories.division_repository.DivisionRepository.get_division')
@patch('app.data.repositories.division_repository.DivisionRepository.division_exists')
def test_delete_division_when_division_exists_should_return_division(fake_division_exists, fake_get_division, fake_sqla):
    # Arrange
    fake_division_exists.return_value = True
    id = 1

    test_app = create_app()
    with test_app.app_context():
        # Act
        test_repo = DivisionRepository()
        division_deleted = test_repo.delete_division(id=id)

    # Assert
    fake_division_exists.assert_called_once_with(id)
    fake_get_division.assert_called_once_with(id)
    fake_sqla.session.delete.assert_called_once_with(fake_get_division.return_value)
    fake_sqla.session.commit.assert_called_once()
    return division_deleted is fake_get_division.return_value
