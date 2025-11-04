from decimal import Decimal
from unittest.mock import patch, call

import pytest

from sqlalchemy.exc import IntegrityError

from test_app import create_app

from app.data.models.team_season import TeamSeason
from app.data.repositories.team_season_repository import TeamSeasonRepository


@pytest.fixture
def test_repo():
    return TeamSeasonRepository()


@patch('app.data.repositories.team_season_repository.TeamSeason')
def test_get_team_seasons_should_get_team_seasons(fake_team_season, test_repo):
    # Arrange
    team_seasons_in = [
        TeamSeason(
            team_name="Team 1",
            season_year=1,
            league_name="League"
        ),
        TeamSeason(
            team_name="Team 2",
            season_year=1,
            league_name="League"
        ),
        TeamSeason(
            team_name="Team 3",
            season_year=1,
            league_name="League"
        ),
    ]
    fake_team_season.query.all.return_value = team_seasons_in

    # Act
    test_repo = TeamSeasonRepository()
    team_seasons_out = test_repo.get_team_seasons()

    # Assert
    assert team_seasons_out == team_seasons_in


@patch('app.data.repositories.team_season_repository.TeamSeason')
def test_get_team_seasons_by_season_year_when_season_year_is_none_should_get_empty_list(fake_team_season, test_repo):
    # Arrange
    team_seasons_in = [
        TeamSeason(
            team_name="Team 1",
            season_year=1,
            league_name="League"
        ),
        TeamSeason(
            team_name="Team 2",
            season_year=1,
            league_name="League"
        ),
        TeamSeason(
            team_name="Team 3",
            season_year=1,
            league_name="League"
        ),
        TeamSeason(
            team_name="Team 1",
            season_year=2,
            league_name="League"
        ),
        TeamSeason(
            team_name="Team 2",
            season_year=2,
            league_name="League"
        ),
        TeamSeason(
            team_name="Team 3",
            season_year=2,
            league_name="League"
        ),
        TeamSeason(
            team_name="Team 1",
            season_year=3,
            league_name="League"
        ),
        TeamSeason(
            team_name="Team 2",
            season_year=3,
            league_name="League"
        ),
        TeamSeason(
            team_name="Team 3",
            season_year=3,
            league_name="League"
        ),
    ]
    filter_year = 2
    fake_team_season.query.filter_by.return_value.all.return_value = [
        x for x in team_seasons_in if x.season_year == filter_year
    ]

    # Act
    test_repo = TeamSeasonRepository()
    team_seasons_out = test_repo.get_team_seasons_by_season_year(season_year=None)

    # Assert
    assert team_seasons_out == []


@patch('app.data.repositories.team_season_repository.TeamSeason')
def test_get_team_seasons_by_season_year_when_season_year_is_not_none_should_get_team_seasons_for_the_specified_season_year(
        fake_team_season, test_repo
):
    # Arrange
    team_seasons_in = [
        TeamSeason(
            team_name="Team 1",
            season_year=1,
            league_name="League"
        ),
        TeamSeason(
            team_name="Team 2",
            season_year=1,
            league_name="League"
        ),
        TeamSeason(
            team_name="Team 3",
            season_year=1,
            league_name="League"
        ),
        TeamSeason(
            team_name="Team 1",
            season_year=2,
            league_name="League"
        ),
        TeamSeason(
            team_name="Team 2",
            season_year=2,
            league_name="League"
        ),
        TeamSeason(
            team_name="Team 3",
            season_year=2,
            league_name="League"
        ),
        TeamSeason(
            team_name="Team 1",
            season_year=3,
            league_name="League"
        ),
        TeamSeason(
            team_name="Team 2",
            season_year=3,
            league_name="League"
        ),
        TeamSeason(
            team_name="Team 3",
            season_year=3,
            league_name="League"
        ),
    ]
    filter_year = 2
    fake_team_season.query.filter_by.return_value.all.return_value = [
        x for x in team_seasons_in if x.season_year == filter_year
    ]

    # Act
    test_repo = TeamSeasonRepository()
    team_seasons_out = test_repo.get_team_seasons_by_season_year(season_year=filter_year)

    # Assert
    for team_season in team_seasons_out:
        assert team_season.season_year == filter_year


