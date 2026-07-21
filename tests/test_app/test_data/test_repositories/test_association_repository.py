from unittest.mock import patch, call

import pytest

from sqlalchemy.exc import IntegrityError

from app import sqla
from app.data.models.association import Association
from app.data.repositories.association_repository import AssociationRepository
from instance.test_db import db_init
from test_app import create_app


@pytest.fixture
def test_app():
    return create_app()


@pytest.fixture
def test_repo():
    return AssociationRepository()


def test_get_associations_should_get_associations(test_app, test_repo):
    # Arrange
    with test_app.app_context():
        # Arrange
        db_init.init_db()

        parent = Association(
            id=1,
            long_name="Association 1",
            short_name="A1",
            parent_id=None,
            parent=None,
            first_season_year=1920
        )
        associations_in = [
            parent,
            Association(
                id=2,
                long_name="Association 2",
                short_name="A2",
                parent_id = 1,
                parent=parent,
                first_season_year=1921
            ),
            Association(
                id=3,
                long_name="Association 3",
                short_name="A3",
                parent_id = 1,
                parent=parent,
                first_season_year=1922
            ),
        ]
        for association in associations_in:
            sqla.session.add(association)
        sqla.session.commit()

        # Act
        associations_out = test_repo.get_associations()

        # Assert
        assert associations_out == associations_in


def test_get_association_when_associations_is_empty_should_return_none(test_app, test_repo):
    with test_app.app_context():
        # Arrange
        db_init.init_db()

        # Act
        association_out = test_repo.get_association(1)

    # Assert
    assert association_out is None


def test_get_association_when_associations_is_not_empty_and_association_is_not_found_should_return_none(
        test_app, test_repo
):
    with test_app.app_context():
        # Arrange
        db_init.init_db()

        parent = Association(
            id=1,
            long_name="Association 1",
            short_name="A1",
            parent_id=None,
            parent=None,
            first_season_year=1920
        )
        associations_in = (
            parent,
            Association(
                id=2,
                long_name="Association 2",
                short_name="A2",
                parent_id = 1,
                parent=parent,
                first_season_year=1921
            ),
            Association(
                id=3,
                long_name="Association 3",
                short_name="A3",
                parent_id = 1,
                parent=parent,
                first_season_year=1922
            ),
        )
        for association in associations_in:
            sqla.session.add(association)
        sqla.session.commit()

        # Act
        association_out = test_repo.get_association(-1)

    # Assert
    assert association_out is None


def test_get_association_when_associations_is_not_empty_and_association_is_found_should_return_association(
        test_app, test_repo
):
    with test_app.app_context():
        # Arrange
        db_init.init_db()

        parent = Association(
            id=1,
            long_name="Association 1",
            short_name="A1",
            parent_id=None,
            parent=None,
            first_season_year=1920
        )
        associations_in = (
            parent,
            Association(
                id=2,
                long_name="Association 2",
                short_name="A2",
                parent_id = 1,
                parent=parent,
                first_season_year=1921
            ),
            Association(
                id=3,
                long_name="Association 3",
                short_name="A3",
                parent_id = 1,
                parent=parent,
                first_season_year=1922
            ),
        )
        for association in associations_in:
            sqla.session.add(association)
        sqla.session.commit()

        # Act
        id = 1
        association_out = test_repo.get_association(id)

    # Assert
    assert association_out is [a for a in associations_in if a.id == id][0]


def test_get_association_by_short_name_when_associations_is_empty_should_return_none(test_app, test_repo):
    with test_app.app_context():
        # Arrange
        db_init.init_db()

        # Act
        association_out = test_repo.get_association_by_short_name("A")

    # Assert
    assert association_out is None


