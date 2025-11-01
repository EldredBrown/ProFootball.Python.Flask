from dataclasses import dataclass
from decimal import Decimal
from typing import Optional


@dataclass
class TeamSeasonScheduleProfileRecord:
    """
    Represents a team's season schedule totals.
    """
    opponent: Optional[str]
    game_points_for: Optional[int]
    game_points_against: Optional[int]
    opponent_wins: Optional[int]
    opponent_losses: Optional[int]
    opponent_ties: Optional[int]
    opponent_winning_percentage: Optional[Decimal]
    opponent_weighted_games: Optional[int]
    opponent_weighted_points_for: Optional[int]
    opponent_weighted_points_against: Optional[int]
