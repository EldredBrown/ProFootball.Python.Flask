from typing import Optional

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
    winner_name = sqla.Column(sqla.String(50))
    winner_score = sqla.Column(sqla.SmallInteger)
    loser_name = sqla.Column(sqla.String(50))
    loser_score = sqla.Column(sqla.SmallInteger)
    is_playoff = sqla.Column(sqla.Boolean, nullable=False, default=False)
    notes = sqla.Column(sqla.String(256))

    # guest = sqla.relationship('Team')
    # host = sqla.relationship('Team')
    # winner = sqla.relationship('Team')
    # loser = sqla.relationship('Team')

    @validates('season_year', 'week', 'guest_name', 'guest_score', 'host_name', 'host_score', 'is_playoff')
    def validate_not_empty(self, key, value):
        if not value and value != 0:
            raise ValueError(f"{key} is required.")

        return value

    def decide_winner_and_loser(self) -> None:
        """
        Decides the current Game object's winner and loser.

        :return: None
        """
        if self._host_win():
            self._set_winner_and_loser_names_and_scores(
                winner_name=self.host_name, winner_score=self.host_score,
                loser_name=self.guest_name, loser_score=self.guest_score
            )
        elif self._guest_win():
            self._set_winner_and_loser_names_and_scores(
                winner_name=self.guest_name, winner_score=self.guest_score,
                loser_name=self.host_name, loser_score=self.host_score
            )
        else:   # Game is a tie.
            self._set_winner_and_loser_names_and_scores(
                winner_name=None, winner_score=None,
                loser_name=None, loser_score=None
            )

    def _guest_win(self):
        return self.guest_score > self.host_score

    def _host_win(self):
        return self.host_score > self.guest_score

    def _set_winner_and_loser_names_and_scores(self,
            winner_name: Optional[str], winner_score: Optional[int],
            loser_name: Optional[str], loser_score: Optional[int]
    ) -> None:
        self.winner_name = winner_name
        self.winner_score = winner_score
        self.loser_name = loser_name
        self.loser_score = loser_score

    def is_tie(self) -> bool:
        """
        Checks to see if the current Game object is a tie.

        :return: True if the current Game object is a tie, otherwise false.
        """
        return self.guest_score == self.host_score
