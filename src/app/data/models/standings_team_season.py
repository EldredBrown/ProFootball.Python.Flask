from dataclasses import dataclass
from decimal import Decimal


@dataclass
class StandingsTeamSeason:
    """
    Class to represent the association between one pro football team and one pro football season.
    """
    team_name: str
    wins: int
    losses: int
    ties: int
    winning_percentage: Decimal
    points_for: int
    points_against: int
    avg_points_for: Decimal
    avg_points_against: Decimal
    expected_wins: Decimal
    expected_losses: Decimal
