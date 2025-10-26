from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, StringField, BooleanField
from wtforms.validators import DataRequired, InputRequired, NumberRange, ValidationError, Optional


def team_name_length_check(form, field):
    length_check(field, 50)


def length_check(field, length):
    if len(field.data) > length:
        raise ValidationError(f"{field} must not be longer than {length} characters.")


class GameForm(FlaskForm):
    season_year = IntegerField(
        "Season Year",
        validators=[
            InputRequired("Please enter a year."),
            DataRequired("Please enter a year."),
            NumberRange(min=1920, message="Please enter a year no earlier than 1920.")
        ]
    )
    week = IntegerField(
        "Week",
        validators=[
            InputRequired("Please enter a week."),
            DataRequired("Please enter a week."),
            NumberRange(min=0, message="Please enter a non-negative week value.")
        ]
    )
    guest_name = StringField(
        "Guest Name",
        validators=[
            InputRequired("Please enter a guest name."),
            DataRequired("Please enter a guest name."),
            team_name_length_check,
        ]
    )
    guest_score = IntegerField(
        "Guest Score",
        validators=[
            InputRequired("Please enter a guest score."),
            NumberRange(min=0, message="Please enter a non-negative guest score.")
        ]
    )
    host_name = StringField(
        "Host Name",
        validators=[
            InputRequired("Please enter a host name."),
            DataRequired("Please enter a host name."),
            team_name_length_check,
        ]
    )
    host_score = IntegerField(
        "Host Score",
        validators=[
            InputRequired("Please enter a host score."),
            NumberRange(min=0, message="Please enter a non-negative hose score.")
        ]
    )
    is_playoff = BooleanField(
        "Is Playoff?",
        validators=[]
    )
    notes = StringField(
        "Notes",
        validators=[Optional()]  # Convert empty string to None
    )


class NewGameForm(GameForm):
    submit = SubmitField("Create")


class EditGameForm(GameForm):
    submit = SubmitField("Update")


class DeleteGameForm(FlaskForm):
    submit = SubmitField("Delete")
