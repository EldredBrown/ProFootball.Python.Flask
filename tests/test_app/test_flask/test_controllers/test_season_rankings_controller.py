from unittest.mock import patch

import pytest

import app.flask.season_rankings_controller as mut
from app.data.models.league import League
from app.data.models.season import Season

from test_app import create_app


@pytest.fixture()
def test_app():
    return create_app()


@patch('app.flask.season_rankings_controller.render_template')
@patch('app.flask.season_rankings_controller.LeagueRepository')
@patch('app.flask.season_rankings_controller.SeasonRepository')
def test_index_should_render_season_rankings_index_template(
        fake_season_repository, fake_league_repository, fake_render_template, test_app
):
    # Act
    with test_app.app_context():
        result = mut.index()

    # Assert
    fake_season_repository.assert_called_once()
    fake_season_repository.return_value.get_seasons.assert_called_once()
    fake_league_repository.assert_called_once()
    fake_league_repository.return_value.get_leagues.assert_called_once()
    fake_render_template.assert_called_once_with(
        'season_rankings/index.html',
        seasons=fake_season_repository.return_value.get_seasons.return_value, selected_year=None,
        leagues=fake_league_repository.return_value.get_leagues.return_value, selected_league_name=None,
        types=mut.RANKING_TYPES, selected_type=None, season_rankings=None
    )
    assert result is fake_render_template.return_value


@pytest.mark.skip('WIP')
def test_select_season_should_render_season_rankings_index_template_for_selected_year(test_app):
    with test_app.app_context():
        with test_app.test_request_context(
                '/season_rankings/select_season',
                method='POST'
        ):
            # Arrange

            # Act
            result = mut.select_season()

    # Assert


@pytest.mark.skip('WIP')
def test_select_league_should_render_rankings_index_template_for_selected_league(test_app):
    with test_app.app_context():
        with test_app.test_request_context(
                '/season_rankings/select_league',
                method='POST'
        ):
            # Arrange

            # Act
            result = mut.select_league()

    # Assert


@pytest.mark.skip('WIP')
def test_select_type_should_render_rankings_index_template_for_selected_type(test_app):
    with test_app.app_context():
        with test_app.test_request_context(
                '/season_rankings/select_type',
                method='POST'
        ):
            # Arrange

            # Act
            result = mut.select_type()

    # Assert


@patch('app.flask.season_rankings_controller.render_template')
@patch('app.flask.season_rankings_controller.flash')
@patch('app.flask.season_rankings_controller.WeeklyUpdateService')
def test_run_weekly_update_should_run_weekly_update(
        fake_weekly_update_service, fake_flash, fake_render_template, test_app
):
    with test_app.app_context():
        # Arrange
        mut.seasons = [
            Season(year=1),
            Season(year=2),
            Season(year=3),
        ]
        mut.selected_year = 1

        mut.leagues = [
            League(long_name="American Professional Football Association", short_name="APFA", first_season_year=1),
            League(long_name="National Football League", short_name="NFL", first_season_year=1),
            League(long_name="American Football League", short_name="AFL", first_season_year=1),
        ]
        mut.selected_league_name = "APFA"

        mut.selected_type = "Total"

        # Act
        mut.run_weekly_update()

    # Assert
    league_name = mut.selected_league_name
    season_year = mut.selected_year
    fake_weekly_update_service.assert_called_once()
    fake_weekly_update_service.return_value.run_weekly_update.assert_called_once_with(league_name, season_year)
    fake_flash.assert_called_once_with(
        f"The weekly update has been successfully completed for the '{league_name}' in {season_year}.",
        'success'
    )
    fake_render_template.assert_called_once_with(
        'season_rankings/index.html',
        seasons=mut.seasons, selected_year=mut.selected_year,
        leagues=mut.leagues, selected_league_name=mut.selected_league_name,
        types=mut.RANKING_TYPES, selected_type=mut.selected_type, season_rankings=None
    )


