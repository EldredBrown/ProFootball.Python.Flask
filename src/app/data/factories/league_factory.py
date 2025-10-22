from app.data.models.season import Season
from app.data.models.league import League
from app.data.models.game import Game
from app.data.models.league_season import LeagueSeason
from app.data.models.team_season import TeamSeason


def create_league(old_league: League=None, **kwargs) -> League:
    for key in ['short_name', 'long_name']:
        if key not in kwargs:
            raise ValueError(f"{key} is required.")

        error_message = f"League already exists with {key}={kwargs[key]}."
        if old_league:
            if old_league.__dict__[key] != kwargs[key]:
                _validate_is_unique(key, kwargs[key], error_message=error_message)
        else:
            _validate_is_unique(key, kwargs[key], error_message=error_message)

    return League(**kwargs)


def _validate_is_unique(key, value, error_message=None):
    if League.query.filter_by(**{key: value}).first() is not None:
        if not error_message:
            error_message = f"{key} must be unique."
        raise ValueError(error_message)
