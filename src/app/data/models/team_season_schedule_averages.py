from dataclasses import dataclass
from decimal import Decimal


@dataclass
class TeamSeasonScheduleAverages:
    """
    Represents a team's season schedule averages.
    """
    points_for: Decimal | None = None
    points_against: Decimal | None = None
    schedule_points_for: Decimal | None = None
    schedule_points_against: Decimal | None = None
