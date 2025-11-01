from app.data.models.season import Season
from app.data.models.division import Division
from app.data.models.game import Game
from app.data.models.league_season import LeagueSeason
from app.data.models.team_season import TeamSeason


def create_division(old_division: Division=None, **kwargs) -> Division:
    key = 'name'
    if key not in kwargs:
        raise ValueError(f"{key} is required.")

    error_message = f"Division already exists with {key}={kwargs[key]}."
    if old_division:
        if _value_has_changed(key, old_division, **kwargs):
            _validate_is_unique(key, kwargs[key], error_message=error_message)
    else:
        _validate_is_unique(key, kwargs[key], error_message=error_message)

    return Division(**kwargs)


def _value_has_changed(key: str, division: Division, **kwargs) -> bool:
    return kwargs[key] != division.__dict__[key]


def _validate_is_unique(key, value, error_message=None):
    if Division.query.filter_by(**{key: value}).first() is not None:
        if not error_message:
            error_message = f"{key} must be unique."
        raise ValueError(error_message)
