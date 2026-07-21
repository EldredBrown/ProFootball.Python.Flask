from app import injector
from app.data.models.league_season import LeagueSeason
from app.data.repositories.association_repository import AssociationRepository
from app.data.repositories.league_season_repository import LeagueSeasonRepository


def create_league_season(**kwargs) -> LeagueSeason:
    view_model_map = {
        'id':                       'id',
        'league_name':              'league_id',
        'season_year':              'season_year',
        'num_of_weeks_scheduled':   'num_of_weeks_scheduled',
        'num_of_weeks_completed':   'num_of_weeks_completed',
    }

    model_kwargs = dict()
    for key in kwargs.keys():
        if key not in view_model_map:
            raise KeyError(f"{key} is invalid.")

        value = kwargs.get(key)
        if key == 'league_name':
            association_repository = injector.get(AssociationRepository)
            league = association_repository.get_association_by_short_name(value)
            model_kwargs[view_model_map[key]] = -1 if league is None else league.id
        else:
            model_kwargs[view_model_map[key]] = value

    return LeagueSeason(**model_kwargs)
