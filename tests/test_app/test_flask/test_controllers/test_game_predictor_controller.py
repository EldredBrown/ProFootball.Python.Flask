from unittest.mock import patch, MagicMock, call

import pytest
from flask import session

import app.flask.game_predictor_controller as mod
from app.data.models.season import Season
from app.data.repositories.season_repository import SeasonRepository
from app.data.repositories.team_season_repository import TeamSeasonRepository
from app.services.game_predictor_service.game_predictor_service import GamePredictorService

from test_app import create_app


@pytest.fixture()
def test_app():
    return create_app()


@patch('app.flask.game_predictor_controller.render_template')
@patch('app.flask.game_predictor_controller.injector')
def test_index_should_render_game_predictor_index_template(
        fake_injector, fake_render_template, test_app
):
    with test_app.test_request_context(
            '/game_predictor/',
            method='GET'
    ):
        # Arrange
        fake_season_repository = MagicMock(SeasonRepository)
        seasons = (
            Season(id=1920),
            Season(id=1921),
            Season(id=1922),
        )
        fake_season_repository.get_seasons.return_value = seasons
        fake_injector.get.return_value = fake_season_repository

        selected_guest_season_year = None
        guests = []
        selected_guest_name = None

        selected_host_season_year = None
        hosts = []
        selected_host_name = None

        # fake_injector.get.return_value.get_seasons.side_effect = [guest_seasons, host_seasons]

        # Act
        result = mod.index()

        # Assert
        fake_injector.get.assert_called_once_with(SeasonRepository)
        fake_season_repository.get_seasons.assert_called_once()

        seasons = [s.to_dict() for s in seasons]
        assert session.get('guest_seasons') == seasons
        assert session.get('selected_guest_season_year') == selected_guest_season_year
        assert session.get('selected_guest_name') == selected_guest_name
        assert session.get('host_seasons') == seasons
        assert session.get('selected_host_season_year') == selected_host_season_year
        assert session.get('selected_host_name') == selected_host_name
        fake_render_template.assert_called_once_with(
            'game_predictor/index.html',
            guest_seasons=seasons, selected_guest_season_year=selected_guest_season_year,
            guests=guests, selected_guest_name=selected_guest_name,
            host_seasons=seasons, selected_host_season_year=selected_host_season_year,
            hosts=hosts, selected_host_name=selected_host_name
        )
        assert result is fake_render_template.return_value


@pytest.mark.skip('WIP')
def test_select_guest_season_should_render_game_predictor_index_template_with_guest_years_dropdown_set_to_selected_guest_year_and_guests_dropdown_populated_with_teams_from_selected_season():
    # Arrange

    # Act
    result = mod.select_guest_season()

    # Assert
    # selected_guest_season_year = int(request.form.get('guest_season_dropdown'))  # Fetch the selected guest season.
    # guests = team_season_repository.get_team_seasons_by_season_year(season_year=selected_guest_season_year)
    # return render_template(
    #     'game_predictor/index.html',
    #     guest_seasons=guest_seasons, selected_guest_season_year=selected_guest_season_year,
    #     guests=guests, selected_guest_name=selected_guest_name,
    #     host_seasons=host_seasons, selected_host_season_year=selected_host_season_year,
    #     hosts=hosts, selected_host_name=selected_host_name
    # )


@pytest.mark.skip('WIP')
def test_select_guest_should_render_game_predictor_index_template_with_guest_years_dropdown_set_to_selected_guest_year_and_guests_dropdown_set_to_selected_guest_name():
    # Arrange

    # Act
    result = mod.select_guest()

    # Assert
    # selected_guest_name = str(request.form.get('guest_dropdown'))
    # return render_template(
    #     'game_predictor/index.html',
    #     guest_seasons=guest_seasons, selected_guest_season_year=selected_guest_season_year,
    #     guests=guests, selected_guest_name=selected_guest_name,
    #     host_seasons=host_seasons, selected_host_season_year=selected_host_season_year,
    #     hosts=hosts, selected_host_name=selected_host_name
    # )


@pytest.mark.skip('WIP')
def test_select_host_season_should_render_game_predictor_index_template_with_host_years_dropdown_set_to_selected_host_year_and_hosts_dropdown_populated_with_teams_from_selected_season():
    # Arrange

    # Act
    result = mod.select_host_season()

    # Assert
    # selected_host_season_year = int(request.form.get('host_season_dropdown'))  # Fetch the selected host season.
    # hosts = team_season_repository.get_team_seasons_by_season_year(season_year=selected_host_season_year)
    # return render_template(
    #     'game_predictor/index.html',
    #     host_seasons=host_seasons, selected_host_season_year=selected_host_season_year,
    #     hosts=hosts, selected_host_name=selected_host_name,
    #     host_seasons=host_seasons, selected_host_season_year=selected_host_season_year,
    #     hosts=hosts, selected_host_name=selected_host_name
    # )


