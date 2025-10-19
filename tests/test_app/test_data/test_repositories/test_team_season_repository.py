import pytest

from unittest.mock import patch, call

from app import create_app
from app.data.models.game import Game
from app.data.models.league_season import LeagueSeason
from app.data.models.team_season import TeamSeason
from app.data.repositories.team_season_repository import TeamSeasonRepository


@patch('app.data.repositories.team_season_repository.TeamSeason')
def test_get_team_seasons_should_get_team_seasons(fake_team_season):
    # Act
    test_app = create_app()
    with test_app.app_context():
        test_repo = TeamSeasonRepository()
        team_seasons = test_repo.get_team_seasons()

    # Assert
    fake_team_season.query.all.assert_called_once()
    assert team_seasons == fake_team_season.query.all.return_value


@patch('app.data.repositories.team_season_repository.TeamSeasonRepository.get_team_seasons')
def test_get_team_season_when_team_seasons_is_empty_should_return_none(fake_get_team_seasons):
    test_app = create_app()
    with test_app.app_context():
        # Arrange
        team_seasons = []
        fake_get_team_seasons.return_value = team_seasons

        # Act
        test_repo = TeamSeasonRepository()
        team_season = test_repo.get_team_season(1)

    # Assert
    assert team_season is None


@patch('app.data.repositories.team_season_repository.TeamSeason')
@patch('app.data.repositories.team_season_repository.TeamSeasonRepository.get_team_seasons')
def test_get_team_season_when_team_seasons_is_not_empty_and_team_season_is_not_found_should_return_none(
        fake_get_team_seasons, fake_team_season
):
    test_app = create_app()
    with test_app.app_context():
        # Arrange
        team_seasons = [
            TeamSeason(team_name="A", season_year=1),
            TeamSeason(team_name="B", season_year=1),
            TeamSeason(team_name="A", season_year=2),
        ]
        fake_get_team_seasons.return_value = team_seasons

        id = len(team_seasons) + 1

        # Act
        test_repo = TeamSeasonRepository()
        team_season = test_repo.get_team_season(id)

    # Assert
    fake_team_season.query.get.assert_called_once_with(id)
    assert team_season == fake_team_season.query.get.return_value


@patch('app.data.repositories.team_season_repository.TeamSeason')
@patch('app.data.repositories.team_season_repository.TeamSeasonRepository.get_team_seasons')
def test_get_team_season_when_team_seasons_is_not_empty_and_team_season_is_found_should_return_team_season(
        fake_get_team_seasons, fake_team_season
):
    test_app = create_app()
    with test_app.app_context():
        # Arrange
        team_seasons = [
            TeamSeason(team_name="A", season_year=1),
            TeamSeason(team_name="B", season_year=1),
            TeamSeason(team_name="A", season_year=2),
        ]
        fake_get_team_seasons.return_value = team_seasons

        id = len(team_seasons) - 1

        # Act
        test_repo = TeamSeasonRepository()
        team_season = test_repo.get_team_season(id)

    # Assert
    fake_team_season.query.get.assert_called_once_with(id)
    assert team_season == fake_team_season.query.get.return_value


@patch('app.data.repositories.team_season_repository.TeamSeasonRepository.get_team_seasons')
def test_get_team_seasons_by_season_when_team_seasons_is_empty_should_return_none(fake_get_team_seasons):
    test_app = create_app()
    with test_app.app_context():
        # Arrange
        team_seasons = []
        fake_get_team_seasons.return_value = team_seasons

        # Act
        test_repo = TeamSeasonRepository()
        team_season = test_repo.get_team_seasons_by_season(season_year=1)

    # Assert
    assert team_season is None


