from unittest.mock import patch, call, MagicMock

import pytest

from sqlalchemy.exc import IntegrityError

from app.data.models.conference import Conference
from app.data.repositories.conference_repository import ConferenceRepository


@pytest.fixture
def test_repo():
    return ConferenceRepository()


@patch('app.data.repositories.conference_repository.joinedload')
@patch('app.data.repositories.conference_repository.Conference')
def test_get_conferences_should_get_conferences(
        fake_conference, fake_joinedload, test_repo
):
    # Arrange
    fake_query = MagicMock('flask_sqlalchemy.query.Query')
    conferences_in = (
        Conference(
            short_name="C1",
            long_name="Conference 1",
            league_id=1,
            first_season_id=1920
        ),
        Conference(
            short_name="C2",
            long_name="Conference 2",
            league_id=1,
            first_season_id=1921
        ),
        Conference(
            short_name="C3",
            long_name="Conference 3",
            league_id=1,
            first_season_id=1922
        ),
    )
    fake_query.return_value.all.return_value = conferences_in
    fake_conference.query.options = fake_query
    fake_joinedload.return_value = MagicMock()

    # Act
    conferences_out = test_repo.get_conferences()

    # Assert
    assert conferences_out == conferences_in


@patch('app.data.repositories.conference_repository.joinedload')
@patch('app.data.repositories.conference_repository.Conference')
def test_get_conference_when_conferences_is_empty_should_return_none(
        fake_conference, fake_joinedload, test_repo
):
    # Arrange
    fake_query = MagicMock('flask_sqlalchemy.query.Query')
    conferences_in = ()
    fake_query.return_value.all.return_value = conferences_in
    fake_conference.query.options = fake_query
    fake_joinedload.return_value = MagicMock()

    # Act
    conference_out = test_repo.get_conference(1)

    # Assert
    assert conference_out is None


@patch('app.data.repositories.conference_repository.joinedload')
@patch('app.data.repositories.conference_repository.Conference')
def test_get_conference_when_conferences_is_not_empty_and_conference_is_not_found_should_return_none(
        fake_conference, fake_joinedload, test_repo
):
    # Arrange
    fake_query = MagicMock('flask_sqlalchemy.query.Query')
    conferences_in = (
        Conference(
            short_name="C1",
            long_name="Conference 1",
            league_id=1,
            first_season_id=1920
        ),
        Conference(
            short_name="C2",
            long_name="Conference 2",
            league_id=1,
            first_season_id=1921
        ),
        Conference(
            short_name="C3",
            long_name="Conference 3",
            league_id=1,
            first_season_id=1922
        ),
    )
    fake_query.return_value.all.return_value = conferences_in
    fake_query.return_value.get.return_value = None
    fake_conference.query.options = fake_query
    fake_joinedload.return_value = MagicMock()

    id = len(conferences_in) + 1

    # Act
    conference_out = test_repo.get_conference(id)

    # Assert
    assert conference_out is None


@patch('app.data.repositories.conference_repository.joinedload')
@patch('app.data.repositories.conference_repository.Conference')
def test_get_conference_when_conferences_is_not_empty_and_conference_is_found_should_return_conference(
        fake_conference, fake_joinedload, test_repo
):
    # Arrange
    fake_query = MagicMock('flask_sqlalchemy.query.Query')
    conferences_in = (
        Conference(
            short_name="C1",
            long_name="Conference 1",
            league_id=1,
            first_season_id=1920
        ),
        Conference(
            short_name="C2",
            long_name="Conference 2",
            league_id=1,
            first_season_id=1921
        ),
        Conference(
            short_name="C3",
            long_name="Conference 3",
            league_id=1,
            first_season_id=1922
        ),
    )
    fake_query.return_value.all.return_value = conferences_in
    id = len(conferences_in) - 1
    fake_query.return_value.get.return_value = conferences_in[id]
    fake_conference.query.options = fake_query
    fake_joinedload.return_value = MagicMock()

    # Act
    conference_out = test_repo.get_conference(id)

    # Assert
    assert conference_out is conferences_in[id]


@patch('app.data.repositories.conference_repository.joinedload')
@patch('app.data.repositories.conference_repository.Conference')
def test_get_conference_by_short_name_when_conferences_is_empty_should_return_none(
        fake_conference, fake_joinedload, test_repo
):
    # Arrange
    fake_query = MagicMock('flask_sqlalchemy.query.Query')
    conferences_in = ()
    fake_query.return_value.all.return_value = conferences_in
    fake_conference.query.options = fake_query
    fake_joinedload.return_value = MagicMock()

    # Act
    conference_out = test_repo.get_conference_by_short_name("NFC")

    # Assert
    assert conference_out is None


