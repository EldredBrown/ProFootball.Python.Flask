from unittest.mock import patch, Mock

import flask
import pytest
from flask import request

from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound

import app.flask.team_season_controller as team_season_controller

from app.data.models.season import Season
from app.data.models.league_season import LeagueSeason
from app.data.models.team_season import TeamSeason

from test_app import create_app


@pytest.fixture()
def test_app():
    return create_app()


@patch('app.flask.team_season_controller.render_template')
@patch('app.flask.team_season_controller.team_season_repository')
@patch('app.flask.team_season_controller.season_repository')
def test_index_should_render_team_season_index_template(
        fake_season_repository, fake_team_season_repository, fake_render_template, test_app
):
    with test_app.app_context():
        # Act
        result = team_season_controller.index()

    # Assert
    fake_season_repository.get_seasons.assert_called_once()
    fake_render_template.assert_called_once_with(
        'team_seasons/index.html',
        seasons=fake_season_repository.get_seasons.return_value, selected_year=None, team_seasons=[]
    )
    assert result is fake_render_template.return_value


@patch('app.flask.team_season_controller.team_season_repository')
@patch('app.flask.team_season_controller.render_template')
def test_details_when_team_season_found_should_render_team_season_details_template(
        fake_render_template, fake_team_season_repository, test_app
):
    # Arrange
    id = 1

    # Act
    with test_app.app_context():
        result = team_season_controller.details(id)

    # Assert
    fake_team_season_repository.get_team_season.assert_called_once_with(id)
    fake_render_template.assert_called_once_with(
        'team_seasons/details.html', team_season=fake_team_season_repository.get_team_season.return_value
    )
    assert result == fake_render_template.return_value


@patch('app.flask.team_season_controller.team_season_repository')
def test_details_when_team_season_not_found_should_abort_with_404_error(fake_team_season_repository, test_app):
    # Arrange
    fake_team_season_repository.get_team_season.side_effect = IndexError()

    # Act
    with test_app.app_context():
        with pytest.raises(NotFound):
            result = team_season_controller.details(1)


@pytest.mark.skip('WIP')
def test_select_season_should_render_team_season_index_template_for_selected_year(test_app):
    with test_app.app_context():
        with test_app.test_request_context(
                '/team_seasons/select_season',
                method='POST'
        ):
            # Arrange

            # Act
            result = team_season_controller.select_season()

    # Assert
