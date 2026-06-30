import unittest

from app.flask.forms.division_forms import DivisionForm
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

    def test_name_not_provided(self):
        form = DivisionForm(data={
            'league_name': "L",
            'conference_name': "C",
            'first_season_year': 1922,
            'last_season_year': None,
        })
        self.assertFalse(form.validate())
        self.assertIn("Please enter a name.", form.name.errors)

    def test_league_name_not_provided(self):
        form = DivisionForm(data={
            'name': "Division",
            'conference_name': "C",
            'first_season_year': 1922,
            'last_season_year': None,
        })
        self.assertFalse(form.validate())
        self.assertIn("Please enter a league name.", form.league_name.errors)

    def test_first_season_year_not_provided(self):
        form = DivisionForm(data={
            'name': "Division",
            'league_name': "L",
            'conference_name': "C",
            'last_season_year': None,
        })
        self.assertFalse(form.validate())
        self.assertIn("Please enter a year.", form.first_season_year.errors)
