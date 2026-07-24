from unittest.mock import patch, MagicMock

import pytest

import app.data.factories.association_factory as mod
from app.data.models.association import Association
from app.data.repositories.association_repository import AssociationRepository


def test_create_association_when_key_is_not_in_view_model_map_should_raise_value_error():
    # Arrange
    kwargs = {
        'invalid_key': "Value"
    }

    # Act
    with pytest.raises(KeyError) as err:
        _ = mod.create_association(**kwargs)

    # Assert
    assert err.value.args[0] == f"invalid_key is invalid."


@pytest.mark.parametrize(
    ("parent", "parent_name", "expected"),
    [
        (None, None, None),
        (None, '', None),
        (None, 'value', -1),
        (Association(id=1, long_name="Parent", short_name="P", parent_id=None), None, 1),
        (Association(id=1, long_name="Parent", short_name="P", parent_id=None), '', 1),
        (Association(id=1, long_name="Parent", short_name="P", parent_id=None), 'value', 1),
    ]
)
@patch('app.data.factories.association_factory.injector')
def test_create_game_should_return_game(fake_injector, parent, parent_name, expected):
    # Arrange
    kwargs = {
        'long_name': "Association",
        'short_name': "A",
        'parent_name': parent_name,
        'first_season_year': 1920,
        'last_season_year': 1922,
    }

    fake_association_repository = MagicMock(AssociationRepository)
    fake_association_repository.get_association_by_short_name.return_value = parent
    fake_injector.get.return_value = fake_association_repository

    # Act
    test_association = mod.create_association(**kwargs)

    # Assert
    assert isinstance(test_association, Association)
    assert test_association.long_name == kwargs.get('long_name')
    assert test_association.short_name == kwargs.get('short_name')

    fake_injector.get.assert_called_once_with(AssociationRepository)
    fake_association_repository.get_association_by_short_name.assert_called_once_with(kwargs.get('parent_name'))
    assert test_association.parent_id == expected

    assert test_association.first_season_year == kwargs.get('first_season_year')
    assert test_association.last_season_year == kwargs.get('last_season_year')
