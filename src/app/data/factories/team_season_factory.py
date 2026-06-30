from app import injector
from app.data.models.team_season import TeamSeason
from app.data.repositories.conference_repository import ConferenceRepository
from app.data.repositories.division_repository import DivisionRepository
from app.data.repositories.league_repository import LeagueRepository
from app.data.repositories.team_repository import TeamRepository
from app.data.repositories.team_season_repository import TeamSeasonRepository


def create_team_season(**kwargs) -> TeamSeason:
    view_model_map = {
        'id':               'id',
        'team_name':        'team_id',
        'season_year':      'season_id',
        'league_name':      'league_id',
        'conference_name':  'conference_id',
        'division_name':    'division_id',
    }

    model_kwargs = dict()
    for key in kwargs.keys():
        if key not in view_model_map:
            raise KeyError(f"{key} is invalid.")

        value = kwargs.get(key)
        if key == 'team_name':
            team_repository = injector.get(TeamRepository)
            team = team_repository.get_team_by_name(value)
            model_kwargs[view_model_map[key]] = team.id if team is not None else -1
        elif key == 'league_name':
            league_repository = injector.get(LeagueRepository)
            league = league_repository.get_league_by_short_name(value)
            model_kwargs[view_model_map[key]] = league.id if league is not None else -1
        elif key == 'conference_name':
            conference_repository = injector.get(ConferenceRepository)
            conference = conference_repository.get_conference_by_short_name(value)
            model_kwargs[view_model_map[key]] = conference.id if conference is not None else None
        elif key == 'division_name':
            division_repository = injector.get(DivisionRepository)
            division = division_repository.get_division_by_name(value)
            model_kwargs[view_model_map[key]] = division.id if division is not None else None
        else:
            model_kwargs[view_model_map[key]] = value

    team_id = int(model_kwargs.get('team_id'))
    season_id = int(model_kwargs.get('season_id'))
    error_message = f"TeamSeason already exists with team_id={team_id} and season_id={season_id}."
    if 'id' in model_kwargs:
        if _values_have_changed(**model_kwargs):
            _validate_is_unique(team_id, season_id, error_message=error_message)
    else:
        _validate_is_unique(team_id, season_id, error_message=error_message)

    return TeamSeason(**model_kwargs)


def _validate_is_unique(team_id: int, season_id: int, error_message=None) -> None:
    team_season_repository = injector.get(TeamSeasonRepository)
    if team_season_repository.get_team_season_by_team_and_season(team_id=team_id, season_id=season_id) is not None:
        if not error_message:
            error_message = "team_id and season_id together must be unique."
        raise ValueError(error_message)


def _values_have_changed(**kwargs) -> bool:
    id = kwargs.get('id')
    team_season_repository = injector.get(TeamSeasonRepository)
    old_team_season = team_season_repository.get_team_season(id)
    return (kwargs.get('team_id') != old_team_season.__dict__['team_id'] or
            kwargs.get('season_id') != old_team_season.__dict__['season_id'] or
            kwargs.get('league_id') != old_team_season.__dict__['league_id'] or
            kwargs.get('conference_id') != old_team_season.__dict__['conference_id'] or
            kwargs.get('division_id') != old_team_season.__dict__['division_id'])
