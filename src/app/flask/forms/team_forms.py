from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, StringField
from wtforms.validators import DataRequired, InputRequired, NumberRange, ValidationError, Optional


def name_length_check(form, field):
    length_check(field, 50)


def length_check(field, length):
    if len(field.data) > length:
        raise ValidationError(f"{field} must not be longer than {length} characters.")


class TeamForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[
            InputRequired("Please enter a name."),
            DataRequired("Please enter a name."),
            name_length_check,
        ]
    )


class NewTeamForm(TeamForm):
    submit = SubmitField("Create")


class EditTeamForm(TeamForm):
    submit = SubmitField("Update")


class DeleteTeamForm(FlaskForm):
    submit = SubmitField("Delete")
