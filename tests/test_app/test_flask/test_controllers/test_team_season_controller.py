from unittest.mock import patch, call, MagicMock

import pytest
from flask import session

from werkzeug.exceptions import NotFound

import app.flask.team_season_controller as mod
from app.data.models.league import League
from app.data.models.season import Season
from app.data.models.team_season import TeamSeason
from app.data.repositories.league_repository import LeagueRepository
from app.data.repositories.season_repository import SeasonRepository
from app.data.repositories.team_season_repository import TeamSeasonRepository
from app.data.repositories.team_season_schedule_repository import TeamSeasonScheduleRepository
from app.services.weekly_update_service.weekly_update_service import WeeklyUpdateService

from test_app import create_app


@pytest.fixture()
def test_app():
    return create_app()


@patch('app.flask.team_season_controller.render_template')
@patch('app.flask.team_season_controller.injector')
def test_index_when_no_values_in_session_should_set_session_variables_and_render_team_season_index_template(
        fake_injector, fake_render_template, test_app
):
    with test_app.test_request_context(
            '/team_seasons/',
            method='GET'
    ):
        # Arrange
        fake_season_repository = MagicMock(SeasonRepository)
        seasons = []
        fake_season_repository.get_seasons.return_value = seasons

        fake_league_repository = MagicMock(LeagueRepository)
        leagues = []
        fake_league_repository.get_leagues.return_value = leagues

        fake_team_season_repository = MagicMock(TeamSeasonRepository)
        team_seasons = []
        fake_team_season_repository.get_team_seasons_by_season.return_value = team_seasons

        fake_injector.get.side_effect = [
            fake_season_repository, fake_league_repository, fake_team_season_repository, fake_team_season_repository,
        ]

        # Act
        result = mod.index()

        # Assert
        fake_injector.get.assert_has_calls([
            call(SeasonRepository),
            call(LeagueRepository),
            call(TeamSeasonRepository),
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

        fake_team_season_repository.get_team_seasons_by_season.assert_called_once_with(season_id=selected_season_year)
        assert session.get('team_seasons') == team_seasons

        fake_render_template.assert_called_with(
            'team_seasons/index.html',
            seasons=seasons, selected_season_year=selected_season_year, leagues=leagues,
            selected_league_name=selected_league_name, team_seasons=team_seasons
        )
        assert result is fake_render_template.return_value


@patch('app.flask.team_season_controller.render_template')
@patch('app.flask.team_season_controller.injector')
def test_index_when_seasons_are_in_session_should_set_seasons_session_variable_and_render_team_season_index_template(
        fake_injector, fake_render_template, test_app
):
    with test_app.test_request_context(
            '/team_seasons/',
            method='GET'
    ):
        # Arrange
        fake_league_repository = MagicMock(LeagueRepository)
        leagues = []
        fake_league_repository.get_leagues.return_value = leagues

        fake_team_season_repository = MagicMock(TeamSeasonRepository)
        team_seasons = []
        fake_team_season_repository.get_team_seasons_by_season.return_value = team_seasons

        fake_injector.get.side_effect = [
            fake_league_repository, fake_team_season_repository, fake_team_season_repository,
        ]

        seasons = (
            Season(id=1920),
            Season(id=1921),
            Season(id=1922),
        )
        session['seasons'] = [s.to_dict() for s in seasons]

        # Act
        result = mod.index()

        # Assert
        fake_injector.get.assert_has_calls([
            call(LeagueRepository),
            call(TeamSeasonRepository),
        ])

        selected_season_year = -1
        assert session.get('selected_season_year') == selected_season_year

        fake_league_repository.get_leagues.assert_called_once()
        assert session.get('leagues') == leagues

        selected_league_name = ''
        assert session.get('selected_league_name') == selected_league_name

        fake_team_season_repository.get_team_seasons_by_season.assert_called_once_with(season_id=selected_season_year)
        assert session.get('team_seasons') == team_seasons

        fake_render_template.assert_called_with(
            'team_seasons/index.html',
            seasons=session.get('seasons'), selected_season_year=selected_season_year, leagues=leagues,
            selected_league_name=selected_league_name, team_seasons=team_seasons
        )
        assert result is fake_render_template.return_value


@patch('app.flask.team_season_controller.render_template')
@patch('app.flask.team_season_controller.injector')
def test_index_when_selected_season_id_is_in_session_should_set_selected_season_id_session_variable_and_render_team_season_index_template(
        fake_injector, fake_render_template, test_app
):
    with test_app.test_request_context(
            '/team_seasons/',
            method='GET'
    ):
        # Arrange
        fake_league_repository = MagicMock(LeagueRepository)
        leagues = []
        fake_league_repository.get_leagues.return_value = leagues

        fake_team_season_repository = MagicMock(TeamSeasonRepository)
        team_seasons = []
        fake_team_season_repository.get_team_seasons_by_season.return_value = team_seasons

        fake_injector.get.side_effect = [
            fake_league_repository, fake_team_season_repository, fake_team_season_repository,
        ]

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
        fake_injector.get.assert_has_calls([
            call(LeagueRepository),
            call(TeamSeasonRepository),
        ])

        fake_league_repository.get_leagues.assert_called_once()
        assert session.get('leagues') == leagues

        selected_league_name = ''
        assert session.get('selected_league_name') == selected_league_name

        fake_team_season_repository.get_team_seasons_by_season.assert_called_once_with(season_id=selected_season_year)
        assert session.get('team_seasons') == team_seasons

        fake_render_template.assert_called_with(
            'team_seasons/index.html',
            seasons=session.get('seasons'), selected_season_year=selected_season_year, leagues=leagues,
            selected_league_name=selected_league_name, team_seasons=team_seasons
        )
        assert result is fake_render_template.return_value


@patch('app.flask.team_season_controller.render_template')
@patch('app.flask.team_season_controller.injector')
def test_index_when_leagues_collection_has_leagues_and_not_all_leagues_are_active_in_selected_season_id_should_set_leagues_session_variable_and_render_team_season_index_template(
        fake_injector, fake_render_template, test_app
):
    with test_app.test_request_context(
            '/team_seasons/',
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

        fake_team_season_repository = MagicMock(TeamSeasonRepository)
        team_seasons = []
        fake_team_season_repository.get_team_seasons_by_season.return_value = team_seasons

        fake_injector.get.side_effect = [
            fake_league_repository, fake_team_season_repository, fake_team_season_repository,
        ]

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
        fake_injector.get.assert_has_calls([
            call(LeagueRepository),
            call(TeamSeasonRepository),
        ])

        fake_league_repository.get_leagues.assert_called_once()
        assert session.get('leagues') == [leagues[1].to_dict()]

        selected_league_name = ''
        assert session.get('selected_league_name') == selected_league_name

        fake_team_season_repository.get_team_seasons_by_season.assert_called_once_with(season_id=selected_season_year)
        assert session.get('team_seasons') == team_seasons

        fake_render_template.assert_called_with(
            'team_seasons/index.html',
            seasons=session.get('seasons'), selected_season_year=selected_season_year, leagues=session.get('leagues'),
            selected_league_name=selected_league_name, team_seasons=team_seasons
        )
        assert result is fake_render_template.return_value


@patch('app.flask.team_season_controller.render_template')
@patch('app.flask.team_season_controller.injector')
def test_index_when_selected_league_name_is_not_empty_should_set_selected_league_name_session_variable_and_render_team_season_index_template(
        fake_injector, fake_render_template, test_app
):
    with test_app.test_request_context(
            '/team_seasons/',
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

        fake_team_season_repository = MagicMock(TeamSeasonRepository)
        team_seasons = []
        fake_team_season_repository.get_team_seasons_by_season.return_value = team_seasons

        fake_injector.get.side_effect = [
            fake_league_repository, fake_team_season_repository, fake_team_season_repository,
        ]

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
        fake_injector.get.assert_has_calls([
            call(LeagueRepository),
            call(TeamSeasonRepository),
        ])

        fake_league_repository.get_leagues.assert_called_once()
        assert session.get('leagues') == [leagues[1].to_dict()]

        fake_team_season_repository.get_team_seasons_by_season.assert_called_once_with(season_id=selected_season_year)
        assert session.get('team_seasons') == team_seasons

        fake_render_template.assert_called_with(
            'team_seasons/index.html',
            seasons=session.get('seasons'), selected_season_year=selected_season_year, leagues=session.get('leagues'),
            selected_league_name=selected_league_name, team_seasons=team_seasons
        )
        assert result is fake_render_template.return_value


@patch('app.flask.team_season_controller.render_template')
@patch('app.flask.team_season_controller.injector')
def test_index_when_team_seasons_is_not_empty_should_set_team_seasons_session_variable_and_render_team_season_index_template(
        fake_injector, fake_render_template, test_app
):
    with test_app.test_request_context(
            '/team_seasons/',
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

        fake_team_season_repository = MagicMock(TeamSeasonRepository)

        team_seasons = []
        for i in range(1, 10):
            team_season = MagicMock(TeamSeason)
            team_season.id = i
            team_season.team_id = i - 3 * ((i - 1) // 3)
            team_season.season_id = 1920 + (i - 1) // 3
            team_seasons.append(team_season)

        selected_season_year = 1922
        selected_team_seasons = [ts for ts in team_seasons if ts.season_id == selected_season_year]
        fake_team_season_repository.get_team_seasons_by_season.return_value = selected_team_seasons

        fake_injector.get.side_effect = [
            fake_league_repository, fake_team_season_repository, fake_team_season_repository,
        ]

        seasons = (
            Season(id=1920),
            Season(id=1921),
            Season(id=1922),
        )
        session['seasons'] = [s.to_dict() for s in seasons]

        session['selected_season_year'] = selected_season_year

        selected_league_name = 'L'
        session['selected_league_name'] = selected_league_name

        # Act
        result = mod.index()

        # Assert
        fake_injector.get.assert_has_calls([
            call(LeagueRepository),
            call(TeamSeasonRepository),
        ])

        fake_league_repository.get_leagues.assert_called_once()
        assert session.get('leagues') == [leagues[1].to_dict()]

        fake_team_season_repository.get_team_seasons_by_season.assert_called_once_with(season_id=selected_season_year)
        assert session.get('team_seasons') == [ts.to_dict() for ts in selected_team_seasons]

        fake_render_template.assert_called_with(
            'team_seasons/index.html',
            seasons=session.get('seasons'), selected_season_year=selected_season_year, leagues=session.get('leagues'),
            selected_league_name=selected_league_name, team_seasons=selected_team_seasons
        )
        assert result is fake_render_template.return_value


@pytest.mark.skip('WIP')
@patch('app.flask.team_season_controller.render_template')
@patch('app.flask.team_season_controller.injector')
@patch('app.flask.team_season_controller.request')
def test_select_season_should_render_team_season_index_template_for_selected_season_id(
        fake_request, fake_injector, fake_render_template, test_app
):
    with test_app.test_request_context(
            '/team_seasons/select_season',
            method='POST'
    ):
        # Arrange
        selected_season_year = 1922
        fake_request.form.get.return_value = selected_season_year

        fake_league_repository = MagicMock(LeagueRepository)
        leagues = (
            League(id=1, short_name='L1', long_name='League 1', first_season_id=1920, last_season_id=1921),
            League(id=2, short_name='L2', long_name='League 2', first_season_id=1921, last_season_id=1923),
            League(id=3, short_name='L3', long_name='League 3', first_season_id=1923, last_season_id=1924),
        )
        fake_league_repository.get_leagues.return_value = leagues

        fake_team_season_repository = MagicMock(TeamSeasonRepository)

        team_seasons = []
        for i in range(1, 4):
            team_season = MagicMock(TeamSeason)
            team_season.id = i
            team_season.team_id = 1
            team_season.season_id = 1919 + i
            team_seasons.append(team_season)

        selected_team_seasons = [team_seasons[-1]]
        fake_team_season_repository.get_team_seasons_by_season.return_value = selected_team_seasons

        fake_injector.get.side_effect = [fake_league_repository, fake_team_season_repository]

        seasons = [
            Season(id=1920),
            Season(id=1921),
            Season(id=1922),
        ]
        session['seasons'] = [s.to_dict() for s in seasons]

        selected_league_name = 'L'
        session['selected_league_name'] = selected_league_name

        # Act
        result = mod.select_season()

    # Assert
    fake_request.form.get.assert_called_once_with('season_dropdown')
    assert session.get('selected_season_year') == selected_season_year
    fake_injector.get.assert_has_calls([
        call(LeagueRepository),
        call(TeamSeasonRepository),
    ])
    fake_league_repository.get_leagues.assert_called_once()
    leagues_active_in_selected_season_id = [leagues[1]]
    assert session.get('leagues') == [l.to_dict() for l in leagues_active_in_selected_season_id]
    fake_team_season_repository.get_team_seasons_by_season.assert_called_once_with(season_id=selected_season_year)
    assert session.get('team_seasons') == [ts.to_dict() for ts in selected_team_seasons]

    fake_render_template.assert_called_with(
        'team_seasons/index.html',
        seasons=session.get('seasons'), selected_season_year=selected_season_year, leagues=leagues_active_in_selected_season_id,
        selected_league_name=session.get('selected_league_name'), team_seasons=team_seasons
    )
    assert result is fake_render_template.return_value


@pytest.mark.skip('WIP')
@patch('app.flask.team_season_controller.render_template')
@patch('app.flask.team_season_controller.injector')
@patch('app.flask.team_season_controller.request')
def test_select_league_should_render_rankings_index_template_for_selected_league(
        fake_request, fake_injector, fake_render_template, test_app
):
    with test_app.test_request_context(
            '/team_seasons/select_league',
            method='POST'
    ):
        # Arrange
        selected_league_name = "L"
        fake_request.form.get.return_value = selected_league_name

        selected_season_year = 1921
        session['selected_season_year'] = selected_season_year

        fake_team_season_repository = MagicMock(TeamSeasonRepository)

        team_seasons = []
        for i in range(1, 4):
            team_season = MagicMock(TeamSeason)
            team_season.id = i
            team_season.team_id = 1
            team_season.season_id = 1919 + i
            team_seasons.append(team_season)

        selected_team_seasons = [team_seasons[1]]
        fake_team_season_repository.get_team_seasons_by_season.return_value = selected_team_seasons
        fake_injector.get.return_value = fake_team_season_repository

        # Act
        result = mod.select_league()

    # Assert
    fake_request.form.get.assert_called_once_with('league_dropdown')
    assert session.get('selected_league_name') == selected_league_name
    fake_injector.get.assert_called_once_with(TeamSeasonRepository)
    fake_team_season_repository.get_team_seasons_by_season.assert_called_once_with(season_id=selected_season_year)
    assert session.get('team_seasons') == [ts.to_dict() for ts in selected_team_seasons]
    fake_render_template.assert_called_once_with(
        'team_seasons/index.html',
        seasons=session.get('seasons'), selected_season_year=session.get('selected_season_year'),
        leagues=session.get('leagues'), selected_league_name=selected_league_name, team_seasons=team_seasons
    )
    assert result is fake_render_template.return_value


@patch('app.flask.team_season_controller.render_template')
@patch('app.flask.team_season_controller.injector')
def test_details_when_team_season_found_should_render_team_season_details_template(
        fake_injector, fake_render_template
):
    # Arrange
    fake_team_season_repository = MagicMock(TeamSeasonRepository)
    team_season = TeamSeason(team_id=1, season_id=1)
    fake_team_season_repository.get_team_season.return_value = team_season

    fake_team_season_schedule_repository = MagicMock(TeamSeasonScheduleRepository)
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
        team_season.team_id, team_season.season_id
    )
    fake_team_season_schedule_repository.get_team_season_schedule_totals.assert_called_once_with(
        team_season.team_id, team_season.season_id
    )
    fake_team_season_schedule_repository.get_team_season_schedule_averages.assert_called_once_with(
        team_season.team_id, team_season.season_id
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
    fake_team_season_repository = MagicMock(TeamSeasonRepository)
    fake_team_season_repository.get_team_season.side_effect = IndexError()
    fake_team_season_schedule_repository = MagicMock(TeamSeasonScheduleRepository)
    fake_injector.get.side_effect = [fake_team_season_repository, fake_team_season_schedule_repository]

    # Act
    with pytest.raises(NotFound):
        result = mod.details(1)


@patch('app.flask.team_season_controller.render_template')
@patch('app.flask.team_season_controller.flash')
@patch('app.flask.team_season_controller.injector')
def test_run_weekly_update_should_run_weekly_update(
        fake_injector, fake_flash, fake_render_template, test_app
):
    with test_app.test_request_context('/team_seasons/', method='GET'):
        # Arrange
        fake_weekly_update_service = MagicMock(WeeklyUpdateService)

        fake_league_repository = MagicMock(LeagueRepository)
        selected_league = League(id=1, short_name="L", long_name="League")
        fake_league_repository.get_league_by_short_name.return_value = selected_league

        fake_injector.get.side_effect = [fake_weekly_update_service, fake_league_repository]

        selected_league_name = "L"
        session['selected_league_name'] = selected_league_name

        selected_season_year = 1920
        session['selected_season_year'] = selected_season_year

        seasons = [
            Season(id=1920),
            Season(id=1921),
            Season(id=1922),
        ]
        session['seasons'] = [s.to_dict() for s in seasons]

        selected_season_year = 1921
        session['selected_season_year'] = selected_season_year

        # Act
        mod.run_weekly_update()

        # Assert
        fake_injector.get.assert_has_calls([
            call(WeeklyUpdateService),
            call(LeagueRepository),
        ])
        fake_league_repository.get_league_by_short_name.assert_called_once_with(selected_league_name)
        fake_weekly_update_service.run_weekly_update.assert_called_once_with(selected_league.id, selected_season_year)

        fake_flash.assert_called_once_with(
            f"The weekly update has been successfully completed for the '{selected_league_name}' in {selected_season_year}.",
            'success'
        )
        fake_render_template.assert_called_once_with(
            'team_seasons/index.html',
            seasons=session.get('seasons'), selected_season_year=selected_season_year, leagues=session.get('leagues'),
            selected_league_name=selected_league_name, team_seasons=session.get('team_seasons')
        )