@patch('app.data.repositories.team_season_repository.TeamSeason')
def test_get_team_season_when_team_seasons_is_empty_should_return_none(fake_team_season, test_repo):
    # Arrange
    team_seasons_in = []
    fake_team_season.query.all.return_value = team_seasons_in

    # Act
    test_repo = TeamSeasonRepository()
    team_season_out = test_repo.get_team_season(1)

    # Assert
    assert team_season_out is None


@patch('app.data.repositories.team_season_repository.TeamSeason')
def test_get_team_season_when_team_seasons_is_not_empty_and_team_season_is_not_found_should_return_none(
        fake_team_season, test_repo
):
    # Arrange
    team_seasons_in = [
        TeamSeason(
            team_name="Team 1",
            season_year=1,
            league_name="League"
        ),
        TeamSeason(
            team_name="Team 2",
            season_year=1,
            league_name="League"
        ),
        TeamSeason(
            team_name="Team 3",
            season_year=1,
            league_name="League"
        ),
    ]
    fake_team_season.query.all.return_value = team_seasons_in
    fake_team_season.query.get.return_value = None

    # Act
    test_repo = TeamSeasonRepository()

    id = len(team_seasons_in) + 1
    team_season_out = test_repo.get_team_season(id)

    # Assert
    assert team_season_out is None


@patch('app.data.repositories.team_season_repository.TeamSeason')
def test_get_team_season_when_team_seasons_is_not_empty_and_team_season_is_found_should_return_team_season(
        fake_team_season, test_repo
):
    # Arrange
    team_seasons_in = [
        TeamSeason(
            team_name="Team 1",
            season_year=1,
            league_name="League"
        ),
        TeamSeason(
            team_name="Team 2",
            season_year=1,
            league_name="League"
        ),
        TeamSeason(
            team_name="Team 3",
            season_year=1,
            league_name="League"
        ),
    ]
    fake_team_season.query.all.return_value = team_seasons_in

    id = len(team_seasons_in) - 1
    fake_team_season.query.get.return_value = team_seasons_in[id]

    # Act
    test_repo = TeamSeasonRepository()
    team_season_out = test_repo.get_team_season(id)

    # Assert
    assert team_season_out is team_seasons_in[id]


@patch('app.data.repositories.team_season_repository.TeamSeason')
def test_get_team_season_by_team_name_and_season_year_should_return_team_season_with_specified_team_name_and_season_year(
        fake_team_season, test_repo
):
    # Arrange
    team_name = "Team"
    season_year = 1

    # Act
    test_repo = TeamSeasonRepository()
    team_season = test_repo.get_team_season_by_team_name_and_season_year(team_name, season_year)

    # Assert
    fake_team_season.query.filter_by.assert_called_once_with(team_name=team_name, season_year=season_year)
    fake_team_season.query.filter_by.return_value.first.assert_called_once()
    assert team_season is fake_team_season.query.filter_by.return_value.first.return_value


@patch('app.data.repositories.team_season_repository.TeamSeason')
def test_team_season_exists_when_team_season_does_not_exist_should_return_false(fake_team_season, test_repo):
    # Arrange
    team_seasons = [
        TeamSeason(
            team_name="Team 1",
            season_year=1,
            league_name="League"
        ),
        TeamSeason(
            team_name="Team 2",
            season_year=1,
            league_name="League"
        ),
        TeamSeason(
            team_name="Team 3",
            season_year=1,
            league_name="League"
        ),
    ]
    fake_team_season.query.all.return_value = team_seasons
    fake_team_season.query.get.return_value = None

    # Act
    test_repo = TeamSeasonRepository()
    team_season_exists = test_repo.team_season_exists(id=1)

    # Assert
    assert not team_season_exists


@patch('app.data.repositories.team_season_repository.TeamSeason')
def test_team_season_exists_when_team_season_exists_should_return_true(fake_team_season, test_repo):
    # Arrange
    team_seasons = [
        TeamSeason(
            team_name="Team 1",
            season_year=1,
            league_name="League"
        ),
        TeamSeason(
            team_name="Team 2",
            season_year=1,
            league_name="League"
        ),
        TeamSeason(
            team_name="Team 3",
            season_year=1,
            league_name="League"
        ),
    ]
    fake_team_season.query.all.return_value = team_seasons
    fake_team_season.query.get.return_value = team_seasons[1]

    # Act
    test_repo = TeamSeasonRepository()
    team_season_exists = test_repo.team_season_exists(id=1)

    # Assert
    assert team_season_exists


