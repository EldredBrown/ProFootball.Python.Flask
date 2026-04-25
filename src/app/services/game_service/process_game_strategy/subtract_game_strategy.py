from app.data.models.game import Game
from app.data.models.team_season import TeamSeason
from app.services.game_service.process_game_strategy.process_game_strategy import ProcessGameStrategy


class SubtractGameStrategy(ProcessGameStrategy):
    """
    A ProcessGameStrategy implementation for adding games to the data store.
    """

    def _update_games_for_team_seasons(self, guest_season: TeamSeason, host_season: TeamSeason) -> None:
        guest_season.games -= 1
        host_season.games -= 1

    def _update_wins_losses_and_ties_for_team_seasons(self,
                                                      guest_season: TeamSeason,
                                                      host_season: TeamSeason,
                                                      game: Game) -> None:
        if game.is_tie():
            guest_season.ties -= 1
            host_season.ties -= 1

        else:
            # Guest is winner if game.winner_name matches guest team name.
            winner, loser = (
                (guest_season, host_season) if game.winner_name == game.guest_name else (host_season, guest_season)
            )
            winner.wins -= 1
            loser.losses -= 1

    def _edit_scoring_data_for_team_season(self, team_season: TeamSeason, team_score: int, opponent_score: int) -> None:
        team_season.points_for -= team_score
        team_season.points_against -= opponent_score
        team_season.calculate_expected_wins_and_losses()
