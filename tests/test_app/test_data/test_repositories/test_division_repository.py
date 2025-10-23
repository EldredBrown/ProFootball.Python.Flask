from unittest.mock import patch, call

import pytest
from sqlalchemy.exc import IntegrityError

from test_app import create_app

from app.data.models.season import Season
from app.data.models.division import Division
from app.data.models.game import Game
from app.data.models.league_season import LeagueSeason
from app.data.models.team_season import TeamSeason
from app.data.repositories.division_repository import DivisionRepository


@pytest.fixture
def test_app():
    return create_app()


@patch('app.data.repositories.division_repository.Division')
def test_get_divisions_should_get_divisions(fake_division, test_app):
    with test_app.app_context():
        # Arrange
        divisions_in = [
            Division(name="NFC East"),
            Division(name="NFC Central"),
            Division(name="NFC West"),
        ]
        fake_division.query.all.return_value = divisions_in

        # Act
        test_repo = DivisionRepository()
        divisions_out = test_repo.get_divisions()

    # Assert
    assert divisions_out == divisions_in


@patch('app.data.repositories.division_repository.Division')
def test_get_division_when_divisions_is_empty_should_return_none(fake_division, test_app):
    with test_app.app_context():
        # Arrange
        divisions_in = []
        fake_division.query.all.return_value = divisions_in

        # Act
        test_repo = DivisionRepository()
        division_out = test_repo.get_division(1)

    # Assert
    assert division_out is None


@patch('app.data.repositories.division_repository.Division')
def test_get_division_when_divisions_is_not_empty_and_division_is_not_found_should_return_none(fake_division, test_app):
    with test_app.app_context():
        # Arrange
        divisions_in = [
            Division(name="NFC East"),
            Division(name="NFC Central"),
            Division(name="NFC West"),
        ]
        fake_division.query.all.return_value = divisions_in
        fake_division.query.get.return_value = None

        # Act
        test_repo = DivisionRepository()

        id = len(divisions_in) + 1
        division_out = test_repo.get_division(id)

    # Assert
    assert division_out is None


@patch('app.data.repositories.division_repository.Division')
def test_get_division_when_divisions_is_not_empty_and_division_is_found_should_return_division(fake_division, test_app):
    with test_app.app_context():
        # Arrange
        divisions_in = [
            Division(name="NFC East"),
            Division(name="NFC Central"),
            Division(name="NFC West"),
        ]
        fake_division.query.all.return_value = divisions_in

        id = len(divisions_in) - 1
        fake_division.query.get.return_value = divisions_in[id]

        # Act
        test_repo = DivisionRepository()

        division_out = test_repo.get_division(id)

    # Assert
    assert division_out is divisions_in[id]


@patch('app.data.repositories.division_repository.Division')
def test_get_division_by_name_when_divisions_is_empty_should_return_none(fake_division, test_app):
    with test_app.app_context():
        # Arrange
        divisions_in = []
        fake_division.query.all.return_value = divisions_in

        # Act
        test_repo = DivisionRepository()
        division_out = test_repo.get_division_by_name("NFC")

    # Assert
    assert division_out is None


@patch('app.data.repositories.division_repository.Division')
def test_get_division_by_name_when_divisions_is_not_empty_and_division_with_name_is_not_found_should_return_none(
        fake_division, test_app
):
    with test_app.app_context():
        # Arrange
        divisions_in = [
            Division(name="NFC East"),
            Division(name="NFC Central"),
            Division(name="NFC West"),
        ]
        fake_division.query.all.return_value = divisions_in
        fake_division.query.filter_by.return_value.first.return_value = None

        # Act
        test_repo = DivisionRepository()
        division_out = test_repo.get_division_by_name("USFC")

    # Assert
    assert division_out is None


@patch('app.data.repositories.division_repository.Division')
def test_get_division_by_year_when_divisions_is_not_empty_and_division_with_year_is_found_should_return_division(
        fake_division, test_app
):
    with test_app.app_context():
        # Arrange
        divisions_in = [
            Division(name="NFC East"),
            Division(name="NFC Central"),
            Division(name="NFC West"),
        ]
        fake_division.query.all.return_value = divisions_in
        fake_division.query.filter_by.return_value.first.return_value = divisions_in[-1]

        # Act
        test_repo = DivisionRepository()
        division_out = test_repo.get_division_by_name("AAFC")

    # Assert
    assert division_out is divisions_in[-1]


