from dataclasses import dataclass
from decimal import Decimal


@dataclass
class TeamSeasonScheduleProfileRecord:
    """
    Represents a team's season schedule totals.
    """
    opponent: str | None = None
    game_points_for: int | None = None
    game_points_against: int | None = None
    opponent_wins: int | None = None
    opponent_losses: int | None = None
    opponent_ties: int | None = None
    opponent_winning_percentage: Decimal | None = None
    opponent_weighted_games: int | None = None
    opponent_weighted_points_for: int | None = None
    opponent_weighted_points_against: int | None = None
