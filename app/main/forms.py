from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, FileField, SubmitField
from wtforms.validators import DataRequired

class StoryForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    description = TextAreaField('description', validators=[DataRequired()])
    save = SubmitField('save')


class UploadForm(FlaskForm):
    file = FileField('', render_kw={'accept':'.png, .jpg'})
    upload = SubmitField('upload')

    