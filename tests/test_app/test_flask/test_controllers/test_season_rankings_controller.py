from unittest.mock import patch, MagicMock, call

import pytest
from flask import session

import app.flask.season_rankings_controller as mod
from app.data.models.league import League
from app.data.models.season import Season
from app.data.repositories.league_repository import LeagueRepository
from app.data.repositories.season_rankings_repository import SeasonRankingsRepository
from app.data.repositories.season_repository import SeasonRepository

from test_app import create_app


@pytest.fixture()
def test_app():
    return create_app()


@patch('app.flask.season_rankings_controller.render_template')
@patch('app.flask.season_rankings_controller.injector')
def test_index_when_no_values_in_session_should_set_session_variables_and_render_team_season_index_template(
        fake_injector, fake_render_template, test_app
):
    with test_app.test_request_context(
            '/season_rankings/',
            method='GET'
    ):
        # Arrange
        fake_season_repository = MagicMock(SeasonRepository)
        seasons = []
        fake_season_repository.get_seasons.return_value = seasons

        fake_league_repository = MagicMock(LeagueRepository)
        leagues = []
        fake_league_repository.get_leagues.return_value = leagues

        fake_injector.get.side_effect = [
            fake_season_repository, fake_league_repository,
        ]

        # Act
        result = mod.index()

        # Assert
        fake_injector.get.assert_has_calls([
            call(SeasonRepository),
            call(LeagueRepository),
        ])

        fake_season_repository.get_seasons.assert_called_once()
        seasons_dict = [s.to_dict() for s in fake_season_repository.get_seasons.return_value]
        assert session.get('seasons') == seasons_dict

        selected_season_year = -1
        assert session.get('selected_season_year') == selected_season_year

        fake_league_repository.get_leagues.assert_called_once()
        assert session.get('leagues') == leagues

        selected_league_name = ''
        assert session.get('selected_league_name') == selected_league_name

        fake_render_template.assert_called_with(
            'season_rankings/index.html',
            seasons=seasons, selected_season_year=selected_season_year,
            leagues=session.get('leagues'), selected_league_name=selected_league_name,
            types=mod.RANKING_TYPES, selected_type=None, season_rankings=None
        )
        assert result is fake_render_template.return_value


@patch('app.flask.season_rankings_controller.render_template')
@patch('app.flask.season_rankings_controller.injector')
def test_index_when_seasons_are_in_session_should_set_seasons_session_variable_and_render_team_season_index_template(
        fake_injector, fake_render_template, test_app
):
    with test_app.test_request_context(
            '/season_rankings/',
            method='GET'
    ):
        # Arrange
        fake_league_repository = MagicMock(LeagueRepository)
        leagues = []
        fake_league_repository.get_leagues.return_value = leagues
        fake_injector.get.return_value = fake_league_repository

        seasons = (
            Season(id=1920),
            Season(id=1921),
            Season(id=1922),
        )
        session['seasons'] = [s.to_dict() for s in seasons]

        # Act
        result = mod.index()

        # Assert
        fake_injector.get.assert_called_once_with(LeagueRepository)

        selected_season_year = -1
        assert session.get('selected_season_year') == selected_season_year

        fake_league_repository.get_leagues.assert_called_once()
        assert session.get('leagues') == leagues

        selected_league_name = ''
        assert session.get('selected_league_name') == selected_league_name

        fake_render_template.assert_called_with(
            'season_rankings/index.html',
            seasons=session.get('seasons'), selected_season_year=selected_season_year,
            leagues=leagues, selected_league_name=selected_league_name,
            types=mod.RANKING_TYPES, selected_type=None, season_rankings=None
        )
        assert result is fake_render_template.return_value


@patch('app.flask.season_rankings_controller.render_template')
@patch('app.flask.season_rankings_controller.injector')
def test_index_when_selected_season_id_is_in_session_should_set_selected_season_id_session_variable_and_render_team_season_index_template(
        fake_injector, fake_render_template, test_app
):
    with test_app.test_request_context(
            '/season_rankings/',
            method='GET'
    ):
        # Arrange
        fake_league_repository = MagicMock(LeagueRepository)
        leagues = []
        fake_league_repository.get_leagues.return_value = leagues
        fake_injector.get.return_value = fake_league_repository

        seasons = (
            Season(id=1920),
            Season(id=1921),
            Season(id=1922),
        )
        session['seasons'] = [s.to_dict() for s in seasons]

        selected_season_year = 1920
        session['selected_season_year'] = selected_season_year

        # Act
        result = mod.index()

        # Assert
        fake_injector.get.assert_called_once_with(LeagueRepository)

        fake_league_repository.get_leagues.assert_called_once()
        assert session.get('leagues') == leagues

        selected_league_name = ''
        assert session.get('selected_league_name') == selected_league_name

        fake_render_template.assert_called_with(
            'season_rankings/index.html',
            seasons=session.get('seasons'), selected_season_year=selected_season_year,
            leagues=leagues, selected_league_name=selected_league_name,
            types=mod.RANKING_TYPES, selected_type=None, season_rankings=None
        )
        assert result is fake_render_template.return_value


