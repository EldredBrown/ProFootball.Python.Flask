from unittest.mock import patch, call

import pytest
from sqlalchemy.exc import IntegrityError

from test_app import create_app

from app.data.models.season import Season
from app.data.models.conference import Conference
from app.data.models.game import Game
from app.data.models.league_season import LeagueSeason
from app.data.models.team_season import TeamSeason
from app.data.repositories.conference_repository import ConferenceRepository


@pytest.fixture
def test_app():
    return create_app()


@patch('app.data.repositories.conference_repository.Conference')
def test_get_conferences_should_get_conferences(fake_conference, test_app):
    with test_app.app_context():
        # Arrange
        conferences_in = [
            Conference(short_name="NFC"),
            Conference(short_name="AFC"),
            Conference(short_name="AAFC"),
        ]
        fake_conference.query.all.return_value = conferences_in

        # Act
        test_repo = ConferenceRepository()
        conferences_out = test_repo.get_conferences()

    # Assert
    assert conferences_out == conferences_in


@patch('app.data.repositories.conference_repository.Conference')
def test_get_conference_when_conferences_is_empty_should_return_none(fake_conference, test_app):
    with test_app.app_context():
        # Arrange
        conferences_in = []
        fake_conference.query.all.return_value = conferences_in

        # Act
        test_repo = ConferenceRepository()
        conference_out = test_repo.get_conference(1)

    # Assert
    assert conference_out is None


@patch('app.data.repositories.conference_repository.Conference')
def test_get_conference_when_conferences_is_not_empty_and_conference_is_not_found_should_return_none(fake_conference, test_app):
    with test_app.app_context():
        # Arrange
        conferences_in = [
            Conference(short_name="NFC"),
            Conference(short_name="AFC"),
            Conference(short_name="AAFC"),
        ]
        fake_conference.query.all.return_value = conferences_in
        fake_conference.query.get.return_value = None

        # Act
        test_repo = ConferenceRepository()

        id = len(conferences_in) + 1
        conference_out = test_repo.get_conference(id)

    # Assert
    assert conference_out is None


@patch('app.data.repositories.conference_repository.Conference')
def test_get_conference_when_conferences_is_not_empty_and_conference_is_found_should_return_conference(fake_conference, test_app):
    with test_app.app_context():
        # Arrange
        conferences_in = [
            Conference(short_name="NFC"),
            Conference(short_name="AFC"),
            Conference(short_name="AAFC"),
        ]
        fake_conference.query.all.return_value = conferences_in

        id = len(conferences_in) - 1
        fake_conference.query.get.return_value = conferences_in[id]

        # Act
        test_repo = ConferenceRepository()
        conference_out = test_repo.get_conference(id)

    # Assert
    assert conference_out is conferences_in[id]


@patch('app.data.repositories.conference_repository.Conference')
def test_get_conference_by_name_when_conferences_is_empty_should_return_none(fake_conference, test_app):
    with test_app.app_context():
        # Arrange
        conferences_in = []
        fake_conference.query.all.return_value = conferences_in

        # Act
        test_repo = ConferenceRepository()
        conference_out = test_repo.get_conference_by_name("NFC")

    # Assert
    assert conference_out is None


@patch('app.data.repositories.conference_repository.Conference')
def test_get_conference_by_name_when_conferences_is_not_empty_and_conference_with_short_name_is_not_found_should_return_none(
        fake_conference, test_app
):
    with test_app.app_context():
        # Arrange
        conferences_in = [
            Conference(short_name="NFC"),
            Conference(short_name="AFC"),
            Conference(short_name="AAFC"),
        ]
        fake_conference.query.all.return_value = conferences_in
        fake_conference.query.filter_by.return_value.first.return_value = None

        # Act
        test_repo = ConferenceRepository()
        conference_out = test_repo.get_conference_by_name("USFC")

    # Assert
    assert conference_out is None


@patch('app.data.repositories.conference_repository.Conference')
def test_get_conference_by_name_when_conferences_is_not_empty_and_conference_with_name_is_found_should_return_conference(
        fake_conference, test_app
):
    with test_app.app_context():
        # Arrange
        conferences_in = [
            Conference(short_name="NFC"),
            Conference(short_name="AFC"),
            Conference(short_name="AAFC"),
        ]
        fake_conference.query.all.return_value = conferences_in
        fake_conference.query.filter_by.return_value.first.return_value = conferences_in[-1]

        # Act
        test_repo = ConferenceRepository()
        conference_out = test_repo.get_conference_by_name("AAFC")

    # Assert
    assert conference_out is conferences_in[-1]