def test_get_association_by_short_name_when_associations_is_not_empty_and_association_is_not_found_should_return_none(
        test_app, test_repo
):
    with test_app.app_context():
        # Arrange
        db_init.init_db()

        parent = Association(
            id=1,
            long_name="Association 1",
            short_name="A1",
            parent_id=None,
            parent=None,
            first_season_year=1920
        )
        associations_in = (
            parent,
            Association(
                id=2,
                long_name="Association 2",
                short_name="A2",
                parent_id = 1,
                parent=parent,
                first_season_year=1921
            ),
            Association(
                id=3,
                long_name="Association 3",
                short_name="A3",
                parent_id = 1,
                parent=parent,
                first_season_year=1922
            ),
        )
        for association in associations_in:
            sqla.session.add(association)
        sqla.session.commit()

        # Act
        association_out = test_repo.get_association_by_short_name("A")

    # Assert
    assert association_out is None


def test_get_association_by_short_name_when_associations_is_not_empty_and_association_is_found_should_return_association(
        test_app, test_repo
):
    with test_app.app_context():
        # Arrange
        db_init.init_db()

        parent = Association(
            id=1,
            long_name="Association 1",
            short_name="A1",
            parent_id=None,
            parent=None,
            first_season_year=1920
        )
        associations_in = (
            parent,
            Association(
                id=2,
                long_name="Association 2",
                short_name="A2",
                parent_id = 1,
                parent=parent,
                first_season_year=1921
            ),
            Association(
                id=3,
                long_name="Association 3",
                short_name="A3",
                parent_id = 1,
                parent=parent,
                first_season_year=1922
            ),
        )
        for association in associations_in:
            sqla.session.add(association)
        sqla.session.commit()

        # Act
        short_name = "A1"
        association_out = test_repo.get_association_by_short_name(short_name)

    # Assert
    assert association_out is [a for a in associations_in if a.short_name == short_name][0]


@patch('app.data.repositories.association_repository.try_commit')
@patch('app.data.repositories.association_repository.sqla')
def test_add_association_when_integrity_error_not_caught_should_add_association(
        fake_sqla, fake_try_commit, test_repo
):
    # Arrange
    association_in = Association(
        long_name="Association",
        short_name="A",
        first_season_year=1920
    )

    # Act
    association_out = test_repo.add_association(association_in)

    # Assert
    fake_sqla.session.add.assert_called_once_with(association_in)
    fake_try_commit.assert_called_once()
    assert association_out is association_in


@patch('app.data.repositories.association_repository.try_commit')
@patch('app.data.repositories.association_repository.sqla')
def test_add_association_when_integrity_error_caught_should_rollback_transaction_and_reraise_error(
        fake_sqla, fake_try_commit, test_repo
):
    # Arrange
    association_in = Association(
        long_name="Association",
        short_name="A",
        first_season_year=1920
    )
    fake_try_commit.side_effect = IntegrityError('statement', 'params', Exception())

    # Act
    with pytest.raises(IntegrityError):
        _ = test_repo.add_association(association_in)

    # Assert
    fake_sqla.session.add.assert_called_once_with(association_in)
    fake_try_commit.assert_called_once()


@patch('app.data.repositories.association_repository.try_commit')
@patch('app.data.repositories.association_repository.sqla')
def test_add_associations_when_associations_arg_is_empty_should_add_no_associations(
        fake_sqla, fake_try_commit, test_repo
):
    # Arrange
    associations_in = ()

    # Act
    associations_out = test_repo.add_associations(associations_in)

    # Assert
    fake_sqla.session.add.assert_not_called()
    fake_try_commit.assert_called_once()
    assert associations_out == tuple()


@patch('app.data.repositories.association_repository.try_commit')
@patch('app.data.repositories.association_repository.sqla')
def test_add_associations_when_associations_arg_is_not_empty_and_no_integrity_error_caught_should_add_associations(
        fake_sqla, fake_try_commit, test_repo
):
    # Arrange
    parent = Association(
        id=1,
        long_name="Association 1",
        short_name="A1",
        parent_id=None,
        parent=None,
        first_season_year=1920
    )
    associations_in = (
        parent,
        Association(
            id=2,
            long_name="Association 2",
            short_name="A2",
            parent_id=1,
            parent=parent,
            first_season_year=1921
        ),
        Association(
            id=3,
            long_name="Association 3",
            short_name="A3",
            parent_id=1,
            parent=parent,
            first_season_year=1922
        ),
    )

    # Act
    associations_out = test_repo.add_associations(associations_in)

    # Assert
    fake_sqla.session.add.assert_has_calls([
        call(associations_in[0]),
        call(associations_in[1]),
        call(associations_in[2]),
    ])
    fake_try_commit.assert_called_once()
    assert associations_out == associations_in


