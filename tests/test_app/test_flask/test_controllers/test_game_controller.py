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
    # Set up seasons.
    fake_season_repository = MagicMock(SeasonRepository)
    seasons = [
        Season(year=1920),
        Season(year=1921),
        Season(year=1922),
    ]
    seasons.sort(key=lambda s: s.year, reverse=True)
    default_season_year = seasons[0].year
    fake_season_repository.get_seasons.return_value = seasons

    # Set up leagues.
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
    active_leagues = [l for l in leagues if l.first_season_year <= default_season_year
                      and (l.last_season is None or default_season_year <= l.last_season_year)]
    active_leagues.sort(key=lambda l: l.id, reverse=True)
    default_league = active_leagues[0]
    fake_association_repository.get_associations.return_value = associations

    # Set up league season.
    fake_league_season_repository = MagicMock(LeagueSeasonRepository)
    selected_league_season = LeagueSeason(
        id=1,
        league_id=1,
        season_year=1920,
        num_of_weeks_scheduled=13,
    )
    fake_league_season_repository.get_league_season_by_league_and_season.return_value = selected_league_season

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
        g for g in games if g.season_year == default_season_year and g.league_id == default_league.id
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
        assert session.get('selected_season_year') == default_season_year
        assert session.get('leagues') == [l.to_dict() for l in active_leagues]
        assert session.get('selected_league_name') == default_league.short_name
        fake_league_season_repository.get_league_season_by_league_and_season.assert_called_once_with(
            default_league.id, default_season_year
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
            season_year=default_season_year, league_id=default_league.id, week=selected_week
        )
        fake_render_template.assert_called_once_with(
            'games/index.html',
            seasons=seasons, selected_season_year=default_season_year,
            leagues=active_leagues, selected_league_name=default_league.short_name,
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
    # Set up seasons.
    fake_season_repository = MagicMock(SeasonRepository)
    seasons = [
        Season(year=1920),
        Season(year=1921),
        Season(year=1922),
    ]
    seasons.sort(key=lambda s: s.year, reverse=True)
    selected_season_year = 1920
    fake_season_repository.get_seasons.return_value = seasons

    # Set up leagues.
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
    default_league = active_leagues[0]
    fake_association_repository.get_associations.return_value = associations

    # Set up league season.
    fake_league_season_repository = MagicMock(LeagueSeasonRepository)
    selected_league_season = LeagueSeason(
        id=1,
        league_id=1,
        season_year=1920,
        num_of_weeks_scheduled=13,
    )
    fake_league_season_repository.get_league_season_by_league_and_season.return_value = selected_league_season

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
        g for g in games if g.season_year == selected_season_year and g.league_id == default_league.id
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
        session['selected_season_year'] = selected_season_year

        selected_league_name = league_name
        session['selected_league_name'] = selected_league_name

        selected_week = None
        session['selected_week'] = selected_week

        result = mod.index()

        # Assert
        fake_season_repository.get_seasons.assert_called_once()
        assert session.get('seasons') == [s.to_dict() for s in seasons]
        assert session.get('selected_season_year') == selected_season_year
        assert session.get('leagues') == [l.to_dict() for l in active_leagues]
        assert session.get('selected_league_name') == default_league.short_name
        fake_league_season_repository.get_league_season_by_league_and_season.assert_called_once_with(
            default_league.id, selected_season_year
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
            season_year=selected_season_year, league_id=default_league.id, week=selected_week
        )
        fake_render_template.assert_called_once_with(
            'games/index.html',
            seasons=seasons, selected_season_year=selected_season_year,
            leagues=active_leagues, selected_league_name=default_league.short_name,
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
    # Set up seasons.
    fake_season_repository = MagicMock(SeasonRepository)
    seasons = [
        Season(year=1920),
        Season(year=1921),
        Season(year=1922),
    ]
    seasons.sort(key=lambda s: s.year, reverse=True)
    selected_season_year = 1920
    fake_season_repository.get_seasons.return_value = seasons

    # Set up leagues.
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
    selected_league_name = "APFA"
    selected_league = [l for l in active_leagues if l.short_name == selected_league_name][0]
    fake_association_repository.get_associations.return_value = associations

    # Set up league season.
    fake_league_season_repository = MagicMock(LeagueSeasonRepository)
    selected_league_season = LeagueSeason(
        id=1,
        league_id=1,
        season_year=1920,
        num_of_weeks_scheduled=13,
    )
    fake_league_season_repository.get_league_season_by_league_and_season.return_value = selected_league_season

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
        g for g in games if g.season_year == selected_season_year and g.league_id == selected_league.id
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
        session['selected_season_year'] = selected_season_year

        session['selected_league_name'] = selected_league_name

        selected_week = None
        session['selected_week'] = selected_week

        result = mod.index()

        # Assert
        fake_season_repository.get_seasons.assert_called_once()
        assert session.get('seasons') == [s.to_dict() for s in seasons]
        assert session.get('selected_season_year') == selected_season_year
        assert session.get('leagues') == [l.to_dict() for l in active_leagues]
        assert session.get('selected_league_name') == selected_league.short_name
        fake_league_season_repository.get_league_season_by_league_and_season.assert_called_once_with(
            selected_league.id, selected_season_year
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
            season_year=selected_season_year, league_id=selected_league.id, week=selected_week
        )
        fake_render_template.assert_called_once_with(
            'games/index.html',
            seasons=seasons, selected_season_year=selected_season_year,
            leagues=active_leagues, selected_league_name=selected_league.short_name,
            weeks=weeks, selected_week=selected_week,
            games=selected_games
        )
        assert result is fake_render_template.return_value


@patch('app.flask.game_controller.render_template')
@patch('app.flask.game_controller.injector')
@patch('app.flask.game_controller.DeleteGameForm')
def test_details_when_game_found_should_render_game_details_template(
        fake_form, fake_injector, fake_render_template
):
    # Arrange
    fake_game_repository = MagicMock(GameRepository)
    fake_injector.get.return_value = fake_game_repository

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
    fake_game_repository = MagicMock(GameRepository)
    fake_game_repository.get_game.side_effect = IndexError()
    fake_injector.get.return_value = fake_game_repository

    # Act
    with pytest.raises(NotFound):
        _ = mod.details(1)


@patch('app.flask.game_controller.render_template')
@patch('app.flask.game_controller.flash')
@patch('app.flask.game_controller.injector')
@patch('app.flask.game_controller.NewGameForm')
def test_create_when_form_not_submitted_and_selected_season_year_is_less_than_1920_and_no_form_errors_should_render_create_template(
        fake_form, fake_injector, fake_flash,
        fake_render_template, test_app
):
    # Arrange
    fake_form.return_value.week.data = None
    fake_form.return_value.validate_on_submit.return_value = False
    fake_form.return_value.errors = None

    fake_game_service = MagicMock(GameService)
    fake_injector.get.return_value = fake_game_service

    # Act
    with test_app.test_request_context(
            '/games/create',
            method='GET'
    ):
        session['selected_season_year'] = 1919
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
    fake_form.return_value.week.data = None
    fake_form.return_value.validate_on_submit.return_value = False
    fake_form.return_value.errors = None

    fake_game_service = MagicMock(GameService)
    fake_injector.get.return_value = fake_game_service

    selected_season_year = 1920

    # Act
    with test_app.test_request_context(
            '/games/create',
            method='GET'
    ):
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
    fake_form.return_value.week.data = None
    fake_form.return_value.validate_on_submit.return_value = False
    fake_form.return_value.errors = None

    fake_game_service = MagicMock(GameService)
    fake_injector.get.return_value = fake_game_service

    selected_season_year = 1921

    # Act
    with test_app.test_request_context(
            '/games/create',
            method='GET'
    ):
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
    fake_form.return_value.week.data = None
    fake_form.return_value.validate_on_submit.return_value = False

    errors = 'errors'
    fake_form.return_value.errors = errors

    fake_game_service = MagicMock(GameService)
    fake_injector.get.return_value = fake_game_service

    # Act
    with test_app.test_request_context(
            '/games/create',
            method='GET'
    ):
        session['selected_season_year'] = 1921
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


@patch('app.flask.game_controller.url_for')
@patch('app.flask.game_controller.redirect')
@patch('app.flask.game_controller.flash')
@patch('app.flask.game_controller.injector')
@patch('app.flask.game_controller.game_factory')
@patch('app.flask.game_controller.NewGameForm')
def test_create_when_form_submitted_and_no_errors_caught_should_flash_success_message_and_redirect_to_game_create(
        fake_form, fake_game_factory, fake_injector, fake_flash,
        fake_redirect, fake_url_for, test_app
):
    # Arrange
    fake_form.return_value.validate_on_submit.return_value = True
    fake_form.return_value.season_year.data = 1920
    fake_form.return_value.league_name.data = "APFA"
    fake_form.return_value.week.data = 1
    fake_form.return_value.guest_name.data = "Guest"
    fake_form.return_value.guest_score.data = 2
    fake_form.return_value.host_name.data = "Host"
    fake_form.return_value.host_score.data = 3
    fake_form.return_value.is_playoff.data = False
    fake_form.return_value.notes.data = None

    fake_game_service = MagicMock(GameService)
    fake_injector.get.return_value = fake_game_service

    # Act
    with test_app.test_request_context(
            '/games/create',
            method='POST'
    ):
        result = mod.create()

        # Assert
        kwargs = {
            'season_year': 1920,
            'league_name': 'APFA',
            'week': 1,
            'guest_name': "Guest",
            'guest_score': 2,
            'host_name': "Host",
            'host_score': 3,
            'is_playoff': False,
            'notes': None,
        }

        fake_form.assert_called_once()
        fake_form.return_value.validate_on_submit.assert_called_once()
        fake_game_factory.create_game.assert_called_once_with(**kwargs)
        fake_injector.get.assert_called_once_with(GameService)
        fake_game_service.add_game.assert_called_once_with(fake_game_factory.create_game.return_value)
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
    fake_form.return_value.validate_on_submit.return_value = True
    fake_form.return_value.season_year.data = 1920
    fake_form.return_value.league_name.data = "APFA"
    fake_form.return_value.week.data = 1
    fake_form.return_value.guest_name.data = "Guest"
    fake_form.return_value.guest_score.data = 2
    fake_form.return_value.host_name.data = "Host"
    fake_form.return_value.host_score.data = 3
    fake_form.return_value.is_playoff.data = False
    fake_form.return_value.notes.data = None

    fake_game_service = MagicMock(GameService)
    err = ValueError()
    fake_game_service.add_game.side_effect = err
    fake_injector.get.return_value = fake_game_service

    # Act
    with test_app.test_request_context(
            '/games/create',
            method='POST'
    ):
        result = mod.create()

    # Assert
    kwargs = {
        'season_year': 1920,
        'league_name': 'APFA',
        'week': 1,
        'guest_name': "Guest",
        'guest_score': 2,
        'host_name': "Host",
        'host_score': 3,
        'is_playoff': False,
        'notes': None,
    }

    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    fake_game_factory.create_game.assert_called_once_with(**kwargs)
    fake_injector.get.assert_called_once_with(GameService)
    fake_game_service.add_game.assert_called_once_with(fake_game_factory.create_game.return_value)
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
    fake_form.return_value.validate_on_submit.return_value = True
    fake_form.return_value.season_year.data = 1920
    fake_form.return_value.league_name.data = "APFA"
    fake_form.return_value.week.data = 1
    fake_form.return_value.guest_name.data = "Guest"
    fake_form.return_value.guest_score.data = 2
    fake_form.return_value.host_name.data = "Host"
    fake_form.return_value.host_score.data = 3
    fake_form.return_value.is_playoff.data = False
    fake_form.return_value.notes.data = None

    fake_game_service = MagicMock(GameService)
    err = IntegrityError(
        'statement', 'params',
        Exception("Violation of PRIMARY KEY constraint")
    )
    fake_game_service.add_game.side_effect = err
    fake_injector.get.return_value = fake_game_service

    # Act
    with test_app.test_request_context(
            '/games/create',
            method='POST'
    ):
        result = mod.create()

    # Assert
    kwargs = {
        'season_year': 1920,
        'league_name': 'APFA',
        'week': 1,
        'guest_name': "Guest",
        'guest_score': 2,
        'host_name': "Host",
        'host_score': 3,
        'is_playoff': False,
        'notes': None,
    }

    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    fake_game_factory.create_game.assert_called_once_with(**kwargs)
    fake_injector.get.assert_called_once_with(GameService)
    fake_game_service.add_game.assert_called_once_with(fake_game_factory.create_game.return_value)
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
    fake_form.return_value.validate_on_submit.return_value = True
    fake_form.return_value.season_year.data = 1920
    fake_form.return_value.league_name.data = "APFA"
    fake_form.return_value.week.data = 1
    fake_form.return_value.guest_name.data = "Guest"
    fake_form.return_value.guest_score.data = 2
    fake_form.return_value.host_name.data = "Host"
    fake_form.return_value.host_score.data = 3
    fake_form.return_value.is_playoff.data = False
    fake_form.return_value.notes.data = None

    fake_game_service = MagicMock(GameService)
    err = IntegrityError(
        'statement', 'params',
        Exception("Violation of UNIQUE KEY constraint 'UQ_Game_Season_League_Week_Teams'")
    )
    fake_game_service.add_game.side_effect = err
    fake_injector.get.return_value = fake_game_service

    # Act
    with test_app.test_request_context(
            '/games/create',
            method='POST'
    ):
        result = mod.create()

    # Assert
    kwargs = {
        'season_year': 1920,
        'league_name': 'APFA',
        'week': 1,
        'guest_name': "Guest",
        'guest_score': 2,
        'host_name': "Host",
        'host_score': 3,
        'is_playoff': False,
        'notes': None,
    }

    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    fake_game_factory.create_game.assert_called_once_with(**kwargs)
    fake_injector.get.assert_called_once_with(GameService)
    fake_game_service.add_game.assert_called_once_with(fake_game_factory.create_game.return_value)
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
    fake_form.return_value.validate_on_submit.return_value = True
    fake_form.return_value.season_year.data = 1920
    fake_form.return_value.league_name.data = "APFA"
    fake_form.return_value.week.data = 1
    fake_form.return_value.guest_name.data = "Guest"
    fake_form.return_value.guest_score.data = 2
    fake_form.return_value.host_name.data = "Host"
    fake_form.return_value.host_score.data = 3
    fake_form.return_value.is_playoff.data = False
    fake_form.return_value.notes.data = None

    fake_game_service = MagicMock(GameService)
    err = IntegrityError(
        'statement', 'params',
        Exception("The INSERT statement conflicted with the FOREIGN KEY constraint 'FK_Game_Season_SeasonYear'")
    )
    fake_game_service.add_game.side_effect = err
    fake_injector.get.return_value = fake_game_service

    # Act
    with test_app.test_request_context(
            '/games/create',
            method='POST'
    ):
        result = mod.create()

    # Assert
    kwargs = {
        'season_year': 1920,
        'league_name': 'APFA',
        'week': 1,
        'guest_name': "Guest",
        'guest_score': 2,
        'host_name': "Host",
        'host_score': 3,
        'is_playoff': False,
        'notes': None,
    }

    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    fake_game_factory.create_game.assert_called_once_with(**kwargs)
    fake_injector.get.assert_called_once_with(GameService)
    fake_game_service.add_game.assert_called_once_with(fake_game_factory.create_game.return_value)
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
    fake_form.return_value.validate_on_submit.return_value = True
    fake_form.return_value.season_year.data = 1920
    fake_form.return_value.league_name.data = "APFA"
    fake_form.return_value.week.data = 1
    fake_form.return_value.guest_name.data = "Guest"
    fake_form.return_value.guest_score.data = 2
    fake_form.return_value.host_name.data = "Host"
    fake_form.return_value.host_score.data = 3
    fake_form.return_value.is_playoff.data = False
    fake_form.return_value.notes.data = None

    fake_game_service = MagicMock(GameService)
    err = IntegrityError(
        'statement', 'params',
        Exception("The INSERT statement conflicted with the FOREIGN KEY constraint 'FK_Game_Association_LeagueId'")
    )
    fake_game_service.add_game.side_effect = err
    fake_injector.get.return_value = fake_game_service

    # Act
    with test_app.test_request_context(
            '/games/create',
            method='POST'
    ):
        result = mod.create()

    # Assert
    kwargs = {
        'season_year': 1920,
        'league_name': 'APFA',
        'week': 1,
        'guest_name': "Guest",
        'guest_score': 2,
        'host_name': "Host",
        'host_score': 3,
        'is_playoff': False,
        'notes': None,
    }

    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    fake_game_factory.create_game.assert_called_once_with(**kwargs)
    fake_injector.get.assert_called_once_with(GameService)
    fake_game_service.add_game.assert_called_once_with(fake_game_factory.create_game.return_value)
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
    fake_form.return_value.validate_on_submit.return_value = True
    fake_form.return_value.season_year.data = 1920
    fake_form.return_value.league_name.data = "APFA"
    fake_form.return_value.week.data = 1
    fake_form.return_value.guest_name.data = "Guest"
    fake_form.return_value.guest_score.data = 2
    fake_form.return_value.host_name.data = "Host"
    fake_form.return_value.host_score.data = 3
    fake_form.return_value.is_playoff.data = False
    fake_form.return_value.notes.data = None

    fake_game_service = MagicMock(GameService)
    err = IntegrityError(
        'statement', 'params',
        Exception("Something else")
    )
    fake_game_service.add_game.side_effect = err
    fake_injector.get.return_value = fake_game_service

    # Act
    with test_app.test_request_context(
            '/games/create',
            method='POST'
    ):
        result = mod.create()

    # Assert
    kwargs = {
        'season_year': 1920,
        'league_name': 'APFA',
        'week': 1,
        'guest_name': "Guest",
        'guest_score': 2,
        'host_name': "Host",
        'host_score': 3,
        'is_playoff': False,
        'notes': None,
    }

    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    fake_game_factory.create_game.assert_called_once_with(**kwargs)
    fake_injector.get.assert_called_once_with(GameService)
    fake_game_service.add_game.assert_called_once_with(fake_game_factory.create_game.return_value)
    fake_flash.assert_called_once_with("An unexpected error occurred.", 'danger')
    fake_render_template.assert_called_once_with(
        'games/create.html', form=fake_form.return_value, game=None
    )
    assert result is fake_render_template.return_value


@patch('app.flask.game_controller.copy')
@patch('app.flask.game_controller.injector')
def test_edit_when_game_not_found_should_abort_with_404_error(fake_injector, fake_copy):
    # Arrange
    fake_game_repository = MagicMock(GameRepository)
    old_game = MagicMock(Game)
    fake_game_repository.get_game.return_value = old_game

    old_game_copy = None
    fake_copy.deepcopy.return_value = old_game_copy

    fake_game_service = MagicMock(GameService)
    fake_injector.get.side_effect = [fake_game_repository, fake_game_service]

    # Act
    with pytest.raises(NotFound):
        result = mod.edit(1)

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
        fake_injector, fake_copy, fake_form,
        fake_flash, fake_render_template
):
    # Arrange
    fake_game_repository = MagicMock(GameRepository)
    old_game = MagicMock(Game)
    fake_game_repository.get_game.return_value = old_game

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

    fake_game_service = MagicMock(GameService)
    fake_injector.get.side_effect = [fake_game_repository, fake_game_service]

    fake_form.return_value.validate_on_submit.return_value = False
    fake_form.return_value.errors = None

    # Act
    result = mod.edit(1)

    # Assert
    fake_injector.get.assert_called_once_with(GameRepository)
    fake_game_repository.get_game.assert_called_once()
    fake_copy.deepcopy.assert_called_once_with(old_game)
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    fake_game_service.update_game.assert_not_called()
    assert fake_form.return_value.season_year.data == old_game_copy.season.year
    assert fake_form.return_value.league_name.data == old_game_copy.league.short_name
    assert fake_form.return_value.week.data == old_game_copy.week
    assert fake_form.return_value.guest_name.data == old_game_copy.guest_name
    assert fake_form.return_value.guest_score.data == old_game_copy.guest_score
    assert fake_form.return_value.host_name.data == old_game_copy.host_name
    assert fake_form.return_value.host_score.data == old_game_copy.host_score
    assert fake_form.return_value.is_playoff.data == old_game_copy.is_playoff
    assert fake_form.return_value.notes.data == old_game_copy.notes
    fake_flash.assert_not_called()
    fake_render_template.assert_called_once_with(
        'games/edit.html', form=fake_form.return_value, game=old_game_copy
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
    fake_game_repository = MagicMock(GameRepository)
    old_game = MagicMock(Game)
    fake_game_repository.get_game.return_value = old_game

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

    fake_game_service = MagicMock(GameService)
    fake_injector.get.side_effect = [fake_game_repository, fake_game_service]

    fake_form.return_value.validate_on_submit.return_value = False
    fake_form.return_value.errors = None

    errors = 'errors'
    fake_form.return_value.errors = errors

    # Act
    result = mod.edit(1)

    # Assert
    fake_injector.get.assert_called_once_with(GameRepository)
    fake_game_repository.get_game.assert_called_once()
    fake_copy.deepcopy.assert_called_once_with(old_game)
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    fake_game_service.update_game.assert_not_called()
    assert fake_form.return_value.season_year.data == old_game_copy.season.year
    assert fake_form.return_value.league_name.data == old_game_copy.league.short_name
    assert fake_form.return_value.week.data == old_game_copy.week
    assert fake_form.return_value.guest_name.data == old_game_copy.guest_name
    assert fake_form.return_value.guest_score.data == old_game_copy.guest_score
    assert fake_form.return_value.host_name.data == old_game_copy.host_name
    assert fake_form.return_value.host_score.data == old_game_copy.host_score
    assert fake_form.return_value.is_playoff.data == old_game_copy.is_playoff
    assert fake_form.return_value.notes.data == old_game_copy.notes
    fake_flash.assert_called_once_with(f"{errors}", 'danger')
    fake_render_template.assert_called_once_with(
        'games/edit.html', form=fake_form.return_value, game=old_game_copy
    )
    assert result is fake_render_template.return_value


@patch('app.flask.game_controller.url_for')
@patch('app.flask.game_controller.redirect')
@patch('app.flask.game_controller.flash')
@patch('app.flask.game_controller.game_factory')
@patch('app.flask.game_controller.EditGameForm')
@patch('app.flask.game_controller.copy')
@patch('app.flask.game_controller.injector')
def test_edit_when_game_found_and_form_submitted_and_no_errors_caught_should_flash_success_message_and_redirect_to_game_details(
        fake_injector, fake_copy, fake_form,
        fake_game_factory, fake_flash, fake_redirect,
        fake_url_for
):
    # Arrange
    fake_game_repository = MagicMock(GameRepository)
    old_game = MagicMock(Game)
    fake_game_repository.get_game.return_value = old_game

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

    fake_game_service = MagicMock(GameService)
    fake_injector.get.side_effect = [fake_game_repository, fake_game_service]

    fake_form.return_value.validate_on_submit.return_value = True
    fake_form.return_value.season_year.data = 1921
    fake_form.return_value.league_name.data = "L2"
    fake_form.return_value.week.data = 2
    fake_form.return_value.guest_name.data = "Guest 2"
    fake_form.return_value.guest_score.data = 3
    fake_form.return_value.host_name.data = "Host 2"
    fake_form.return_value.host_score.data = 2
    fake_form.return_value.is_playoff.data = True
    fake_form.return_value.notes.data = "Notes"

    id = 1
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

    # Act
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
    fake_game_repository = MagicMock(GameRepository)
    old_game = MagicMock(Game)
    fake_game_repository.get_game.return_value = old_game

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

    fake_game_service = MagicMock(GameService)
    fake_injector.get.side_effect = [fake_game_repository, fake_game_service]

    fake_form.return_value.validate_on_submit.return_value = True
    fake_form.return_value.season_year.data = 1921
    fake_form.return_value.league_name.data = "L2"
    fake_form.return_value.week.data = 2
    fake_form.return_value.guest_name.data = "Guest 2"
    fake_form.return_value.guest_score.data = 3
    fake_form.return_value.host_name.data = "Host 2"
    fake_form.return_value.host_score.data = 2
    fake_form.return_value.is_playoff.data = True
    fake_form.return_value.notes.data = "Notes"

    id = 1
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

    err = ValueError()
    fake_game_service.update_game.side_effect = err

    # Act
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
    fake_game_repository = MagicMock(GameRepository)
    old_game = MagicMock(Game)
    fake_game_repository.get_game.return_value = old_game

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

    fake_game_service = MagicMock(GameService)
    err = IntegrityError(
        'statement', 'params',
        Exception("Violation of UNIQUE KEY constraint 'UQ_Game_Season_League_Week_Teams'")
    )
    fake_game_service.update_game.side_effect = err
    fake_injector.get.side_effect = [fake_game_repository, fake_game_service]

    fake_form.return_value.validate_on_submit.return_value = True
    fake_form.return_value.season_year.data = 1921
    fake_form.return_value.league_name.data = "L2"
    fake_form.return_value.week.data = 2
    fake_form.return_value.guest_name.data = "Guest 2"
    fake_form.return_value.guest_score.data = 3
    fake_form.return_value.host_name.data = "Host 2"
    fake_form.return_value.host_score.data = 2
    fake_form.return_value.is_playoff.data = True
    fake_form.return_value.notes.data = "Notes"

    id = 1
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

    # Act
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
    fake_game_repository = MagicMock(GameRepository)
    old_game = MagicMock(Game)
    fake_game_repository.get_game.return_value = old_game

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

    fake_game_service = MagicMock(GameService)
    err = IntegrityError(
        'statement', 'params',
        Exception("The UPDATE statement conflicted with the FOREIGN KEY constraint 'FK_Game_Season_SeasonYear'")
    )
    fake_game_service.update_game.side_effect = err
    fake_injector.get.side_effect = [fake_game_repository, fake_game_service]

    fake_form.return_value.validate_on_submit.return_value = True
    fake_form.return_value.season_year.data = 1921
    fake_form.return_value.league_name.data = "L2"
    fake_form.return_value.week.data = 2
    fake_form.return_value.guest_name.data = "Guest 2"
    fake_form.return_value.guest_score.data = 3
    fake_form.return_value.host_name.data = "Host 2"
    fake_form.return_value.host_score.data = 2
    fake_form.return_value.is_playoff.data = True
    fake_form.return_value.notes.data = "Notes"

    id = 1
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

    # Act
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
    fake_game_repository = MagicMock(GameRepository)
    old_game = MagicMock(Game)
    fake_game_repository.get_game.return_value = old_game

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

    fake_game_service = MagicMock(GameService)
    err = IntegrityError(
        'statement', 'params',
        Exception("The UPDATE statement conflicted with the FOREIGN KEY constraint 'FK_Game_Association_LeagueId'")
    )
    fake_game_service.update_game.side_effect = err
    fake_injector.get.side_effect = [fake_game_repository, fake_game_service]

    fake_form.return_value.validate_on_submit.return_value = True
    fake_form.return_value.season_year.data = 1921
    fake_form.return_value.league_name.data = "L2"
    fake_form.return_value.week.data = 2
    fake_form.return_value.guest_name.data = "Guest 2"
    fake_form.return_value.guest_score.data = 3
    fake_form.return_value.host_name.data = "Host 2"
    fake_form.return_value.host_score.data = 2
    fake_form.return_value.is_playoff.data = True
    fake_form.return_value.notes.data = "Notes"

    id = 1
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

    # Act
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
    fake_game_repository = MagicMock(GameRepository)
    old_game = MagicMock(Game)
    fake_game_repository.get_game.return_value = old_game

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

    fake_game_service = MagicMock(GameService)
    err = IntegrityError(
        'statement', 'params',
        Exception("Something else")
    )
    fake_game_service.update_game.side_effect = err
    fake_injector.get.side_effect = [fake_game_repository, fake_game_service]

    fake_form.return_value.validate_on_submit.return_value = True
    fake_form.return_value.season_year.data = 1921
    fake_form.return_value.league_name.data = "L2"
    fake_form.return_value.week.data = 2
    fake_form.return_value.guest_name.data = "Guest 2"
    fake_form.return_value.guest_score.data = 3
    fake_form.return_value.host_name.data = "Host 2"
    fake_form.return_value.host_score.data = 2
    fake_form.return_value.is_playoff.data = True
    fake_form.return_value.notes.data = "Notes"

    id = 1
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

    # Act
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
    fake_game_factory.create_game.assert_called_once_with(**kwargs)
    fake_flash.assert_called_once_with("An unexpected error occurred.", 'danger')
    fake_render_template.assert_called_once_with(
        'games/edit.html', form=fake_form.return_value, game=old_game_copy
    )
    assert result is fake_render_template.return_value


@patch('app.flask.game_controller.flash')
@patch('app.flask.game_controller.game_factory')
@patch('app.flask.game_controller.EditGameForm')
@patch('app.flask.game_controller.url_for')
@patch('app.flask.game_controller.redirect')
@patch('app.flask.game_controller.copy')
@patch('app.flask.game_controller.injector')
def test_edit_when_game_found_and_form_submitted_and_index_error_caught_should_abort_with_404_error(
        fake_injector, fake_copy, fake_redirect, fake_url_for,
        fake_form, fake_game_factory, fake_flash,
):
    # Arrange
    fake_game_repository = MagicMock(GameRepository)
    old_game = MagicMock(Game)
    fake_game_repository.get_game.return_value = old_game

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

    fake_game_service = MagicMock(GameService)
    fake_injector.get.side_effect = [fake_game_repository, fake_game_service]

    fake_form.return_value.validate_on_submit.return_value = True
    fake_form.return_value.season_year.data = 1921
    fake_form.return_value.league_name.data = "L2"
    fake_form.return_value.week.data = 2
    fake_form.return_value.guest_name.data = "Guest 2"
    fake_form.return_value.guest_score.data = 3
    fake_form.return_value.host_name.data = "Host 2"
    fake_form.return_value.host_score.data = 2
    fake_form.return_value.is_playoff.data = True
    fake_form.return_value.notes.data = "Notes"

    id = 1
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

    err = IndexError()
    fake_url_for.side_effect = err

    # Act
    with pytest.raises(NotFound):
        result = mod.edit(1)

    # Assert
    fake_injector.get.assert_has_calls([
        call(GameRepository),
        call(GameService),
    ])
    fake_game_repository.get_game.assert_called_once_with(id)
    fake_copy.deepcopy.assert_called_once_with(old_game)
    fake_form.assert_called_once()
    fake_form.return_value.validate_on_submit.assert_called_once()
    fake_game_factory.create_game.assert_called_once_with(**kwargs)


@patch('app.flask.game_controller.injector')
def test_delete_when_game_not_found_should_abort_with_404_error(fake_injector, test_app):
    # Arrange
    fake_game_repository = MagicMock(GameRepository)
    fake_game_repository.get_game.return_value = None

    fake_game_service = MagicMock(GameService)
    fake_injector.get.side_effect = [fake_game_repository, fake_game_service]

    id = 1

    # Act
    with test_app.test_request_context(
            f'/games/delete?id={id}',
            method='POST'
    ):
        with pytest.raises(NotFound):
            result = mod.delete(id)

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
    fake_game_repository = MagicMock(GameRepository)
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
    fake_game_repository.get_game.return_value = game

    fake_game_service = MagicMock(GameService)
    fake_injector.get.side_effect = [fake_game_repository, fake_game_service]

    id = 1

    # Act
    with test_app.test_request_context(
            f'/games/delete?id={id}',
            method='GET'
    ):
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
    fake_game_repository = MagicMock(GameRepository)
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
    fake_game_repository.get_game.return_value = game

    fake_game_service = MagicMock(GameService)
    fake_injector.get.side_effect = [fake_game_repository, fake_game_service]

    id = 1

    # Act
    with test_app.test_request_context(
            '/games/delete?id=1',
            method='POST'
    ):
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
    fake_game_repository = MagicMock(GameRepository)
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
    fake_game_repository.get_game.return_value = game

    fake_game_service = MagicMock(GameService)
    fake_game_service.delete_game.side_effect = IndexError()

    fake_injector.get.side_effect = [fake_game_repository, fake_game_service]

    id = 1

    # Act
    with test_app.test_request_context(
            f'/games/delete?id={id}',
            method='POST'
    ):
        with pytest.raises(NotFound):
            _ = mod.delete(id)

    # Assert
    fake_injector.get.assert_has_calls([
        call(GameRepository),
        call(GameService),
    ])
    fake_game_repository.get_game.assert_called_once_with(id)
    fake_game_service.delete_game.assert_called_once_with(id)


@pytest.mark.skip('WIP')
@patch('app.flask.game_controller.render_template')
@patch('app.flask.game_controller.injector')
@patch('app.flask.game_controller.request')
def test_select_season_should_render_game_index_template_for_selected_season(
        fake_request, fake_injector, fake_render_template, test_app
):
    with test_app.test_request_context(
            '/season_standings/select_season',
            method='POST'
    ):
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
    with test_app.test_request_context(
            '/season_standings/select_season',
            method='POST'
    ):
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
    with test_app.test_request_context(
            '/season_standings/select_season',
            method='POST'
    ):
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
    with test_app.test_request_context(
            '/season_standings/select_season',
            method='POST'
    ):
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