@patch('app.data.repositories.conference_repository.sqla')
@patch('app.data.repositories.conference_repository.conference_factory')
def test_add_conference_when_no_integrity_error_caught_should_add_conference(fake_conference_factory, fake_sqla, test_app):
    with test_app.app_context():
        # Arrange
        conference_in = Conference(short_name="NFC")
        fake_conference_factory.create_conference.return_value = conference_in

        # Act
        test_repo = ConferenceRepository()
        kwargs = {
            'short_name': "NFC",
        }
        conference_out = test_repo.add_conference(**kwargs)

    # Assert
    fake_sqla.session.add.assert_called_once_with(conference_in)
    fake_sqla.session.commit.assert_called_once()
    assert conference_out is conference_in


@patch('app.data.repositories.conference_repository.sqla')
@patch('app.data.repositories.conference_repository.conference_factory')
def test_add_conference_when_integrity_error_caught_should_rollback_transaction_and_reraise_error(
        fake_conference_factory, fake_sqla, test_app
):
    with test_app.app_context():
        # Arrange
        conference_in = Conference(short_name="NFC")
        fake_conference_factory.create_conference.return_value = conference_in
        fake_sqla.session.commit.side_effect = IntegrityError('statement', 'params', Exception())

        # Act
        test_repo = ConferenceRepository()
        kwargs = {
            'short_name': "NFC",
        }
        with pytest.raises(IntegrityError):
            conference_out = test_repo.add_conference(**kwargs)

    # Assert
    fake_sqla.session.rollback.assert_called_once()


@patch('app.data.repositories.conference_repository.sqla')
def test_add_conferences_when_conferences_arg_is_empty_should_add_no_conferences(fake_sqla, test_app):
    # Arrange
    with test_app.app_context():
        # Act
        test_repo = ConferenceRepository()

        conference_args = ()
        conferences_out = test_repo.add_conferences(conference_args)

    # Assert
    fake_sqla.session.add.assert_not_called()
    fake_sqla.session.commit.assert_called_once()
    assert conferences_out == []


@patch('app.data.repositories.conference_repository.sqla')
@patch('app.data.repositories.conference_repository.conference_factory')
def test_add_conferences_when_conferences_arg_is_not_empty_and_no_integrity_error_caught_should_add_conferences(
        fake_conference_factory, fake_sqla, test_app
):
    with test_app.app_context():
        # Arrange
        conferences_in = [
            Conference(short_name="NFC"),
            Conference(short_name="AFC"),
            Conference(short_name="AAFC"),
        ]
        fake_conference_factory.create_conference.side_effect = conferences_in

        # Act
        test_repo = ConferenceRepository()

        conference_args = (
            {'short_name': "NFC"},
            {'short_name': "AFC"},
            {'short_name': "AAFC"},
        )
        conferences_out = test_repo.add_conferences(conference_args)

    # Assert
    fake_sqla.session.add.assert_has_calls([
        call(conferences_in[0]),
        call(conferences_in[1]),
        call(conferences_in[2]),
    ])
    fake_sqla.session.commit.assert_called_once()
    assert conferences_out == conferences_in


@patch('app.data.repositories.conference_repository.sqla')
@patch('app.data.repositories.conference_repository.conference_factory')
def test_add_conferences_when_conferences_arg_is_not_empty_and_integrity_error_caught_should_rollback_transaction_and_reraise_error(
        fake_conference_factory, fake_sqla, test_app
):
    with test_app.app_context():
        # Arrange
        conferences_in = [
            Conference(short_name="NFC"),
            Conference(short_name="AFC"),
            Conference(short_name="AAFC"),
        ]
        fake_conference_factory.create_conference.side_effect = conferences_in
        fake_sqla.session.commit.side_effect = IntegrityError('statement', 'params', Exception())

        # Act
        test_repo = ConferenceRepository()

        conference_args = (
            {'short_name': "NFC"},
            {'short_name': "AFC"},
            {'short_name': "AAFC"},
        )
        with pytest.raises(IntegrityError):
            conferences_out = test_repo.add_conferences(conference_args)

    # Assert
    fake_sqla.session.rollback.assert_called_once()


