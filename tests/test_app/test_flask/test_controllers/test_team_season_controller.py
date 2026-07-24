from typing import Any, Optional
from unittest.mock import patch, call, MagicMock

import pytest
from flask import session

from werkzeug.exceptions import NotFound

import app.flask.team_season_controller as mod
from app.data.models.association import Association
from app.data.models.season import Season
from app.data.models.team_season import TeamSeason
from app.data.repositories.association_repository import AssociationRepository
from app.data.repositories.season_repository import SeasonRepository
from app.data.repositories.team_season_repository import TeamSeasonRepository
from app.services.weekly_update_service.weekly_update_service import WeeklyUpdateService

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
@patch('app.flask.team_season_controller.render_template')
@patch('app.flask.team_season_controller.injector')
def test_index_when_selected_season_year_is_none_and_selected_league_name_is_none_or_empty_should_set_selected_season_year_and_selected_league_name_and_render_team_season_index_template(
        fake_injector, fake_render_template, league_name, test_app
):
    with (test_app.test_request_context('/team_seasons/', method='GET')):
        # Arrange
        seasons, fake_season_repository, associations, fake_association_repository, team_seasons, fake_team_season_repository = (
            _set_up_index(fake_injector, league_name=league_name)
        )

        # Act
        result = mod.index()

        # Assert
        fake_injector.get.assert_has_calls([
            call(SeasonRepository),
            call(AssociationRepository),
            call(TeamSeasonRepository)
        ])

        fake_season_repository.get_seasons.assert_called_once()
        seasons.sort(key=lambda s: s.year, reverse=True)
        assert session.get('seasons') == [s.to_dict() for s in seasons]

        default_season = seasons[0]
        assert session.get('selected_season_year') == default_season.year

        fake_association_repository.get_associations.assert_called_once()
        leagues = [a for a in associations if a.parent_id is None]
        active_leagues = [l for l in leagues if l.first_season_year <= default_season.year
                          and (l.last_season is None or default_season.year <= l.last_season_year)]
        active_leagues.sort(key=lambda l: l.id, reverse=True)
        assert session.get('leagues') == [l.to_dict() for l in active_leagues]
        default_league = active_leagues[0]
        assert session.get('selected_league_name') == default_league.short_name

        fake_team_season_repository.get_team_seasons_by_season.assert_called_once_with(season_year=default_season.year)
        assert session.get('team_seasons') == [ts.to_dict() for ts in team_seasons]

        fake_render_template.assert_called_once_with(
            'team_seasons/index.html',
            seasons=seasons, selected_season_year=default_season.year,
            leagues=active_leagues, selected_league_name=default_league.short_name,
            team_seasons=team_seasons
        )
        assert result is fake_render_template.return_value


@pytest.mark.parametrize(
    "league_name",
    [
        None,
        '',
    ]
)
@patch('app.flask.team_season_controller.render_template')
@patch('app.flask.team_season_controller.injector')
def test_index_when_selected_season_year_is_not_none_should_set_selected_season_year_and_render_team_season_index_template(
        fake_injector, fake_render_template, league_name, test_app
):
    with test_app.test_request_context('/team_seasons/', method='GET'):
        # Arrange
        selected_season_year = 1920
        seasons, fake_season_repository, associations, fake_association_repository, team_seasons, fake_team_season_repository = (
            _set_up_index(fake_injector, season_year=selected_season_year, league_name=league_name)
        )

        # Act
        result = mod.index()

        # Assert
        fake_injector.get.assert_has_calls([
            call(SeasonRepository),
            call(AssociationRepository),
            call(TeamSeasonRepository)
        ])

        fake_season_repository.get_seasons.assert_called_once()
        seasons.sort(key=lambda s: s.year, reverse=True)
        assert session.get('seasons') == [s.to_dict() for s in seasons]
        assert session.get('selected_season_year') == selected_season_year

        fake_association_repository.get_associations.assert_called_once()
        leagues = [a for a in associations if a.parent_id is None]
        active_leagues = [l for l in leagues if l.first_season_year <= selected_season_year
                          and (l.last_season is None or selected_season_year <= l.last_season_year)]
        active_leagues.sort(key=lambda l: l.id, reverse=True)
        assert session.get('leagues') == [l.to_dict() for l in active_leagues]
        default_league = active_leagues[0]
        assert session.get('selected_league_name') == default_league.short_name

        fake_team_season_repository.get_team_seasons_by_season.assert_called_once_with(season_year=selected_season_year)
        assert session.get('team_seasons') == [ts.to_dict() for ts in team_seasons]

        fake_render_template.assert_called_once_with(
            'team_seasons/index.html',
            seasons=seasons, selected_season_year=selected_season_year,
            leagues=active_leagues, selected_league_name=default_league.short_name,
            team_seasons=team_seasons
        )
        assert result is fake_render_template.return_value


