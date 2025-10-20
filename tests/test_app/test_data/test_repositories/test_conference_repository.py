import pytest

from unittest.mock import patch, call

from app.data.models.conference import Conference
from app.data.models.division import Division
from app.data.models.game import Game
from app.data.models.league_season import LeagueSeason
from app.data.models.team_season import TeamSeason
from app.data.repositories.conference_repository import ConferenceRepository
from test_app import create_app


@patch('app.data.repositories.conference_repository.Conference')
def test_get_conferences_should_get_conferences(fake_conference):
    # Act
    test_app = create_app()
    with test_app.app_context():
        test_repo = ConferenceRepository()
        conferences = test_repo.get_conferences()

    # Assert
    fake_conference.query.all.assert_called_once()
    assert conferences == fake_conference.query.all.return_value


@patch('app.data.repositories.conference_repository.ConferenceRepository.get_conferences')
def test_get_conference_when_conferences_is_empty_should_return_none(fake_get_conferences):
    test_app = create_app()
    with test_app.app_context():
        # Arrange
        conferences = []
        fake_get_conferences.return_value = conferences

        # Act
        test_repo = ConferenceRepository()
        conference = test_repo.get_conference(id=1)

    # Assert
    assert conference is None


@patch('app.data.repositories.conference_repository.Conference')
@patch('app.data.repositories.conference_repository.ConferenceRepository.get_conferences')
def test_get_conference_when_conferences_is_not_empty_and_conference_is_not_found_should_return_none(fake_get_conferences, fake_conference):
    test_app = create_app()
    with test_app.app_context():
        # Arrange
        conferences = [
            Conference(short_name='A', long_name='A', league_name="A", first_season_year=1, last_season_year=2),
            Conference(short_name='B', long_name='B', league_name="A", first_season_year=3, last_season_year=4),
            Conference(short_name='C', long_name='C', league_name="A", first_season_year=5, last_season_year=None),
        ]
        fake_get_conferences.return_value = conferences

        id = len(conferences) + 1

        # Act
        test_repo = ConferenceRepository()
        conference = test_repo.get_conference(id=id)

    # Assert
    fake_conference.query.get.assert_called_once_with(id)
    assert conference == fake_conference.query.get.return_value


@patch('app.data.repositories.conference_repository.Conference')
@patch('app.data.repositories.conference_repository.ConferenceRepository.get_conferences')
def test_get_conference_when_conferences_is_not_empty_and_conference_is_found_should_return_conference(fake_get_conferences, fake_conference):
    test_app = create_app()
    with test_app.app_context():
        # Arrange
        conferences = [
            Conference(short_name='A', long_name='A', league_name="A", first_season_year=1, last_season_year=2),
            Conference(short_name='B', long_name='B', league_name="A", first_season_year=3, last_season_year=4),
            Conference(short_name='C', long_name='C', league_name="A", first_season_year=5, last_season_year=None),
        ]
        fake_get_conferences.return_value = conferences

        id = len(conferences) - 1

        # Act
        test_repo = ConferenceRepository()
        conference = test_repo.get_conference(id=id)

    # Assert
    fake_conference.query.get.assert_called_once_with(id)
    assert conference == fake_conference.query.get.return_value


@patch('app.data.repositories.conference_repository.ConferenceRepository.get_conferences')
def test_get_conference_by_name_when_conferences_is_empty_should_return_none(fake_get_conferences):
    test_app = create_app()
    with test_app.app_context():
        # Arrange
        conferences = []
        fake_get_conferences.return_value = conferences

        # Act
        test_repo = ConferenceRepository()
        conference = test_repo.get_conference_by_name(short_name="A")

    # Assert
    assert conference is None


