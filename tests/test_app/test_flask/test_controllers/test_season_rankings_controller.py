from unittest.mock import patch, call, Mock

import pytest
from flask import session

import app.flask.season_rankings_controller as mod
from app.data.models.league import League
from app.data.models.season import Season
from app.data.repositories.league_repository import LeagueRepository
from app.data.repositories.season_rankings_repository import SeasonRankingsRepository
from app.data.repositories.season_repository import SeasonRepository
from app.services.weekly_update_service.weekly_update_service import WeeklyUpdateService

from test_app import create_app


@pytest.fixture()
def test_app():
    return create_app()


@patch('app.flask.season_rankings_controller.render_template')
@patch('app.flask.season_rankings_controller.injector')
def test_index_should_render_season_rankings_index_template(fake_injector, fake_render_template, test_app):
    with test_app.test_request_context(
            '/season_rankings/',
            method='GET'
    ):
        # Arrange
        fake_season_repository = Mock(SeasonRepository)
        seasons = [
            Season(year=1920),
            Season(year=1921),
            Season(year=1922),
        ]
        fake_season_repository.get_seasons.return_value = seasons
        fake_injector.get.return_value = fake_season_repository

        session['seasons'] = []
        selected_year = None
        leagues = []
        selected_league_name = None
        selected_type = None

        # Act
        result = mod.index()

        # Assert
        fake_injector.get.assert_called_once_with(SeasonRepository)
        fake_season_repository.get_seasons.assert_called_once()

        seasons = [s.to_dict() for s in seasons]
        assert session.get('seasons') == seasons

        fake_render_template.assert_called_once_with(
            'season_rankings/index.html',
            seasons=seasons, selected_year=selected_year,
            leagues=leagues, selected_league_name=selected_league_name,
            types=mod.RANKING_TYPES, selected_type=selected_type, season_rankings=None
        )
        assert result is fake_render_template.return_value


@pytest.mark.skip('WIP')
def test_select_season_should_render_season_rankings_index_template_for_selected_year(test_app):
    with test_app.test_request_context(
            '/season_rankings/select_season',
            method='POST'
    ):
        # Arrange

        # Act
        result = mod.select_season()

    # Assert


@pytest.mark.skip('WIP')
def test_select_league_should_render_rankings_index_template_for_selected_league(test_app):
    with test_app.test_request_context(
            '/season_rankings/select_league',
            method='POST'
    ):
        # Arrange

        # Act
        result = mod.select_league()

    # Assert


@pytest.mark.skip('WIP')
def test_select_type_should_render_rankings_index_template_for_selected_type(test_app):
    with test_app.test_request_context(
            '/season_rankings/select_type',
            method='POST'
    ):
        # Arrange

        # Act
        result = mod.select_type()

    # Assert


@patch('app.flask.season_rankings_controller.render_template')
@patch('app.flask.season_rankings_controller.injector')
def test_offense_should_render_season_offensive_rankings_template(fake_injector, fake_render_template, test_app):
    with test_app.test_request_context(
            '/season_rankings/',
            method='GET'
    ):
        # Arrange
        fake_season_rankings_repository = Mock(SeasonRankingsRepository)
        fake_injector.get.return_value = fake_season_rankings_repository

        seasons = [
            Season(year=1),
            Season(year=2),
            Season(year=3),
        ]
        session['seasons'] = [s.to_dict() for s in seasons]

        selected_year = 1
        session['selected_year'] = selected_year

        leagues = [
            League(long_name="American Professional Football Association", short_name="APFA", first_season_year=1),
            League(long_name="National Football League", short_name="NFL", first_season_year=1),
            League(long_name="American Football League", short_name="AFL", first_season_year=1),
        ]
        session['leagues'] = [l.to_dict() for l in leagues]
        session['selected_league_name'] = "APFA"

        session['selected_type'] = "Offense"

        # Act
        result = mod.offense()

        # Assert
        fake_injector.get.assert_called_once_with(SeasonRankingsRepository)
        assert session.get('selected_year') == selected_year
        fake_season_rankings_repository.get_offensive_rankings_by_season_year.assert_called_once_with(selected_year)
        fake_render_template.assert_called_once_with(
            'season_rankings/offense.html',
            seasons=session.get('seasons'), selected_year=selected_year,
            leagues=session.get('leagues'), selected_league_name=session.get('selected_league_name'),
            types=mod.RANKING_TYPES, selected_type=session.get('selected_type'),
            season_rankings=fake_season_rankings_repository.get_offensive_rankings_by_season_year.return_value
        )
        assert result is fake_render_template.return_value


