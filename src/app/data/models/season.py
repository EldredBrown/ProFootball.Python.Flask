from sqlalchemy.orm import validates

from app.data.models.game import Game
from app.data.models.association import Association
from app.data.sqla import sqla


class Season(sqla.Model):
    """
    Model to represent a pro football season.
    """
    __tablename__ = 'Season'

    year = sqla.Column(sqla.Integer, primary_key=True, nullable=False)

    associations_first_season_of = sqla.relationship(
        'Association', foreign_keys=[Association.first_season_year], back_populates='first_season'
    )
    associations_last_season_of = sqla.relationship(
        'Association', foreign_keys=[Association.last_season_year], back_populates='last_season'
    )
    games = sqla.relationship('Game', foreign_keys=[Game.season_year])

    league_seasons = sqla.relationship('LeagueSeason', back_populates='season')
    team_seasons = sqla.relationship('TeamSeason', back_populates='season')

    def to_dict(self):
        d = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        return d

    @validates('year')
    def validate_not_empty(self, key, value):
        if not value and value != 0:
            raise ValueError(f"{key.capitalize()} is required.")

        return value
