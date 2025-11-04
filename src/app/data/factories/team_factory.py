from app.data.models.season import Season
from app.data.models.team import Team
from app.data.models.game import Game
from app.data.models.league_season import LeagueSeason
from app.data.models.team_season import TeamSeason


def create_team(old_team: Team=None, **kwargs) -> Team:
    key = 'name'
    _validate_key_is_in_kwargs(key, **kwargs)

    error_message = f"Team already exists with {key}={kwargs[key]}."
    if old_team:
        if _value_has_changed(key, old_team, **kwargs):
            _validate_is_unique(key, kwargs[key], error_message=error_message)
    else:
        _validate_is_unique(key, kwargs[key], error_message=error_message)

    return Team(**kwargs)


def _validate_key_is_in_kwargs(key, **kwargs):
    if key not in kwargs:
        raise ValueError(f"{key} is required.")


def _value_has_changed(key: str, team: Team, **kwargs) -> bool:
    return kwargs[key] != team.__dict__[key]


def _validate_is_unique(key, value, error_message=None):
    if Team.query.filter_by(**{key: value}).first() is not None:
        if not error_message:
            error_message = f"{key} must be unique."
        raise ValueError(error_message)
