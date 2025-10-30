from unittest.mock import patch

import pytest

import app.flask.game_predictor_controller as mut

from test_app import create_app


@pytest.fixture()
def test_app():
    return create_app()


@patch('app.flask.game_predictor_controller.render_template')
@patch('app.flask.game_predictor_controller.season_repository')
def test_index_should_render_game_predictor_index_template(fake_season_repository, fake_render_template, test_app):
    with test_app.app_context():
        # Arrange
        guest_seasons = [1920, 1921, 1922]
        host_seasons = [1920, 1921, 1922]
        fake_season_repository.get_seasons.side_effect = [guest_seasons, host_seasons]

        # Act
        result = mut.index()

    # Assert
    assert fake_season_repository.get_seasons.call_count == 2

    selected_guest_year = None
    guests = []
    selected_guest_name = None
    selected_host_year = None
    hosts = []
    selected_host_name = None

    fake_render_template.assert_called_once_with(
        'game_predictor/index.html',
        guest_seasons=guest_seasons, selected_guest_year=selected_guest_year,
        guests=guests, selected_guest_name=selected_guest_name,
        host_seasons=host_seasons, selected_host_year=selected_host_year,
        hosts=hosts, selected_host_name=selected_host_name
    )
    assert result is fake_render_template.return_value


@pytest.mark.skip('WIP')
def test_select_guest_season_should_render_game_predictor_index_template_with_guest_years_dropdown_set_to_selected_guest_year_and_guests_dropdown_populated_with_teams_from_selected_season(
        test_app
):
    with test_app.app_context():
        # Arrange

        # Act
        result = mut.select_guest_season()

    # Assert
    # selected_guest_year = int(request.form.get('guest_season_dropdown'))  # Fetch the selected guest season.
    # guests = team_season_repository.get_team_seasons_by_season_year(season_year=selected_guest_year)
    # return render_template(
    #     'game_predictor/index.html',
    #     guest_seasons=guest_seasons, selected_guest_year=selected_guest_year,
    #     guests=guests, selected_guest_name=selected_guest_name,
    #     host_seasons=host_seasons, selected_host_year=selected_host_year,
    #     hosts=hosts, selected_host_name=selected_host_name
    # )


@pytest.mark.skip('WIP')
def test_select_guest_should_render_game_predictor_index_template_with_guest_years_dropdown_set_to_selected_guest_year_and_guests_dropdown_set_to_selected_guest_name(
        test_app
):
    with test_app.app_context():
        # Arrange

        # Act
        result = mut.select_guest()

    # Assert
    # selected_guest_name = str(request.form.get('guest_dropdown'))
    # return render_template(
    #     'game_predictor/index.html',
    #     guest_seasons=guest_seasons, selected_guest_year=selected_guest_year,
    #     guests=guests, selected_guest_name=selected_guest_name,
    #     host_seasons=host_seasons, selected_host_year=selected_host_year,
    #     hosts=hosts, selected_host_name=selected_host_name
    # )


@pytest.mark.skip('WIP')
def test_select_host_season_should_render_game_predictor_index_template_with_host_years_dropdown_set_to_selected_host_year_and_hosts_dropdown_populated_with_teams_from_selected_season(
        test_app
):
    with test_app.app_context():
        # Arrange

        # Act
        result = mut.select_host_season()

    # Assert
    # selected_host_year = int(request.form.get('host_season_dropdown'))  # Fetch the selected host season.
    # hosts = team_season_repository.get_team_seasons_by_season_year(season_year=selected_host_year)
    # return render_template(
    #     'game_predictor/index.html',
    #     host_seasons=host_seasons, selected_host_year=selected_host_year,
    #     hosts=hosts, selected_host_name=selected_host_name,
    #     host_seasons=host_seasons, selected_host_year=selected_host_year,
    #     hosts=hosts, selected_host_name=selected_host_name
    # )


@pytest.mark.skip('WIP')
def test_select_host_should_render_game_predictor_index_template_with_host_years_dropdown_set_to_selected_host_year_and_hosts_dropdown_set_to_selected_host_name(
        test_app
):
    with test_app.app_context():
        # Arrange

        # Act
        result = mut.select_host()

    # Assert
    # selected_host_name = str(request.form.get('host_dropdown'))
    # return render_template(
    #     'game_predictor/index.html',
    #     host_seasons=host_seasons, selected_host_year=selected_host_year,
    #     hosts=hosts, selected_host_name=selected_host_name,
    #     host_seasons=host_seasons, selected_host_year=selected_host_year,
    #     hosts=hosts, selected_host_name=selected_host_name
    # )


@patch('app.flask.game_predictor_controller.render_template')
@patch('app.flask.game_predictor_controller.flash')
def test_predict_game_when_selected_guest_year_is_none_should_flash_error_message(
        fake_flash, fake_render_template, test_app
):
    with test_app.app_context():
        # Arrange
        mut.selected_guest_year = None

        # Act
        result = mut.predict_game()

    # Assert
    fake_flash.assert_called_once_with("Please select one guest season.", 'danger')
    fake_render_template.assert_called_once_with(
        'game_predictor/index.html',
        guest_seasons=mut.guest_seasons, selected_guest_year=mut.selected_guest_year,
        guests=mut.guests, selected_guest_name=mut.selected_guest_name,
        host_seasons=mut.host_seasons, selected_host_year=mut.selected_host_year,
        hosts=mut.hosts, selected_host_name=mut.selected_host_name
    )
    assert result is fake_render_template.return_value