@patch('app.flask.season_rankings_controller.render_template')
@patch('app.flask.season_rankings_controller.season_rankings_repository')
def test_offense_should_render_season_offensive_rankings_template(
        fake_season_rankings_repository, fake_render_template, test_app
):
    # Arrange
    mut.seasons = [
        Season(year=1),
        Season(year=2),
        Season(year=3),
    ]
    mut.selected_year = 1

    mut.leagues = [
        League(long_name="American Professional Football Association", short_name="APFA", first_season_year=1),
        League(long_name="National Football League", short_name="NFL", first_season_year=1),
        League(long_name="American Football League", short_name="AFL", first_season_year=1),
    ]
    mut.selected_league_name = "APFA"

    mut.selected_type = "Offense"

    # Act
    with test_app.app_context():
        result = mut.offense()

    # Assert
    fake_season_rankings_repository.get_offensive_rankings_by_season_year.assert_called_once_with(mut.selected_year)
    fake_render_template.assert_called_once_with(
        'season_rankings/offense.html',
        seasons=mut.seasons, selected_year=mut.selected_year,
        leagues=mut.leagues, selected_league_name=mut.selected_league_name,
        types=mut.RANKING_TYPES, selected_type=mut.selected_type,
        season_rankings=fake_season_rankings_repository.get_offensive_rankings_by_season_year.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.season_rankings_controller.render_template')
@patch('app.flask.season_rankings_controller.season_rankings_repository')
def test_defense_should_render_season_offensive_rankings_template(
        fake_season_rankings_repository, fake_render_template, test_app
):
    # Arrange
    mut.seasons = [
        Season(year=1),
        Season(year=2),
        Season(year=3),
    ]
    mut.selected_year = 1

    mut.leagues = [
        League(long_name="American Professional Football Association", short_name="APFA", first_season_year=1),
        League(long_name="National Football League", short_name="NFL", first_season_year=1),
        League(long_name="American Football League", short_name="AFL", first_season_year=1),
    ]
    mut.selected_league_name = "APFA"

    mut.selected_type = "Defense"

    # Act
    with test_app.app_context():
        result = mut.defense()

    # Assert
    fake_season_rankings_repository.get_defensive_rankings_by_season_year.assert_called_once_with(mut.selected_year)
    fake_render_template.assert_called_once_with(
        'season_rankings/defense.html',
        seasons=mut.seasons, selected_year=mut.selected_year,
        leagues=mut.leagues, selected_league_name=mut.selected_league_name,
        types=mut.RANKING_TYPES, selected_type=mut.selected_type,
        season_rankings=fake_season_rankings_repository.get_defensive_rankings_by_season_year.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.season_rankings_controller.render_template')
@patch('app.flask.season_rankings_controller.season_rankings_repository')
def test_total_should_render_season_offensive_rankings_template(
        fake_season_rankings_repository, fake_render_template, test_app
):
    # Arrange
    mut.seasons = [
        Season(year=1),
        Season(year=2),
        Season(year=3),
    ]
    mut.selected_year = 1

    mut.leagues = [
        League(long_name="American Professional Football Association", short_name="APFA", first_season_year=1),
        League(long_name="National Football League", short_name="NFL", first_season_year=1),
        League(long_name="American Football League", short_name="AFL", first_season_year=1),
    ]
    mut.selected_league_name = "APFA"

    mut.selected_type = "Offense"

    # Act
    with test_app.app_context():
        result = mut.total()

    # Assert
    fake_season_rankings_repository.get_total_rankings_by_season_year.assert_called_once_with(mut.selected_year)
    fake_render_template.assert_called_once_with(
        'season_rankings/total.html',
        seasons=mut.seasons, selected_year=mut.selected_year,
        leagues=mut.leagues, selected_league_name=mut.selected_league_name,
        types=mut.RANKING_TYPES, selected_type=mut.selected_type,
        season_rankings=fake_season_rankings_repository.get_total_rankings_by_season_year.return_value
    )
    assert result is fake_render_template.return_value