@pytest.mark.skip('WIP')
def test_select_host_should_render_game_predictor_index_template_with_host_years_dropdown_set_to_selected_host_year_and_hosts_dropdown_set_to_selected_host_name():
    # Arrange

    # Act
    result = mod.select_host()

    # Assert
    # selected_host_name = str(request.form.get('host_dropdown'))
    # return render_template(
    #     'game_predictor/index.html',
    #     host_seasons=host_seasons, selected_host_season_year=selected_host_season_year,
    #     hosts=hosts, selected_host_name=selected_host_name,
    #     host_seasons=host_seasons, selected_host_season_year=selected_host_season_year,
    #     hosts=hosts, selected_host_name=selected_host_name
    # )


@patch('app.flask.game_predictor_controller.render_template')
@patch('app.flask.game_predictor_controller.flash')
@patch('app.flask.game_predictor_controller.injector')
def test_predict_game_when_selected_guest_season_year_is_none_should_flash_error_message(
        fake_injector, fake_flash, fake_render_template, test_app
):
    with test_app.test_request_context(
            '/game_predictor/',
            method='GET'
    ):
        # Arrange
        fake_team_season_repository = MagicMock(TeamSeasonRepository)
        guests = []
        hosts = []
        fake_team_season_repository.get_team_seasons_by_season.side_effect = [guests, hosts]
        fake_injector.get.return_value = fake_team_season_repository

        guest_seasons = None
        session['guest_seasons'] = guest_seasons

        selected_guest_season_year = None
        session['selected_guest_season_year'] = selected_guest_season_year

        selected_guest_name = None
        session['selected_guest_name'] = selected_guest_name

        host_seasons = None
        session['host_seasons'] = host_seasons

        selected_host_season_year = None
        session['selected_host_season_year'] = selected_host_season_year

        selected_host_name = None
        session['selected_host_name'] = selected_host_name

        fake_game_predictor_service = MagicMock(GamePredictorService)

        # Act
        result = mod.predict_game()

        # Assert
        fake_injector.get.assert_called_once_with(TeamSeasonRepository)
        fake_team_season_repository.get_team_seasons_by_season.assert_has_calls([
            call(season_id=selected_guest_season_year),
            call(season_id=selected_host_season_year),
        ])
        fake_flash.assert_called_once_with("Please select one guest season.", 'danger')
        fake_game_predictor_service.predict_game_score.assert_not_called()
        fake_render_template.assert_called_once_with(
            'game_predictor/index.html',
            guest_seasons=guest_seasons, selected_guest_season_year=selected_guest_season_year,
            guests=session.get('guests'), selected_guest_name=selected_guest_name,
            host_seasons=host_seasons, selected_host_season_year=selected_host_season_year,
            hosts=session.get('hosts'), selected_host_name=selected_host_name
        )
        assert result is fake_render_template.return_value


@patch('app.flask.game_predictor_controller.render_template')
@patch('app.flask.game_predictor_controller.flash')
@patch('app.flask.game_predictor_controller.injector')
def test_predict_game_when_selected_guest_name_is_none_should_flash_error_message(
        fake_injector, fake_flash, fake_render_template, test_app
):
    with test_app.test_request_context(
            '/game_predictor/',
            method='GET'
    ):
        # Arrange
        fake_team_season_repository = MagicMock(TeamSeasonRepository)
        guests = []
        hosts = []
        fake_team_season_repository.get_team_seasons_by_season.side_effect = [guests, hosts]
        fake_injector.get.return_value = fake_team_season_repository

        guest_seasons = None
        session['guest_seasons'] = guest_seasons

        selected_guest_season_year = 1920
        session['selected_guest_season_year'] = selected_guest_season_year

        selected_guest_name = None
        session['selected_guest_name'] = selected_guest_name

        host_seasons = None
        session['host_seasons'] = host_seasons

        selected_host_season_year = None
        session['selected_host_season_year'] = selected_host_season_year

        selected_host_name = None
        session['selected_host_name'] = selected_host_name

        fake_game_predictor_service = MagicMock(GamePredictorService)

        # Act
        result = mod.predict_game()

        # Assert
        fake_injector.get.assert_called_once_with(TeamSeasonRepository)
        fake_team_season_repository.get_team_seasons_by_season.assert_has_calls([
            call(season_id=selected_guest_season_year),
            call(season_id=selected_host_season_year),
        ])
        fake_flash.assert_called_once_with("Please select one guest name.", 'danger')
        fake_game_predictor_service.predict_game_score.assert_not_called()
        fake_render_template.assert_called_once_with(
            'game_predictor/index.html',
            guest_seasons=guest_seasons, selected_guest_season_year=selected_guest_season_year,
            guests=session.get('guests'), selected_guest_name=selected_guest_name,
            host_seasons=host_seasons, selected_host_season_year=selected_host_season_year,
            hosts=session.get('hosts'), selected_host_name=selected_host_name
        )
        assert result is fake_render_template.return_value


