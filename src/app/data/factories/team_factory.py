from app import injector
from app.data.models.team import Team
from app.data.repositories.team_repository import TeamRepository


def create_team(**kwargs) -> Team:
    view_model_map = {
        'id':   'id',
        'name': 'name',
    }

    model_kwargs = dict()
    for key in kwargs.keys():
        if key not in view_model_map:
            raise KeyError(f"{key} is invalid.")

        value = kwargs.get(key)
        if key == 'name':
            error_message = f"Team already exists with {key}={value}."
            if 'id' in kwargs:
                if _value_has_changed(key, **kwargs):
                    _validate_is_unique(key, value, error_message=error_message)
            else:
                _validate_is_unique(key, value, error_message=error_message)
            model_kwargs[key] = value
        else:    # key == 'id':
            model_kwargs[view_model_map[key]] = value

    return Team(**model_kwargs)


def _validate_is_unique(key, value, error_message=None):
    if Team.query.filter_by(**{key: value}).first() is not None:
        if not error_message:
            error_message = f"{key} must be unique."
        raise ValueError(error_message)


def _value_has_changed(key: str, **kwargs) -> bool:
    id = kwargs.get('id')
    team_repository = injector.get(TeamRepository)
    old_team = team_repository.get_team(id)
    return kwargs.get(key) != old_team.__dict__[key]
