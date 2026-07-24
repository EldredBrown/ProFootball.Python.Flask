from typing import Optional
from unittest.mock import patch, MagicMock, call

import pytest
from flask import session

import app.flask.season_rankings_controller as mod
from app.data.models.association import Association
from app.data.models.season import Season
from app.data.repositories.association_repository import AssociationRepository
from app.data.repositories.season_repository import SeasonRepository

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
@patch('app.flask.season_rankings_controller.render_template')
@patch('app.flask.season_rankings_controller.injector')
def test_index_when_selected_season_year_is_none_and_selected_league_name_is_none_or_empty_should_set_selected_season_year_and_selected_league_name_and_render_team_season_index_template(
        fake_injector, fake_render_template, league_name, test_app
):
    with (test_app.test_request_context('/team_seasons/', method='GET')):
        # Arrange
        seasons, fake_season_repository, associations, fake_association_repository = (
            _set_up_index(fake_injector, league_name=league_name)
        )

        # Act
        result = mod.index()

        # Assert
        fake_injector.get.assert_has_calls([
            call(SeasonRepository),
            call(AssociationRepository),
        ])

        # Verify seasons.
        fake_season_repository.get_seasons.assert_called_once()
        seasons.sort(key=lambda s: s.year, reverse=True)
        assert session.get('seasons') == [s.to_dict() for s in seasons]

        default_season = seasons[0]
        assert session.get('selected_season_year') == default_season.year

        # Verify leagues.
        fake_association_repository.get_associations.assert_called_once()
        leagues = [a for a in associations if a.parent_id is None]
        active_leagues = [l for l in leagues if l.first_season_year <= default_season.year
                          and (l.last_season is None or default_season.year <= l.last_season_year)]
        active_leagues.sort(key=lambda l: l.id, reverse=True)
        assert session.get('leagues') == [l.to_dict() for l in active_leagues]

        default_league = active_leagues[0]
        assert session.get('selected_league_name') == default_league.short_name

        # Verify render.
        fake_render_template.assert_called_once_with(
            'season_rankings/index.html',
            seasons=seasons, selected_season_year=default_season.year,
            leagues=active_leagues, selected_league_name=default_league.short_name,
            types=mod.RANKING_TYPES, selected_type=None, season_rankings=None
        )
        assert result is fake_render_template.return_value


@pytest.mark.parametrize(
    "league_name",
    [
        None,
        '',
    ]
)
@patch('app.flask.season_rankings_controller.render_template')
@patch('app.flask.season_rankings_controller.injector')
def test_index_when_selected_season_year_is_not_none_should_set_selected_season_year_and_render_team_season_index_template(
        fake_injector, fake_render_template, league_name, test_app
):
    with test_app.test_request_context('/team_seasons/', method='GET'):
        selected_season_year = 1920
        seasons, fake_season_repository, associations, fake_association_repository = (
            _set_up_index(fake_injector, season_year=selected_season_year, league_name=league_name)
        )

        # Act
        result = mod.index()

        # Assert
        fake_injector.get.assert_has_calls([
            call(SeasonRepository),
            call(AssociationRepository),
        ])

        # Verify seasons.
        fake_season_repository.get_seasons.assert_called_once()
        seasons.sort(key=lambda s: s.year, reverse=True)
        assert session.get('seasons') == [s.to_dict() for s in seasons]
        assert session.get('selected_season_year') == selected_season_year

        # Verify leagues.
        fake_association_repository.get_associations.assert_called_once()
        leagues = [a for a in associations if a.parent_id is None]
        active_leagues = [l for l in leagues if l.first_season_year <= selected_season_year
                          and (l.last_season is None or selected_season_year <= l.last_season_year)]
        active_leagues.sort(key=lambda l: l.id, reverse=True)
        assert session.get('leagues') == [l.to_dict() for l in active_leagues]

        default_league = active_leagues[0]
        assert session.get('selected_league_name') == default_league.short_name

        # Verify render.
        fake_render_template.assert_called_once_with(
            'season_rankings/index.html',
            seasons=seasons, selected_season_year=selected_season_year,
            leagues=active_leagues, selected_league_name=default_league.short_name,
            types=mod.RANKING_TYPES, selected_type=None, season_rankings=None
        )
        assert result is fake_render_template.return_value


