from dataclasses import dataclass
from decimal import Decimal


@dataclass
class LeagueSeasonTotals:
    """
    Class to represent the total games and points of a pro football league season.
    """
    total_games: int
    total_points: int
    average_points: Decimal
    week_count: int
