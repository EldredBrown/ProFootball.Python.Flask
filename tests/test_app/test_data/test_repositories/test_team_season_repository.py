from unittest.mock import patch, call

import pytest

from sqlalchemy.exc import IntegrityError

from app import sqla
from instance.test_db import db_init
from test_app import create_app

from app.data.models.season import Season
from app.data.models.game import Game
from app.data.models.league_season import LeagueSeason
from app.data.models.team_season import TeamSeason
from app.data.repositories.team_season_repository import TeamSeasonRepository


@pytest.fixture
def test_app():
    return create_app()


@patch('app.data.repositories.team_season_repository.TeamSeason')
def test_get_team_seasons_should_get_team_seasons(fake_team_season, test_app):
    with test_app.app_context():
        # Arrange
        team_seasons_in = [
            TeamSeason(
                team_name="Chicago Cardinals",
                season_year=1920,
                league_name="APFA"
            ),
            TeamSeason(
                team_name="Decatur Staleys",
                season_year=1920,
                league_name="APFA"
            ),
            TeamSeason(
                team_name="Akron Pros",
                season_year=1920,
                league_name="APFA"
            ),
        ]
        fake_team_season.query.all.return_value = team_seasons_in

        # Act
        test_repo = TeamSeasonRepository()
        team_seasons_out = test_repo.get_team_seasons()

    # Assert
    assert team_seasons_out == team_seasons_in


@patch('app.data.repositories.team_season_repository.TeamSeason')
def test_get_team_seasons_by_season_year_when_season_year_is_none_should_get_empty_list(
        fake_team_season, test_app
):
    with test_app.app_context():
        # Arrange
        team_seasons_in = [
            TeamSeason(
                team_name="Chicago Cardinals",
                season_year=1920,
                league_name="APFA"
            ),
            TeamSeason(
                team_name="Decatur Staleys",
                season_year=1920,
                league_name="APFA"
            ),
            TeamSeason(
                team_name="Akron Pros",
                season_year=1920,
                league_name="APFA"
            ),
            TeamSeason(
                team_name="Chicago Cardinals",
                season_year=1921,
                league_name="APFA"
            ),
            TeamSeason(
                team_name="Decatur Staleys",
                season_year=1921,
                league_name="APFA"
            ),
            TeamSeason(
                team_name="Akron Pros",
                season_year=1921,
                league_name="APFA"
            ),
            TeamSeason(
                team_name="Chicago Cardinals",
                season_year=1922,
                league_name="APFA"
            ),
            TeamSeason(
                team_name="Decatur Staleys",
                season_year=1922,
                league_name="APFA"
            ),
            TeamSeason(
                team_name="Akron Pros",
                season_year=1922,
                league_name="APFA"
            ),
        ]
        filter_year = 1921
        fake_team_season.query.filter_by.return_value.all.return_value = [
            x for x in team_seasons_in if x.season_year == filter_year
        ]

        # Act
        test_repo = TeamSeasonRepository()
        team_seasons_out = test_repo.get_team_seasons_by_season_year(season_year=None)

    # Assert
    assert team_seasons_out == []


@patch('app.data.repositories.team_season_repository.TeamSeason')
def test_get_team_seasons_by_season_year_when_season_year_is_not_none_should_get_team_seasons_for_the_specified_season_year(
        fake_team_season, test_app
):
    with test_app.app_context():
        # Arrange
        team_seasons_in = [
            TeamSeason(
                team_name="Chicago Cardinals",
                season_year=1920,
                league_name="APFA"
            ),
            TeamSeason(
                team_name="Decatur Staleys",
                season_year=1920,
                league_name="APFA"
            ),
            TeamSeason(
                team_name="Akron Pros",
                season_year=1920,
                league_name="APFA"
            ),
            TeamSeason(
                team_name="Chicago Cardinals",
                season_year=1921,
                league_name="APFA"
            ),
            TeamSeason(
                team_name="Decatur Staleys",
                season_year=1921,
                league_name="APFA"
            ),
            TeamSeason(
                team_name="Akron Pros",
                season_year=1921,
                league_name="APFA"
            ),
            TeamSeason(
                team_name="Chicago Cardinals",
                season_year=1922,
                league_name="APFA"
            ),
            TeamSeason(
                team_name="Decatur Staleys",
                season_year=1922,
                league_name="APFA"
            ),
            TeamSeason(
                team_name="Akron Pros",
                season_year=1922,
                league_name="APFA"
            ),
        ]
        filter_year = 1921
        fake_team_season.query.filter_by.return_value.all.return_value = [
            x for x in team_seasons_in if x.season_year == filter_year
        ]

        # Act
        test_repo = TeamSeasonRepository()
        team_seasons_out = test_repo.get_team_seasons_by_season_year(season_year=filter_year)

    # Assert
    for team_season in team_seasons_out:
        assert team_season.season_year == filter_year


@patch('app.data.repositories.team_season_repository.TeamSeason')
def test_get_team_season_when_team_seasons_is_empty_should_return_none(fake_team_season, test_app):
    with test_app.app_context():
        # Arrange
        team_seasons_in = []
        fake_team_season.query.all.return_value = team_seasons_in

        # Act
        test_repo = TeamSeasonRepository()
        team_season_out = test_repo.get_team_season(1)

    # Assert
    assert team_season_out is None


@patch('app.data.repositories.team_season_repository.TeamSeason')
def test_get_team_season_when_team_seasons_is_not_empty_and_team_season_is_not_found_should_return_none(fake_team_season, test_app):
    with test_app.app_context():
        # Arrange
        team_seasons_in = [
            TeamSeason(
                team_name="Chicago Cardinals",
                season_year=1920,
                league_name="APFA"
            ),
            TeamSeason(
                team_name="Decatur Staleys",
                season_year=1920,
                league_name="APFA"
            ),
            TeamSeason(
                team_name="Akron Pros",
                season_year=1920,
                league_name="APFA"
            ),
        ]
        fake_team_season.query.all.return_value = team_seasons_in
        fake_team_season.query.get.return_value = None

        # Act
        test_repo = TeamSeasonRepository()

        id = len(team_seasons_in) + 1
        team_season_out = test_repo.get_team_season(id)

    # Assert
    assert team_season_out is None


@patch('app.data.repositories.team_season_repository.TeamSeason')
def test_get_team_season_when_team_seasons_is_not_empty_and_team_season_is_found_should_return_team_season(fake_team_season, test_app):
    with test_app.app_context():
        # Arrange
        team_seasons_in = [
            TeamSeason(
                team_name="Chicago Cardinals",
                season_year=1920,
                league_name="APFA"
            ),
            TeamSeason(
                team_name="Decatur Staleys",
                season_year=1920,
                league_name="APFA"
            ),
            TeamSeason(
                team_name="Akron Pros",
                season_year=1920,
                league_name="APFA"
            ),
        ]
        fake_team_season.query.all.return_value = team_seasons_in

        id = len(team_seasons_in) - 1
        fake_team_season.query.get.return_value = team_seasons_in[id]

        # Act
        test_repo = TeamSeasonRepository()
        team_season_out = test_repo.get_team_season(id)

    # Assert
    assert team_season_out is team_seasons_in[id]