@patch('app.data.repositories.team_season_repository.TeamSeason')
def test_team_season_exists_with_team_name_and_season_year_when_team_season_does_not_exist_should_return_false(
        fake_team_season, test_repo
):
    # Arrange
    fake_team_season.query.filter_by.return_value.first.return_value = None

    # Act
    test_repo = TeamSeasonRepository()
    team_season_exists = test_repo.team_season_exists_with_team_name_and_season_year(
        team_name="Team", season_year=1
    )

    # Assert
    assert not team_season_exists


@patch('app.data.repositories.team_season_repository.TeamSeason')
def test_team_season_exists_with_team_name_and_season_year_when_team_season_exists_should_return_true(
        fake_team_season, test_repo
):
    # Arrange
    team_season = TeamSeason(
        team_name="Team",
        season_year=1,
        league_name="League"
    ),
    fake_team_season.query.filter_by.return_value.first.return_value = team_season

    # Act
    test_repo = TeamSeasonRepository()
    team_season_exists = test_repo.team_season_exists_with_team_name_and_season_year(
        team_name="Team", season_year=1
    )

    # Assert
    assert team_season_exists


@patch('app.data.repositories.team_season_repository.try_commit')
@patch('app.data.repositories.team_season_repository.sqla')
@patch('app.data.repositories.team_season_repository.TeamSeasonRepository.team_season_exists')
def test_update_team_season_when_no_team_season_exists_with_id_should_return_team_season_and_not_update_database(
        fake_team_season_exists, fake_sqla, fake_try_commit, test_repo
):
    # Arrange
    fake_team_season_exists.return_value = False

    # Act
    test_repo = TeamSeasonRepository()
    team_season = TeamSeason(
        team_name="Team",
        season_year=1,
        league_name="League"
    )
    try:
        team_season_updated = test_repo.update_team_season(team_season)
    except ValueError:
        assert False

    # Assert
    fake_sqla.session.add.assert_not_called()
    fake_try_commit.assert_not_called()
    assert isinstance(team_season_updated, TeamSeason)
    assert team_season_updated.team_name == team_season.team_name
    assert team_season_updated.season_year == team_season.season_year
    assert team_season_updated.league_name == team_season.league_name
    assert team_season_updated.conference_name == team_season.conference_name
    assert team_season_updated.division_name == team_season.division_name
    assert team_season_updated.games == team_season.games
    assert team_season_updated.wins == team_season.wins
    assert team_season_updated.losses == team_season.losses
    assert team_season_updated.ties == team_season.ties
    assert team_season_updated.winning_percentage == team_season.winning_percentage
    assert team_season_updated.points_for == team_season.points_for
    assert team_season_updated.points_against == team_season.points_against
    assert team_season_updated.expected_wins == team_season.expected_wins
    assert team_season_updated.expected_losses == team_season.expected_losses
    assert team_season_updated.offensive_average == team_season.offensive_average
    assert team_season_updated.offensive_factor == team_season.offensive_factor
    assert team_season_updated.offensive_index == team_season.offensive_index
    assert team_season_updated.defensive_average == team_season.defensive_average
    assert team_season_updated.defensive_factor == team_season.defensive_factor
    assert team_season_updated.defensive_index == team_season.defensive_index
    assert team_season_updated.final_expected_winning_percentage == team_season.final_expected_winning_percentage