@patch('app.data.repositories.division_repository.sqla')
@patch('app.data.repositories.division_repository.division_factory')
def test_add_division_when_no_integrity_error_caught_should_add_division(fake_division_factory, fake_sqla, test_app):
    with test_app.app_context():
        # Arrange
        division_in = Division(name="NFC East")
        fake_division_factory.create_division.return_value = division_in

        # Act
        test_repo = DivisionRepository()
        kwargs = {
            'name': "NFC East",
        }
        division_out = test_repo.add_division(**kwargs)

    # Assert
    fake_sqla.session.add.assert_called_once_with(division_in)
    fake_sqla.session.commit.assert_called_once()
    assert division_out is division_in


@patch('app.data.repositories.division_repository.sqla')
@patch('app.data.repositories.division_repository.division_factory')
def test_add_division_when_integrity_error_caught_should_rollback_transaction_and_reraise_error(
        fake_division_factory, fake_sqla, test_app
):
    with test_app.app_context():
        # Arrange
        division_in = Division(name="NFC East")
        fake_division_factory.create_division.return_value = division_in
        fake_sqla.session.commit.side_effect = IntegrityError('statement', 'params', Exception())

        # Act
        test_repo = DivisionRepository()
        kwargs = {
            'name': "NFC East",
        }
        with pytest.raises(IntegrityError):
            division_out = test_repo.add_division(**kwargs)

    # Assert
    fake_sqla.session.rollback.assert_called_once()


@patch('app.data.repositories.division_repository.sqla')
def test_add_divisions_when_divisions_arg_is_empty_should_add_no_divisions(fake_sqla, test_app):
    # Arrange
    with test_app.app_context():
        # Act
        test_repo = DivisionRepository()

        division_args = ()
        divisions_out = test_repo.add_divisions(division_args)

    # Assert
    fake_sqla.session.add.assert_not_called()
    fake_sqla.session.commit.assert_called_once()
    assert divisions_out == []


@patch('app.data.repositories.division_repository.sqla')
@patch('app.data.repositories.division_repository.division_factory')
def test_add_divisions_when_divisions_arg_is_not_empty_should_add_divisions(fake_division_factory, fake_sqla, test_app):
    with test_app.app_context():
        # Arrange
        divisions_in = [
            Division(name="NFC East"),
            Division(name="NFC Central"),
            Division(name="NFC West"),
        ]
        fake_division_factory.create_division.side_effect = divisions_in

        # Act
        test_repo = DivisionRepository()

        division_args = (
            {'name': "NFC East"},
            {'name': "NFC Central"},
            {'name': "NFC West"},
        )
        divisions_out = test_repo.add_divisions(division_args)

    # Assert
    fake_sqla.session.add.assert_has_calls([
        call(divisions_in[0]),
        call(divisions_in[1]),
        call(divisions_in[2]),
    ])
    fake_sqla.session.commit.assert_called_once()
    assert divisions_out == divisions_in


@patch('app.data.repositories.division_repository.sqla')
@patch('app.data.repositories.division_repository.division_factory')
def test_add_divisions_when_divisions_arg_is_not_empty_and_no_integrity_error_caught_should_add_divisions(
        fake_division_factory, fake_sqla, test_app
):
    with test_app.app_context():
        # Arrange
        divisions_in = [
            Division(name="NFC East"),
            Division(name="NFC Central"),
            Division(name="NFC West"),
        ]
        fake_division_factory.create_division.side_effect = divisions_in

        # Act
        test_repo = DivisionRepository()

        division_args = (
            {'name': "NFC East"},
            {'name': "NFC Central"},
            {'name': "NFC West"},
        )
        divisions_out = test_repo.add_divisions(division_args)

    # Assert
    fake_sqla.session.add.assert_has_calls([
        call(divisions_in[0]),
        call(divisions_in[1]),
        call(divisions_in[2]),
    ])
    fake_sqla.session.commit.assert_called_once()
    assert divisions_out == divisions_in


@patch('app.data.repositories.division_repository.sqla')
@patch('app.data.repositories.division_repository.division_factory')
def test_add_divisions_when_divisions_arg_is_not_empty_and_integrity_error_caught_should_rollback_transaction_and_reraise_error(
        fake_division_factory, fake_sqla, test_app
):
    with test_app.app_context():
        # Arrange
        divisions_in = [
            Division(name="NFC East"),
            Division(name="NFC Central"),
            Division(name="NFC West"),
        ]
        fake_division_factory.create_division.side_effect = divisions_in
        fake_sqla.session.commit.side_effect = IntegrityError('statement', 'params', Exception())

        # Act
        test_repo = DivisionRepository()

        division_args = (
            {'name': "NFC East"},
            {'name': "NFC Central"},
            {'name': "NFC West"},
        )
        with pytest.raises(IntegrityError):
            divisions_out = test_repo.add_divisions(division_args)

    # Assert
    fake_sqla.session.rollback.assert_called_once()


