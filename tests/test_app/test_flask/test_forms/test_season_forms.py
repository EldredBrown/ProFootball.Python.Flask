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

    def test_id_not_provided(self):
        form = SeasonForm(data={
            'num_of_weeks_scheduled': 13,
        })
        self.assertFalse(form.validate())
        self.assertIn("Please enter a year.", form.id.errors)