@patch('app.data.repositories.team_season_repository.try_commit')
@patch('app.data.repositories.team_season_repository.sqla')
@patch('app.data.repositories.team_season_repository.TeamSeason')
@patch('app.data.repositories.team_season_repository.TeamSeasonRepository.team_season_exists')
def test_update_team_season_when_team_season_exists_with_id_and_no_integrity_error_caught_should_return_team_season_and_update_database(
        fake_team_season_exists, fake_team_season, fake_sqla, fake_try_commit, test_repo
):
    # Arrange
    fake_team_season_exists.return_value = True

    team_seasons = [
        TeamSeason(
            id=1,
            team_name="Team 1",
            season_year=1,
            league_name="League 1",
            conference_name="Conference 1",
            division_name="Division 1",
            games=1,
            wins=1,
            losses=1,
            ties=1,
            winning_percentage=Decimal('1.000'),
            points_for=1,
            points_against=1,
            expected_wins=Decimal('1.0'),
            expected_losses=Decimal('1.0'),
            offensive_average=Decimal('1.00'),
            offensive_factor=Decimal('1.000'),
            offensive_index=Decimal('1.00'),
            defensive_average=Decimal('1.00'),
            defensive_factor=Decimal('1.000'),
            defensive_index=Decimal('1.00'),
            final_expected_winning_percentage=Decimal('1.000')
        ),
        TeamSeason(
            id=2,
            team_name="Team 2",
            season_year=2,
            league_name="League 2",
            conference_name="Conference 2",
            division_name="Division 2",
            games=2,
            wins=2,
            losses=2,
            ties=2,
            winning_percentage=Decimal('2.000'),
            points_for=2,
            points_against=2,
            expected_wins=Decimal('2.0'),
            expected_losses=Decimal('2.0'),
            offensive_average=Decimal('2.00'),
            offensive_factor=Decimal('2.000'),
            offensive_index=Decimal('2.00'),
            defensive_average=Decimal('2.00'),
            defensive_factor=Decimal('2.000'),
            defensive_index=Decimal('2.00'),
            final_expected_winning_percentage=Decimal('2.000')
        ),
        TeamSeason(
            id=3,
            team_name="Team 3",
            season_year=3,
            league_name="League 3",
            conference_name="Conference 3",
            division_name="Division 3",
            games=3,
            wins=3,
            losses=3,
            ties=3,
            winning_percentage=Decimal('3.000'),
            points_for=3,
            points_against=3,
            expected_wins=Decimal('3.0'),
            expected_losses=Decimal('3.0'),
            offensive_average=Decimal('3.00'),
            offensive_factor=Decimal('3.000'),
            offensive_index=Decimal('3.00'),
            defensive_average=Decimal('3.00'),
            defensive_factor=Decimal('3.000'),
            defensive_index=Decimal('3.00'),
            final_expected_winning_percentage=Decimal('3.000')
        ),
    ]
    fake_team_season.query.all.return_value = team_seasons

    old_team_season = team_seasons[1]
    fake_team_season.query.get.return_value = old_team_season

    new_team_season = TeamSeason(
        id=2,
        team_name="Team 4",
        season_year=4,
        league_name="League 4",
        conference_name="Conference 4",
        division_name="Division 4",
        games=4,
        wins=4,
        losses=4,
        ties=4,
        winning_percentage=Decimal('4.000'),
        points_for=4,
        points_against=4,
        expected_wins=Decimal('4.0'),
        expected_losses=Decimal('4.0'),
        offensive_average=Decimal('4.00'),
        offensive_factor=Decimal('4.000'),
        offensive_index=Decimal('4.00'),
        defensive_average=Decimal('4.00'),
        defensive_factor=Decimal('4.000'),
        defensive_index=Decimal('4.00'),
        final_expected_winning_percentage=Decimal('4.000')
    )

    # Act
    test_repo = TeamSeasonRepository()
    try:
        team_season_updated = test_repo.update_team_season(new_team_season)
    except ValueError:
        assert False

    # Assert
    fake_sqla.session.add.assert_called_once_with(old_team_season)
    fake_try_commit.assert_called_once()
    assert isinstance(team_season_updated, TeamSeason)
    assert team_season_updated.team_name == new_team_season.team_name
    assert team_season_updated.season_year == new_team_season.season_year
    assert team_season_updated.league_name == new_team_season.league_name
    assert team_season_updated.conference_name == new_team_season.conference_name
    assert team_season_updated.division_name == new_team_season.division_name
    assert team_season_updated.games == new_team_season.games
    assert team_season_updated.wins == new_team_season.wins
    assert team_season_updated.losses == new_team_season.losses
    assert team_season_updated.ties == new_team_season.ties
    assert team_season_updated.winning_percentage == new_team_season.winning_percentage
    assert team_season_updated.points_for == new_team_season.points_for
    assert team_season_updated.points_against == new_team_season.points_against
    assert team_season_updated.expected_wins == new_team_season.expected_wins
    assert team_season_updated.expected_losses == new_team_season.expected_losses
    assert team_season_updated.offensive_average == new_team_season.offensive_average
    assert team_season_updated.offensive_factor == new_team_season.offensive_factor
    assert team_season_updated.offensive_index == new_team_season.offensive_index
    assert team_season_updated.defensive_average == new_team_season.defensive_average
    assert team_season_updated.defensive_factor == new_team_season.defensive_factor
    assert team_season_updated.defensive_index == new_team_season.defensive_index
    assert team_season_updated.final_expected_winning_percentage == new_team_season.final_expected_winning_percentage
    assert team_season_updated is new_team_season