@patch('app.data.repositories.division_repository.Division')
def test_division_exists_when_division_does_not_exist_should_return_false(fake_division, test_app):
    with test_app.app_context():
        # Arrange
        divisions_in = [
            Division(name="NFC East"),
            Division(name="NFC Central"),
            Division(name="NFC West"),
        ]
        fake_division.query.all.return_value = divisions_in
        fake_division.query.get.return_value = None

        # Act
        test_repo = DivisionRepository()
        division_exists = test_repo.division_exists(id=1)

    # Assert
    assert not division_exists


@patch('app.data.repositories.division_repository.Division')
def test_division_exists_when_division_exists_should_return_true(fake_division, test_app):
    with test_app.app_context():
        # Arrange
        divisions_in = [
            Division(name="NFC East"),
            Division(name="NFC Central"),
            Division(name="NFC West"),
        ]
        fake_division.query.all.return_value = divisions_in
        fake_division.query.get.return_value = divisions_in[1]

        # Act
        test_repo = DivisionRepository()
        division_exists = test_repo.division_exists(id=1)

    # Assert
    assert division_exists


def test_update_division_when_id_not_in_kwargs_should_raise_value_error(test_app):
    # Arrange
    with test_app.app_context():
        # Act
        test_repo = DivisionRepository()
        kwargs = {
            'name': "NFC East",
            'league_name': "NFL",
            'conference_name': "NFC",
            'first_season_year': 1970,
            'last_season_year': None,
        }
        with pytest.raises(ValueError) as err:
            division_updated = test_repo.update_division(**kwargs)

    # Assert
    assert err.value.args[0] == "ID must be provided for existing Division."


@patch('app.data.repositories.division_repository.sqla')
@patch('app.data.repositories.division_repository.DivisionRepository.division_exists')
def test_update_division_when_id_is_in_kwargs_and_no_division_exists_with_id_should_return_division_and_not_update_database(
        fake_division_exists, fake_sqla, test_app
):
    with test_app.app_context():
        # Arrange
        fake_division_exists.return_value = False

        # Act
        test_repo = DivisionRepository()
        kwargs = {
            'id': 1,
            'name': "NFC East",
            'league_name': "NFL",
            'conference_name': "NFC",
            'first_season_year': 1970,
            'last_season_year': None,
        }
        try:
            division_updated = test_repo.update_division(**kwargs)
        except ValueError as err:
            assert False

    # Assert
    fake_sqla.session.add.assert_not_called()
    fake_sqla.session.commit.assert_not_called()
    assert isinstance(division_updated, Division)
    assert division_updated.id == 1
    assert division_updated.name == "NFC East"
    assert division_updated.league_name == "NFL"
    assert division_updated.conference_name == "NFC"
    assert division_updated.first_season_year == 1970
    assert division_updated.last_season_year == None


@patch('app.data.repositories.division_repository.sqla')
@patch('app.data.repositories.division_repository.division_factory')
@patch('app.data.repositories.division_repository.Division')
@patch('app.data.repositories.division_repository.DivisionRepository.division_exists')
def test_update_division_when_id_is_in_kwargs_and_division_exists_with_id_and_no_integrity_error_caught_should_return_division_and_update_database(
        fake_division_exists, fake_division, fake_division_factory, fake_sqla, test_app
):
    with test_app.app_context():
        # Arrange
        fake_division_exists.return_value = True

        divisions = [
            Division(
                id=1, name="NFC East", league_name="NFL", conference_name="NFC",
                first_season_year=1970, last_season_year=None
            ),
            Division(
                id=2, name="NFC Central", league_name="NFL", conference_name="NFC",
                first_season_year=1970, last_season_year=None
            ),
            Division(
                id=3, name="NFC West", league_name="NFL", conference_name="NFC",
                first_season_year=1970, last_season_year=None
            ),
        ]
        fake_division.query.all.return_value = divisions

        old_division = divisions[1]
        fake_division.query.get.return_value = old_division

        new_division = Division(
            id=2, name="AFC Central", league_name="NFL", conference_name="AFC",
            first_season_year=1970, last_season_year=None
        )
        fake_division_factory.create_division.return_value = new_division

        # Act
        test_repo = DivisionRepository()
        kwargs = {
            'id': 2,
            'name': "AFC Central",
            'league_name': "NFL",
            'conference_name': "AFC",
            'first_season_year': 1970,
            'last_season_year': None,
        }
        try:
            division_updated = test_repo.update_division(**kwargs)
        except ValueError:
            assert False

    # Assert
    fake_sqla.session.add.assert_called_once_with(old_division)
    fake_sqla.session.commit.assert_called_once()
    assert isinstance(division_updated, Division)
    assert division_updated.id == 2
    assert division_updated.name == "AFC Central"
    assert division_updated.league_name == "NFL"
    assert division_updated.conference_name == "AFC"
    assert division_updated.first_season_year == 1970
    assert division_updated.last_season_year is None
    assert division_updated is new_division


