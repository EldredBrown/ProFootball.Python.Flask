from app import injector
from app.data.models.team_season import TeamSeason
from app.data.repositories.association_repository import AssociationRepository
from app.data.repositories.team_repository import TeamRepository


def create_team_season(**kwargs) -> TeamSeason:
    view_model_map = {
        'id':               'id',
        'team_name':        'team_id',
        'season_year':      'season_year',
        'league_name':      'league_id',
        'conference_name':  'conference_id',
        'division_name':    'division_id',
    }

    association_repository = injector.get(AssociationRepository)

    model_kwargs = dict()
    for key in kwargs.keys():
        if key not in view_model_map:
            raise KeyError(f"{key} is invalid.")

        value = kwargs.get(key)
        if key == 'team_name':
            team_repository = injector.get(TeamRepository)
            team = team_repository.get_team_by_name(value)
            model_kwargs['team_id'] = -1 if team is None else team.id
        elif key == 'league_name':
            league = association_repository.get_association_by_short_name(value)
            model_kwargs['league_id'] = -1 if league is None else league.id
        elif key == 'conference_name':
            conference = association_repository.get_association_by_short_name(value)
            model_kwargs['conference_id'] = None if conference is None else conference.id
        elif key == 'division_name':
            division = association_repository.get_association_by_short_name(value)
            model_kwargs['division_id'] = None if division is None else division.id
        else:
            model_kwargs[view_model_map[key]] = value

    return TeamSeason(**model_kwargs)
