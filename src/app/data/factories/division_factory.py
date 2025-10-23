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
        if kwargs[key] != old_division.__dict__[key]:
            _validate_is_unique(key, kwargs[key], error_message=error_message)
    else:
        _validate_is_unique(key, kwargs[key], error_message=error_message)

    return Division(**kwargs)


def _validate_is_unique(key, value, error_message=None):
    if Division.query.filter_by(**{key: value}).first() is not None:
        if not error_message:
            error_message = f"{key} must be unique."
        raise ValueError(error_message)
