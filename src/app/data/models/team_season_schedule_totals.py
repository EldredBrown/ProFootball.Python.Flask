from dataclasses import dataclass
from decimal import Decimal


@dataclass
class TeamSeasonScheduleTotals:
    """
    Represents a team's season schedule totals.
    """
    games: int | None = None
    points_for: int | None = None
    points_against: int | None = None
    schedule_wins: int | None = None
    schedule_losses: int | None = None
    schedule_ties: int | None = None
    schedule_winning_percentage: Decimal | None = None
    schedule_games: int | None = None
    schedule_points_for: int | None = None
    schedule_points_against: int | None = None
