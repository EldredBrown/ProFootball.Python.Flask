from sqlalchemy.orm import validates

from app.data.sqla import sqla


class Division(sqla.Model):
    """
    Class to represent a pro football division.
    """
    __tablename__ = 'Division'

    id = sqla.Column(sqla.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = sqla.Column(sqla.String(50), unique=True, nullable=False)
    league_name = sqla.Column(sqla.String(5), sqla.ForeignKey('League.short_name'), nullable=False)
    conference_name = sqla.Column(sqla.String(5), sqla.ForeignKey('Conference.short_name'), nullable=True)
    first_season_year = sqla.Column(sqla.SmallInteger, sqla.ForeignKey('Season.year'), nullable=False)
    last_season_year = sqla.Column(sqla.SmallInteger, sqla.ForeignKey('Season.year'), nullable=True)

    team_seasons = sqla.relationship('TeamSeason', cascade='save-update, delete, delete-orphan, merge')

    @validates('name', 'league_name', 'first_season_year')
    def validate_not_empty(self, key, value):
        if not value and value != 0:
            raise ValueError(f"{key} is required.")
        return value
