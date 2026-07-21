from unittest.mock import patch, MagicMock

import pytest

from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound

import app.flask.league_season_controller as mod
from app.data.models.association import Association
from app.data.models.league_season import LeagueSeason
from app.data.models.season import Season
from app.data.repositories.league_season_repository import LeagueSeasonRepository
from test_app import create_app


@pytest.fixture()
def test_app():
    return create_app()


@patch('app.flask.league_season_controller.render_template')
@patch('app.flask.league_season_controller.injector')
def test_index_should_render_league_season_index_template(
        fake_injector, fake_render_template
):
    # Arrange
    fake_league_season_repository = MagicMock(LeagueSeasonRepository)
    fake_injector.get.return_value = fake_league_season_repository

    # Act
    result = mod.index()

    # Assert
    fake_injector.get.assert_called_once_with(LeagueSeasonRepository)
    fake_league_season_repository.get_league_seasons.assert_called_once()
    fake_render_template.assert_called_once_with(
        'league_seasons/index.html', league_seasons=fake_league_season_repository.get_league_seasons.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.league_season_controller.render_template')
@patch('app.flask.league_season_controller.injector')
@patch('app.flask.league_season_controller.DeleteLeagueSeasonForm')
def test_details_when_league_season_found_should_render_league_season_details_template(
        fake_form, fake_injector, fake_render_template
):
    # Arrange
    fake_league_season_repository = MagicMock(LeagueSeasonRepository)
    fake_injector.get.return_value = fake_league_season_repository

    # Act
    id = 1
    result = mod.details(id)

    # Assert
    fake_form.assert_called_once()
    fake_injector.get.assert_called_once_with(LeagueSeasonRepository)
    fake_league_season_repository.get_league_season.assert_called_once_with(id)
    fake_render_template.assert_called_once_with(
        'league_seasons/details.html',
        league_season=fake_league_season_repository.get_league_season.return_value,
        form=fake_form.return_value
    )
    assert result == fake_render_template.return_value


@patch('app.flask.league_season_controller.injector')
@patch('app.flask.league_season_controller.DeleteLeagueSeasonForm')
def test_details_when_league_season_not_found_should_abort_with_404_error(fake_form, fake_injector):
    # Arrange
    fake_league_season_repository = MagicMock(LeagueSeasonRepository)
    fake_league_season_repository.get_league_season.side_effect = IndexError()
    fake_injector.get.return_value = fake_league_season_repository

    # Act
    with pytest.raises(NotFound):
        result = mod.details(1)


@patch('app.flask.league_season_controller.render_template')
@patch('app.flask.league_season_controller.flash')
@patch('app.flask.league_season_controller.injector')
@patch('app.flask.league_season_controller.NewLeagueSeasonForm')
def test_create_when_form_not_submitted_and_no_form_errors_should_render_create_template(
        fake_form, fake_injector, fake_flash, fake_render_template
):
    # Arrange
    fake_form.return_value.validate_on_submit.return_value = False
    fake_form.return_value.errors = None

    fake_league_season_repository = MagicMock(LeagueSeasonRepository)
    fake_injector.get.return_value = fake_league_season_repository

    # Act
    result = mod.create()

    # Assert
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    fake_injector.get.assert_not_called()
    fake_league_season_repository.add_league_season.assert_not_called()
    fake_flash.assert_not_called()
    fake_render_template.assert_called_once_with('league_seasons/create.html', form=fake_form.return_value)
    assert result is fake_render_template.return_value


@patch('app.flask.league_season_controller.render_template')
@patch('app.flask.league_season_controller.flash')
@patch('app.flask.league_season_controller.injector')
@patch('app.flask.league_season_controller.NewLeagueSeasonForm')
def test_create_when_form_not_submitted_and_form_errors_should_flash_errors_and_render_create_template(
        fake_form, fake_injector, fake_flash, fake_render_template
):
    # Arrange
    fake_form.return_value.validate_on_submit.return_value = False

    errors = 'errors'
    fake_form.return_value.errors = errors

    fake_league_season_repository = MagicMock(LeagueSeasonRepository)
    fake_injector.get.return_value = fake_league_season_repository

    # Act
    result = mod.create()

    # Assert
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    fake_injector.get.assert_not_called()
    fake_league_season_repository.add_league_season.assert_not_called()
    fake_flash.assert_called_once_with(f"{errors}", 'danger')
    fake_render_template.assert_called_once_with('league_seasons/create.html', form=fake_form.return_value)
    assert result is fake_render_template.return_value


@patch('app.flask.league_season_controller.redirect')
@patch('app.flask.league_season_controller.url_for')
@patch('app.flask.league_season_controller.flash')
@patch('app.flask.league_season_controller.injector')
@patch('app.flask.league_season_controller.league_season_factory')
@patch('app.flask.league_season_controller.NewLeagueSeasonForm')
def test_create_when_form_submitted_and_no_errors_caught_should_flash_success_message_and_redirect_to_league_season_index(
        fake_form, fake_league_season_factory, fake_injector, fake_flash,
        fake_url_for, fake_redirect
):
    # Arrange
    league_season = LeagueSeason(league_id=1, season_year=1920, num_of_weeks_scheduled=13, num_of_weeks_completed=0)
    league_season.league = Association(id=1, long_name="Association", short_name="A")
    league_season.season = Season(year=1920)

    fake_form.return_value.validate_on_submit.return_value = True
    fake_form.return_value.league_name.data = league_season.league.short_name
    fake_form.return_value.season_year.data = league_season.season.year
    fake_form.return_value.num_of_weeks_scheduled.data = league_season.num_of_weeks_scheduled
    fake_form.return_value.num_of_weeks_completed.data = league_season.num_of_weeks_completed

    fake_league_season_factory.create_league_season.return_value = league_season

    fake_league_season_repository = MagicMock(LeagueSeasonRepository)
    fake_injector.get.return_value = fake_league_season_repository

    # Act
    result = mod.create()

    # Assert
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    view_kwargs = {
        'league_name': league_season.league.short_name,
        'season_year': league_season.season.year,
        'num_of_weeks_scheduled': league_season.num_of_weeks_scheduled,
        'num_of_weeks_completed': league_season.num_of_weeks_completed,
    }
    fake_league_season_factory.create_league_season.assert_called_once_with(**view_kwargs)
    fake_injector.get.assert_called_once_with(LeagueSeasonRepository)
    fake_league_season_repository.add_league_season.assert_called_once_with(league_season)
    fake_flash(f"Item {league_season.league.short_name}, {league_season.season.year} has been successfully submitted.", 'success')
    fake_url_for.assert_called_once_with('league_season.index')
    fake_redirect.assert_called_once_with(fake_url_for.return_value)
    assert result is fake_redirect.return_value


@patch('app.flask.league_season_controller.render_template')
@patch('app.flask.league_season_controller.flash')
@patch('app.flask.league_season_controller.injector')
@patch('app.flask.league_season_controller.league_season_factory')
@patch('app.flask.league_season_controller.NewLeagueSeasonForm')
def test_create_when_form_submitted_and_value_error_caught_should_flash_error_message_and_render_create_template(
        fake_form, fake_league_season_factory, fake_injector, 
        fake_flash, fake_render_template
):
    # Arrange
    league_season = LeagueSeason(league_id=1, season_year=1920, num_of_weeks_scheduled=13, num_of_weeks_completed=0)
    league_season.league = Association(id=1, long_name="Association", short_name="A")
    league_season.season = Season(year=1920)

    fake_form.return_value.validate_on_submit.return_value = True
    fake_form.return_value.league_name.data = league_season.league.short_name
    fake_form.return_value.season_year.data = league_season.season.year
    fake_form.return_value.num_of_weeks_scheduled.data = league_season.num_of_weeks_scheduled
    fake_form.return_value.num_of_weeks_completed.data = league_season.num_of_weeks_completed

    fake_league_season_factory.create_league_season.return_value = league_season

    fake_league_season_repository = MagicMock(LeagueSeasonRepository)
    err = ValueError()
    fake_league_season_repository.add_league_season.side_effect = err
    fake_injector.get.return_value = fake_league_season_repository

    # Act
    result = mod.create()

    # Assert
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    view_kwargs = {
        'league_name': league_season.league.short_name,
        'season_year': league_season.season.year,
        'num_of_weeks_scheduled': league_season.num_of_weeks_scheduled,
        'num_of_weeks_completed': league_season.num_of_weeks_completed,
    }
    fake_league_season_factory.create_league_season.assert_called_once_with(**view_kwargs)
    fake_injector.get.assert_called_once_with(LeagueSeasonRepository)
    fake_league_season_repository.add_league_season.assert_called_once_with(league_season)
    fake_flash.assert_called_once_with(str(err), 'danger')
    fake_render_template.assert_called_once_with(
        'league_seasons/create.html', league_season=None, form=fake_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.league_season_controller.render_template')
@patch('app.flask.league_season_controller.flash')
@patch('app.flask.league_season_controller.injector')
@patch('app.flask.league_season_controller.league_season_factory')
@patch('app.flask.league_season_controller.NewLeagueSeasonForm')
def test_create_when_form_submitted_and_integrity_error_caught_for_primary_key_constraint_violation_should_flash_error_message_and_render_create_template(
        fake_form, fake_league_season_factory, fake_injector,
        fake_flash, fake_render_template
):
    # Arrange
    league_season = LeagueSeason(league_id=1, season_year=1920, num_of_weeks_scheduled=13, num_of_weeks_completed=0)
    league_season.league = Association(id=1, long_name="Association", short_name="A")
    league_season.season = Season(year=1920)

    fake_form.return_value.validate_on_submit.return_value = True
    fake_form.return_value.league_name.data = league_season.league.short_name
    fake_form.return_value.season_year.data = league_season.season.year
    fake_form.return_value.num_of_weeks_scheduled.data = league_season.num_of_weeks_scheduled
    fake_form.return_value.num_of_weeks_completed.data = league_season.num_of_weeks_completed

    fake_league_season_factory.create_league_season.return_value = league_season

    fake_league_season_repository = MagicMock(LeagueSeasonRepository)
    err = IntegrityError(
        'statement', 'params',
        Exception("Violation of PRIMARY KEY constraint")
    )
    fake_league_season_repository.add_league_season.side_effect = err
    fake_injector.get.return_value = fake_league_season_repository

    # Act
    result = mod.create()

    # Assert
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    view_kwargs = {
        'league_name': league_season.league.short_name,
        'season_year': league_season.season.year,
        'num_of_weeks_scheduled': league_season.num_of_weeks_scheduled,
        'num_of_weeks_completed': league_season.num_of_weeks_completed,
    }
    fake_league_season_factory.create_league_season.assert_called_once_with(**view_kwargs)
    fake_injector.get.assert_called_once_with(LeagueSeasonRepository)
    fake_league_season_repository.add_league_season.assert_called_once_with(league_season)
    fake_flash.assert_called_once_with("A LeagueSeason with the same id already exists.", 'danger')
    fake_render_template.assert_called_once_with(
        'league_seasons/create.html', league_season=None, form=fake_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.league_season_controller.render_template')
@patch('app.flask.league_season_controller.flash')
@patch('app.flask.league_season_controller.injector')
@patch('app.flask.league_season_controller.league_season_factory')
@patch('app.flask.league_season_controller.NewLeagueSeasonForm')
def test_create_when_form_submitted_and_integrity_error_caught_for_unique_key_constraint_violation_should_flash_error_message_and_render_create_template(
        fake_form, fake_league_season_factory, fake_injector,
        fake_flash, fake_render_template
):
    # Arrange
    league_season = LeagueSeason(league_id=1, season_year=1920, num_of_weeks_scheduled=13, num_of_weeks_completed=0)
    league_season.league = Association(id=1, long_name="Association", short_name="A")
    league_season.season = Season(year=1920)

    fake_form.return_value.validate_on_submit.return_value = True
    fake_form.return_value.league_name.data = league_season.league.short_name
    fake_form.return_value.season_year.data = league_season.season.year
    fake_form.return_value.num_of_weeks_scheduled.data = league_season.num_of_weeks_scheduled
    fake_form.return_value.num_of_weeks_completed.data = league_season.num_of_weeks_completed

    fake_league_season_factory.create_league_season.return_value = league_season

    fake_league_season_repository = MagicMock(LeagueSeasonRepository)
    err = IntegrityError(
        'statement', 'params',
        Exception("Violation of UNIQUE KEY constraint 'UQ_LeagueSeason_League_Season'")
    )
    fake_league_season_repository.add_league_season.side_effect = err
    fake_injector.get.return_value = fake_league_season_repository

    # Act
    result = mod.create()

    # Assert
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    view_kwargs = {
        'league_name': league_season.league.short_name,
        'season_year': league_season.season.year,
        'num_of_weeks_scheduled': league_season.num_of_weeks_scheduled,
        'num_of_weeks_completed': league_season.num_of_weeks_completed,
    }
    fake_league_season_factory.create_league_season.assert_called_once_with(**view_kwargs)
    fake_injector.get.assert_called_once_with(LeagueSeasonRepository)
    fake_league_season_repository.add_league_season.assert_called_once_with(league_season)
    fake_flash.assert_called_once_with(
        "A LeagueSeason with the same league_id and season_year already exists.", 'danger'
    )
    fake_render_template.assert_called_once_with(
        'league_seasons/create.html', league_season=None, form=fake_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.league_season_controller.render_template')
@patch('app.flask.league_season_controller.flash')
@patch('app.flask.league_season_controller.injector')
@patch('app.flask.league_season_controller.league_season_factory')
@patch('app.flask.league_season_controller.NewLeagueSeasonForm')
def test_create_when_form_submitted_and_integrity_error_caught_for_conflict_with_foreign_key_constraint_on_league_id_should_flash_error_message_and_render_create_template(
        fake_form, fake_league_season_factory, fake_injector,
        fake_flash, fake_render_template
):
    # Arrange
    league_season = LeagueSeason(league_id=1, season_year=1920, num_of_weeks_scheduled=13, num_of_weeks_completed=0)
    league_season.league = Association(id=1, long_name="Association", short_name="A")
    league_season.season = Season(year=1920)

    fake_form.return_value.validate_on_submit.return_value = True
    fake_form.return_value.league_name.data = league_season.league.short_name
    fake_form.return_value.season_year.data = league_season.season.year
    fake_form.return_value.num_of_weeks_scheduled.data = league_season.num_of_weeks_scheduled
    fake_form.return_value.num_of_weeks_completed.data = league_season.num_of_weeks_completed

    fake_league_season_factory.create_league_season.return_value = league_season

    fake_league_season_repository = MagicMock(LeagueSeasonRepository)
    err = IntegrityError(
        'statement', 'params',
        Exception(f"The INSERT statement conflicted with the FOREIGN KEY constraint 'FK_LeagueSeason_Association_LeagueId'")
    )
    fake_league_season_repository.add_league_season.side_effect = err
    fake_injector.get.return_value = fake_league_season_repository

    # Act
    result = mod.create()

    # Assert
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    view_kwargs = {
        'league_name': league_season.league.short_name,
        'season_year': league_season.season.year,
        'num_of_weeks_scheduled': league_season.num_of_weeks_scheduled,
        'num_of_weeks_completed': league_season.num_of_weeks_completed,
    }
    fake_league_season_factory.create_league_season.assert_called_once_with(**view_kwargs)
    fake_injector.get.assert_called_once_with(LeagueSeasonRepository)
    fake_league_season_repository.add_league_season.assert_called_once_with(league_season)
    fake_flash.assert_called_once_with("FOREIGN KEY constraint violation on league name.", 'danger')
    fake_render_template.assert_called_once_with(
        'league_seasons/create.html', league_season=None, form=fake_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.league_season_controller.render_template')
@patch('app.flask.league_season_controller.flash')
@patch('app.flask.league_season_controller.injector')
@patch('app.flask.league_season_controller.league_season_factory')
@patch('app.flask.league_season_controller.NewLeagueSeasonForm')
def test_create_when_form_submitted_and_integrity_error_caught_for_conflict_with_foreign_key_constraint_on_season_year_should_flash_error_message_and_render_create_template(
        fake_form, fake_league_season_factory, fake_injector,
        fake_flash, fake_render_template
):
    # Arrange
    league_season = LeagueSeason(league_id=1, season_year=1920, num_of_weeks_scheduled=13, num_of_weeks_completed=0)
    league_season.league = Association(id=1, long_name="Association", short_name="A")
    league_season.season = Season(year=1920)

    fake_form.return_value.validate_on_submit.return_value = True
    fake_form.return_value.league_name.data = league_season.league.short_name
    fake_form.return_value.season_year.data = league_season.season.year
    fake_form.return_value.num_of_weeks_scheduled.data = league_season.num_of_weeks_scheduled
    fake_form.return_value.num_of_weeks_completed.data = league_season.num_of_weeks_completed

    fake_league_season_factory.create_league_season.return_value = league_season

    fake_league_season_repository = MagicMock(LeagueSeasonRepository)
    err = IntegrityError(
        'statement', 'params',
        Exception(f"The INSERT statement conflicted with the FOREIGN KEY constraint 'FK_LeagueSeason_Season_SeasonYear'")
    )
    fake_league_season_repository.add_league_season.side_effect = err
    fake_injector.get.return_value = fake_league_season_repository

    # Act
    result = mod.create()

    # Assert
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    view_kwargs = {
        'league_name': league_season.league.short_name,
        'season_year': league_season.season.year,
        'num_of_weeks_scheduled': league_season.num_of_weeks_scheduled,
        'num_of_weeks_completed': league_season.num_of_weeks_completed,
    }
    fake_league_season_factory.create_league_season.assert_called_once_with(**view_kwargs)
    fake_injector.get.assert_called_once_with(LeagueSeasonRepository)
    fake_league_season_repository.add_league_season.assert_called_once_with(league_season)
    fake_flash.assert_called_once_with("FOREIGN KEY constraint violation on season year.", 'danger')
    fake_render_template.assert_called_once_with(
        'league_seasons/create.html', league_season=None, form=fake_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.league_season_controller.render_template')
@patch('app.flask.league_season_controller.flash')
@patch('app.flask.league_season_controller.injector')
@patch('app.flask.league_season_controller.league_season_factory')
@patch('app.flask.league_season_controller.NewLeagueSeasonForm')
def test_create_when_form_submitted_and_integrity_error_caught_for_something_else_should_flash_error_message_and_render_create_template(
        fake_form, fake_league_season_factory, fake_injector,
        fake_flash, fake_render_template
):
    # Arrange
    league_season = LeagueSeason(league_id=1, season_year=1920, num_of_weeks_scheduled=13, num_of_weeks_completed=0)
    league_season.league = Association(id=1, long_name="Association", short_name="A")
    league_season.season = Season(year=1920)

    fake_form.return_value.validate_on_submit.return_value = True
    fake_form.return_value.league_name.data = league_season.league.short_name
    fake_form.return_value.season_year.data = league_season.season.year
    fake_form.return_value.num_of_weeks_scheduled.data = league_season.num_of_weeks_scheduled
    fake_form.return_value.num_of_weeks_completed.data = league_season.num_of_weeks_completed

    fake_league_season_factory.create_league_season.return_value = league_season

    fake_league_season_repository = MagicMock(LeagueSeasonRepository)
    err = IntegrityError(
        'statement', 'params',
        Exception(f"Something else")
    )
    fake_league_season_repository.add_league_season.side_effect = err
    fake_injector.get.return_value = fake_league_season_repository

    # Act
    result = mod.create()

    # Assert
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    view_kwargs = {
        'league_name': league_season.league.short_name,
        'season_year': league_season.season.year,
        'num_of_weeks_scheduled': league_season.num_of_weeks_scheduled,
        'num_of_weeks_completed': league_season.num_of_weeks_completed,
    }
    fake_league_season_factory.create_league_season.assert_called_once_with(**view_kwargs)
    fake_injector.get.assert_called_once_with(LeagueSeasonRepository)
    fake_league_season_repository.add_league_season.assert_called_once_with(league_season)
    fake_flash.assert_called_once_with("An unexpected error occurred.", 'danger')
    fake_render_template.assert_called_once_with(
        'league_seasons/create.html', league_season=None, form=fake_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.league_season_controller.copy')
@patch('app.flask.league_season_controller.injector')
def test_edit_when_league_season_not_found_should_abort_with_404_error(fake_injector, fake_copy):
    # Arrange
    fake_league_season_repository = MagicMock(LeagueSeasonRepository)
    old_league_season = LeagueSeason()
    fake_league_season_repository.get_league_season.return_value = old_league_season
    fake_injector.get.return_value = fake_league_season_repository

    old_league_season_copy = None
    fake_copy.deepcopy.return_value = old_league_season_copy

    # Act
    id = 1
    with pytest.raises(NotFound):
        result = mod.edit(id)

    # Assert
    fake_injector.get.assert_called_once_with(LeagueSeasonRepository)
    fake_league_season_repository.get_league_season.assert_called_once_with(id)
    fake_copy.deepcopy.assert_called_once_with(old_league_season)


@patch('app.flask.league_season_controller.render_template')
@patch('app.flask.league_season_controller.flash')
@patch('app.flask.league_season_controller.EditLeagueSeasonForm')
@patch('app.flask.league_season_controller.copy')
@patch('app.flask.league_season_controller.league_season_factory')
@patch('app.flask.league_season_controller.injector')
def test_edit_when_league_season_found_and_form_not_submitted_and_no_form_errors_should_render_edit_template(
        fake_injector, fake_league_season_factory, fake_copy,
        fake_form, fake_flash, fake_render_template
):
    # Arrange
    fake_league_season_repository = MagicMock(LeagueSeasonRepository)
    old_league_season = LeagueSeason()
    fake_league_season_repository.get_league_season.return_value = old_league_season
    fake_injector.get.return_value = fake_league_season_repository

    new_league_season = LeagueSeason(league_id=2, season_year=1921, num_of_weeks_scheduled=14, num_of_weeks_completed=0)
    fake_league_season_factory.create_league_season.return_value = new_league_season

    old_league_season_copy = LeagueSeason(
        league_id=1,
        season_year=1920,
        num_of_weeks_scheduled=13,
        num_of_weeks_completed=0
    )
    old_league_season_copy.league = Association(id=1, long_name="Association 1", short_name="A1")
    old_league_season_copy.season = Season(year=1920)
    fake_copy.deepcopy.return_value = old_league_season_copy

    fake_form.return_value.validate_on_submit.return_value = False
    fake_form.return_value.errors = None

    # Act
    id = 1
    result = mod.edit(id)

    # Assert
    fake_injector.get.assert_called_once_with(LeagueSeasonRepository)
    fake_league_season_repository.get_league_season.assert_called_once_with(id)
    fake_copy.deepcopy.assert_called_once_with(old_league_season)
    fake_form.assert_called_once()
    assert fake_form.return_value.league_name.data == old_league_season_copy.league.short_name
    assert fake_form.return_value.season_year.data == old_league_season_copy.season.year
    assert fake_form.return_value.num_of_weeks_scheduled.data == old_league_season_copy.num_of_weeks_scheduled
    assert fake_form.return_value.num_of_weeks_completed.data == old_league_season_copy.num_of_weeks_completed
    fake_form.return_value.validate_on_submit.assert_called_once()
    fake_flash.assert_not_called()
    fake_render_template.assert_called_once_with(
        'league_seasons/edit.html', league_season=old_league_season_copy, form=fake_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.league_season_controller.render_template')
@patch('app.flask.league_season_controller.flash')
@patch('app.flask.league_season_controller.EditLeagueSeasonForm')
@patch('app.flask.league_season_controller.copy')
@patch('app.flask.league_season_controller.league_season_factory')
@patch('app.flask.league_season_controller.injector')
def test_edit_when_league_season_found_and_form_not_submitted_and_form_errors_should_flash_errors_and_render_edit_template(
        fake_injector, fake_league_season_factory, fake_copy,
        fake_form, fake_flash, fake_render_template
):
    # Arrange
    fake_league_season_repository = MagicMock(LeagueSeasonRepository)
    old_league_season = LeagueSeason()
    fake_league_season_repository.get_league_season.return_value = old_league_season
    fake_injector.get.return_value = fake_league_season_repository

    new_league_season = LeagueSeason(league_id=2, season_year=1921, num_of_weeks_scheduled=14, num_of_weeks_completed=0)
    fake_league_season_factory.create_league_season.return_value = new_league_season

    old_league_season_copy = LeagueSeason(
        league_id=1,
        season_year=1920,
        num_of_weeks_scheduled=13,
        num_of_weeks_completed=0
    )
    old_league_season_copy.league = Association(id=1, long_name="Association 1", short_name="A1")
    old_league_season_copy.season = Season(year=1920)
    fake_copy.deepcopy.return_value = old_league_season_copy

    fake_form.return_value.validate_on_submit.return_value = False
    errors = 'errors'
    fake_form.return_value.errors = errors

    # Act
    id = 1
    result = mod.edit(id)

    # Assert
    fake_injector.get.assert_called_once_with(LeagueSeasonRepository)
    fake_league_season_repository.get_league_season.assert_called_once_with(id)
    fake_copy.deepcopy.assert_called_once_with(old_league_season)
    fake_form.assert_called_once()
    assert fake_form.return_value.league_name.data == old_league_season_copy.league.short_name
    assert fake_form.return_value.season_year.data == old_league_season_copy.season.year
    assert fake_form.return_value.num_of_weeks_scheduled.data == old_league_season_copy.num_of_weeks_scheduled
    assert fake_form.return_value.num_of_weeks_completed.data == old_league_season_copy.num_of_weeks_completed
    fake_form.return_value.validate_on_submit.assert_called_once()
    fake_flash.assert_called_once_with(f"{errors}", 'danger')
    fake_render_template('league_seasons/create.html', form=fake_form.return_value)
    assert result is fake_render_template.return_value


@patch('app.flask.league_season_controller.redirect')
@patch('app.flask.league_season_controller.url_for')
@patch('app.flask.league_season_controller.flash')
@patch('app.flask.league_season_controller.league_season_factory')
@patch('app.flask.league_season_controller.EditLeagueSeasonForm')
@patch('app.flask.league_season_controller.copy')
@patch('app.flask.league_season_controller.injector')
def test_edit_when_league_season_found_and_form_submitted_and_no_errors_caught_should_flash_success_message_and_redirect_to_league_season_details(
        fake_injector, fake_copy, fake_form,
        fake_league_season_factory, fake_flash,
        fake_url_for, fake_redirect
):
    # Arrange
    fake_league_season_repository = MagicMock(LeagueSeasonRepository)
    old_league_season = LeagueSeason()
    fake_league_season_repository.get_league_season.return_value = old_league_season
    fake_injector.get.return_value = fake_league_season_repository

    old_league_season_copy = LeagueSeason(
        league_id=1,
        season_year=1920,
        num_of_weeks_scheduled=13,
        num_of_weeks_completed=0
    )
    old_league_season_copy.league = Association(id=1, long_name="Association 1", short_name="A1")
    old_league_season_copy.season = Season(year=1920)
    fake_copy.deepcopy.return_value = old_league_season_copy

    new_league_id = 2
    new_league_name = "A2"
    new_season_year = 1921
    new_num_of_weeks_scheduled = 14
    new_num_of_weeks_completed = 7

    fake_form.return_value.validate_on_submit.return_value = True
    fake_form.return_value.league_name.data = new_league_name
    fake_form.return_value.season_year.data = new_season_year
    fake_form.return_value.num_of_weeks_scheduled.data = new_num_of_weeks_scheduled
    fake_form.return_value.num_of_weeks_completed.data = new_num_of_weeks_completed

    new_league_season = LeagueSeason(
        league_id=new_league_id,
        season_year=new_season_year,
        num_of_weeks_scheduled=new_num_of_weeks_scheduled,
        num_of_weeks_completed=new_num_of_weeks_completed
    )
    new_league_season.league = Association(id=new_league_id, long_name="Association 2", short_name=new_league_name)
    new_league_season.season = Season(year=new_season_year)
    fake_league_season_factory.create_league_season.return_value = new_league_season

    # Act
    id = 1
    result = mod.edit(id)

    # Assert
    fake_injector.get.assert_called_once_with(LeagueSeasonRepository)
    fake_league_season_repository.get_league_season.assert_called_once_with(id)
    fake_copy.deepcopy.assert_called_once_with(old_league_season)
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    kwargs = {
        'id': id,
        'league_name': new_league_name,
        'season_year': new_season_year,
        'num_of_weeks_scheduled': new_num_of_weeks_scheduled,
        'num_of_weeks_completed': new_num_of_weeks_completed,
    }
    fake_league_season_factory.create_league_season.assert_called_once_with(**kwargs)
    fake_league_season_repository.update_league_season.assert_called_once_with(new_league_season)
    fake_flash.assert_called_once_with(
        f"Item {new_league_name}, {new_season_year} has been successfully updated.", 'success'
    )
    fake_url_for.assert_called_once_with('league_season.details', id=id)
    fake_redirect.assert_called_once_with(fake_url_for.return_value)
    assert result is fake_redirect.return_value


@patch('app.flask.league_season_controller.render_template')
@patch('app.flask.league_season_controller.flash')
@patch('app.flask.league_season_controller.league_season_factory')
@patch('app.flask.league_season_controller.EditLeagueSeasonForm')
@patch('app.flask.league_season_controller.copy')
@patch('app.flask.league_season_controller.injector')
def test_edit_when_value_error_caught_should_flash_error_message_and_render_edit_template(
        fake_injector, fake_copy, fake_form,
        fake_league_season_factory, fake_flash,
        fake_render_template
):
    # Arrange
    fake_league_season_repository = MagicMock(LeagueSeasonRepository)
    old_league_season = LeagueSeason()
    fake_league_season_repository.get_league_season.return_value = old_league_season
    err = ValueError()
    fake_league_season_repository.update_league_season.side_effect = err
    fake_injector.get.return_value = fake_league_season_repository

    old_league_season_copy = LeagueSeason(
        league_id=1,
        season_year=1920,
        num_of_weeks_scheduled=13,
        num_of_weeks_completed=0
    )
    old_league_season_copy.league = Association(id=1, long_name="Association 1", short_name="A1")
    old_league_season_copy.season = Season(year=1920)
    fake_copy.deepcopy.return_value = old_league_season_copy

    new_league_id = 2
    new_league_name = "A2"
    new_season_year = 1921
    new_num_of_weeks_scheduled = 14
    new_num_of_weeks_completed = 7

    fake_form.return_value.validate_on_submit.return_value = True
    fake_form.return_value.league_name.data = new_league_name
    fake_form.return_value.season_year.data = new_season_year
    fake_form.return_value.num_of_weeks_scheduled.data = new_num_of_weeks_scheduled
    fake_form.return_value.num_of_weeks_completed.data = new_num_of_weeks_completed

    new_league_season = LeagueSeason(
        league_id=new_league_id,
        season_year=new_season_year,
        num_of_weeks_scheduled=new_num_of_weeks_scheduled,
        num_of_weeks_completed=new_num_of_weeks_completed
    )
    new_league_season.league = Association(id=new_league_id, short_name=new_league_name)
    new_league_season.season = Season(year=new_season_year)
    fake_league_season_factory.create_league_season.return_value = new_league_season

    # Act
    id = 1
    result = mod.edit(id)

    # Assert
    fake_injector.get.assert_called_once_with(LeagueSeasonRepository)
    fake_league_season_repository.get_league_season.assert_called_once_with(id)
    fake_copy.deepcopy.assert_called_once_with(old_league_season)
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    kwargs = {
        'id': id,
        'league_name': new_league_name,
        'season_year': new_season_year,
        'num_of_weeks_scheduled': new_num_of_weeks_scheduled,
        'num_of_weeks_completed': new_num_of_weeks_completed,
    }
    fake_league_season_factory.create_league_season.assert_called_once_with(**kwargs)
    fake_league_season_repository.update_league_season.assert_called_once_with(new_league_season)
    fake_flash.assert_called_once_with(str(err), 'danger')
    fake_render_template.assert_called_once_with(
        'league_seasons/edit.html', league_season=old_league_season_copy, form=fake_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.league_season_controller.render_template')
@patch('app.flask.league_season_controller.flash')
@patch('app.flask.league_season_controller.league_season_factory')
@patch('app.flask.league_season_controller.EditLeagueSeasonForm')
@patch('app.flask.league_season_controller.copy')
@patch('app.flask.league_season_controller.injector')
def test_edit_when_integrity_error_caught_for_unique_key_constraint_violation_should_flash_error_message_and_render_edit_template(
        fake_injector, fake_copy, fake_form,
        fake_league_season_factory, fake_flash,
        fake_render_template
):
    # Arrange
    fake_league_season_repository = MagicMock(LeagueSeasonRepository)
    old_league_season = LeagueSeason()
    fake_league_season_repository.get_league_season.return_value = old_league_season
    err = IntegrityError(
        'statement', 'params',
        Exception("Violation of UNIQUE KEY constraint 'UQ_LeagueSeason_League_Season'")
    )
    fake_league_season_repository.update_league_season.side_effect = err
    fake_injector.get.return_value = fake_league_season_repository

    old_league_season_copy = LeagueSeason(
        league_id=1,
        season_year=1920,
        num_of_weeks_scheduled=13,
        num_of_weeks_completed=0
    )
    old_league_season_copy.league = Association(id=1, long_name="Association 1", short_name="A1")
    old_league_season_copy.season = Season(year=1920)
    fake_copy.deepcopy.return_value = old_league_season_copy

    new_league_id = 2
    new_league_name = "A2"
    new_season_year = 1921
    new_num_of_weeks_scheduled = 14
    new_num_of_weeks_completed = 7

    fake_form.return_value.validate_on_submit.return_value = True
    fake_form.return_value.league_name.data = new_league_name
    fake_form.return_value.season_year.data = new_season_year
    fake_form.return_value.num_of_weeks_scheduled.data = new_num_of_weeks_scheduled
    fake_form.return_value.num_of_weeks_completed.data = new_num_of_weeks_completed

    new_league_season = LeagueSeason(
        league_id=new_league_id,
        season_year=new_season_year,
        num_of_weeks_scheduled=new_num_of_weeks_scheduled,
        num_of_weeks_completed=new_num_of_weeks_completed
    )
    new_league_season.league = Association(id=new_league_id, short_name=new_league_name)
    new_league_season.season = Season(year=new_season_year)
    fake_league_season_factory.create_league_season.return_value = new_league_season

    # Act
    id = 1
    result = mod.edit(id)

    # Assert
    fake_injector.get.assert_called_once_with(LeagueSeasonRepository)
    fake_league_season_repository.get_league_season.assert_called_once_with(id)
    fake_copy.deepcopy.assert_called_once_with(old_league_season)
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    kwargs = {
        'id': id,
        'league_name': new_league_name,
        'season_year': new_season_year,
        'num_of_weeks_scheduled': new_num_of_weeks_scheduled,
        'num_of_weeks_completed': new_num_of_weeks_completed,
    }
    fake_league_season_factory.create_league_season.assert_called_once_with(**kwargs)
    fake_league_season_repository.update_league_season.assert_called_once_with(new_league_season)
    fake_flash.assert_called_once_with(
        "A LeagueSeason with the same league_id and season_year already exists.", 'danger'
    )
    fake_render_template.assert_called_once_with(
        'league_seasons/edit.html', league_season=old_league_season_copy, form=fake_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.league_season_controller.render_template')
@patch('app.flask.league_season_controller.flash')
@patch('app.flask.league_season_controller.league_season_factory')
@patch('app.flask.league_season_controller.EditLeagueSeasonForm')
@patch('app.flask.league_season_controller.copy')
@patch('app.flask.league_season_controller.injector')
def test_edit_when_integrity_error_caught_for_conflict_with_foreign_key_constraint_on_league_id_should_flash_error_message_and_render_edit_template(
        fake_injector, fake_copy, fake_form,
        fake_league_season_factory, fake_flash,
        fake_render_template
):
    # Arrange
    fake_league_season_repository = MagicMock(LeagueSeasonRepository)
    old_league_season = LeagueSeason()
    fake_league_season_repository.get_league_season.return_value = old_league_season
    err = IntegrityError(
        'statement', 'params',
        Exception(f"The UPDATE statement conflicted with the FOREIGN KEY constraint 'FK_LeagueSeason_Association_LeagueId'")
    )
    fake_league_season_repository.update_league_season.side_effect = err
    fake_injector.get.return_value = fake_league_season_repository

    old_league_season_copy = LeagueSeason(
        league_id=1,
        season_year=1920,
        num_of_weeks_scheduled=13,
        num_of_weeks_completed=0
    )
    old_league_season_copy.league = Association(id=1, long_name="Association 1", short_name="A1")
    old_league_season_copy.season = Season(year=1920)
    fake_copy.deepcopy.return_value = old_league_season_copy

    new_league_id = 2
    new_league_name = "A2"
    new_season_year = 1921
    new_num_of_weeks_scheduled = 14
    new_num_of_weeks_completed = 7

    fake_form.return_value.validate_on_submit.return_value = True
    fake_form.return_value.league_name.data = new_league_name
    fake_form.return_value.season_year.data = new_season_year
    fake_form.return_value.num_of_weeks_scheduled.data = new_num_of_weeks_scheduled
    fake_form.return_value.num_of_weeks_completed.data = new_num_of_weeks_completed

    new_league_season = LeagueSeason(
        league_id=new_league_id,
        season_year=new_season_year,
        num_of_weeks_scheduled=new_num_of_weeks_scheduled,
        num_of_weeks_completed=new_num_of_weeks_completed
    )
    new_league_season.league = Association(id=new_league_id, short_name=new_league_name)
    new_league_season.season = Season(year=new_season_year)
    fake_league_season_factory.create_league_season.return_value = new_league_season

    # Act
    id = 1
    result = mod.edit(id)

    # Assert
    fake_injector.get.assert_called_once_with(LeagueSeasonRepository)
    fake_league_season_repository.get_league_season.assert_called_once_with(id)
    fake_copy.deepcopy.assert_called_once_with(old_league_season)
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    kwargs = {
        'id': id,
        'league_name': new_league_name,
        'season_year': new_season_year,
        'num_of_weeks_scheduled': new_num_of_weeks_scheduled,
        'num_of_weeks_completed': new_num_of_weeks_completed,
    }
    fake_league_season_factory.create_league_season.assert_called_once_with(**kwargs)
    fake_league_season_repository.update_league_season.assert_called_once_with(new_league_season)
    fake_flash.assert_called_once_with("FOREIGN KEY constraint violation on league name.", 'danger')
    fake_render_template.assert_called_once_with(
        'league_seasons/edit.html', league_season=old_league_season_copy, form=fake_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.league_season_controller.render_template')
@patch('app.flask.league_season_controller.flash')
@patch('app.flask.league_season_controller.league_season_factory')
@patch('app.flask.league_season_controller.EditLeagueSeasonForm')
@patch('app.flask.league_season_controller.copy')
@patch('app.flask.league_season_controller.injector')
def test_edit_when_integrity_error_caught_for_conflict_with_foreign_key_constraint_on_season_year_should_flash_error_message_and_render_edit_template(
        fake_injector, fake_copy, fake_form,
        fake_league_season_factory, fake_flash,
        fake_render_template
):
    # Arrange
    fake_league_season_repository = MagicMock(LeagueSeasonRepository)
    old_league_season = LeagueSeason()
    fake_league_season_repository.get_league_season.return_value = old_league_season
    err = IntegrityError(
        'statement', 'params',
        Exception(f"The UPDATE statement conflicted with the FOREIGN KEY constraint 'FK_LeagueSeason_Season_SeasonYear'")
    )
    fake_league_season_repository.update_league_season.side_effect = err
    fake_injector.get.return_value = fake_league_season_repository

    old_league_season_copy = LeagueSeason(
        league_id=1,
        season_year=1920,
        num_of_weeks_scheduled=13,
        num_of_weeks_completed=0
    )
    old_league_season_copy.league = Association(id=1, long_name="Association 1", short_name="A1")
    old_league_season_copy.season = Season(year=1920)
    fake_copy.deepcopy.return_value = old_league_season_copy

    new_league_id = 2
    new_league_name = "A2"
    new_season_year = 1921
    new_num_of_weeks_scheduled = 14
    new_num_of_weeks_completed = 7

    fake_form.return_value.validate_on_submit.return_value = True
    fake_form.return_value.league_name.data = new_league_name
    fake_form.return_value.season_year.data = new_season_year
    fake_form.return_value.num_of_weeks_scheduled.data = new_num_of_weeks_scheduled
    fake_form.return_value.num_of_weeks_completed.data = new_num_of_weeks_completed

    new_league_season = LeagueSeason(
        league_id=new_league_id,
        season_year=new_season_year,
        num_of_weeks_scheduled=new_num_of_weeks_scheduled,
        num_of_weeks_completed=new_num_of_weeks_completed
    )
    new_league_season.league = Association(id=new_league_id, short_name=new_league_name)
    new_league_season.season = Season(year=new_season_year)
    fake_league_season_factory.create_league_season.return_value = new_league_season

    # Act
    id = 1
    result = mod.edit(id)

    # Assert
    fake_injector.get.assert_called_once_with(LeagueSeasonRepository)
    fake_league_season_repository.get_league_season.assert_called_once_with(id)
    fake_copy.deepcopy.assert_called_once_with(old_league_season)
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    kwargs = {
        'id': id,
        'league_name': new_league_name,
        'season_year': new_season_year,
        'num_of_weeks_scheduled': new_num_of_weeks_scheduled,
        'num_of_weeks_completed': new_num_of_weeks_completed,
    }
    fake_league_season_factory.create_league_season.assert_called_once_with(**kwargs)
    fake_league_season_repository.update_league_season.assert_called_once_with(new_league_season)
    fake_flash.assert_called_once_with("FOREIGN KEY constraint violation on season year.", 'danger')
    fake_render_template.assert_called_once_with(
        'league_seasons/edit.html', league_season=old_league_season_copy, form=fake_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.league_season_controller.render_template')
@patch('app.flask.league_season_controller.flash')
@patch('app.flask.league_season_controller.league_season_factory')
@patch('app.flask.league_season_controller.EditLeagueSeasonForm')
@patch('app.flask.league_season_controller.copy')
@patch('app.flask.league_season_controller.injector')
def test_edit_when_integrity_error_caught_for_something_else_should_flash_error_message_and_render_edit_template(
        fake_injector, fake_copy, fake_form,
        fake_league_season_factory, fake_flash,
        fake_render_template
):
    # Arrange
    fake_league_season_repository = MagicMock(LeagueSeasonRepository)
    old_league_season = LeagueSeason()
    fake_league_season_repository.get_league_season.return_value = old_league_season
    err = IntegrityError(
        'statement', 'params',
        Exception(f"Something else")
    )
    fake_league_season_repository.update_league_season.side_effect = err
    fake_injector.get.return_value = fake_league_season_repository

    old_league_season_copy = LeagueSeason(
        league_id=1,
        season_year=1920,
        num_of_weeks_scheduled=13,
        num_of_weeks_completed=0
    )
    old_league_season_copy.league = Association(id=1, long_name="Association 1", short_name="A1")
    old_league_season_copy.season = Season(year=1920)
    fake_copy.deepcopy.return_value = old_league_season_copy

    new_league_id = 2
    new_league_name = "A2"
    new_season_year = 1921
    new_num_of_weeks_scheduled = 14
    new_num_of_weeks_completed = 7

    fake_form.return_value.validate_on_submit.return_value = True
    fake_form.return_value.league_name.data = new_league_name
    fake_form.return_value.season_year.data = new_season_year
    fake_form.return_value.num_of_weeks_scheduled.data = new_num_of_weeks_scheduled
    fake_form.return_value.num_of_weeks_completed.data = new_num_of_weeks_completed

    new_league_season = LeagueSeason(
        league_id=new_league_id,
        season_year=new_season_year,
        num_of_weeks_scheduled=new_num_of_weeks_scheduled,
        num_of_weeks_completed=new_num_of_weeks_completed
    )
    new_league_season.league = Association(id=new_league_id, short_name=new_league_name)
    new_league_season.season = Season(year=new_season_year)
    fake_league_season_factory.create_league_season.return_value = new_league_season

    # Act
    id = 1
    result = mod.edit(id)

    # Assert
    fake_injector.get.assert_called_once_with(LeagueSeasonRepository)
    fake_league_season_repository.get_league_season.assert_called_once_with(id)
    fake_copy.deepcopy.assert_called_once_with(old_league_season)
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    kwargs = {
        'id': id,
        'league_name': new_league_name,
        'season_year': new_season_year,
        'num_of_weeks_scheduled': new_num_of_weeks_scheduled,
        'num_of_weeks_completed': new_num_of_weeks_completed,
    }
    fake_league_season_factory.create_league_season.assert_called_once_with(**kwargs)
    fake_league_season_repository.update_league_season.assert_called_once_with(new_league_season)
    fake_flash.assert_called_once_with("An unexpected error occurred.", 'danger')
    fake_render_template.assert_called_once_with(
        'league_seasons/edit.html', league_season=old_league_season_copy, form=fake_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.league_season_controller.flash')
@patch('app.flask.league_season_controller.league_season_factory')
@patch('app.flask.league_season_controller.EditLeagueSeasonForm')
@patch('app.flask.league_season_controller.copy')
@patch('app.flask.league_season_controller.injector')
def test_edit_when_league_season_found_and_form_submitted_and_index_error_caught_should_abort_with_404_error(
        fake_injector, fake_copy, fake_form,
        fake_league_season_factory, fake_flash
):
    # Arrange
    fake_league_season_repository = MagicMock(LeagueSeasonRepository)
    old_league_season = LeagueSeason()
    fake_league_season_repository.get_league_season.return_value = old_league_season
    err = IndexError()
    fake_league_season_repository.update_league_season.side_effect = err
    fake_injector.get.return_value = fake_league_season_repository

    old_league_season_copy = LeagueSeason(
        league_id=1,
        season_year=1920,
        num_of_weeks_scheduled=13,
        num_of_weeks_completed=0
    )
    old_league_season_copy.league = Association(id=1, long_name="Association 1", short_name="A1")
    old_league_season_copy.season = Season(year=1920)
    fake_copy.deepcopy.return_value = old_league_season_copy

    new_league_id = 2
    new_league_name = "A2"
    new_season_year = 1921
    new_num_of_weeks_scheduled = 14
    new_num_of_weeks_completed = 7

    fake_form.return_value.validate_on_submit.return_value = True
    fake_form.return_value.league_name.data = new_league_name
    fake_form.return_value.season_year.data = new_season_year
    fake_form.return_value.num_of_weeks_scheduled.data = new_num_of_weeks_scheduled
    fake_form.return_value.num_of_weeks_completed.data = new_num_of_weeks_completed

    new_league_season = LeagueSeason(
        league_id=new_league_id,
        season_year=new_season_year,
        num_of_weeks_scheduled=new_num_of_weeks_scheduled,
        num_of_weeks_completed=new_num_of_weeks_completed
    )
    new_league_season.league = Association(id=new_league_id, short_name=new_league_name)
    new_league_season.season = Season(year=new_season_year)
    fake_league_season_factory.create_league_season.return_value = new_league_season

    # Act
    id = 1
    with pytest.raises(NotFound):
        _ = mod.edit(id)

    # Assert
    fake_injector.get.assert_called_once_with(LeagueSeasonRepository)
    fake_league_season_repository.get_league_season.assert_called_once_with(id)
    fake_copy.deepcopy.assert_called_once_with(old_league_season)
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    kwargs = {
        'id': id,
        'league_name': new_league_name,
        'season_year': new_season_year,
        'num_of_weeks_scheduled': new_num_of_weeks_scheduled,
        'num_of_weeks_completed': new_num_of_weeks_completed,
    }
    fake_league_season_factory.create_league_season.assert_called_once_with(**kwargs)
    fake_league_season_repository.update_league_season.assert_called_once_with(new_league_season)


@patch('app.flask.league_season_controller.injector')
@patch('app.flask.league_season_controller.DeleteLeagueSeasonForm')
def test_delete_when_league_season_not_found_should_abort_with_404_error(
        fake_form, fake_injector, test_app
):
    # Arrange
    fake_league_season_repository = MagicMock(LeagueSeasonRepository)
    fake_league_season_repository.get_league_season.return_value = None
    fake_injector.get.return_value = fake_league_season_repository

    # Act
    id = 1
    with test_app.test_request_context(
            f'/league_seasons/delete?id={id}',
            method='GET'
    ):
        with pytest.raises(NotFound):
            _ = mod.delete(id)

    # Assert
    fake_form.assert_called_once()
    fake_injector.get.assert_called_once_with(LeagueSeasonRepository)
    fake_league_season_repository.get_league_season.assert_called_once_with(id)


@patch('app.flask.league_season_controller.render_template')
@patch('app.flask.league_season_controller.injector')
@patch('app.flask.league_season_controller.DeleteLeagueSeasonForm')
def test_delete_when_request_method_is_get_should_render_delete_template(
        fake_form, fake_injector, fake_render_template, test_app
):
    # Arrange
    fake_league_season_repository = MagicMock(LeagueSeasonRepository)
    league_season = LeagueSeason()
    fake_league_season_repository.get_league_season.return_value = league_season
    fake_injector.get.return_value = fake_league_season_repository

    # Act
    id = 1
    with test_app.test_request_context(
            f'/league_seasons/delete?id={id}',
            method='GET'
    ):
        result = mod.delete(id)

    # Assert
    fake_form.assert_called_once()
    fake_injector.get.assert_called_once_with(LeagueSeasonRepository)
    fake_league_season_repository.get_league_season.assert_called_once_with(id)
    fake_render_template.assert_called_once_with(
        'league_seasons/delete.html', league_season=league_season, form=fake_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.league_season_controller.redirect')
@patch('app.flask.league_season_controller.url_for')
@patch('app.flask.league_season_controller.flash')
@patch('app.flask.league_season_controller.injector')
@patch('app.flask.league_season_controller.DeleteLeagueSeasonForm')
def test_delete_when_request_method_is_post_and_league_season_found_should_flash_success_message_and_redirect_to_league_seasons_index(
        fake_form, fake_injector, fake_flash,
        fake_url_for, fake_redirect, test_app
):
    # Arrange
    fake_league_season_repository = MagicMock(LeagueSeasonRepository)
    league_season = LeagueSeason(league_id=1, season_year=1920, num_of_weeks_scheduled=13, num_of_weeks_completed=0)
    league_season.league = Association(id=1, long_name="Association", short_name="A")
    league_season.season = Season(year=1920)
    fake_league_season_repository.get_league_season.return_value = league_season
    fake_injector.get.return_value = fake_league_season_repository

    # Act
    id = 1
    with test_app.test_request_context(
            f'/league_seasons/delete?id={id}',
            method='POST'
    ):
        result = mod.delete(id)

    # Assert
    fake_form.assert_called_once()
    fake_injector.get.assert_called_once_with(LeagueSeasonRepository)
    fake_league_season_repository.get_league_season.assert_called_once_with(id)
    fake_league_season_repository.delete_league_season.assert_called_once_with(id)
    fake_flash.assert_called_once_with(
        f"LeagueSeason {league_season.league.short_name}. {league_season.season.year} has been successfully deleted.",
        'success'
    )
    fake_url_for.assert_called_once_with('league_season.index')
    fake_redirect.assert_called_once_with(fake_url_for.return_value)
    assert result is fake_redirect.return_value


@patch('app.flask.league_season_controller.injector')
def test_delete_when_request_method_is_post_and_index_error_is_caught_should_abort_with_404_error(
        fake_injector, test_app
):
    # Arrange
    fake_league_season_repository = MagicMock(LeagueSeasonRepository)
    league_season = LeagueSeason()
    fake_league_season_repository.get_league_season.return_value = league_season
    fake_league_season_repository.delete_league_season.side_effect = IndexError()
    fake_injector.get.return_value = fake_league_season_repository

    # Act
    id = 1
    with test_app.test_request_context(
            f'/league_seasons/delete?id={id}',
            method='POST'
    ):
        with pytest.raises(NotFound):
            _ = mod.delete(id)

    # Assert
    fake_injector.get.assert_called_once_with(LeagueSeasonRepository)
    fake_league_season_repository.get_league_season.assert_called_once_with(id)
