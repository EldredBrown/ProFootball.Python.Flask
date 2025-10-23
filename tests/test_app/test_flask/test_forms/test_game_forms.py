import unittest

from app.flask.forms.game_forms import GameForm
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
    #     form = GameForm(data={
    #         'season_year': 1920,
    #         'week': 1,
    #         'guest_name': "St. Paul Ideals",
    #         'guest_score': 0,
    #         'host_name': "Rock Island Independents",
    #         'host_score': 48,
    #         'is_playoff': False,
    #     })
    #     self.assertTrue(form.validate())

    def test_season_year_not_provided(self):
        form = GameForm(data={
            'week': 1,
            'guest_name': "St. Paul Ideals",
            'guest_score': 0,
            'host_name': "Rock Island Independents",
            'host_score': 48,
            'is_playoff': False,
        })
        self.assertFalse(form.validate())
        self.assertIn("Please enter a year.", form.season_year.errors)

    # def test_season_year_less_than_minimum(self):
    #     form = GameForm(data={
    #         'season_year': 1919,
    #         'week': 1,
    #         'guest_name': "St. Paul Ideals",
    #         'guest_score': 0,
    #         'host_name': "Rock Island Independents",
    #         'host_score': 48,
    #         'is_playoff': False,
    #     })
    #     self.assertFalse(form.validate())
    #     self.assertIn("Please enter a year no earlier than 1920.", form.season_year.errors)

    def test_week_not_provided(self):
        form = GameForm(data={
            'season_year': 1920,
            'guest_name': "St. Paul Ideals",
            'guest_score': 0,
            'host_name': "Rock Island Independents",
            'host_score': 48,
            'is_playoff': False,
        })
        self.assertFalse(form.validate())
        self.assertIn("Please enter a week.", form.week.errors)

    # def test_week_less_than_zero(self):
    #     form = GameForm(data={
    #         'season_year': 1919,
    #         'week': -1,
    #         'guest_name': "St. Paul Ideals",
    #         'guest_score': 0,
    #         'host_name': "Rock Island Independents",
    #         'host_score': 48,
    #         'is_playoff': False,
    #     })
    #     self.assertFalse(form.validate())
    #     self.assertIn("Please enter a non-negative week value.", form.week.errors)

    def test_guest_name_not_provided(self):
        form = GameForm(data={
            'season_year': 1920,
            'week': 1,
            'guest_score': 0,
            'host_name': "Rock Island Independents",
            'host_score': 48,
            'is_playoff': False,
        })
        self.assertFalse(form.validate())
        self.assertIn("Please enter a guest name.", form.guest_name.errors)

    # def test_guest_name_longer_than_max_length(self):
    #     form = GameForm(data={
    #         'season_year': 1920,
    #         'week': 1,
    #         'guest_name': "The quick sly fox jumped over the lazy brown dog...",
    #         'guest_score': 0,
    #         'host_name': "Rock Island Independents",
    #         'host_score': 48,
    #         'is_playoff': False,
    #     })
    #     self.assertFalse(form.validate())
    #     self.assertIn(f"guest_name must not be longer than 50 characters.", form.guest_name.errors)

    def test_guest_score_not_provided(self):
        form = GameForm(data={
            'season_year': 1920,
            'week': 1,
            'guest_name': "St. Paul Ideals",
            'host_name': "Rock Island Independents",
            'host_score': 48,
            'is_playoff': False,
        })
        self.assertFalse(form.validate())
        self.assertIn("Please enter a guest score.", form.guest_score.errors)

    # def test_guest_score_less_than_zero(self):
    #     form = GameForm(data={
    #         'season_year': 1920,
    #         'week': 1,
    #         'guest_name': "St. Paul Ideals",
    #         'guest_score': -1,
    #         'host_name': "Rock Island Independents",
    #         'host_score': 48,
    #         'is_playoff': False,
    #     })
    #     self.assertFalse(form.validate())
    #     self.assertIn("Please enter a non-negative guest score.", form.guest_score.errors)

    def test_host_name_not_provided(self):
        form = GameForm(data={
            'season_year': 1920,
            'week': 1,
            'guest_name': "St. Paul Ideals",
            'guest_score': 0,
            'host_score': 48,
            'is_playoff': False,
        })
        self.assertFalse(form.validate())
        self.assertIn("Please enter a host name.", form.host_name.errors)

    # def test_host_name_longer_than_max_length(self):
    #     form = GameForm(data={
    #         'season_year': 1920,
    #         'week': 1,
    #         'guest_name': "St. Paul Ideals",
    #         'guest_score': 0,
    #         'host_name': "The quick sly fox jumped over the lazy brown dog...",
    #         'host_score': 48,
    #         'is_playoff': False,
    #     })
    #     self.assertFalse(form.validate())
    #     self.assertIn(f"host_name must not be longer than 50 characters.", form.host_name.errors)

    def test_host_score_not_provided(self):
        form = GameForm(data={
            'season_year': 1920,
            'week': 1,
            'guest_name': "St. Paul Ideals",
            'guest_score': 0,
            'host_name': "Rock Island Independents",
            'is_playoff': False,
        })
        self.assertFalse(form.validate())
        self.assertIn("Please enter a host score.", form.host_score.errors)

    # def test_host_score_less_than_zero(self):
    #     form = GameForm(data={
    #         'season_year': 1920,
    #         'week': 1,
    #         'guest_name': "St. Paul Ideals",
    #         'guest_score': 0,
    #         'host_name': "Rock Island Independents",
    #         'host_score': -1,
    #         'is_playoff': False,
    #     })
    #     self.assertFalse(form.validate())
    #     self.assertIn("Please enter a non-negative host score.", form.host_score.errors)

    def test_is_playoff_not_provided(self):
        form = GameForm(data={
            'season_year': 1920,
            'week': 1,
            'guest_name': "St. Paul Ideals",
            'guest_score': 0,
            'host_name': "Rock Island Independents",
            'host_score': 48,
        })
        self.assertFalse(form.validate())
        self.assertIn("Please enter a host score.", form.host_score.errors)