@patch('app.data.repositories.conference_repository.Conference')
@patch('app.data.repositories.conference_repository.ConferenceRepository.get_conferences')
def test_get_conference_by_name_when_conferences_is_not_empty_and_conference_with_short_name_is_not_found_should_return_none(
        fake_get_conferences, fake_conference
):
    test_app = create_app()
    with test_app.app_context():
        # Arrange
        conferences = [
            Conference(short_name='A', long_name='A', league_name="A", first_season_year=1, last_season_year=2),
            Conference(short_name='B', long_name='B', league_name="A", first_season_year=3, last_season_year=4),
            Conference(short_name='C', long_name='C', league_name="A", first_season_year=5, last_season_year=None),
        ]
        fake_get_conferences.return_value = conferences

        # Act
        test_repo = ConferenceRepository()
        conference = test_repo.get_conference_by_name(short_name="D")

    # Assert
    fake_conference.query.filter_by.assert_called_once_with(short_name="D")
    fake_conference.query.filter_by.return_value.first.assert_called_once_with()
    assert conference == fake_conference.query.filter_by.return_value.first.return_value


@patch('app.data.repositories.conference_repository.Conference')
@patch('app.data.repositories.conference_repository.ConferenceRepository.get_conferences')
def test_get_conference_by_name_when_conferences_is_not_empty_and_conference_with_short_name_is_found_should_return_conference(
        fake_get_conferences, fake_conference
):
    test_app = create_app()
    with test_app.app_context():
        # Arrange
        conferences = [
            Conference(short_name='A', long_name='A', league_name="A", first_season_year=1, last_season_year=2),
            Conference(short_name='B', long_name='B', league_name="A", first_season_year=3, last_season_year=4),
            Conference(short_name='C', long_name='C', league_name="A", first_season_year=5, last_season_year=None),
        ]
        fake_get_conferences.return_value = conferences

        # Act
        test_repo = ConferenceRepository()
        conference = test_repo.get_conference_by_name(short_name="B")

    # Assert
    fake_conference.query.filter_by.assert_called_once_with(short_name="B")
    fake_conference.query.filter_by.return_value.first.assert_called_once_with()
    assert conference == fake_conference.query.filter_by.return_value.first.return_value


@patch('app.data.repositories.conference_repository.sqla')
def test_add_conference_should_add_conference(fake_sqla):
    # Arrange
    test_app = create_app()
    with test_app.app_context():
        # Act
        test_repo = ConferenceRepository()
        conference_in = Conference(
            short_name="AAFC", long_name="All-American Football Conference", league_name="A",
            first_season_year=1946, last_season_year=1949
        )
        conference_out = test_repo.add_conference(conference_in)

    # Assert
    fake_sqla.session.add.assert_called_once_with(conference_in)
    fake_sqla.session.commit.assert_called_once()
    assert conference_out is conference_in


@patch('app.data.repositories.conference_repository.sqla')
def test_add_conferences_when_conferences_arg_is_empty_should_add_no_conferences(fake_sqla):
    # Arrange
    test_app = create_app()
    with test_app.app_context():
        # Act
        test_repo = ConferenceRepository()
        conferences_in = ()
        conferences_out = test_repo.add_conferences(conferences_in)

    # Assert
    fake_sqla.session.add.assert_not_called()
    fake_sqla.session.commit.assert_called_once()
    assert conferences_out is conferences_in


@patch('app.data.repositories.conference_repository.sqla')
def test_add_conferences_when_conferences_arg_is_not_empty_should_add_conferences(fake_sqla):
    # Arrange
    test_app = create_app()
    with test_app.app_context():
        # Act
        test_repo = ConferenceRepository()
        conferences_in = (
            Conference(short_name="D", long_name="D", league_name="A", first_season_year=7, last_season_year=8),
            Conference(short_name="E", long_name="E", league_name="A", first_season_year=9, last_season_year=10),
            Conference(short_name="F", long_name="F", league_name="A", first_season_year=11, last_season_year=12),
        )
        conferences_out = test_repo.add_conferences(conferences_in)

    # Assert
    fake_sqla.session.add.assert_has_calls([
        call(conferences_in[0]),
        call(conferences_in[1]),
        call(conferences_in[2]),
    ])
    fake_sqla.session.commit.assert_called_once()
    assert conferences_out is conferences_in


