from app.services.utilities.auto_repr import auto_repr


@auto_repr
class LeagueSeasonTotals:
    """
    Class to represent the total games and points of a pro football conference's seasons.
    """

    def __init__(self, total_games: int | None = 0, total_points: int | None = 0) -> None:
        """
        Initializes a new instance of the LeagueSeasonTotals class.

        :param total_games: The new LeagueSeasonTotals object's total games played.
        :param total_points: The new LeagueSeasonTotals object's total points scored.
        """
        self.total_games = total_games
        self.total_points = total_points

    def __str__(self):
        return format(self)

    def __format__(self, format_spec):
        return f"Total Games: {self.total_games}, " \
               f"Total Points: {self.total_points}"

    @property
    def total_games(self):
        return self._total_games

    @total_games.setter
    def total_games(self, value):
        if (value is not None) and (value < 0):
            raise ValueError("Please enter a non-negative value for total games.")

        self._total_games = value

    @property
    def total_points(self):
        return self._total_points

    @total_points.setter
    def total_points(self, value):
        if (value is not None) and (value < 0):
            raise ValueError("Please enter a non-negative value for total points.")

        self._total_points = value
