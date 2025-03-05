from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, FileField, SubmitField
from wtforms.validators import DataRequired



class IllustrationForm(FlaskForm):
    description = StringField('description', validators=[DataRequired()])
    file = FileField('', render_kw={'accept':'.png, .jpg'})
    upload = SubmitField('upload')