@patch('app.data.repositories.division_repository.sqla')
@patch('app.data.repositories.division_repository.division_factory')
@patch('app.data.repositories.division_repository.Division')
@patch('app.data.repositories.division_repository.DivisionRepository.division_exists')
def test_update_division_when_id_is_in_kwargs_and_division_exists_with_id_and_integrity_error_caught_should_rollback_transaction_and_reraise_error(
        fake_division_exists, fake_division, fake_division_factory, fake_sqla, test_app
):
    with test_app.app_context():
        # Arrange
        fake_division_exists.return_value = True

        divisions = [
            Division(
                id=1, name="NFC East", league_name="NFL", conference_name="NFC",
                first_season_year=1970, last_season_year=None
            ),
            Division(
                id=2, name="NFC Central", league_name="NFL", conference_name="NFC",
                first_season_year=1970, last_season_year=None
            ),
            Division(
                id=3, name="NFC West", league_name="NFL", conference_name="NFC",
                first_season_year=1970, last_season_year=None
            ),
        ]
        fake_division.query.all.return_value = divisions

        old_division = divisions[1]
        fake_division.query.get.return_value = old_division

        new_division = Division(
            id=2, name="AFC Central", league_name="NFL", conference_name="AFC",
            first_season_year=1970, last_season_year=None
        )
        fake_division_factory.create_division.return_value = new_division

        fake_sqla.session.commit.side_effect = IntegrityError('statement', 'params', Exception())

        # Act
        test_repo = DivisionRepository()
        kwargs = {
            'id': 2,
            'name': "AFC Central",
            'league_name': "NFL",
            'conference_name': "AFC",
            'first_season_year': 1970,
            'last_season_year': None,
        }
        with pytest.raises(IntegrityError):
            division_updated = test_repo.update_division(**kwargs)

    # Assert
    fake_sqla.session.rollback.assert_called_once()


@patch('app.data.repositories.division_repository.sqla')
@patch('app.data.repositories.division_repository.Division')
def test_delete_division_when_division_does_not_exist_should_return_none_and_not_delete_division_from_database(
        fake_division, fake_sqla, test_app
):
    with test_app.app_context():
        # Arrange
        divisions_in = [
            Division(name="NFC East"),
            Division(name="NFC Central"),
            Division(name="NFC West"),
        ]
        fake_division.query.all.return_value = divisions_in
        fake_division.query.get.return_value = None

        id = 1

        # Act
        test_repo = DivisionRepository()
        division_deleted = test_repo.delete_division(id)

    # Assert
    assert division_deleted is None
    fake_sqla.session.delete.assert_not_called()
    fake_sqla.session.commit.assert_not_called()


@patch('app.data.repositories.division_repository.sqla')
@patch('app.data.repositories.division_repository.Division')
def test_delete_division_when_division_exists_should_return_division_and_delete_division_from_database(
        fake_division, fake_sqla, test_app
):
    with test_app.app_context():
        # Arrange
        divisions_in = [
            Division(name="NFC East"),
            Division(name="NFC Central"),
            Division(name="NFC West"),
        ]
        fake_division.query.all.return_value = divisions_in

        id = 1
        fake_division.query.get.return_value = divisions_in[id]

        # Act
        test_repo = DivisionRepository()
        division_deleted = test_repo.delete_division(id)

    # Assert
    fake_sqla.session.delete.assert_called_once_with(division_deleted)
    fake_sqla.session.commit.assert_called_once()
    assert division_deleted is divisions_in[id]
