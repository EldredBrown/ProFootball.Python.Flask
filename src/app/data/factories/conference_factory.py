from app.data.models.season import Season
from app.data.models.conference import Conference
from app.data.models.game import Game
from app.data.models.league_season import LeagueSeason
from app.data.models.team_season import TeamSeason


def create_conference(old_conference: Conference=None, **kwargs) -> Conference:
    for key in ['short_name', 'long_name']:
        if key not in kwargs:
            raise ValueError(f"{key} is required.")

        error_message = f"Conference already exists with {key}={kwargs[key]}."
        if old_conference:
            if kwargs[key] != old_conference.__dict__[key]:
                _validate_is_unique(key, kwargs[key], error_message=error_message)
        else:
            _validate_is_unique(key, kwargs[key], error_message=error_message)

    return Conference(**kwargs)


def _validate_is_unique(key, value, error_message=None):
    if Conference.query.filter_by(**{key: value}).first() is not None:
        if not error_message:
            error_message = f"{key} must be unique."
        raise ValueError(error_message)
