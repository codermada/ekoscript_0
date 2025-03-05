from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, FileField, SelectField, SubmitField
from wtforms.validators import DataRequired



class ChapterForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    description = TextAreaField('description', validators=[DataRequired()])
    save = SubmitField('save')


class TextForm(FlaskForm):
    header = SelectField('')
    text = StringField('')
    append = SubmitField('append')
    def __init__(self, headers):
        super().__init__()
        self.header.choices = headers