@patch('app.flask.game_predictor_controller.render_template')
@patch('app.flask.game_predictor_controller.flash')
def test_predict_game_when_selected_guest_is_none_should_flash_error_message(
        fake_flash, fake_render_template, test_app
):
    with test_app.app_context():
        # Arrange
        mut.selected_guest_year = 1
        mut.selected_guest_name = None

        # Act
        result = mut.predict_game()

    # Assert
    fake_flash.assert_called_once_with("Please select one guest name.", 'danger')
    fake_render_template.assert_called_once_with(
        'game_predictor/index.html',
        guest_seasons=mut.guest_seasons, selected_guest_year=mut.selected_guest_year,
        guests=mut.guests, selected_guest_name=mut.selected_guest_name,
        host_seasons=mut.host_seasons, selected_host_year=mut.selected_host_year,
        hosts=mut.hosts, selected_host_name=mut.selected_host_name
    )
    assert result is fake_render_template.return_value


@patch('app.flask.game_predictor_controller.render_template')
@patch('app.flask.game_predictor_controller.flash')
def test_predict_game_when_selected_host_year_is_none_should_flash_error_message(
        fake_flash, fake_render_template, test_app
):
    with test_app.app_context():
        # Arrange
        mut.selected_guest_year = 1
        mut.selected_guest_name = "Guest"
        mut.selected_host_year = None

        # Act
        result = mut.predict_game()

    # Assert
    fake_flash.assert_called_once_with("Please select one host season.", 'danger')
    fake_render_template.assert_called_once_with(
        'game_predictor/index.html',
        guest_seasons=mut.guest_seasons, selected_guest_year=mut.selected_guest_year,
        guests=mut.guests, selected_guest_name=mut.selected_guest_name,
        host_seasons=mut.host_seasons, selected_host_year=mut.selected_host_year,
        hosts=mut.hosts, selected_host_name=mut.selected_host_name
    )
    assert result is fake_render_template.return_value


@patch('app.flask.game_predictor_controller.render_template')
@patch('app.flask.game_predictor_controller.flash')
def test_predict_game_when_selected_host_is_none_should_flash_error_message(
        fake_flash, fake_render_template, test_app
):
    with test_app.app_context():
        # Arrange
        mut.selected_guest_year = 1
        mut.selected_guest_name = "Guest"
        mut.selected_host_year = 1
        mut.selected_host_name = None

        # Act
        result = mut.predict_game()

    # Assert
    fake_flash.assert_called_once_with("Please select one host name.", 'danger')
    fake_render_template.assert_called_once_with(
        'game_predictor/index.html',
        guest_seasons=mut.guest_seasons, selected_guest_year=mut.selected_guest_year,
        guests=mut.guests, selected_guest_name=mut.selected_guest_name,
        host_seasons=mut.host_seasons, selected_host_year=mut.selected_host_year,
        hosts=mut.hosts, selected_host_name=mut.selected_host_name
    )
    assert result is fake_render_template.return_value


@patch('app.flask.game_predictor_controller.render_template')
@patch('app.flask.game_predictor_controller.flash')
@patch('app.flask.game_predictor_controller.GamePredictorService')
def test_predict_game_when_selected_guest_year_and_selected_guest_and_selected_host_year_and_selected_host_are_not_none_and_type_error_is_caught_should_flash_error_message(
        fake_game_predictor_service, fake_flash, fake_render_template, test_app
):
    with test_app.app_context():
        # Arrange
        mut.selected_guest_year = 1
        mut.selected_guest_name = "Guest"
        mut.selected_host_year = 1
        mut.selected_host_name = "Host"

        fake_game_predictor_service.return_value.predict_game_score.side_effect = Exception()

        # Act
        result = mut.predict_game()

    # Assert
    fake_flash.assert_called_once_with("The prediction could not be calculated.", 'danger')
    fake_render_template.assert_called_once_with(
        'game_predictor/index.html',
        guest_seasons=mut.guest_seasons, selected_guest_year=mut.selected_guest_year,
        guests=mut.guests, selected_guest_name=mut.selected_guest_name,
        host_seasons=mut.host_seasons, selected_host_year=mut.selected_host_year,
        hosts=mut.hosts, selected_host_name=mut.selected_host_name
    )
    assert result is fake_render_template.return_value


@patch('app.flask.game_predictor_controller.render_template')
@patch('app.flask.game_predictor_controller.flash')
@patch('app.flask.game_predictor_controller.GamePredictorService')
def test_predict_game_when_type_error_is_not_caught_should_flash_success_message(
        fake_game_predictor_service, fake_flash, fake_render_template, test_app
):
    with test_app.app_context():
        # Arrange
        mut.selected_guest_year = 1
        mut.selected_guest_name = "Guest"
        mut.selected_host_year = 1
        mut.selected_host_name = "Host"

        guest_score = 0
        host_score = 0
        fake_game_predictor_service.return_value.predict_game_score.return_value = (guest_score, host_score)

        # Act
        result = mut.predict_game()

    # Assert
    fake_game_predictor_service.return_value.predict_game_score.assert_called_once_with(
        mut.selected_guest_name, mut.selected_guest_year, mut.selected_host_name, mut.selected_host_year
    )
    fake_flash.assert_called_once_with(
        f"Game score predicted successfully. "
        f"{mut.selected_guest_name} - {round(guest_score, 0)}, "
        f"{mut.selected_host_name} - {round(host_score, 0)}",
        'success'
    )
    fake_render_template.assert_called_once_with(
        'game_predictor/index.html',
        guest_seasons=mut.guest_seasons, selected_guest_year=mut.selected_guest_year,
        guests=mut.guests, selected_guest_name=mut.selected_guest_name,
        host_seasons=mut.host_seasons, selected_host_year=mut.selected_host_year,
        hosts=mut.hosts, selected_host_name=mut.selected_host_name
    )
    assert result is fake_render_template.return_value