@patch('app.data.repositories.team_season_repository.try_commit')
@patch('app.data.repositories.team_season_repository.sqla')
@patch('app.data.repositories.team_season_repository.TeamSeason')
@patch('app.data.repositories.team_season_repository.TeamSeasonRepository.team_season_exists')
def test_update_team_season_when_and_team_season_exists_with_id_and_integrity_error_caught_should_rollback_transaction_and_reraise_error(
        fake_team_season_exists, fake_team_season, fake_sqla, fake_try_commit, test_repo
):
    # Arrange
    fake_team_season_exists.return_value = True

    team_seasons = [
        TeamSeason(
            id=1,
            team_name="Team 1",
            season_year=1,
            league_name="League 1",
            conference_name="Conference 1",
            division_name="Division 1",
            games=1,
            wins=1,
            losses=1,
            ties=1,
            winning_percentage=Decimal('1.000'),
            points_for=1,
            points_against=1,
            expected_wins=Decimal('1.0'),
            expected_losses=Decimal('1.0'),
            offensive_average=Decimal('1.00'),
            offensive_factor=Decimal('1.000'),
            offensive_index=Decimal('1.00'),
            defensive_average=Decimal('1.00'),
            defensive_factor=Decimal('1.000'),
            defensive_index=Decimal('1.00'),
            final_expected_winning_percentage=Decimal('1.000')
        ),
        TeamSeason(
            id=2,
            team_name="Team 2",
            season_year=2,
            league_name="League 2",
            conference_name="Conference 2",
            division_name="Division 2",
            games=2,
            wins=2,
            losses=2,
            ties=2,
            winning_percentage=Decimal('2.000'),
            points_for=2,
            points_against=2,
            expected_wins=Decimal('2.0'),
            expected_losses=Decimal('2.0'),
            offensive_average=Decimal('2.00'),
            offensive_factor=Decimal('2.000'),
            offensive_index=Decimal('2.00'),
            defensive_average=Decimal('2.00'),
            defensive_factor=Decimal('2.000'),
            defensive_index=Decimal('2.00'),
            final_expected_winning_percentage=Decimal('2.000')
        ),
        TeamSeason(
            id=3,
            team_name="Team 3",
            season_year=3,
            league_name="League 3",
            conference_name="Conference 3",
            division_name="Division 3",
            games=3,
            wins=3,
            losses=3,
            ties=3,
            winning_percentage=Decimal('3.000'),
            points_for=3,
            points_against=3,
            expected_wins=Decimal('3.0'),
            expected_losses=Decimal('3.0'),
            offensive_average=Decimal('3.00'),
            offensive_factor=Decimal('3.000'),
            offensive_index=Decimal('3.00'),
            defensive_average=Decimal('3.00'),
            defensive_factor=Decimal('3.000'),
            defensive_index=Decimal('3.00'),
            final_expected_winning_percentage=Decimal('3.000')
        ),
    ]
    fake_team_season.query.all.return_value = team_seasons

    old_team_season = team_seasons[1]
    fake_team_season.query.get.return_value = old_team_season

    new_team_season = TeamSeason(
        id=2,
        team_name="Team 4",
        season_year=4,
        league_name="League 4",
        conference_name="Conference 4",
        division_name="Division 4",
        games=4,
        wins=4,
        losses=4,
        ties=4,
        winning_percentage=Decimal('4.000'),
        points_for=4,
        points_against=4,
        expected_wins=Decimal('4.0'),
        expected_losses=Decimal('4.0'),
        offensive_average=Decimal('2.00'),
        offensive_factor=Decimal('2.000'),
        offensive_index=Decimal('4.00'),
        defensive_average=Decimal('2.00'),
        defensive_factor=Decimal('2.000'),
        defensive_index=Decimal('4.00'),
        final_expected_winning_percentage=Decimal('4.000')
    )

    fake_try_commit.side_effect = IntegrityError('statement', 'params', Exception())

    # Act
    test_repo = TeamSeasonRepository()
    with pytest.raises(IntegrityError):
        team_season_updated = test_repo.update_team_season(new_team_season)

    # Assert
    fake_sqla.session.add.assert_called_once_with(old_team_season)
    fake_try_commit.assert_called_once()