@patch('app.data.repositories.conference_repository.joinedload')
@patch('app.data.repositories.conference_repository.Conference')
def test_get_conference_by_short_name_when_conferences_is_not_empty_and_conference_with_short_name_is_not_found_should_return_none(
        fake_conference, fake_joinedload, test_repo
):
    # Arrange
    fake_query = MagicMock('flask_sqlalchemy.query.Query')
    conferences_in = (
        Conference(
            short_name="C1",
            long_name="Conference 1",
            league_id=1,
            first_season_id=1920
        ),
        Conference(
            short_name="C2",
            long_name="Conference 2",
            league_id=1,
            first_season_id=1921
        ),
        Conference(
            short_name="C3",
            long_name="Conference 3",
            league_id=1,
            first_season_id=1922
        ),
    )
    fake_query.return_value.all.return_value = conferences_in
    fake_query.return_value.filter_by.return_value.first.return_value = None
    fake_conference.query.options = fake_query
    fake_joinedload.return_value = MagicMock()

    # Act
    conference_out = test_repo.get_conference_by_short_name("C4")

    # Assert
    assert conference_out is None


@patch('app.data.repositories.conference_repository.joinedload')
@patch('app.data.repositories.conference_repository.Conference')
def test_get_conference_by_short_name_when_conferences_is_not_empty_and_conference_with_name_is_found_should_return_conference(
        fake_conference, fake_joinedload, test_repo
):
    # Arrange
    fake_query = MagicMock('flask_sqlalchemy.query.Query')
    conferences_in = (
        Conference(
            short_name="C1",
            long_name="Conference 1",
            league_id=1,
            first_season_id=1920
        ),
        Conference(
            short_name="C2",
            long_name="Conference 2",
            league_id=1,
            first_season_id=1921
        ),
        Conference(
            short_name="C3",
            long_name="Conference 3",
            league_id=1,
            first_season_id=1922
        ),
    )
    fake_query.return_value.all.return_value = conferences_in
    fake_query.return_value.filter_by.return_value.first.return_value = conferences_in[-1]
    fake_conference.query.options = fake_query
    fake_joinedload.return_value = MagicMock()

    # Act
    conference_out = test_repo.get_conference_by_short_name("AAFC")

    # Assert
    assert conference_out is conferences_in[-1]


@patch('app.data.repositories.conference_repository.try_commit')
@patch('app.data.repositories.conference_repository.sqla')
def test_add_conference_when_no_integrity_error_caught_should_add_conference(
        fake_sqla, fake_try_commit, test_repo
):
    # Arrange
    conference_in = Conference(
        short_name="C",
        long_name="Conference",
        league_id=1,
        first_season_id=1920
    )

    # Act
    conference_out = test_repo.add_conference(conference_in)

    # Assert
    fake_sqla.session.add.assert_called_once_with(conference_in)
    fake_try_commit.assert_called_once()
    assert conference_out is conference_in


@patch('app.data.repositories.conference_repository.try_commit')
@patch('app.data.repositories.conference_repository.sqla')
def test_add_conference_when_integrity_error_caught_should_rollback_transaction_and_reraise_error(
        fake_sqla, fake_try_commit, test_repo
):
    # Arrange
    conference_in = Conference(
        short_name="C",
        long_name="Conference",
        league_id=1,
        first_season_id=1920
    )
    fake_try_commit.side_effect = IntegrityError('statement', 'params', Exception())

    # Act
    with pytest.raises(IntegrityError):
        conference_out = test_repo.add_conference(conference_in)

    # Assert
    fake_sqla.session.add.assert_called_once_with(conference_in)
    fake_try_commit.assert_called_once()


@patch('app.data.repositories.conference_repository.try_commit')
@patch('app.data.repositories.conference_repository.sqla')
def test_add_conferences_when_conferences_arg_is_empty_should_add_no_conferences(
        fake_sqla, fake_try_commit, test_repo
):
    # Arrange
    conferences_in = ()

    # Act
    conferences_out = test_repo.add_conferences(conferences_in)

    # Assert
    fake_sqla.session.add.assert_not_called()
    fake_try_commit.assert_called_once()
    assert conferences_out == tuple()


