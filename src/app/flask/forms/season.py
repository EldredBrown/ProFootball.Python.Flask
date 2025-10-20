from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired, InputRequired, NumberRange


class SeasonForm(FlaskForm):
    year = IntegerField(
        "Year",
        validators=[
            InputRequired("Please enter a year (input)."),
            DataRequired("Please enter a year (data)."),
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


class NewSeasonForm(SeasonForm):
    submit = SubmitField("Create")


class EditSeasonForm(SeasonForm):
    submit = SubmitField("Update")


class DeleteSeasonForm(FlaskForm):
    submit = SubmitField("Delete")
