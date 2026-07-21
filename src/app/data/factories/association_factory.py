from app import injector
from app.data.models.association import Association
from app.data.repositories.association_repository import AssociationRepository


def create_association(**kwargs) -> Association:
    view_model_map = {
        'id':                   'id',
        'long_name':            'long_name',
        'short_name':           'short_name',
        'parent_name':          'parent_id',
        'first_season_year':    'first_season_year',
        'last_season_year':     'last_season_year',
    }

    model_kwargs = dict()
    for key in kwargs.keys():
        if key not in view_model_map:
            raise KeyError(f"{key} is invalid.")

        value = kwargs.get(key)
        if key in ['long_name', 'short_name']:
            error_message = f"Association already exists with {key}='{value}'."
            if 'id' in kwargs:
                if _value_has_changed(key, **kwargs):
                    _validate_is_unique(key, value, error_message=error_message)
            else:
                _validate_is_unique(key, value, error_message=error_message)
            model_kwargs[view_model_map[key]] = value
        elif key == 'parent_name':
            association_repository = injector.get(AssociationRepository)
            parent_id = association_repository.get_association_by_short_name(kwargs.get('parent_name')).id
            model_kwargs[view_model_map[key]] = parent_id
        else:    # key in ['id', 'first_season_year', 'last_season_year']:
            model_kwargs[view_model_map[key]] = value

    return Association(**model_kwargs)


def _validate_is_unique(key, value, error_message=None):
    if Association.query.filter_by(**{key: value}).first() is not None:
        if not error_message:
            error_message = f"{key} must be unique."
        raise ValueError(error_message)


def _value_has_changed(key: str, **kwargs) -> bool:
    id = kwargs.get('id')
    association_repository = injector.get(AssociationRepository)
    old_association = association_repository.get_association(id)
    return kwargs[key] != old_association.__dict__[key]
