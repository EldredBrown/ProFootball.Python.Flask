from decimal import Decimal

from app.services.utilities.auto_repr import auto_repr


@auto_repr
class TeamSeasonScheduleTotals:
    """
    Represents a team's seasons schedule totals.
    """

    def __init__(
            self,
            games: int = None,
            points_for: int = None,
            points_against: int = None,
            schedule_wins: int = None,
            schedule_losses: int = None,
            schedule_ties: int = None,
            schedule_winning_percentage: float = None,
            schedule_games: int = None,
            schedule_points_for: int = None,
            schedule_points_against: int = None
    ):
        """
        Initializes a new instance of the TeamSeasonScheduleTotals class.

        :param games:
        :param points_for:
        :param points_against:
        :param schedule_wins:
        :param schedule_losses:
        :param schedule_ties:
        :param schedule_winning_percentage:
        :param schedule_games:
        :param schedule_points_for:
        :param schedule_points_against:
        """
        self.games = games
        self.points_for = points_for
        self.points_against = points_against
        self.schedule_wins = schedule_wins
        self.schedule_losses = schedule_losses
        self.schedule_ties = schedule_ties
        self.schedule_winning_percentage = schedule_winning_percentage
        self.schedule_games = schedule_games
        self.schedule_points_for = schedule_points_for
        self.schedule_points_against = schedule_points_against

    def __str__(self):
        return format(self)

    def __format__(self, format_spec):
        return f"G: {self.games}, PF: {self.points_for}, PA: {self.points_against}, " \
               f"SW: {self.schedule_wins}, SL: {self.schedule_losses}, ST: {self.schedule_ties}, " \
               f"SWP: {self.schedule_winning_percentage}, SG: {self.schedule_games}, " \
               f"SPF: {self.schedule_points_for}, SPA: {self.schedule_points_against}"

    @property
    def games(self) -> int | None:
        """
        Gets the total games played by a team.

        :return: The total games played by a team.
        """
        return self._games

    @games.setter
    def games(self, value: int | None) -> None:
        """
        Sets the total games played by a team.

        :param value: The value to which a team's total games will be set.

        :return: None
        """
        if (value is not None) and (value < 0):
            raise ValueError("Please enter a non-negative value for games.")

        self._games = value

    @property
    def points_for(self) -> int | None:
        """
        Gets the total points scored by a team.

        :return: The total points scored by a team.
        """
        return self._points_for

    @points_for.setter
    def points_for(self, value: int | None) -> None:
        """
        Sets the total points scored by a team.

        :param value: The value to which a team's total points scored will be set.

        :return: None
        """
        if (value is not None) and (value < 0):
            raise ValueError("Please enter a non-negative value for points for.")

        self._points_for = value

    @property
    def points_against(self) -> int | None:
        """
        Gets the total points allowed by a team.

        :return: The total points allowed by a team.
        """
        return self._points_against

    @points_against.setter
    def points_against(self, value: int | None) -> None:
        """
        Sets the total points allowed by a team.

        :param value: The value to which a team's total points allowed will be set.

        :return: None
        """
        if (value is not None) and (value < 0):
            raise ValueError("Please enter a non-negative value for points against.")

        self._points_against = value

    @property
    def schedule_wins(self) -> int | None:
        """
        Gets the total wins by a team's opponents.

        :return: The total wins by a team's opponents.
        """
        return self._schedule_wins

    @schedule_wins.setter
    def schedule_wins(self, value: int | None) -> None:
        """
        Sets the total wins by a team's opponents.

        :param value: The value to which the total wins by a team's opponents will be set.

        :return: None
        """
        if (value is not None) and (value < 0):
            raise ValueError("Please enter a non-negative value for schedule wins.")

        self._schedule_wins = value

    @property
    def schedule_losses(self) -> int | None:
        """
        Gets the total losses by a team's opponents.

        :return: The total losses by a team's opponents.
        """
        return self._schedule_losses

    @schedule_losses.setter
    def schedule_losses(self, value: int | None) -> None:
        """
        Sets the total losses by a team's opponents.

        :param value: The value to which the total losses by a team's opponents will be set.

        :return: None
        """
        if (value is not None) and (value < 0):
            raise ValueError("Please enter a non-negative value for schedule losses.")

        self._schedule_losses = value

    @property
    def schedule_ties(self) -> int | None:
        """
        Gets the total ties by a team's opponents.

        :return: The total ties by a team's opponents.
        """
        return self._schedule_ties

    @schedule_ties.setter
    def schedule_ties(self, value: int | None) -> None:
        """
        Sets the total ties by a team's opponents.

        :param value: The value to which the total ties by a team's opponents will be set.

        :return: None
        """
        if (value is not None) and (value < 0):
            raise ValueError("Please enter a non-negative value for schedule ties.")

        self._schedule_ties = value

    @property
    def schedule_winning_percentage(self) -> Decimal | None:
        """
        Gets the winning percentage by all opponents on a team's schedule.

        :return: The winning percentage by all opponents on a team's schedule.
        """
        return self._schedule_winning_percentage

    @schedule_winning_percentage.setter
    def schedule_winning_percentage(self, value: Decimal | None) -> None:
        """
        Sets the winning percentage by all opponents on a team's schedule.

        :param value: The value to which the winning percentage by all opponents on a team's schedule will be set.

        :return: None
        """
        if (value is not None) and (value < Decimal('0')):
            raise ValueError("Please enter a non-negative value for schedule winning percentage.")

        self._schedule_winning_percentage = value

    @property
    def schedule_games(self) -> Decimal | None:
        """
        Gets the weighted total of games played by a team's opponents.

        :return: The weighted total of games played by a team's opponents.
        """
        return self._schedule_games

    @schedule_games.setter
    def schedule_games(self, value: Decimal | None) -> None:
        """
        Sets the weighted total of games played by a team's opponents.

        :param value: The value to which the weighted total of games played by a team's opponents will be set.

        :return: None
        """
        if (value is not None) and (value < Decimal('0')):
            raise ValueError("Please enter a non-negative value for schedule games.")

        self._schedule_games = value

    @property
    def schedule_points_for(self) -> int | None:
        """
        Gets the total points scored by a team's opponents.

        :return: The total points scored by a team's opponents.
        """
        return self._schedule_points_for

    @schedule_points_for.setter
    def schedule_points_for(self, value: int | None) -> None:
        """
        Sets the total points scored by a team's opponents.

        :param value: The value to which the total points scored by a team's opponents will be set.

        :return: None
        """
        if (value is not None) and (value < 0):
            raise ValueError("Please enter a non-negative value for schedule points for.")

        self._schedule_points_for = value

    @property
    def schedule_points_against(self) -> int | None:
        """
        Gets the total points allowed by a team's opponents.

        :return: The total points allowed by a team's opponents.
        """
        return self._schedule_points_against

    @schedule_points_against.setter
    def schedule_points_against(self, value: int | None) -> None:
        """
        Sets the total points allowed by a team's opponents.

        :param value: The value to which the total points allowed by a team's opponents will be set.

        :return: None
        """
        if (value is not None) and (value < 0):
            raise ValueError("Please enter a non-negative value for schedule points against.")

        self._schedule_points_against = value
