from sqlalchemy.orm import validates

from app.data.sqla import sqla


class Game(sqla.Model):
    """
    Class to represent a pro football game.
    """
    __tablename__ = 'game'

    id = sqla.Column(sqla.Integer, primary_key=True, autoincrement=True, nullable=False)
    season_year = sqla.Column(sqla.SmallInteger, sqla.ForeignKey('Season.year'), nullable=False)
    week = sqla.Column(sqla.SmallInteger, nullable=False)
    guest_name = sqla.Column(sqla.String(50), nullable=False)
    guest_score = sqla.Column(sqla.SmallInteger, nullable=False)
    host_name = sqla.Column(sqla.String(50), nullable=False)
    host_score = sqla.Column(sqla.SmallInteger, nullable=False)
    is_playoff = sqla.Column(sqla.Boolean, nullable=False, default=False)
    notes = sqla.Column(sqla.String(256))

    @property
    def winner_name(self) -> str | None:
        if self.guest_score > self.host_score:
            return self.guest_name
        elif self.host_score > self.guest_score:
            return self.host_name
        return None

    @property
    def winner_score(self) -> int:
        if self.guest_score > self.host_score:
            return self.guest_score
        elif self.host_score > self.guest_score:
            return self.host_score
        return None

    @property
    def loser_name(self) -> str | None:
        if self.guest_score > self.host_score:
            return self.host_name
        elif self.host_score > self.guest_score:
            return self.guest_name
        return None

    @property
    def loser_score(self) -> int:
        if self.guest_score > self.host_score:
            return self.host_score
        elif self.host_score > self.guest_score:
            return self.guest_score
        return None

    # guest = sqla.relationship('Team')
    # host = sqla.relationship('Team')
    # winner = sqla.relationship('Team')
    # loser = sqla.relationship('Team')

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @validates('season_year', 'week', 'guest_score', 'host_score')
    def validate_not_none_numeric(self, key, value):
        if value is None:
            raise ValueError(f"{key} is required.")
        return value

    @validates('guest_name', 'host_name')
    def validate_not_empty_string(self, key, value):
        if not value or not value.strip():
            raise ValueError(f"{key} is required.")
        return value

    def is_tie(self) -> bool:
        """
        Checks to see if the current Game object is a tie.

        :return: True if the current Game object is a tie, otherwise false.
        """
        return self.guest_score == self.host_score
