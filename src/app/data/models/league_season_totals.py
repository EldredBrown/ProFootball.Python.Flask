from dataclasses import dataclass
from decimal import Decimal


@dataclass
class LeagueSeasonTotals:
    """
    Class to represent the total games and points of a pro football league season.
    """
    total_games: int | None = 0
    total_points: int | None = 0
    average_points: Decimal | None = Decimal('0')
    week_count: int | None = 0
