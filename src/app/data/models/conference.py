from sqlalchemy.orm import validates

from app.data.sqla import sqla


class Conference(sqla.Model):
    """
    Class to represent a pro football conference.
    """
    __tablename__ = 'conference'

    id = sqla.Column(sqla.Integer, primary_key=True, autoincrement=True, nullable=False)
    short_name = sqla.Column(sqla.String(5), unique=True, nullable=False)
    long_name = sqla.Column(sqla.String(50), unique=True, nullable=False)
    league_name = sqla.Column(sqla.String(5), sqla.ForeignKey('league.short_name'), nullable=False)
    first_season_year = sqla.Column(sqla.SmallInteger, sqla.ForeignKey('season.year'), nullable=False)
    last_season_year = sqla.Column(sqla.SmallInteger, sqla.ForeignKey('season.year'), nullable=True)

    divisions = sqla.relationship('Division', cascade='save-update, delete, delete-orphan, merge')

    team_seasons = sqla.relationship('TeamSeason', cascade='save-update, delete, delete-orphan, merge')

    @validates('short_name', 'long_name', 'league_name', 'first_season_year')
    def validate_not_empty(self, key, value):
        if not value and value != 0:
            raise ValueError(f"{key} is required.")

        if key in ('short_name', 'long_name'):
            self.validate_is_unique(
                key, value, error_message=f"Row with {key}={value} already exists in the Conference table."
            )
        return value

    def validate_is_unique(self, key, value, error_message=None):
        if Conference.query.filter_by(**{key: value}).first() is not None:
            if not error_message:
                error_message = f"{key} must be unique."
            raise ValueError(error_message)