@patch('app.data.repositories.team_season_repository.TeamSeason')
@patch('app.data.repositories.team_season_repository.TeamSeasonRepository.get_team_seasons')
def test_get_team_seasons_by_season_when_team_seasons_is_not_empty_and_team_season_is_not_found_should_return_none(
        fake_get_team_seasons, fake_team_season
):
    test_app = create_app()
    with test_app.app_context():
        # Arrange
        team_seasons = [
            TeamSeason(team_name="A", season_year=1),
            TeamSeason(team_name="B", season_year=1),
            TeamSeason(team_name="A", season_year=2),
        ]
        fake_get_team_seasons.return_value = team_seasons

        # Act
        test_repo = TeamSeasonRepository()
        team_season = test_repo.get_team_seasons_by_season(season_year=3)

    # Assert
    fake_team_season.query.filter_by.assert_called_once_with(season_year=3)
    fake_team_season.query.filter_by.return_value.fetchall.assert_called_once()
    assert team_season == fake_team_season.query.filter_by.return_value.fetchall.return_value


@patch('app.data.repositories.team_season_repository.TeamSeason')
@patch('app.data.repositories.team_season_repository.TeamSeasonRepository.get_team_seasons')
def test_get_team_season_by_season_when_team_seasons_is_not_empty_and_team_season_is_found_should_return_team_season(fake_get_team_seasons, fake_team_season):
    test_app = create_app()
    with test_app.app_context():
        # Arrange
        team_seasons = [
            TeamSeason(team_name="A", season_year=1),
            TeamSeason(team_name="B", season_year=1),
            TeamSeason(team_name="A", season_year=2),
        ]
        fake_get_team_seasons.return_value = team_seasons

        # Act
        test_repo = TeamSeasonRepository()
        team_season = test_repo.get_team_seasons_by_season(season_year=1)

    # Assert
    fake_team_season.query.filter_by.assert_called_once_with(season_year=1)
    fake_team_season.query.filter_by.return_value.fetchall.assert_called_once()
    assert team_season == fake_team_season.query.filter_by.return_value.fetchall.return_value


@patch('app.data.repositories.team_season_repository.TeamSeasonRepository.get_team_seasons')
def test_get_team_season_by_team_and_season_when_team_seasons_is_empty_should_return_none(fake_get_team_seasons):
    test_app = create_app()
    with test_app.app_context():
        # Arrange
        team_seasons = []
        fake_get_team_seasons.return_value = team_seasons

        # Act
        test_repo = TeamSeasonRepository()
        team_season = test_repo.get_team_season_by_team_and_season(team_name="A", season_year=1)

    # Assert
    assert team_season is None


@patch('app.data.repositories.team_season_repository.TeamSeason')
@patch('app.data.repositories.team_season_repository.TeamSeasonRepository.get_team_seasons')
def test_get_team_season_by_team_and_season_when_team_seasons_is_not_empty_and_team_season_is_not_found_should_return_none(
        fake_get_team_seasons, fake_team_season
):
    test_app = create_app()
    with test_app.app_context():
        # Arrange
        team_seasons = [
            TeamSeason(team_name="A", season_year=1),
            TeamSeason(team_name="B", season_year=1),
            TeamSeason(team_name="A", season_year=2),
        ]
        fake_get_team_seasons.return_value = team_seasons

        # Act
        test_repo = TeamSeasonRepository()
        team_season = test_repo.get_team_season_by_team_and_season(team_name="C", season_year=3)

    # Assert
    fake_team_season.query.filter_by.assert_called_once_with(team_name="C", season_year=3)
    fake_team_season.query.filter_by.return_value.first.assert_called_once()
    assert team_season == fake_team_season.query.filter_by.return_value.first.return_value


@patch('app.data.repositories.team_season_repository.TeamSeason')
@patch('app.data.repositories.team_season_repository.TeamSeasonRepository.get_team_seasons')
def test_get_team_season_by_team_and_season_when_team_seasons_is_not_empty_and_team_season_is_found_should_return_team_season(fake_get_team_seasons, fake_team_season):
    test_app = create_app()
    with test_app.app_context():
        # Arrange
        team_seasons = [
            TeamSeason(team_name="A", season_year=1),
            TeamSeason(team_name="B", season_year=1),
            TeamSeason(team_name="A", season_year=2),
        ]
        fake_get_team_seasons.return_value = team_seasons

        # Act
        test_repo = TeamSeasonRepository()
        team_season = test_repo.get_team_season_by_team_and_season(team_name="A", season_year=1)

    # Assert
    fake_team_season.query.filter_by.assert_called_once_with(team_name="A", season_year=1)
    fake_team_season.query.filter_by.return_value.first.assert_called_once()
    assert team_season == fake_team_season.query.filter_by.return_value.first.return_value