@patch('app.data.repositories.conference_repository.Conference')
def test_conference_exists_when_conference_does_not_exist_should_return_false(fake_conference, test_app):
    with test_app.app_context():
        # Arrange
        conferences_in = [
            Conference(short_name="NFC"),
            Conference(short_name="AFC"),
            Conference(short_name="AAFC"),
        ]
        fake_conference.query.all.return_value = conferences_in
        fake_conference.query.get.return_value = None

        # Act
        test_repo = ConferenceRepository()
        conference_exists = test_repo.conference_exists(id=1)

    # Assert
    assert not conference_exists


@patch('app.data.repositories.conference_repository.Conference')
def test_conference_exists_when_conference_exists_should_return_true(fake_conference, test_app):
    with test_app.app_context():
        # Arrange
        conferences_in = [
            Conference(short_name="NFC"),
            Conference(short_name="AFC"),
            Conference(short_name="AAFC"),
        ]
        fake_conference.query.all.return_value = conferences_in
        fake_conference.query.get.return_value = conferences_in[1]

        # Act
        test_repo = ConferenceRepository()
        conference_exists = test_repo.conference_exists(id=1)

    # Assert
    assert conference_exists


def test_update_conference_when_id_not_in_kwargs_should_raise_value_error(test_app):
    # Arrange
    with test_app.app_context():
        # Act
        test_repo = ConferenceRepository()
        kwargs = {
            'short_name': "NFC",
            'long_name': "National Football Conference",
            'league_name': "NFL",
            'first_season_year': 1970,
            'last_season_year': None,
        }
        with pytest.raises(ValueError) as err:
            conference_updated = test_repo.update_conference(**kwargs)

    # Assert
    assert err.value.args[0] == "ID must be provided for existing Conference."


@patch('app.data.repositories.conference_repository.sqla')
@patch('app.data.repositories.conference_repository.ConferenceRepository.conference_exists')
def test_update_conference_when_id_is_in_kwargs_and_no_conference_exists_with_id_should_return_conference_and_not_update_database(
        fake_conference_exists, fake_sqla, test_app
):
    with test_app.app_context():
        # Arrange
        fake_conference_exists.return_value = False

        # Act
        test_repo = ConferenceRepository()
        kwargs = {
            'id': 1,
            'short_name': "NFC",
            'long_name': "National Football Conference",
            'league_name': "NFL",
            'first_season_year': 1970,
            'last_season_year': None,
        }
        try:
            conference_updated = test_repo.update_conference(**kwargs)
        except ValueError as err:
            assert False

    # Assert
    fake_sqla.session.add.assert_not_called()
    fake_sqla.session.commit.assert_not_called()
    assert isinstance(conference_updated, Conference)
    assert conference_updated.id == kwargs['id']
    assert conference_updated.short_name == kwargs['short_name']
    assert conference_updated.long_name == kwargs['long_name']
    assert conference_updated.league_name == kwargs['league_name']
    assert conference_updated.first_season_year == kwargs['first_season_year']
    assert conference_updated.last_season_year == kwargs['last_season_year']


@patch('app.data.repositories.conference_repository.sqla')
@patch('app.data.repositories.conference_repository.conference_factory')
@patch('app.data.repositories.conference_repository.Conference')
@patch('app.data.repositories.conference_repository.ConferenceRepository.conference_exists')
def test_update_conference_when_id_is_in_kwargs_and_conference_exists_with_id_and_no_integrity_error_caught_should_return_conference_and_update_database(
        fake_conference_exists, fake_conference, fake_conference_factory, fake_sqla, test_app
):
    with test_app.app_context():
        # Arrange
        fake_conference_exists.return_value = True

        conferences = [
            Conference(
                id=1, short_name="NFC", long_name="National Football Conference", league_name="NFL",
                first_season_year=1970, last_season_year=None
            ),
            Conference(
                id=2, short_name="AFC", long_name="American Football Conference", league_name="NFL",
                first_season_year=1970, last_season_year=None
            ),
            Conference(
                id=3, short_name="AAFC", long_name="All-American Football Conference", league_name="AAFL",
                first_season_year=1946, last_season_year=1949
            ),
        ]
        fake_conference.query.all.return_value = conferences

        old_conference = conferences[1]
        fake_conference.query.get.return_value = old_conference

        new_conference = Conference(
            id=2, short_name="USFC", long_name="United States Football Conference", league_name="USFL",
            first_season_year=1983, last_season_year=1987
        )
        fake_conference_factory.create_conference.return_value = new_conference

        # Act
        test_repo = ConferenceRepository()
        kwargs = {
            'id': 2,
            'short_name': "USFC",
            'long_name': "United States Football Conference",
            'league_name': "USFL",
            'first_season_year': 1983,
            'last_season_year': 1987,
        }
        try:
            conference_updated = test_repo.update_conference(**kwargs)
        except ValueError as err:
            assert False

    # Assert
    fake_sqla.session.add.assert_called_once_with(old_conference)
    fake_sqla.session.commit.assert_called_once()
    assert isinstance(conference_updated, Conference)
    assert conference_updated.id == kwargs['id']
    assert conference_updated.short_name == kwargs['short_name']
    assert conference_updated.long_name == kwargs['long_name']
    assert conference_updated.league_name == kwargs['league_name']
    assert conference_updated.first_season_year == kwargs['first_season_year']
    assert conference_updated.last_season_year == kwargs['last_season_year']
    assert conference_updated is new_conference


