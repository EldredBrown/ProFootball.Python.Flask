from unittest.mock import patch, MagicMock, MagicMock

import pytest

from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound

import app.flask.team_season_admin_controller as mod
from app.data.models.association import Association
from app.data.models.season import Season
from app.data.models.team import Team
from app.data.models.team_season import TeamSeason
from app.data.repositories.team_season_repository import TeamSeasonRepository
from test_app import create_app


@pytest.fixture()
def test_app():
    return create_app()


@patch('app.flask.team_season_admin_controller.render_template')
@patch('app.flask.team_season_admin_controller.injector')
def test_index_should_render_team_season_index_template(
        fake_injector, fake_render_template
):
    # Arrange
    fake_team_season_repository = MagicMock(TeamSeasonRepository)
    fake_injector.get.return_value = fake_team_season_repository

    # Act
    result = mod.index()

    # Assert
    fake_injector.get.assert_called_once_with(TeamSeasonRepository)
    fake_team_season_repository.get_team_seasons.assert_called_once()
    fake_render_template.assert_called_once_with(
        'team_seasons_admin/index.html', team_seasons=fake_team_season_repository.get_team_seasons.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.team_season_admin_controller.render_template')
@patch('app.flask.team_season_admin_controller.injector')
@patch('app.flask.team_season_admin_controller.DeleteTeamSeasonForm')
def test_details_when_team_season_found_should_render_team_season_details_template(
        fake_form, fake_injector, fake_render_template
):
    # Arrange
    fake_team_season_repository = MagicMock(TeamSeasonRepository)
    fake_injector.get.return_value = fake_team_season_repository

    id = 1

    # Act
    result = mod.details(id)

    # Assert
    fake_form.assert_called_once()
    fake_injector.get.assert_called_once_with(TeamSeasonRepository)
    fake_team_season_repository.get_team_season.assert_called_once_with(id)
    fake_render_template.assert_called_once_with(
        'team_seasons_admin/details.html',
        team_season=fake_team_season_repository.get_team_season.return_value,
        form=fake_form.return_value
    )
    assert result == fake_render_template.return_value


@patch('app.flask.team_season_admin_controller.injector')
@patch('app.flask.team_season_admin_controller.DeleteTeamSeasonForm')
def test_details_when_team_season_not_found_should_abort_with_404_error(fake_form, fake_injector):
    # Arrange
    fake_team_season_repository = MagicMock(TeamSeasonRepository)
    fake_team_season_repository.get_team_season.side_effect = IndexError()
    fake_injector.get.return_value = fake_team_season_repository

    # Act
    with pytest.raises(NotFound):
        result = mod.details(1)


@patch('app.flask.team_season_admin_controller.render_template')
@patch('app.flask.team_season_admin_controller.flash')
@patch('app.flask.team_season_admin_controller.injector')
@patch('app.flask.team_season_admin_controller.NewTeamSeasonForm')
def test_create_when_form_not_submitted_and_no_form_errors_should_render_create_template(
        fake_form, fake_injector, fake_flash, fake_render_template
):
    # Arrange
    fake_form.return_value.validate_on_submit.return_value = False
    fake_form.return_value.errors = None

    fake_team_season_repository = MagicMock(TeamSeasonRepository)
    fake_injector.get.return_value = fake_team_season_repository

    # Act
    result = mod.create()

    # Assert
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    fake_injector.get.assert_not_called()
    fake_team_season_repository.add_team_season.assert_not_called()
    fake_flash.assert_not_called()
    fake_render_template('team_seasons_admin/create.html', form=fake_form.return_value)
    assert result is fake_render_template.return_value


@patch('app.flask.team_season_admin_controller.render_template')
@patch('app.flask.team_season_admin_controller.flash')
@patch('app.flask.team_season_admin_controller.injector')
@patch('app.flask.team_season_admin_controller.NewTeamSeasonForm')
def test_create_when_form_not_submitted_and_form_errors_should_flash_errors_and_render_create_template(
        fake_form, fake_injector, fake_flash, fake_render_template
):
    # Arrange
    fake_form.return_value.validate_on_submit.return_value = False

    errors = 'errors'
    fake_form.return_value.errors = errors

    fake_team_season_repository = MagicMock(TeamSeasonRepository)
    fake_injector.get.return_value = fake_team_season_repository

    # Act
    result = mod.create()

    # Assert
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    fake_injector.get.assert_not_called()
    fake_team_season_repository.add_team_season.assert_not_called()
    fake_flash.assert_called_once_with(f"{errors}", 'danger')
    fake_render_template('team_seasons_admin/create.html', form=fake_form.return_value)
    assert result is fake_render_template.return_value


@patch('app.flask.team_season_admin_controller.redirect')
@patch('app.flask.team_season_admin_controller.url_for')
@patch('app.flask.team_season_admin_controller.flash')
@patch('app.flask.team_season_admin_controller.injector')
@patch('app.flask.team_season_admin_controller.team_season_factory')
@patch('app.flask.team_season_admin_controller.NewTeamSeasonForm')
def test_create_when_form_submitted_and_no_errors_caught_should_flash_success_message_and_redirect_to_team_season_index(
        fake_form, fake_team_season_factory, fake_injector, fake_flash,
        fake_url_for, fake_redirect
):
    # Arrange
    team_season = TeamSeason(team_id=1, season_year=1920, league_id=1, conference_id=2, division_id=3)
    team_season.team = Team(id=1, name="Team")
    team_season.season = Season(year=1920)
    team_season.league = Association(id=1, long_name="League", short_name="L")
    team_season.conference = Association(id=2, long_name="Conference", short_name="C")
    team_season.division = Association(id=3, long_name="Division", short_name="D")

    fake_form.return_value.validate_on_submit.return_value = True
    fake_form.return_value.team_name.data = team_season.team.name
    fake_form.return_value.season_year.data = team_season.season.year
    fake_form.return_value.league_name.data = team_season.league.short_name
    fake_form.return_value.conference_name.data = team_season.conference.short_name
    fake_form.return_value.division_name.data = team_season.division.short_name

    fake_team_season_factory.create_team_season.return_value = team_season

    fake_team_season_repository = MagicMock(TeamSeasonRepository)
    fake_injector.get.return_value = fake_team_season_repository

    # Act
    result = mod.create()

    # Assert
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    view_kwargs = {
        'team_name': team_season.team.name,
        'season_year': team_season.season.year,
        'league_name': team_season.league.short_name,
        'conference_name': team_season.conference.short_name,
        'division_name': team_season.division.short_name,
    }
    fake_team_season_factory.create_team_season.assert_called_once_with(**view_kwargs)
    fake_injector.get.assert_called_once_with(TeamSeasonRepository)
    fake_team_season_repository.add_team_season.assert_called_once_with(team_season)
    fake_flash(f"Item {team_season.team.name}, {team_season.season.year} has been successfully submitted.", 'success')
    fake_url_for.assert_called_once_with('team_season_admin.index')
    fake_redirect.assert_called_once_with(fake_url_for.return_value)
    assert result is fake_redirect.return_value


@patch('app.flask.team_season_admin_controller.render_template')
@patch('app.flask.team_season_admin_controller.flash')
@patch('app.flask.team_season_admin_controller.injector')
@patch('app.flask.team_season_admin_controller.team_season_factory')
@patch('app.flask.team_season_admin_controller.NewTeamSeasonForm')
def test_create_when_form_submitted_and_value_error_caught_should_flash_error_message_and_render_create_template(
        fake_form, fake_team_season_factory, fake_injector, 
        fake_flash, fake_render_template
):
    # Arrange
    team_season = TeamSeason(team_id=1, season_year=1920, league_id=1, conference_id=2, division_id=3)
    team_season.team = Team(id=1, name="Team")
    team_season.season = Season(year=1920)
    team_season.league = Association(id=1, long_name="League", short_name="L")
    team_season.conference = Association(id=2, long_name="Conference", short_name="C")
    team_season.division = Association(id=3, long_name="Division", short_name="D")

    fake_form.return_value.validate_on_submit.return_value = True
    fake_form.return_value.team_name.data = team_season.team.name
    fake_form.return_value.season_year.data = team_season.season.year
    fake_form.return_value.league_name.data = team_season.league.short_name
    fake_form.return_value.conference_name.data = team_season.conference.short_name
    fake_form.return_value.division_name.data = team_season.division.short_name

    fake_team_season_factory.create_team_season.return_value = team_season

    fake_team_season_repository = MagicMock(TeamSeasonRepository)
    err = ValueError()
    fake_team_season_repository.add_team_season.side_effect = err
    fake_injector.get.return_value = fake_team_season_repository

    # Act
    result = mod.create()

    # Assert
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    view_kwargs = {
        'team_name': team_season.team.name,
        'season_year': team_season.season.year,
        'league_name': team_season.league.short_name,
        'conference_name': team_season.conference.short_name,
        'division_name': team_season.division.short_name,
    }
    fake_team_season_factory.create_team_season.assert_called_once_with(**view_kwargs)
    fake_injector.get.assert_called_once_with(TeamSeasonRepository)
    fake_team_season_repository.add_team_season.assert_called_once_with(team_season)
    fake_flash.assert_called_once_with(str(err), 'danger')
    fake_render_template.assert_called_once_with(
        'team_seasons_admin/create.html', team_season=None, form=fake_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.team_season_admin_controller.render_template')
@patch('app.flask.team_season_admin_controller.flash')
@patch('app.flask.team_season_admin_controller.injector')
@patch('app.flask.team_season_admin_controller.team_season_factory')
@patch('app.flask.team_season_admin_controller.NewTeamSeasonForm')
def test_create_when_form_submitted_and_integrity_error_caught_should_flash_error_message_and_render_create_template(
        fake_form, fake_team_season_factory, fake_injector,
        fake_flash, fake_render_template
):
    # Arrange
    team_season = TeamSeason(team_id=1, season_year=1920, league_id=1, conference_id=2, division_id=3)
    team_season.team = Team(id=1, name="Team")
    team_season.season = Season(year=1920)
    team_season.league = Association(id=1, long_name="League", short_name="L")
    team_season.conference = Association(id=2, long_name="Conference", short_name="C")
    team_season.division = Association(id=3, long_name="Division", short_name="D")

    fake_form.return_value.validate_on_submit.return_value = True
    fake_form.return_value.team_name.data = team_season.team.name
    fake_form.return_value.season_year.data = team_season.season.year
    fake_form.return_value.league_name.data = team_season.league.short_name
    fake_form.return_value.conference_name.data = team_season.conference.short_name
    fake_form.return_value.division_name.data = team_season.division.short_name

    fake_team_season_factory.create_team_season.return_value = team_season

    fake_team_season_repository = MagicMock(TeamSeasonRepository)
    err = IntegrityError('statement', 'params', Exception())
    fake_team_season_repository.add_team_season.side_effect = err
    fake_injector.get.return_value = fake_team_season_repository

    # Act
    result = mod.create()

    # Assert
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    view_kwargs = {
        'team_name': team_season.team.name,
        'season_year': team_season.season.year,
        'league_name': team_season.league.short_name,
        'conference_name': team_season.conference.short_name,
        'division_name': team_season.division.short_name,
    }
    fake_team_season_factory.create_team_season.assert_called_once_with(**view_kwargs)
    fake_injector.get.assert_called_once_with(TeamSeasonRepository)
    fake_team_season_repository.add_team_season.assert_called_once_with(team_season)
    fake_flash.assert_called_once_with(str(err), 'danger')
    fake_render_template.assert_called_once_with(
        'team_seasons_admin/create.html', team_season=None, form=fake_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.team_season_admin_controller.copy')
@patch('app.flask.team_season_admin_controller.injector')
def test_edit_when_team_season_not_found_should_abort_with_404_error(fake_injector, fake_copy):
    # Arrange
    fake_team_season_repository = MagicMock(TeamSeasonRepository)
    old_team_season = TeamSeason()
    fake_team_season_repository.get_team_season.return_value = old_team_season
    fake_injector.get.return_value = fake_team_season_repository

    old_team_season_copy = None
    fake_copy.deepcopy.return_value = old_team_season_copy

    id = 1

    # Act
    with pytest.raises(NotFound):
        result = mod.edit(id)

    # Assert
    fake_injector.get.assert_called_once_with(TeamSeasonRepository)
    fake_team_season_repository.get_team_season.assert_called_once_with(id)
    fake_copy.deepcopy.assert_called_once_with(old_team_season)


@patch('app.flask.team_season_admin_controller.render_template')
@patch('app.flask.team_season_admin_controller.flash')
@patch('app.flask.team_season_admin_controller.EditTeamSeasonForm')
@patch('app.flask.team_season_admin_controller.copy')
@patch('app.flask.team_season_admin_controller.team_season_factory')
@patch('app.flask.team_season_admin_controller.injector')
def test_edit_when_team_season_found_and_form_not_submitted_and_no_form_errors_should_render_edit_template(
        fake_injector, fake_team_season_factory, fake_copy,
        fake_form, fake_flash, fake_render_template
):
    # Arrange
    fake_team_season_repository = MagicMock(TeamSeasonRepository)
    old_team_season = TeamSeason()
    fake_team_season_repository.get_team_season.return_value = old_team_season
    fake_injector.get.return_value = fake_team_season_repository

    new_team_season = TeamSeason(team_id=2, season_year=1921)
    fake_team_season_factory.create_team_season.return_value = new_team_season

    old_team_season_copy = TeamSeason(team_id=1, season_year=1920)
    old_team_season_copy.team = Team(id=1, name='Team 1')
    old_team_season_copy.season = Season(year=1920)
    old_team_season_copy.league = Association(id=1, short_name="L")
    old_team_season_copy.conference = Association(id=1, short_name="C")
    old_team_season_copy.division = Association(id=1, short_name="D")
    fake_copy.deepcopy.return_value = old_team_season_copy

    fake_form.return_value.validate_on_submit.return_value = False
    fake_form.return_value.errors = None

    id = 1

    # Act
    result = mod.edit(id)

    # Assert
    fake_injector.get.assert_called_once_with(TeamSeasonRepository)
    fake_team_season_repository.get_team_season.assert_called_once_with(id)
    fake_copy.deepcopy.assert_called_once_with(old_team_season)
    fake_form.assert_called_once()
    assert fake_form.return_value.team_name.data == old_team_season_copy.team.name
    assert fake_form.return_value.season_year.data == old_team_season_copy.season.year
    assert fake_form.return_value.league_name.data == old_team_season_copy.league.short_name
    assert fake_form.return_value.conference_name.data == old_team_season_copy.conference.short_name
    assert fake_form.return_value.division_name.data == old_team_season_copy.division.short_name
    fake_form.return_value.validate_on_submit.assert_called_once()
    fake_flash.assert_not_called()
    fake_render_template.assert_called_once_with(
        'team_seasons_admin/edit.html', team_season=old_team_season_copy, form=fake_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.team_season_admin_controller.render_template')
@patch('app.flask.team_season_admin_controller.flash')
@patch('app.flask.team_season_admin_controller.EditTeamSeasonForm')
@patch('app.flask.team_season_admin_controller.copy')
@patch('app.flask.team_season_admin_controller.team_season_factory')
@patch('app.flask.team_season_admin_controller.injector')
def test_edit_when_team_season_found_and_form_not_submitted_and_form_errors_should_flash_errors_and_render_edit_template(
        fake_injector, fake_team_season_factory, fake_copy,
        fake_form, fake_flash, fake_render_template
):
    # Arrange
    fake_team_season_repository = MagicMock(TeamSeasonRepository)
    old_team_season = TeamSeason()
    fake_team_season_repository.get_team_season.return_value = old_team_season
    fake_injector.get.return_value = fake_team_season_repository

    new_team_season = TeamSeason(team_id=2, season_year=1921)
    fake_team_season_factory.create_team_season.return_value = new_team_season

    old_team_season_copy = TeamSeason(team_id=1, season_year=1920)
    old_team_season_copy.team = Team(id=1, name='Team 1')
    old_team_season_copy.season = Season(year=1920)
    old_team_season_copy.league = Association(id=1, short_name="L")
    old_team_season_copy.conference = Association(id=1, short_name="C")
    old_team_season_copy.division = Association(id=1, short_name="D")
    fake_copy.deepcopy.return_value = old_team_season_copy

    fake_form.return_value.validate_on_submit.return_value = False
    errors = 'errors'
    fake_form.return_value.errors = errors

    id = 1

    # Act
    result = mod.edit(id)

    # Assert
    fake_injector.get.assert_called_once_with(TeamSeasonRepository)
    fake_team_season_repository.get_team_season.assert_called_once_with(id)
    fake_copy.deepcopy.assert_called_once_with(old_team_season)
    fake_form.assert_called_once()
    assert fake_form.return_value.team_name.data == old_team_season_copy.team.name
    assert fake_form.return_value.season_year.data == old_team_season_copy.season.year
    assert fake_form.return_value.league_name.data == old_team_season_copy.league.short_name
    assert fake_form.return_value.conference_name.data == old_team_season_copy.conference.short_name
    assert fake_form.return_value.division_name.data == old_team_season_copy.division.short_name
    fake_form.return_value.validate_on_submit.assert_called_once()
    fake_flash.assert_called_once_with(f"{errors}", 'danger')
    fake_render_template('team_seasons_admin/create.html', form=fake_form.return_value)
    assert result is fake_render_template.return_value


@patch('app.flask.team_season_admin_controller.redirect')
@patch('app.flask.team_season_admin_controller.url_for')
@patch('app.flask.team_season_admin_controller.flash')
@patch('app.flask.team_season_admin_controller.team_season_factory')
@patch('app.flask.team_season_admin_controller.EditTeamSeasonForm')
@patch('app.flask.team_season_admin_controller.copy')
@patch('app.flask.team_season_admin_controller.injector')
def test_edit_when_team_season_found_and_form_submitted_and_no_errors_caught_should_flash_success_message_and_redirect_to_team_season_details(
        fake_injector, fake_copy, fake_form,
        fake_team_season_factory, fake_flash,
        fake_url_for, fake_redirect
):
    # Arrange
    fake_team_season_repository = MagicMock(TeamSeasonRepository)
    old_team_season = TeamSeason()
    fake_team_season_repository.get_team_season.return_value = old_team_season
    fake_injector.get.return_value = fake_team_season_repository

    new_team_season = TeamSeason(team_id=2, season_year=1921)
    fake_team_season_factory.create_team_season.return_value = new_team_season

    old_team_season_copy = TeamSeason(team_id=1, season_year=1920)
    old_team_season_copy.team = Team(id=1, name='Team 1')
    old_team_season_copy.season = Season(year=1920)
    old_team_season_copy.league = Association(id=1, short_name="L1")
    old_team_season_copy.conference = Association(id=1, short_name="C1")
    old_team_season_copy.division = Association(id=1, short_name="D1")
    fake_copy.deepcopy.return_value = old_team_season_copy

    new_team_name = "Team 2"
    new_season_year = 1921
    new_league_name = "L2"
    new_conference_name = "C2"
    new_division_name = "Association 2"

    fake_form.return_value.validate_on_submit.return_value = True
    fake_form.return_value.team_name.data = new_team_name
    fake_form.return_value.season_year.data = new_season_year
    fake_form.return_value.league_name.data = new_league_name
    fake_form.return_value.conference_name.data = new_conference_name
    fake_form.return_value.division_name.data = new_division_name

    id = 1

    # Act
    result = mod.edit(id)

    # Assert
    fake_injector.get.assert_called_once_with(TeamSeasonRepository)
    fake_team_season_repository.get_team_season.assert_called_once_with(id)
    fake_copy.deepcopy.assert_called_once_with(old_team_season)
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    kwargs = {
        'id': id,
        'team_name': new_team_name,
        'season_year': new_season_year,
        'league_name': new_league_name,
        'conference_name': new_conference_name,
        'division_name': new_division_name,
    }
    fake_team_season_factory.create_team_season.assert_called_once_with(**kwargs)
    fake_team_season_repository.update_team_season.assert_called_once_with(new_team_season)
    fake_flash.assert_called_once_with(
        f"Item {new_team_name}, {new_season_year} has been successfully updated.", 'success'
    )
    fake_url_for.assert_called_once_with('team_season_admin.details', id=id)
    fake_redirect.assert_called_once_with(fake_url_for.return_value)
    assert result is fake_redirect.return_value


@patch('app.flask.team_season_admin_controller.render_template')
@patch('app.flask.team_season_admin_controller.flash')
@patch('app.flask.team_season_admin_controller.team_season_factory')
@patch('app.flask.team_season_admin_controller.EditTeamSeasonForm')
@patch('app.flask.team_season_admin_controller.copy')
@patch('app.flask.team_season_admin_controller.injector')
def test_edit_when_team_season_found_and_form_submitted_and_value_error_caught_should_flash_error_message_and_render_edit_template(
        fake_injector, fake_copy, fake_form,
        fake_team_season_factory, fake_flash,
        fake_render_template
):
    # Arrange
    fake_team_season_repository = MagicMock(TeamSeasonRepository)
    old_team_season = TeamSeason()
    fake_team_season_repository.get_team_season.return_value = old_team_season
    err = ValueError()
    fake_team_season_repository.update_team_season.side_effect = err
    fake_injector.get.return_value = fake_team_season_repository

    new_team_season = TeamSeason(team_id=2, season_year=1921)
    fake_team_season_factory.create_team_season.return_value = new_team_season

    old_team_season_copy = TeamSeason(team_id=1, season_year=1920)
    old_team_season_copy.team = Team(id=1, name='Team 1')
    old_team_season_copy.season = Season(year=1920)
    old_team_season_copy.league = Association(id=1, short_name="L1")
    old_team_season_copy.conference = Association(id=1, short_name="C1")
    old_team_season_copy.division = Association(id=1, short_name="D1")
    fake_copy.deepcopy.return_value = old_team_season_copy

    new_id = 2
    new_team_name = "Team 2"
    new_season_year = 1921
    new_league_name = "L2"
    new_conference_name = "C2"
    new_division_name = "Association 2"

    fake_form.return_value.validate_on_submit.return_value = True
    fake_form.return_value.team_name.data = new_team_name
    fake_form.return_value.season_year.data = new_season_year
    fake_form.return_value.league_name.data = new_league_name
    fake_form.return_value.conference_name.data = new_conference_name
    fake_form.return_value.division_name.data = new_division_name

    new_team_season = TeamSeason(
        team_id=new_id,
        season_year=new_season_year,
        league_id=new_id,
        conference_id=new_id,
        division_id=new_id
    )
    new_team_season.team = Team(id=new_id, name=new_team_name)
    new_team_season.season = Season(year=new_season_year)
    new_team_season.league = Association(id=new_id, short_name=new_league_name)
    new_team_season.conference = Association(id=new_id, short_name=new_conference_name)
    new_team_season.division = Association(id=new_id, short_name=new_division_name)
    fake_team_season_factory.create_team_season.return_value = new_team_season

    id = 1

    # Act
    result = mod.edit(id)

    # Assert
    fake_injector.get.assert_called_once_with(TeamSeasonRepository)
    fake_team_season_repository.get_team_season.assert_called_once_with(id)
    fake_copy.deepcopy.assert_called_once_with(old_team_season)
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    kwargs = {
        'id': id,
        'team_name': new_team_name,
        'season_year': new_season_year,
        'league_name': new_league_name,
        'conference_name': new_conference_name,
        'division_name': new_division_name,
    }
    fake_team_season_factory.create_team_season.assert_called_once_with(**kwargs)
    fake_team_season_repository.update_team_season.assert_called_once_with(new_team_season)
    fake_flash.assert_called_once_with(str(err), 'danger')
    fake_render_template.assert_called_once_with(
        'team_seasons_admin/edit.html', team_season=old_team_season_copy, form=fake_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.team_season_admin_controller.render_template')
@patch('app.flask.team_season_admin_controller.flash')
@patch('app.flask.team_season_admin_controller.team_season_factory')
@patch('app.flask.team_season_admin_controller.EditTeamSeasonForm')
@patch('app.flask.team_season_admin_controller.copy')
@patch('app.flask.team_season_admin_controller.injector')
def test_edit_when_team_season_found_and_form_submitted_and_integrity_error_caught_should_flash_error_message_and_render_edit_template(
        fake_injector, fake_copy, fake_form,
        fake_team_season_factory, fake_flash,
        fake_render_template
):
    # Arrange
    fake_team_season_repository = MagicMock(TeamSeasonRepository)
    old_team_season = TeamSeason()
    fake_team_season_repository.get_team_season.return_value = old_team_season
    err = IntegrityError('statement', 'params', Exception())
    fake_team_season_repository.update_team_season.side_effect = err
    fake_injector.get.return_value = fake_team_season_repository

    new_team_season = TeamSeason(team_id=2, season_year=1921)
    fake_team_season_factory.create_team_season.return_value = new_team_season

    old_team_season_copy = TeamSeason(team_id=1, season_year=1920)
    old_team_season_copy.team = Team(id=1, name='Team 1')
    old_team_season_copy.season = Season(year=1920)
    old_team_season_copy.league = Association(id=1, short_name="L1")
    old_team_season_copy.conference = Association(id=1, short_name="C1")
    old_team_season_copy.division = Association(id=1, short_name="D1")
    fake_copy.deepcopy.return_value = old_team_season_copy

    new_id = 2
    new_team_name = "Team 2"
    new_season_year = 1921
    new_league_name = "L2"
    new_conference_name = "C2"
    new_division_name = "Association 2"

    fake_form.return_value.validate_on_submit.return_value = True
    fake_form.return_value.team_name.data = new_team_name
    fake_form.return_value.season_year.data = new_season_year
    fake_form.return_value.league_name.data = new_league_name
    fake_form.return_value.conference_name.data = new_conference_name
    fake_form.return_value.division_name.data = new_division_name

    new_team_season = TeamSeason(
        team_id=new_id,
        season_year=new_season_year,
        league_id=new_id,
        conference_id=new_id,
        division_id=new_id
    )
    new_team_season.team = Team(id=new_id, name=new_team_name)
    new_team_season.season = Season(year=new_season_year)
    new_team_season.league = Association(id=new_id, short_name=new_league_name)
    new_team_season.conference = Association(id=new_id, short_name=new_conference_name)
    new_team_season.division = Association(id=new_id, short_name=new_division_name)
    fake_team_season_factory.create_team_season.return_value = new_team_season

    id = 1

    # Act
    result = mod.edit(id)

    # Assert
    fake_injector.get.assert_called_once_with(TeamSeasonRepository)
    fake_team_season_repository.get_team_season.assert_called_once_with(id)
    fake_copy.deepcopy.assert_called_once_with(old_team_season)
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    kwargs = {
        'id': id,
        'team_name': new_team_name,
        'season_year': new_season_year,
        'league_name': new_league_name,
        'conference_name': new_conference_name,
        'division_name': new_division_name,
    }
    fake_team_season_factory.create_team_season.assert_called_once_with(**kwargs)
    fake_team_season_repository.update_team_season.assert_called_once_with(new_team_season)
    fake_flash.assert_called_once_with(str(err), 'danger')
    fake_render_template.assert_called_once_with(
        'team_seasons_admin/edit.html', team_season=old_team_season_copy, form=fake_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.team_season_admin_controller.flash')
@patch('app.flask.team_season_admin_controller.team_season_factory')
@patch('app.flask.team_season_admin_controller.EditTeamSeasonForm')
@patch('app.flask.team_season_admin_controller.copy')
@patch('app.flask.team_season_admin_controller.injector')
def test_edit_when_team_season_found_and_form_submitted_and_index_error_caught_should_abort_with_404_error(
        fake_injector, fake_copy, fake_form,
        fake_team_season_factory, fake_flash
):
    # Arrange
    fake_team_season_repository = MagicMock(TeamSeasonRepository)
    old_team_season = TeamSeason()
    fake_team_season_repository.get_team_season.return_value = old_team_season
    err = IndexError()
    fake_team_season_repository.update_team_season.side_effect = err
    fake_injector.get.return_value = fake_team_season_repository

    new_team_season = TeamSeason(team_id=2, season_year=1921)
    fake_team_season_factory.create_team_season.return_value = new_team_season

    old_team_season_copy = TeamSeason(team_id=1, season_year=1920)
    old_team_season_copy.team = Team(id=1, name='Team 1')
    old_team_season_copy.season = Season(year=1920)
    old_team_season_copy.league = Association(id=1, short_name="L1")
    old_team_season_copy.conference = Association(id=1, short_name="C1")
    old_team_season_copy.division = Association(id=1, short_name="D1")
    fake_copy.deepcopy.return_value = old_team_season_copy

    new_id = 2
    new_team_name = "Team 2"
    new_season_year = 1921
    new_league_name = "L2"
    new_conference_name = "C2"
    new_division_name = "Association 2"

    fake_form.return_value.validate_on_submit.return_value = True
    fake_form.return_value.team_name.data = new_team_name
    fake_form.return_value.season_year.data = new_season_year
    fake_form.return_value.league_name.data = new_league_name
    fake_form.return_value.conference_name.data = new_conference_name
    fake_form.return_value.division_name.data = new_division_name

    new_team_season = TeamSeason(
        team_id=new_id,
        season_year=new_season_year,
        league_id=new_id,
        conference_id=new_id,
        division_id=new_id
    )
    new_team_season.team = Team(id=new_id, name=new_team_name)
    new_team_season.season = Season(year=new_season_year)
    new_team_season.league = Association(id=new_id, short_name=new_league_name)
    new_team_season.conference = Association(id=new_id, short_name=new_conference_name)
    new_team_season.division = Association(id=new_id, short_name=new_division_name)
    fake_team_season_factory.create_team_season.return_value = new_team_season

    id = 1

    # Act
    with pytest.raises(NotFound):
        _ = mod.edit(id)

    # Assert
    fake_injector.get.assert_called_once_with(TeamSeasonRepository)
    fake_team_season_repository.get_team_season.assert_called_once_with(id)
    fake_copy.deepcopy.assert_called_once_with(old_team_season)
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    kwargs = {
        'id': id,
        'team_name': new_team_name,
        'season_year': new_season_year,
        'league_name': new_league_name,
        'conference_name': new_conference_name,
        'division_name': new_division_name,
    }
    fake_team_season_factory.create_team_season.assert_called_once_with(**kwargs)
    fake_team_season_repository.update_team_season.assert_called_once_with(new_team_season)


@patch('app.flask.team_season_admin_controller.injector')
@patch('app.flask.team_season_admin_controller.DeleteTeamSeasonForm')
def test_delete_when_team_season_not_found_should_abort_with_404_error(
        fake_form, fake_injector, test_app
):
    # Arrange
    fake_team_season_repository = MagicMock(TeamSeasonRepository)
    fake_team_season_repository.get_team_season.return_value = None
    fake_injector.get.return_value = fake_team_season_repository

    id = 1

    # Act
    with test_app.test_request_context(
            f'/team_seasons_admin/delete?id={id}',
            method='GET'
    ):
        with pytest.raises(NotFound):
            _ = mod.delete(id)

    # Assert
    fake_form.assert_called_once()
    fake_injector.get.assert_called_once_with(TeamSeasonRepository)
    fake_team_season_repository.get_team_season.assert_called_once_with(id)


@patch('app.flask.team_season_admin_controller.render_template')
@patch('app.flask.team_season_admin_controller.injector')
@patch('app.flask.team_season_admin_controller.DeleteTeamSeasonForm')
def test_delete_when_request_method_is_get_should_render_delete_template(
        fake_form, fake_injector, fake_render_template, test_app
):
    # Arrange
    fake_team_season_repository = MagicMock(TeamSeasonRepository)
    team_season = TeamSeason()
    fake_team_season_repository.get_team_season.return_value = team_season
    fake_injector.get.return_value = fake_team_season_repository

    id = 1

    # Act
    with test_app.test_request_context(
            f'/team_seasons_admin/delete?id={id}',
            method='GET'
    ):
        result = mod.delete(id)

    # Assert
    fake_form.assert_called_once()
    fake_injector.get.assert_called_once_with(TeamSeasonRepository)
    fake_team_season_repository.get_team_season.assert_called_once_with(id)
    fake_render_template.assert_called_once_with(
        'team_seasons_admin/delete.html', team_season=team_season, form=fake_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.team_season_admin_controller.redirect')
@patch('app.flask.team_season_admin_controller.url_for')
@patch('app.flask.team_season_admin_controller.flash')
@patch('app.flask.team_season_admin_controller.injector')
@patch('app.flask.team_season_admin_controller.DeleteTeamSeasonForm')
def test_delete_when_request_method_is_post_and_team_season_found_should_flash_success_message_and_redirect_to_team_seasons_index(
        fake_form, fake_injector, fake_flash,
        fake_url_for, fake_redirect, test_app
):
    # Arrange
    fake_team_season_repository = MagicMock(TeamSeasonRepository)
    team_season = TeamSeason(team_id=1, season_year=1920, league_id=1, conference_id=2, division_id=3)
    team_season.team = Team(id=1, name="Team")
    team_season.season = Season(year=1920)
    team_season.league = Association(id=1, long_name="League", short_name="L")
    team_season.conference = Association(id=2, long_name="Conference", short_name="C")
    team_season.division = Association(id=3, long_name="Division", short_name="D")
    fake_team_season_repository.get_team_season.return_value = team_season
    fake_injector.get.return_value = fake_team_season_repository

    id = 1

    # Act
    with test_app.test_request_context(
            f'/team_seasons_admin/delete?id={id}',
            method='POST'
    ):
        result = mod.delete(id)

    # Assert
    fake_form.assert_called_once()
    fake_injector.get.assert_called_once_with(TeamSeasonRepository)
    fake_team_season_repository.get_team_season.assert_called_once_with(id)
    fake_team_season_repository.delete_team_season.assert_called_once_with(id)
    fake_flash.assert_called_once_with(
        f"TeamSeason {team_season.team.name}. {team_season.season.year} has been successfully deleted.",
        'success'
    )
    fake_url_for.assert_called_once_with('team_season_admin.index')
    fake_redirect.assert_called_once_with(fake_url_for.return_value)
    assert result is fake_redirect.return_value


@patch('app.flask.team_season_admin_controller.injector')
def test_delete_when_request_method_is_post_and_index_error_is_caught_should_abort_with_404_error(
        fake_injector, test_app
):
    # Arrange
    fake_team_season_repository = MagicMock(TeamSeasonRepository)
    team_season = TeamSeason()
    fake_team_season_repository.get_team_season.return_value = team_season
    fake_team_season_repository.delete_team_season.side_effect = IndexError()
    fake_injector.get.return_value = fake_team_season_repository

    id = 1

    # Act
    with test_app.test_request_context(
            f'/team_seasons_admin/delete?id={id}',
            method='POST'
    ):
        with pytest.raises(NotFound):
            _ = mod.delete(id)

    # Assert
    fake_injector.get.assert_called_once_with(TeamSeasonRepository)
    fake_team_season_repository.get_team_season.assert_called_once_with(id)
