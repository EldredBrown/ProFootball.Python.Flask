from dataclasses import dataclass
from decimal import Decimal
from typing import Optional


@dataclass
class TeamSeasonScheduleAverages:
    """
    Represents a team's season schedule averages.
    """
    avg_points_for: Optional[Decimal] = None
    avg_points_against: Optional[Decimal] = None
    avg_schedule_points_for: Optional[Decimal] = None
    avg_schedule_points_against: Optional[Decimal] = None
