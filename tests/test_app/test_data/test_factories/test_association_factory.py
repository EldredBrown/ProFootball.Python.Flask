from unittest.mock import patch, call

import pytest

from app.data.factories import association_factory
from app.data.models.association import Association


def test_create_association_when_key_is_not_in_view_model_map_should_raise_value_error():
    # Arrange
    kwargs = {
        'invalid_key': "Value"
    }

    # Act
    with pytest.raises(KeyError) as err:
        test_association = association_factory.create_association(**kwargs)

    # Assert
    assert err.value.args[0] == f"invalid_key is invalid."


@patch('app.data.factories.association_factory.AssociationRepository')
@patch('app.data.factories.association_factory.injector')
@patch('app.data.factories.association_factory._validate_is_unique')
def test_create_association_when_unique_keys_are_in_kwargs_and_old_association_id_is_not_provided_and_kwargs_long_name_and_short_name_are_unique_should_return_association(
        fake_validate_is_unique, fake_injector,
        fake_association_repository
):
    # Arrange
    kwargs = {
        'long_name': "Association",
        'short_name': "A",
        'parent_name': "P",
        'first_season_year': 1920,
        'last_season_year': None,
    }

    fake_validate_is_unique.return_value = None

    parent_id = 1
    parent = Association(id=parent_id, long_name="Parent", short_name="P")
    fake_association_repository.get_association_by_short_name.return_value = parent
    fake_injector.get.return_value = fake_association_repository

    # Act
    try:
        test_association = association_factory.create_association(**kwargs)
    except ValueError:
        assert False

    # Assert
    error_messages = (
        f"Association already exists with long_name='{kwargs.get('long_name')}'.",
        f"Association already exists with short_name='{kwargs.get('short_name')}'.",
    )
    fake_validate_is_unique.assert_has_calls([
        call('long_name', kwargs.get('long_name'), error_message=error_messages[0]),
        call('short_name', kwargs.get('short_name'), error_message=error_messages[1]),
    ])
    assert isinstance(test_association, Association)
    assert test_association.long_name == kwargs.get('long_name')
    assert test_association.short_name == kwargs.get('short_name')
    fake_injector.get.assert_called_once_with(fake_association_repository)
    fake_association_repository.get_association_by_short_name.assert_called_once_with(kwargs.get('parent_name'))
    assert test_association.parent_id == parent_id
    assert test_association.first_season_year == kwargs.get('first_season_year')
    assert test_association.last_season_year == kwargs.get('last_season_year')


@patch('app.data.factories.association_factory._validate_is_unique')
def test_create_association_when_kwargs_long_name_is_not_unique_should_raise_value_error(
        fake_validate_is_unique
):
    # Arrange
    kwargs = {
        'long_name': "Association",
        'short_name': "A",
        'parent_name': "P",
        'first_season_year': 1920,
        'last_season_year': None,
    }

    error_message = f"Association already exists with long_name='{kwargs.get('long_name')}'."
    fake_validate_is_unique.side_effect = ValueError(error_message)

    # Act
    with pytest.raises(ValueError) as err:
        _ = association_factory.create_association(**kwargs)

    # Assert
    fake_validate_is_unique.assert_called_once_with('long_name', kwargs.get('long_name'), error_message=error_message)
    assert err.value.args[0] == error_message


@patch('app.data.factories.association_factory._validate_is_unique')
def test_create_association_when_kwargs_short_name_is_not_unique_should_raise_value_error(
        fake_validate_is_unique
):
    # Arrange
    kwargs = {
        'long_name': "Association",
        'short_name': "A",
        'parent_name': "P",
        'first_season_year': 1920,
        'last_season_year': None,
    }

    error_messages = (
        f"Association already exists with long_name='{kwargs.get('long_name')}'.",
        f"Association already exists with short_name='{kwargs.get('short_name')}'.",
    )
    fake_validate_is_unique.side_effect = [None, ValueError(error_messages[1])]

    # Act
    with pytest.raises(ValueError) as err:
        _ = association_factory.create_association(**kwargs)

    # Assert
    fake_validate_is_unique.assert_has_calls([
        call('long_name', kwargs.get('long_name'), error_message=error_messages[0]),
        call('short_name', kwargs.get('short_name'), error_message=error_messages[1]),
    ])
    assert err.value.args[0] == error_messages[1]


