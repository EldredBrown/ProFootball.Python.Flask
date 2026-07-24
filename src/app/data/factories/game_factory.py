from app import injector
from app.data.models.game import Game
from app.data.repositories.association_repository import AssociationRepository


def create_game(**kwargs) -> Game:
    view_model_map = {
        'id':           'id',
        'season_year':  'season_year',
        'league_name':  'league_id',
        'week':         'week',
        'guest_name':   'guest_name',
        'guest_score':  'guest_score',
        'host_name':    'host_name',
        'host_score':   'host_score',
        'is_playoff':   'is_playoff',
        'notes':        'notes',
    }

    model_kwargs = dict()
    for key in kwargs.keys():
        if key not in view_model_map:
            raise KeyError(f"{key} is invalid.")

        value = kwargs.get(key)
        if key == 'league_name':
            association_repository = injector.get(AssociationRepository)
            league = association_repository.get_association_by_short_name(value)
            if league is None:
                league_id = None if value is None or value == '' else -1
            else:
                league_id = league.id
            model_kwargs['league_id'] = league_id
        else:
            model_kwargs[view_model_map[key]] = value

    return Game(**model_kwargs)
