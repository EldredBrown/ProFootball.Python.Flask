from typing import List

from sqlalchemy.exc import IntegrityError

from app.data.models.game import Game
from app.data.sqla import sqla
from app.data.factories import game_factory


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

    def get_games_by_season_year(self, season_year: int) -> List[Game]:
        """
        Gets all the games in the data store filtered by season_year.

        :param season_year: The season_year to filter.

        :return: A list of all fetched games.
        """
        return Game.query.filter_by(season_year=season_year).all()

    def get_games_by_season_year_and_week(self, season_year: int, week: int) -> List[Game]:
        """
        Gets all the games in the data store filtered by season_year.

        :param season_year: The season_year to filter.

        :return: A list of all fetched games.
        """
        return Game.query.filter_by(season_year=season_year, week=week).all()

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

    def add_game(self, **kwargs) -> Game:
        """
        Adds a game to the data store.

        :param **kwargs: A keyword args dictionary containing values for the game to add.

        :return: The added game.
        """
        game = game_factory.create_game(**kwargs)
        sqla.session.add(game)
        try:
            sqla.session.commit()
        except IntegrityError:
            sqla.session.rollback()
            raise
        return game

    def add_games(self, game_args: tuple) -> List[Game]:
        """
        Adds a collection of game_args dictionaries to the data store.

        :param game_args: The tuple of game keyword args dictionaries to add.

        :return: The added games.
        """
        games = []
        try:
            for kwargs in game_args:
                game = game_factory.create_game(kwargs)
                games.append(game)
                sqla.session.add(game)
            sqla.session.commit()
        except IntegrityError:
            sqla.session.rollback()
            raise
        return games

    def update_game(self, **kwargs) -> Game | None:
        """
        Updates a game in the data store.

        :param game: The game to update.

        :return: The updated game.
        """
        if 'id' not in kwargs:
            raise ValueError("ID must be provided for existing Game.")

        if not self.game_exists(kwargs['id']):
            return Game(**kwargs)

        old_game = self.get_game(kwargs['id'])
        new_game = game_factory.create_game(**kwargs)

        old_game.season_year = new_game.season_year
        old_game.week = new_game.week
        old_game.guest_name = new_game.guest_name
        old_game.guest_score = new_game.guest_score
        old_game.host_name = new_game.host_name
        old_game.host_score = new_game.host_score
        old_game.is_playoff = new_game.is_playoff
        old_game.notes = new_game.notes

        sqla.session.add(old_game)
        try:
            sqla.session.commit()
        except IntegrityError:
            sqla.session.rollback()
            raise

        return new_game

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
        return self.get_game(id) is not None
