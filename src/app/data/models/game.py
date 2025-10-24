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
        if self.guest_score > self.host_score:
            self.winner_name = self.guest_name
            self.winner_score = self.guest_score
            self.loser_name = self.host_name
            self.loser_score = self.host_score
        elif self.guest_score < self.host_score:
            self.winner_name = self.host_name
            self.winner_score = self.host_score
            self.loser_name = self.guest_name
            self.loser_score = self.guest_score
        else:
            self.winner_name = None
            self.loser_name = None

    def is_tie(self) -> bool:
        """
        Checks to see if the current Game object is a tie.

        :return: True if the current Game object is a tie, otherwise false.
        """
        return self.guest_score == self.host_score
