from decimal import Decimal

from app.services.utilities.auto_repr import auto_repr


@auto_repr
class TeamSeasonScheduleAverages:
    """
    Represents a team's seasons schedule averages.
    """

    def __init__(
            self,
            points_for: float = None,
            points_against: float = None,
            schedule_points_for: float = None,
            schedule_points_against: float = None
    ):
        """
        Initializes a new instance of the TeamSeasonScheduleAverages class.

        :param points_for:
        :param points_against:
        :param schedule_points_for:
        :param schedule_points_against:
        """
        self.points_for = points_for
        self.points_against = points_against
        self.schedule_points_for = schedule_points_for
        self.schedule_points_against = schedule_points_against

    def __str__(self):
        return format(self)

    def __format__(self, format_spec):
        return f"PF: {self.points_for}, PA: {self.points_against}, " \
               f"SPF: {self.schedule_points_for}, SPA: {self.schedule_points_against}"

    @property
    def points_for(self) -> float | None:
        """
        Gets the average points scored per game by a team.

        :return: The average points scored per game by a team.
        """
        return self._points_for

    @points_for.setter
    def points_for(self, value: float | None) -> None:
        """
        Sets the average points scored per game by a team.

        :param value: The value to which the average points scored per game by a team will be set.

        :return: None
        """
        if (value is not None) and (value < 0):
            raise ValueError("Please enter a non-negative value for points for.")

        self._points_for = value

    @property
    def points_against(self) -> float | None:
        """
        Gets the average points allowed per game by a team.

        :return: The average points allowed per game by a team.
        """
        return self._points_against

    @points_against.setter
    def points_against(self, value: float | None) -> None:
        """
        Sets the average points allowed per game by a team.

        :param value: The value to which the average points allowed per game by a team will be set.

        :return: None
        """
        if (value is not None) and (value < 0):
            raise ValueError("Please enter a non-negative value for points against.")

        self._points_against = value

    @property
    def schedule_points_for(self) -> float | None:
        """
        Gets the weighted average points scored per game by a team's opponents.

        :return: The average points scored per game by a team's opponents.
        """
        return self._schedule_points_for

    @schedule_points_for.setter
    def schedule_points_for(self, value: float | None) -> None:
        """
        Sets the average points scored per game by a team's opponents.

        :param value: The value to which the average points scored by a team's opponents will be set.

        :return: None
        """
        if (value is not None) and (value < 0):
            raise ValueError("Please enter a non-negative value for schedule points for.")

        self._schedule_points_for = value

    @property
    def schedule_points_against(self) -> float | None:
        """
        Gets the weighted average points allowed per game by a team's opponents.

        :return: The average points allowed per game by a team's opponents.
        """
        return self._schedule_points_against

    @schedule_points_against.setter
    def schedule_points_against(self, value: float | None) -> None:
        """
        Sets the average points allowed per game by a team's opponents.

        :param value: The value to which the average points allowed by a team's opponents will be set.

        :return: None
        """
        if (value is not None) and (value < 0):
            raise ValueError("Please enter a non-negative value for schedule points against.")

        self._schedule_points_against = value