@patch('app.data.repositories.conference_repository.sqla')
@patch('app.data.repositories.conference_repository.exists')
def test_conference_exists_should_query_database(fake_exists, fake_sqla):
    # Arrange
    test_app = create_app()
    with test_app.app_context():
        # Act
        test_repo = ConferenceRepository()
        conference_exists = test_repo.conference_exists(id=1)

    # Assert
    fake_exists.assert_called_once()
    fake_exists.return_value.where.assert_called_once()
    fake_sqla.session.query.assert_called_once_with(fake_exists.return_value.where.return_value)
    fake_sqla.session.query.return_value.scalar.assert_called_once()
    assert conference_exists == fake_sqla.session.query.return_value.scalar.return_value


@patch('app.data.repositories.conference_repository.ConferenceRepository.conference_exists')
def test_update_conference_when_conference_does_not_exist_should_return_conference(fake_conference_exists):
    # Arrange
    fake_conference_exists.return_value = False

    test_app = create_app()
    with test_app.app_context():
        # Act
        test_repo = ConferenceRepository()
        conference_to_update = Conference(
            id=1, short_name="B", long_name="B", league_name="A",
            first_season_year=98, last_season_year=99
        )
        conference_updated = test_repo.update_conference(conference_to_update)

    # Assert
    fake_conference_exists.assert_called_once_with(conference_to_update.id)
    assert conference_updated is conference_to_update


@patch('app.data.repositories.conference_repository.sqla')
@patch('app.data.repositories.conference_repository.ConferenceRepository.get_conference')
@patch('app.data.repositories.conference_repository.ConferenceRepository.conference_exists')
def test_update_conference_when_conference_exists_should_update_and_return_conference(
        fake_conference_exists, fake_get_conference, fake_sqla
):
    # Arrange
    test_app = create_app()
    with test_app.app_context():
        fake_conference_exists.return_value = True
        old_conference = Conference(
            id=1, short_name="A", long_name="A", league_name="A", first_season_year=1, last_season_year=2
        )
        fake_get_conference.return_value = old_conference

        new_conference = Conference(
            id=1, short_name="Z", long_name="Z", league_name="Z", first_season_year=98, last_season_year=99
        )

        # Act
        test_repo = ConferenceRepository()
        conference_updated = test_repo.update_conference(new_conference)

    # Assert
    fake_conference_exists.assert_called_once_with(old_conference.id)
    fake_get_conference.assert_called_once_with(old_conference.id)
    assert conference_updated.short_name == new_conference.short_name
    assert conference_updated.long_name == new_conference.long_name
    assert conference_updated.league_name == new_conference.league_name
    assert conference_updated.first_season_year == new_conference.first_season_year
    assert conference_updated.last_season_year == new_conference.last_season_year
    fake_sqla.session.add.assert_called_once_with(old_conference)
    fake_sqla.session.commit.assert_called_once()
    assert conference_updated is new_conference


@patch('app.data.repositories.conference_repository.ConferenceRepository.conference_exists')
def test_delete_conference_when_conference_does_not_exist_should_return_none(fake_conference_exists):
    # Arrange
    fake_conference_exists.return_value = False
    id = 1

    test_app = create_app()
    with test_app.app_context():
        # Act
        test_repo = ConferenceRepository()
        conference_deleted = test_repo.delete_conference(id=id)

    # Assert
    fake_conference_exists.assert_called_once_with(id)
    assert conference_deleted is None


@patch('app.data.repositories.conference_repository.sqla')
@patch('app.data.repositories.conference_repository.ConferenceRepository.get_conference')
@patch('app.data.repositories.conference_repository.ConferenceRepository.conference_exists')
def test_delete_conference_when_conference_exists_should_return_conference(fake_conference_exists, fake_get_conference, fake_sqla):
    # Arrange
    fake_conference_exists.return_value = True
    id = 1

    test_app = create_app()
    with test_app.app_context():
        # Act
        test_repo = ConferenceRepository()
        conference_deleted = test_repo.delete_conference(id=id)

    # Assert
    fake_conference_exists.assert_called_once_with(id)
    fake_get_conference.assert_called_once_with(id)
    fake_sqla.session.delete.assert_called_once_with(fake_get_conference.return_value)
    fake_sqla.session.commit.assert_called_once()
    return conference_deleted is fake_get_conference.return_value
