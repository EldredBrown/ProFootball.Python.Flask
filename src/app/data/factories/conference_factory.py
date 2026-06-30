from app import injector
from app.data.models.conference import Conference
from app.data.repositories.conference_repository import ConferenceRepository
from app.data.repositories.league_repository import LeagueRepository


def create_conference(**kwargs) -> Conference:
    view_model_map = {
        'id':                   'id',
        'short_name':           'short_name',
        'long_name':            'long_name',
        'league_name':          'league_id',
        'first_season_year':    'first_season_id',
        'last_season_year':     'last_season_id',
    }

    model_kwargs = dict()
    for key in kwargs.keys():
        if key not in view_model_map:
            raise KeyError(f"{key} is invalid.")

        value = kwargs.get(key)
        if key in ['short_name', 'long_name']:
            error_message = f"Conference already exists with {key}={value}."
            if 'id' in kwargs:
                if _value_has_changed(key, **kwargs):
                    _validate_is_unique(key, value, error_message=error_message)
            else:
                _validate_is_unique(key, value, error_message=error_message)
            model_kwargs[key] = value
        elif key == 'league_name':
            league_repository = injector.get(LeagueRepository)
            league = league_repository.get_league_by_short_name(value)
            model_kwargs[view_model_map[key]] = league.id if league is not None else -1
        else:    # key in ['id', 'first_season_year', 'last_season_year']:
            model_kwargs[view_model_map[key]] = value

    return Conference(**model_kwargs)


def _validate_is_unique(key, value, error_message=None):
    if Conference.query.filter_by(**{key: value}).first() is not None:
        if not error_message:
            error_message = f"{key} must be unique."
        raise ValueError(error_message)


def _value_has_changed(key: str, **kwargs) -> bool:
    id = kwargs.get('id')
    conference_repository = injector.get(ConferenceRepository)
    old_conference = conference_repository.get_conference(id)
    return kwargs.get(key) != old_conference.__dict__[key]
