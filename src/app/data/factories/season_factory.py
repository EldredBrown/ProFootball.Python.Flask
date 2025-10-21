from app.data.models.season import Season
from app.data.models.game import Game
from app.data.models.league_season import LeagueSeason
from app.data.models.team_season import TeamSeason


def create_season(old_season: Season=None, **kwargs) -> Season:
    if 'year' not in kwargs:
        raise ValueError("Year is required.")

    error_message = f"Season already exists with year={kwargs['year']}."
    if old_season:
        if old_season.year != kwargs['year']:
            _validate_is_unique('year', kwargs['year'], error_message=error_message)
    else:
        _validate_is_unique('year', kwargs['year'], error_message=error_message)

    return Season(**kwargs)


def _validate_is_unique(key, value, error_message=None):
    if Season.query.filter_by(**{key: value}).first() is not None:
        if not error_message:
            error_message = f"{key} must be unique."
        raise ValueError(error_message)
