from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, PasswordField, FileField, SubmitField
from wtforms.validators import DataRequired


class ItemForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    description = TextAreaField('description', validators=[DataRequired()])
    save = SubmitField('save')