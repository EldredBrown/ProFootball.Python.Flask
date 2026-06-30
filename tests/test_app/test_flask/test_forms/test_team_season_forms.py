import unittest

from app.flask.forms.team_season_forms import TeamSeasonForm
from test_app import create_app


class TestForms(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.ctx = self.app.test_request_context()
        self.ctx.push()

    def tearDown(self):
        self.ctx.pop()

    def test_team_name_not_provided(self):
        form = TeamSeasonForm(data={
            'season_year': 1920,
            'league_name': "L",
        })
        self.assertFalse(form.validate())
        self.assertIn("Please enter a team name.", form.team_name.errors)

    def test_season_year_not_provided(self):
        form = TeamSeasonForm(data={
            'team_name': "Team",
            'league_name': "L",
        })
        self.assertFalse(form.validate())
        self.assertIn("Please enter a year.", form.season_year.errors)

    def test_league_name_not_provided(self):
        form = TeamSeasonForm(data={
            'season_year': 1920,
            'team_name': "Team",
        })
        self.assertFalse(form.validate())
        self.assertIn("Please enter a league's short name.", form.league_name.errors)