@patch('app.data.repositories.association_repository.try_commit')
@patch('app.data.repositories.association_repository.sqla')
def test_add_associations_when_associations_arg_is_not_empty_and_integrity_error_caught_should_rollback_transaction_and_reraise_error(
        fake_sqla, fake_try_commit, test_repo
):
    # Arrange
    parent = Association(
        id=1,
        long_name="Association 1",
        short_name="A1",
        parent_id=None,
        parent=None,
        first_season_year=1920
    )
    associations_in = (
        parent,
        Association(
            id=2,
            long_name="Association 2",
            short_name="A2",
            parent_id=1,
            parent=parent,
            first_season_year=1921
        ),
        Association(
            id=3,
            long_name="Association 3",
            short_name="A3",
            parent_id=1,
            parent=parent,
            first_season_year=1922
        ),
    )

    fake_try_commit.side_effect = IntegrityError('statement', 'params', Exception())

    # Act
    with pytest.raises(IntegrityError):
        associations_out = test_repo.add_associations(associations_in)

    # Assert
    fake_sqla.session.add.assert_has_calls([
        call(associations_in[0]),
        call(associations_in[1]),
        call(associations_in[2]),
    ])
    fake_try_commit.assert_called_once()


def test_association_exists_when_association_does_not_exist_should_return_false(test_app, test_repo):
    # Arrange
    with test_app.app_context():
        db_init.init_db()

        parent = Association(
            id=1,
            long_name="Association 1",
            short_name="A1",
            parent_id=None,
            parent=None,
            first_season_year=1920
        )
        associations_in = (
            parent,
            Association(
                id=2,
                long_name="Association 2",
                short_name="A2",
                parent_id = 1,
                parent=parent,
                first_season_year=1921
            ),
            Association(
                id=3,
                long_name="Association 3",
                short_name="A3",
                parent_id = 1,
                parent=parent,
                first_season_year=1922
            ),
        )
        for association in associations_in:
            sqla.session.add(association)
        sqla.session.commit()

        # Act
        association_exists = test_repo.association_exists(id=-1)

    # Assert
    assert not association_exists


def test_association_exists_when_association_exists_should_return_true(test_app, test_repo):
    # Arrange
    with test_app.app_context():
        db_init.init_db()

        parent = Association(
            id=1,
            long_name="Association 1",
            short_name="A1",
            parent_id=None,
            parent=None,
            first_season_year=1920
        )
        associations_in = (
            parent,
            Association(
                id=2,
                long_name="Association 2",
                short_name="A2",
                parent_id = 1,
                parent=parent,
                first_season_year=1921
            ),
            Association(
                id=3,
                long_name="Association 3",
                short_name="A3",
                parent_id = 1,
                parent=parent,
                first_season_year=1922
            ),
        )
        for association in associations_in:
            sqla.session.add(association)
        sqla.session.commit()

        # Act
        association_exists = test_repo.association_exists(id=1)

    # Assert
    assert association_exists


