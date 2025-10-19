from unittest.mock import patch, call

from test_app import create_app

from app.data.models.season import Season
from app.data.models.game import Game
from app.data.models.league_season import LeagueSeason
from app.data.models.team_season import TeamSeason
from app.data.repositories.season_repository import SeasonRepository


@patch('app.data.repositories.season_repository.Season')
def test_get_seasons_should_get_seasons(fake_season):
    # Act
    test_app = create_app()
    with test_app.app_context():
        test_repo = SeasonRepository()
        seasons = test_repo.get_seasons()

    # Assert
    fake_season.query.all.assert_called_once()
    assert seasons == fake_season.query.all.return_value


@patch('app.data.repositories.season_repository.SeasonRepository.get_seasons')
def test_get_season_when_seasons_is_empty_should_return_none(fake_get_seasons):
    test_app = create_app()
    with test_app.app_context():
        # Arrange
        seasons = []
        fake_get_seasons.return_value = seasons

        # Act
        test_repo = SeasonRepository()
        season = test_repo.get_season(1)

    # Assert
    assert season is None


@patch('app.data.repositories.season_repository.Season')
@patch('app.data.repositories.season_repository.SeasonRepository.get_seasons')
def test_get_season_when_seasons_is_not_empty_and_season_is_not_found_should_return_none(fake_get_seasons, fake_season):
    test_app = create_app()
    with test_app.app_context():
        # Arrange
        seasons = [
            Season(year=1),
            Season(year=2),
            Season(year=3),
        ]
        fake_get_seasons.return_value = seasons

        id = len(seasons) + 1

        # Act
        test_repo = SeasonRepository()
        season = test_repo.get_season(id)

    # Assert
    fake_season.query.get.assert_called_once_with(id)
    assert season == fake_season.query.get.return_value


@patch('app.data.repositories.season_repository.Season')
@patch('app.data.repositories.season_repository.SeasonRepository.get_seasons')
def test_get_season_when_seasons_is_not_empty_and_season_is_found_should_return_season(fake_get_seasons, fake_season):
    test_app = create_app()
    with test_app.app_context():
        # Arrange
        seasons = [
            Season(year=1),
            Season(year=2),
            Season(year=3),
        ]
        fake_get_seasons.return_value = seasons

        id = len(seasons) - 1

        # Act
        test_repo = SeasonRepository()
        season = test_repo.get_season(id)

    # Assert
    fake_season.query.get.assert_called_once_with(id)
    assert season == fake_season.query.get.return_value


@patch('app.data.repositories.season_repository.SeasonRepository.get_seasons')
def test_get_season_by_year_when_seasons_is_empty_should_return_none(fake_get_seasons):
    test_app = create_app()
    with test_app.app_context():
        # Arrange
        seasons = []
        fake_get_seasons.return_value = seasons

        # Act
        test_repo = SeasonRepository()
        season = test_repo.get_season_by_year(year=1)

    # Assert
    assert season is None


@patch('app.data.repositories.season_repository.Season')
@patch('app.data.repositories.season_repository.SeasonRepository.get_seasons')
def test_get_season_by_year_when_seasons_is_not_empty_and_season_with_year_is_not_found_should_return_none(
        fake_get_seasons, fake_season
):
    test_app = create_app()
    with test_app.app_context():
        # Arrange
        seasons = [
            Season(year=1),
            Season(year=2),
            Season(year=3),
        ]
        fake_get_seasons.return_value = seasons

        year = len(seasons) + 1

        # Act
        test_repo = SeasonRepository()
        season = test_repo.get_season_by_year(year=year)

    # Assert
    fake_season.query.filter_by.assert_called_once_with(year=year)
    fake_season.query.filter_by.return_value.first.assert_called_once_with()
    assert season == fake_season.query.filter_by.return_value.first.return_value


@patch('app.data.repositories.season_repository.Season')
@patch('app.data.repositories.season_repository.SeasonRepository.get_seasons')
def test_get_season_by_year_when_seasons_is_not_empty_and_season_with_year_is_found_should_return_season(
        fake_get_seasons, fake_season
):
    test_app = create_app()
    with test_app.app_context():
        # Arrange
        seasons = [
            Season(year=1),
            Season(year=2),
            Season(year=3),
        ]
        fake_get_seasons.return_value = seasons

        year = len(seasons) - 1

        # Act
        test_repo = SeasonRepository()
        season = test_repo.get_season_by_year(year=year)

    # Assert
    fake_season.query.filter_by.assert_called_once_with(year=year)
    fake_season.query.filter_by.return_value.first.assert_called_once_with()
    assert season == fake_season.query.filter_by.return_value.first.return_value