@patch('app.flask.team_season_controller.render_template')
@patch('app.flask.team_season_controller.injector')
def test_index_when_selected_league_name_is_neither_none_nor_empty_should_set_selected_league_name_and_render_team_season_index_template(
        fake_injector, fake_render_template, test_app
):
    with test_app.test_request_context('/team_seasons/', method='GET'):
        # Arrange
        selected_season_year = 1920
        selected_league_name = "APFA"
        seasons, fake_season_repository, associations, fake_association_repository, team_seasons, fake_team_season_repository = (
            _set_up_index(fake_injector, season_year=selected_season_year, league_name=selected_league_name)
        )

        # Act
        result = mod.index()

        # Assert
        fake_injector.get.assert_has_calls([
            call(SeasonRepository),
            call(AssociationRepository),
            call(TeamSeasonRepository)
        ])

        fake_season_repository.get_seasons.assert_called_once()
        seasons.sort(key=lambda s: s.year, reverse=True)
        assert session.get('seasons') == [s.to_dict() for s in seasons]
        assert session.get('selected_season_year') == selected_season_year

        fake_association_repository.get_associations.assert_called_once()
        leagues = [a for a in associations if a.parent_id is None]
        active_leagues = [l for l in leagues if l.first_season_year <= selected_season_year
                          and (l.last_season is None or selected_season_year <= l.last_season_year)]
        active_leagues.sort(key=lambda l: l.id, reverse=True)
        assert session.get('leagues') == [l.to_dict() for l in active_leagues]
        assert session.get('selected_league_name') == selected_league_name

        fake_team_season_repository.get_team_seasons_by_season.assert_called_once_with(season_year=selected_season_year)
        assert session.get('team_seasons') == [ts.to_dict() for ts in team_seasons]

        fake_render_template.assert_called_once_with(
            'team_seasons/index.html',
            seasons=seasons, selected_season_year=selected_season_year,
            leagues=active_leagues, selected_league_name=selected_league_name,
            team_seasons=team_seasons
        )
        assert result is fake_render_template.return_value


def _set_up_index(fake_injector, season_year: Optional[int] = None, league_name: Optional[str] = None) \
        -> tuple[list[Season], MagicMock, list[Association], MagicMock, list[TeamSeason], MagicMock]:
    seasons, fake_season_repository = _set_up_index_seasons(season_year)
    associations, fake_association_repository = _set_up_index_associations(league_name)
    team_seasons, fake_team_season_repository = _set_up_index_team_seasons()
    fake_injector.get.side_effect = [
        fake_season_repository, fake_association_repository, fake_team_season_repository
    ]
    return (
        seasons, fake_season_repository,
        associations, fake_association_repository,
        team_seasons, fake_team_season_repository
    )


def _set_up_index_seasons(season_year: Optional[int]) -> tuple[list[Season], MagicMock]:
    fake_season_repository = MagicMock(SeasonRepository)
    seasons = [
        Season(year=1920),
        Season(year=1921),
        Season(year=1922),
    ]
    fake_season_repository.get_seasons.return_value = seasons

    session['selected_season_year'] = season_year

    return seasons, fake_season_repository


