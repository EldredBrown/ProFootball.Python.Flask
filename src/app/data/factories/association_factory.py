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
        if key == 'parent_name':
            association_repository = injector.get(AssociationRepository)
            association = association_repository.get_association_by_short_name(value)
            if association is None:
                parent_id = None if value is None or value == '' else -1
            else:
                parent_id = association.id
            model_kwargs['parent_id'] = parent_id
        else:
            model_kwargs[view_model_map[key]] = value

    return Association(**model_kwargs)
