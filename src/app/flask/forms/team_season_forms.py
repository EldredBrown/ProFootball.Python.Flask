from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, StringField
from wtforms.validators import DataRequired, InputRequired, NumberRange, ValidationError, Optional


def long_name_length_check(form, field):
    length_check(field, 50)


def short_name_length_check(form, field):
    length_check(field, 5)


def length_check(field, length):
    if len(field.data) > length:
        raise ValidationError(f"{field} must not be longer than {length} characters.")


class TeamSeasonForm(FlaskForm):
    team_name = StringField(
        "Team Name",
        validators=[
            InputRequired("Please enter a team name."),
            DataRequired("Please enter a team name."),
            long_name_length_check,
        ]
    )
    season_year = IntegerField(
        "Season Year",
        validators=[
            InputRequired("Please enter a year."),
            DataRequired("Please enter a year."),
            NumberRange(min=1920, message="Please enter a year no earlier than 1920.")
        ]
    )
    league_name = StringField(
        "League Name",
        validators=[
            InputRequired("Please enter a league's short name."),
            DataRequired("Please enter a league's short name."),
            short_name_length_check,
        ]
    )
    conference_name = StringField(
        "Conference Name"
    )
    division_name = StringField(
        "Division Name"
    )


class NewTeamSeasonForm(TeamSeasonForm):
    submit = SubmitField("Create")


class EditTeamSeasonForm(TeamSeasonForm):
    submit = SubmitField("Update")


class DeleteTeamSeasonForm(FlaskForm):
    submit = SubmitField("Delete")
