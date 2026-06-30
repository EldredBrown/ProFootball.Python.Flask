from typing import List, Optional

from sqlalchemy.orm import joinedload

from app.data.models.game import Game
from app.data.sqla import sqla, try_commit


class GameRepository:
    """
    Provides CRUD access to an external data store.
    """

    def get_games(self) -> List[Game]:
        """
        Gets all the games in the data store.

        :return: A list of all fetched games.
        """
        games = self._get_games_with_navigation_properties()
        return games.all()

    def get_games_by_season(self, season_id: Optional[int]) -> List[Game]:
        """
        Gets all the games in the data store filtered by season_year.

        :param season_id: The season_year to filter.

        :return: A list of all fetched games.
        """
        games = self._get_games_with_navigation_properties()
        if season_id is None:
            return []
        return games.filter_by(season_id=season_id).all()

    def get_games_by_season_and_week(self, season_id: Optional[int], week: Optional[int]) -> List[Game]:
        """
        Gets all the games in the data store filtered by season_year.

        :param season_id: The season_year to filter.

        :return: A list of all fetched games.
        """
        games = self._get_games_with_navigation_properties()
        if season_id is None or week is None:
            return []
        return games.filter_by(season_id=season_id, week=week).all()

    def get_game(self, id: int) -> Optional[Game]:
        """
        Gets the game in the data store with the specified id.

        :param id: The id of the game to fetch.

        :return: The fetched game.
        """
        games = self._get_games_with_navigation_properties()
        if len(games.all()) == 0:
            return None
        return games.get(id)

    def get_game_by_season_week_guest_and_host(self, season_id: int, week: int, guest_name: str, host_name: str) -> Optional[Game]:
        """
        Gets the game in the data store with the specified id.

        :param id: The id of the game to fetch.

        :return: The fetched game.
        """
        games = self._get_games_with_navigation_properties()
        if len(games.all()) == 0:
            return None
        return games.filter_by(season_id=season_id, week=week, guest_name=guest_name, host_name=host_name).first()

    def add_game(self, game: Game) -> Game:
        """
        Adds a game to the data store.

        :param **kwargs: A keyword args dictionary containing values for the game to add.

        :return: The added game.
        """
        sqla.session.add(game)
        try_commit()
        return game

    def add_games(self, games: tuple) -> tuple:
        """
        Adds a collection of game_args dictionaries to the data store.

        :param game_args: The tuple of game keyword args dictionaries to add.

        :return: The added games.
        """
        for game in games:
            sqla.session.add(game)
        try_commit()
        return games

    def update_game(self, game: Game) -> Optional[Game]:
        """
        Updates a game in the data store.

        :param game: The game to update.

        :return: The updated game.
        """
        if not self.game_exists(game.id):
            return game
        game_in_db = self._set_values_of_game_in_db(game)
        sqla.session.add(game_in_db)
        try_commit()
        return game

    def delete_game(self, id: int) -> Optional[Game]:
        """
        Deletes a game from the data store.

        :param id: The id of the game to delete.

        :return: The deleted game.
        """
        if not self.game_exists(id):
            return None
        game = self.get_game(id)
        sqla.session.delete(game)
        try_commit()
        return game

    def game_exists(self, id: int) -> bool:
        """
        Checks to verify whether a specific game exists in the data store.

        :param id: The id of the game to verify.

        :return: True if the game with the specified id exists in the data store; otherwise false.
        """
        return self.get_game(id) is not None

    def get_max_week_by_season(self, season_id: int) -> int | None:
        weeks = [game.week for game in self.get_games_by_season(season_id)]
        if weeks:
            return max(weeks)

    def _get_games_with_navigation_properties(self):
        return Game.query.options(joinedload(Game.season))

    def _set_values_of_game_in_db(self, game: Game) -> Game | None:
        game_in_db = self.get_game(game.id)
        game_in_db.season_id = game.season_id
        game_in_db.week = game.week
        game_in_db.guest_name = game.guest_name
        game_in_db.guest_score = game.guest_score
        game_in_db.host_name = game.host_name
        game_in_db.host_score = game.host_score
        game_in_db.is_playoff = game.is_playoff
        game_in_db.notes = game.notes
        return game_in_db
