from flask_wtf import FlaskForm
from wtforms import TextField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class GroupInputForm(FlaskForm):
    generators = TextAreaField('Generators', validators=[DataRequired()])
    relation = TextAreaField('Relation')
    submit = SubmitField('Break down')
