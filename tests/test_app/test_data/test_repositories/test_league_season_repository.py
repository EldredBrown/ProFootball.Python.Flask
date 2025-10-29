from unittest.mock import patch, call

from app.data.models.game import Game
from app.data.models.league_season import LeagueSeason
from app.data.models.team_season import TeamSeason
from app.data.repositories.league_season_repository import LeagueSeasonRepository
from test_app import create_app


@patch('app.data.repositories.league_season_repository.LeagueSeason')
def test_get_league_seasons_should_get_league_seasons(fake_league_season):
    # Act
    test_app = create_app()
    with test_app.app_context():
        test_repo = LeagueSeasonRepository()
        league_seasons = test_repo.get_league_seasons()

    # Assert
    fake_league_season.query.all.assert_called_once()
    assert league_seasons == fake_league_season.query.all.return_value


@patch('app.data.repositories.league_season_repository.LeagueSeasonRepository.get_league_seasons')
def test_get_league_season_when_league_seasons_is_empty_should_return_none(fake_get_league_seasons):
    test_app = create_app()
    with test_app.app_context():
        # Arrange
        league_seasons = []
        fake_get_league_seasons.return_value = league_seasons

        # Act
        test_repo = LeagueSeasonRepository()
        league_season = test_repo.get_league_season(1)

    # Assert
    assert league_season is None


@patch('app.data.repositories.league_season_repository.LeagueSeason')
@patch('app.data.repositories.league_season_repository.LeagueSeasonRepository.get_league_seasons')
def test_get_league_season_when_league_seasons_is_not_empty_and_league_season_is_not_found_should_return_none(
        fake_get_league_seasons, fake_league_season
):
    test_app = create_app()
    with test_app.app_context():
        # Arrange
        league_seasons = [
            LeagueSeason(league_name=1, season_year=1),
            LeagueSeason(league_name=2, season_year=1),
            LeagueSeason(league_name=1, season_year=2),
        ]
        fake_get_league_seasons.return_value = league_seasons

        id = len(league_seasons) + 1

        # Act
        test_repo = LeagueSeasonRepository()
        league_season = test_repo.get_league_season(id)

    # Assert
    fake_league_season.query.get.assert_called_once_with(id)
    assert league_season == fake_league_season.query.get.return_value


@patch('app.data.repositories.league_season_repository.LeagueSeason')
@patch('app.data.repositories.league_season_repository.LeagueSeasonRepository.get_league_seasons')
def test_get_league_season_when_league_seasons_is_not_empty_and_league_season_is_found_should_return_league_season(fake_get_league_seasons, fake_league_season):
    test_app = create_app()
    with test_app.app_context():
        # Arrange
        league_seasons = [
            LeagueSeason(league_name=1, season_year=1),
            LeagueSeason(league_name=2, season_year=1),
            LeagueSeason(league_name=1, season_year=2),
        ]
        fake_get_league_seasons.return_value = league_seasons

        id = len(league_seasons) - 1

        # Act
        test_repo = LeagueSeasonRepository()
        league_season = test_repo.get_league_season(id)

    # Assert
    fake_league_season.query.get.assert_called_once_with(id)
    assert league_season == fake_league_season.query.get.return_value


@patch('app.data.repositories.league_season_repository.LeagueSeasonRepository.get_league_seasons')
def test_get_league_season_by_league_and_season_when_league_seasons_is_empty_should_return_none(fake_get_league_seasons):
    test_app = create_app()
    with test_app.app_context():
        # Arrange
        league_seasons = []
        fake_get_league_seasons.return_value = league_seasons

        # Act
        test_repo = LeagueSeasonRepository()
        league_season = test_repo.get_league_season_by_league_name_and_season_year(league_name="A", season_year=1)

    # Assert
    assert league_season is None


