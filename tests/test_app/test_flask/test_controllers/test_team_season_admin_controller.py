from typing import Optional
from unittest.mock import patch, MagicMock

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
    fake_team_season_repository = _set_up_index_and_details(fake_injector)

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
    fake_team_season_repository = _set_up_index_and_details(fake_injector)

    # Act
    id = 1
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
    err = IndexError()
    _ = _set_up_index_and_details(fake_injector, err=err)

    # Act
    with pytest.raises(NotFound):
        _ = mod.details(1)


def _set_up_index_and_details(fake_injector, err: Optional[Exception] = None) -> MagicMock:
    fake_team_season_repository = MagicMock(TeamSeasonRepository)
    fake_team_season_repository.get_team_season.side_effect = err
    fake_injector.get.return_value = fake_team_season_repository

    return fake_team_season_repository


@patch('app.flask.team_season_admin_controller.render_template')
@patch('app.flask.team_season_admin_controller.flash')
@patch('app.flask.team_season_admin_controller.NewTeamSeasonForm')
def test_create_when_form_not_submitted_and_no_form_errors_should_render_create_template(
        fake_form, fake_flash, fake_render_template
):
    # Arrange
    _set_up_create_get(fake_form)

    # Act
    result = mod.create()

    # Assert
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    fake_flash.assert_not_called()
    fake_render_template('team_seasons_admin/create.html', form=fake_form.return_value)
    assert result is fake_render_template.return_value


@patch('app.flask.team_season_admin_controller.render_template')
@patch('app.flask.team_season_admin_controller.flash')
@patch('app.flask.team_season_admin_controller.NewTeamSeasonForm')
def test_create_when_form_not_submitted_and_form_errors_should_flash_errors_and_render_create_template(
        fake_form, fake_flash, fake_render_template
):
    # Arrange
    errors = 'errors'
    _set_up_create_get(fake_form, errors=errors)

    # Act
    result = mod.create()

    # Assert
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    fake_flash.assert_called_once_with(f"{errors}", 'danger')
    fake_render_template('team_seasons_admin/create.html', form=fake_form.return_value)
    assert result is fake_render_template.return_value


def _set_up_create_get(fake_form, errors: Optional[str] = None) -> None:
    form = fake_form.return_value
    form.validate_on_submit.return_value = False
    form.errors = errors


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
    team_season, fake_team_season_repository = _set_up_create_post(fake_injector, fake_form, fake_team_season_factory)

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
    err = ValueError()
    team_season, fake_team_season_repository = (
        _set_up_create_post(fake_injector, fake_form, fake_team_season_factory, err=err)
    )

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
    err = IntegrityError('statement', 'params', Exception())
    team_season, fake_team_season_repository = (
        _set_up_create_post(fake_injector, fake_form, fake_team_season_factory, err=err)
    )

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


def _set_up_create_post(
        fake_injector, fake_form, fake_team_season_factory,
        err: Optional[Exception] = None
) -> tuple[TeamSeason, MagicMock]:
    team_season = TeamSeason(
        team_id=1,
        team=Team(id=1, name="Team"),
        season_year=1920,
        season=Season(year=1920),
        league_id=1,
        league=Association(id=1, long_name="League", short_name="L"),
        conference_id=2,
        conference=Association(id=2, long_name="Conference", short_name="C"),
        division_id=3,
        division=Association(id=3, long_name="Division", short_name="D")
    )

    form = fake_form.return_value
    form.validate_on_submit.return_value = True
    form.team_name.data = team_season.team.name
    form.season_year.data = team_season.season.year
    form.league_name.data = team_season.league.short_name
    form.conference_name.data = team_season.conference.short_name
    form.division_name.data = team_season.division.short_name

    fake_team_season_factory.create_team_season.return_value = team_season

    fake_team_season_repository = MagicMock(TeamSeasonRepository)
    fake_team_season_repository.add_team_season.side_effect = err
    fake_injector.get.return_value = fake_team_season_repository

    return team_season, fake_team_season_repository


@patch('app.flask.team_season_admin_controller.copy')
@patch('app.flask.team_season_admin_controller.injector')
def test_edit_when_team_season_not_found_should_abort_with_404_error(fake_injector, fake_copy):
    # Arrange
    old_team_season_copy = None
    old_team_season, fake_team_season_repository = (
        _set_up_edit(fake_injector, fake_copy, old_team_season_copy=old_team_season_copy)
    )

    # Act
    id = 1
    with pytest.raises(NotFound):
        _ = mod.edit(id)

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
    old_team_season, old_team_season_copy, fake_team_season_repository = (
        _set_up_edit_get(fake_injector, fake_copy, fake_form)
    )

    # Act
    id = 1
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
    errors = 'errors'
    old_team_season, old_team_season_copy, fake_team_season_repository = (
        _set_up_edit_get(fake_injector, fake_copy, fake_form, errors=errors)
    )

    # Act
    id = 1
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


