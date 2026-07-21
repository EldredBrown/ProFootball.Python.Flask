from unittest.mock import patch, MagicMock

import pytest
from flask import session

import app.flask.season_standings_controller as mod
from app.data.models.season import Season
from app.data.repositories.season_repository import SeasonRepository
from app.data.repositories.season_standings_repository import SeasonStandingsRepository

from test_app import create_app


@pytest.fixture()
def test_app():
    return create_app()


@patch('app.flask.season_standings_controller.render_template')
@patch('app.flask.season_standings_controller.injector')
def test_index_should_render_season_standings_index_template(fake_injector, fake_render_template, test_app):
    with test_app.test_request_context(
            '/season_standings/',
            method='GET'
    ):
        # Arrange
        fake_season_repository = MagicMock(SeasonRepository)
        seasons = (
            Season(year=1920),
            Season(year=1921),
            Season(year=1922),
        )
        fake_season_repository.get_seasons.return_value = seasons
        fake_injector.get.return_value = fake_season_repository

        session['seasons'] = []

        # Act
        result = mod.index()

        # Assert
        fake_injector.get.assert_called_once_with(SeasonRepository)
        fake_season_repository.get_seasons.assert_called_once()
        assert session.get('seasons') == [s.to_dict() for s in seasons]
        fake_render_template.assert_called_once_with(
            'season_standings/index.html',
            seasons=fake_season_repository.get_seasons.return_value, selected_season_year=-1, season_standings=[]
        )
        assert result is fake_render_template.return_value


@pytest.mark.skip('WIP')
@patch('app.flask.season_standings_controller.render_template')
@patch('app.flask.season_standings_controller.injector')
def test_select_season_should_render_season_standings_index_template_for_selected_year(
        fake_injector, fake_render_template, test_app
):
    with test_app.test_request_context(
            '/season_standings/select_season',
            method='POST'
    ):
        # Arrange
        fake_season_standings_repository = MagicMock(SeasonStandingsRepository)
        fake_injector.get.return_value = fake_season_standings_repository

        selected_year = 0
        fake_request.form.get.return_value = str(selected_year)

        # Act
        result = mod.select_season(fake_season_standings_repository)

        # Assert
        fake_request.form.get.assert_called_once_with('season_dropdown')

        fake_injector.get.assert_called_once_with(SeasonStandingsRepository)
        fake_season_standings_repository.get_season_standings_by_season_year.assert_called_once_with(season_year=selected_year)
        fake_render_template.assert_called_once_with(
            'season_standings/index.html',
            seasons=session.get('seasons'), selected_year=selected_year,
            season_standings=fake_season_standings_repository.get_season_standings_by_season_year.return_value
        )
        assert result is fake_render_template.return_value