@patch('app.data.repositories.league_season_repository.LeagueSeason')
@patch('app.data.repositories.league_season_repository.LeagueSeasonRepository.get_league_seasons')
def test_get_league_season_by_league_and_season_when_league_seasons_is_not_empty_and_league_season_is_not_found_should_return_none(
        fake_get_league_seasons, fake_league_season
):
    test_app = create_app()
    with test_app.app_context():
        # Arrange
        league_seasons = [
            LeagueSeason(league_name=1, season_year=1),
            LeagueSeason(league_name=2, season_year=1),
            LeagueSeason(league_name=1, season_year=2),
        ]
        fake_get_league_seasons.return_value = league_seasons

        # Act
        test_repo = LeagueSeasonRepository()
        league_season = test_repo.get_league_season_by_league_name_and_season_year(league_name=3, season_year=3)

    # Assert
    fake_league_season.query.filter_by.assert_called_once_with(league_name=3, season_year=3)
    fake_league_season.query.filter_by.return_value.first.assert_called_once()
    assert league_season == fake_league_season.query.filter_by.return_value.first.return_value


@patch('app.data.repositories.league_season_repository.LeagueSeason')
@patch('app.data.repositories.league_season_repository.LeagueSeasonRepository.get_league_seasons')
def test_get_league_season_by_league_and_season_when_league_seasons_is_not_empty_and_league_season_is_found_should_return_league_season(fake_get_league_seasons, fake_league_season):
    test_app = create_app()
    with test_app.app_context():
        # Arrange
        league_seasons = [
            LeagueSeason(league_name=1, season_year=1),
            LeagueSeason(league_name=2, season_year=1),
            LeagueSeason(league_name=1, season_year=2),
        ]
        fake_get_league_seasons.return_value = league_seasons

        # Act
        test_repo = LeagueSeasonRepository()
        league_season = test_repo.get_league_season_by_league_name_and_season_year(league_name=1, season_year=1)

    # Assert
    fake_league_season.query.filter_by.assert_called_once_with(league_name=1, season_year=1)
    fake_league_season.query.filter_by.return_value.first.assert_called_once()
    assert league_season == fake_league_season.query.filter_by.return_value.first.return_value


@patch('app.data.repositories.league_season_repository.sqla')
def test_add_league_season_should_add_league_season(fake_sqla):
    # Arrange
    test_app = create_app()
    with test_app.app_context():
        # Act
        test_repo = LeagueSeasonRepository()
        league_season_in = LeagueSeason(league_name=3, season_year=3)
        league_season_out = test_repo.add_league_season(league_season_in)

    # Assert
    fake_sqla.session.add.assert_called_once_with(league_season_in)
    fake_sqla.session.commit.assert_called_once()
    assert league_season_out is league_season_in


@patch('app.data.repositories.league_season_repository.sqla')
def test_add_league_seasons_when_league_seasons_arg_is_empty_should_add_no_league_seasons(fake_sqla):
    # Arrange
    test_app = create_app()
    with test_app.app_context():
        # Act
        test_repo = LeagueSeasonRepository()
        league_seasons_in = ()
        league_seasons_out = test_repo.add_league_seasons(league_seasons_in)

    # Assert
    fake_sqla.session.add.assert_not_called()
    fake_sqla.session.commit.assert_called_once()
    assert league_seasons_out is league_seasons_in


@patch('app.data.repositories.league_season_repository.sqla')
def test_add_league_seasons_when_league_seasons_arg_is_not_empty_should_add_league_seasons(fake_sqla):
    # Arrange
    test_app = create_app()
    with test_app.app_context():
        # Act
        test_repo = LeagueSeasonRepository()
        league_seasons_in = (
            LeagueSeason(league_name=3, season_year=4),
            LeagueSeason(league_name=4, season_year=3),
            LeagueSeason(league_name=4, season_year=4),
        )
        league_seasons_out = test_repo.add_league_seasons(league_seasons_in)

    # Assert
    fake_sqla.session.add.assert_has_calls([
        call(league_seasons_in[0]),
        call(league_seasons_in[1]),
        call(league_seasons_in[2]),
    ])
    fake_sqla.session.commit.assert_called_once()
    assert league_seasons_out is league_seasons_in