@patch('app.flask.season_rankings_controller.render_template')
@patch('app.flask.season_rankings_controller.injector')
def test_index_when_selected_league_name_is_neither_none_nor_empty_should_set_selected_league_name_and_render_team_season_index_template(
        fake_injector, fake_render_template, test_app
):
    with test_app.test_request_context('/team_seasons/', method='GET'):
        # Arrange
        selected_season_year = 1920
        selected_league_name = "APFA"
        seasons, fake_season_repository, associations, fake_association_repository = (
            _set_up_index(fake_injector, season_year=selected_season_year, league_name=selected_league_name)
        )

        # Act
        result = mod.index()

        # Assert
        fake_injector.get.assert_has_calls([
            call(SeasonRepository),
            call(AssociationRepository),
        ])

        # Verify seasons.
        fake_season_repository.get_seasons.assert_called_once()
        seasons.sort(key=lambda s: s.year, reverse=True)
        assert session.get('seasons') == [s.to_dict() for s in seasons]
        assert session.get('selected_season_year') == selected_season_year

        # Verify leagues.
        fake_association_repository.get_associations.assert_called_once()
        leagues = [a for a in associations if a.parent_id is None]
        active_leagues = [l for l in leagues if l.first_season_year <= selected_season_year
                          and (l.last_season is None or selected_season_year <= l.last_season_year)]
        active_leagues.sort(key=lambda l: l.id, reverse=True)
        assert session.get('leagues') == [l.to_dict() for l in active_leagues]
        assert session.get('selected_league_name') == selected_league_name

        fake_render_template.assert_called_once_with(
            'season_rankings/index.html',
            seasons=seasons, selected_season_year=selected_season_year,
            leagues=active_leagues, selected_league_name=selected_league_name,
            types=mod.RANKING_TYPES, selected_type=None, season_rankings=None
        )
        assert result is fake_render_template.return_value


def _set_up_index(fake_injector, season_year: Optional[int] = None, league_name: Optional[str] = None) \
        -> tuple[list[Season], MagicMock, list[Association], MagicMock]:
    seasons, fake_season_repository = _set_up_index_seasons(season_year)
    associations, fake_association_repository = _set_up_index_leagues(league_name)

    fake_injector.get.side_effect = [fake_season_repository, fake_association_repository]

    return seasons, fake_season_repository, associations, fake_association_repository


