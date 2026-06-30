from sqlalchemy.orm import validates

from app.data.models.game import Game
from app.data.models.league import League
from app.data.models.conference import Conference
from app.data.models.division import Division
from app.data.sqla import sqla


class Season(sqla.Model):
    """
    Model to represent a pro football season.
    """
    __tablename__ = 'Season'

    id = sqla.Column(sqla.Integer, primary_key=True, autoincrement=True, nullable=False)
    num_of_weeks_scheduled = sqla.Column(sqla.Integer, nullable=False, default=0)
    num_of_weeks_completed = sqla.Column(sqla.Integer, nullable=False, default=0)

    leagues_first_season_of = sqla.relationship('League', foreign_keys=[League.first_season_id])
    leagues_last_season_of = sqla.relationship('League', foreign_keys=[League.last_season_id])
    conferences_first_season_of = sqla.relationship('Conference', foreign_keys=[Conference.first_season_id])
    conferences_last_season_of = sqla.relationship('Conference', foreign_keys=[Conference.last_season_id])
    divisions_first_season_of = sqla.relationship('Division', foreign_keys=[Division.first_season_id])
    divisions_last_season_of = sqla.relationship('Division', foreign_keys=[Division.last_season_id])
    games = sqla.relationship('Game', foreign_keys=[Game.season_id])

    league_seasons = sqla.relationship('LeagueSeason', back_populates='season')
    team_seasons = sqla.relationship('TeamSeason', back_populates='season')

    def to_dict(self):
        d = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        return d

    @validates('id')
    def validate_not_empty(self, key, value):
        if not value and value != 0:
            raise ValueError(f"{key.capitalize()} is required.")

        return value
