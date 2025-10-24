from sqlalchemy.orm import validates

from app.data.sqla import sqla


class Team(sqla.Model):
    """
    Class to represent a pro football team.
    """
    __tablename__ = 'Team'

    id = sqla.Column(sqla.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = sqla.Column(sqla.String(50), unique=True, nullable=False)

    team_seasons = sqla.relationship('Season', secondary='TeamSeason', lazy=True)

    @validates('name')
    def validate_not_empty(self, key, value):
        if not value and value != 0:
            raise ValueError(f"{key} is required.")
        return value