@patch('app.data.repositories.team_season_repository.sqla')
def test_add_team_season_should_add_team_season(fake_sqla):
    # Arrange
    test_app = create_app()
    with test_app.app_context():
        # Act
        test_repo = TeamSeasonRepository()
        team_season_in = TeamSeason(team_name=3, season_year=3)
        team_season_out = test_repo.add_team_season(team_season_in)

    # Assert
    fake_sqla.session.add.assert_called_once_with(team_season_in)
    fake_sqla.session.commit.assert_called_once()
    assert team_season_out is team_season_in


@patch('app.data.repositories.team_season_repository.sqla')
def test_add_team_seasons_when_team_seasons_arg_is_empty_should_add_no_team_seasons(fake_sqla):
    # Arrange
    test_app = create_app()
    with test_app.app_context():
        # Act
        test_repo = TeamSeasonRepository()
        team_seasons_in = ()
        team_seasons_out = test_repo.add_team_seasons(team_seasons_in)

    # Assert
    fake_sqla.session.add.assert_not_called()
    fake_sqla.session.commit.assert_called_once()
    assert team_seasons_out is team_seasons_in


@patch('app.data.repositories.team_season_repository.sqla')
def test_add_team_seasons_when_team_seasons_arg_is_not_empty_should_add_team_seasons(fake_sqla):
    # Arrange
    test_app = create_app()
    with test_app.app_context():
        # Act
        test_repo = TeamSeasonRepository()
        team_seasons_in = (
            TeamSeason(team_name="C", season_year=4),
            TeamSeason(team_name="D", season_year=3),
            TeamSeason(team_name="D", season_year=4),
        )
        team_seasons_out = test_repo.add_team_seasons(team_seasons_in)

    # Assert
    fake_sqla.session.add.assert_has_calls([
        call(team_seasons_in[0]),
        call(team_seasons_in[1]),
        call(team_seasons_in[2]),
    ])
    fake_sqla.session.commit.assert_called_once()
    assert team_seasons_out is team_seasons_in


@patch('app.data.repositories.team_season_repository.sqla')
@patch('app.data.repositories.team_season_repository.exists')
def test_team_season_exists_should_query_database(fake_exists, fake_sqla):
    # Arrange
    test_app = create_app()
    with test_app.app_context():
        # Act
        test_repo = TeamSeasonRepository()
        team_season_exists = test_repo.team_season_exists(id=1)

    # Assert
    fake_exists.assert_called_once()
    fake_exists.return_value.where.assert_called_once()
    fake_sqla.session.query.assert_called_once_with(fake_exists.return_value.where.return_value)
    fake_sqla.session.query.return_value.scalar.assert_called_once()
    assert team_season_exists == fake_sqla.session.query.return_value.scalar.return_value


@patch('app.data.repositories.team_season_repository.TeamSeasonRepository.team_season_exists')
def test_update_team_season_when_team_season_does_not_exist_should_return_team_season(fake_team_season_exists):
    # Arrange
    fake_team_season_exists.return_value = False

    test_app = create_app()
    with test_app.app_context():
        # Act
        test_repo = TeamSeasonRepository()
        team_season_to_update = TeamSeason(
            team_name="Z",
            season_year=99,
            league_name="Z",
            conference_name="Z",
            division_name="Z",
            games=99,
            wins=33,
            losses=33,
            ties=33,
            winning_percentage=0.5,
            points_for=660,
            points_against=660,
            expected_wins=49.5,
            expected_losses=49.5,
            offensive_average=20.00,
            offensive_factor=1.000,
            offensive_index=20.00,
            defensive_average=20.00,
            defensive_factor=1.000,
            defensive_index=20.00,
            final_expected_winning_percentage=0.500
        )
        team_season_updated = test_repo.update_team_season(team_season_to_update)

    # Assert
    fake_team_season_exists.assert_called_once_with(team_season_to_update.id)
    assert team_season_updated is team_season_to_update