@patch('app.flask.season_rankings_controller.render_template')
@patch('app.flask.season_rankings_controller.injector')
def test_index_when_leagues_collection_has_leagues_and_not_all_leagues_are_active_in_selected_season_id_should_set_leagues_session_variable_and_render_team_season_index_template(
        fake_injector, fake_render_template, test_app
):
    with test_app.test_request_context(
            '/season_rankings/',
            method='GET'
    ):
        # Arrange
        fake_league_repository = MagicMock(LeagueRepository)
        leagues = (
            League(id=1, short_name='L1', long_name='League 1', first_season_id=1920, last_season_id=1921),
            League(id=2, short_name='L2', long_name='League 2', first_season_id=1921, last_season_id=1923),
            League(id=3, short_name='L3', long_name='League 3', first_season_id=1923, last_season_id=1924),
        )
        fake_league_repository.get_leagues.return_value = leagues
        fake_injector.get.return_value = fake_league_repository

        seasons = (
            Season(id=1920),
            Season(id=1921),
            Season(id=1922),
        )
        session['seasons'] = [s.to_dict() for s in seasons]

        selected_season_year = 1922
        session['selected_season_year'] = selected_season_year

        # Act
        result = mod.index()

        # Assert
        fake_injector.get.assert_called_once_with(LeagueRepository)

        fake_league_repository.get_leagues.assert_called_once()
        assert session.get('leagues') == [leagues[1].to_dict()]

        selected_league_name = ''
        assert session.get('selected_league_name') == selected_league_name

        fake_render_template.assert_called_with(
            'season_rankings/index.html',
            seasons=session.get('seasons'), selected_season_year=selected_season_year,
            leagues=session.get('leagues'), selected_league_name=selected_league_name,
            types=mod.RANKING_TYPES, selected_type=None, season_rankings=None
        )
        assert result is fake_render_template.return_value


