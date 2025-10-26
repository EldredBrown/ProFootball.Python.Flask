from dataclasses import dataclass
from decimal import Decimal


@dataclass
class OffensiveRankingsTeamSeason:
    """
    Class to represent the association between one pro football team and one pro football season.
    """
    team_name: str
    wins: int
    losses: int
    ties: int
    offensive_average: Decimal
    offensive_factor: Decimal
    offensive_index: Decimal


@dataclass
class DefensiveRankingsTeamSeason:
    """
    Class to represent the association between one pro football team and one pro football season.
    """
    team_name: str
    wins: int
    losses: int
    ties: int
    defensive_average: Decimal
    defensive_factor: Decimal
    defensive_index: Decimal


@dataclass
class TotalRankingsTeamSeason:
    """
    Class to represent the association between one pro football team and one pro football season.
    """
    team_name: str
    wins: int
    losses: int
    ties: int
    offensive_average: Decimal
    offensive_factor: Decimal
    offensive_index: Decimal
    defensive_average: Decimal
    defensive_factor: Decimal
    defensive_index: Decimal
    final_expected_winning_percentage: Decimal
