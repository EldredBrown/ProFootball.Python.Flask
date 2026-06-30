from app import injector
from app.data.models.league_season import LeagueSeason
from app.data.repositories.league_repository import LeagueRepository
from app.data.repositories.league_season_repository import LeagueSeasonRepository


def create_league_season(**kwargs) -> LeagueSeason:
    view_model_map = {
        'id':           'id',
        'league_name':  'league_id',
        'season_year':  'season_id',
    }

    model_kwargs = dict()
    for key in kwargs.keys():
        if key not in view_model_map:
            raise KeyError(f"{key} is invalid.")

        value = kwargs.get(key)
        if key == 'league_name':
            league_repository = injector.get(LeagueRepository)
            league = league_repository.get_league_by_short_name(value)
            model_kwargs[view_model_map[key]] = league.id
        else:
            model_kwargs[view_model_map[key]] = value

    league_id = int(model_kwargs.get('league_id'))
    season_id = int(model_kwargs.get('season_id'))
    error_message = f"LeagueSeason already exists with league_id={league_id} and season_id={season_id}."
    if 'id' in model_kwargs:
        if _values_have_changed(**model_kwargs):
            _validate_is_unique(league_id, season_id, error_message=error_message)
    else:
        _validate_is_unique(league_id, season_id, error_message=error_message)

    return LeagueSeason(**model_kwargs)


def _validate_is_unique(league_id: int, season_id: int, error_message=None) -> None:
    league_season_repository = injector.get(LeagueSeasonRepository)
    if league_season_repository.get_league_season_by_league_and_season(league_id=league_id, season_id=season_id) is not None:
        if not error_message:
            error_message = "league_id and season_id together must be unique."
        raise ValueError(error_message)


def _values_have_changed(**kwargs) -> bool:
    id = kwargs.get('id')
    league_season_repository = injector.get(LeagueSeasonRepository)
    old_league_season = league_season_repository.get_league_season(id)
    return (kwargs.get('league_id') != old_league_season.__dict__['league_id'] or
            kwargs.get('season_id') != old_league_season.__dict__['season_id'])
