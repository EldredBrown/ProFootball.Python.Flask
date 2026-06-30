from decimal import Decimal

from app.data.sqla import sqla
from app.services.utilities import team_season_utils


_PCT_NUMERIC = dict(precision=18, scale=17)   # e.g. winning percentages (0.000...–1.000...)
_EXP_NUMERIC = dict(precision=18, scale=16)   # e.g. expected wins/losses
_AVG_NUMERIC = dict(precision=18, scale=15)   # e.g. averages
_FCT_NUMERIC = dict(precision=18, scale=14)   # e.g. factors


class TeamSeason(sqla.Model):
    """
    Class to represent the association between one pro football team and one pro football season.
    """
    __tablename__ = 'TeamSeason'

    id = sqla.Column(sqla.Integer, primary_key=True, autoincrement=True, nullable=False)
    team_id = sqla.Column(sqla.String(50), sqla.ForeignKey('Team.id'), nullable=False)
    season_id = sqla.Column(sqla.Integer, sqla.ForeignKey('Season.id'), nullable=False)
    league_id = sqla.Column(sqla.String(5), sqla.ForeignKey('League.id'), nullable=False)
    conference_id = sqla.Column(sqla.String(5), sqla.ForeignKey('Conference.id'))
    division_id = sqla.Column(sqla.String(50), sqla.ForeignKey('Division.id'))
    games = sqla.Column(sqla.Integer, nullable=False, default=0)
    wins = sqla.Column(sqla.Integer, nullable=False, default=0)
    losses = sqla.Column(sqla.Integer, nullable=False, default=0)
    ties = sqla.Column(sqla.Integer, nullable=False, default=0)
    points_for = sqla.Column(sqla.Integer, nullable=False, default=0)
    points_against = sqla.Column(sqla.Integer, nullable=False, default=0)
    expected_wins = sqla.Column(sqla.Numeric(**_EXP_NUMERIC), nullable=False, default=0)
    expected_losses = sqla.Column(sqla.Numeric(**_EXP_NUMERIC), nullable=False, default=0)
    offensive_average = sqla.Column(sqla.Numeric(**_AVG_NUMERIC))
    offensive_factor = sqla.Column(sqla.Numeric(**_FCT_NUMERIC))
    offensive_index = sqla.Column(sqla.Numeric(**_AVG_NUMERIC))
    defensive_average = sqla.Column(sqla.Numeric(**_AVG_NUMERIC))
    defensive_factor = sqla.Column(sqla.Numeric(**_FCT_NUMERIC))
    defensive_index = sqla.Column(sqla.Numeric(**_AVG_NUMERIC))
    final_expected_winning_percentage = sqla.Column(sqla.Numeric(**_PCT_NUMERIC))

    __table_args__ = (
        sqla.UniqueConstraint('team_id', 'season_id', name='uq_team_season'),
    )

    team = sqla.relationship('Team', back_populates='team_seasons')
    season = sqla.relationship('Season', back_populates='team_seasons')
    league = sqla.relationship('League', back_populates='team_seasons')
    conference = sqla.relationship('Conference', back_populates='team_seasons')
    division = sqla.relationship('Division', back_populates='team_seasons')

    def __repr__(self) -> str:
        return (f"<TeamSeason id={self.id!r} team={self.team_id!r} "
                f"season={self.season_id} record={self.wins}-{self.losses}-{self.ties}>")

    def to_dict(self) -> dict[str, object]:
        d = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        d.update({
            'winning_percentage': self.winning_percentage,
        })
        return d

    @property
    def winning_percentage(self) -> Decimal | None:
        return team_season_utils.divide(2 * self.wins + self.ties, 2 * self.games)

    def calculate_expected_wins_and_losses(self) -> None:
        """
        Calculates and updates the current TeamSeason object's Pythagorean wins and losses.

        :return: None
        """
        if self.games == 0:
            self.expected_wins = Decimal(0)
            self.expected_losses = Decimal(0)
            return

        exp_pct = team_season_utils.calculate_expected_winning_percentage(self.points_for, self.points_against)
        if exp_pct is None:
            self.expected_wins = Decimal(0)
            self.expected_losses = Decimal(0)
        else:
            self.expected_wins = exp_pct * self.games
            self.expected_losses = (1 - exp_pct) * self.games

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
        offense = team_season_utils.update_rankings(
            self.points_for, self.games,
            team_season_schedule_average_points_against,
            league_season_average_points
        )
        self.offensive_average = offense.average
        self.offensive_factor = offense.factor
        self.offensive_index = offense.index

        defense = team_season_utils.update_rankings(
            self.points_against, self.games,
            team_season_schedule_average_points_for,
            league_season_average_points
        )
        self.defensive_average = defense.average
        self.defensive_factor = defense.factor
        self.defensive_index = defense.index

        self._calculate_final_expected_winning_percentage()

    def _calculate_final_expected_winning_percentage(self) -> None:
        if self.offensive_index is None or self.defensive_index is None:
            self.final_expected_winning_percentage = None
            return

        self.final_expected_winning_percentage = \
            team_season_utils.calculate_expected_winning_percentage(self.offensive_index, self.defensive_index)
