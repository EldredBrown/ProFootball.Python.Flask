from sqlalchemy.orm import validates

from app.data.sqla import sqla


class League(sqla.Model):
    """
    Model to represent a pro football league.
    """
    __tablename__ = 'League'

    id = sqla.Column(sqla.Integer, primary_key=True, autoincrement=True, nullable=False)
    short_name = sqla.Column(sqla.String(5), unique=True, nullable=False)
    long_name = sqla.Column(sqla.String(50), unique=True, nullable=False)
    first_season_id = sqla.Column(sqla.Integer, sqla.ForeignKey('Season.id'), nullable=False)
    last_season_id = sqla.Column(sqla.Integer, sqla.ForeignKey('Season.id'), nullable=True)

    conferences = sqla.relationship('Conference', cascade='save-update, delete, delete-orphan, merge')
    divisions = sqla.relationship('Division', cascade='save-update, delete, delete-orphan, merge')

    league_seasons = sqla.relationship('LeagueSeason', back_populates='league')
    team_seasons = sqla.relationship('TeamSeason', cascade='save-update, delete, delete-orphan, merge')

    def to_dict(self):
        return {
            'id': self.id,
            'short_name': self.short_name,
            'long_name': self.long_name,
            'first_season_id': self.first_season_id,
            'last_season_id': self.last_season_id,
        }

    @validates('short_name', 'long_name', 'first_season_id')
    def validate_not_empty(self, key, value):
        if not value and value != 0:
            raise ValueError(f"{key} is required.")

        return value
