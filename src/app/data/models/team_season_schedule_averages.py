from dataclasses import dataclass
from decimal import Decimal
from typing import Optional


@dataclass
class TeamSeasonScheduleAverages:
    """
    Represents a team's season schedule averages.
    """
    points_for: Optional[Decimal] = None
    points_against: Optional[Decimal] = None
    schedule_points_for: Optional[Decimal] = None
    schedule_points_against: Optional[Decimal] = None