@patch('app.data.factories.association_factory._validate_is_unique')
@patch('app.data.factories.association_factory.AssociationRepository')
@patch('app.data.factories.association_factory.injector')
def test_create_association_when_old_association_id_is_provided_and_long_name_and_short_name_have_not_changed_should_not_validate_unique_key_values_and_return_association(
        fake_injector, fake_association_repository, fake_validate_is_unique
):
    # Arrange
    kwargs = {
        'id': 1,
        'long_name': "Association",
        'short_name': "A",
        'parent_name': "P",
        'first_season_year': 1920,
        'last_season_year': None,
    }

    error_messages = (
        f"Association already exists with long_name='{kwargs.get('long_name')}'.",
        f"Association already exists with short_name='{kwargs.get('short_name')}'.",
    )
    fake_validate_is_unique.side_effect = [None, ValueError(error_messages[1])]

    old_association = Association(long_name="Association", short_name="A", first_season_year=1920)
    fake_association_repository.get_association.return_value = old_association

    parent_id = 1
    parent = Association(id=parent_id, long_name="Parent", short_name="P")
    fake_association_repository.get_association_by_short_name.return_value = parent
    fake_injector.get.return_value = fake_association_repository

    # Act
    try:
        test_association = association_factory.create_association(**kwargs)
    except ValueError:
        assert False

    # Assert
    fake_injector.get.assert_has_calls([
        call(fake_association_repository),
        call(fake_association_repository),
        call(fake_association_repository),
    ])
    fake_association_repository.get_association.assert_has_calls([
        call(kwargs.get('id')),
        call(kwargs.get('id')),
    ])
    fake_validate_is_unique.assert_not_called()
    assert isinstance(test_association, Association)
    assert test_association.id == kwargs.get('id')
    assert test_association.long_name == kwargs.get('long_name')
    assert test_association.short_name == kwargs.get('short_name')
    fake_association_repository.get_association_by_short_name.assert_called_once_with(kwargs.get('parent_name'))
    assert test_association.parent_id == parent_id
    assert test_association.first_season_year == kwargs.get('first_season_year')
    assert test_association.last_season_year == kwargs.get('last_season_year')


@patch('app.data.factories.association_factory._validate_is_unique')
@patch('app.data.factories.association_factory.AssociationRepository')
@patch('app.data.factories.association_factory.injector')
def test_create_association_when_long_name_has_changed_and_is_not_unique_should_validate_unique_key_values_and_raise_value_error(
        fake_injector, fake_association_repository, fake_validate_is_unique
):
    # Arrange
    kwargs = {
        'id': 1,
        'long_name': "New Association",
        'short_name': "NA",
        'parent_name': "P",
        'first_season_year': 1922,
        'last_season_year': None,
    }

    old_association = Association(
        long_name="Association", short_name="A", parent_id=1, first_season_year=1920, last_season_year=1921
    )
    fake_association_repository.get_association.return_value = old_association
    fake_injector.get.return_value = fake_association_repository

    parent_id = 1
    parent = Association(id=parent_id, long_name="Parent", short_name="P")
    fake_association_repository.get_association_by_short_name.return_value = parent
    fake_injector.get.return_value = fake_association_repository

    fake_validate_is_unique.side_effect = ValueError("long_name must be unique.")

    exp_err_msg = f"Association already exists with long_name='{kwargs.get('long_name')}'."

    # Act
    with pytest.raises(ValueError) as err:
        _ = association_factory.create_association(**kwargs)

    # Assert
    fake_injector.get.assert_called_once()
    fake_association_repository.get_association.assert_called_once_with(kwargs.get('id'))
    fake_validate_is_unique.assert_called_once_with('long_name', kwargs.get('long_name'), error_message=exp_err_msg)


@patch('app.data.factories.association_factory._validate_is_unique')
@patch('app.data.factories.association_factory.AssociationRepository')
@patch('app.data.factories.association_factory.injector')
def test_create_association_when_long_name_is_unique_and_short_name_has_changed_and_is_not_unique_should_validate_unique_key_values_and_raise_value_error(
        fake_injector, fake_association_repository, fake_validate_is_unique
):
    # Arrange
    kwargs = {
        'id': 1,
        'long_name': "New Association",
        'short_name': "NA",
        'parent_name': "P",
        'first_season_year': 1922,
        'last_season_year': None,
    }

    old_association = Association(
        long_name="Association", short_name="A", parent_id=1, first_season_year=1920, last_season_year=1921
    )
    fake_association_repository.get_association.return_value = old_association
    fake_injector.get.return_value = fake_association_repository

    parent_id = 1
    parent = Association(id=parent_id, long_name="Parent", short_name="P")
    fake_association_repository.get_association_by_short_name.return_value = parent
    fake_injector.get.return_value = fake_association_repository

    fake_validate_is_unique.side_effect = [True, ValueError("short_name must be unique.")]

    exp_err_msgs = [
        f"Association already exists with long_name='{kwargs.get('long_name')}'.",
        f"Association already exists with short_name='{kwargs.get('short_name')}'.",
    ]

    # Act
    with pytest.raises(ValueError) as err:
        _ = association_factory.create_association(**kwargs)

    # Assert
    fake_injector.get.assert_has_calls([
        call(fake_association_repository),
        call(fake_association_repository),
    ])
    fake_association_repository.get_association.assert_has_calls([
        call(kwargs.get('id')),
        call(kwargs.get('id')),
    ])
    fake_validate_is_unique.assert_has_calls([
        call('long_name', kwargs.get('long_name'), error_message=exp_err_msgs[0]),
        call('short_name', kwargs.get('short_name'), error_message=exp_err_msgs[1]),
    ])


