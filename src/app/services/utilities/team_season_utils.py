from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

EXPONENT = Decimal('2.37')

@dataclass
class TeamSeasonRankingsData:
    average: Optional[Decimal]
    factor: Optional[Decimal]
    index: Optional[Decimal]


def calculate_expected_winning_percentage(points_for: Decimal, points_against: Decimal) -> Optional[Decimal]:
    if points_for < 0 or points_against < 0:
        raise ValueError(f"Points values must be non-negative; got {points_for},  {points_against}")
    o = pow(points_for, EXPONENT)
    d = pow(points_against, EXPONENT)
    return divide(o, o + d)


def divide(numerator: int | Decimal, denominator: int | Decimal) -> Optional[Decimal]:
    if denominator == 0:
        return None

    return Decimal(numerator) / Decimal(denominator)


def update_rankings(
        points: int, games: int, team_season_schedule_average_points: Decimal, league_season_average_points: Decimal
) -> TeamSeasonRankingsData:
    if games == 0:
        return TeamSeasonRankingsData(average=None, factor=None, index=None)

    average = divide(points, games)
    factor = divide(average, team_season_schedule_average_points)

    if factor is None:
        index = None
    else:
        index = divide(average + factor * league_season_average_points, 2)

    return TeamSeasonRankingsData(average=average, factor=factor, index=index)
