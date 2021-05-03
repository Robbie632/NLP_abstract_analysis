from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import DataRequired


class Form(FlaskForm):


    question = StringField(""" please enter keywords""",
                            validators = [DataRequired()])

    clusters = RadioField("number of clusters", choices=[("2", "2 cluster"),
                                                         ("3", "3 clusters"),
                                                         ("4", "4 clusters"),
                                                         ("5", "5 clusters"),
                                                         ("6", "6 clusters"),
                                                         ("7", "7 clusters")
                                                        ])
    abstracts = StringField("number of abstracts", validators = [DataRequired()]) 

    submit = SubmitField('submit')