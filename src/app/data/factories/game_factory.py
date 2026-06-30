from app.data.models.game import Game


def create_game(**kwargs) -> Game:
    return Game(**kwargs)