@patch('app.data.repositories.conference_repository.try_commit')
@patch('app.data.repositories.conference_repository.sqla')
def test_add_conferences_when_conferences_arg_is_not_empty_and_no_integrity_error_caught_should_add_conferences(
        fake_sqla, fake_try_commit, test_repo
):
    # Arrange
    conferences_in = (
        Conference(
            short_name="C1",
            long_name="Conference 1",
            league_id=1,
            first_season_id=1920
        ),
        Conference(
            short_name="C2",
            long_name="Conference 2",
            league_id=1,
            first_season_id=1921
        ),
        Conference(
            short_name="C3",
            long_name="Conference 3",
            league_id=1,
            first_season_id=1922
        ),
    )

    # Act
    conferences_out = test_repo.add_conferences(conferences_in)

    # Assert
    fake_sqla.session.add.assert_has_calls([
        call(conferences_in[0]),
        call(conferences_in[1]),
        call(conferences_in[2]),
    ])
    fake_try_commit.assert_called_once()
    assert conferences_out == conferences_in


@patch('app.data.repositories.conference_repository.try_commit')
@patch('app.data.repositories.conference_repository.sqla')
def test_add_conferences_when_conferences_arg_is_not_empty_and_integrity_error_caught_should_rollback_transaction_and_reraise_error(
        fake_sqla, fake_try_commit, test_repo
):
    # Arrange
    conferences_in = (
        Conference(
            short_name="C1",
            long_name="Conference 1",
            league_id=1,
            first_season_id=1920
        ),
        Conference(
            short_name="C2",
            long_name="Conference 2",
            league_id=1,
            first_season_id=1921
        ),
        Conference(
            short_name="C3",
            long_name="Conference 3",
            league_id=1,
            first_season_id=1922
        ),
    )
    fake_try_commit.side_effect = IntegrityError('statement', 'params', Exception())

    # Act
    with pytest.raises(IntegrityError):
        conferences_out = test_repo.add_conferences(conferences_in)

    # Assert
    fake_sqla.session.add.assert_has_calls([
        call(conferences_in[0]),
        call(conferences_in[1]),
        call(conferences_in[2]),
    ])
    fake_try_commit.assert_called_once()


@patch('app.data.repositories.conference_repository.joinedload')
@patch('app.data.repositories.conference_repository.Conference')
def test_conference_exists_when_conference_does_not_exist_should_return_false(
        fake_conference, fake_joinedload, test_repo
):
    # Arrange
    fake_query = MagicMock('flask_sqlalchemy.query.Query')
    conferences = (
        Conference(
            short_name="C1",
            long_name="Conference 1",
            league_id=1,
            first_season_id=1920
        ),
        Conference(
            short_name="C2",
            long_name="Conference 2",
            league_id=1,
            first_season_id=1921
        ),
        Conference(
            short_name="C3",
            long_name="Conference 3",
            league_id=1,
            first_season_id=1922
        ),
    )
    fake_query.return_value.all.return_value = conferences
    fake_query.return_value.get.return_value = None
    fake_conference.query.options = fake_query
    fake_joinedload.return_value = MagicMock()

    # Act
    conference_exists = test_repo.conference_exists(id=1)

    # Assert
    assert not conference_exists


@patch('app.data.repositories.conference_repository.joinedload')
@patch('app.data.repositories.conference_repository.Conference')
def test_conference_exists_when_conference_exists_should_return_true(
        fake_conference, fake_joinedload, test_repo
):
    # Arrange
    fake_query = MagicMock('flask_sqlalchemy.query.Query')
    conferences = (
        Conference(
            short_name="C1",
            long_name="Conference 1",
            league_id=1,
            first_season_id=1920
        ),
        Conference(
            short_name="C2",
            long_name="Conference 2",
            league_id=1,
            first_season_id=1921
        ),
        Conference(
            short_name="C3",
            long_name="Conference 3",
            league_id=1,
            first_season_id=1922
        ),
    )
    fake_query.return_value.all.return_value = conferences
    fake_query.return_value.get.return_value = conferences[1]
    fake_conference.query.options = fake_query
    fake_joinedload.return_value = MagicMock()

    # Act
    conference_exists = test_repo.conference_exists(id=1)

    # Assert
    assert conference_exists


@patch('app.data.repositories.conference_repository.try_commit')
@patch('app.data.repositories.conference_repository.sqla')
@patch('app.data.repositories.conference_repository.ConferenceRepository.conference_exists')
def test_update_conference_when_no_conference_exists_with_id_should_return_conference_and_not_update_database(
        fake_conference_exists, fake_sqla, fake_try_commit,
        test_repo
):
    # Arrange
    fake_conference_exists.return_value = False

    # Act
    conference = Conference(
        id=1,
        short_name="C",
        long_name="Conference",
        league_id=1,
        first_season_id=1920,
        last_season_id=1921
    )

    try:
        conference_updated = test_repo.update_conference(conference)
    except ValueError:
        assert False

    # Assert
    fake_sqla.session.add.assert_not_called()
    fake_try_commit.assert_not_called()
    assert isinstance(conference_updated, Conference)
    assert isinstance(conference_updated, Conference)
    assert conference_updated.id == conference.id
    assert conference_updated.short_name == conference.short_name
    assert conference_updated.league_id == conference.league_id
    assert conference_updated.long_name == conference.long_name
    assert conference_updated.first_season_id == conference.first_season_id
    assert conference_updated.last_season_id == conference.last_season_id


