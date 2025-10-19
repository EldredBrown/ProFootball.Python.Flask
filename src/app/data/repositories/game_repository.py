from typing import List

from sqlalchemy import exists

from app.data.models.game import Game
from app.data.sqla import sqla


class GameRepository:
    """
    Provides CRUD access to an external data store.
    """

    def __init__(self) -> None:
        """
        Initializes a new instance of the GameRepository class.
        """
        pass

    def get_games(self) -> List[Game]:
        """
        Gets all the games in the data store.

        :return: A list of all fetched games.
        """
        return Game.query.all()

    def get_game(self, id: int) -> Game | None:
        """
        Gets the game in the data store with the specified id.

        :param id: The id of the game to fetch.

        :return: The fetched game.
        """
        games = self.get_games()
        if len(games) == 0:
            return None
        return Game.query.get(id)

    def add_game(self, game: Game) -> Game:
        """
        Adds a game to the data store.

        :param game: The game to add.

        :return: The added game.
        """
        sqla.session.add(game)
        sqla.session.commit()
        return game

    def add_games(self, games: tuple) -> tuple:
        """
        Adds a collection of games to the data store.

        :param games: The games to add.

        :return: The added games.
        """
        for game in games:
            sqla.session.add(game)
        sqla.session.commit()
        return games

    def update_game(self, game: Game) -> Game | None:
        """
        Updates a game in the data store.

        :param game: The game to update.

        :return: The updated game.
        """
        if not self.game_exists(game.id):
            return game

        game_to_update = self.get_game(game.id)
        game_to_update.season_year = game.season_year
        game_to_update.week = game.week
        game_to_update.guest_name = game.guest_name
        game_to_update.guest_score = game.guest_score
        game_to_update.host_name = game.host_name
        game_to_update.host_score = game.host_score
        sqla.session.add(game_to_update)
        sqla.session.commit()
        return game

    def delete_game(self, id: int) -> Game | None:
        """
        Deletes a game from the data store.

        :param id: The id of the game to delete.

        :return: The deleted game.
        """
        if not self.game_exists(id):
            return None

        game = self.get_game(id)
        sqla.session.delete(game)
        sqla.session.commit()
        return game

    def game_exists(self, id: int) -> bool:
        """
        Checks to verify whether a specific game exists in the data store.

        :param id: The id of the game to verify.

        :return: True if the game with the specified id exists in the data store; otherwise false.
        """
        return sqla.session.query(exists().where(Game.id == id)).scalar()
