from unittest.mock import patch, call

import pytest

from test_app import create_app

from app.data.models.season import Season
from app.data.models.game import Game
from app.data.models.league_season import LeagueSeason
from app.data.models.team_season import TeamSeason
from app.data.repositories.season_repository import SeasonRepository


@patch('app.data.repositories.season_repository.Season')
def test_get_seasons_should_get_seasons(fake_season):
    # Arrange
    seasons_in = [
        Season(year=1),
        Season(year=2),
        Season(year=3),
    ]
    fake_season.query.all.return_value = seasons_in

    # Act
    test_app = create_app()
    with test_app.app_context():
        test_repo = SeasonRepository()
        seasons_out = test_repo.get_seasons()

    # Assert
    assert seasons_out == seasons_in


@patch('app.data.repositories.season_repository.Season')
def test_get_season_when_seasons_is_empty_should_return_none(fake_season):
    # Arrange
    seasons_in = []
    fake_season.query.all.return_value = seasons_in

    test_app = create_app()
    with test_app.app_context():
        # Act
        test_repo = SeasonRepository()
        season_out = test_repo.get_season(1)

    # Assert
    assert season_out is None


@patch('app.data.repositories.season_repository.Season')
def test_get_season_when_seasons_is_not_empty_and_season_is_not_found_should_return_none(fake_season):
    seasons_in = [
        Season(year=1),
        Season(year=2),
        Season(year=3),
    ]
    fake_season.query.all.return_value = seasons_in
    fake_season.query.get.return_value = None

    test_app = create_app()
    with test_app.app_context():
        # Act
        test_repo = SeasonRepository()

        id = len(seasons_in) + 1
        season_out = test_repo.get_season(id)

    # Assert
    assert season_out is None


@patch('app.data.repositories.season_repository.Season')
def test_get_season_when_seasons_is_not_empty_and_season_is_found_should_return_season(fake_season):
    seasons_in = [
        Season(year=1),
        Season(year=2),
        Season(year=3),
    ]
    fake_season.query.all.return_value = seasons_in

    id = len(seasons_in) - 1
    fake_season.query.get.return_value = seasons_in[id]

    test_app = create_app()
    with test_app.app_context():
        # Act
        test_repo = SeasonRepository()

        season_out = test_repo.get_season(id)

    # Assert
    assert season_out is seasons_in[id]


@patch('app.data.repositories.season_repository.Season')
def test_get_season_by_year_when_seasons_is_empty_should_return_none(fake_season):
    # Arrange
    seasons_in = []
    fake_season.query.all.return_value = seasons_in

    test_app = create_app()
    with test_app.app_context():
        # Act
        test_repo = SeasonRepository()
        season_out = test_repo.get_season_by_year(1920)

    # Assert
    assert season_out is None


@patch('app.data.repositories.season_repository.Season')
def test_get_season_by_year_when_seasons_is_not_empty_and_season_with_year_is_not_found_should_return_none(fake_season):
    seasons_in = [
        Season(year=1920),
        Season(year=1921),
        Season(year=1922),
    ]
    fake_season.query.all.return_value = seasons_in
    fake_season.query.filter_by.return_value.first.return_value = None

    test_app = create_app()
    with test_app.app_context():
        # Act
        test_repo = SeasonRepository()
        season_out = test_repo.get_season_by_year(1923)

    # Assert
    assert season_out is None


@patch('app.data.repositories.season_repository.Season')
def test_get_season_by_year_when_seasons_is_not_empty_and_season_with_year_is_found_should_return_season(fake_season):
    seasons_in = [
        Season(year=1920),
        Season(year=1921),
        Season(year=1922),
    ]
    fake_season.query.all.return_value = seasons_in
    fake_season.query.filter_by.return_value.first.return_value = seasons_in[-1]

    test_app = create_app()
    with test_app.app_context():
        # Act
        test_repo = SeasonRepository()
        season_out = test_repo.get_season_by_year(1922)

    # Assert
    assert season_out is seasons_in[-1]