@patch('app.data.repositories.conference_repository.try_commit')
@patch('app.data.repositories.conference_repository.sqla')
@patch('app.data.repositories.conference_repository.joinedload')
@patch('app.data.repositories.conference_repository.Conference')
@patch('app.data.repositories.conference_repository.ConferenceRepository.conference_exists')
def test_update_conference_when_conference_exists_with_id_and_no_integrity_error_caught_should_return_conference_and_update_database(
        fake_conference_exists, fake_conference, fake_joinedload, fake_sqla,
        fake_try_commit, test_repo
):
    # Arrange
    fake_conference_exists.return_value = True

    fake_query = MagicMock('flask_sqlalchemy.query.Query')
    conferences = (
        Conference(
            id=1,
            short_name="C1",
            long_name="Conference 1",
            league_id=1,
            first_season_id=1920,
            last_season_id=1921
        ),
        Conference(
            id=2,
            short_name="C2",
            long_name="Conference 2",
            league_id=1,
            first_season_id=1922,
            last_season_id=1923
        ),
        Conference(
            id=3,
            short_name="C3",
            long_name="Conference 3",
            league_id=1,
            first_season_id=1924,
            last_season_id=1925
        ),
    )
    fake_query.return_value.all.return_value = conferences
    old_conference = conferences[1]
    fake_query.return_value.get.return_value = old_conference
    fake_conference.query.options = fake_query
    fake_joinedload.return_value = MagicMock()

    new_conference = Conference(
        id=2,
        short_name="C4",
        long_name="Conference 4",
        league_id=1,
        first_season_id=1926,
        last_season_id=1927
    )

    # Act
    try:
        conference_updated = test_repo.update_conference(new_conference)
    except IntegrityError:
        assert False

    # Assert
    fake_sqla.session.add.assert_called_once_with(old_conference)
    fake_try_commit.assert_called_once()
    assert isinstance(conference_updated, Conference)
    assert isinstance(conference_updated, Conference)
    assert conference_updated.id == new_conference.id
    assert conference_updated.short_name == new_conference.short_name
    assert conference_updated.long_name == new_conference.long_name
    assert conference_updated.league_id == new_conference.league_id
    assert conference_updated.first_season_id == new_conference.first_season_id
    assert conference_updated.last_season_id == new_conference.last_season_id
    assert conference_updated is new_conference


@patch('app.data.repositories.conference_repository.try_commit')
@patch('app.data.repositories.conference_repository.sqla')
@patch('app.data.repositories.conference_repository.joinedload')
@patch('app.data.repositories.conference_repository.Conference')
@patch('app.data.repositories.conference_repository.ConferenceRepository.conference_exists')
def test_update_conference_when_conference_exists_with_id_and_integrity_error_caught_should_rollback_transaction_and_reraise_error(
        fake_conference_exists, fake_conference, fake_joinedload, fake_sqla,
        fake_try_commit, test_repo
):
    # Arrange
    fake_conference_exists.return_value = True

    fake_query = MagicMock('flask_sqlalchemy.query.Query')
    conferences = (
        Conference(
            id=1,
            short_name="C1",
            long_name="Conference 1",
            league_id=1,
            first_season_id=1920,
            last_season_id=1921
        ),
        Conference(
            id=2,
            short_name="C2",
            long_name="Conference 2",
            league_id=1,
            first_season_id=1922,
            last_season_id=1923
        ),
        Conference(
            id=3,
            short_name="C3",
            long_name="Conference 3",
            league_id=1,
            first_season_id=1924,
            last_season_id=1925
        ),
    )
    fake_query.return_value.all.return_value = conferences
    old_conference = conferences[1]
    fake_query.return_value.get.return_value = old_conference
    fake_conference.query.options = fake_query
    fake_joinedload.return_value = MagicMock()

    new_conference = Conference(
        id=2,
        short_name="C4",
        long_name="Conference 4",
        league_id=1,
        first_season_id=1926,
        last_season_id=1927
    )

    fake_try_commit.side_effect = IntegrityError('statement', 'params', Exception())

    # Act
    with pytest.raises(IntegrityError):
        conference_updated = test_repo.update_conference(new_conference)

    # Assert
    fake_sqla.session.add.assert_called_once_with(old_conference)
    fake_try_commit.assert_called_once()