@patch('app.data.factories.association_factory._validate_is_unique')
@patch('app.data.factories.association_factory.AssociationRepository')
@patch('app.data.factories.association_factory.injector')
def test_create_association_when_short_name_is_unique_should_validate_unique_key_values_and_return_association(
        fake_injector, fake_association_repository, fake_validate_is_unique
):
    # Arrange
    kwargs = {
        'id': 1,
        'long_name': "New Association",
        'short_name': "NA",
        'parent_name': "P",
        'first_season_year': 1922,
        'last_season_year': None,
    }

    old_association = Association(
        long_name="Association", short_name="A", parent_id=1, first_season_year=1920, last_season_year=1921
    )
    fake_association_repository.get_association.return_value = old_association
    fake_injector.get.return_value = fake_association_repository

    parent_id = 1
    parent = Association(id=parent_id, long_name="Parent", short_name="P")
    fake_association_repository.get_association_by_short_name.return_value = parent
    fake_injector.get.return_value = fake_association_repository

    fake_validate_is_unique.side_effect = [True, True]

    exp_err_msgs = [
        f"Association already exists with long_name='{kwargs.get('long_name')}'.",
        f"Association already exists with short_name='{kwargs.get('short_name')}'.",
    ]

    # Act
    try:
        test_association = association_factory.create_association(**kwargs)
    except ValueError:
        assert False

    # Assert
    fake_injector.get.assert_has_calls([
        call(fake_association_repository),
        call(fake_association_repository),
        call(fake_association_repository),
    ])
    fake_association_repository.get_association.assert_has_calls([
        call(kwargs.get('id')),
        call(kwargs.get('id')),
    ])
    fake_validate_is_unique.assert_has_calls([
        call('long_name', kwargs.get('long_name'), error_message=exp_err_msgs[0]),
        call('short_name', kwargs.get('short_name'), error_message=exp_err_msgs[1]),
    ])
    assert isinstance(test_association, Association)
    assert test_association.id == kwargs.get('id')
    assert test_association.long_name == kwargs.get('long_name')
    assert test_association.short_name == kwargs.get('short_name')
    fake_association_repository.get_association_by_short_name.assert_called_once_with(kwargs.get('parent_name'))
    assert test_association.parent_id == parent_id
    assert test_association.first_season_year == kwargs.get('first_season_year')
    assert test_association.last_season_year == kwargs.get('last_season_year')


@patch('app.data.factories.association_factory.Association')
def test_validate_is_unique_when_value_is_not_unique_and_error_message_is_not_provided_should_raise_value_error_with_default_error_message(fake_association):
    # Arrange
    fake_association.query.filter_by.return_value.first.return_value = Association()

    # Act
    with pytest.raises(ValueError) as err:
        _ = association_factory._validate_is_unique('short_name', "L")

    # Assert
    assert err.value.args[0] == "short_name must be unique."


@patch('app.data.factories.association_factory.Association')
def test_validate_is_unique_when_value_is_not_unique_and_error_message_is_provided_should_raise_value_error_with_provided_error_message(fake_association):
    # Arrange
    fake_association.query.filter_by.return_value.first.return_value = Association()

    error_message = f"Association already exists with short_name=A."

    # Act
    with pytest.raises(ValueError) as err:
        _ = association_factory._validate_is_unique('short_name', "A", error_message=error_message)

    # Assert
    assert err.value.args[0] == error_message


@patch('app.data.factories.association_factory.AssociationRepository')
@patch('app.data.factories.association_factory.injector')
def test_value_has_changed_when_new_value_equals_old_value_should_return_false(
        fake_injector, fake_association_repository
):
    # Arrange
    kwargs = {
        'id': 1,
        'long_name': "Association",
    }

    old_association = Association(long_name="Association", short_name="A", first_season_year=1920)
    fake_association_repository.get_association.return_value = old_association
    fake_injector.get.return_value = fake_association_repository

    # Act
    result = association_factory._value_has_changed('long_name', **kwargs)

    # Assert
    assert result is False
    fake_injector.get.assert_called_once_with(fake_association_repository)
    fake_association_repository.get_association.assert_called_once_with(kwargs.get('id'))


@patch('app.data.factories.association_factory.AssociationRepository')
@patch('app.data.factories.association_factory.injector')
def test_value_has_changed_when_new_value_does_not_equal_old_value_should_return_true(
        fake_injector, fake_association_repository
):
    # Arrange
    kwargs = {
        'id': 1,
        'long_name': "New Association",
    }

    old_association = Association(long_name="Old Association", short_name="OA", first_season_year=1920)
    fake_association_repository.get_association.return_value = old_association
    fake_injector.get.return_value = fake_association_repository

    # Act
    result = association_factory._value_has_changed('long_name', **kwargs)

    # Assert
    assert result is True
    fake_injector.get.assert_called_once_with(fake_association_repository)
    fake_association_repository.get_association.assert_called_once_with(kwargs.get('id'))
