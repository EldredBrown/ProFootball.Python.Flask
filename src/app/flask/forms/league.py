from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, StringField
from wtforms.validators import DataRequired, InputRequired, NumberRange, ValidationError


def short_name_length_check(form, field):
    length_check(field, 5)


def long_name_check(form, field):
    length_check(field, 50)


def length_check(field, length):
    if len(field.data) > length:
        raise ValidationError(f"{field} must not be longer than {length} characters.")


class LeagueForm(FlaskForm):
    short_name = StringField(
        "Short Name",
        validators=[
            InputRequired("Please enter a short name."),
            DataRequired("Please enter a short name."),
            short_name_length_check,
        ]
    )
    long_name = StringField(
        "Long Name",
        validators=[
            InputRequired("Please enter a long name."),
            DataRequired("Please enter a long name."),
            long_name_check,
        ]
    )
    first_season_year = IntegerField(
        "First Season",
        validators=[
            InputRequired("Please enter a year."),
            DataRequired("Please enter a year."),
            NumberRange(min=1920, message="Please enter a year no earlier than 1920.")
        ]
    )
    last_season_year = IntegerField(
        "Last Season"
    )


class NewLeagueForm(LeagueForm):
    submit = SubmitField("Create")


class EditLeagueForm(LeagueForm):
    submit = SubmitField("Update")


class DeleteLeagueForm(FlaskForm):
    submit = SubmitField("Delete")