@patch('app.flask.game_predictor_controller.render_template')
@patch('app.flask.game_predictor_controller.flash')
@patch('app.flask.game_predictor_controller.injector')
def test_predict_game_when_selected_host_season_year_is_none_should_flash_error_message(
        fake_injector, fake_flash, fake_render_template, test_app
):
    with test_app.test_request_context(
            '/game_predictor/',
            method='GET'
    ):
        # Arrange
        fake_team_season_repository = MagicMock(TeamSeasonRepository)
        guests = []
        hosts = []
        fake_team_season_repository.get_team_seasons_by_season.side_effect = [guests, hosts]
        fake_injector.get.return_value = fake_team_season_repository

        guest_seasons = None
        session['guest_seasons'] = guest_seasons

        selected_guest_season_year = 1920
        session['selected_guest_season_year'] = selected_guest_season_year

        selected_guest_name = "Guest"
        session['selected_guest_name'] = selected_guest_name

        host_seasons = None
        session['host_seasons'] = host_seasons

        selected_host_season_year = None
        session['selected_host_season_year'] = selected_host_season_year

        selected_host_name = None
        session['selected_host_name'] = selected_host_name

        fake_game_predictor_service = MagicMock(GamePredictorService)

        # Act
        result = mod.predict_game()

        # Assert
        fake_injector.get.assert_called_once_with(TeamSeasonRepository)
        fake_team_season_repository.get_team_seasons_by_season.assert_has_calls([
            call(season_id=selected_guest_season_year),
            call(season_id=selected_host_season_year),
        ])
        fake_flash.assert_called_once_with("Please select one host season.", 'danger')
        fake_game_predictor_service.predict_game_score.assert_not_called()
        fake_render_template.assert_called_once_with(
            'game_predictor/index.html',
            guest_seasons=guest_seasons, selected_guest_season_year=selected_guest_season_year,
            guests=session.get('guests'), selected_guest_name=selected_guest_name,
            host_seasons=host_seasons, selected_host_season_year=selected_host_season_year,
            hosts=session.get('hosts'), selected_host_name=selected_host_name
        )
        assert result is fake_render_template.return_value


@patch('app.flask.game_predictor_controller.render_template')
@patch('app.flask.game_predictor_controller.flash')
@patch('app.flask.game_predictor_controller.injector')
def test_predict_game_when_selected_host_name_is_none_should_flash_error_message(
        fake_injector, fake_flash, fake_render_template, test_app
):
    with test_app.test_request_context(
            '/game_predictor/',
            method='GET'
    ):
        # Arrange
        fake_team_season_repository = MagicMock(TeamSeasonRepository)
        guests = []
        hosts = []
        fake_team_season_repository.get_team_seasons_by_season.side_effect = [guests, hosts]
        fake_injector.get.return_value = fake_team_season_repository

        guest_seasons = None
        session['guest_seasons'] = guest_seasons

        selected_guest_season_year = 1920
        session['selected_guest_season_year'] = selected_guest_season_year

        selected_guest_name = "Guest"
        session['selected_guest_name'] = selected_guest_name

        host_seasons = None
        session['host_seasons'] = host_seasons

        selected_host_season_year = 1921
        session['selected_host_season_year'] = selected_host_season_year

        selected_host_name = None
        session['selected_host_name'] = selected_host_name

        fake_game_predictor_service = MagicMock(GamePredictorService)

        # Act
        result = mod.predict_game()

        # Assert
        fake_injector.get.assert_called_once_with(TeamSeasonRepository)
        fake_team_season_repository.get_team_seasons_by_season.assert_has_calls([
            call(season_id=selected_guest_season_year),
            call(season_id=selected_host_season_year),
        ])
        fake_flash.assert_called_once_with("Please select one host name.", 'danger')
        fake_game_predictor_service.predict_game_score.assert_not_called()
        fake_render_template.assert_called_once_with(
            'game_predictor/index.html',
            guest_seasons=guest_seasons, selected_guest_season_year=selected_guest_season_year,
            guests=session.get('guests'), selected_guest_name=selected_guest_name,
            host_seasons=host_seasons, selected_host_season_year=selected_host_season_year,
            hosts=session.get('hosts'), selected_host_name=selected_host_name
        )
        assert result is fake_render_template.return_value