@patch('app.data.repositories.team_season_repository.sqla')
@patch('app.data.repositories.team_season_repository.TeamSeasonRepository.get_team_season')
@patch('app.data.repositories.team_season_repository.TeamSeasonRepository.team_season_exists')
def test_update_team_season_when_team_season_exists_should_update_and_return_team_season(
        fake_team_season_exists, fake_get_team_season, fake_sqla
):
    # Arrange
    test_app = create_app()
    with test_app.app_context():
        fake_team_season_exists.return_value = True
        old_team_season = TeamSeason(
            team_name="A",
            season_year=1,
            league_name="A",
            conference_name="A",
            division_name="A",
            games=3,
            wins=1,
            losses=1,
            ties=1,
            winning_percentage=0.5,
            points_for=75,
            points_against=75,
            expected_wins=1.5,
            expected_losses=1.5,
            offensive_average=25.00,
            offensive_factor=2.000,
            offensive_index=25.00,
            defensive_average=25.00,
            defensive_factor=0.500,
            defensive_index=25.00,
            final_expected_winning_percentage=0.750
        )
        fake_get_team_season.return_value = old_team_season

        new_team_season = TeamSeason(
            team_name="Z",
            season_year=99,
            league_name="Z",
            conference_name="Z",
            division_name="Z",
            games=99,
            wins=33,
            losses=33,
            ties=33,
            winning_percentage=0.5,
            points_for=660,
            points_against=660,
            expected_wins=49.5,
            expected_losses=49.5,
            offensive_average=20.00,
            offensive_factor=1.000,
            offensive_index=20.00,
            defensive_average=20.00,
            defensive_factor=1.000,
            defensive_index=20.00,
            final_expected_winning_percentage=0.500
        )

        # Act
        test_repo = TeamSeasonRepository()
        team_season_updated = test_repo.update_team_season(new_team_season)

    # Assert
    fake_team_season_exists.assert_called_once_with(old_team_season.id)
    fake_get_team_season.assert_called_once_with(old_team_season.id)
    assert team_season_updated.team_name == new_team_season.team_name
    assert team_season_updated.season_year == new_team_season.season_year
    fake_sqla.session.add.assert_called_once_with(old_team_season)
    fake_sqla.session.commit.assert_called_once()
    assert team_season_updated is new_team_season


@patch('app.data.repositories.team_season_repository.TeamSeasonRepository.team_season_exists')
def test_delete_team_season_when_team_season_does_not_exist_should_return_none(fake_team_season_exists):
    # Arrange
    fake_team_season_exists.return_value = False
    id = 1

    test_app = create_app()
    with test_app.app_context():
        # Act
        test_repo = TeamSeasonRepository()
        team_season_deleted = test_repo.delete_team_season(id)

    # Assert
    fake_team_season_exists.assert_called_once_with(id)
    assert team_season_deleted is None


@patch('app.data.repositories.team_season_repository.sqla')
@patch('app.data.repositories.team_season_repository.TeamSeasonRepository.get_team_season')
@patch('app.data.repositories.team_season_repository.TeamSeasonRepository.team_season_exists')
def test_delete_team_season_when_team_season_exists_should_return_team_season(fake_team_season_exists, fake_get_team_season, fake_sqla):
    # Arrange
    fake_team_season_exists.return_value = True
    id = 1

    test_app = create_app()
    with test_app.app_context():
        # Act
        test_repo = TeamSeasonRepository()
        team_season_deleted = test_repo.delete_team_season(id)

    # Assert
    fake_team_season_exists.assert_called_once_with(id)
    fake_get_team_season.assert_called_once_with(id)
    fake_sqla.session.delete.assert_called_once_with(fake_get_team_season.return_value)
    fake_sqla.session.commit.assert_called_once()
    return team_season_deleted is fake_get_team_season.return_value
