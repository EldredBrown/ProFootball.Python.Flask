from typing import Optional, Any
from unittest.mock import patch, call, MagicMock

import pytest
from flask import session

from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound

import app.flask.game_controller as mod
from app.data.models.association import Association
from app.data.models.league_season import LeagueSeason

from app.data.models.season import Season
from app.data.models.game import Game
from app.data.repositories.association_repository import AssociationRepository
from app.data.repositories.game_repository import GameRepository
from app.data.repositories.league_season_repository import LeagueSeasonRepository
from app.data.repositories.season_repository import SeasonRepository
from app.services.game_service.game_service import GameService

from test_app import create_app


@pytest.fixture()
def test_app():
    return create_app()


@pytest.mark.parametrize(
    "league_name",
    [
        None,
        '',
    ]
)
@patch('app.flask.game_controller.render_template')
@patch('app.flask.game_controller.injector')
def test_index_when_selected_season_year_is_none_and_selected_league_name_is_none_or_empty_should_set_selected_season_year_and_selected_league_name_to_default_values_and_render_index_template(
        fake_injector, fake_render_template, league_name, test_app
):
    # Arrange
    fake_season_repository, seasons, selected_season, fake_association_repository, leagues, selected_league, fake_league_season_repository, selected_league_season, fake_game_repository, selected_games = (
        _set_up_index(fake_injector, selected_league_name=league_name)
    )

    with test_app.test_request_context(
            '/games/',
            method='GET'
    ):
        # Act
        selected_season_year = None
        session['selected_season_year'] = selected_season_year

        selected_league_name = league_name
        session['selected_league_name'] = selected_league_name

        selected_week = None
        session['selected_week'] = selected_week

        result = mod.index()

        # Assert
        fake_season_repository.get_seasons.assert_called_once()
        assert session.get('seasons') == [s.to_dict() for s in seasons]
        assert session.get('selected_season_year') == selected_season.year
        assert session.get('leagues') == [l.to_dict() for l in leagues]
        assert session.get('selected_league_name') == selected_league.short_name
        fake_league_season_repository.get_league_season_by_league_and_season.assert_called_once_with(
            selected_league.id, selected_season.year
        )
        weeks = [None, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
        assert session.get('weeks') == weeks
        fake_injector.get.assert_has_calls([
            call(SeasonRepository),
            call(AssociationRepository),
            call(LeagueSeasonRepository),
            call(GameRepository),
        ])
        fake_game_repository.get_games_by_season_league_and_week.assert_called_once_with(
            season_year=selected_season.year, league_id=selected_league.id, week=selected_week
        )
        fake_render_template.assert_called_once_with(
            'games/index.html',
            seasons=seasons, selected_season_year=selected_season.year,
            leagues=leagues, selected_league_name=selected_league.short_name,
            weeks=weeks, selected_week=selected_week,
            games=selected_games
        )
        assert result is fake_render_template.return_value


@pytest.mark.parametrize(
    "league_name",
    [
        None,
        '',
    ]
)
@patch('app.flask.game_controller.render_template')
@patch('app.flask.game_controller.injector')
def test_index_when_selected_season_year_is_not_none_should_set_selected_season_year_and_render_index_template(
        fake_injector, fake_render_template, league_name, test_app
):
    # Arrange
    fake_season_repository, seasons, selected_season, fake_association_repository, leagues, selected_league, fake_league_season_repository, selected_league_season, fake_game_repository, selected_games = (
        _set_up_index(fake_injector, selected_season_year=1920, selected_league_name=league_name)
    )

    fake_injector.get.side_effect = [
        fake_season_repository,
        fake_association_repository,
        fake_league_season_repository,
        fake_game_repository,
    ]

    with test_app.test_request_context(
            '/games/',
            method='GET'
    ):
        # Act
        session['selected_season_year'] = selected_season.year

        selected_league_name = league_name
        session['selected_league_name'] = selected_league_name

        selected_week = None
        session['selected_week'] = selected_week

        result = mod.index()

        # Assert
        fake_season_repository.get_seasons.assert_called_once()
        assert session.get('seasons') == [s.to_dict() for s in seasons]
        assert session.get('selected_season_year') == selected_season.year
        assert session.get('leagues') == [l.to_dict() for l in leagues]
        assert session.get('selected_league_name') == selected_league.short_name
        fake_league_season_repository.get_league_season_by_league_and_season.assert_called_once_with(
            selected_league.id, selected_season.year
        )
        weeks = [None, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
        assert session.get('weeks') == weeks
        fake_injector.get.assert_has_calls([
            call(SeasonRepository),
            call(AssociationRepository),
            call(LeagueSeasonRepository),
            call(GameRepository),
        ])
        fake_game_repository.get_games_by_season_league_and_week.assert_called_once_with(
            season_year=selected_season.year, league_id=selected_league.id, week=selected_week
        )
        fake_render_template.assert_called_once_with(
            'games/index.html',
            seasons=seasons, selected_season_year=selected_season.year,
            leagues=leagues, selected_league_name=selected_league.short_name,
            weeks=weeks, selected_week=selected_week,
            games=selected_games
        )
        assert result is fake_render_template.return_value


@patch('app.flask.game_controller.render_template')
@patch('app.flask.game_controller.injector')
def test_index_when_selected_league_name_is_neither_none_nor_empty_should_selected_league_name_and_render_index_template(
        fake_injector, fake_render_template, test_app
):
    # Arrange
    fake_season_repository, seasons, selected_season, fake_association_repository, leagues, selected_league, fake_league_season_repository, selected_league_season, fake_game_repository, selected_games = (
        _set_up_index(fake_injector, selected_season_year=1920, selected_league_name="APFA")
    )

    # Set up games.
    fake_game_repository = MagicMock(GameRepository)
    games = []
    for s in range(1920, 1923):
        for l in range(1, 4):
            for w in range(1, 4):
                for t in range(1, 4):
                    games.append(
                        Game(
                            id=(9 * s + 3 * l + w),
                            season_year=s,
                            league_id=l,
                            week=w,
                            guest_name=f"Guest {t}",
                            guest_score=0,
                            host_name=f"Guest {t}",
                            host_score=0
                        )
                    )
    selected_games = [
        g for g in games if g.season_year == selected_season.year and g.league_id == selected_league.id
    ]
    fake_game_repository.get_games_by_season_league_and_week.return_value = selected_games

    fake_injector.get.side_effect = [
        fake_season_repository,
        fake_association_repository,
        fake_league_season_repository,
        fake_game_repository,
    ]

    with test_app.test_request_context(
            '/games/',
            method='GET'
    ):
        # Act
        session['selected_season_year'] = selected_season.year
        session['selected_league_name'] = selected_league.short_name

        selected_week = None
        session['selected_week'] = selected_week

        result = mod.index()

        # Assert
        fake_season_repository.get_seasons.assert_called_once()
        assert session.get('seasons') == [s.to_dict() for s in seasons]
        assert session.get('selected_season_year') == selected_season.year
        assert session.get('leagues') == [l.to_dict() for l in leagues]
        assert session.get('selected_league_name') == selected_league.short_name
        fake_league_season_repository.get_league_season_by_league_and_season.assert_called_once_with(
            selected_league.id, selected_season.year
        )
        weeks = [None, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
        assert session.get('weeks') == weeks
        fake_injector.get.assert_has_calls([
            call(SeasonRepository),
            call(AssociationRepository),
            call(LeagueSeasonRepository),
            call(GameRepository),
        ])
        fake_game_repository.get_games_by_season_league_and_week.assert_called_once_with(
            season_year=selected_season.year, league_id=selected_league.id, week=selected_week
        )
        fake_render_template.assert_called_once_with(
            'games/index.html',
            seasons=seasons, selected_season_year=selected_season.year,
            leagues=leagues, selected_league_name=selected_league.short_name,
            weeks=weeks, selected_week=selected_week,
            games=selected_games
        )
        assert result is fake_render_template.return_value


def _set_up_index(
        fake_injector, selected_season_year: Optional[int] = None, selected_league_name: Optional[str] = None
) -> tuple[MagicMock, list[Season], Season, MagicMock, list[Association], Association, MagicMock, LeagueSeason, MagicMock, list[Game]]:
    fake_season_repository, seasons, selected_season = _set_up_index_seasons(selected_season_year)
    fake_association_repository, leagues, selected_league = (
        _set_up_index_leagues(selected_season.year, selected_league_name)
    )
    fake_league_season_repository, selected_league_season = _set_up_index_league_season()
    fake_game_repository, selected_games = _set_up_index_games(selected_season.year, selected_league.id)

    fake_injector.get.side_effect = [
        fake_season_repository,
        fake_association_repository,
        fake_league_season_repository,
        fake_game_repository,
    ]
    return (
        fake_season_repository, seasons, selected_season,
        fake_association_repository, leagues, selected_league,
        fake_league_season_repository, selected_league_season,
        fake_game_repository, selected_games
    )


def _set_up_index_seasons(selected_season_year: Optional[int]) -> tuple[MagicMock, list[Season], Season]:
    fake_season_repository = MagicMock(SeasonRepository)
    seasons = [
        Season(year=1920),
        Season(year=1921),
        Season(year=1922),
    ]
    seasons.sort(key=lambda s: s.year, reverse=True)
    selected_season = [s for s in seasons if s.year == selected_season_year][0] if selected_season_year else seasons[0]
    fake_season_repository.get_seasons.return_value = seasons
    return fake_season_repository, seasons, selected_season


def _set_up_index_leagues(selected_season_year: int, selected_league_name: Optional[str]) \
    -> tuple[MagicMock, list[Association], Association]:
    fake_association_repository = MagicMock(AssociationRepository)
    associations = [
        Association(
            id=1,
            long_name="American Professional Football Association",
            short_name="APFA",
            parent_id=None,
            first_season_year=1920,
            last_season_year=1922
        ),
        Association(
            id=2,
            long_name="National Football League",
            short_name="NFL",
            parent_id=None,
            first_season_year=1922
        ),
        Association(
            id=3,
            long_name="National Football Conference",
            short_name="NFC",
            parent_id=2,
            first_season_year=1970
        ),
        Association(
            id=4,
            long_name="American Football Conference",
            short_name="AFC",
            parent_id=2,
            first_season_year=1970
        ),
    ]
    leagues = [a for a in associations if a.parent_id is None]
    active_leagues = [l for l in leagues if l.first_season_year <= selected_season_year
                      and (l.last_season is None or selected_season_year <= l.last_season_year)]
    active_leagues.sort(key=lambda l: l.id, reverse=True)
    selected_league = (
        [l for l in active_leagues if l.short_name == selected_league_name][0]
        if selected_league_name else active_leagues[0]
    )
    fake_association_repository.get_associations.return_value = associations
    return fake_association_repository, active_leagues, selected_league


def _set_up_index_league_season() -> tuple[MagicMock, LeagueSeason]:
    fake_league_season_repository = MagicMock(LeagueSeasonRepository)
    selected_league_season = LeagueSeason(
        id=1,
        league_id=1,
        season_year=1920,
        num_of_weeks_scheduled=13,
    )
    fake_league_season_repository.get_league_season_by_league_and_season.return_value = selected_league_season
    return fake_league_season_repository, selected_league_season


def _set_up_index_games(selected_season_year: int, selected_league_id: int) -> tuple[MagicMock, list[Game]]:
    fake_game_repository = MagicMock(GameRepository)
    games = []
    for s in range(1920, 1923):
        for l in range(1, 4):
            for w in range(1, 4):
                for t in range(1, 4):
                    games.append(
                        Game(
                            id=(9 * s + 3 * l + w),
                            season_year=s,
                            league_id=l,
                            week=w,
                            guest_name=f"Guest {t}",
                            guest_score=0,
                            host_name=f"Guest {t}",
                            host_score=0
                        )
                    )
    selected_games = [
        g for g in games if g.season_year == selected_season_year and g.league_id == selected_league_id
    ]
    fake_game_repository.get_games_by_season_league_and_week.return_value = selected_games
    return fake_game_repository, selected_games


@patch('app.flask.game_controller.render_template')
@patch('app.flask.game_controller.injector')
@patch('app.flask.game_controller.DeleteGameForm')
def test_details_when_game_found_should_render_game_details_template(
        fake_form, fake_injector, fake_render_template
):
    # Arrange
    fake_game_repository = _set_up_details(fake_injector)

    # Act
    id = 1
    result = mod.details(id)

    # Assert
    fake_form.assert_called_once()
    fake_injector.get.assert_called_once_with(GameRepository)
    fake_game_repository.get_game.assert_called_once_with(id)
    fake_render_template.assert_called_once_with(
        'games/details.html',
        form=fake_form.return_value,
        game = fake_game_repository.get_game.return_value
    )
    assert result == fake_render_template.return_value


@patch('app.flask.game_controller.injector')
@patch('app.flask.game_controller.DeleteGameForm')
def test_details_when_game_not_found_should_abort_with_404_error(fake_form, fake_injector):
    # Arrange
    _ = _set_up_details(fake_injector, IndexError())

    # Act
    with pytest.raises(NotFound):
        _ = mod.details(1)


def _set_up_details(fake_injector, err: Optional[Exception] = None) -> MagicMock:
    fake_game_repository = MagicMock(GameRepository)
    if err:
        fake_game_repository.get_game.side_effect = err
    fake_injector.get.return_value = fake_game_repository

    return fake_game_repository


@patch('app.flask.game_controller.render_template')
@patch('app.flask.game_controller.flash')
@patch('app.flask.game_controller.injector')
@patch('app.flask.game_controller.NewGameForm')
def test_create_when_form_not_submitted_and_selected_season_year_is_less_than_1920_and_no_form_errors_should_render_create_template(
        fake_form, fake_injector, fake_flash,
        fake_render_template, test_app
):
    # Arrange
    fake_game_service = _set_up_create_get(fake_injector, fake_form)

    # Act
    with test_app.test_request_context('/games/create', method='GET'):
        selected_season_year = 1919
        session['selected_season_year'] = selected_season_year
        session['selected_week'] = 1

        result = mod.create()

        # Assert
        fake_form.assert_called_once()
        assert fake_form.return_value.season_year.data == -1
        assert fake_form.return_value.week.data == 1
        fake_form.return_value.validate_on_submit.assert_called_once()
        fake_injector.get.assert_not_called()
        fake_game_service.add_game.assert_not_called()
        fake_flash.assert_not_called()
        fake_render_template('games/create.html', form=fake_form.return_value)
        assert result is fake_render_template.return_value


@patch('app.flask.game_controller.render_template')
@patch('app.flask.game_controller.flash')
@patch('app.flask.game_controller.injector')
@patch('app.flask.game_controller.NewGameForm')
def test_create_when_form_not_submitted_and_selected_season_year_is_equal_to_1920_and_no_form_errors_should_render_create_template(
        fake_form, fake_injector, fake_flash,
        fake_render_template, test_app
):
    # Arrange
    fake_game_service = _set_up_create_get(fake_injector, fake_form)

    with test_app.test_request_context('/games/create', method='GET'):
        # Act
        selected_season_year = 1920
        session['selected_season_year'] = selected_season_year
        session['selected_week'] = 1

        result = mod.create()

        # Assert
        fake_form.assert_called_once()
        assert fake_form.return_value.season_year.data == selected_season_year
        assert fake_form.return_value.week.data == 1
        fake_form.return_value.validate_on_submit.assert_called_once()
        fake_injector.get.assert_not_called()
        fake_game_service.add_game.assert_not_called()
        fake_flash.assert_not_called()
        fake_render_template('games/create.html', form=fake_form.return_value)
        assert result is fake_render_template.return_value


@patch('app.flask.game_controller.render_template')
@patch('app.flask.game_controller.flash')
@patch('app.flask.game_controller.injector')
@patch('app.flask.game_controller.NewGameForm')
def test_create_when_form_not_submitted_and_selected_season_year_is_greater_than_1920_and_no_form_errors_should_render_create_template(
        fake_form, fake_injector, fake_flash,
        fake_render_template, test_app
):
    # Arrange
    fake_game_service = _set_up_create_get(fake_injector, fake_form)

    with test_app.test_request_context('/games/create', method='GET'):
        # Act
        selected_season_year = 1921
        session['selected_season_year'] = selected_season_year
        session['selected_week'] = 1

        result = mod.create()

        # Assert
        fake_form.assert_called_once()
        assert fake_form.return_value.season_year.data == selected_season_year
        assert fake_form.return_value.week.data == 1
        fake_form.return_value.validate_on_submit.assert_called_once()
        fake_injector.get.assert_not_called()
        fake_game_service.add_game.assert_not_called()
        fake_flash.assert_not_called()
        fake_render_template('games/create.html', form=fake_form.return_value)
        assert result is fake_render_template.return_value


@patch('app.flask.game_controller.render_template')
@patch('app.flask.game_controller.flash')
@patch('app.flask.game_controller.injector')
@patch('app.flask.game_controller.NewGameForm')
def test_create_when_form_not_submitted_and_form_errors_should_flash_errors_and_render_create_template(
        fake_form, fake_injector, fake_flash,
        fake_render_template, test_app
):
    # Arrange
    errors = 'errors'
    fake_game_service = _set_up_create_get(fake_injector, fake_form, errors=errors)

    with test_app.test_request_context('/games/create', method='GET'):
        # Act
        selected_season_year = 1921
        session['selected_season_year'] = selected_season_year
        session['selected_week'] = 1

        result = mod.create()

        # Assert
        fake_form.assert_called_once()
        fake_form.return_value.validate_on_submit.assert_called_once()
        fake_injector.get.assert_not_called()
        fake_game_service.add_game.assert_not_called()
        fake_flash.assert_called_once_with(f"{errors}", 'danger')
        fake_render_template('games/create.html', form=fake_form.return_value)
        assert result is fake_render_template.return_value


def _set_up_create_get(fake_injector, fake_form, errors: Optional[str] = None) -> MagicMock:
    fake_form.return_value.week.data = None
    fake_form.return_value.validate_on_submit.return_value = False

    fake_form.return_value.errors = errors

    fake_game_service = MagicMock(GameService)
    fake_injector.get.return_value = fake_game_service

    return fake_game_service


@patch('app.flask.game_controller.url_for')
@patch('app.flask.game_controller.redirect')
@patch('app.flask.game_controller.flash')
@patch('app.flask.game_controller.injector')
@patch('app.flask.game_controller.game_factory')
@patch('app.flask.game_controller.NewGameForm')
def test_create_when_form_submitted_and_no_errors_caught_should_flash_success_message_and_redirect_to_game_create(
        fake_form, fake_game_factory, fake_injector,
        fake_flash, fake_redirect, fake_url_for,
        test_app
):
    # Arrange
    fake_game_service, game = _set_up_create_post(fake_injector, fake_form, fake_game_factory)

    # Act
    with test_app.test_request_context('/games/create', method='POST'):
        result = mod.create()

        # Assert
        kwargs = {
            'season_year': 1920,
            'league_name': "A",
            'week': 1,
            'guest_name': "Guest",
            'guest_score': 3,
            'host_name': "Host",
            'host_score': 3,
            'is_playoff': False,
            'notes': None,
        }

        fake_form.assert_called_once()
        fake_form.return_value.validate_on_submit.assert_called_once()
        fake_game_factory.create_game.assert_called_once_with(**kwargs)
        fake_injector.get.assert_called_once_with(GameService)
        fake_game_service.add_game.assert_called_once_with(game)
        fake_flash.assert_called_once_with(f"Game for season={kwargs['season_year']}, league={kwargs['league_name']}, week={kwargs['week']}, with guest={kwargs['guest_name']} and host={kwargs['host_name']} has been successfully submitted.", 'success')
        assert session.get('week') == 1
        fake_url_for.assert_called_once_with('game.create')
        fake_redirect.assert_called_once_with(fake_url_for.return_value)
        assert result is fake_redirect.return_value


@patch('app.flask.game_controller.render_template')
@patch('app.flask.game_controller.flash')
@patch('app.flask.game_controller.injector')
@patch('app.flask.game_controller.game_factory')
@patch('app.flask.game_controller.NewGameForm')
def test_create_when_form_submitted_and_value_error_caught_should_flash_error_message_and_render_create_template(
        fake_form, fake_game_factory, fake_injector,
        fake_flash, fake_render_template, test_app
):
    # Arrange
    err = ValueError()
    fake_game_service, game = _set_up_create_post(fake_injector, fake_form, fake_game_factory, err=err)

    # Act
    with test_app.test_request_context('/games/create', method='POST'):
        result = mod.create()

    # Assert
    kwargs = {
        'season_year': 1920,
        'league_name': "A",
        'week': 1,
        'guest_name': "Guest",
        'guest_score': 3,
        'host_name': "Host",
        'host_score': 3,
        'is_playoff': False,
        'notes': None,
    }

    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    fake_game_factory.create_game.assert_called_once_with(**kwargs)
    fake_injector.get.assert_called_once_with(GameService)
    fake_game_service.add_game.assert_called_once_with(game)
    fake_flash.assert_called_once_with(str(err), 'danger')
    fake_render_template.assert_called_once_with(
        'games/create.html', form=fake_form.return_value, game=None
    )
    assert result is fake_render_template.return_value


@patch('app.flask.game_controller.render_template')
@patch('app.flask.game_controller.flash')
@patch('app.flask.game_controller.injector')
@patch('app.flask.game_controller.game_factory')
@patch('app.flask.game_controller.NewGameForm')
def test_create_when_form_submitted_and_integrity_error_caught_for_primary_key_constraint_violation_on_id_should_flash_error_message_and_render_create_template(
        fake_form, fake_game_factory, fake_injector,
        fake_flash, fake_render_template, test_app
):
    # Arrange
    err = IntegrityError(
        'statement', 'params',
        Exception("Violation of PRIMARY KEY constraint")
    )
    fake_game_service, game = _set_up_create_post(fake_injector, fake_form, fake_game_factory, err=err)

    # Act
    with test_app.test_request_context('/games/create', method='POST'):
        result = mod.create()

    # Assert
    kwargs = {
        'season_year': 1920,
        'league_name': "A",
        'week': 1,
        'guest_name': "Guest",
        'guest_score': 3,
        'host_name': "Host",
        'host_score': 3,
        'is_playoff': False,
        'notes': None,
    }

    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    fake_game_factory.create_game.assert_called_once_with(**kwargs)
    fake_injector.get.assert_called_once_with(GameService)
    fake_game_service.add_game.assert_called_once_with(game)
    fake_flash.assert_called_once_with("A game with the same id already exists.", 'danger')
    fake_render_template.assert_called_once_with(
        'games/create.html', form=fake_form.return_value, game=None
    )
    assert result is fake_render_template.return_value


@patch('app.flask.game_controller.render_template')
@patch('app.flask.game_controller.flash')
@patch('app.flask.game_controller.injector')
@patch('app.flask.game_controller.game_factory')
@patch('app.flask.game_controller.NewGameForm')
def test_create_when_form_submitted_and_integrity_error_caught_for_unique_key_constraint_violation_should_flash_error_message_and_render_create_template(
        fake_form, fake_game_factory, fake_injector,
        fake_flash, fake_render_template, test_app
):
    # Arrange
    err = IntegrityError(
        'statement', 'params',
        Exception("Violation of UNIQUE KEY constraint 'UQ_Game_Season_League_Week_Teams'")
    )
    fake_game_service, game = _set_up_create_post(fake_injector, fake_form, fake_game_factory, err=err)

    # Act
    with test_app.test_request_context('/games/create', method='POST'):
        result = mod.create()

    # Assert
    kwargs = {
        'season_year': 1920,
        'league_name': "A",
        'week': 1,
        'guest_name': "Guest",
        'guest_score': 3,
        'host_name': "Host",
        'host_score': 3,
        'is_playoff': False,
        'notes': None,
    }

    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    fake_game_factory.create_game.assert_called_once_with(**kwargs)
    fake_injector.get.assert_called_once_with(GameService)
    fake_game_service.add_game.assert_called_once_with(game)
    fake_flash.assert_called_once_with(
        "A game with the same season, league, week, guest, and host already exists.", 'danger'
    )
    fake_render_template.assert_called_once_with(
        'games/create.html', form=fake_form.return_value, game=None
    )
    assert result is fake_render_template.return_value


@patch('app.flask.game_controller.render_template')
@patch('app.flask.game_controller.flash')
@patch('app.flask.game_controller.injector')
@patch('app.flask.game_controller.game_factory')
@patch('app.flask.game_controller.NewGameForm')
def test_create_when_form_submitted_and_integrity_error_caught_for_conflict_with_foreign_key_constraint_on_season_year_should_flash_error_message_and_render_create_template(
        fake_form, fake_game_factory, fake_injector,
        fake_flash, fake_render_template, test_app
):
    # Arrange
    err = IntegrityError(
        'statement', 'params',
        Exception("The INSERT statement conflicted with the FOREIGN KEY constraint 'FK_Game_Season_SeasonYear'")
    )
    fake_game_service, game = _set_up_create_post(fake_injector, fake_form, fake_game_factory, err=err)

    # Act
    with test_app.test_request_context('/games/create', method='POST'):
        result = mod.create()

    # Assert
    kwargs = {
        'season_year': 1920,
        'league_name': "A",
        'week': 1,
        'guest_name': "Guest",
        'guest_score': 3,
        'host_name': "Host",
        'host_score': 3,
        'is_playoff': False,
        'notes': None,
    }

    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    fake_game_factory.create_game.assert_called_once_with(**kwargs)
    fake_injector.get.assert_called_once_with(GameService)
    fake_game_service.add_game.assert_called_once_with(game)
    fake_flash.assert_called_once_with("FOREIGN KEY constraint violation on season year.", 'danger')
    fake_render_template.assert_called_once_with(
        'games/create.html', form=fake_form.return_value, game=None
    )
    assert result is fake_render_template.return_value


@patch('app.flask.game_controller.render_template')
@patch('app.flask.game_controller.flash')
@patch('app.flask.game_controller.injector')
@patch('app.flask.game_controller.game_factory')
@patch('app.flask.game_controller.NewGameForm')
def test_create_when_form_submitted_and_integrity_error_caught_for_conflict_with_foreign_key_constraint_on_league_name_should_flash_error_message_and_render_create_template(
        fake_form, fake_game_factory, fake_injector,
        fake_flash, fake_render_template, test_app
):
    # Arrange
    err = IntegrityError(
        'statement', 'params',
        Exception("The INSERT statement conflicted with the FOREIGN KEY constraint 'FK_Game_Association_LeagueId'")
    )
    fake_game_service, game = _set_up_create_post(fake_injector, fake_form, fake_game_factory, err=err)

    # Act
    with test_app.test_request_context('/games/create', method='POST'):
        result = mod.create()

    # Assert
    kwargs = {
        'season_year': 1920,
        'league_name': "A",
        'week': 1,
        'guest_name': "Guest",
        'guest_score': 3,
        'host_name': "Host",
        'host_score': 3,
        'is_playoff': False,
        'notes': None,
    }

    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    fake_game_factory.create_game.assert_called_once_with(**kwargs)
    fake_injector.get.assert_called_once_with(GameService)
    fake_game_service.add_game.assert_called_once_with(game)
    fake_flash.assert_called_once_with("FOREIGN KEY constraint violation on league name.", 'danger')
    fake_render_template.assert_called_once_with(
        'games/create.html', form=fake_form.return_value, game=None
    )
    assert result is fake_render_template.return_value


@patch('app.flask.game_controller.render_template')
@patch('app.flask.game_controller.flash')
@patch('app.flask.game_controller.injector')
@patch('app.flask.game_controller.game_factory')
@patch('app.flask.game_controller.NewGameForm')
def test_create_when_form_submitted_and_integrity_error_caught_for_something_else_should_flash_error_message_and_render_create_template(
        fake_form, fake_game_factory, fake_injector,
        fake_flash, fake_render_template, test_app
):
    # Arrange
    err = IntegrityError(
        'statement', 'params',
        Exception("Something else")
    )
    fake_game_service, game = _set_up_create_post(fake_injector, fake_form, fake_game_factory, err=err)

    # Act
    with test_app.test_request_context('/games/create', method='POST'):
        result = mod.create()

    # Assert
    kwargs = {
        'season_year': 1920,
        'league_name': "A",
        'week': 1,
        'guest_name': "Guest",
        'guest_score': 3,
        'host_name': "Host",
        'host_score': 3,
        'is_playoff': False,
        'notes': None,
    }

    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    fake_game_factory.create_game.assert_called_once_with(**kwargs)
    fake_injector.get.assert_called_once_with(GameService)
    fake_game_service.add_game.assert_called_once_with(game)
    fake_flash.assert_called_once_with("An unexpected error occurred.", 'danger')
    fake_render_template.assert_called_once_with(
        'games/create.html', form=fake_form.return_value, game=None
    )
    assert result is fake_render_template.return_value


def _set_up_create_post(
        fake_injector, fake_form, fake_game_factory, err: Optional[Exception] = None
) -> tuple[Game, MagicMock]:
    game = Game(
        season_year=1920,
        season=Season(year=1920),
        league_id = 1,
        league=Association(id=1, long_name="Association", short_name="A"),
        week=1,
        guest_name="Guest",
        guest_score=3,
        host_name="Host",
        host_score=3
    )

    form = fake_form.return_value
    form.validate_on_submit.return_value = True
    form.season_year.data = game.season.year
    form.league_name.data = game.league.short_name
    form.week.data = game.week
    form.guest_name.data = game.guest_name
    form.guest_score.data = game.guest_score
    form.host_name.data = game.host_name
    form.host_score.data = game.host_score
    form.is_playoff.data = False
    form.notes.data = None

    fake_game_factory.create_game.return_value = game

    fake_game_service = MagicMock(GameService)
    if err:
        fake_game_service.add_game.side_effect = err
    fake_injector.get.return_value = fake_game_service

    return fake_game_service, game


@patch('app.flask.game_controller.copy')
@patch('app.flask.game_controller.injector')
def test_edit_when_game_not_found_should_abort_with_404_error(fake_injector, fake_copy):
    # Arrange
    old_game_copy = None
    fake_game_repository, old_game, new_game, fake_game_service = (
        _set_up_edit(fake_injector, fake_copy, old_game_copy=old_game_copy)
    )

    # Act
    with pytest.raises(NotFound):
        _ = mod.edit(1)

    # Assert
    fake_injector.get.assert_called_once_with(GameRepository)
    fake_game_repository.get_game.assert_called_once()
    fake_copy.deepcopy.assert_called_once_with(old_game)
    fake_game_service.update_game.assert_not_called()


@patch('app.flask.game_controller.render_template')
@patch('app.flask.game_controller.flash')
@patch('app.flask.game_controller.EditGameForm')
@patch('app.flask.game_controller.copy')
@patch('app.flask.game_controller.injector')
def test_edit_when_game_found_and_form_not_submitted_and_no_form_errors_should_render_edit_template(
        fake_injector, fake_copy, fake_form, fake_flash,
        fake_render_template
):
    # Arrange
    fake_game_repository, old_game, old_game_copy, fake_game_service = (
        _set_up_edit_get(fake_injector, fake_copy, fake_form)
    )

    # Act
    id = 1
    result = mod.edit(id)

    # Assert
    fake_injector.get.assert_called_once_with(GameRepository)
    fake_game_repository.get_game.assert_called_once_with(id)
    fake_copy.deepcopy.assert_called_once_with(old_game)
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    fake_game_service.update_game.assert_not_called()

    form = fake_form.return_value
    assert form.season_year.data == old_game_copy.season.year
    assert form.league_name.data == old_game_copy.league.short_name
    assert form.week.data == old_game_copy.week
    assert form.guest_name.data == old_game_copy.guest_name
    assert form.guest_score.data == old_game_copy.guest_score
    assert form.host_name.data == old_game_copy.host_name
    assert form.host_score.data == old_game_copy.host_score
    assert form.is_playoff.data == old_game_copy.is_playoff
    assert form.notes.data == old_game_copy.notes

    fake_flash.assert_not_called()
    fake_render_template.assert_called_once_with(
        'games/edit.html', game=old_game_copy, form=fake_form.return_value
    )
    assert result is fake_render_template.return_value


@patch('app.flask.game_controller.render_template')
@patch('app.flask.game_controller.flash')
@patch('app.flask.game_controller.EditGameForm')
@patch('app.flask.game_controller.copy')
@patch('app.flask.game_controller.injector')
def test_edit_when_game_found_and_form_not_submitted_and_form_errors_should_flash_errors_and_render_edit_template(
        fake_injector, fake_copy, fake_form,
        fake_flash, fake_render_template
):
    # Arrange
    errors = 'errors'
    fake_game_repository, old_game, old_game_copy, fake_game_service = (
        _set_up_edit_get(fake_injector, fake_copy, fake_form, errors=errors)
    )

    # Act
    result = mod.edit(1)

    # Assert
    fake_injector.get.assert_called_once_with(GameRepository)
    fake_game_repository.get_game.assert_called_once()
    fake_copy.deepcopy.assert_called_once_with(old_game)
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    fake_game_service.update_game.assert_not_called()
    form = fake_form.return_value
    assert form.season_year.data == old_game_copy.season.year
    assert form.league_name.data == old_game_copy.league.short_name
    assert form.week.data == old_game_copy.week
    assert form.guest_name.data == old_game_copy.guest_name
    assert form.guest_score.data == old_game_copy.guest_score
    assert form.host_name.data == old_game_copy.host_name
    assert form.host_score.data == old_game_copy.host_score
    assert form.is_playoff.data == old_game_copy.is_playoff
    assert form.notes.data == old_game_copy.notes
    fake_flash.assert_called_once_with(f"{errors}", 'danger')
    fake_render_template.assert_called_once_with(
        'games/edit.html', form=fake_form.return_value, game=old_game_copy
    )
    assert result is fake_render_template.return_value


def _set_up_edit_get(
        fake_injector, fake_copy, fake_form, errors: Optional[str] = None
) -> tuple[MagicMock, Game, Game, MagicMock]:
    old_game_copy = MagicMock(Game)
    old_game_copy.season_year = 1920
    old_game_copy.season = Season(year=1920)
    old_game_copy.league_id = 1
    old_game_copy.league = Association(id=1, long_name="League", short_name="L", parent_id=None)
    old_game_copy.week = 1
    old_game_copy.guest_name = "Guest"
    old_game_copy.guest_score = 2
    old_game_copy.host_name = "Host"
    old_game_copy.host_score = 3
    old_game_copy.is_playoff = False
    old_game_copy.notes = None
    fake_game_repository, old_game, _, fake_game_service = (
        _set_up_edit(fake_injector, fake_copy, old_game_copy=old_game_copy)
    )

    form = fake_form.return_value
    form.validate_on_submit.return_value = False
    form.errors = errors

    return fake_game_repository, old_game, old_game_copy, fake_game_service


@patch('app.flask.game_controller.url_for')
@patch('app.flask.game_controller.redirect')
@patch('app.flask.game_controller.flash')
@patch('app.flask.game_controller.game_factory')
@patch('app.flask.game_controller.EditGameForm')
@patch('app.flask.game_controller.copy')
@patch('app.flask.game_controller.injector')
def test_edit_when_game_found_and_form_submitted_and_no_errors_caught_should_flash_success_message_and_redirect_to_game_details(
        fake_injector, fake_copy, fake_form,
        fake_game_factory, fake_flash,
        fake_redirect, fake_url_for
):
    # Arrange
    fake_game_repository, old_game, old_game_copy, new_game, fake_game_service = (
        _set_up_edit_post(fake_injector, fake_game_factory, fake_copy, fake_form)
    )

    # Act
    id = 1
    result = mod.edit(id)

    # Assert
    fake_injector.get.assert_has_calls([
        call(GameRepository),
        call(GameService),
    ])
    fake_game_repository.get_game.assert_called_once()
    fake_copy.deepcopy.assert_called_once_with(old_game)
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    kwargs = {
        'id': id,
        'season_year': 1921,
        'league_name': "L2",
        'week': 2,
        'guest_name': "Guest 2",
        'guest_score': 3,
        'host_name': "Host 2",
        'host_score': 2,
        'is_playoff': True,
        'notes': "Notes",
    }
    fake_game_factory.create_game.assert_called_once_with(**kwargs)
    fake_game_service.update_game.assert_called_once_with(fake_game_factory.create_game.return_value, old_game_copy)
    fake_flash.assert_called_once_with(
        f"Game for season={fake_form.return_value.season_year.data}, league={fake_form.return_value.league_name.data}, and week={fake_form.return_value.week.data} with guest={fake_form.return_value.guest_name.data} and host={fake_form.return_value.host_name.data} has been successfully updated.",
        'success'
    )
    fake_url_for.assert_called_once_with('game.details', id=id)
    fake_redirect.assert_called_once_with(fake_url_for.return_value)
    assert result is fake_redirect.return_value


@patch('app.flask.game_controller.render_template')
@patch('app.flask.game_controller.flash')
@patch('app.flask.game_controller.game_factory')
@patch('app.flask.game_controller.EditGameForm')
@patch('app.flask.game_controller.copy')
@patch('app.flask.game_controller.injector')
def test_edit_when_game_found_and_form_submitted_and_value_error_caught_should_flash_error_message_and_render_edit_template(
        fake_injector, fake_copy, fake_form,
        fake_game_factory, fake_flash, fake_render_template
):
    # Arrange
    err = ValueError()
    fake_game_repository, old_game, old_game_copy, new_game, fake_game_service = (
        _set_up_edit_post(fake_injector, fake_game_factory, fake_copy, fake_form, err=err)
    )

    err = ValueError()
    fake_game_service.update_game.side_effect = err

    # Act
    id = 1
    result = mod.edit(id)

    # Assert
    fake_injector.get.assert_has_calls([
        call(GameRepository),
        call(GameService),
    ])
    fake_game_repository.get_game.assert_called_once()
    fake_copy.deepcopy.assert_called_once_with(old_game)
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    kwargs = {
        'id': id,
        'season_year': 1921,
        'league_name': "L2",
        'week': 2,
        'guest_name': "Guest 2",
        'guest_score': 3,
        'host_name': "Host 2",
        'host_score': 2,
        'is_playoff': True,
        'notes': "Notes",
    }
    fake_game_factory.create_game.assert_called_once_with(**kwargs)
    fake_flash.assert_called_once_with(str(err), 'danger')
    fake_render_template.assert_called_once_with(
        'games/edit.html', form=fake_form.return_value, game=old_game_copy
    )
    assert result is fake_render_template.return_value


@patch('app.flask.game_controller.render_template')
@patch('app.flask.game_controller.flash')
@patch('app.flask.game_controller.game_factory')
@patch('app.flask.game_controller.EditGameForm')
@patch('app.flask.game_controller.copy')
@patch('app.flask.game_controller.injector')
def test_edit_when_game_found_and_form_submitted_and_integrity_error_caught_for_unique_key_constraint_violation_should_flash_error_message_and_render_edit_template(
        fake_injector, fake_copy, fake_form,
        fake_game_factory, fake_flash, fake_render_template
):
    # Arrange
    err = IntegrityError(
        'statement', 'params',
        Exception("Violation of UNIQUE KEY constraint 'UQ_Game_Season_League_Week_Teams'")
    )
    fake_game_repository, old_game, old_game_copy, new_game, fake_game_service = (
        _set_up_edit_post(fake_injector, fake_game_factory, fake_copy, fake_form, err=err)
    )

    # Act
    id = 1
    result = mod.edit(id)

    # Assert
    fake_injector.get.assert_has_calls([
        call(GameRepository),
        call(GameService),
    ])
    fake_game_repository.get_game.assert_called_once()
    fake_copy.deepcopy.assert_called_once_with(old_game)
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    kwargs = {
        'id': id,
        'season_year': 1921,
        'league_name': "L2",
        'week': 2,
        'guest_name': "Guest 2",
        'guest_score': 3,
        'host_name': "Host 2",
        'host_score': 2,
        'is_playoff': True,
        'notes': "Notes",
    }
    fake_game_factory.create_game.assert_called_once_with(**kwargs)
    fake_flash.assert_called_once_with(
        "A game with the same season, league, week, guest, and host already exists.", 'danger'
    )
    fake_render_template.assert_called_once_with(
        'games/edit.html', form=fake_form.return_value, game=old_game_copy
    )
    assert result is fake_render_template.return_value


@patch('app.flask.game_controller.render_template')
@patch('app.flask.game_controller.flash')
@patch('app.flask.game_controller.game_factory')
@patch('app.flask.game_controller.EditGameForm')
@patch('app.flask.game_controller.copy')
@patch('app.flask.game_controller.injector')
def test_edit_when_game_found_and_form_submitted_and_integrity_error_caught_for_conflict_with_foreign_key_constraint_on_season_year_should_flash_error_message_and_render_edit_template(
        fake_injector, fake_copy, fake_form,
        fake_game_factory, fake_flash, fake_render_template
):
    # Arrange
    err = IntegrityError(
        'statement', 'params',
        Exception("The UPDATE statement conflicted with the FOREIGN KEY constraint 'FK_Game_Season_SeasonYear'")
    )
    fake_game_repository, old_game, old_game_copy, new_game, fake_game_service = (
        _set_up_edit_post(fake_injector, fake_game_factory, fake_copy, fake_form, err=err)
    )

    # Act
    id = 1
    result = mod.edit(id)

    # Assert
    fake_injector.get.assert_has_calls([
        call(GameRepository),
        call(GameService),
    ])
    fake_game_repository.get_game.assert_called_once()
    fake_copy.deepcopy.assert_called_once_with(old_game)
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    kwargs = {
        'id': id,
        'season_year': 1921,
        'league_name': "L2",
        'week': 2,
        'guest_name': "Guest 2",
        'guest_score': 3,
        'host_name': "Host 2",
        'host_score': 2,
        'is_playoff': True,
        'notes': "Notes",
    }
    fake_game_factory.create_game.assert_called_once_with(**kwargs)
    fake_flash.assert_called_once_with("FOREIGN KEY constraint violation on season year.", 'danger')
    fake_render_template.assert_called_once_with(
        'games/edit.html', form=fake_form.return_value, game=old_game_copy
    )
    assert result is fake_render_template.return_value


@patch('app.flask.game_controller.render_template')
@patch('app.flask.game_controller.flash')
@patch('app.flask.game_controller.game_factory')
@patch('app.flask.game_controller.EditGameForm')
@patch('app.flask.game_controller.copy')
@patch('app.flask.game_controller.injector')
def test_edit_when_game_found_and_form_submitted_and_integrity_error_caught_for_conflict_with_foreign_key_constraint_on_league_name_should_flash_error_message_and_render_edit_template(
        fake_injector, fake_copy, fake_form,
        fake_game_factory, fake_flash, fake_render_template
):
    # Arrange
    err = IntegrityError(
        'statement', 'params',
        Exception("The UPDATE statement conflicted with the FOREIGN KEY constraint 'FK_Game_Association_LeagueId'")
    )
    fake_game_repository, old_game, old_game_copy, new_game, fake_game_service = (
        _set_up_edit_post(fake_injector, fake_game_factory, fake_copy, fake_form, err=err)
    )

    # Act
    id = 1
    result = mod.edit(id)

    # Assert
    fake_injector.get.assert_has_calls([
        call(GameRepository),
        call(GameService),
    ])
    fake_game_repository.get_game.assert_called_once()
    fake_copy.deepcopy.assert_called_once_with(old_game)
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    kwargs = {
        'id': id,
        'season_year': 1921,
        'league_name': "L2",
        'week': 2,
        'guest_name': "Guest 2",
        'guest_score': 3,
        'host_name': "Host 2",
        'host_score': 2,
        'is_playoff': True,
        'notes': "Notes",
    }
    fake_game_factory.create_game.assert_called_once_with(**kwargs)
    fake_flash.assert_called_once_with("FOREIGN KEY constraint violation on league name.", 'danger')
    fake_render_template.assert_called_once_with(
        'games/edit.html', form=fake_form.return_value, game=old_game_copy
    )
    assert result is fake_render_template.return_value


@patch('app.flask.game_controller.render_template')
@patch('app.flask.game_controller.flash')
@patch('app.flask.game_controller.game_factory')
@patch('app.flask.game_controller.EditGameForm')
@patch('app.flask.game_controller.copy')
@patch('app.flask.game_controller.injector')
def test_edit_when_game_found_and_form_submitted_and_integrity_error_caught_for_something_else_should_flash_error_message_and_render_edit_template(
        fake_injector, fake_copy, fake_form,
        fake_game_factory, fake_flash, fake_render_template
):
    # Arrange
    err = IntegrityError(
        'statement', 'params',
        Exception("Something else")
    )
    fake_game_repository, old_game, old_game_copy, new_game, fake_game_service = (
        _set_up_edit_post(fake_injector, fake_game_factory, fake_copy, fake_form, err=err)
    )

    # Act
    id = 1
    result = mod.edit(id)

    # Assert
    fake_injector.get.assert_has_calls([
        call(GameRepository),
        call(GameService),
    ])
    fake_game_repository.get_game.assert_called_once()
    fake_copy.deepcopy.assert_called_once_with(old_game)
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    kwargs = {
        'id': id,
        'season_year': 1921,
        'league_name': "L2",
        'week': 2,
        'guest_name': "Guest 2",
        'guest_score': 3,
        'host_name': "Host 2",
        'host_score': 2,
        'is_playoff': True,
        'notes': "Notes",
    }
    fake_game_factory.create_game.assert_called_once_with(**kwargs)
    fake_flash.assert_called_once_with("An unexpected error occurred.", 'danger')
    fake_render_template.assert_called_once_with(
        'games/edit.html', form=fake_form.return_value, game=old_game_copy
    )
    assert result is fake_render_template.return_value


@patch('app.flask.game_controller.game_factory')
@patch('app.flask.game_controller.EditGameForm')
@patch('app.flask.game_controller.url_for')
@patch('app.flask.game_controller.redirect')
@patch('app.flask.game_controller.copy')
@patch('app.flask.game_controller.injector')
def test_edit_when_game_found_and_form_submitted_and_index_error_caught_should_abort_with_404_error(
        fake_injector, fake_copy, fake_redirect, fake_url_for, fake_form,
        fake_game_factory,
):
    # Arrange
    err = IndexError()
    fake_game_repository, old_game, old_game_copy, new_game, fake_game_service = (
        _set_up_edit_post(fake_injector, fake_game_factory, fake_copy, fake_form, err=err)
    )

    # Act
    id = 1
    with pytest.raises(NotFound):
        result = mod.edit(id)

    # Assert
    fake_injector.get.assert_has_calls([
        call(GameRepository),
        call(GameService),
    ])
    fake_game_repository.get_game.assert_called_once_with(id)
    fake_copy.deepcopy.assert_called_once_with(old_game)
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    kwargs = {
        'id': id,
        'season_year': 1921,
        'league_name': "L2",
        'week': 2,
        'guest_name': "Guest 2",
        'guest_score': 3,
        'host_name': "Host 2",
        'host_score': 2,
        'is_playoff': True,
        'notes': "Notes",
    }
    fake_game_factory.create_game.assert_called_once_with(**kwargs)


def _set_up_edit_post(
        fake_injector, fake_game_factory, fake_copy, fake_form,
        err: Optional[Exception] = None
) -> tuple[MagicMock, MagicMock, MagicMock, MagicMock, MagicMock]:
    old_game_copy = MagicMock(Game)
    old_game_copy.season_year = 1920
    old_game_copy.season = Season(year=1920)
    old_game_copy.league_id = 1
    old_game_copy.league = Association(id=1, long_name="League", short_name="L")
    old_game_copy.week = 1
    old_game_copy.guest_name = "Guest"
    old_game_copy.guest_score.data = 2
    old_game_copy.host_name = "Host"
    old_game_copy.host_score.data = 3
    old_game_copy.is_playoff = False
    old_game_copy.notes = None
    fake_copy.deepcopy.return_value = old_game_copy
    fake_game_repository, old_game, new_game, fake_game_service = (
        _set_up_edit(fake_injector, fake_copy, old_game_copy=old_game_copy, fake_game_factory=fake_game_factory)
    )

    form = fake_form.return_value
    form.validate_on_submit.return_value = True
    form.season_year.data = 1921
    form.league_name.data = "L2"
    form.week.data = 2
    form.guest_name.data = "Guest 2"
    form.guest_score.data = 3
    form.host_name.data = "Host 2"
    form.host_score.data = 2
    form.is_playoff.data = True
    form.notes.data = "Notes"

    if err:
        fake_game_service.update_game.side_effect = err

    return fake_game_repository, old_game, old_game_copy, new_game, fake_game_service


@patch('app.flask.game_controller.injector')
def test_delete_when_game_not_found_should_abort_with_404_error(fake_injector, test_app):
    # Arrange
    fake_game_repository, fake_game_service = _set_up_delete(fake_injector)

    # Act
    id = 1
    with test_app.test_request_context(f'/games/delete?id={id}', method='POST'):
        with pytest.raises(NotFound):
            _ = mod.delete(id)

    # Assert
    fake_injector.get.assert_called_once_with(GameRepository)
    fake_game_repository.get_game.assert_called_once_with(id)
    fake_game_service.delete_game.assert_not_called()


@patch('app.flask.game_controller.render_template')
@patch('app.flask.game_controller.injector')
@patch('app.flask.game_controller.DeleteGameForm')
def test_delete_when_request_method_is_get_should_render_delete_template(
        fake_form, fake_injector, fake_render_template,
        test_app
):
    # Arrange
    game = Game(
        season_year=1920,
        season=Season(year=1920),
        league_id = 1,
        league=Association(id=1, long_name="Association", short_name="A"),
        week=1,
        guest_name="Guest",
        guest_score=2,
        host_name="Host",
        host_score=3
    )
    fake_game_repository, fake_game_service = _set_up_delete(fake_injector, game=game)

    # Act
    id = 1
    with test_app.test_request_context(f'/games/delete?id={id}', method='GET'):
        result = mod.delete(id)

        # Assert
        fake_form.assert_called_once()
        fake_injector.get.assert_called_once_with(GameRepository)
        fake_game_repository.get_game.assert_called_once_with(id)
        fake_game_service.delete_game.assert_not_called()
        fake_render_template.assert_called_once_with('games/delete.html', form=fake_form.return_value, game=game)
        assert result is fake_render_template.return_value


@patch('app.flask.game_controller.redirect')
@patch('app.flask.game_controller.url_for')
@patch('app.flask.game_controller.flash')
@patch('app.flask.game_controller.injector')
def test_delete_when_request_method_is_post_and_game_found_should_delete_game_and_flash_success_message_and_redirect_to_games_index(
        fake_injector, fake_flash, fake_url_for,
        fake_redirect, test_app
):
    # Arrange
    game = Game(
        season_year=1920,
        season=Season(year=1920),
        league_id = 1,
        league=Association(id=1, long_name="Association", short_name="A"),
        week=1,
        guest_name="Guest",
        guest_score=2,
        host_name="Host",
        host_score=3
    )
    fake_game_repository, fake_game_service = _set_up_delete(fake_injector, game)

    # Act
    id = 1
    with test_app.test_request_context('/games/delete?id=1', method='POST'):
        result = mod.delete(id)

    # Assert
    fake_injector.get.assert_has_calls([
        call(GameRepository),
        call(GameService),
    ])
    fake_game_repository.get_game.assert_called_once_with(id)
    fake_game_service.delete_game.assert_called_once_with(id)
    fake_flash.assert_called_once_with(
        f"Game for season={game.season.year}, league={game.league.short_name}, and week={game.week} with guest={game.guest_name} and host={game.host_name} has been successfully deleted.",
        'success'
    )
    fake_url_for.assert_called_once_with('game.index')
    fake_redirect.assert_called_once_with(fake_url_for.return_value)
    assert result is fake_redirect.return_value


@patch('app.flask.game_controller.injector')
def test_delete_when_request_method_is_post_and_index_error_is_caught_should_abort_with_404_error(
        fake_injector, test_app
):
    # Arrange
    game = Game()
    err = IndexError()
    fake_game_repository, fake_game_service = _set_up_delete(fake_injector, game, err=err)

    # Act
    id = 1
    with test_app.test_request_context(f'/games/delete?id={id}', method='POST'):
        with pytest.raises(NotFound):
            _ = mod.delete(id)

    # Assert
    fake_injector.get.assert_has_calls([
        call(GameRepository),
        call(GameService),
    ])
    fake_game_repository.get_game.assert_called_once_with(id)
    fake_game_service.delete_game.assert_called_once_with(id)


def _set_up_delete(fake_injector, game: Optional[Game] = None, err: Optional[Exception] = None)\
        -> tuple[MagicMock, MagicMock]:
    fake_game_repository = MagicMock(GameRepository)
    fake_game_repository.get_game.return_value = game

    fake_game_service = MagicMock(GameService)
    if err:
        fake_game_service.delete_game.side_effect = err

    fake_injector.get.side_effect = [fake_game_repository, fake_game_service]

    return fake_game_repository, fake_game_service


@pytest.mark.skip('WIP')
@patch('app.flask.game_controller.render_template')
@patch('app.flask.game_controller.injector')
@patch('app.flask.game_controller.request')
def test_select_season_should_render_game_index_template_for_selected_season(
        fake_request, fake_injector, fake_render_template, test_app
):
    with test_app.test_request_context('/season_standings/select_season', method='POST'):
        # Arrange
        selected_season_year = 1920
        fake_request.form.get.return_value = str(selected_season_year)

        seasons = [
            Season(1920),
            Season(1921),
            Season(1922),
        ]
        session['seasons'] = [s.to_dict() for s in seasons]

        fake_association_repository = MagicMock(AssociationRepository)
        associations = [
            Association(
                id=1,
                long_name="American Professional Football Association",
                short_name="APFA",
                parent_id=None,
                first_season_year=1920,
                last_season_year=1922
            ),
            Association(
                id=2,
                long_name="National Football League",
                short_name="NFL",
                parent_id=None,
                first_season_year=1922
            ),
            Association(
                id=3,
                long_name="National Football Conference",
                short_name="NFC",
                parent_id=2,
                first_season_year=1970
            ),
            Association(
                id=4,
                long_name="American Football Conference",
                short_name="AFC",
                parent_id=2,
                first_season_year=1970
            ),
        ]
        fake_association_repository.get_associations.return_value = associations
        leagues = [a for a in associations if a.parent_id is None]
        active_leagues = [l for l in leagues if l.first_season.year <= selected_season_year
                          and (l.last_season is None or selected_season_year <= l.last_season.year)]
        active_leagues.sort(key=lambda l: l.id, reverse=True)
        selected_league = active_leagues[0]

        fake_league_season_repository = MagicMock(LeagueSeasonRepository)
        league_season = LeagueSeason(id=1, league_id=selected_league.id, season_year=selected_season_year)
        fake_league_season_repository.get_league_season_by_league_and_season.return_value = league_season

        fake_game_repository = MagicMock(GameRepository)
        games = []
        for s in range(1920, 1923):
            for l in range(1, 4):
                for w in range(1, 4):
                    for t in range(1, 4):
                        games.append(
                            Game(
                                id=(9 * s + 3 * l + w),
                                season_year=s,
                                league_id=l,
                                week=w,
                                guest_name=f"Guest {t}",
                                guest_score=0,
                                host_name=f"Guest {t}",
                                host_score=0
                            )
                        )
        fake_game_repository.get_games_by_season_league_and_week.return_value = games
        selected_games = [
            g for g in games if g.season_year == selected_season_year and g.league_id == selected_league.id
        ]
        fake_game_repository.get_games_by_season_league_and_week.return_value = selected_games

        fake_injector.get.side_effect = [
            fake_association_repository,
            fake_league_season_repository,
            fake_game_repository
        ]

        # Act
        result = mod.select_season()

        # Assert
        fake_request.form.get.assert_called_once_with('season_dropdown')
        assert session.get('selected_season_year') == selected_season_year
        fake_association_repository.get_associations.assert_called_once()
        assert session.get('leagues') == [l.to_dict() for l in active_leagues]
        assert session.get('selected_league_name') == selected_league.short_name
        fake_league_season_repository.get_league_season_by_league_and_season.assert_called_once_with(
            selected_league.id, selected_season_year
        )
        weeks = [None, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
        assert session.get('weeks') == weeks

        selected_week = None
        assert session.get('selected_week') == selected_week

        fake_injector.get.assert_has_calls(
            call(AssociationRepository),
            call(LeagueSeasonRepository),
            call(GameRepository)
        )
        fake_game_repository.get_games_by_season_league_and_week.assert_called_once_with(
            season_year=selected_season_year, league_id=selected_league.id, week=selected_week
        )
        fake_render_template.assert_called_once_with(
            'games/index.html',
            seasons=seasons, selected_season_year=selected_season_year,
            leagues=active_leagues, selected_league_name=selected_league.short_name,
            weeks=weeks, selected_week=selected_week,
            games=games
        )
        assert result is fake_render_template.return_value


@pytest.mark.skip('WIP')
@patch('app.flask.game_controller.render_template')
@patch('app.flask.game_controller.injector')
@patch('app.flask.game_controller.request')
def test_select_league_should_render_game_index_template_for_selected_league(
        fake_request, fake_injector, fake_render_template, test_app
):
    with test_app.test_request_context('/season_standings/select_season', method='POST'):
        # Arrange
        selected_league_name = "APFA"
        fake_request.form.get.return_value = selected_league_name

        seasons = [
            Season(1920),
            Season(1921),
            Season(1922),
        ]
        session['seasons'] = [s.to_dict() for s in seasons]

        selected_season_year = 1920
        session['selected_season_year'] = selected_season_year

        fake_association_repository = MagicMock(AssociationRepository)
        associations = [
            Association(
                id=1,
                long_name="American Professional Football Association",
                short_name="APFA",
                parent_id=None,
                first_season_year=1920,
                last_season_year=1922
            ),
            Association(
                id=2,
                long_name="National Football League",
                short_name="NFL",
                parent_id=None,
                first_season_year=1922
            ),
            Association(
                id=3,
                long_name="National Football Conference",
                short_name="NFC",
                parent_id=2,
                first_season_year=1970
            ),
            Association(
                id=4,
                long_name="American Football Conference",
                short_name="AFC",
                parent_id=2,
                first_season_year=1970
            ),
        ]
        fake_association_repository.get_associations.return_value = associations
        leagues = [a for a in associations if a.parent_id is None]
        active_leagues = [l for l in leagues if l.first_season.year <= selected_season_year
                          and (l.last_season is None or selected_season_year <= l.last_season.year)]
        active_leagues.sort(key=lambda l: l.id, reverse=True)
        session['leagues'] = active_leagues

        kwargs = [l for l in active_leagues if l['short_name'] == selected_league_name][0]
        selected_league = Association(**kwargs)

        fake_league_season_repository = MagicMock(LeagueSeasonRepository)
        league_season = LeagueSeason(id=1, league_id=selected_league.id, season_year=selected_season_year)
        fake_league_season_repository.get_league_season_by_league_and_season.return_value = league_season

        fake_game_repository = MagicMock(GameRepository)
        games = []
        for s in range(1920, 1923):
            for l in range(1, 4):
                for w in range(1, 4):
                    for t in range(1, 4):
                        games.append(
                            Game(
                                id=(9 * s + 3 * l + w),
                                season_year=s,
                                league_id=l,
                                week=w,
                                guest_name=f"Guest {t}",
                                guest_score=0,
                                host_name=f"Guest {t}",
                                host_score=0
                            )
                        )
        fake_game_repository.get_games_by_season_league_and_week.return_value = games
        selected_games = [
            g for g in games if g.season_year == selected_season_year and g.league_id == selected_league.id
        ]
        fake_game_repository.get_games_by_season_league_and_week.return_value = selected_games

        fake_injector.get.return_value = [fake_league_season_repository, fake_game_repository]

        # Act
        result = mod.select_league()

        # Assert
        fake_request.form.get.assert_called_once_with('league_dropdown')
        assert session.get('selected_league_name') == selected_league_name
        fake_league_season_repository.get_league_season_by_league_and_season.assert_called_once_with(
            selected_league.id, selected_season_year
        )

        weeks = [None, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
        assert session.get('weeks') == weeks

        selected_week = None
        assert session.get('selected_week') == selected_week

        fake_injector.get.assert_has_calls([
            call(LeagueSeasonRepository),
            call(GameRepository),
        ])

        fake_game_repository.get_games_by_season_league_and_week.assert_called_once_with(
            season_year=selected_season_year, league_id=selected_league.id, week=selected_week
        )
        fake_render_template.assert_called_once_with(
            'games/index.html',
            seasons=seasons, selected_season_year=selected_season_year,
            leagues=active_leagues, selected_league_name=selected_league.short_name,
            weeks=weeks, selected_week=selected_week,
            games=games
        )
        assert result is fake_render_template.return_value


@pytest.mark.skip('WIP')
@patch('app.flask.game_controller.render_template')
@patch('app.flask.game_controller.injector')
@patch('app.flask.game_controller.request')
def test_select_week_when_selected_week_is_none_should_render_game_index_template_for_selected_season_and_selected_week(
        fake_request, fake_injector, fake_render_template, test_app
):
    with test_app.test_request_context('/season_standings/select_season', method='POST'):
        # Arrange
        selected_week = None
        fake_request.form.get.return_value = str(selected_week)

        seasons = [
            Season(1920),
            Season(1921),
            Season(1922),
        ]
        session['seasons'] = [s.to_dict() for s in seasons]
        selected_season_year = 1920
        session['selected_season_year'] = selected_season_year

        fake_association_repository = MagicMock(AssociationRepository)
        associations = [
            Association(
                id=1,
                long_name="American Professional Football Association",
                short_name="APFA",
                parent_id=None,
                first_season_year=1920,
                last_season_year=1922
            ),
            Association(
                id=2,
                long_name="National Football League",
                short_name="NFL",
                parent_id=None,
                first_season_year=1922
            ),
            Association(
                id=3,
                long_name="National Football Conference",
                short_name="NFC",
                parent_id=2,
                first_season_year=1970
            ),
            Association(
                id=4,
                long_name="American Football Conference",
                short_name="AFC",
                parent_id=2,
                first_season_year=1970
            ),
        ]
        fake_association_repository.get_associations.return_value = associations
        leagues = [a for a in associations if a.parent_id is None]
        active_leagues = [l for l in leagues if l.first_season.year <= selected_season_year
                          and (l.last_season is None or selected_season_year <= l.last_season.year)]
        active_leagues.sort(key=lambda l: l.id, reverse=True)
        session['leagues'] = active_leagues

        selected_league_name = "APFA"
        session['selected_league_name'] = selected_league_name

        kwargs = [l for l in active_leagues if l['short_name'] == selected_league_name][0]
        selected_league = Association(**kwargs)

        weeks = [None, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
        assert session.get('weeks') == weeks

        fake_game_repository = MagicMock(GameRepository)
        games = []
        for s in range(1920, 1923):
            for l in range(1, 4):
                for w in range(1, 4):
                    for t in range(1, 4):
                        games.append(
                            Game(
                                id=(9 * s + 3 * l + w),
                                season_year=s,
                                league_id=l,
                                week=w,
                                guest_name=f"Guest {t}",
                                guest_score=0,
                                host_name=f"Guest {t}",
                                host_score=0
                            )
                        )
        fake_game_repository.get_games_by_season_league_and_week.return_value = games
        selected_games = [
            g for g in games if g.season_year == selected_season_year and g.league_id == selected_league.id
        ]
        fake_game_repository.get_games_by_season_league_and_week.return_value = selected_games

        fake_injector.get.return_value = fake_game_repository

        # Act
        result = mod.select_week()

    # Assert
    fake_request.form.get.assert_called_once_with('week_dropdown')
    assert session.get('selected_week') == selected_week
    fake_injector.get.assert_called_once_with(GameRepository)
    fake_render_template.assert_called_once_with(
        'games/index.html',
        seasons=seasons, selected_season_year=selected_season_year,
        leagues=active_leagues, selected_league_name=selected_league.short_name,
        weeks=weeks, selected_week=selected_week,
        games=games
    )
    assert result is fake_render_template.return_value


@pytest.mark.skip('WIP')
@patch('app.flask.game_controller.render_template')
@patch('app.flask.game_controller.injector')
@patch('app.flask.game_controller.request')
def test_select_week_when_selected_week_is_not_none_should_render_game_index_template_for_selected_season_and_selected_week(
        fake_request, fake_injector, fake_render_template, test_app
):
    with test_app.test_request_context('/season_standings/select_season', method='POST'):
        # Arrange
        selected_week = 1
        fake_request.form.get.return_value = str(selected_week)

        seasons = [
            Season(1920),
            Season(1921),
            Season(1922),
        ]
        session['seasons'] = [s.to_dict() for s in seasons]
        selected_season_year = 1920
        session['selected_season_year'] = selected_season_year

        fake_association_repository = MagicMock(AssociationRepository)
        associations = [
            Association(
                id=1,
                long_name="American Professional Football Association",
                short_name="APFA",
                parent_id=None,
                first_season_year=1920,
                last_season_year=1922
            ),
            Association(
                id=2,
                long_name="National Football League",
                short_name="NFL",
                parent_id=None,
                first_season_year=1922
            ),
            Association(
                id=3,
                long_name="National Football Conference",
                short_name="NFC",
                parent_id=2,
                first_season_year=1970
            ),
            Association(
                id=4,
                long_name="American Football Conference",
                short_name="AFC",
                parent_id=2,
                first_season_year=1970
            ),
        ]
        fake_association_repository.get_associations.return_value = associations
        leagues = [a for a in associations if a.parent_id is None]
        active_leagues = [l for l in leagues if l.first_season.year <= selected_season_year
                          and (l.last_season is None or selected_season_year <= l.last_season.year)]
        active_leagues.sort(key=lambda l: l.id, reverse=True)
        session['leagues'] = active_leagues

        selected_league_name = "APFA"
        session['selected_league_name'] = selected_league_name

        kwargs = [l for l in active_leagues if l['short_name'] == selected_league_name][0]
        selected_league = Association(**kwargs)

        weeks = [None, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
        assert session.get('weeks') == weeks

        fake_game_repository = MagicMock(GameRepository)
        games = []
        for s in range(1920, 1923):
            for l in range(1, 4):
                for w in range(1, 4):
                    for t in range(1, 4):
                        games.append(
                            Game(
                                id=(9 * s + 3 * l + w),
                                season_year=s,
                                league_id=l,
                                week=w,
                                guest_name=f"Guest {t}",
                                guest_score=0,
                                host_name=f"Guest {t}",
                                host_score=0
                            )
                        )
        fake_game_repository.get_games_by_season_league_and_week.return_value = games
        selected_games = [
            g for g in games if g.season_year == selected_season_year and g.league_id == selected_league.id
        ]
        fake_game_repository.get_games_by_season_league_and_week.return_value = selected_games

        fake_injector.get.return_value = fake_game_repository

        # Act
        result = mod.select_week()

    # Assert
    fake_request.form.get.assert_called_once_with('week_dropdown')
    assert session.get('selected_week') == selected_week
    fake_injector.get.assert_called_once_with(GameRepository)
    fake_render_template.assert_called_once_with(
        'games/index.html',
        seasons=seasons, selected_season_year=selected_season_year,
        leagues=active_leagues, selected_league_name=selected_league.short_name,
        weeks=weeks, selected_week=selected_week,
        games=games
    )
    assert result is fake_render_template.return_value


def _set_up_edit(
        fake_injector, fake_copy, old_game_copy: Optional[Game] = None,
        fake_game_factory: Optional[MagicMock] = None, err: Optional[Exception] = None
) -> tuple[MagicMock, LeagueSeason, LeagueSeason, MagicMock]:
    fake_game_repository = MagicMock(GameRepository)
    old_game = MagicMock(Game)
    fake_game_repository.get_game.return_value = old_game
    if err:
        fake_game_repository.update_game.side_effect = err

    fake_game_service = MagicMock(GameService)

    fake_injector.get.side_effect = [fake_game_repository, fake_game_service]

    fake_copy.deepcopy.return_value = old_game_copy

    new_season_year = 1921
    new_league_id = 2

    new_game = MagicMock(Game)
    new_game.season_year = new_season_year
    new_game.season = Season(year=new_season_year)
    new_game.league_id = new_league_id
    new_game.league = Association(id=new_league_id, long_name="League", short_name="L", parent_id=None)
    new_game.week = 2
    new_game.guest_name = "Guest 2"
    new_game.guest_score = 3
    new_game.host_name = "Host 2"
    new_game.host_score = 3
    new_game.is_playoff = False
    new_game.notes = None
    if fake_game_factory:
        fake_game_factory.create_game.return_value = new_game

    return fake_game_repository, old_game, new_game, fake_game_service