@patch('app.data.repositories.association_repository.try_commit')
@patch('app.data.repositories.association_repository.sqla')
@patch('app.data.repositories.association_repository.AssociationRepository.association_exists')
def test_update_association_when_no_association_exists_with_id_should_return_association_and_not_update_database(
        fake_association_exists, fake_sqla, fake_try_commit,
        test_app, test_repo
):
    with test_app.app_context():
        # Arrange
        fake_association_exists.return_value = False

        # Act
        association = Association(
            id=1,
            long_name="Association",
            short_name="A",
            parent_id=None,
            parent=None,
            first_season_year=1920
        )
        try:
            association_updated = test_repo.update_association(association)
        except ValueError:
            assert False

    # Assert
    fake_sqla.session.add.assert_not_called()
    fake_try_commit.assert_not_called()
    assert isinstance(association_updated, Association)
    assert association_updated.id == association.id
    assert association_updated.long_name == association.long_name
    assert association_updated.short_name == association.short_name
    assert association_updated.parent_id == association.parent_id
    assert association_updated.first_season_year == association.first_season_year
    assert association_updated.last_season_year == association.last_season_year



@patch('app.data.repositories.association_repository.try_commit')
@patch('app.data.repositories.association_repository.sqla')
@patch('app.data.repositories.association_repository.AssociationRepository.association_exists')
def test_update_association_when_association_exists_with_id_and_no_integrity_error_caught_should_return_association_and_update_database(
        fake_association_exists, fake_sqla, fake_try_commit,
        test_app, test_repo
):
    with test_app.app_context():
        # Arrange
        fake_association_exists.return_value = True

        db_init.init_db()

        parent = Association(
            id=1,
            long_name="Association 1",
            short_name="A1",
            parent_id=None,
            parent=None,
            first_season_year=1920
        )
        associations_in = (
            parent,
            Association(
                id=2,
                long_name="Association 2",
                short_name="A2",
                parent_id=1,
                parent=parent,
                first_season_year=1921
            ),
            Association(
                id=3,
                long_name="Association 3",
                short_name="A3",
                parent_id=1,
                parent=parent,
                first_season_year=1922
            ),
        )
        for association in associations_in:
            sqla.session.add(association)
        sqla.session.commit()

        id = 2
        old_association = [a for a in associations_in if a.id == id][0]
        new_association = Association(
            id=id,
            short_name="A4",
            long_name="Association 4",
            first_season_year=1926,
            last_season_year=1927
        )

        # Act
        try:
            association_updated = test_repo.update_association(new_association)
        except IntegrityError:
            assert False

    # Assert
    fake_sqla.session.add.assert_called_once_with(old_association)
    fake_try_commit.assert_called_once()
    assert isinstance(association_updated, Association)
    assert association_updated.id == new_association.id
    assert association_updated.long_name == new_association.long_name
    assert association_updated.short_name == new_association.short_name
    assert association_updated.parent_id == new_association.parent_id
    assert association_updated.first_season_year == new_association.first_season_year
    assert association_updated.last_season_year == new_association.last_season_year
    assert association_updated is new_association


@patch('app.data.repositories.association_repository.try_commit')
@patch('app.data.repositories.association_repository.sqla')
@patch('app.data.repositories.association_repository.AssociationRepository.association_exists')
def test_update_association_when_integrity_error_caught_should_rollback_transaction_and_reraise_error(
        fake_association_exists, fake_sqla, fake_try_commit,
        test_app, test_repo
):
    with test_app.app_context():
        # Arrange
        fake_association_exists.return_value = True

        db_init.init_db()

        parent = Association(
            id=1,
            long_name="Association 1",
            short_name="A1",
            parent_id=None,
            parent=None,
            first_season_year=1920
        )
        associations_in = (
            parent,
            Association(
                id=2,
                long_name="Association 2",
                short_name="A2",
                parent_id=1,
                parent=parent,
                first_season_year=1921
            ),
            Association(
                id=3,
                long_name="Association 3",
                short_name="A3",
                parent_id=1,
                parent=parent,
                first_season_year=1922
            ),
        )
        for association in associations_in:
            sqla.session.add(association)
        sqla.session.commit()

        old_association = associations_in[1]

        new_association = Association(
            id=2,
            short_name="A4",
            long_name="Association 4",
            first_season_year=1926,
            last_season_year=1927
        )

        fake_try_commit.side_effect = IntegrityError('statement', 'params', Exception())

        # Act
        with pytest.raises(IntegrityError):
            _ = test_repo.update_association(new_association)

    # Assert
    fake_sqla.session.add.assert_called_once_with(old_association)
    fake_try_commit.assert_called_once()


