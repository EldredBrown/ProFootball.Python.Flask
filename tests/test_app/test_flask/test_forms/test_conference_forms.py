import unittest

from app.flask.forms.conference_forms import ConferenceForm
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

    def test_short_name_not_provided(self):
        form = ConferenceForm(data={
            'long_name': "National Football Conference",
            'league_name': "NFL",
            'first_season_year': 1922,
            'last_season_year': None,
        })
        self.assertFalse(form.validate())
        self.assertIn("Please enter a short name.", form.short_name.errors)

    def test_long_name_not_provided(self):
        form = ConferenceForm(data={
            'short_name': "NFL",
            'league_name': "NFL",
            'first_season_year': 1922,
            'last_season_year': None,
        })
        self.assertFalse(form.validate())
        self.assertIn("Please enter a long name.", form.long_name.errors)

    def test_league_name_not_provided(self):
        form = ConferenceForm(data={
            'short_name': "NFL",
            'long_name': "National Football Conference",
            'first_season_year': 1922,
            'last_season_year': None,
        })
        self.assertFalse(form.validate())
        self.assertIn("Please enter a league name.", form.league_name.errors)

    def test_first_season_year_not_provided(self):
        form = ConferenceForm(data={
            'short_name': "NFL",
            'long_name': "National Football Conference",
            'league_name': "NFL",
            'last_season_year': None,
        })
        self.assertFalse(form.validate())
        self.assertIn("Please enter a year.", form.first_season_year.errors)