def _set_up_index_leagues(league_name: str | None) -> tuple[MagicMock, list[Association]]:
    fake_association_repository = MagicMock(AssociationRepository)
    associations = [
        Association(
            id=1,
            long_name="American Professional Football Association",
            short_name="APFA",
            parent_id=None,
            first_season_year=1920,
            last_season_year=1922,
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

    session['selected_league_name'] = league_name
    return associations, fake_association_repository


def _set_up_index_seasons(season_year: int | None) -> tuple[list[Season], MagicMock]:
    fake_season_repository = MagicMock(SeasonRepository)
    seasons = [
        Season(year=1920),
        Season(year=1921),
        Season(year=1922),
    ]
    fake_season_repository.get_seasons.return_value = seasons

    session['selected_season_year'] = season_year

    return seasons, fake_season_repository


@pytest.mark.skip('WIP')
def test_select_season_should_render_season_rankings_index_template_for_selected_year(test_app):
    with test_app.test_request_context('/season_rankings/select_season', method='POST'):
        # Arrange

        # Act
        result = mod.select_season()

    # Assert


@pytest.mark.skip('WIP')
def test_select_league_should_render_rankings_index_template_for_selected_league(test_app):
    with test_app.test_request_context('/season_rankings/select_league', method='POST'):
        # Arrange

        # Act
        result = mod.select_league()

    # Assert


@pytest.mark.skip('WIP')
def test_select_type_should_render_rankings_index_template_for_selected_type(test_app):
    with test_app.test_request_context('/season_rankings/select_type', method='POST'):
        # Arrange

        # Act
        result = mod.select_type()

    # Assert


@patch('app.flask.season_rankings_controller.render_template')
@patch('app.flask.season_rankings_controller.season_rankings_repository')
@patch('app.flask.season_rankings_controller.injector')
def test_offense_should_render_season_offensive_rankings_template(
        fake_injector, fake_season_rankings_repository,
        fake_render_template, test_app
):
    with (test_app.test_request_context('/season_rankings/', method='GET')):
        # Arrange
        selected_season_year, selected_league_name, fake_association_repository, selected_league = (
            _set_up_rankings(fake_injector)
        )

        # Act
        result = mod.offense()

        # Assert
        fake_injector.get.assert_called_once_with(AssociationRepository)
        fake_association_repository.get_association_by_short_name.assert_called_once_with(selected_league_name)
        fake_season_rankings_repository.get_offensive_rankings.assert_called_once_with(
            season_year=selected_season_year, league_id=selected_league.id
        )
        fake_render_template.assert_called_once_with(
            f'season_rankings/offense.html',
            seasons=session.get('seasons'), selected_season_year=selected_season_year,
            leagues=session.get('leagues'), selected_league_name=selected_league_name,
            types=mod.RANKING_TYPES, selected_type=session.get('selected_type'),
            season_rankings=fake_season_rankings_repository.get_offensive_rankings.return_value
        )
        assert result is fake_render_template.return_value


@patch('app.flask.season_rankings_controller.render_template')
@patch('app.flask.season_rankings_controller.season_rankings_repository')
@patch('app.flask.season_rankings_controller.injector')
def test_defense_should_render_season_defensive_rankings_template(
        fake_injector, fake_season_rankings_repository,
        fake_render_template, test_app
):
    with test_app.test_request_context('/season_rankings/', method='GET'):
        # Arrange
        selected_season_year, selected_league_name, fake_association_repository, selected_league = (
            _set_up_rankings(fake_injector)
        )

        # Act
        result = mod.defense()

        # Assert
        fake_injector.get.assert_called_once_with(AssociationRepository)
        fake_association_repository.get_association_by_short_name.assert_called_once_with(selected_league_name)
        fake_season_rankings_repository.get_defensive_rankings.assert_called_once_with(
            season_year=selected_season_year, league_id=selected_league.id
        )
        fake_render_template.assert_called_once_with(
            f'season_rankings/defense.html',
            seasons=session.get('seasons'), selected_season_year=selected_season_year,
            leagues=session.get('leagues'), selected_league_name=selected_league_name,
            types=mod.RANKING_TYPES, selected_type=session.get('selected_type'),
            season_rankings=fake_season_rankings_repository.get_defensive_rankings.return_value
        )
        assert result is fake_render_template.return_value


@patch('app.flask.season_rankings_controller.render_template')
@patch('app.flask.season_rankings_controller.season_rankings_repository')
@patch('app.flask.season_rankings_controller.injector')
def test_total_should_render_season_total_rankings_template(
        fake_injector, fake_season_rankings_repository,
        fake_render_template, test_app
):
    with (test_app.test_request_context('/season_rankings/', method='GET')):
        # Arrange
        selected_season_year, selected_league_name, fake_association_repository, selected_league = (
            _set_up_rankings(fake_injector)
        )

        # Act
        result = mod.total()

        # Assert
        fake_injector.get.assert_called_once_with(AssociationRepository)
        fake_association_repository.get_association_by_short_name.assert_called_once_with(selected_league_name)
        fake_season_rankings_repository.get_total_rankings.assert_called_once_with(
            season_year=selected_season_year, league_id=selected_league.id
        )
        fake_render_template.assert_called_once_with(
            f'season_rankings/total.html',
            seasons=session.get('seasons'), selected_season_year=selected_season_year,
            leagues=session.get('leagues'), selected_league_name=selected_league_name,
            types=mod.RANKING_TYPES, selected_type=session.get('selected_type'),
            season_rankings=fake_season_rankings_repository.get_total_rankings.return_value
        )
        assert result is fake_render_template.return_value


def _set_up_rankings(fake_injector) -> tuple[int, str, MagicMock, Association]:
    seasons = [
        Season(year=1920),
        Season(year=1921),
        Season(year=1922),
    ]
    session['seasons'] = [s.to_dict() for s in seasons]

    selected_season_year = 1920
    session['selected_season_year'] = selected_season_year

    leagues = [
        Association(
            id=1,
            long_name="American Professional Football Association",
            short_name="APFA",
            parent_id=None,
            first_season_year=1920,
            last_season_year=1922,
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
            long_name="American Football League",
            short_name="AFL",
            parent_id=None,
            first_season_year=1922
        ),
    ]
    session['leagues'] = [l.to_dict() for l in leagues]

    selected_league_name = "APFA"
    session['selected_league_name'] = selected_league_name

    fake_association_repository = MagicMock(AssociationRepository)
    selected_league = [l for l in leagues if l.short_name == selected_league_name][0]
    fake_association_repository.get_association_by_short_name.return_value = selected_league
    fake_injector.get.return_value = fake_association_repository

    return selected_season_year, selected_league_name, fake_association_repository, selected_league