@patch('app.flask.game_predictor_controller.render_template')
@patch('app.flask.game_predictor_controller.flash')
@patch('app.flask.game_predictor_controller.injector')
def test_predict_game_when_selected_guest_year_and_selected_guest_and_selected_host_year_and_selected_host_are_not_none_and_type_error_is_caught_should_flash_error_message(
        fake_injector, fake_flash, fake_render_template, test_app
):
    with test_app.test_request_context(
            '/game_predictor/',
            method='GET'
    ):
        # Arrange
        fake_team_season_repository = MagicMock(TeamSeasonRepository)
        guests = []
        hosts = []
        fake_team_season_repository.get_team_seasons_by_season.side_effect = [guests, hosts]

        fake_game_predictor_service = MagicMock(GamePredictorService)
        fake_game_predictor_service.predict_game_score.side_effect = Exception()

        fake_injector.get.side_effect = [fake_team_season_repository, fake_game_predictor_service]

        guest_seasons = None
        session['guest_seasons'] = guest_seasons

        selected_guest_season_year = 1920
        session['selected_guest_season_year'] = selected_guest_season_year

        selected_guest_name = "Guest"
        session['selected_guest_name'] = selected_guest_name

        host_seasons = None
        session['host_seasons'] = host_seasons

        selected_host_season_year = 1921
        session['selected_host_season_year'] = selected_host_season_year

        selected_host_name = "Host"
        session['selected_host_name'] = selected_host_name

        # Act
        result = mod.predict_game()

        # Assert
        fake_injector.get.assert_has_calls([
            call(TeamSeasonRepository),
            call(GamePredictorService),
        ])
        fake_team_season_repository.get_team_seasons_by_season.assert_has_calls([
            call(season_id=selected_guest_season_year),
            call(season_id=selected_host_season_year),
        ])
        fake_game_predictor_service.predict_game_score.assert_called_once_with(
            selected_guest_name, selected_guest_season_year, selected_host_name, selected_host_season_year
        )
        fake_flash.assert_called_once_with("A prediction could not be calculated.", 'danger')
        fake_render_template.assert_called_once_with(
            'game_predictor/index.html',
            guest_seasons=guest_seasons, selected_guest_season_year=selected_guest_season_year,
            guests=guests, selected_guest_name=selected_guest_name,
            host_seasons=host_seasons, selected_host_season_year=selected_host_season_year,
            hosts=hosts, selected_host_name=selected_host_name
        )
        assert result is fake_render_template.return_value


@patch('app.flask.game_predictor_controller.render_template')
@patch('app.flask.game_predictor_controller.flash')
@patch('app.flask.game_predictor_controller.injector')
def test_predict_game_when_type_error_is_not_caught_should_flash_success_message(
        fake_injector, fake_flash, fake_render_template, test_app
):
    with test_app.test_request_context(
            '/game_predictor/',
            method='GET'
    ):
        # Arrange
        fake_team_season_repository = MagicMock(TeamSeasonRepository)
        guests = []
        hosts = []
        fake_team_season_repository.get_team_seasons_by_season.side_effect = [guests, hosts]

        fake_game_predictor_service = MagicMock(GamePredictorService)
        guest_score = 0
        host_score = 0
        fake_game_predictor_service.predict_game_score.return_value = (guest_score, host_score)

        fake_injector.get.side_effect = [fake_team_season_repository, fake_game_predictor_service]

        guest_seasons = None
        session['guest_seasons'] = guest_seasons

        selected_guest_season_year = 1920
        session['selected_guest_season_year'] = selected_guest_season_year

        selected_guest_name = "Guest"
        session['selected_guest_name'] = selected_guest_name

        host_seasons = None
        session['host_seasons'] = host_seasons

        selected_host_season_year = 1921
        session['selected_host_season_year'] = selected_host_season_year

        selected_host_name = "Host"
        session['selected_host_name'] = selected_host_name

        # Act
        result = mod.predict_game()

        # Assert
        fake_injector.get.assert_has_calls([
            call(TeamSeasonRepository),
            call(GamePredictorService),
        ])
        fake_team_season_repository.get_team_seasons_by_season.assert_has_calls([
            call(season_id=selected_guest_season_year),
            call(season_id=selected_host_season_year),
        ])
        fake_game_predictor_service.predict_game_score.assert_called_once_with(
            selected_guest_name, selected_guest_season_year, selected_host_name, selected_host_season_year
        )
        fake_flash.assert_called_once_with(
            f"Game score predicted successfully. "
            f"{selected_guest_name} - {round(guest_score, 0)}, "
            f"{selected_host_name} - {round(host_score, 0)}",
            'success'
        )
        fake_render_template.assert_called_once_with(
            'game_predictor/index.html',
            guest_seasons=guest_seasons, selected_guest_season_year=selected_guest_season_year,
            guests=guests, selected_guest_name=selected_guest_name,
            host_seasons=host_seasons, selected_host_season_year=selected_host_season_year,
            hosts=hosts, selected_host_name=selected_host_name
        )
        assert result is fake_render_template.return_value