def _set_up_index_associations(league_name: Optional[str] = None) -> tuple[list[Association], MagicMock]:
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


def _set_up_index_team_seasons() -> tuple[list[TeamSeason], MagicMock]:
    fake_team_season_repository = MagicMock(TeamSeasonRepository)
    team_seasons = []
    for t in range(3):
        for y in range(1920, 1924):
            team_seasons.append(
                TeamSeason(
                    id=10 * t + y,
                    team_id=t,
                    season_year=y,
                    games=3,
                    wins=1,
                    losses=1,
                    ties=1
                )
            )
    fake_team_season_repository.get_team_seasons_by_season.return_value = team_seasons
    return team_seasons, fake_team_season_repository


@patch('app.flask.team_season_controller.render_template')
@patch('app.flask.team_season_controller.team_season_schedule_repository')
@patch('app.flask.team_season_controller.injector')
def test_details_when_team_season_found_should_render_team_season_details_template(
        fake_injector, fake_team_season_schedule_repository, fake_render_template
):
    # Arrange
    fake_team_season_repository, team_season = _set_up_details(fake_injector)

    # Act
    id = 1
    result = mod.details(id)

    # Assert
    fake_injector.get.assert_called_once_with(TeamSeasonRepository)

    fake_team_season_repository.get_team_season.assert_called_once_with(id)
    fake_team_season_schedule_repository.get_team_season_schedule_profile.assert_called_once_with(
        team_season.team_id, team_season.season_year
    )
    fake_team_season_schedule_repository.get_team_season_schedule_totals.assert_called_once_with(
        team_season.team_id, team_season.season_year
    )
    fake_team_season_schedule_repository.get_team_season_schedule_averages.assert_called_once_with(
        team_season.team_id, team_season.season_year
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
    _, _ = _set_up_details(fake_injector, err=IndexError())

    # Act
    with pytest.raises(NotFound):
        _ = mod.details(1)


def _set_up_details(fake_injector, err: Exception = None) -> tuple[MagicMock, TeamSeason]:
    fake_team_season_repository = MagicMock(TeamSeasonRepository)

    team_season = TeamSeason(team_id=1, season_year=1)

    if err:
        fake_team_season_repository.get_team_season.side_effect = err
    else:
        fake_team_season_repository.get_team_season.return_value = team_season

    fake_injector.get.return_value = fake_team_season_repository

    return fake_team_season_repository, team_season


@pytest.mark.skip('WIP')
@patch('app.flask.team_season_controller.render_template')
@patch('app.flask.team_season_controller.injector')
@patch('app.flask.team_season_controller.request')
def test_select_season_should_render_team_season_index_template_for_selected_season_year(
        fake_request, fake_injector, fake_render_template, test_app
):
    with test_app.test_request_context('/team_seasons/select_season', method='POST'):
        # Arrange
        selected_season_year = 1920
        fake_request.form.get.return_value = str(selected_season_year)

        seasons = [
            Season(year=1920),
            Season(year=1921),
            Season(year=1922),
        ]
        session['seasons'] = seasons

        fake_association_repository, associations = _set_up_index_associations()
        fake_team_season_repository, team_seasons = _set_up_index_team_seasons()
        fake_injector.get.side_effect = [fake_association_repository, fake_team_season_repository]

        # Act
        result = mod.select_season()

        # Assert
        fake_request.form.get.assert_called_once_with('season_dropdown')
        assert session.get('selected_season_year') == selected_season_year

        fake_injector.get.assert_has_calls([
            call(AssociationRepository),
            call(TeamSeasonRepository)
        ])
        fake_association_repository.get_associations.assert_called_once()
        leagues = [a for a in associations if a.parent_id is None]
        active_leagues = [l for l in leagues if l.first_season_year <= selected_season_year
                          and (l.last_season is None or selected_season_year <= l.last_season_year)]
        active_leagues.sort(key=lambda l: l.id, reverse=True)
        assert session.get('leagues') == [l.to_dict() for l in active_leagues]
        selected_league = active_leagues[0]
        assert session.get('selected_league_name') == selected_league.short_name

        fake_team_season_repository.get_team_seasons_by_season.assert_called_once_with(season_year=selected_season_year)
        assert session.get('team_seasons') == [ts.to_dict() for ts in team_seasons]

        fake_render_template.assert_called_once_with(
            'team_seasons/index.html',
            seasons=seasons, selected_season_year=selected_season_year,
            leagues=active_leagues, selected_league_name=selected_league.short_name,
            team_seasons=team_seasons
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
        fake_request.form.get.return_value = str(selected_league_name)

        seasons = [
            Season(year=1920),
            Season(year=1921),
            Season(year=1922),
        ]
        session['seasons'] = seasons

        selected_season_year = 1920
        session['selected_season_year'] = selected_season_year

        fake_association_repository, associations = _set_up_index_associations()
        leagues = [a for a in associations if a.parent_id is None]
        active_leagues = [l for l in leagues if l.first_season_year <= selected_season_year
                          and (l.last_season is None or selected_season_year <= l.last_season_year)]
        active_leagues.sort(key=lambda l: l.id, reverse=True)
        session['leagues'] = active_leagues

        fake_team_season_repository, team_seasons = _set_up_index_team_seasons()

        fake_injector.get.return_value = fake_team_season_repository

        # Act
        result = mod.select_league()

        # Assert
        fake_request.form.get.assert_called_once_with('league_dropdown')
        assert session.get('selected_league_name') == selected_league_name
        kwargs = [l for l in active_leagues if l['short_name'] == selected_league_name][0]
        selected_league = Association(**kwargs)
        fake_injector.get.assert_called_once_with(TeamSeasonRepository)
        fake_team_season_repository.get_team_seasons_by_season.assert_called_once_with(season_year=selected_season_year)
        assert session.get('team_seasons') == [ts.to_dict() for ts in team_seasons]

        fake_render_template.assert_called_once_with(
            'team_seasons/index.html',
            seasons=seasons, selected_season_year=selected_season_year,
            leagues=active_leagues, selected_league_name=selected_league.short_name,
            team_seasons=team_seasons
        )
        assert result is fake_render_template.return_value


@patch('app.flask.team_season_controller.render_template')
@patch('app.flask.team_season_controller.flash')
@patch('app.flask.team_season_controller.injector')
def test_run_weekly_update_should_run_weekly_update(
        fake_injector, fake_flash, fake_render_template, test_app
):
    with test_app.test_request_context('/team_seasons/', method='GET'):
        # Arrange
        fake_weekly_update_service = MagicMock(WeeklyUpdateService)

        fake_association_repository = MagicMock(AssociationRepository)
        selected_league = Association(id=1, long_name="League", short_name="L", parent_id=None)
        fake_association_repository.get_association_by_short_name.return_value = selected_league

        fake_injector.get.side_effect = [fake_weekly_update_service, fake_association_repository]

        selected_league_name = "L"
        session['selected_league_name'] = selected_league_name

        selected_season_year = 1920
        session['selected_season_year'] = selected_season_year

        seasons = [
            Season(year=1920),
            Season(year=1921),
            Season(year=1922),
        ]
        session['seasons'] = [s.to_dict() for s in seasons]

        selected_season_year = 1921
        session['selected_season_year'] = selected_season_year

        # Act
        mod.run_weekly_update()

        # Assert
        fake_injector.get.assert_has_calls([
            call(WeeklyUpdateService),
            call(AssociationRepository),
        ])
        fake_association_repository.get_association_by_short_name.assert_called_once_with(selected_league_name)
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
