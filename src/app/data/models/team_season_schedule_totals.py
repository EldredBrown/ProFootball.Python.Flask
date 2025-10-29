from dataclasses import dataclass
from decimal import Decimal

from app.services.utilities.auto_repr import auto_repr


@dataclass
class TeamSeasonScheduleTotals:
    """
    Represents a team's season schedule totals.
    """
    games: int = 0
    points_for: int = 0
    points_against: int = 0
    schedule_wins: int = 0
    schedule_losses: int = 0
    schedule_ties: int = 0
    schedule_winning_percentage: Decimal = Decimal('0')
    schedule_games: int = 0
    schedule_points_for: int = 0
    schedule_points_against: int = 0
