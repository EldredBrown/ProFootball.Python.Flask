from sqlalchemy.orm import validates

from app.data.models.game import Game
from app.data.models.team_season import TeamSeason
from app.data.sqla import sqla


class Association(sqla.Model):
    """
    Model to represent a pro football league.
    """
    __tablename__ = 'Association'

    id = sqla.Column(sqla.Integer, primary_key=True, autoincrement=True, nullable=False)
    long_name = sqla.Column(sqla.String(100), unique=True, nullable=False)
    short_name = sqla.Column(sqla.String(5), unique=True, nullable=False)
    parent_id = sqla.Column(sqla.Integer, sqla.ForeignKey('Association.id'), nullable=True)
    first_season_year = sqla.Column(sqla.Integer, sqla.ForeignKey('Season.year'), nullable=False)
    last_season_year = sqla.Column(sqla.Integer, sqla.ForeignKey('Season.year'), nullable=True)

    parent = sqla.relationship('Association', back_populates='children', remote_side=[id])
    children = sqla.relationship('Association', back_populates='parent')
    first_season = sqla.relationship('Season', foreign_keys=[first_season_year],
                                     back_populates='associations_first_season_of')
    last_season = sqla.relationship('Season', foreign_keys=[last_season_year],
                                    back_populates='associations_last_season_of')
    games = sqla.relationship('Game', foreign_keys=[Game.league_id], back_populates='league')
    league_seasons = sqla.relationship('LeagueSeason', back_populates='league')
    team_seasons_league_of = sqla.relationship('TeamSeason', foreign_keys=[TeamSeason.league_id], back_populates='league')
    team_seasons_conference_of = sqla.relationship('TeamSeason', foreign_keys=[TeamSeason.conference_id], back_populates='conference')
    team_seasons_division_of = sqla.relationship('TeamSeason', foreign_keys=[TeamSeason.division_id], back_populates='division')

    def to_dict(self):
        return {
            'id': self.id,
            'long_name': self.long_name,
            'short_name': self.short_name,
            'parent_id': self.parent_id,
            'first_season_year': self.first_season_year,
            'last_season_year': self.last_season_year,
        }

    @validates('long_name', 'short_name', 'first_season_year')
    def validate_not_empty(self, key, value):
        if not value and value != 0:
            raise ValueError(f"{key} is required.")

        return value
