from dataclasses import dataclass
from decimal import Decimal
from typing import Optional


@dataclass
class LeagueSeasonTotals:
    """
    Class to represent the total games and points of a pro football league season.
    """
    total_games: Optional[int] = None
    total_points: Optional[int] = None
    average_points: Optional[Decimal] = None
    week_count: Optional[int] = None