@patch('app.data.repositories.conference_repository.try_commit')
@patch('app.data.repositories.conference_repository.sqla')
@patch('app.data.repositories.conference_repository.joinedload')
@patch('app.data.repositories.conference_repository.Conference')
def test_delete_conference_when_conference_does_not_exist_should_return_none_and_not_delete_conference_from_database(
        fake_conference, fake_joinedload, fake_sqla, fake_try_commit,
        test_repo
):
    # Arrange
    fake_query = MagicMock('flask_sqlalchemy.query.Query')
    conferences = (
        Conference(
            short_name="C1",
            long_name="Conference 1",
            league_id=1,
            first_season_id=1920,
            last_season_id=1921
        ),
        Conference(
            short_name="C2",
            long_name="Conference 2",
            league_id=1,
            first_season_id=1922,
            last_season_id=1923
        ),
        Conference(
            short_name="C3",
            long_name="Conference 3",
            league_id=1,
            first_season_id=1924,
            last_season_id=1925
        ),
    )
    fake_query.return_value.all.return_value = conferences
    fake_query.return_value.get.return_value = None
    fake_conference.query.options = fake_query
    fake_joinedload.return_value = MagicMock()

    id = 1

    # Act
    conference_deleted = test_repo.delete_conference(id)

    # Assert
    assert conference_deleted is None
    fake_sqla.session.delete.assert_not_called()
    fake_try_commit.assert_not_called()


@patch('app.data.repositories.conference_repository.try_commit')
@patch('app.data.repositories.conference_repository.sqla')
@patch('app.data.repositories.conference_repository.joinedload')
@patch('app.data.repositories.conference_repository.Conference')
def test_delete_conference_when_conference_exists_and_integrity_error_not_caught_should_return_conference_and_delete_conference_from_database(
        fake_conference, fake_joinedload, fake_sqla, fake_try_commit,
        test_repo
):
    # Arrange
    fake_query = MagicMock('flask_sqlalchemy.query.Query')
    conferences = (
        Conference(
            short_name="C1",
            long_name="Conference 1",
            league_id=1,
            first_season_id=1920,
            last_season_id=1921
        ),
        Conference(
            short_name="C2",
            long_name="Conference 2",
            league_id=1,
            first_season_id=1922,
            last_season_id=1923
        ),
        Conference(
            short_name="C3",
            long_name="Conference 3",
            league_id=1,
            first_season_id=1924,
            last_season_id=1925
        ),
    )
    fake_query.return_value.all.return_value = conferences
    id = 1
    fake_query.return_value.get.return_value = conferences[id]
    fake_conference.query.options = fake_query
    fake_joinedload.return_value = MagicMock()

    # Act
    try:
        conference_deleted = test_repo.delete_conference(id)
    except IntegrityError:
        assert False

    # Assert
    fake_sqla.session.delete.assert_called_once_with(conference_deleted)
    fake_try_commit.assert_called_once()
    assert conference_deleted is conferences[id]


@patch('app.data.repositories.conference_repository.try_commit')
@patch('app.data.repositories.conference_repository.sqla')
@patch('app.data.repositories.conference_repository.joinedload')
@patch('app.data.repositories.conference_repository.Conference')
def test_delete_conference_when_conference_exists_and_integrity_error_caught_should_rollback_commit(
        fake_conference, fake_joinedload, fake_sqla,
        fake_try_commit, test_repo
):
    # Arrange
    fake_query = MagicMock('flask_sqlalchemy.query.Query')
    conferences = (
        Conference(
            short_name="C1",
            long_name="Conference 1",
            league_id=1,
            first_season_id=1920,
            last_season_id=1921
        ),
        Conference(
            short_name="C2",
            long_name="Conference 2",
            league_id=1,
            first_season_id=1922,
            last_season_id=1923
        ),
        Conference(
            short_name="C3",
            long_name="Conference 3",
            league_id=1,
            first_season_id=1924,
            last_season_id=1925
        ),
    )
    fake_query.return_value.all.return_value = conferences
    id = 1
    fake_query.return_value.get.return_value = conferences[id]
    fake_conference.query.options = fake_query
    fake_joinedload.return_value = MagicMock()

    fake_try_commit.side_effect = IntegrityError('statement', 'params', Exception())

    # Act
    with pytest.raises(IntegrityError):
        conference_deleted = test_repo.delete_conference(id)

    # Assert
    fake_sqla.session.delete.assert_called_once_with(conferences[id])
    fake_try_commit.assert_called_once()
