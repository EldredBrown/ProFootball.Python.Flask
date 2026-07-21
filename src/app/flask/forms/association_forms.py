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


class AssociationForm(FlaskForm):
    long_name = StringField(
        "Long Name",
        validators=[
            InputRequired("Please enter a long name."),
            DataRequired("Please enter a long name."),
            long_name_length_check,
        ]
    )
    short_name = StringField(
        "Short Name",
        validators=[
            InputRequired("Please enter a short name."),
            DataRequired("Please enter a short name."),
            short_name_length_check,
        ]
    )
    parent_name = StringField(
        "Parent Name",
        validators=[Optional()],
        filters=[lambda x: x or None]
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


class NewAssociationForm(AssociationForm):
    submit = SubmitField("Create")


class EditAssociationForm(AssociationForm):
    submit = SubmitField("Update")


class DeleteAssociationForm(FlaskForm):
    submit = SubmitField("Delete")
