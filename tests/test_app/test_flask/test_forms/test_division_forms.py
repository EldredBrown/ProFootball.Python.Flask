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

    # def test_valid_form(self):
    #     form = DivisionForm(data={
    #         'name': "NFC East",
    #         'league_name': "NFL",
    #         'conference_name': "NFC",
    #         'first_season_year': 1970,
    #         'last_season_year': None,
    #     })
    #     self.assertTrue(form.validate())

    def test_name_not_provided(self):
        form = DivisionForm(data={
            'league_name': "NFL",
            'conference_name': "NFC",
            'first_season_year': 1970,
            'last_season_year': None,
        })
        self.assertFalse(form.validate())
        self.assertIn("Please enter a name.", form.name.errors)

    # def test_name_longer_than_max_length(self):
    #     form = DivisionForm(data={
    #         'name': "The quick sly fox jumped over the lazy brown dog...",
    #         'league_name': "NFL",
    #         'conference_name': "NFC",
    #         'first_season_year': 1970,
    #         'last_season_year': None,
    #     })
    #     self.assertFalse(form.validate())
    #     self.assertIn(f"name must not be longer than 50 characters.", form.name.errors)

    def test_league_name_not_provided(self):
        form = DivisionForm(data={
            'name': "NFC East",
            'conference_name': "NFC",
            'first_season_year': 1970,
            'last_season_year': None,
        })
        self.assertFalse(form.validate())
        self.assertIn("Please enter a league name.", form.league_name.errors)

    # def test_league_name_longer_than_max_length(self):
    #     form = DivisionForm(data={
    #         'name': "NFC East",
    #         'league_name': "The quick sly fox jumped over the lazy brown dog...",
    #         'conference_name': "NFC",
    #         'first_season_year': 1970,
    #         'last_season_year': None,
    #     })
    #     self.assertFalse(form.validate())
    #     self.assertIn("long_name must not be longer than 50 characters.", form.league_name.errors)

    def test_first_season_year_not_provided(self):
        form = DivisionForm(data={
            'name': "NFC East",
            'league_name': "NFL",
            'conference_name': None,
            'last_season_year': None,
        })
        self.assertFalse(form.validate())
        self.assertIn("Please enter a year.", form.first_season_year.errors)

    # def test_first_season_year_less_than_minimum(self):
    #     form = DivisionForm(data={
    #         'name': "NFC",
    #         'league_name': "NFL",
    #         'conference_name': "NFC",
    #         'first_season_year': 1919,
    #         'last_season_year': None,
    #     })
    #     self.assertFalse(form.validate())
    #     self.assertIn("Please enter a year no earlier than 1920.", form.first_season_year.errors)
