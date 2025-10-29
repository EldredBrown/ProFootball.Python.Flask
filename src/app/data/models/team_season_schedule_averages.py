from dataclasses import dataclass
from decimal import Decimal

from app.services.utilities.auto_repr import auto_repr


@dataclass
class TeamSeasonScheduleAverages:
    """
    Represents a team's season schedule averages.
    """
    points_for: Decimal = Decimal('0')
    points_against: Decimal = Decimal('0')
    schedule_points_for: Decimal = Decimal('0')
    schedule_points_against: Decimal = Decimal('0')
