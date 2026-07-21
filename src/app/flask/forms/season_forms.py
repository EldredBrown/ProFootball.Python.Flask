from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired, InputRequired, NumberRange


class SeasonForm(FlaskForm):
    year = IntegerField(
        "Year",
        validators=[
            InputRequired("Please enter a year."),
            DataRequired("Please enter a year."),
            NumberRange(min=1920, message="Please enter a year no earlier than 1920.")
        ]
    )


class NewSeasonForm(SeasonForm):
    submit = SubmitField("Create")


class EditSeasonForm(SeasonForm):
    submit = SubmitField("Update")


class DeleteSeasonForm(FlaskForm):
    submit = SubmitField("Delete")
