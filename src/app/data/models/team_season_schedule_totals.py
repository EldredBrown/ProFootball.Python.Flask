from dataclasses import dataclass
from decimal import Decimal
from typing import Optional


@dataclass
class TeamSeasonScheduleTotals:
    """
    Represents a team's season schedule totals.
    """
    games: Optional[int] = None
    points_for: Optional[int] = None
    points_against: Optional[int] = None
    schedule_wins: Optional[int] = None
    schedule_losses: Optional[int] = None
    schedule_ties: Optional[int] = None
    schedule_winning_percentage: Optional[Decimal] = None
    schedule_games: Optional[int] = None
    schedule_points_for: Optional[int] = None
    schedule_points_against: Optional[int] = None
