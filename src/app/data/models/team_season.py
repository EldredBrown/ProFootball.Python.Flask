from decimal import Decimal

from app.data.sqla import sqla
from app.services.utilities import team_season_utils


class TeamSeason(sqla.Model):
    """
    Class to represent the association between one pro football team and one pro football season.
    """
    __tablename__ = 'TeamSeason'

    id = sqla.Column(sqla.Integer, primary_key=True, autoincrement=True, nullable=False)
    team_name = sqla.Column(sqla.String(50), sqla.ForeignKey('Team.name'), nullable=False)
    season_year = sqla.Column(sqla.SmallInteger, sqla.ForeignKey('Season.year'), nullable=False)
    league_name = sqla.Column(sqla.String(5), sqla.ForeignKey('League.short_name'), nullable=False)
    conference_name = sqla.Column(sqla.String(5), sqla.ForeignKey('Conference.short_name'))
    division_name = sqla.Column(sqla.String(50), sqla.ForeignKey('Division.name'))
    games = sqla.Column(sqla.SmallInteger, nullable=False, default=0)
    wins = sqla.Column(sqla.SmallInteger, nullable=False, default=0)
    losses = sqla.Column(sqla.SmallInteger, nullable=False, default=0)
    ties = sqla.Column(sqla.SmallInteger, nullable=False, default=0)
    winning_percentage = sqla.Column(sqla.Numeric(precision=18, scale=17), nullable=False, default=0)
    points_for = sqla.Column(sqla.SmallInteger, nullable=False, default=0)
    points_against = sqla.Column(sqla.SmallInteger, nullable=False, default=0)
    expected_wins = sqla.Column(sqla.Numeric(precision=18, scale=16), nullable=False, default=0)
    expected_losses = sqla.Column(sqla.Numeric(precision=18, scale=16), nullable=False, default=0)
    offensive_average = sqla.Column(sqla.Numeric(precision=18, scale=15))
    offensive_factor = sqla.Column(sqla.Numeric(precision=18, scale=14))
    offensive_index = sqla.Column(sqla.Numeric(precision=18, scale=15))
    defensive_average = sqla.Column(sqla.Numeric(precision=18, scale=15))
    defensive_factor = sqla.Column(sqla.Numeric(precision=18, scale=14))
    defensive_index = sqla.Column(sqla.Numeric(precision=18, scale=15))
    final_expected_winning_percentage = sqla.Column(sqla.Numeric(precision=18, scale=17))

    def calculate_expected_wins_and_losses(self) -> None:
        """
        Calculates and updates the current TeamSeason object's Pythagorean wins and losses.

        :return: None
        """
        exp_pct = team_season_utils.calculate_expected_winning_percentage(self.points_for, self.points_against)
        if exp_pct is None:
            self.expected_wins = 0
            self.expected_losses = 0
        else:
            self.expected_wins = exp_pct * self.games
            self.expected_losses = (1 - exp_pct) * self.games

    def calculate_winning_percentage(self) -> None:
        """
        Calculates the current TeamSeason object's winning percentage.

        :return: None
        """
        self.winning_percentage = team_season_utils.divide(2 * self.wins + self.ties, 2 * self.games)

    def update_rankings(
            self,
            team_season_schedule_average_points_for: Decimal,
            team_season_schedule_average_points_against: Decimal,
            league_season_average_points: Decimal
    ) -> None:
        """
        Updates the current TeamSeason object's offensive and defensive averages, factors, and indices.

        :param team_season_schedule_average_points_for: This TeamSeason's schedule's average points scored per game.
        :param team_season_schedule_average_points_against: This TeamSeason's schedule's average allowed scored per game.
        :param league_season_average_points: The LeagueSeason's average points scored per game.

        :return: None
        """
        self.offensive_average, self.offensive_factor, self.offensive_index = \
            team_season_utils.update_rankings(
                self.points_for, self.games, team_season_schedule_average_points_against, league_season_average_points
            )

        self.defensive_average, self.defensive_factor, self.defensive_index = \
            team_season_utils.update_rankings(
                self.points_against, self.games, team_season_schedule_average_points_for, league_season_average_points
            )

        self._calculate_final_expected_winning_percentage()

    def _calculate_final_expected_winning_percentage(self) -> None:
        if self.offensive_index is None or self.defensive_index is None:
            return

        self.final_expected_winning_percentage = \
            team_season_utils.calculate_expected_winning_percentage(self.offensive_index, self.defensive_index)
