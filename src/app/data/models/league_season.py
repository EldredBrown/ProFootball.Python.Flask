from decimal import Decimal

from sqlalchemy.orm import validates

from app.data.sqla import sqla


class LeagueSeason(sqla.Model):
    """
    Class to represent the association between one pro football league and one pro football season.
    """
    __tablename__ = 'LeagueSeason'

    id = sqla.Column(sqla.Integer, primary_key=True, autoincrement=True, nullable=False)
    league_id = sqla.Column(sqla.Integer, sqla.ForeignKey('Association.id'), nullable=False)
    season_year = sqla.Column(sqla.Integer, sqla.ForeignKey('Season.year'), nullable=False)
    num_of_weeks_scheduled = sqla.Column(sqla.Integer, nullable=False, default=0)
    num_of_weeks_completed = sqla.Column(sqla.Integer, nullable=False, default=0)
    total_games = sqla.Column(sqla.Integer, nullable=False, default=0)
    total_points = sqla.Column(sqla.Integer, nullable=False, default=0)
    average_points = sqla.Column(sqla.Numeric(precision=18, scale=16), nullable=True)

    __table_args__ = (
        sqla.UniqueConstraint('league_id', 'season_year', name='uq_league_season'),
    )

    league = sqla.relationship('Association', back_populates='league_seasons')
    season = sqla.relationship('Season', back_populates='league_seasons')

    @validates('league_id', 'season_year')
    def validate_not_empty(self, key, value):
        if not value and value != 0:
            raise ValueError(f"{key} is required.")

        return value

    def update_games_and_points(self, total_games: int, total_points: int) -> None:
        """
        Updates the games and points league_season_totals of the current LeagueSeason object.

        :param total_games: The value to which the current LeagueSeason object's total games will be updated.
        :param total_points: The value to which the current LeagueSeason object's total points will be
        updated.

        :return: None
        """
        self.total_games = total_games
        self.total_points = total_points
        self.average_points = Decimal(total_points) / Decimal(total_games) if total_games != Decimal('0') else None
