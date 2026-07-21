from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, StringField
from wtforms.validators import DataRequired, InputRequired, NumberRange, ValidationError, Optional


def short_name_length_check(form, field):
    length_check(field, 5)


def length_check(field, length):
    if len(field.data) > length:
        raise ValidationError(f"{field} must not be longer than {length} characters.")


class LeagueSeasonForm(FlaskForm):
    league_name = StringField(
        "League Name",
        validators=[
            InputRequired("Please enter a league's short name."),
            DataRequired("Please enter a league's short name."),
            short_name_length_check,
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
    num_of_weeks_scheduled = IntegerField(
        "Weeks Scheduled", default=0,
        validators=[
            NumberRange(min=0, message="Please enter a non-negative number of weeks scheduled.")
        ]
    )
    num_of_weeks_completed = IntegerField(
        "Weeks Completed", default=0,
        validators=[
            NumberRange(min=0, message="Please enter a non-negative number of weeks completed.")
        ]
    )


class NewLeagueSeasonForm(LeagueSeasonForm):
    submit = SubmitField("Create")


class EditLeagueSeasonForm(LeagueSeasonForm):
    submit = SubmitField("Update")


class DeleteLeagueSeasonForm(FlaskForm):
    submit = SubmitField("Delete")