@patch('app.data.repositories.season_repository.sqla')
def test_add_season_should_add_season(fake_sqla):
    # Arrange
    test_app = create_app()
    with test_app.app_context():
        # Act
        test_repo = SeasonRepository()
        season_in = Season(year=1)
        season_out = test_repo.add_season(season_in)

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
        seasons_in = ()
        seasons_out = test_repo.add_seasons(seasons_in)

    # Assert
    fake_sqla.session.add.assert_not_called()
    fake_sqla.session.commit.assert_called_once()
    assert seasons_out is seasons_in


@patch('app.data.repositories.season_repository.sqla')
def test_add_seasons_when_seasons_arg_is_not_empty_should_add_seasons(fake_sqla):
    # Arrange
    test_app = create_app()
    with test_app.app_context():
        # Act
        test_repo = SeasonRepository()
        seasons_in = (
            Season(year=1),
            Season(year=2),
            Season(year=3),
        )
        seasons_out = test_repo.add_seasons(seasons_in)

    # Assert
    fake_sqla.session.add.assert_has_calls([
        call(seasons_in[0]),
        call(seasons_in[1]),
        call(seasons_in[2]),
    ])
    fake_sqla.session.commit.assert_called_once()
    assert seasons_out is seasons_in


@patch('app.data.repositories.season_repository.sqla')
@patch('app.data.repositories.season_repository.exists')
def test_season_exists_should_query_database(fake_exists, fake_sqla):
    # Arrange
    test_app = create_app()
    with test_app.app_context():
        # Act
        test_repo = SeasonRepository()
        season_exists = test_repo._season_exists(id=1)

    # Assert
    fake_exists.assert_called_once()
    fake_exists.return_value.where.assert_called_once()
    fake_sqla.session.query.assert_called_once_with(fake_exists.return_value.where.return_value)
    fake_sqla.session.query.return_value.scalar.assert_called_once()
    assert season_exists == fake_sqla.session.query.return_value.scalar.return_value


@patch('app.data.repositories.season_repository.SeasonRepository._season_exists')
def test_update_season_when_season_does_not_exist_should_return_season(fake_season_exists):
    # Arrange
    fake_season_exists.return_value = False

    test_app = create_app()
    with test_app.app_context():
        # Act
        test_repo = SeasonRepository()
        season_to_update = Season(year=1)
        season_updated = test_repo.update_season(season_to_update)

    # Assert
    fake_season_exists.assert_called_once_with(season_to_update.id)
    assert season_updated is season_to_update


@patch('app.data.repositories.season_repository.sqla')
@patch('app.data.repositories.season_repository.SeasonRepository.get_season')
@patch('app.data.repositories.season_repository.SeasonRepository._season_exists')
def test_update_season_when_season_exists_should_update_and_return_season(
        fake_season_exists, fake_get_season, fake_sqla
):
    # Arrange
    test_app = create_app()
    with test_app.app_context():
        fake_season_exists.return_value = True
        old_season = Season(id=1, year=1)
        fake_get_season.return_value = old_season

        new_season = Season(id=1, year=99)

        # Act
        test_repo = SeasonRepository()
        season_updated = test_repo.update_season(new_season)

    # Assert
    fake_season_exists.assert_called_once_with(old_season.id)
    fake_get_season.assert_called_once_with(old_season.id)
    assert season_updated.year == new_season.year
    assert season_updated.num_of_weeks_scheduled == new_season.num_of_weeks_scheduled
    assert season_updated.num_of_weeks_completed == new_season.num_of_weeks_completed
    fake_sqla.session.add.assert_called_once_with(old_season)
    fake_sqla.session.commit.assert_called_once()
    assert season_updated is new_season


@patch('app.data.repositories.season_repository.SeasonRepository._season_exists')
def test_delete_season_when_season_does_not_exist_should_return_none(fake_season_exists):
    # Arrange
    fake_season_exists.return_value = False
    id = 1

    test_app = create_app()
    with test_app.app_context():
        # Act
        test_repo = SeasonRepository()
        season_deleted = test_repo.delete_season(id)

    # Assert
    fake_season_exists.assert_called_once_with(id)
    assert season_deleted is None


@patch('app.data.repositories.season_repository.sqla')
@patch('app.data.repositories.season_repository.SeasonRepository.get_season')
@patch('app.data.repositories.season_repository.SeasonRepository._season_exists')
def test_delete_season_when_season_exists_should_return_season(fake_season_exists, fake_get_season, fake_sqla):
    # Arrange
    fake_season_exists.return_value = True
    id = 1

    test_app = create_app()
    with test_app.app_context():
        # Act
        test_repo = SeasonRepository()
        season_deleted = test_repo.delete_season(id)

    # Assert
    fake_season_exists.assert_called_once_with(id)
    fake_get_season.assert_called_once_with(id)
    fake_sqla.session.delete.assert_called_once_with(fake_get_season.return_value)
    fake_sqla.session.commit.assert_called_once()
    return season_deleted is fake_get_season.return_value
