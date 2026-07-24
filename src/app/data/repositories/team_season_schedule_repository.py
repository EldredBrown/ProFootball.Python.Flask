from typing import List, Any

from app.data import sqla
from app.data.models.team_season_schedule_averages import TeamSeasonScheduleAverages
from app.data.models.team_season_schedule_profile import TeamSeasonOpponentProfile
from app.data.models.team_season_schedule_totals import TeamSeasonScheduleTotals


def get_team_season_schedule_profile(team_id: int, season_year: int) -> List[TeamSeasonOpponentProfile]:
    """
    Gets the TeamSeasonScheduleTotals in the data store with the specified team_name and season_year.

    :param team_id: The id of the team for which this TeamSeasonScheduleTotals will be fetched.
    :param season_year: The id of the seasons for which this TeamSeasonScheduleTotals will be fetched.

    :return: The fetched TeamSeasonScheduleTotals.
    """
    result = sqla.callproc(f"EXEC sp_GetTeamSeasonScheduleProfile '{team_id}', {season_year};")
    profile = result.all()

    opponent_records = []
    for row in profile:
        opp = TeamSeasonOpponentProfile(
            opponent=row[0],
            game_points_for=row[1],
            game_points_against=row[2],
            opponent_wins=row[3],
            opponent_losses=row[4],
            opponent_ties=row[5],
            opponent_winning_percentage=row[6],
            opponent_weighted_games=row[7],
            opponent_weighted_points_for=row[8],
            opponent_weighted_points_against=row[9]
        )
        opponent_records.append(opp)
    return opponent_records


def get_team_season_schedule_totals(team_id: int, season_year: int) -> TeamSeasonScheduleTotals:
    """
    Gets the TeamSeasonScheduleTotals in the data store with the specified team_name and season_year.

    :param team_id: The id of the team for which this TeamSeasonScheduleTotals will be fetched.
    :param season_year: The id of the seasons for which this TeamSeasonScheduleTotals will be fetched.

    :return: The fetched TeamSeasonScheduleTotals.
    """
    result = sqla.callproc(f"EXEC sp_GetTeamSeasonScheduleTotals '{team_id}', {season_year};")
    totals = result.first()

    if totals is None:
        return TeamSeasonScheduleTotals()

    return TeamSeasonScheduleTotals(
        games=totals[0],
        points_for=totals[1],
        points_against=totals[2],
        schedule_wins=totals[3],
        schedule_losses=totals[4],
        schedule_ties=totals[5],
        schedule_winning_percentage=totals[6],
        schedule_games=totals[7],
        schedule_points_for=totals[8],
        schedule_points_against=totals[9]
    )


def get_team_season_schedule_averages(team_id: int, season_year: int) -> TeamSeasonScheduleAverages:
    """
    Gets the TeamSeasonScheduleAverages in the data store with the specified team_name and season_year.

    :param team_id: The id of the team for which this TeamSeasonScheduleAverages will be fetched.
    :param season_year: The id of the seasons for which this TeamSeasonScheduleAverages will be fetched.

    :return: The fetched TeamSeasonScheduleAverages.
    """
    result = sqla.callproc(f"EXEC sp_GetTeamSeasonScheduleAverages '{team_id}', {season_year};")
    averages = result.first()

    if averages is None:
        return TeamSeasonScheduleAverages()

    return TeamSeasonScheduleAverages(
        avg_points_for=averages[0],
        avg_points_against=averages[1],
        avg_schedule_points_for=averages[2],
        avg_schedule_points_against=averages[3]
    )
