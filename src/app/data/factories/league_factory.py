from app import injector
from app.data.models.league import League
from app.data.repositories.league_repository import LeagueRepository


def create_league(**kwargs) -> League:
    view_model_map = {
        'id':                   'id',
        'short_name':           'short_name',
        'long_name':            'long_name',
        'first_season_year':    'first_season_id',
        'last_season_year':     'last_season_id',
    }

    model_kwargs = dict()
    for key in kwargs.keys():
        if key not in view_model_map:
            raise KeyError(f"{key} is invalid.")

        value = kwargs.get(key)
        if key in ['short_name', 'long_name']:
            error_message = f"League already exists with {key}={value}."
            if 'id' in kwargs:
                if _value_has_changed(key, **kwargs):
                    _validate_is_unique(key, value, error_message=error_message)
            else:
                _validate_is_unique(key, value, error_message=error_message)
            model_kwargs[key] = value
        else:    # key in ['id', 'first_season_year', 'last_season_year']:
            model_kwargs[view_model_map[key]] = value

    return League(**model_kwargs)


def _validate_is_unique(key, value, error_message=None):
    if League.query.filter_by(**{key: value}).first() is not None:
        if not error_message:
            error_message = f"{key} must be unique."
        raise ValueError(error_message)


def _value_has_changed(key: str, **kwargs) -> bool:
    id = kwargs.get('id')
    league_repository = injector.get(LeagueRepository)
    old_league = league_repository.get_league(id)
    return kwargs[key] != old_league.__dict__[key]
