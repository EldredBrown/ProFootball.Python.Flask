from sqlalchemy.orm import validates

from app.data.sqla import sqla

EXPONENT = 2.37


class TeamSeason(sqla.Model):
    """
    Class to represent the association between one pro football team and one pro football season.
    """
    __tablename__ = 'team_season'

    id = sqla.Column(sqla.Integer, primary_key=True, autoincrement=True, nullable=False)
    team_name = sqla.Column(sqla.String(50), sqla.ForeignKey('team.name'), nullable=False)
    season_year = sqla.Column(sqla.SmallInteger, sqla.ForeignKey('season.year'), nullable=False)
    league_name = sqla.Column(sqla.SmallInteger, sqla.ForeignKey('league.short_name'), nullable=False)
    conference_name = sqla.Column(sqla.SmallInteger, sqla.ForeignKey('conference.short_name'))
    division_name = sqla.Column(sqla.SmallInteger, sqla.ForeignKey('division.name'))
    games = sqla.Column(sqla.SmallInteger, nullable=False, default=0)
    wins = sqla.Column(sqla.SmallInteger, nullable=False, default=0)
    losses = sqla.Column(sqla.SmallInteger, nullable=False, default=0)
    ties = sqla.Column(sqla.SmallInteger, nullable=False, default=0)
    winning_percentage = sqla.Column(sqla.Float)
    points_for = sqla.Column(sqla.SmallInteger, nullable=False, default=0)
    points_against = sqla.Column(sqla.SmallInteger, nullable=False, default=0)
    expected_wins = sqla.Column(sqla.Float, nullable=False, default=0)
    expected_losses = sqla.Column(sqla.Float, nullable=False, default=0)
    offensive_average = sqla.Column(sqla.Float)
    offensive_factor = sqla.Column(sqla.Float)
    offensive_index = sqla.Column(sqla.Float)
    defensive_average = sqla.Column(sqla.Float)
    defensive_factor = sqla.Column(sqla.Float)
    defensive_index = sqla.Column(sqla.Float)
    final_expected_winning_percentage = sqla.Column(sqla.Float)

    @validates('team_name', 'season_year', 'league_name')
    def validate_not_empty(self, key, value):
        if not value and value != 0:
            raise ValueError(f"{key} is required.")

        return value

    def calculate_expected_wins_and_losses(self) -> None:
        """
        Calculates and updates the current TeamSeason object's Pythagorean wins and losses.

        :return: None
        """
        exp_pct = calculate_expected_winning_percentage(self.points_for, self.points_against)
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
        if self.games == 0:
            self.winning_percentage = None
        else:
            self.winning_percentage = (2 * self.wins + self.ties) / (2 * self.games)

    def update_rankings(self, team_season_schedule_average_points_for: float,
                        team_season_schedule_average_points_against: float,
                        league_season_average_points: float) -> None:
        """
        Updates the current TeamSeason object's offensive and defensive averages, factors, and indices.

        :param team_season_schedule_average_points_for:
        :param team_season_schedule_average_points_against:
        :param league_season_average_points:

        :return: None
        """
        self.offensive_average, self.offensive_factor, self.offensive_index = \
            update_rankings(self.points_for, self.games, team_season_schedule_average_points_against,
                            league_season_average_points)

        self.defensive_average, self.defensive_factor, self.defensive_index = \
            update_rankings(self.points_against, self.games, team_season_schedule_average_points_for,
                            league_season_average_points)

        self._calculate_final_expected_winning_percentage()

    def _calculate_final_expected_winning_percentage(self) -> None:
        if self.offensive_index is None or self.defensive_index is None:
            return

        self.final_expected_winning_percentage = \
            calculate_expected_winning_percentage(self.offensive_index, self.defensive_index)


def calculate_expected_winning_percentage(points_for: float, points_against: float) -> float | None:
    o = pow(points_for, EXPONENT)
    d = pow(points_against, EXPONENT)
    return divide(o, o + d)


def divide(numerator: int | float, denominator: int | float) -> float | None:
    if denominator == 0:
        return None

    return numerator / denominator


def update_rankings(points: int, games: int, team_season_schedule_average_points: float,
                    league_season_average_points: float) -> tuple[float | None, float | None, float | None]:
    if games == 0:
        return None, None, None

    average = divide(points, games)
    factor = divide(average, team_season_schedule_average_points)

    if factor is None:
        index = None
    else:
        index = divide(average + factor * league_season_average_points, 2)

    return average, factor, index
