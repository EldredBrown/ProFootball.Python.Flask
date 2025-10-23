from app.data.models.season import Season
from app.data.models.game import Game
from app.data.models.league_season import LeagueSeason
from app.data.models.team_season import TeamSeason


def create_game(**kwargs) -> Game:
    return Game(**kwargs)
