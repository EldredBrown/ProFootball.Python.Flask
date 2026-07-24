from typing import Optional
from unittest.mock import patch, MagicMock, call

import pytest

from app.data.factories import team_season_factory
from app.data.models.association import Association
from app.data.models.team import Team
from app.data.models.team_season import TeamSeason
from app.data.repositories.association_repository import AssociationRepository
from app.data.repositories.team_repository import TeamRepository


def test_create_team_season_when_key_is_not_in_view_model_map_should_raise_value_error():
    # Arrange
    kwargs = {
        'invalid_key': "Value"
    }

    # Act
    with pytest.raises(KeyError) as err:
        test_team_season = team_season_factory.create_team_season(**kwargs)

    # Assert
    assert err.value.args[0] == f"invalid_key is invalid."


@pytest.mark.parametrize(
    ('team', 'exp_team_id', 'league', 'exp_league_id', 'conference', 'exp_conference_id', 'division', 'exp_division_id'),
    [
        (
                None, -1,
                None, -1,
                None, None,
                None, None
        ),
        (
                Team(id=1, name="Team"), 1,
                None, -1,
                None, None,
                None, None
        ),
        (
                Team(id=1, name="Team"), 1,
                Association(id=1, long_name="League", short_name="L", parent_id=None), 1,
                None, None,
                None, None
        ),
        (
                Team(id=1, name="Team"), 1,
                Association(id=1, long_name="League", short_name="L", parent_id=None), 1,
                Association(id=2, long_name="Conference", short_name="C", parent_id=1), 2,
                None, None
        ),
        (
                Team(id=1, name="Team"), 1,
                Association(id=1, long_name="League", short_name="L", parent_id=None), 1,
                Association(id=2, long_name="Conference", short_name="C", parent_id=1), 2,
                Association(id=3, long_name="Division", short_name="D", parent_id=2), 3
        ),
    ]
)
@patch('app.data.factories.team_season_factory.injector')
def test_create_team_season_should_set_team_id_league_id_conference_id_and_division_id_to_correct_values_and_create_team_season(
        fake_injector,
        team, exp_team_id,
        league, exp_league_id,
        conference, exp_conference_id,
        division, exp_division_id
):
    # Arrange
    kwargs = {
        'id': 1,
        'team_name': None,
        'season_year': 1920,
        'league_name': None,
        'conference_name': None,
        'division_name': None,
    }

    fake_association_repository = MagicMock(AssociationRepository)
    fake_association_repository.get_association_by_short_name.side_effect = [league, conference, division]

    fake_team_repository = MagicMock(TeamRepository)
    fake_team_repository.get_team_by_name.return_value = team

    fake_injector.get.side_effect = [fake_association_repository, fake_team_repository]

    # Act
    result = team_season_factory.create_team_season(**kwargs)

    # Assert
    assert isinstance(result, TeamSeason)
    assert result.id == 1

    fake_team_repository.get_team_by_name.assert_called_once_with(kwargs.get('team_name'))
    assert result.team_id == exp_team_id

    assert result.season_year == 1920

    fake_association_repository.get_association_by_short_name.assert_has_calls([
        call(kwargs.get('league_name')),
        call(kwargs.get('conference_name')),
        call(kwargs.get('division_name')),
    ])
    assert result.league_id == exp_league_id
    assert result.conference_id == exp_conference_id
    assert result.division_id == exp_division_id
