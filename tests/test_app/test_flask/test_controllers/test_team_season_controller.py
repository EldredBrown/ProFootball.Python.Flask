from unittest.mock import patch, Mock, call

import pytest
from flask import session

from werkzeug.exceptions import NotFound

import app.flask.team_season_controller as mod
from app.data.models.season import Season
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
def test_index_should_render_team_season_index_template(fake_injector, fake_render_template, test_app):
    with test_app.test_request_context(
            '/team_seasons/',
            method='GET'
    ):
        # Arrange
        fake_season_repository = Mock(SeasonRepository)
        fake_season_repository.get_seasons.return_value = [
            Season(year=1920),
            Season(year=1921),
            Season(year=1922),
        ]
        fake_injector.get.return_value = fake_season_repository

        session['seasons'] = []

        selected_year = 0

        # Act
        result = mod.index()

        # Assert
        fake_injector.get.assert_called_once_with(SeasonRepository)
        fake_season_repository.get_seasons.assert_called_once()

        seasons = [s.to_dict() for s in fake_season_repository.get_seasons.return_value]
        assert session.get('seasons') == seasons

        assert session.get('selected_year') == selected_year

        fake_render_template.assert_called_once_with(
            'team_seasons/index.html',
            seasons=seasons, selected_year=selected_year, team_seasons=[]
        )
        assert result is fake_render_template.return_value


@patch('app.flask.team_season_controller.render_template')
@patch('app.flask.team_season_controller.injector')
def test_details_when_team_season_found_should_render_team_season_details_template(fake_injector, fake_render_template):
    # Arrange
    fake_team_season_repository = Mock(TeamSeasonRepository)
    team_season = TeamSeason(team_name="Team", season_year=1)
    fake_team_season_repository.get_team_season.return_value = team_season

    fake_team_season_schedule_repository = Mock(TeamSeasonScheduleRepository)
    fake_injector.get.side_effect = [fake_team_season_repository, fake_team_season_schedule_repository]

    id = 1

    # Act
    result = mod.details(id)

    # Assert
    fake_injector.get.assert_has_calls([
        call(TeamSeasonRepository),
        call(TeamSeasonScheduleRepository),
    ])

    fake_team_season_repository.get_team_season.assert_called_once_with(id)
    fake_team_season_schedule_repository.get_team_season_schedule_profile.assert_called_once_with(
        team_season.team_name, team_season.season_year
    )
    fake_team_season_schedule_repository.get_team_season_schedule_totals.assert_called_once_with(
        team_season.team_name, team_season.season_year
    )
    fake_team_season_schedule_repository.get_team_season_schedule_averages.assert_called_once_with(
        team_season.team_name, team_season.season_year
    )
    fake_render_template.assert_called_once_with(
        'team_seasons/details.html',
        team_season=team_season,
        team_season_schedule_profile=fake_team_season_schedule_repository.get_team_season_schedule_profile.return_value,
        team_season_schedule_totals=[fake_team_season_schedule_repository.get_team_season_schedule_totals.return_value],
        team_season_schedule_averages=[fake_team_season_schedule_repository.get_team_season_schedule_averages.return_value]
    )
    assert result is fake_render_template.return_value


@patch('app.flask.team_season_controller.injector')
def test_details_when_team_season_not_found_should_abort_with_404_error(fake_injector):
    # Arrange
    fake_team_season_repository = Mock(TeamSeasonRepository)
    fake_team_season_repository.get_team_season.side_effect = IndexError()
    fake_team_season_schedule_repository = Mock(TeamSeasonScheduleRepository)
    fake_injector.get.side_effect = [fake_team_season_repository, fake_team_season_schedule_repository]

    # Act
    with pytest.raises(NotFound):
        result = mod.details(1)


@pytest.mark.skip('WIP')
@patch('app.flask.team_season_controller.render_template')
@patch('app.flask.team_season_controller.injector')
@patch('app.flask.team_season_controller.request')
def test_select_season_should_render_team_season_index_template_for_selected_year(
        fake_request, fake_injector, fake_render_template, test_app
):
    with test_app.test_request_context(
            '/team_seasons/select_season',
            method='POST'
    ) as context:
        # Arrange
        fake_team_season_repository = Mock(TeamSeasonRepository)
        fake_injector.get.return_value = fake_team_season_repository

        # Act
        result = mod.select_season()

        # Assert
        fake_request.form.get.assert_called_once_with('season_dropdown')

        fake_injector.get.assert_called_once_with(TeamSeasonRepository)

        selected_year = int(fake_request.form.get.return_value)
        fake_team_season_repository.get_team_seasons_by_season_year.assert_called_once_with(season_year=selected_year)

        fake_render_template.assert_called_once_with(
            'team_seasons/index.html',
            seasons=session.get('seasons'), selected_year=selected_year,
            team_seasons=fake_team_season_repository.get_team_seasons_by_season_year.return_value
        )
        assert result is fake_render_template.return_value
