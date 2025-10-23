from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, StringField
from wtforms.validators import DataRequired, InputRequired, NumberRange, ValidationError, Optional


def short_name_length_check(form, field):
    length_check(field, 5)


def long_name_length_check(form, field):
    length_check(field, 50)


def length_check(field, length):
    if len(field.data) > length:
        raise ValidationError(f"{field} must not be longer than {length} characters.")


class DivisionForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[
            InputRequired("Please enter a name."),
            DataRequired("Please enter a name."),
            long_name_length_check,
        ]
    )
    league_name = StringField(
        "League Name",
        validators=[
            InputRequired("Please enter a league name."),
            DataRequired("Please enter a league name."),
            short_name_length_check,
        ]
    )
    conference_name = StringField(
        "Conference Name",
        validators=[Optional()],
        filters=[lambda x: x or None]  # Convert empty string to None
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
        "Last Season",
        validators=[Optional()],
        filters=[lambda x: x or None]  # Convert empty string to None
    )


class NewDivisionForm(DivisionForm):
    submit = SubmitField("Create")


class EditDivisionForm(DivisionForm):
    submit = SubmitField("Update")


class DeleteDivisionForm(FlaskForm):
    submit = SubmitField("Delete")
