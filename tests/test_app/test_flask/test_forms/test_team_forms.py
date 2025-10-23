import unittest

from app.flask.forms.team_forms import TeamForm
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
    #     form = TeamForm(data={
    #         'name': "Chicago Cardinals",
    #     })
    #     self.assertTrue(form.validate())

    def test_name_not_provided(self):
        form = TeamForm(data={})
        self.assertFalse(form.validate())
        self.assertIn("Please enter a name.", form.name.errors)

    # def test_name_longer_than_max_length(self):
    #     form = TeamForm(data={
    #         'name': "The quick sly fox jumped over the lazy brown dog...",
    #     })
    #     self.assertFalse(form.validate())
    #     self.assertIn(f"name must not be longer than 50 characters.", form.name.errors)