@patch('app.data.repositories.season_repository.sqla')
@patch('app.data.repositories.season_repository.season_factory')
def test_add_season_should_add_season(fake_season_factory, fake_sqla):
    # Arrange
    season_in = Season(year=1)
    fake_season_factory.create_season.return_value = season_in

    test_app = create_app()
    with test_app.app_context():
        # Act
        test_repo = SeasonRepository()
        kwargs = {
            'year': 1,
        }
        season_out = test_repo.add_season(**kwargs)

    # Assert
    fake_sqla.session.add.assert_called_once_with(season_in)
    fake_sqla.session.commit.assert_called_once()
    assert season_out is season_in


@patch('app.data.repositories.season_repository.sqla')
def test_add_seasons_when_seasons_arg_is_empty_should_add_no_seasons(fake_sqla):
    # Arrange
    test_app = create_app()
    with test_app.app_context():
        # Act
        test_repo = SeasonRepository()

        season_args = ()
        seasons_out = test_repo.add_seasons(season_args)

    # Assert
    fake_sqla.session.add.assert_not_called()
    fake_sqla.session.commit.assert_called_once()
    assert seasons_out == []


@patch('app.data.repositories.season_repository.sqla')
@patch('app.data.repositories.season_repository.season_factory')
def test_add_seasons_when_seasons_arg_is_not_empty_should_add_seasons(fake_season_factory, fake_sqla):
    # Arrange
    seasons_in = [
        Season(year=1),
        Season(year=2),
        Season(year=3),
    ]
    fake_season_factory.create_season.side_effect = seasons_in

    test_app = create_app()
    with test_app.app_context():
        # Act
        test_repo = SeasonRepository()

        season_args = (
            {'year': 1},
            {'year': 2},
            {'year': 3},
        )
        seasons_out = test_repo.add_seasons(season_args)

    # Assert
    fake_sqla.session.add.assert_has_calls([
        call(seasons_in[0]),
        call(seasons_in[1]),
        call(seasons_in[2]),
    ])
    fake_sqla.session.commit.assert_called_once()
    assert seasons_out == seasons_in


@patch('app.data.repositories.season_repository.Season')
def test_season_exists_when_season_does_not_exist_should_return_false(fake_season):
    # Arrange
    seasons_in = [
        Season(year=1),
        Season(year=2),
        Season(year=3),
    ]
    fake_season.query.all.return_value = seasons_in
    fake_season.query.get.return_value = None

    test_app = create_app()
    with test_app.app_context():
        # Act
        test_repo = SeasonRepository()
        season_exists = test_repo.season_exists(id=1)

    # Assert
    assert not season_exists


@patch('app.data.repositories.season_repository.Season')
def test_season_exists_when_season_exists_should_return_true(fake_season):
    # Arrange
    seasons_in = [
        Season(year=1),
        Season(year=2),
        Season(year=3),
    ]
    fake_season.query.all.return_value = seasons_in
    fake_season.query.get.return_value = seasons_in[1]

    test_app = create_app()
    with test_app.app_context():
        # Act
        test_repo = SeasonRepository()
        season_exists = test_repo.season_exists(id=1)

    # Assert
    assert season_exists


def test_update_season_when_id_not_in_kwargs_should_raise_value_error():
    # Arrange
    test_app = create_app()
    with test_app.app_context():
        # Act
        test_repo = SeasonRepository()
        kwargs = {
            'year': 1,
            'num_of_weeks_scheduled': 2,
            'num_of_weeks_completed': 3
        }
        with pytest.raises(ValueError) as err:
            season_updated = test_repo.update_season(**kwargs)

    # Assert
    assert err.value.args[0] == "ID must be provided for existing Season."


