from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class Form(FlaskForm):


    question = StringField(""" please enter keywords""",
                            validators = [DataRequired()])

    submit = SubmitField('submit')