@patch('app.flask.season_rankings_controller.render_template')
@patch('app.flask.season_rankings_controller.injector')
def test_index_when_selected_league_name_is_not_empty_should_set_selected_league_name_session_variable_and_render_team_season_index_template(
        fake_injector, fake_render_template, test_app
):
    with test_app.test_request_context(
            '/season_rankings/',
            method='GET'
    ):
        # Arrange
        fake_league_repository = MagicMock(LeagueRepository)
        leagues = (
            League(id=1, short_name='L1', long_name='League 1', first_season_id=1920, last_season_id=1921),
            League(id=2, short_name='L2', long_name='League 2', first_season_id=1921, last_season_id=1923),
            League(id=3, short_name='L3', long_name='League 3', first_season_id=1923, last_season_id=1924),
        )
        fake_league_repository.get_leagues.return_value = leagues
        fake_injector.get.return_value = fake_league_repository

        seasons = (
            Season(id=1920),
            Season(id=1921),
            Season(id=1922),
        )
        session['seasons'] = [s.to_dict() for s in seasons]

        selected_season_year = 1922
        session['selected_season_year'] = selected_season_year

        selected_league_name = 'L'
        session['selected_league_name'] = selected_league_name

        # Act
        result = mod.index()

        # Assert
        fake_injector.get.assert_called_once_with(LeagueRepository)

        fake_league_repository.get_leagues.assert_called_once()
        assert session.get('leagues') == [leagues[1].to_dict()]

        fake_render_template.assert_called_with(
            'season_rankings/index.html',
            seasons=session.get('seasons'), selected_season_year=selected_season_year,
            leagues=session.get('leagues'), selected_league_name=selected_league_name,
            types=mod.RANKING_TYPES, selected_type=None, season_rankings=None
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
def test_offense_should_render_season_offensive_rankings_template(
        fake_injector, fake_render_template, test_app
):
    with test_app.test_request_context(
            '/season_rankings/',
            method='GET'
    ):
        # Arrange
        fake_season_rankings_repository = MagicMock(SeasonRankingsRepository)
        fake_injector.get.return_value = fake_season_rankings_repository

        seasons = (
            Season(id=1),
            Season(id=2),
            Season(id=3),
        )
        session['seasons'] = [s.to_dict() for s in seasons]

        selected_season_year = 1920
        session['selected_season_year'] = selected_season_year

        leagues = (
            League(long_name="American Professional Football Association", short_name="APFA", first_season_id=1920),
            League(long_name="National Football League", short_name="NFL", first_season_id=1920),
            League(long_name="American Football League", short_name="AFL", first_season_id=1920),
        )
        session['leagues'] = [l.to_dict() for l in leagues]
        session['selected_league_name'] = "APFA"

        session['selected_type'] = "Offense"

        # Act
        result = mod.offense()

        # Assert
        fake_injector.get.assert_called_once_with(SeasonRankingsRepository)
        assert session.get('selected_season_year') == selected_season_year
        fake_season_rankings_repository.get_offensive_rankings_by_season.assert_called_once_with(
            season_id=selected_season_year
        )
        fake_render_template.assert_called_once_with(
            'season_rankings/offense.html',
            seasons=session.get('seasons'), selected_season_year=selected_season_year,
            leagues=session.get('leagues'), selected_league_name=session.get('selected_league_name'),
            types=mod.RANKING_TYPES, selected_type=session.get('selected_type'),
            season_rankings=fake_season_rankings_repository.get_offensive_rankings_by_season.return_value
        )
        assert result is fake_render_template.return_value


@patch('app.flask.season_rankings_controller.render_template')
@patch('app.flask.season_rankings_controller.injector')
def test_defense_should_render_season_defensive_rankings_template(
        fake_injector, fake_render_template, test_app
):
    with test_app.test_request_context(
            '/season_rankings/',
            method='GET'
    ):
        # Arrange
        fake_season_rankings_repository = MagicMock(SeasonRankingsRepository)
        fake_injector.get.return_value = fake_season_rankings_repository

        seasons = (
            Season(id=1),
            Season(id=2),
            Season(id=3),
        )
        session['seasons'] = [s.to_dict() for s in seasons]

        selected_season_year = 1920
        session['selected_season_year'] = selected_season_year

        leagues = (
            League(long_name="American Professional Football Association", short_name="APFA", first_season_id=1920),
            League(long_name="National Football League", short_name="NFL", first_season_id=1920),
            League(long_name="American Football League", short_name="AFL", first_season_id=1920),
        )
        session['leagues'] = [l.to_dict() for l in leagues]
        session['selected_league_name'] = "APFA"

        session['selected_type'] = "Defense"

        # Act
        result = mod.defense()

        # Assert
        fake_injector.get.assert_called_once_with(SeasonRankingsRepository)
        assert session.get('selected_season_year') == selected_season_year
        fake_season_rankings_repository.get_defensive_rankings_by_season.assert_called_once_with(
            season_id=selected_season_year
        )
        fake_render_template.assert_called_once_with(
            'season_rankings/defense.html',
            seasons=session.get('seasons'), selected_season_year=selected_season_year,
            leagues=session.get('leagues'), selected_league_name=session.get('selected_league_name'),
            types=mod.RANKING_TYPES, selected_type=session.get('selected_type'),
            season_rankings=fake_season_rankings_repository.get_defensive_rankings_by_season.return_value
        )
        assert result is fake_render_template.return_value


@patch('app.flask.season_rankings_controller.render_template')
@patch('app.flask.season_rankings_controller.injector')
def test_total_should_render_season_total_rankings_template(
        fake_injector, fake_render_template, test_app
):
    with test_app.test_request_context(
            '/season_rankings/',
            method='GET'
    ):
        # Arrange
        fake_season_rankings_repository = MagicMock(SeasonRankingsRepository)
        fake_injector.get.return_value = fake_season_rankings_repository

        seasons = (
            Season(id=1),
            Season(id=2),
            Season(id=3),
        )
        session['seasons'] = [s.to_dict() for s in seasons]

        selected_season_year = 1920
        session['selected_season_year'] = selected_season_year

        leagues = (
            League(long_name="American Professional Football Association", short_name="APFA", first_season_id=1920),
            League(long_name="National Football League", short_name="NFL", first_season_id=1920),
            League(long_name="American Football League", short_name="AFL", first_season_id=1920),
        )
        session['leagues'] = [l.to_dict() for l in leagues]
        session['selected_league_name'] = "APFA"

        session['selected_type'] = "Total"

        # Act
        result = mod.total()

        # Assert
        fake_injector.get.assert_called_once_with(SeasonRankingsRepository)
        assert session.get('selected_season_year') == selected_season_year
        fake_season_rankings_repository.get_total_rankings_by_season.assert_called_once_with(
            season_id=selected_season_year
        )
        fake_render_template.assert_called_once_with(
            'season_rankings/total.html',
            seasons=session.get('seasons'), selected_season_year=selected_season_year,
            leagues=session.get('leagues'), selected_league_name=session.get('selected_league_name'),
            types=mod.RANKING_TYPES, selected_type=session.get('selected_type'),
            season_rankings=fake_season_rankings_repository.get_total_rankings_by_season.return_value
        )
        assert result is fake_render_template.return_value