@patch('app.data.repositories.season_repository.sqla')
@patch('app.data.repositories.season_repository.SeasonRepository.season_exists')
def test_update_season_when_id_is_in_kwargs_and_no_season_exists_with_id_should_return_season_and_not_update_database(
        fake_season_exists, fake_sqla
):
    # Arrange
    fake_season_exists.return_value = False

    test_app = create_app()
    with test_app.app_context():
        # Act
        test_repo = SeasonRepository()
        kwargs = {
            'id': 1,
            'year': 1920,
            'num_of_weeks_scheduled': 13,
            'num_of_weeks_completed': 0
        }
        try:
            season_updated = test_repo.update_season(**kwargs)
        except ValueError as err:
            assert False

    # Assert
    assert isinstance(season_updated, Season)
    assert season_updated.id == 1
    assert season_updated.year == 1920
    assert season_updated.num_of_weeks_scheduled == 13
    assert season_updated.num_of_weeks_completed == 0
    fake_sqla.session.add.assert_not_called()
    fake_sqla.session.commit.assert_not_called()


@patch('app.data.repositories.season_repository.sqla')
@patch('app.data.repositories.season_repository.season_factory')
@patch('app.data.repositories.season_repository.Season')
@patch('app.data.repositories.season_repository.SeasonRepository.season_exists')
def test_update_season_when_id_is_in_kwargs_and_season_exists_with_id_should_return_season_and_update_database(
        fake_season_exists, fake_season, fake_season_factory, fake_sqla
):
    # Arrange
    fake_season_exists.return_value = True

    seasons = [
        Season(id=1, year=1, num_of_weeks_scheduled=1, num_of_weeks_completed=1),
        Season(id=2, year=2, num_of_weeks_scheduled=2, num_of_weeks_completed=2),
        Season(id=3, year=3, num_of_weeks_scheduled=3, num_of_weeks_completed=3),
    ]
    fake_season.query.all.return_value = seasons

    old_season = seasons[1]
    fake_season.query.get.return_value = old_season

    new_season = Season(id=2, year=4, num_of_weeks_scheduled=4, num_of_weeks_completed=4)
    fake_season_factory.create_season.return_value = new_season

    test_app = create_app()
    with test_app.app_context():
        # Act
        test_repo = SeasonRepository()
        kwargs = {
            'id': 2,
            'year': 4,
            'num_of_weeks_scheduled': 4,
            'num_of_weeks_completed': 4
        }
        try:
            season_updated = test_repo.update_season(**kwargs)
        except ValueError as err:
            assert False

    # Assert
    assert isinstance(season_updated, Season)
    assert season_updated.id == 2
    assert season_updated.year == 4
    assert season_updated.num_of_weeks_scheduled == 4
    assert season_updated.num_of_weeks_completed == 4
    fake_sqla.session.add.assert_called_once_with(old_season)
    fake_sqla.session.commit.assert_called_once()
    assert season_updated is new_season


@patch('app.data.repositories.season_repository.sqla')
@patch('app.data.repositories.season_repository.Season')
def test_delete_season_when_season_does_not_exist_should_return_none_and_not_delete_season_from_database(
        fake_season, fake_sqla
):
    # Arrange
    seasons_in = [
        Season(year=1),
        Season(year=2),
        Season(year=3),
    ]
    fake_season.query.all.return_value = seasons_in
    fake_season.query.get.return_value = None

    id = 1

    test_app = create_app()
    with test_app.app_context():
        # Act
        test_repo = SeasonRepository()
        season_deleted = test_repo.delete_season(id)

    # Assert
    assert season_deleted is None
    fake_sqla.session.delete.assert_not_called()
    fake_sqla.session.commit.assert_not_called()


@patch('app.data.repositories.season_repository.sqla')
@patch('app.data.repositories.season_repository.Season')
def test_delete_season_when_season_exists_should_return_season_and_delete_season_from_database(
        fake_season, fake_sqla
):
    # Arrange
    seasons_in = [
        Season(year=1),
        Season(year=2),
        Season(year=3),
    ]
    fake_season.query.all.return_value = seasons_in

    id = 1
    fake_season.query.get.return_value = seasons_in[id]

    test_app = create_app()
    with test_app.app_context():
        # Act
        test_repo = SeasonRepository()
        season_deleted = test_repo.delete_season(id)

    # Assert
    fake_sqla.session.delete.assert_called_once_with(season_deleted)
    fake_sqla.session.commit.assert_called_once()
    assert season_deleted is seasons_in[id]
