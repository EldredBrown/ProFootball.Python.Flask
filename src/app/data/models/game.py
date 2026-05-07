from sqlalchemy.orm import validates

from app.data.sqla import sqla


FIRST_YEAR = 1920


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
    notes = sqla.Column(sqla.Text)

    __table_args__ = (
        sqla.UniqueConstraint('season_year', 'week', 'guest_name', 'host_name',
                              name='uq_game_season_week_teams'),
    )

    def __repr__(self) -> str:
        return (f"<Game id={self.id!r} week={self.week} "
                f"{self.guest_name} {self.guest_score} @ "
                f"{self.host_name} {self.host_score}>")

    def to_dict(self) -> dict[str, object]:
        d = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        d.update({
            'winner_name': self.winner_name,
            'winner_score': self.winner_score,
            'loser_name': self.loser_name,
            'loser_score': self.loser_score,
            'is_tie': self.is_tie,
        })
        return d

    @property
    def winner_name(self) -> str | None:
        return self._outcome[0] if self._outcome else None

    @property
    def winner_score(self) -> int | None:
        return self._outcome[1] if self._outcome else None

    @property
    def loser_name(self) -> str | None:
        return self._outcome[2] if self._outcome else None

    @property
    def loser_score(self) -> int | None:
        return self._outcome[3] if self._outcome else None

    @property
    def _outcome(self) -> tuple[str, int, str, int] | None:
        """(winner_name, winner_score, loser_name, loser_score) or None if tie."""
        if self.is_tie:
            return None
        if self.guest_score > self.host_score:
            return self.guest_name, self.guest_score, self.host_name, self.host_score
        return self.host_name, self.host_score, self.guest_name, self.guest_score

    @property
    def is_tie(self) -> bool:
        """
        Checks to see if the current Game object is a tie.

        :return: True if the current Game object is a tie, otherwise false.
        """
        return self.guest_score == self.host_score

    @validates('season_year')
    def validate_season_year(self, key, value):
        if value is None:
            raise ValueError(f"{key} is required.")
        if value < FIRST_YEAR:
            raise ValueError(f"{key} cannot be earlier than {FIRST_YEAR}.")
        return value

    @validates('week')
    def validate_week(self, key, value):
        if value is None:
            raise ValueError(f"{key} is required.")
        if value < 1:
            raise ValueError(f"{key} cannot be less than 1.")
        return value

    @validates('guest_name', 'host_name')
    def validate_name(self, key, value):
        if not value or not value.strip():
            raise ValueError(f"{key} is required.")
        return value.strip()

    @validates('guest_score', 'host_score')
    def validate_score(self, key, value):
        if value is None:
            raise ValueError(f"{key} is required.")
        if value < 0:
            raise ValueError(f"{key} cannot be negative.")
        return value