@patch('app.data.repositories.conference_repository.sqla')
@patch('app.data.repositories.conference_repository.conference_factory')
@patch('app.data.repositories.conference_repository.Conference')
@patch('app.data.repositories.conference_repository.ConferenceRepository.conference_exists')
def test_update_conference_when_id_is_in_kwargs_and_conference_exists_with_id_and_integrity_error_caught_should_rollback_transaction_and_reraise_error(
        fake_conference_exists, fake_conference, fake_conference_factory, fake_sqla, test_app
):
    with test_app.app_context():
        # Arrange
        fake_conference_exists.return_value = True

        conferences = [
            Conference(
                id=1, short_name="NFC", long_name="National Football Conference", league_name="NFL",
                first_season_year=1970, last_season_year=None
            ),
            Conference(
                id=2, short_name="AFC", long_name="American Football Conference", league_name="NFL",
                first_season_year=1970, last_season_year=None
            ),
            Conference(
                id=3, short_name="AAFC", long_name="All-American Football Conference", league_name="AAFL",
                first_season_year=1946, last_season_year=1949
            ),
        ]
        fake_conference.query.all.return_value = conferences

        old_conference = conferences[1]
        fake_conference.query.get.return_value = old_conference

        new_conference = Conference(
            id=2, short_name="USFC", long_name="United States Football Conference", league_name="USFL",
            first_season_year=1983, last_season_year=1987
        )
        fake_conference_factory.create_conference.return_value = new_conference

        fake_sqla.session.commit.side_effect = IntegrityError('statement', 'params', Exception())

        # Act
        test_repo = ConferenceRepository()
        kwargs = {
            'id': 2,
            'short_name': "USFC",
            'long_name': "United States Football Conference",
            'league_name': "USFL",
            'first_season_year': 1983,
            'last_season_year': 1987,
        }
        with pytest.raises(IntegrityError):
            conference_updated = test_repo.update_conference(**kwargs)

    # Assert
    fake_sqla.session.rollback.assert_called_once()


@patch('app.data.repositories.conference_repository.sqla')
@patch('app.data.repositories.conference_repository.Conference')
def test_delete_conference_when_conference_does_not_exist_should_return_none_and_not_delete_conference_from_database(
        fake_conference, fake_sqla, test_app
):
    with test_app.app_context():
        # Arrange
        conferences_in = [
            Conference(short_name="NFC"),
            Conference(short_name="AFC"),
            Conference(short_name="AAFC"),
        ]
        fake_conference.query.all.return_value = conferences_in
        fake_conference.query.get.return_value = None

        id = 1

        # Act
        test_repo = ConferenceRepository()
        conference_deleted = test_repo.delete_conference(id)

    # Assert
    assert conference_deleted is None
    fake_sqla.session.delete.assert_not_called()
    fake_sqla.session.commit.assert_not_called()


@patch('app.data.repositories.conference_repository.sqla')
@patch('app.data.repositories.conference_repository.Conference')
def test_delete_conference_when_conference_exists_should_return_conference_and_delete_conference_from_database(
        fake_conference, fake_sqla, test_app
):
    with test_app.app_context():
        # Arrange
        conferences_in = [
            Conference(short_name="NFC"),
            Conference(short_name="AFC"),
            Conference(short_name="AAFC"),
        ]
        fake_conference.query.all.return_value = conferences_in

        id = 1
        fake_conference.query.get.return_value = conferences_in[id]

        # Act
        test_repo = ConferenceRepository()
        conference_deleted = test_repo.delete_conference(id)

    # Assert
    fake_sqla.session.delete.assert_called_once_with(conference_deleted)
    fake_sqla.session.commit.assert_called_once()
    assert conference_deleted is conferences_in[id]