@patch('app.flask.season_rankings_controller.render_template')
@patch('app.flask.season_rankings_controller.injector')
def test_defense_should_render_season_defensive_rankings_template(fake_injector, fake_render_template, test_app):
    with test_app.test_request_context(
            '/season_rankings/',
            method='GET'
    ):
        # Arrange
        fake_season_rankings_repository = Mock(SeasonRankingsRepository)
        fake_injector.get.return_value = fake_season_rankings_repository

        seasons = [
            Season(year=1),
            Season(year=2),
            Season(year=3),
        ]
        session['seasons'] = [s.to_dict() for s in seasons]

        selected_year = 1
        session['selected_year'] = selected_year

        leagues = [
            League(long_name="American Professional Football Association", short_name="APFA", first_season_year=1),
            League(long_name="National Football League", short_name="NFL", first_season_year=1),
            League(long_name="American Football League", short_name="AFL", first_season_year=1),
        ]
        session['leagues'] = [l.to_dict() for l in leagues]
        session['selected_league_name'] = "APFA"

        session['selected_type'] = "Defense"

        # Act
        result = mod.defense()

        # Assert
        fake_injector.get.assert_called_once_with(SeasonRankingsRepository)
        assert session.get('selected_year') == selected_year
        fake_season_rankings_repository.get_defensive_rankings_by_season_year.assert_called_once_with(selected_year)
        fake_render_template.assert_called_once_with(
            'season_rankings/defense.html',
            seasons=session.get('seasons'), selected_year=selected_year,
            leagues=session.get('leagues'), selected_league_name=session.get('selected_league_name'),
            types=mod.RANKING_TYPES, selected_type=session.get('selected_type'),
            season_rankings=fake_season_rankings_repository.get_defensive_rankings_by_season_year.return_value
        )
        assert result is fake_render_template.return_value


@patch('app.flask.season_rankings_controller.render_template')
@patch('app.flask.season_rankings_controller.injector')
def test_total_should_render_season_total_rankings_template(fake_injector, fake_render_template, test_app):
    with test_app.test_request_context(
            '/season_rankings/',
            method='GET'
    ):
        # Arrange
        fake_season_rankings_repository = Mock(SeasonRankingsRepository)
        fake_injector.get.return_value = fake_season_rankings_repository

        seasons = [
            Season(year=1),
            Season(year=2),
            Season(year=3),
        ]
        session['seasons'] = [s.to_dict() for s in seasons]

        selected_year = 1
        session['selected_year'] = selected_year

        leagues = [
            League(long_name="American Professional Football Association", short_name="APFA", first_season_year=1),
            League(long_name="National Football League", short_name="NFL", first_season_year=1),
            League(long_name="American Football League", short_name="AFL", first_season_year=1),
        ]
        session['leagues'] = [l.to_dict() for l in leagues]
        session['selected_league_name'] = "APFA"

        session['selected_type'] = "Total"

        # Act
        result = mod.total()

        # Assert
        fake_injector.get.assert_called_once_with(SeasonRankingsRepository)
        assert session.get('selected_year') == selected_year
        fake_season_rankings_repository.get_total_rankings_by_season_year.assert_called_once_with(selected_year)
        fake_render_template.assert_called_once_with(
            'season_rankings/total.html',
            seasons=session.get('seasons'), selected_year=selected_year,
            leagues=session.get('leagues'), selected_league_name=session.get('selected_league_name'),
            types=mod.RANKING_TYPES, selected_type=session.get('selected_type'),
            season_rankings=fake_season_rankings_repository.get_total_rankings_by_season_year.return_value
        )
        assert result is fake_render_template.return_value


@patch('app.flask.season_rankings_controller.render_template')
@patch('app.flask.season_rankings_controller.flash')
@patch('app.flask.season_rankings_controller.injector')
def test_run_weekly_update_should_run_weekly_update(fake_injector, fake_flash, fake_render_template, test_app):
    with test_app.test_request_context(
            '/season_rankings/',
            method='GET'
    ):
        # Arrange
        fake_weekly_update_service = Mock(WeeklyUpdateService)
        fake_injector.get.return_value = fake_weekly_update_service

        seasons = [
            Season(year=1),
            Season(year=2),
            Season(year=3),
        ]
        seasons = [s.to_dict() for s in seasons]
        session['seasons'] = seasons

        selected_year = 1
        session['selected_year'] = selected_year

        leagues = [
            League(long_name="American Professional Football Association", short_name="APFA", first_season_year=1),
            League(long_name="National Football League", short_name="NFL", first_season_year=1),
            League(long_name="American Football League", short_name="AFL", first_season_year=1),
        ]
        leagues = [l.to_dict() for l in leagues]
        session['leagues'] = leagues

        selected_league_name = "APFA"
        session['selected_league_name'] = selected_league_name

        selected_type = None
        session['selected_type'] = selected_type

        # Act
        mod.run_weekly_update()

        # Assert
        fake_injector.get.assert_called_once_with(WeeklyUpdateService)
        assert session.get('selected_league_name') == selected_league_name
        assert session.get('selected_year') == selected_year
        fake_weekly_update_service.run_weekly_update.assert_called_once_with(selected_league_name, selected_year)
        fake_flash.assert_called_once_with(
            f"The weekly update has been successfully completed for the '{selected_league_name}' in {selected_year}.",
            'success'
        )
        fake_render_template.assert_called_once_with(
            'season_rankings/index.html',
            seasons=seasons, selected_year=selected_year,
            leagues=leagues, selected_league_name=selected_league_name,
            types=mod.RANKING_TYPES, selected_type=selected_type, season_rankings=None
        )
