from dataclasses import dataclass
from decimal import Decimal
from typing import Optional


@dataclass
class TeamSeasonScheduleProfileRecord:
    """
    Represents a team's season schedule totals.
    """
    opponent: Optional[str] = None
    game_points_for: Optional[int] = None
    game_points_against: Optional[int] = None
    opponent_wins: Optional[int] = None
    opponent_losses: Optional[int] = None
    opponent_ties: Optional[int] = None
    opponent_winning_percentage: Optional[Decimal] = None
    opponent_weighted_games: Optional[int] = None
    opponent_weighted_points_for: Optional[int] = None
    opponent_weighted_points_against: Optional[int] = None