def _set_up_edit_get(
        fake_injector, fake_copy, fake_form,
        errors: Optional[str] = None
) -> tuple[MagicMock, TeamSeason, TeamSeason]:
    old_team_season_copy = TeamSeason(
        team_id=1,
        team=Team(id=1, name='Team 1'),
        season_year=1920,
        season=Season(year=1920),
        league_id=1,
        league=Association(id=1, long_name="League", short_name="L"),
        conference_id=2,
        conference=Association(id=2, long_name="Conference", short_name="C"),
        division_id=3,
        division=Association(id=3, long_name="Division", short_name="D")
    )
    old_team_season, fake_team_season_repository = (
        _set_up_edit(
            fake_injector, fake_copy, old_team_season_copy=old_team_season_copy
        )
    )

    fake_form.return_value.validate_on_submit.return_value = False
    fake_form.return_value.errors = errors
    return old_team_season, old_team_season_copy, fake_team_season_repository


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
    old_team_season, old_team_season_copy, new_team_season, fake_team_season_repository = (
        _set_up_edit_post(fake_injector, fake_copy, fake_form, fake_team_season_factory)
    )

    # Act
    id = 1
    result = mod.edit(id)

    # Assert
    fake_injector.get.assert_called_once_with(TeamSeasonRepository)
    fake_team_season_repository.get_team_season.assert_called_once_with(id)
    fake_copy.deepcopy.assert_called_once_with(old_team_season)
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    kwargs = {
        'id': id,
        'team_name': new_team_season.team.name,
        'season_year': new_team_season.season.year,
        'league_name': new_team_season.league.short_name,
        'conference_name': new_team_season.conference.short_name,
        'division_name': new_team_season.division.short_name,
    }
    fake_team_season_factory.create_team_season.assert_called_once_with(**kwargs)
    fake_team_season_repository.update_team_season.assert_called_once_with(new_team_season)
    fake_flash.assert_called_once_with(
        f"Item {new_team_season.team.name}, {new_team_season.season.year} has been successfully updated.", 'success'
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
    err = ValueError()
    old_team_season, old_team_season_copy, new_team_season, fake_team_season_repository = (
        _set_up_edit_post(fake_injector, fake_copy, fake_form, fake_team_season_factory, err=err)
    )

    # Act
    id = 1
    result = mod.edit(id)

    # Assert
    fake_injector.get.assert_called_once_with(TeamSeasonRepository)
    fake_team_season_repository.get_team_season.assert_called_once_with(id)
    fake_copy.deepcopy.assert_called_once_with(old_team_season)
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    kwargs = {
        'id': id,
        'team_name': new_team_season.team.name,
        'season_year': new_team_season.season.year,
        'league_name': new_team_season.league.short_name,
        'conference_name': new_team_season.conference.short_name,
        'division_name': new_team_season.division.short_name,
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
    err = IntegrityError('statement', 'params', Exception())
    old_team_season, old_team_season_copy, new_team_season, fake_team_season_repository = (
        _set_up_edit_post(fake_injector, fake_copy, fake_form, fake_team_season_factory, err=err)
    )

    # Act
    id = 1
    result = mod.edit(id)

    # Assert
    fake_injector.get.assert_called_once_with(TeamSeasonRepository)
    fake_team_season_repository.get_team_season.assert_called_once_with(id)
    fake_copy.deepcopy.assert_called_once_with(old_team_season)
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    kwargs = {
        'id': id,
        'team_name': new_team_season.team.name,
        'season_year': new_team_season.season.year,
        'league_name': new_team_season.league.short_name,
        'conference_name': new_team_season.conference.short_name,
        'division_name': new_team_season.division.short_name,
    }
    fake_team_season_factory.create_team_season.assert_called_once_with(**kwargs)
    fake_team_season_repository.update_team_season.assert_called_once_with(new_team_season)
    fake_flash.assert_called_once_with(str(err), 'danger')
    fake_render_template.assert_called_once_with(
        'team_seasons_admin/edit.html', team_season=old_team_season_copy, form=fake_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.team_season_admin_controller.team_season_factory')
@patch('app.flask.team_season_admin_controller.EditTeamSeasonForm')
@patch('app.flask.team_season_admin_controller.copy')
@patch('app.flask.team_season_admin_controller.injector')
def test_edit_when_team_season_found_and_form_submitted_and_index_error_caught_should_abort_with_404_error(
        fake_injector, fake_copy, fake_form,
        fake_team_season_factory
):
    # Arrange
    err = IndexError()
    old_team_season, old_team_season_copy, new_team_season, fake_team_season_repository = (
        _set_up_edit_post(fake_injector, fake_copy, fake_form, fake_team_season_factory, err=err)
    )

    # Act
    id = 1
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
        'team_name': new_team_season.team.name,
        'season_year': new_team_season.season.year,
        'league_name': new_team_season.league.short_name,
        'conference_name': new_team_season.conference.short_name,
        'division_name': new_team_season.division.short_name,
    }
    fake_team_season_factory.create_team_season.assert_called_once_with(**kwargs)
    fake_team_season_repository.update_team_season.assert_called_once_with(new_team_season)


def _set_up_edit_post(
        fake_injector, fake_copy, fake_form, fake_team_season_factory,
        err: Optional[Exception] = None
) -> tuple[TeamSeason, TeamSeason, TeamSeason, MagicMock]:
    old_team_season_copy = TeamSeason(
        team_id=1,
        team=Team(id=1, name='Team 1'),
        season_year=1920,
        season=Season(year=1920),
        league_id=1,
        league=Association(id=1, long_name="League", short_name="L"),
        conference_id=2,
        conference=Association(id=2, long_name="Conference", short_name="C"),
        division_id=3,
        division=Association(id=3, long_name="Division", short_name="D")
    )
    old_team_season, fake_team_season_repository = (
        _set_up_edit(fake_injector, fake_copy, old_team_season_copy=old_team_season_copy, err=err)
    )

    new_id = 2
    new_season_year = 1921

    new_team_season = TeamSeason(
        team_id=new_id,
        team=Team(id=new_id, name="Team 2"),
        season_year=new_season_year,
        season=Season(year=new_season_year),
        league_id=new_id,
        league=Association(id=new_id, short_name="L2"),
        conference_id=new_id,
        conference=Association(id=new_id, short_name="C2"),
        division_id=new_id,
        division=Association(id=new_id, short_name="D2")
    )

    form = fake_form.return_value
    form.team_name.data = new_team_season.team.name
    form.season_year.data = new_team_season.season.year
    form.league_name.data = new_team_season.league.short_name
    form.conference_name.data = new_team_season.conference.short_name
    form.division_name.data = new_team_season.division.short_name
    form.validate_on_submit.return_value = True

    fake_team_season_factory.create_team_season.return_value = new_team_season

    return old_team_season, old_team_season_copy, new_team_season, fake_team_season_repository


@patch('app.flask.team_season_admin_controller.injector')
@patch('app.flask.team_season_admin_controller.DeleteTeamSeasonForm')
def test_delete_when_team_season_not_found_should_abort_with_404_error(
        fake_form, fake_injector, test_app
):
    # Arrange
    fake_team_season_repository = _set_up_delete(fake_injector)

    # Act
    id = 1
    with test_app.test_request_context(f'/team_seasons_admin/delete?id={id}', method='GET'):
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
    team_season = TeamSeason()
    fake_team_season_repository = _set_up_delete(fake_injector, team_season=team_season)

    # Act
    id = 1
    with test_app.test_request_context(f'/team_seasons_admin/delete?id={id}', method='GET'):
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
    id = 1
    team_season = TeamSeason(
        id=id,
        team_id=1,
        team=Team(id=1, name="Team"),
        season_year=1920,
        season=Season(year=1920),
        league_id=1,
        league=Association(id=1, long_name="League", short_name="L"),
        conference_id=2,
        conference=Association(id=2, long_name="Conference", short_name="C"),
        division_id=3,
        division=Association(id=3, long_name="Division", short_name="D")
    )
    fake_team_season_repository = _set_up_delete(fake_injector, team_season)

    # Act
    with test_app.test_request_context(f'/team_seasons_admin/delete?id={id}', method='POST'):
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
    team_season = TeamSeason()
    err = IndexError()
    fake_team_season_repository = _set_up_delete(fake_injector, team_season, err=err)

    # Act
    id = 1
    with test_app.test_request_context(f'/team_seasons_admin/delete?id={id}', method='POST'):
        with pytest.raises(NotFound):
            _ = mod.delete(id)

    # Assert
    fake_injector.get.assert_called_once_with(TeamSeasonRepository)
    fake_team_season_repository.get_team_season.assert_called_once_with(id)


def _set_up_delete(fake_injector, team_season: Optional[TeamSeason] = None, err: Optional[Exception] = None) \
        -> MagicMock:
    fake_team_season_repository = MagicMock(TeamSeasonRepository)
    fake_team_season_repository.get_team_season.return_value = team_season
    fake_team_season_repository.delete_team_season.side_effect = err
    fake_injector.get.return_value = fake_team_season_repository
    
    return fake_team_season_repository


def _set_up_edit(fake_injector, fake_copy, old_team_season_copy, err: Optional[Exception] = None) \
        -> tuple[TeamSeason, MagicMock]:
    fake_team_season_repository = MagicMock(TeamSeasonRepository)
    old_team_season = TeamSeason()
    fake_team_season_repository.get_team_season.return_value = old_team_season
    fake_team_season_repository.update_team_season.side_effect = err
    fake_injector.get.return_value = fake_team_season_repository

    fake_copy.deepcopy.return_value = old_team_season_copy

    return old_team_season, fake_team_season_repository
