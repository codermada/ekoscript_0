from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, PasswordField, FileField, SubmitField
from wtforms.validators import DataRequired


class CharacterForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    birthday = DateField('birthday', validators=[DataRequired()])
    description = TextAreaField('description', validators=[DataRequired()])
    save = SubmitField('save')