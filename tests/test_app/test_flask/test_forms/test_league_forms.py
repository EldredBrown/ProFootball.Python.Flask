import unittest

from app.flask.forms.league_forms import LeagueForm
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

    # def test_valid_form(self):
    #     form = LeagueForm(data={
    #         'short_name': "NFL",
    #         'long_name': "National Football League",
    #         'first_season_year': 1922,
    #         'last_season_year': None,
    #     })
    #     self.assertTrue(form.validate())

    def test_short_name_not_provided(self):
        form = LeagueForm(data={
            'long_name': "National Football League",
            'first_season_year': 1922,
            'last_season_year': None,
        })
        self.assertFalse(form.validate())
        self.assertIn("Please enter a short name.", form.short_name.errors)

    # def test_short_name_longer_than_max_length(self):
    #     form = LeagueForm(data={
    #         'short_name': "NFLLFN",
    #         'long_name': "National Football League",
    #         'first_season_year': 1922,
    #         'last_season_year': None,
    #     })
    #     self.assertFalse(form.validate())
    #     self.assertIn(f"short_name must not be longer than 5 characters.", form.short_name.errors)

    def test_long_name_not_provided(self):
        form = LeagueForm(data={
            'short_name': "NFL",
            'first_season_year': 1922,
            'last_season_year': None,
        })
        self.assertFalse(form.validate())
        self.assertIn("Please enter a long name.", form.long_name.errors)

    # def test_long_name_longer_than_max_length(self):
    #     form = LeagueForm(data={
    #         'short_name': "NFL",
    #         'long_name': "National Football League  American Football League",
    #         'first_season_year': 1922,
    #         'last_season_year': None,
    #     })
    #     self.assertFalse(form.validate())
    #     self.assertIn(f"long_name must not be longer than 50 characters.", form.long_name.errors)

    def test_first_season_year_not_provided(self):
        form = LeagueForm(data={
            'short_name': "NFL",
            'long_name': "National Football League",
            'last_season_year': None,
        })
        self.assertFalse(form.validate())
        self.assertIn("Please enter a year.", form.first_season_year.errors)

    # def test_first_season_year_less_than_minimum(self):
    #     form = LeagueForm(data={
    #         'short_name': "NFL",
    #         'long_name': "National Football League",
    #         'first_season_year': 1919,
    #         'last_season_year': None,
    #     })
    #     self.assertFalse(form.validate())
    #     self.assertIn("Please enter a year no earlier than 1920.", form.first_season_year.errors)
