from app.data.models.season import Season
from app.data.models.game import Game
from app.data.models.league_season import LeagueSeason
from app.data.models.team_season import TeamSeason


def create_season(old_season: Season=None, **kwargs) -> Season:
    key = 'year'
    if key not in kwargs:
        raise ValueError(f"{str.capitalize(key)} is required.")

    error_message = f"League already exists with {key}={kwargs[key]}."
    if old_season:
        if _value_has_changed(key, old_season, **kwargs):
            _validate_is_unique(key, kwargs[key], error_message=error_message)
    else:
        _validate_is_unique(key, kwargs[key], error_message=error_message)

    return Season(**kwargs)


def _value_has_changed(key: str, season: Season, **kwargs) -> bool:
    return season.__dict__[key] != kwargs[key]


def _validate_is_unique(key, value, error_message=None):
    if Season.query.filter_by(**{key: value}).first() is not None:
        if not error_message:
            error_message = f"{key} must be unique."
        raise ValueError(error_message)
