from unittest.mock import patch, Mock

import pytest

from werkzeug.exceptions import NotFound

import app.flask.team_season_controller as mod
from app.data.models.game import Game
from app.data.models.league_season import LeagueSeason
from app.data.models.team_season import TeamSeason
from app.data.repositories.season_repository import SeasonRepository
from app.data.repositories.team_season_repository import TeamSeasonRepository
from app.data.repositories.team_season_schedule_repository import TeamSeasonScheduleRepository

from test_app import create_app


@pytest.fixture()
def test_app():
    return create_app()


@patch('app.flask.team_season_controller.render_template')
@patch('app.flask.team_season_controller.injector')
def test_index_should_render_team_season_index_template(fake_injector, fake_render_template):
    # Arrange
    mod.selected_year = 1

    # Act
    result = mod.index()

    # Assert
    fake_injector.get.assert_called_once_with(SeasonRepository)
    fake_injector.get.return_value.get_seasons.assert_called_once()
    fake_render_template.assert_called_once_with(
        'team_seasons/index.html',
        seasons=fake_injector.get.return_value.get_seasons.return_value, selected_year=mod.selected_year,
        team_seasons=[]
    )
    assert result is fake_render_template.return_value


@patch('app.flask.team_season_controller.render_template')
@patch('app.flask.team_season_controller.team_season_repository')
@patch('app.flask.team_season_controller.injector')
def test_details_when_team_season_found_should_render_team_season_details_template(
        fake_injector, fake_team_season_repository, fake_render_template
):
    # Arrange
    team_season = TeamSeason(team_name="Team", season_year=1)
    fake_team_season_repository.get_team_season.return_value = team_season

    id = 1

    # Act
    result = mod.details(id)

    # Assert
    fake_injector.get.assert_called_once_with(TeamSeasonScheduleRepository)

    fake_team_season_repository.get_team_season.assert_called_once_with(id)
    fake_injector.get.return_value.get_team_season_schedule_profile.assert_called_once_with(
        team_season.team_name, team_season.season_year
    )
    fake_injector.get.return_value.get_team_season_schedule_totals.assert_called_once_with(
        team_season.team_name, team_season.season_year
    )
    fake_injector.get.return_value.get_team_season_schedule_averages.assert_called_once_with(
        team_season.team_name, team_season.season_year
    )
    fake_render_template.assert_called_once_with(
        'team_seasons/details.html',
        team_season=team_season,
        team_season_schedule_profile=fake_injector.get.return_value.get_team_season_schedule_profile.return_value,
        team_season_schedule_totals=[fake_injector.get.return_value.get_team_season_schedule_totals.return_value],
        team_season_schedule_averages=[fake_injector.get.return_value.get_team_season_schedule_averages.return_value]
    )
    assert result is fake_render_template.return_value


@patch('app.flask.team_season_controller.team_season_repository')
def test_details_when_team_season_not_found_should_abort_with_404_error(fake_team_season_repository):
    # Arrange
    fake_team_season_repository.get_team_season.side_effect = IndexError()

    # Act
    with pytest.raises(NotFound):
        result = mod.details(1)


@pytest.mark.skip('WIP')
def test_select_season_should_render_team_season_index_template_for_selected_year(test_app):
    with test_app.test_request_context(
            '/team_seasons/select_season',
            method='POST'
    ):
        # Arrange

        # Act
        result = mod.select_season()

    # Assert
