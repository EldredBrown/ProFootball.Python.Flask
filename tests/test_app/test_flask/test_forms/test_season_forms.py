import unittest

from app.flask.forms.season_forms import SeasonForm
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
    #     form = SeasonForm(data={
    #         'year': 1920,
    #         'num_of_weeks_scheduled': 0,
    #     })
    #     self.assertTrue(form.validate())

    def test_year_not_provided(self):
        form = SeasonForm(data={
            'num_of_weeks_scheduled': 13,
        })
        self.assertFalse(form.validate())
        self.assertIn("Please enter a year.", form.year.errors)

    # def test_year_less_than_minimum(self):
    #     form = SeasonForm(data={
    #         'year': 1919,
    #         'num_of_weeks_scheduled': 0,
    #     })
    #     self.assertFalse(form.validate())
    #     self.assertIn("Please enter a year no earlier than 1920.", form.year.errors)
    #
    # def test_num_of_weeks_scheduled_less_than_zero(self):
    #     form = SeasonForm(data={
    #         'year': 1920,
    #         'num_of_weeks_scheduled': -1,
    #     })
    #     self.assertFalse(form.validate())
    #     self.assertIn("Please enter a non-negative number of weeks scheduled.", form.num_of_weeks_scheduled.errors)
