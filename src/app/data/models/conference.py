from sqlalchemy.orm import validates

from app.data.sqla import sqla


class Conference(sqla.Model):
    """
    Model to represent a pro football conference.
    """
    __tablename__ = 'Conference'

    id = sqla.Column(sqla.Integer, primary_key=True, autoincrement=True, nullable=False)
    short_name = sqla.Column(sqla.String(5), unique=True, nullable=False)
    long_name = sqla.Column(sqla.String(50), unique=True, nullable=False)
    league_id = sqla.Column(sqla.Integer, sqla.ForeignKey('League.id'), nullable=False)
    first_season_id = sqla.Column(sqla.Integer, sqla.ForeignKey('Season.id'), nullable=False)
    last_season_id = sqla.Column(sqla.Integer, sqla.ForeignKey('Season.id'), nullable=True)

    league = sqla.relationship('League', back_populates='conferences')

    divisions = sqla.relationship('Division', cascade='save-update, delete, delete-orphan, merge')
    team_seasons = sqla.relationship('TeamSeason', cascade='save-update, delete, delete-orphan, merge')

    def to_dict(self):
        return {
            'id': self.id,
            'short_name': self.short_name,
            'long_name': self.long_name,
            'league_id': self.league_id,
            'first_season_id': self.first_season_id,
            'last_season_id': self.last_season_id,
        }

    @validates('short_name', 'long_name', 'league_id', 'first_season_id')
    def validate_not_empty(self, key, value):
        if not value and value != 0:
            raise ValueError(f"{key} is required.")

        return value
