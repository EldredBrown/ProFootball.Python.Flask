import pytest

import app.data.factories.team_factory as mod
from app.data.models.team import Team


def test_create_team_when_key_is_not_in_view_model_map_should_raise_value_error():
    # Arrange
    kwargs = {
        'invalid_key': "Value"
    }

    # Act
    with pytest.raises(KeyError) as err:
        _ = mod.create_team(**kwargs)

    # Assert
    assert err.value.args[0] == f"invalid_key is invalid."


def test_create_team_should_return_game():
    # Arrange
    kwargs = {
        'name': "Team",
    }

    # Act
    test_team = mod.create_team(**kwargs)

    # Assert
    assert isinstance(test_team, Team)
    assert test_team.name == kwargs.get('name')
