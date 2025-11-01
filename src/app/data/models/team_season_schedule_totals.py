from dataclasses import dataclass
from decimal import Decimal
from typing import Optional


@dataclass
class TeamSeasonScheduleTotals:
    """
    Represents a team's season schedule totals.
    """
    games: Optional[int]
    points_for: Optional[int]
    points_against: Optional[int]
    schedule_wins: Optional[int]
    schedule_losses: Optional[int]
    schedule_ties: Optional[int]
    schedule_winning_percentage: Optional[Decimal]
    schedule_games: Optional[int]
    schedule_points_for: Optional[int]
    schedule_points_against: Optional[int]