@patch('app.data.repositories.association_repository.try_commit')
@patch('app.data.repositories.association_repository.sqla')
def test_delete_association_when_association_does_not_exist_should_return_none_and_not_delete_association_from_database(
        fake_sqla, fake_try_commit, test_app, test_repo
):
    with test_app.app_context():
        # Arrange
        db_init.init_db()

        parent = Association(
            id=1,
            long_name="Association 1",
            short_name="A1",
            parent_id=None,
            parent=None,
            first_season_year=1920
        )
        associations_in = (
            parent,
            Association(
                id=2,
                long_name="Association 2",
                short_name="A2",
                parent_id=1,
                parent=parent,
                first_season_year=1921
            ),
            Association(
                id=3,
                long_name="Association 3",
                short_name="A3",
                parent_id=1,
                parent=parent,
                first_season_year=1922
            ),
        )
        for association in associations_in:
            sqla.session.add(association)
        sqla.session.commit()

        # Act
        association_deleted = test_repo.delete_association(id=-1)

    # Assert
    assert association_deleted is None
    fake_sqla.session.delete.assert_not_called()
    fake_try_commit.assert_not_called()


@patch('app.data.repositories.association_repository.try_commit')
@patch('app.data.repositories.association_repository.sqla')
def test_delete_association_when_association_exists_and_integrity_error_not_caught_should_return_association_and_delete_association_from_database(
        fake_sqla, fake_try_commit, test_app, test_repo
):
    with test_app.app_context():
        # Arrange
        db_init.init_db()

        parent = Association(
            id=1,
            long_name="Association 1",
            short_name="A1",
            parent_id=None,
            parent=None,
            first_season_year=1920
        )
        associations_in = (
            parent,
            Association(
                id=2,
                long_name="Association 2",
                short_name="A2",
                parent_id=1,
                parent=parent,
                first_season_year=1921
            ),
            Association(
                id=3,
                long_name="Association 3",
                short_name="A3",
                parent_id=1,
                parent=parent,
                first_season_year=1922
            ),
        )
        for association in associations_in:
            sqla.session.add(association)
        sqla.session.commit()

        # Act
        id = 1
        try:
            association_deleted = test_repo.delete_association(id=id)
        except IntegrityError:
            assert False

    # Assert
    fake_sqla.session.delete.assert_called_once_with(association_deleted)
    fake_try_commit.assert_called_once()
    assert association_deleted is [a for a in associations_in if a.id == id][0]


@patch('app.data.repositories.association_repository.try_commit')
@patch('app.data.repositories.association_repository.sqla')
def test_delete_association_when_association_exists_and_integrity_error_caught_should_rollback_commit(
        fake_sqla, fake_try_commit, test_app, test_repo
):
    with test_app.app_context():
        # Arrange
        db_init.init_db()

        parent = Association(
            id=1,
            long_name="Association 1",
            short_name="A1",
            parent_id=None,
            parent=None,
            first_season_year=1920
        )
        associations_in = (
            parent,
            Association(
                id=2,
                long_name="Association 2",
                short_name="A2",
                parent_id=1,
                parent=parent,
                first_season_year=1921
            ),
            Association(
                id=3,
                long_name="Association 3",
                short_name="A3",
                parent_id=1,
                parent=parent,
                first_season_year=1922
            ),
        )
        for association in associations_in:
            sqla.session.add(association)
        sqla.session.commit()

        fake_try_commit.side_effect = IntegrityError('statement', 'params', Exception())

        # Act
        id = 1
        with pytest.raises(IntegrityError):
            _ = test_repo.delete_association(id)

    # Assert
    fake_sqla.session.delete.assert_called_once_with([a for a in associations_in if a.id == id][0])
    fake_try_commit.assert_called_once()
