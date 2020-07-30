from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class InputForm(FlaskForm):
    group = StringField('Group', validators=[DataRequired()])
    submit = SubmitField('Break down')
