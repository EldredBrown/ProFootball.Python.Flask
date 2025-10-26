from unittest.mock import patch

import pytest

import app.flask.rankings_controller as rankings_controller

from test_app import create_app


@pytest.fixture()
def test_app():
    return create_app()


@patch('app.flask.rankings_controller.render_template')
@patch('app.flask.rankings_controller.season_repository')
def test_index_should_render_offensive_rankings_index_template(
        fake_season_repository, fake_render_template, test_app
):
    # Act
    with test_app.app_context():
        result = rankings_controller.index()

    # Assert
    fake_season_repository.get_seasons.assert_called_once()
    fake_render_template.assert_called_once_with(
        'rankings/index.html',
        seasons=fake_season_repository.get_seasons.return_value, selected_year=None, rankings=[]
    )
    assert result is fake_render_template.return_value


@pytest.mark.skip('WIP')
@patch('app.flask.rankings_controller.render_template')
@patch('app.flask.rankings_controller.season_repository')
@patch('app.flask.rankings_controller.rankings_repository')
def test_select_season_should_render_rankings_index_template_for_selected_year(
        fake_rankings_repository, fake_season_repository, fake_render_template, test_app
):
    with test_app.app_context():
        with test_app.test_request_context(
                '/rankings/select_season',
                method='POST'
        ):
            # Arrange
            selected_year = 0

            # Act
            result = rankings_controller.select_season()

    # Assert
    # fake_request.form.get.assert_called_once_with('season_dropdown')
    fake_rankings_repository.get_rankings_by_season_year.assert_called_once_with(season_year=selected_year)
    fake_render_template.assert_called_once_with(
        'rankings/index.html',
        seasons=fake_season_repository.get_seasons.return_value, selected_year=selected_year,
        rankings=fake_rankings_repository.get_team_seasons_by_season_year.return_value
    )
    assert result is fake_render_template.return_value
