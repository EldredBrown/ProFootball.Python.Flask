from sqlalchemy.orm import validates

from app.data.sqla import sqla


class Team(sqla.Model):
    """
    Class to represent a pro football team.
    """
    __tablename__ = 'team'

    id = sqla.Column(sqla.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = sqla.Column(sqla.String(50), unique=True, nullable=False)

    team_seasons = sqla.relationship('Season', secondary='team_season', lazy=True)

    @validates('name')
    def validate_not_empty(self, key, value):
        if not value and value != 0:
            raise ValueError(f"{key} is required.")

        if key == 'name':
            self.validate_is_unique(
                key, value, error_message=f"Row with {key}='{value}' already exists in the Team table."
            )
        return value

    def validate_is_unique(self, key, value, error_message=None):
        if Team.query.filter_by(**{key: value}).first() is not None:
            if not error_message:
                error_message = f"{key} must be unique."
            raise ValueError(error_message)