@patch('app.data.repositories.league_season_repository.sqla')
@patch('app.data.repositories.league_season_repository.exists')
def test_league_season_exists_should_query_database(fake_exists, fake_sqla):
    # Arrange
    test_app = create_app()
    with test_app.app_context():
        # Act
        test_repo = LeagueSeasonRepository()
        league_season_exists = test_repo.league_season_exists(id=1)

    # Assert
    fake_exists.assert_called_once()
    fake_exists.return_value.where.assert_called_once()
    fake_sqla.session.query.assert_called_once_with(fake_exists.return_value.where.return_value)
    fake_sqla.session.query.return_value.scalar.assert_called_once()
    assert league_season_exists == fake_sqla.session.query.return_value.scalar.return_value


@patch('app.data.repositories.league_season_repository.LeagueSeasonRepository.league_season_exists')
def test_update_league_season_when_league_season_does_not_exist_should_return_league_season(fake_league_season_exists):
    # Arrange
    fake_league_season_exists.return_value = False

    test_app = create_app()
    with test_app.app_context():
        # Act
        test_repo = LeagueSeasonRepository()
        league_season_to_update = LeagueSeason(
            league_name=3, season_year=3, total_games=100, total_points=2000, average_points=20
        )
        league_season_updated = test_repo.update_league_season(league_season_to_update)

    # Assert
    fake_league_season_exists.assert_called_once_with(league_season_to_update.id)
    assert league_season_updated is league_season_to_update


@patch('app.data.repositories.league_season_repository.sqla')
@patch('app.data.repositories.league_season_repository.LeagueSeasonRepository.get_league_season')
@patch('app.data.repositories.league_season_repository.LeagueSeasonRepository.league_season_exists')
def test_update_league_season_when_league_season_exists_should_update_and_return_league_season(
        fake_league_season_exists, fake_get_league_season, fake_sqla
):
    # Arrange
    test_app = create_app()
    with test_app.app_context():
        fake_league_season_exists.return_value = True
        old_league_season = LeagueSeason(
            league_name=1, season_year=1, total_games=100, total_points=2000, average_points=20
        )
        fake_get_league_season.return_value = old_league_season

        new_league_season = LeagueSeason(
            league_name=2, season_year=2, total_games=200, total_points=5000, average_points=25
        )

        # Act
        test_repo = LeagueSeasonRepository()
        league_season_updated = test_repo.update_league_season(new_league_season)

    # Assert
    fake_league_season_exists.assert_called_once_with(old_league_season.id)
    fake_get_league_season.assert_called_once_with(old_league_season.id)
    assert league_season_updated.league_name == new_league_season.league_name
    assert league_season_updated.season_year == new_league_season.season_year
    fake_sqla.session.add.assert_called_once_with(old_league_season)
    fake_sqla.session.commit.assert_called_once()
    assert league_season_updated is new_league_season


@patch('app.data.repositories.league_season_repository.LeagueSeasonRepository.league_season_exists')
def test_delete_league_season_when_league_season_does_not_exist_should_return_none(fake_league_season_exists):
    # Arrange
    fake_league_season_exists.return_value = False
    id = 1

    test_app = create_app()
    with test_app.app_context():
        # Act
        test_repo = LeagueSeasonRepository()
        league_season_deleted = test_repo.delete_league_season(id)

    # Assert
    fake_league_season_exists.assert_called_once_with(id)
    assert league_season_deleted is None


@patch('app.data.repositories.league_season_repository.sqla')
@patch('app.data.repositories.league_season_repository.LeagueSeasonRepository.get_league_season')
@patch('app.data.repositories.league_season_repository.LeagueSeasonRepository.league_season_exists')
def test_delete_league_season_when_league_season_exists_should_return_league_season(fake_league_season_exists, fake_get_league_season, fake_sqla):
    # Arrange
    fake_league_season_exists.return_value = True
    id = 1

    test_app = create_app()
    with test_app.app_context():
        # Act
        test_repo = LeagueSeasonRepository()
        league_season_deleted = test_repo.delete_league_season(id)

    # Assert
    fake_league_season_exists.assert_called_once_with(id)
    fake_get_league_season.assert_called_once_with(id)
    fake_sqla.session.delete.assert_called_once_with(fake_get_league_season.return_value)
    fake_sqla.session.commit.assert_called_once()
    return league_season_deleted is fake_get_league_season.return_value
