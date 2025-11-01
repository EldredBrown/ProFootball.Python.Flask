from unittest.mock import patch

import pytest

import app.flask.season_standings_controller as mod

from test_app import create_app


@pytest.fixture()
def test_app():
    return create_app()


@patch('app.flask.season_standings_controller.render_template')
@patch('app.flask.season_standings_controller.SeasonRepository')
def test_index_should_render_season_standings_index_template(
        fake_season_repository, fake_render_template
):
    # Act
    result = mod.index()

    # Assert
    fake_season_repository.assert_called_once()
    fake_season_repository.return_value.get_seasons.assert_called_once()
    fake_render_template.assert_called_once_with(
        'season_standings/index.html',
        seasons=fake_season_repository.return_value.get_seasons.return_value, selected_year=None, season_standings=[]
    )
    assert result is fake_render_template.return_value


@pytest.mark.skip('WIP')
@patch('app.flask.season_standings_controller.render_template')
@patch('app.flask.season_standings_controller.season_repository')
@patch('app.flask.season_standings_controller.season_standings_repository')
def test_select_season_should_render_season_standings_index_template_for_selected_year(
        fake_season_standings_repository, fake_season_repository, fake_render_template, test_app
):
    with test_app.test_request_context(
            '/season_standings/select_season',
            method='POST'
    ):
        # Arrange
        selected_year = 0

        # Act
        result = mod.select_season()

    # Assert
    # fake_request.form.get.assert_called_once_with('season_dropdown')
    fake_season_standings_repository.get_season_standings_by_season_year.assert_called_once_with(season_year=selected_year)
    fake_render_template.assert_called_once_with(
        'season_standings/index.html',
        seasons=fake_season_repository.get_seasons.return_value, selected_year=selected_year,
        season_standings=fake_season_standings_repository.get_team_seasons_by_season_year.return_value
    )
    assert result is fake_render_template.return_value
